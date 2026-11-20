# Bảng duyệt câu hỏi: Xác Suất và Thống Kê

Tạo bởi `python tools/math_review.py`. Đánh dấu đã duyệt bằng `"reviewed": true` trong `server/data/math/items/xac_suat_thong_ke.json`.

## Tầng 1: Phép thử, sự kiện và giải tích kết hợp

46 dạng câu (37 câu viết tay, 9 bộ sinh câu); 46 chưa duyệt.

### Phép thử và không gian mẫu (`xs_t1_khong_gian_mau`)

- `xs_t1_kg_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt và ghi số chấm xuất hiện. Không gian mẫu của phép thử này có 6 phần tử.
  - **Đáp án:** Đúng
    1. Một kết quả là số chấm của mặt trên: 1, 2, 3, 4, 5 hoặc 6.
    2. Không gian mẫu là {1, 2, 3, 4, 5, 6}, có 6 phần tử.
- `xs_t1_kg_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu hai lần liên tiếp và ghi mặt xuất hiện theo thứ tự lần tung (S là sấp, N là ngửa). Không gian mẫu là tập nào?
    - **(đúng)** {SS, SN, NS, NN}
    - {SS, SN, NN}
    - {S, N}
    - {SN, NS}
  - **Đáp án:** {SS, SN, NS, NN}
    1. Mỗi kết quả ghi hai mặt theo thứ tự: mặt của lần 1 rồi mặt của lần 2.
    2. Lần 1 có 2 khả năng, lần 2 có 2 khả năng, nên có 4 kết quả.
    3. SN (lần 1 sấp, lần 2 ngửa) và NS là hai kết quả khác nhau, nên không được gộp: không gian mẫu là {SS, SN, NS, NN}.
- `xs_t1_kg_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 viên bi đánh số 1, 2, 3. Lấy lần lượt 2 viên, không trả viên thứ nhất vào hộp, và ghi số theo thứ tự lấy. Không gian mẫu có bao nhiêu phần tử?
  - **Đáp án:** 6
    1. Một kết quả là cặp có thứ tự (số lần 1, số lần 2) gồm hai số khác nhau.
    2. Liệt kê: (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2).
    3. Có 3 . 2 = 6 phần tử.
- `xs_t1_kg_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phép thử với số phần tử của không gian mẫu (các đồng xu, xúc xắc phân biệt được với nhau, ghi mặt của từng cái).
  - **Đáp án (ghép đúng):**
    - Tung một đồng xu — 2
    - Gieo một xúc xắc sáu mặt — 6
    - Tung hai đồng xu — 4
    - Gieo hai xúc xắc sáu mặt — 36
  - **Lời giải:**
    1. Một đồng xu có 2 mặt, một xúc xắc có 6 mặt.
    2. Với hai đồng xu, mỗi kết quả là một cặp mặt: 2 . 2 = 4.
    3. Với hai xúc xắc, mỗi kết quả là một cặp số chấm: 6 . 6 = 36.
- `xs_g1_khong_gian_mau` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tung 2 đồng xu, các đồng xu đều phân biệt được với nhau. Một kết quả ghi mặt của từng đồng xu. Không gian mẫu có bao nhiêu phần tử?
  - **Đáp án:** 4
    1. Một kết quả chọn đồng thời mặt của mọi đồng xu và mọi xúc xắc, nên dùng quy tắc nhân.
    2. Mỗi đồng xu có 2 mặt: 2 đồng xu cho 2^2 = 4 khả năng.
    3. Không gian mẫu có 4 phần tử.
  - **Câu hỏi:** Gieo 2 con xúc xắc sáu mặt, các xúc xắc đều phân biệt được với nhau. Một kết quả ghi số chấm của từng xúc xắc. Không gian mẫu có bao nhiêu phần tử?
  - **Đáp án:** 36
    1. Một kết quả chọn đồng thời mặt của mọi đồng xu và mọi xúc xắc, nên dùng quy tắc nhân.
    2. Mỗi xúc xắc có 6 mặt: 2 xúc xắc cho 6^2 = 36 khả năng.
    3. Không gian mẫu có 36 phần tử.
  - **Câu hỏi:** Tung 1 đồng xu và gieo 1 con xúc xắc sáu mặt, mọi đồng xu và xúc xắc đều phân biệt được với nhau. Một kết quả ghi mặt của từng đồng xu và số chấm của từng xúc xắc. Không gian mẫu có bao nhiêu phần tử?
  - **Đáp án:** 12
    1. Một kết quả chọn đồng thời mặt của mọi đồng xu và mọi xúc xắc, nên dùng quy tắc nhân.
    2. Mỗi đồng xu có 2 mặt: 1 đồng xu cho 2^1 = 2 khả năng.
    3. Mỗi xúc xắc có 6 mặt: 1 xúc xắc cho 6^1 = 6 khả năng.
    4. Không gian mẫu có 12 phần tử.
- `xs_t1_kg_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối và chỉ ghi tổng số chấm. Mười một giá trị tổng từ 2 đến 12 là mười một kết quả đồng khả năng.
  - **Đáp án:** Sai
    1. Các kết quả đồng khả năng là 36 cặp (số chấm xúc xắc 1, số chấm xúc xắc 2).
    2. Tổng 2 chỉ đến từ cặp (1, 1), còn tổng 7 đến từ 6 cặp: (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1).
    3. Vậy các giá trị tổng không đồng khả năng: tổng 7 dễ ra gấp 6 lần tổng 2.
- `xs_t1_kg_06` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt rồi tung một đồng xu. Mỗi kết quả là một cặp (số chấm, mặt đồng xu). Có bao nhiêu kết quả mà số chấm là số chẵn và đồng xu ra mặt ngửa?
  - **Đáp án:** 3
    1. Không gian mẫu có 6 . 2 = 12 cặp.
    2. Số chấm chẵn có 3 khả năng: 2, 4, 6; mặt ngửa có 1 khả năng.
    3. Có 3 . 1 = 3 kết quả: (2, N), (4, N), (6, N).
- `xs_t1_kg_07` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 5 viên bi đánh số 1 đến 5. Lấy lần lượt 2 viên không hoàn lại và ghi số theo thứ tự lấy. Sắp xếp các bước đếm số phần tử của không gian mẫu.
  - **Đáp án (thứ tự đúng):**
    1. Xác định một kết quả là gì: cặp có thứ tự (số bi lần 1, số bi lần 2).
    2. Lần 1 có 5 cách lấy.
    3. Bi lần 1 không được trả lại, nên ứng với mỗi cách lấy lần 1, lần 2 chỉ còn 4 cách.
    4. Theo quy tắc nhân, không gian mẫu có 5 . 4 = 20 phần tử.
  - **Lời giải:**
    1. Trước hết phải nói rõ một kết quả là cặp có thứ tự, vì đề ghi số theo thứ tự lấy.
    2. Đếm từng bước: lần 1 có 5 cách, lần 2 còn 4 cách vì không hoàn lại.
    3. Nhân lại được 20 phần tử.
- `xs_t1_kg_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung ba đồng xu phân biệt, ghi mặt của từng đồng xu. Đếm số phần tử của không gian mẫu. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi kết quả là một bộ ba (mặt đồng xu 1, mặt đồng xu 2, mặt đồng xu 3).
    2. Mỗi đồng xu có 2 mặt.
    3. Số kết quả là 2 + 2 + 2 = 6.   **<- bước sai đầu tiên**
    4. Vậy không gian mẫu có 6 phần tử.
  - **Đáp án:** Bước 3: Số kết quả là 2 + 2 + 2 = 6.
  - **Vì sao sai, và bước đúng:**
    1. Một kết quả chọn cùng lúc mặt của cả ba đồng xu, đó là ba bước nối tiếp, nên phải nhân chứ không cộng.
    2. Đúng là 2 . 2 . 2 = 8 phần tử: SSS, SSN, SNS, SNN, NSS, NSN, NNS, NNN.

### Quan hệ giữa các sự kiện (`xs_t1_quan_he_su_kien`)

- `xs_t1_qh_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc. A là sự kiện ra mặt có số chấm chẵn, B là sự kiện ra mặt có số chấm lẻ. A và B là hai sự kiện xung khắc.
  - **Đáp án:** Đúng
    1. Hai sự kiện xung khắc khi chúng không thể cùng xảy ra, tức là không có kết quả chung.
    2. A = {2, 4, 6}, B = {1, 3, 5} không có phần tử chung.
    3. Vậy A và B xung khắc.
- `xs_t1_qh_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc. A là sự kiện ra mặt có số chấm chẵn. Sự kiện đối Ā của A là sự kiện nào?
    - **(đúng)** Ra mặt có số chấm lẻ
    - Ra mặt 1 chấm
    - Ra mặt có số chấm lớn hơn 3
    - Không ra mặt nào cả
  - **Đáp án:** Ra mặt có số chấm lẻ
    1. Sự kiện đối Ā xảy ra đúng khi A không xảy ra.
    2. A = {2, 4, 6}, nên Ā gồm các kết quả còn lại: {1, 3, 5}.
    3. Đó là sự kiện ra mặt có số chấm lẻ.
- `xs_t1_qh_03` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc. A: ra mặt chẵn, A = {2, 4, 6}. B: ra mặt lớn hơn 3, B = {4, 5, 6}. Ghép mỗi sự kiện với tập kết quả của nó.
  - **Đáp án (ghép đúng):**
    - A + B (A hoặc B xảy ra) — {2, 4, 5, 6}
    - AB (A và B cùng xảy ra) — {4, 6}
    - Ā (A không xảy ra) — {1, 3, 5}
    - A xảy ra nhưng B không xảy ra — {2}
  - **Lời giải:**
    1. Tổng A + B gom mọi kết quả thuộc A hoặc thuộc B: {2, 4, 5, 6}.
    2. Tích AB lấy các kết quả thuộc cả hai: {4, 6}.
    3. Ā là phần còn lại của {1, 2, 3, 4, 5, 6} sau khi bỏ A: {1, 3, 5}.
    4. A xảy ra mà B không: thuộc A nhưng không thuộc B, chỉ còn {2}.
- `xs_t1_qh_04` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung hai đồng xu phân biệt (S là sấp, N là ngửa, ghi mặt đồng xu 1 trước). A: đồng xu thứ nhất ra ngửa. B: có đúng một đồng xu ra ngửa. Sự kiện A + B gồm bao nhiêu kết quả?
  - **Đáp án:** 3
    1. Không gian mẫu: {SS, SN, NS, NN}.
    2. A = {NS, NN} và B = {SN, NS}.
    3. A + B gom các kết quả thuộc A hoặc B, mỗi kết quả tính một lần: {NS, NN, SN}, có 3 kết quả.
- `xs_g1_su_kien` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt. A là sự kiện số chấm chia hết cho 3, B là sự kiện số chấm lớn hơn 4. Liệt kê các kết quả (số chấm) của sự kiện AB (A và B cùng xảy ra).
  - **Đáp án:** 6  (thứ tự nào cũng được)
    1. A = {3, 6} và B = {5, 6}.
    2. AB gồm các kết quả thuộc cả A và B.
    3. Sự kiện cần tìm là {6}.
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt. A là sự kiện số chấm là số chẵn, B là sự kiện số chấm lớn hơn 2. Liệt kê các kết quả (số chấm) của sự kiện A + B (ít nhất một trong hai sự kiện xảy ra).
  - **Đáp án:** 2, 3, 4, 5, 6  (thứ tự nào cũng được)
    1. A = {2, 4, 6} và B = {3, 4, 5, 6}.
    2. A + B gồm các kết quả thuộc A hoặc thuộc B.
    3. Sự kiện cần tìm là {2, 3, 4, 5, 6}.
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt. A là sự kiện số chấm chia hết cho 3, B là sự kiện số chấm lớn hơn 4. Liệt kê các kết quả (số chấm) của sự kiện A + B (ít nhất một trong hai sự kiện xảy ra).
  - **Đáp án:** 3, 5, 6  (thứ tự nào cũng được)
    1. A = {3, 6} và B = {5, 6}.
    2. A + B gồm các kết quả thuộc A hoặc thuộc B.
    3. Sự kiện cần tìm là {3, 5, 6}.
- `xs_t1_qh_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai sự kiện xung khắc A và B, trong đó B không phải là sự kiện không thể, sự kiện đối Ā cũng xung khắc với B.
  - **Đáp án:** Sai
    1. A và B xung khắc nên khi B xảy ra thì A không xảy ra, tức là B kéo theo Ā.
    2. Vì vậy ĀB = B, mà B không phải sự kiện không thể nên Ā và B có thể cùng xảy ra.
    3. Ví dụ gieo xúc xắc, A = {1}, B = {2}: Ā = {2, 3, 4, 5, 6} chứa cả 2, nên Ā và B không xung khắc. Mệnh đề sai.
- `xs_t1_qh_06` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc. A: ra mặt 6. B: ra mặt có số chấm chẵn. Khẳng định nào đúng?
    - **(đúng)** A kéo theo B
    - B kéo theo A
    - A và B xung khắc
    - A và B là hai sự kiện đối nhau
  - **Đáp án:** A kéo theo B
    1. A kéo theo B nghĩa là hễ A xảy ra thì B cũng xảy ra, tức mọi kết quả của A đều thuộc B.
    2. A = {6} và 6 thuộc B = {2, 4, 6}, nên A kéo theo B.
    3. Ngược lại thì không: ra mặt 2 thì B xảy ra mà A không. A và B có chung kết quả 6 nên cũng không xung khắc.
- `xs_t1_qh_07` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung ba đồng xu phân biệt và ghi mặt của từng đồng xu. A là sự kiện có ít nhất một đồng xu ra mặt ngửa. Sự kiện đối Ā gồm bao nhiêu kết quả?
  - **Đáp án:** 1
    1. Ā xảy ra khi A không xảy ra: không có đồng xu nào ra ngửa.
    2. Tức là cả ba đồng xu đều ra sấp: chỉ có kết quả SSS.
    3. Ā có 1 kết quả, còn A có 8 - 1 = 7 kết quả.
- `xs_t1_qh_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Gieo một con xúc xắc. A = {1, 2, 3}, B = {2, 4, 6}. Tìm sự kiện đối của A + B. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ā gồm các kết quả không thuộc A: Ā = {4, 5, 6}.
    2. Sự kiện đối của B là {1, 3, 5}.
    3. Sự kiện đối của A + B bằng tổng của hai sự kiện đối: {4, 5, 6} + {1, 3, 5}.   **<- bước sai đầu tiên**
    4. Vậy sự kiện đối của A + B là {1, 3, 4, 5, 6}.
  - **Đáp án:** Bước 3: Sự kiện đối của A + B bằng tổng của hai sự kiện đối: {4, 5, 6} + {1, 3, 5}.
  - **Vì sao sai, và bước đúng:**
    1. 'A + B không xảy ra' nghĩa là A không xảy ra và B cũng không xảy ra: phải lấy tích của hai sự kiện đối, không lấy tổng.
    2. Tích của {4, 5, 6} và {1, 3, 5} là {5}.
    3. Kiểm tra lại: A + B = {1, 2, 3, 4, 6}, phần còn lại đúng là {5}.

### Quy tắc cộng và quy tắc nhân (`xs_t1_quy_tac_dem`)

- `xs_t1_qd_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ thành phố X đến thành phố Y có 3 chuyến tàu và 2 chuyến bay, các chuyến đều khác nhau. Một người chọn đúng một chuyến để đi. Số cách chọn là 3 . 2 = 6.
  - **Đáp án:** Sai
    1. Người đó đi tàu hoặc đi máy bay, chỉ chọn một chuyến: đây là các phương án loại trừ nhau, dùng quy tắc cộng.
    2. Số cách là 3 + 2 = 5, không phải 6.
    3. Quy tắc nhân chỉ dùng khi phải làm nhiều bước nối tiếp, ví dụ đi tàu rồi lại bay tiếp.
- `xs_t1_qd_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bạn có 4 chiếc áo khác nhau và 3 chiếc quần khác nhau. Mỗi bộ trang phục gồm 1 áo và 1 quần. Có bao nhiêu bộ trang phục khác nhau?
    - **(đúng)** 12
    - 7
    - 64
    - 81
  - **Đáp án:** 12
    1. Chọn một bộ gồm hai bước nối tiếp: chọn áo, rồi chọn quần.
    2. Có 4 cách chọn áo, và với mỗi áo có 3 cách chọn quần.
    3. Theo quy tắc nhân: 4 . 3 = 12 bộ.
- `xs_t1_qd_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một biển hiệu gồm 2 chữ cái rồi đến 1 chữ số. Mỗi chữ cái chọn trong 26 chữ cái (được lặp lại), chữ số chọn từ 0 đến 9. Có bao nhiêu biển hiệu khác nhau?
  - **Đáp án:** 6760
    1. Lập biển hiệu gồm ba bước: chữ cái thứ nhất, chữ cái thứ hai, chữ số.
    2. Hai chữ cái được lặp nên mỗi vị trí có 26 cách; chữ số có 10 cách.
    3. Theo quy tắc nhân: 26 . 26 . 10 = 6760.
- `xs_t1_qd_07` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bữa ăn gồm 1 món chính chọn trong 4 món và 1 đồ uống chọn trong 3 loại. Sắp xếp các bước đếm số cách chọn bữa ăn.
  - **Đáp án (thứ tự đúng):**
    1. Nhận ra chọn bữa ăn gồm hai bước nối tiếp: chọn món chính, rồi chọn đồ uống.
    2. Bước chọn món chính có 4 cách.
    3. Ứng với mỗi món chính đã chọn, bước chọn đồ uống có 3 cách.
    4. Theo quy tắc nhân, có 4 . 3 = 12 cách.
  - **Lời giải:**
    1. Việc phải làm qua hai bước liên tiếp thì dùng quy tắc nhân.
    2. Đếm số cách của từng bước: 4 và 3.
    3. Nhân lại: 12 cách.
- `xs_g1_thuc_don` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một quán có 3 món khai vị, 6 món chính và 2 món tráng miệng, các món đều khác nhau. Một suất ăn gồm đúng 1 món khai vị, 1 món chính và 1 món tráng miệng. Có bao nhiêu suất ăn khác nhau?
  - **Đáp án:** 36
    1. Chọn suất ăn gồm ba bước nối tiếp: chọn khai vị, chọn món chính, chọn tráng miệng.
    2. Các bước có lần lượt 3, 6 và 2 cách, bước sau không phụ thuộc bước trước.
    3. Theo quy tắc nhân: 3 . 6 . 2 = 36 suất ăn.
  - **Câu hỏi:** Một quán có 2 món khai vị, 2 món chính và 2 món tráng miệng, các món đều khác nhau. Một suất ăn gồm đúng 1 món khai vị, 1 món chính và 1 món tráng miệng. Có bao nhiêu suất ăn khác nhau?
  - **Đáp án:** 8
    1. Chọn suất ăn gồm ba bước nối tiếp: chọn khai vị, chọn món chính, chọn tráng miệng.
    2. Các bước có lần lượt 2, 2 và 2 cách, bước sau không phụ thuộc bước trước.
    3. Theo quy tắc nhân: 2 . 2 . 2 = 8 suất ăn.
  - **Câu hỏi:** Một quán có 3 món khai vị, 6 món chính và 3 món tráng miệng, các món đều khác nhau. Một suất ăn gồm đúng 1 món khai vị, 1 món chính và 1 món tráng miệng. Có bao nhiêu suất ăn khác nhau?
  - **Đáp án:** 54
    1. Chọn suất ăn gồm ba bước nối tiếp: chọn khai vị, chọn món chính, chọn tráng miệng.
    2. Các bước có lần lượt 3, 6 và 3 cách, bước sau không phụ thuộc bước trước.
    3. Theo quy tắc nhân: 3 . 6 . 3 = 54 suất ăn.
- `xs_t1_qd_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số tự nhiên có 3 chữ số đôi một khác nhau được lập từ các chữ số 0, 1, 2, 3, 4?
  - **Đáp án:** 48
    1. Chữ số hàng trăm phải khác 0: có 4 cách (1, 2, 3, 4).
    2. Chữ số hàng chục khác chữ số hàng trăm, được là 0: còn 4 cách.
    3. Chữ số hàng đơn vị khác hai chữ số trước: còn 3 cách.
    4. Theo quy tắc nhân: 4 . 4 . 3 = 48 số.
- `xs_t1_qd_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có đúng 9 . 5 = 45 số tự nhiên chẵn có hai chữ số.
  - **Đáp án:** Đúng
    1. Chữ số hàng chục từ 1 đến 9: 9 cách.
    2. Chữ số hàng đơn vị phải chẵn: 0, 2, 4, 6, 8, có 5 cách.
    3. Quy tắc nhân cho 9 . 5 = 45; kiểm tra lại: các số chẵn từ 10 đến 98 có (98 - 10)/2 + 1 = 45 số. Mệnh đề đúng.
- `xs_t1_qd_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Có bao nhiêu số tự nhiên có 3 chữ số đôi một khác nhau được lập từ các chữ số 0, 1, 2, 3, 4, 5? Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Một số như vậy là bộ (chữ số hàng trăm, hàng chục, hàng đơn vị) gồm ba chữ số khác nhau.
    2. Chữ số hàng trăm có 6 cách chọn.   **<- bước sai đầu tiên**
    3. Chữ số hàng chục có 5 cách, chữ số hàng đơn vị có 4 cách.
    4. Vậy có 6 . 5 . 4 = 120 số.
  - **Đáp án:** Bước 2: Chữ số hàng trăm có 6 cách chọn.
  - **Vì sao sai, và bước đúng:**
    1. Chữ số hàng trăm của một số có 3 chữ số không được là 0, nên chỉ có 5 cách.
    2. Sau đó hàng chục còn 5 cách (được dùng 0), hàng đơn vị còn 4 cách.
    3. Đáp số đúng: 5 . 5 . 4 = 100 số.
- `xs_g1_ma_so` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một mã số gồm 4 chữ số, mỗi chữ số lấy trong các chữ số từ 1 đến 4 và được phép lặp lại. Có bao nhiêu mã số như vậy?
  - **Đáp án:** 256
    1. Lập mã là chọn lần lượt từng chữ số, từ trái sang phải.
    2. Mỗi vị trí có 4 cách chọn, vì được lặp lại.
    3. Theo quy tắc nhân: 4^4 = 256 mã.
  - **Câu hỏi:** Một mã số gồm 2 chữ số, mỗi chữ số lấy trong các chữ số từ 1 đến 9 và được phép lặp lại. Có bao nhiêu mã số như vậy?
  - **Đáp án:** 81
    1. Lập mã là chọn lần lượt từng chữ số, từ trái sang phải.
    2. Mỗi vị trí có 9 cách chọn, vì được lặp lại.
    3. Theo quy tắc nhân: 9^2 = 81 mã.
  - **Câu hỏi:** Một mã số gồm 4 chữ số, mỗi chữ số lấy trong các chữ số từ 1 đến 4 và được phép lặp lại. Có bao nhiêu mã số như vậy?
  - **Đáp án:** 256
    1. Lập mã là chọn lần lượt từng chữ số, từ trái sang phải.
    2. Mỗi vị trí có 4 cách chọn, vì được lặp lại.
    3. Theo quy tắc nhân: 4^4 = 256 mã.

### Hoán vị và chỉnh hợp (`xs_t1_hoan_vi_chinh_hop`)

- `xs_t1_hv_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có 5! = 120 cách xếp 5 bạn ngồi vào một hàng ghế có đúng 5 chỗ.
  - **Đáp án:** Đúng
    1. Ghế 1 có 5 cách chọn người, ghế 2 còn 4 cách, ghế 3 còn 3, ghế 4 còn 2, ghế 5 còn 1.
    2. Số cách là 5 . 4 . 3 . 2 . 1 = 5! = 120. Mệnh đề đúng.
- `xs_t1_hv_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lớp có 30 học sinh. Bầu 1 lớp trưởng và 1 lớp phó, hai người khác nhau. Số cách bầu là bao nhiêu?
    - **(đúng)** A(30, 2) = 870
    - C(30, 2) = 435
    - 30^2 = 900
    - 30 + 29 = 59
  - **Đáp án:** A(30, 2) = 870
    1. Hai chức vụ khác nhau: An làm lớp trưởng, Bình làm lớp phó khác với Bình làm lớp trưởng, An làm lớp phó. Thứ tự có ý nghĩa.
    2. Lớp trưởng có 30 cách, lớp phó còn 29 cách.
    3. Số cách là A(30, 2) = 30 . 29 = 870.
- `xs_t1_hv_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu cách xếp 4 cuốn sách khác nhau thành một hàng trên ngăn kệ?
  - **Đáp án:** 24
    1. Mỗi cách xếp là một hoán vị của 4 cuốn sách.
    2. Số hoán vị là 4! = 4 . 3 . 2 . 1 = 24.
- `xs_g1_hoan_vi` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu cách xếp 4 bạn thành một hàng dọc?
  - **Đáp án:** 24
    1. Mỗi cách xếp là một hoán vị của các bạn.
    2. Số hoán vị của 4 phần tử là 4! = 24.
  - **Câu hỏi:** Có bao nhiêu cách xếp 3 bạn, trong đó có Lan, thành một hàng dọc sao cho Lan đứng đầu hàng?
  - **Đáp án:** 2
    1. Vị trí đầu hàng đã là của Lan, chỉ còn xếp các bạn khác.
    2. 2 bạn còn lại xếp vào 2 chỗ còn lại: 2! = 2 cách.
  - **Câu hỏi:** Có bao nhiêu cách xếp 4 bạn thành một hàng dọc?
  - **Đáp án:** 24
    1. Mỗi cách xếp là một hoán vị của các bạn.
    2. Số hoán vị của 4 phần tử là 4! = 24.
- `xs_t1_hv_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp 5 người A, B, C, D, E thành một hàng ngang sao cho A và B đứng cạnh nhau. Có bao nhiêu cách?
  - **Đáp án:** 48
    1. Buộc A và B thành một khối. Khối này cùng C, D, E là 4 phần tử xếp thành hàng: 4! = 24 cách.
    2. Trong khối, A và B đổi chỗ được: 2 cách (AB hoặc BA).
    3. Số cách là 24 . 2 = 48.
- `xs_t1_hv_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số chỉnh hợp chập 2 của 6 phần tử, A(6, 2), bằng số tổ hợp chập 2 của 6 phần tử, C(6, 2).
  - **Đáp án:** Sai
    1. A(6, 2) = 6 . 5 = 30 đếm các cặp có thứ tự.
    2. C(6, 2) = 30 / 2! = 15 đếm các nhóm hai phần tử không kể thứ tự.
    3. Mỗi nhóm {x, y} cho hai chỉnh hợp (x, y) và (y, x), nên A(6, 2) = 2 . C(6, 2). Mệnh đề sai.
- `xs_t1_hv_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước đếm số cách xếp 6 người thành một hàng sao cho hai người X và Y không đứng cạnh nhau.
  - **Đáp án (thứ tự đúng):**
    1. Coi X và Y là một khối; khối này cùng 4 người còn lại xếp được 5! = 120 cách.
    2. Trong khối, X và Y đổi chỗ được 2 cách, nên có 120 . 2 = 240 cách xếp mà hai người đứng cạnh nhau.
    3. Số cách xếp 6 người tùy ý là 6! = 720, trong đó có 240 cách vừa đếm là cách không hợp lệ.
    4. Bỏ các cách không hợp lệ: 720 - 240 = 480 cách X và Y không đứng cạnh nhau.
  - **Lời giải:**
    1. Đếm thẳng các cách 'không cạnh nhau' khó, nên đếm phần ngược lại: các cách X, Y đứng cạnh nhau.
    2. Cạnh nhau: buộc thành khối (5! cách) rồi đổi chỗ trong khối (2 cách): 240.
    3. Lấy tất cả trừ đi: 720 - 240 = 480.
- `xs_t1_hv_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chọn 3 trong 7 vận động viên để trao huy chương vàng, bạc, đồng (mỗi người nhiều nhất một huy chương). Có bao nhiêu cách? Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ba huy chương khác nhau nên đổi huy chương giữa hai người là một cách trao khác.
    2. Huy chương vàng có 7 cách trao.
    3. Huy chương bạc còn 6 cách, huy chương đồng còn 5 cách.
    4. Vì thứ tự không quan trọng, chia cho 3! = 6: được 7 . 6 . 5 / 6 = 35 cách.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vì thứ tự không quan trọng, chia cho 3! = 6: được 7 . 6 . 5 / 6 = 35 cách.
  - **Vì sao sai, và bước đúng:**
    1. Bước đầu đã nói đúng: các huy chương khác nhau nên thứ tự có ý nghĩa. Không được chia cho 3!.
    2. Chia cho 3! chỉ đúng khi chọn một nhóm 3 người không phân biệt vai trò.
    3. Đáp số đúng là chỉnh hợp A(7, 3) = 7 . 6 . 5 = 210 cách.
- `xs_g1_chinh_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một nhóm có 7 người. Chọn ra một trưởng nhóm, một phó nhóm, một thư ký và một thủ quỹ, mỗi người giữ nhiều nhất một chức vụ. Có bao nhiêu cách chọn?
  - **Đáp án:** 840
    1. Các chức vụ khác nhau, nên đổi chỗ hai người là một cách chọn khác: thứ tự có ý nghĩa.
    2. Đây là chỉnh hợp chập 4 của 7: chức vụ đầu có 7 cách, mỗi chức vụ sau ít đi một cách.
    3. A(7, 4) = 7 . 6 . 5 . 4 = 840.
  - **Câu hỏi:** Một nhóm có 5 người. Chọn ra một trưởng nhóm và một phó nhóm, mỗi người giữ nhiều nhất một chức vụ. Có bao nhiêu cách chọn?
  - **Đáp án:** 20
    1. Các chức vụ khác nhau, nên đổi chỗ hai người là một cách chọn khác: thứ tự có ý nghĩa.
    2. Đây là chỉnh hợp chập 2 của 5: chức vụ đầu có 5 cách, mỗi chức vụ sau ít đi một cách.
    3. A(5, 2) = 5 . 4 = 20.
  - **Câu hỏi:** Một nhóm có 8 người. Chọn ra một trưởng nhóm, một phó nhóm, một thư ký và một thủ quỹ, mỗi người giữ nhiều nhất một chức vụ. Có bao nhiêu cách chọn?
  - **Đáp án:** 1680
    1. Các chức vụ khác nhau, nên đổi chỗ hai người là một cách chọn khác: thứ tự có ý nghĩa.
    2. Đây là chỉnh hợp chập 4 của 8: chức vụ đầu có 8 cách, mỗi chức vụ sau ít đi một cách.
    3. A(8, 4) = 8 . 7 . 6 . 5 = 1680.

### Tổ hợp (`xs_t1_to_hop`)

- `xs_t1_th_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có 10 cách chọn 2 bạn trong 5 bạn để cùng đi trực nhật.
  - **Đáp án:** Đúng
    1. Hai bạn làm cùng một việc nên không kể thứ tự: đây là tổ hợp chập 2 của 5.
    2. C(5, 2) = (5 . 4)/2 = 10. Mệnh đề đúng.
- `xs_t1_th_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Việc đếm nào sau đây dùng tổ hợp (chọn không kể thứ tự)?
    - **(đúng)** Chọn 3 bạn vào đội văn nghệ
    - Xếp 3 bạn vào 3 ghế đánh số 1, 2, 3
    - Bầu lớp trưởng, lớp phó và bí thư trong 10 bạn
    - Lập một số có 3 chữ số khác nhau
  - **Đáp án:** Chọn 3 bạn vào đội văn nghệ
    1. Tổ hợp dùng khi chỉ quan tâm nhóm gồm những ai, đổi thứ tự không cho cách mới.
    2. Đội văn nghệ không phân vai, nên chọn {An, Bình, Chi} hay {Chi, An, Bình} là một.
    3. Ba việc còn lại đều có thứ tự: ghế đánh số, chức vụ khác nhau, vị trí chữ số trong số.
- `xs_t1_th_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên mặt phẳng có 6 điểm, không có 3 điểm nào thẳng hàng. Có bao nhiêu đoạn thẳng có hai đầu mút là hai trong 6 điểm đó?
  - **Đáp án:** 15
    1. Một đoạn thẳng được xác định bởi hai đầu mút, và đoạn PQ cũng là đoạn QP: không kể thứ tự.
    2. Số đoạn thẳng là C(6, 2) = (6 . 5)/2 = 15.
- `xs_t1_th_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi số đếm với giá trị của nó (C là tổ hợp, A là chỉnh hợp).
  - **Đáp án (ghép đúng):**
    - C(6, 2) — 15
    - A(6, 2) — 30
    - 6^2 — 36
    - 3! — 6
  - **Lời giải:**
    1. C(6, 2) = (6 . 5)/2 = 15: chọn 2 trong 6, không kể thứ tự.
    2. A(6, 2) = 6 . 5 = 30: chọn 2 trong 6, có thứ tự.
    3. 6^2 = 36: chọn 2 lần trong 6, được lặp lại.
    4. 3! = 3 . 2 . 1 = 6.
- `xs_g1_to_hop` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một tổ có 7 bạn. Chọn 4 bạn đi trực nhật cùng nhau (không phân công việc riêng). Có bao nhiêu cách chọn?
  - **Đáp án:** 35
    1. Các bạn được chọn làm cùng một việc, nên chỉ quan tâm nhóm gồm những ai: không kể thứ tự.
    2. Đây là tổ hợp chập 4 của 7: C(7, 4) = A(7, 4) / 4!.
    3. C(7, 4) = 840 / 24 = 35.
  - **Câu hỏi:** Một tổ có 5 bạn. Chọn 2 bạn đi trực nhật cùng nhau (không phân công việc riêng). Có bao nhiêu cách chọn?
  - **Đáp án:** 10
    1. Các bạn được chọn làm cùng một việc, nên chỉ quan tâm nhóm gồm những ai: không kể thứ tự.
    2. Đây là tổ hợp chập 2 của 5: C(5, 2) = A(5, 2) / 2!.
    3. C(5, 2) = 20 / 2 = 10.
  - **Câu hỏi:** Một tổ có 8 bạn. Chọn 4 bạn đi trực nhật cùng nhau (không phân công việc riêng). Có bao nhiêu cách chọn?
  - **Đáp án:** 70
    1. Các bạn được chọn làm cùng một việc, nên chỉ quan tâm nhóm gồm những ai: không kể thứ tự.
    2. Đây là tổ hợp chập 4 của 8: C(8, 4) = A(8, 4) / 4!.
    3. C(8, 4) = 1680 / 24 = 70.
- `xs_t1_th_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một nhóm có 5 nam và 4 nữ. Chọn 3 người (không phân biệt vai trò) sao cho có ít nhất 1 nữ. Có bao nhiêu cách?
  - **Đáp án:** 74
    1. Đếm phần bù: mọi cách chọn 3 người trong 9 người trừ đi các cách không có nữ nào.
    2. Mọi cách: C(9, 3) = 84. Không có nữ, tức cả 3 là nam: C(5, 3) = 10.
    3. Số cách có ít nhất 1 nữ: 84 - 10 = 74.
- `xs_t1_th_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số nguyên n >= 2, C(n, 2) = C(n, n - 2).
  - **Đáp án:** Đúng
    1. Chọn 2 phần tử để lấy cũng là chọn n - 2 phần tử để bỏ lại, nên hai cách đếm cho cùng một số.
    2. Bằng công thức: C(n, n - 2) = n! / ((n - 2)! 2!) = C(n, 2). Mệnh đề đúng.
- `xs_t1_th_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 6 bi đỏ và 4 bi xanh, các bi khác nhau. Lấy 3 bi sao cho có đúng 2 bi đỏ. Có bao nhiêu cách? Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Việc lấy gồm hai bước: chọn 2 bi đỏ trong 6 bi đỏ, rồi chọn 1 bi xanh trong 4 bi xanh.
    2. Chọn 2 bi đỏ: C(6, 2) = 15 cách.
    3. Chọn 1 bi xanh: C(4, 1) = 4 cách.
    4. Theo quy tắc cộng, có 15 + 4 = 19 cách.   **<- bước sai đầu tiên**
    5. Vậy có 19 cách.
  - **Đáp án:** Bước 4: Theo quy tắc cộng, có 15 + 4 = 19 cách.
  - **Vì sao sai, và bước đúng:**
    1. Hai bước là nối tiếp (phải làm cả hai mới có một cách lấy), nên dùng quy tắc nhân, không dùng quy tắc cộng.
    2. Đúng là 15 . 4 = 60 cách.
- `xs_g1_hai_nhom` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một câu lạc bộ có 5 nam và 7 nữ. Chọn một đội gồm 1 nam và 2 nữ (không phân biệt vai trò trong đội). Có bao nhiêu cách chọn?
  - **Đáp án:** 105
    1. Chọn 1 nam trong 5 nam: C(5, 1) = 5 cách.
    2. Chọn 2 nữ trong 7 nữ: C(7, 2) = 21 cách.
    3. Hai bước nối tiếp nên nhân: 5 . 21 = 105 cách.
  - **Câu hỏi:** Một câu lạc bộ có 4 nam và 3 nữ. Chọn một đội gồm 1 nam và 2 nữ (không phân biệt vai trò trong đội). Có bao nhiêu cách chọn?
  - **Đáp án:** 12
    1. Chọn 1 nam trong 4 nam: C(4, 1) = 4 cách.
    2. Chọn 2 nữ trong 3 nữ: C(3, 2) = 3 cách.
    3. Hai bước nối tiếp nên nhân: 4 . 3 = 12 cách.
  - **Câu hỏi:** Một câu lạc bộ có 5 nam và 7 nữ. Chọn một đội gồm 3 nam và 1 nữ (không phân biệt vai trò trong đội). Có bao nhiêu cách chọn?
  - **Đáp án:** 70
    1. Chọn 3 nam trong 5 nam: C(5, 3) = 10 cách.
    2. Chọn 1 nữ trong 7 nữ: C(7, 1) = 7 cách.
    3. Hai bước nối tiếp nên nhân: 10 . 7 = 70 cách.
- `xs_g1_thu_tu_tf` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có 6 bạn. Số cách chọn 2 bạn rồi giao cho họ một trưởng nhóm và một phó nhóm là 15.
  - **Đáp án:** Sai
    1. Các chức vụ khác nhau nên thứ tự có ý nghĩa: số cách là A(6, 2) = 30.
    2. Mệnh đề nói 15, nên mệnh đề sai.
  - **Câu hỏi:** Có 5 bạn. Số cách chọn 2 bạn rồi giao cho họ một trưởng nhóm và một phó nhóm là 20.
  - **Đáp án:** Đúng
    1. Các chức vụ khác nhau nên thứ tự có ý nghĩa: số cách là A(5, 2) = 20.
    2. Mệnh đề nói 20, nên mệnh đề đúng.
  - **Câu hỏi:** Có 6 bạn. Số cách chọn 2 bạn rồi giao cho họ một trưởng nhóm và một phó nhóm là 15.
  - **Đáp án:** Sai
    1. Các chức vụ khác nhau nên thứ tự có ý nghĩa: số cách là A(6, 2) = 30.
    2. Mệnh đề nói 15, nên mệnh đề sai.

## Tầng 2: Định nghĩa xác suất: cổ điển và thống kê

45 dạng câu (37 câu viết tay, 8 bộ sinh câu); 45 chưa duyệt.

### Xác suất cổ điển (`xs_t2_co_dien`)

- `xs_t2_cd_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối. Xác suất ra mặt có số chấm lớn hơn 4 là 1/3.
  - **Đáp án:** Đúng
    1. Xúc xắc cân đối nên 6 mặt đồng khả năng.
    2. Số chấm lớn hơn 4 là 5 hoặc 6: 2 kết quả thuận lợi.
    3. P = 2/6 = 1/3. Mệnh đề đúng.
- `xs_t2_cd_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung hai đồng xu cân đối, phân biệt được với nhau. Xác suất được một mặt sấp và một mặt ngửa là bao nhiêu?
    - **(đúng)** 1/2
    - 1/3
    - 1/4
    - 2/3
  - **Đáp án:** 1/2
    1. Các kết quả đồng khả năng là SS, SN, NS, NN: có 4 kết quả.
    2. Một sấp một ngửa gồm SN và NS: 2 kết quả.
    3. P = 2/4 = 1/2. Đáp án 1/3 sai vì đã coi 'hai sấp', 'hai ngửa', 'một sấp một ngửa' là ba kết quả đồng khả năng.
- `xs_t2_cd_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chọn ngẫu nhiên một số trong các số nguyên từ 1 đến 20, mỗi số cùng khả năng được chọn. Tính xác suất số đó là số nguyên tố.
  - **Đáp án:** 2/5
    1. Có 20 kết quả đồng khả năng.
    2. Các số nguyên tố từ 1 đến 20: 2, 3, 5, 7, 11, 13, 17, 19, có 8 số (1 không phải số nguyên tố).
    3. P = 8/20 = 2/5.
- `xs_t2_cd_04` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Sắp xếp các bước tính xác suất để tổng số chấm bằng 5.
  - **Đáp án (thứ tự đúng):**
    1. Mỗi kết quả là một cặp có thứ tự (số chấm xúc xắc 1, số chấm xúc xắc 2), các cặp đồng khả năng.
    2. Đếm số cặp: 6 . 6 = 36.
    3. Trong 36 cặp đó, liệt kê các cặp có tổng bằng 5: (1, 4), (2, 3), (3, 2), (4, 1).
    4. Xác suất bằng 4/36 = 1/9.
  - **Lời giải:**
    1. Định nghĩa cổ điển cần một không gian mẫu đồng khả năng: các cặp có thứ tự.
    2. Có 36 cặp, trong đó 4 cặp có tổng 5.
    3. P = 4/36 = 1/9.
- `xs_g2_tong_hai_xuc_xac` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo đồng thời hai con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất để tổng số chấm bằng 11.
  - **Đáp án:** 1/18
    1. Mỗi kết quả là một cặp (số chấm xúc xắc 1, số chấm xúc xắc 2): có 6 . 6 = 36 kết quả đồng khả năng.
    2. Tổng t (từ 2 đến 12) có 6 - |t - 7| cặp: tổng 7 có nhiều cặp nhất, hai đầu ít nhất.
    3. Số kết quả thuận lợi: 2.
    4. Xác suất là 2/36 = 1/18.
  - **Câu hỏi:** Gieo đồng thời hai con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất để tổng số chấm bằng 3.
  - **Đáp án:** 1/18
    1. Mỗi kết quả là một cặp (số chấm xúc xắc 1, số chấm xúc xắc 2): có 6 . 6 = 36 kết quả đồng khả năng.
    2. Tổng t (từ 2 đến 12) có 6 - |t - 7| cặp: tổng 7 có nhiều cặp nhất, hai đầu ít nhất.
    3. Số kết quả thuận lợi: 2.
    4. Xác suất là 2/36 = 1/18.
  - **Câu hỏi:** Gieo đồng thời hai con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất để tổng số chấm bằng 11.
  - **Đáp án:** 1/18
    1. Mỗi kết quả là một cặp (số chấm xúc xắc 1, số chấm xúc xắc 2): có 6 . 6 = 36 kết quả đồng khả năng.
    2. Tổng t (từ 2 đến 12) có 6 - |t - 7| cặp: tổng 7 có nhiều cặp nhất, hai đầu ít nhất.
    3. Số kết quả thuận lợi: 2.
    4. Xác suất là 2/36 = 1/18.
- `xs_t2_cd_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất để hai xúc xắc ra cùng số chấm.
  - **Đáp án:** 1/6
    1. Có 36 cặp (số chấm xúc xắc 1, số chấm xúc xắc 2) đồng khả năng.
    2. Cùng số chấm: (1, 1), (2, 2), ..., (6, 6), có 6 cặp.
    3. P = 6/36 = 1/6.
- `xs_t2_cd_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối giống hệt nhau. Có 21 cặp số không kể thứ tự, nên xác suất ra một mặt 1 chấm và một mặt 2 chấm là 1/21.
  - **Đáp án:** Sai
    1. Hai xúc xắc giống nhau vẫn là hai vật khác nhau; 21 cặp không kể thứ tự không đồng khả năng.
    2. Đánh dấu hai xúc xắc thì có 36 cặp đồng khả năng; một mặt 1 và một mặt 2 gồm (1, 2) và (2, 1).
    3. P = 2/36 = 1/18, không phải 1/21. Mệnh đề sai.
- `xs_t2_cd_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung ba đồng xu cân đối, phân biệt được với nhau. Tính xác suất được đúng hai mặt ngửa. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Số mặt ngửa có thể là 0, 1, 2 hoặc 3.
    2. Vậy phép thử có 4 kết quả đồng khả năng.   **<- bước sai đầu tiên**
    3. Chỉ có một kết quả thuận lợi là 'đúng hai mặt ngửa'.
    4. Xác suất bằng 1/4.
  - **Đáp án:** Bước 2: Vậy phép thử có 4 kết quả đồng khả năng.
  - **Vì sao sai, và bước đúng:**
    1. Số mặt ngửa có 4 giá trị, nhưng 4 giá trị đó không đồng khả năng: 0 ngửa chỉ có SSS, còn 2 ngửa có ba cách.
    2. Không gian mẫu đồng khả năng là 2^3 = 8 bộ mặt; đúng hai ngửa gồm NNS, NSN, SNN.
    3. P = 3/8.
- `xs_t2_cd_08` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ, 5 bi xanh và 2 bi vàng, các bi cùng cỡ. Lấy ngẫu nhiên 1 bi. Xác suất lấy được bi không phải màu xanh là bao nhiêu?
    - **(đúng)** 1/2
    - 2/3
    - 3/10
    - 1/3
  - **Đáp án:** 1/2
    1. Có 10 bi, mỗi bi cùng khả năng được lấy: 10 kết quả đồng khả năng.
    2. Bi không phải màu xanh gồm 3 đỏ và 2 vàng: 5 bi.
    3. P = 5/10 = 1/2. Đáp án 2/3 sai vì đã coi ba màu là ba kết quả đồng khả năng.
- `xs_g2_dong_xu` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tung 3 đồng xu cân đối, phân biệt được với nhau. Tính xác suất không có đồng xu nào ra mặt ngửa.
  - **Đáp án:** 1/8
    1. Mỗi đồng xu có 2 mặt, nên có 2^3 = 8 kết quả đồng khả năng.
    2. Một kết quả thuận lợi được xác định bằng việc chọn 0 đồng xu ngửa trong 3 đồng: C(3, 0) = 1 cách.
    3. Xác suất là 1/8 = 1/8.
  - **Câu hỏi:** Tung 2 đồng xu cân đối, phân biệt được với nhau. Tính xác suất không có đồng xu nào ra mặt ngửa.
  - **Đáp án:** 1/4
    1. Mỗi đồng xu có 2 mặt, nên có 2^2 = 4 kết quả đồng khả năng.
    2. Một kết quả thuận lợi được xác định bằng việc chọn 0 đồng xu ngửa trong 2 đồng: C(2, 0) = 1 cách.
    3. Xác suất là 1/4 = 1/4.
  - **Câu hỏi:** Tung 3 đồng xu cân đối, phân biệt được với nhau. Tính xác suất có đúng 1 đồng xu ra mặt ngửa.
  - **Đáp án:** 3/8
    1. Mỗi đồng xu có 2 mặt, nên có 2^3 = 8 kết quả đồng khả năng.
    2. Một kết quả thuận lợi được xác định bằng việc chọn 1 đồng xu ngửa trong 3 đồng: C(3, 1) = 3 cách.
    3. Xác suất là 3/8 = 3/8.

### Xác suất cổ điển dùng tổ hợp (`xs_t2_co_dien_to_hop`)

- `xs_t2_ct_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 4 bi đỏ và 6 bi xanh. Lấy ngẫu nhiên đồng thời 2 bi. Số kết quả đồng khả năng của phép thử là C(10, 2) = 45.
  - **Đáp án:** Đúng
    1. Lấy đồng thời nên mỗi kết quả là một nhóm 2 bi trong 10 bi, không kể thứ tự.
    2. Số nhóm là C(10, 2) = (10 . 9)/2 = 45. Mệnh đề đúng.
- `xs_t2_ct_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lớp có 12 nam và 8 nữ. Chọn ngẫu nhiên đồng thời 2 bạn. Xác suất chọn được 2 bạn nữ là bao nhiêu?
    - **(đúng)** 14/95
    - 4/25
    - 2/5
    - 1/10
  - **Đáp án:** 14/95
    1. Không gian mẫu: C(20, 2) = 190 nhóm 2 bạn.
    2. Nhóm 2 bạn nữ: C(8, 2) = 28.
    3. P = 28/190 = 14/95. Đáp án 4/25 = (8/20)^2 sai vì đã chọn có hoàn lại, cho phép một bạn được chọn hai lần.
- `xs_t2_ct_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một nhóm có 5 người, trong đó có An và Bình. Chọn ngẫu nhiên đồng thời 2 người đi công tác. Tính xác suất cả An và Bình đều được chọn.
  - **Đáp án:** 1/10
    1. Số cách chọn 2 người trong 5 người: C(5, 2) = 10, các cách đồng khả năng.
    2. Chỉ có một nhóm gồm đúng An và Bình.
    3. P = 1/10.
- `xs_t2_ct_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp ngẫu nhiên 5 người, trong đó có An và Bình, thành một hàng ngang. Tính xác suất An và Bình đứng cạnh nhau.
  - **Đáp án:** 2/5
    1. Có 5! = 120 cách xếp đồng khả năng.
    2. An và Bình cạnh nhau: buộc thành khối, xếp khối cùng 3 người còn lại được 4! = 24 cách, đổi chỗ trong khối 2 cách: 48 cách.
    3. P = 48/120 = 2/5.
- `xs_t2_ct_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Rút ngẫu nhiên đồng thời 5 lá từ bộ bài tây 52 lá (13 lá mỗi chất). Xác suất cả 5 lá đều là lá cơ bằng C(13, 5)/C(52, 5).
  - **Đáp án:** Đúng
    1. Rút đồng thời nên mỗi kết quả là một nhóm 5 lá, có C(52, 5) nhóm đồng khả năng.
    2. Nhóm toàn lá cơ là cách chọn 5 trong 13 lá cơ: C(13, 5).
    3. Tử và mẫu cùng đếm nhóm không kể thứ tự, nên P = C(13, 5)/C(52, 5). Mệnh đề đúng.
- `xs_t2_ct_06` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 2 bi xanh, các bi cùng cỡ. Lấy ngẫu nhiên đồng thời 2 bi. Ghép mỗi sự kiện với xác suất của nó.
  - **Đáp án (ghép đúng):**
    - Cả hai bi đều đỏ — 3/10
    - Cả hai bi đều xanh — 1/10
    - Một bi đỏ và một bi xanh — 3/5
  - **Lời giải:**
    1. Không gian mẫu: C(5, 2) = 10 nhóm 2 bi.
    2. Hai đỏ: C(3, 2) = 3, P = 3/10. Hai xanh: C(2, 2) = 1, P = 1/10.
    3. Một đỏ một xanh: 3 . 2 = 6, P = 6/10 = 3/5. Ba xác suất cộng lại bằng 1.
- `xs_t2_ct_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 5 bi trắng và 3 bi đen. Lấy ngẫu nhiên đồng thời 3 bi. Tính xác suất được đúng 1 bi đen. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Không gian mẫu: lấy 3 bi trong 8 bi có kể thứ tự, A(8, 3) = 336 kết quả.   **<- bước sai đầu tiên**
    2. Đúng 1 bi đen nghĩa là 1 bi đen và 2 bi trắng.
    3. Số kết quả thuận lợi là C(3, 1) . C(5, 2) = 3 . 10 = 30.
    4. Xác suất là 30/336 = 5/56.
  - **Đáp án:** Bước 1: Không gian mẫu: lấy 3 bi trong 8 bi có kể thứ tự, A(8, 3) = 336 kết quả.
  - **Vì sao sai, và bước đúng:**
    1. Ba bi lấy đồng thời, mỗi kết quả là một nhóm không có thứ tự; tử số cũng đã đếm theo nhóm. Tử và mẫu phải đếm cùng một kiểu.
    2. Không gian mẫu đúng là C(8, 3) = 56.
    3. P = 30/56 = 15/28.
- `xs_g2_rut_bai` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Rút ngẫu nhiên đồng thời 2 lá từ bộ bài tây 52 lá (4 chất, mỗi chất 13 lá từ 2 đến 10, J, Q, K, át). Tính xác suất cả hai lá đều là lá cơ.
  - **Đáp án:** 1/17
    1. Rút đồng thời nên không kể thứ tự: có C(52, 2) = 1326 kết quả đồng khả năng.
    2. Chọn 2 trong 13 lá cơ: C(13, 2) = 78.
    3. Xác suất là 78/1326 = 1/17.
  - **Câu hỏi:** Rút ngẫu nhiên đồng thời 2 lá từ bộ bài tây 52 lá (4 chất, mỗi chất 13 lá từ 2 đến 10, J, Q, K, át). Tính xác suất cả hai lá đều là át.
  - **Đáp án:** 1/221
    1. Rút đồng thời nên không kể thứ tự: có C(52, 2) = 1326 kết quả đồng khả năng.
    2. Chọn 2 trong 4 lá át: C(4, 2) = 6.
    3. Xác suất là 6/1326 = 1/221.
  - **Câu hỏi:** Rút ngẫu nhiên đồng thời 2 lá từ bộ bài tây 52 lá (4 chất, mỗi chất 13 lá từ 2 đến 10, J, Q, K, át). Tính xác suất hai lá cùng chất.
  - **Đáp án:** 4/17
    1. Rút đồng thời nên không kể thứ tự: có C(52, 2) = 1326 kết quả đồng khả năng.
    2. Chọn chất (4 cách) rồi chọn 2 trong 13 lá của chất đó: 4 . 78 = 312.
    3. Xác suất là 312/1326 = 4/17.
- `xs_g2_rut_bi` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 6 bi xanh, các bi cùng cỡ. Lấy ngẫu nhiên đồng thời 2 bi. Tính xác suất lấy được đúng 1 bi đỏ.
  - **Đáp án:** 1/2
    1. Lấy đồng thời nên không kể thứ tự: không gian mẫu có C(9, 2) = 36 kết quả.
    2. Đúng 1 bi đỏ nghĩa là 1 bi đỏ và 1 bi xanh: C(3, 1) . C(6, 1) = 3 . 6 = 18 cách.
    3. Xác suất là 18/36 = 1/2.
  - **Câu hỏi:** Một hộp có 2 bi đỏ và 2 bi xanh, các bi cùng cỡ. Lấy ngẫu nhiên đồng thời 2 bi. Tính xác suất lấy được đúng 1 bi đỏ.
  - **Đáp án:** 2/3
    1. Lấy đồng thời nên không kể thứ tự: không gian mẫu có C(4, 2) = 6 kết quả.
    2. Đúng 1 bi đỏ nghĩa là 1 bi đỏ và 1 bi xanh: C(2, 1) . C(2, 1) = 2 . 2 = 4 cách.
    3. Xác suất là 4/6 = 2/3.
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 6 bi xanh, các bi cùng cỡ. Lấy ngẫu nhiên đồng thời 4 bi. Tính xác suất lấy được đúng 1 bi đỏ.
  - **Đáp án:** 10/21
    1. Lấy đồng thời nên không kể thứ tự: không gian mẫu có C(9, 4) = 126 kết quả.
    2. Đúng 1 bi đỏ nghĩa là 1 bi đỏ và 3 bi xanh: C(3, 1) . C(6, 3) = 3 . 20 = 60 cách.
    3. Xác suất là 60/126 = 10/21.

### Lấy có hoàn lại và không hoàn lại (`xs_t2_hoan_lai`)

- `xs_t2_hl_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 5 bi đánh số 1 đến 5. Lấy lần lượt 2 bi có hoàn lại (lấy xong trả bi vào hộp rồi mới lấy lần sau), ghi số theo thứ tự lấy. Không gian mẫu có 5 . 5 = 25 kết quả.
  - **Đáp án:** Đúng
    1. Có hoàn lại nên lần nào hộp cũng đủ 5 bi: mỗi lần có 5 cách.
    2. Hai lần nối tiếp nên nhân: 5 . 5 = 25, kể cả các kết quả như (3, 3). Mệnh đề đúng.
- `xs_t2_hl_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 4 bi đánh số 1 đến 4. Lấy lần lượt 2 bi không hoàn lại và ghi số theo thứ tự lấy. Không gian mẫu có bao nhiêu kết quả?
    - **(đúng)** 12
    - 16
    - 6
    - 8
  - **Đáp án:** 12
    1. Lần 1 có 4 cách; bi đã lấy không trả lại nên lần 2 còn 3 cách.
    2. Ghi theo thứ tự nên (1, 2) và (2, 1) khác nhau: 4 . 3 = 12.
    3. 16 là của lấy có hoàn lại, 6 là của lấy đồng thời không kể thứ tự.
- `xs_t2_hl_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 10 phiếu đánh số 1 đến 10. Rút lần lượt 2 phiếu có hoàn lại (rút xong trả phiếu vào hộp). Tính xác suất hai phiếu rút được có cùng số.
  - **Đáp án:** 1/10
    1. Có hoàn lại: 10 . 10 = 100 cặp có thứ tự đồng khả năng.
    2. Cùng số: (1, 1), (2, 2), ..., (10, 10), có 10 cặp.
    3. P = 10/100 = 1/10.
- `xs_t2_hl_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 6 bi đánh số 1 đến 6. Lấy 2 bi. Ghép mỗi cách lấy với số kết quả của không gian mẫu.
  - **Đáp án (ghép đúng):**
    - Lần lượt, có hoàn lại, ghi theo thứ tự — 36
    - Lần lượt, không hoàn lại, ghi theo thứ tự — 30
    - Đồng thời 2 bi, không kể thứ tự — 15
  - **Lời giải:**
    1. Có hoàn lại: mỗi lần 6 cách, 6 . 6 = 36.
    2. Không hoàn lại, có thứ tự: 6 . 5 = 30.
    3. Đồng thời: mỗi nhóm {x, y} ứng với hai cặp có thứ tự, nên 30/2 = 15 = C(6, 2).
- `xs_t2_hl_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 2 bi xanh. Lấy lần lượt 2 bi không hoàn lại. Xác suất bi lấy lần thứ hai là bi đỏ bằng 3/5.
  - **Đáp án:** Đúng
    1. Có 5 . 4 = 20 cặp có thứ tự đồng khả năng.
    2. Lần 2 đỏ: lần 1 đỏ rồi lần 2 đỏ có 3 . 2 = 6 cặp; lần 1 xanh rồi lần 2 đỏ có 2 . 3 = 6 cặp.
    3. P = 12/20 = 3/5, đúng bằng tỷ lệ bi đỏ ban đầu. Mệnh đề đúng.
- `xs_t2_hl_06` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 4 bi trắng và 2 bi đen. Lấy lần lượt 2 bi không hoàn lại. Tính xác suất hai bi lấy được khác màu.
  - **Đáp án:** 8/15
    1. Không gian mẫu (có thứ tự): 6 . 5 = 30 cặp.
    2. Khác màu: trắng rồi đen 4 . 2 = 8 cặp, đen rồi trắng 2 . 4 = 8 cặp, tổng 16.
    3. P = 16/30 = 8/15.
- `xs_t2_hl_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 5 bi đỏ và 3 bi xanh. Lấy lần lượt 2 bi không hoàn lại. Tính xác suất cả hai bi đều đỏ. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi kết quả là một cặp có thứ tự (bi lần 1, bi lần 2) gồm hai bi khác nhau.
    2. Không gian mẫu có 8 . 8 = 64 kết quả.   **<- bước sai đầu tiên**
    3. Số kết quả cả hai bi đều đỏ là 5 . 4 = 20.
    4. Xác suất là 20/64 = 5/16.
  - **Đáp án:** Bước 2: Không gian mẫu có 8 . 8 = 64 kết quả.
  - **Vì sao sai, và bước đúng:**
    1. Không hoàn lại nên lần 2 chỉ còn 7 bi: không gian mẫu có 8 . 7 = 56 kết quả. 8 . 8 là của lấy có hoàn lại.
    2. Tử số 5 . 4 = 20 đã đúng.
    3. P = 20/56 = 5/14.
- `xs_t2_hl_08` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 2 bi đỏ và 3 bi xanh. Lấy lần lượt 2 bi có hoàn lại. Sắp xếp các bước tính xác suất lấy được ít nhất một bi đỏ.
  - **Đáp án (thứ tự đúng):**
    1. Mỗi lần lấy, bi được trả lại nên hộp luôn có 5 bi; không gian mẫu có 5 . 5 = 25 kết quả.
    2. Trong 25 kết quả đó, sự kiện đối của 'ít nhất một bi đỏ' là 'cả hai lần đều xanh'.
    3. Số kết quả cả hai lần đều xanh là 3 . 3 = 9.
    4. Xác suất ít nhất một bi đỏ là 1 - 9/25 = 16/25.
  - **Lời giải:**
    1. Có hoàn lại nên không gian mẫu là 25 cặp có thứ tự.
    2. 'Ít nhất một' dễ tính qua sự kiện đối: cả hai đều xanh, 9 cặp.
    3. P = 1 - 9/25 = 16/25.
- `xs_g2_hoan_lai` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi trắng và 6 bi đen, các bi cùng cỡ. Lấy lần lượt 2 bi không hoàn lại. Tính xác suất cả hai lần đều được bi trắng.
  - **Đáp án:** 1/12
    1. Không hoàn lại nên lần sau còn 8 bi: 9 . 8 = 72 kết quả có thứ tự.
    2. Số kết quả thuận lợi (kể thứ tự): 3 . 2 = 6.
    3. Xác suất là 6/72 = 1/12.
  - **Câu hỏi:** Một hộp có 2 bi trắng và 2 bi đen, các bi cùng cỡ. Lấy lần lượt 2 bi có hoàn lại (lấy xong trả bi vào hộp rồi mới lấy lần sau). Tính xác suất cả hai lần đều được bi trắng.
  - **Đáp án:** 1/4
    1. Có hoàn lại nên lần nào cũng có 4 bi: 4 . 4 = 16 kết quả có thứ tự.
    2. Số kết quả thuận lợi (kể thứ tự): 2 . 2 = 4.
    3. Xác suất là 4/16 = 1/4.
  - **Câu hỏi:** Một hộp có 3 bi trắng và 6 bi đen, các bi cùng cỡ. Lấy lần lượt 2 bi không hoàn lại. Tính xác suất cả hai lần đều được bi đen.
  - **Đáp án:** 5/12
    1. Không hoàn lại nên lần sau còn 8 bi: 9 . 8 = 72 kết quả có thứ tự.
    2. Số kết quả thuận lợi (kể thứ tự): 6 . 5 = 30.
    3. Xác suất là 30/72 = 5/12.

### Tính chất của xác suất và sự kiện đối (`xs_t2_tinh_chat`)

- `xs_t2_tc_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi sự kiện A của một phép thử, P(A) + P(Ā) = 1.
  - **Đáp án:** Đúng
    1. A và Ā xung khắc, và A + Ā là sự kiện chắc chắn.
    2. Nên P(A) + P(Ā) = P(A + Ā) = 1. Mệnh đề đúng.
- `xs_t2_tc_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xác suất để một bóng đèn bị hỏng trong năm đầu sử dụng là 1/8. Xác suất để bóng đèn đó không hỏng trong năm đầu là bao nhiêu?
    - **(đúng)** 7/8
    - 1/8
    - 8/7
    - 1/7
  - **Đáp án:** 7/8
    1. 'Không hỏng' là sự kiện đối của 'hỏng'.
    2. P = 1 - 1/8 = 7/8.
    3. 8/7 lớn hơn 1 nên không thể là một xác suất.
- `xs_t2_tc_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Rút ngẫu nhiên một lá từ bộ bài tây 52 lá có 4 lá át. Dùng sự kiện đối, tính xác suất lá rút được không phải là lá át.
  - **Đáp án:** 12/13
    1. P(lá át) = 4/52 = 1/13.
    2. 'Không phải át' là sự kiện đối: P = 1 - 1/13 = 12/13.
- `xs_t2_tc_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối. Xác suất có ít nhất một mặt 6 bằng 1/6 + 1/6 = 1/3.
  - **Đáp án:** Sai
    1. Cộng thẳng 1/6 + 1/6 đã đếm kết quả (6, 6) hai lần.
    2. Dùng sự kiện đối: không có mặt 6 nào có 5 . 5 = 25 trong 36 kết quả.
    3. P = 1 - 25/36 = 11/36, nhỏ hơn 1/3 = 12/36. Mệnh đề sai.
- `xs_t2_tc_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một mật khẩu gồm 4 chữ số, mỗi chữ số từ 0 đến 9 (được lặp lại), được chọn ngẫu nhiên, mọi mật khẩu cùng khả năng. Tính xác suất mật khẩu có ít nhất hai chữ số giống nhau.
  - **Đáp án:** 62/125
    1. Có 10^4 = 10000 mật khẩu đồng khả năng.
    2. Sự kiện đối: bốn chữ số đôi một khác nhau, có 10 . 9 . 8 . 7 = 5040 mật khẩu.
    3. P = 1 - 5040/10000 = 4960/10000 = 62/125.
- `xs_t2_tc_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung 4 đồng xu cân đối, phân biệt được với nhau. Tính xác suất có ít nhất một mặt ngửa. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Không gian mẫu có 2^4 = 16 kết quả đồng khả năng.
    2. Sự kiện đối của 'có ít nhất một mặt ngửa' là 'có ít nhất một mặt sấp'.   **<- bước sai đầu tiên**
    3. Sự kiện 'có ít nhất một mặt sấp' có 15 kết quả.
    4. Xác suất cần tìm là 1 - 15/16 = 1/16.
  - **Đáp án:** Bước 2: Sự kiện đối của 'có ít nhất một mặt ngửa' là 'có ít nhất một mặt sấp'.
  - **Vì sao sai, và bước đúng:**
    1. Sự kiện đối của 'có ít nhất một mặt ngửa' là 'không có mặt ngửa nào', tức cả 4 đồng xu đều sấp.
    2. Sự kiện đó chỉ có 1 kết quả SSSS.
    3. P = 1 - 1/16 = 15/16.
- `xs_t2_tc_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi xác suất với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - Xác suất của sự kiện chắc chắn — 1
    - Xác suất của sự kiện không thể — 0
    - P(Ā) khi P(A) = 2/5 — 3/5
    - P(A + B) khi A, B xung khắc, P(A) = 1/5, P(B) = 1/3 — 8/15
  - **Lời giải:**
    1. Sự kiện chắc chắn có xác suất 1, sự kiện không thể có xác suất 0.
    2. P(Ā) = 1 - 2/5 = 3/5.
    3. A, B xung khắc thì xác suất của tổng bằng tổng các xác suất: 1/5 + 1/3 = 3/15 + 5/15 = 8/15.
- `xs_g2_it_nhat_mot` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo 4 con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất có ít nhất một con xúc xắc ra mặt 6 chấm.
  - **Đáp án:** 671/1296
    1. Không gian mẫu có 6^4 = 1296 kết quả đồng khả năng.
    2. Sự kiện đối của 'có ít nhất một' là 'không con xúc xắc nào ra mặt 6'.
    3. Đếm sự kiện đối: mỗi xúc xắc có 5 cách (từ 1 đến 5 chấm), nên có 5^4 = 625 kết quả; xác suất của nó là 625/1296.
    4. Xác suất cần tìm là 1 - 625/1296 = 671/1296.
  - **Câu hỏi:** Gieo 2 con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất có ít nhất một con xúc xắc ra mặt 6 chấm.
  - **Đáp án:** 11/36
    1. Không gian mẫu có 6^2 = 36 kết quả đồng khả năng.
    2. Sự kiện đối của 'có ít nhất một' là 'không con xúc xắc nào ra mặt 6'.
    3. Đếm sự kiện đối: mỗi xúc xắc có 5 cách (từ 1 đến 5 chấm), nên có 5^2 = 25 kết quả; xác suất của nó là 25/36.
    4. Xác suất cần tìm là 1 - 25/36 = 11/36.
  - **Câu hỏi:** Gieo 4 con xúc xắc cân đối, phân biệt được với nhau. Tính xác suất có ít nhất một con xúc xắc ra mặt 6 chấm.
  - **Đáp án:** 671/1296
    1. Không gian mẫu có 6^4 = 1296 kết quả đồng khả năng.
    2. Sự kiện đối của 'có ít nhất một' là 'không con xúc xắc nào ra mặt 6'.
    3. Đếm sự kiện đối: mỗi xúc xắc có 5 cách (từ 1 đến 5 chấm), nên có 5^4 = 625 kết quả; xác suất của nó là 625/1296.
    4. Xác suất cần tìm là 1 - 625/1296 = 671/1296.

### Định nghĩa thống kê: tần suất (`xs_t2_thong_ke`)

- `xs_t2_tk_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu 100 lần thấy 47 lần ra mặt ngửa. Tần suất ra mặt ngửa trong 100 lần tung đó là 47/100.
  - **Đáp án:** Đúng
    1. Tần suất = số lần sự kiện xảy ra / số lần thử.
    2. Tần suất = 47/100. Mệnh đề đúng.
- `xs_t2_tk_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ bắn 50 phát, trúng 40 phát. Tần suất bắn trúng của xạ thủ là bao nhiêu?
    - **(đúng)** 4/5
    - 1/5
    - 40
    - 5/4
  - **Đáp án:** 4/5
    1. Tần suất bắn trúng = số phát trúng / số phát bắn.
    2. 40/50 = 4/5.
    3. 1/5 là tần suất bắn trượt; 40 là số lần, chưa chia; 5/4 lớn hơn 1 nên không thể là tần suất.
- `xs_t2_tk_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Kiểm tra 200 sản phẩm của một dây chuyền thấy có 6 phế phẩm. Tính tần suất phế phẩm.
  - **Đáp án:** 3/100
    1. Tần suất phế phẩm = số phế phẩm / số sản phẩm được kiểm tra.
    2. 6/200 = 3/100.
- `xs_g2_tan_suat` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ tập bắn 2 ngày: ngày 1: bắn 30 phát, trúng 23 phát; ngày 2: bắn 10 phát, trúng 5 phát. Tính tần suất bắn trượt của xạ thủ trong toàn bộ các lần bắn đó.
  - **Đáp án:** 3/10
    1. Tần suất = số lần sự kiện xảy ra / tổng số lần thử, tính trên tất cả các ngày gộp lại.
    2. Tổng số phát bắn: 30 + 10 = 40; số phát trúng: 23 + 5 = 28. Số phát trượt: 40 - 28 = 12.
    3. Tần suất bắn trượt là 12/40 = 3/10.
  - **Câu hỏi:** Một xạ thủ tập bắn 2 ngày: ngày 1: bắn 10 phát, trúng 7 phát; ngày 2: bắn 10 phát, trúng 6 phát. Tính tần suất bắn trúng của xạ thủ trong toàn bộ các lần bắn đó.
  - **Đáp án:** 13/20
    1. Tần suất = số lần sự kiện xảy ra / tổng số lần thử, tính trên tất cả các ngày gộp lại.
    2. Tổng số phát bắn: 10 + 10 = 20; số phát trúng: 7 + 6 = 13.
    3. Tần suất bắn trúng là 13/20 = 13/20.
  - **Câu hỏi:** Một xạ thủ tập bắn 2 ngày: ngày 1: bắn 30 phát, trúng 19 phát; ngày 2: bắn 30 phát, trúng 26 phát. Tính tần suất bắn trúng của xạ thủ trong toàn bộ các lần bắn đó.
  - **Đáp án:** 3/4
    1. Tần suất = số lần sự kiện xảy ra / tổng số lần thử, tính trên tất cả các ngày gộp lại.
    2. Tổng số phát bắn: 30 + 30 = 60; số phát trúng: 19 + 26 = 45.
    3. Tần suất bắn trúng là 45/60 = 3/4.
- `xs_t2_tk_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu cân đối 10 lần thì chắc chắn có đúng 5 lần ra mặt ngửa.
  - **Đáp án:** Sai
    1. Xác suất 1/2 không có nghĩa là đúng một nửa số lần: tần suất dao động quanh 1/2.
    2. Có thể ra 4, 6 hay số lần khác; xác suất ra đúng 5 lần ngửa chỉ là C(10, 5)/2^10 = 252/1024, chưa tới một phần tư. Mệnh đề sai.
- `xs_t2_tk_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khẳng định nào đúng về định nghĩa thống kê của xác suất?
    - **(đúng)** Khi số lần thử n rất lớn, tần suất của A dao động quanh một số cố định, và số đó được lấy làm P(A).
    - Tần suất của A sau 10 lần thử luôn bằng P(A).
    - Tần suất chỉ dùng được khi các kết quả đồng khả năng.
    - Tần suất của A luôn lớn hơn P(A).
  - **Đáp án:** Khi số lần thử n rất lớn, tần suất của A dao động quanh một số cố định, và số đó được lấy làm P(A).
    1. Định nghĩa thống kê lấy giới hạn mà tần suất ổn định quanh khi số lần thử rất lớn.
    2. Với ít lần thử, tần suất có thể lệch xa P(A), lúc lớn lúc nhỏ hơn.
    3. Ưu điểm của nó chính là dùng được cả khi các kết quả không đồng khả năng, như xác suất một sản phẩm bị lỗi.
- `xs_t2_tk_06` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Theo dõi nhiều năm, một nhà máy thấy tần suất sản phẩm hỏng ổn định quanh 1/50. Lấy tần suất này làm xác suất một sản phẩm hỏng. Trong một lô 1500 sản phẩm, trung bình có khoảng bao nhiêu sản phẩm hỏng?
  - **Đáp án:** 30
    1. Định nghĩa thống kê: tần suất ổn định sau rất nhiều lần thử được lấy làm xác suất, P(hỏng) = 1/50.
    2. Ngược lại, trong n sản phẩm thì số sản phẩm hỏng xấp xỉ n . P(hỏng).
    3. 1500 . 1/50 = 30 sản phẩm.
- `xs_t2_tk_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Gieo một con xúc xắc 60 lần thấy mặt 6 xuất hiện 12 lần. Tính tần suất ra mặt 6 và so với xác suất của xúc xắc cân đối. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Tần suất là số lần mặt 6 xuất hiện chia số lần gieo.
    2. Tần suất ra mặt 6 là 12/60 = 1/5.
    3. Xác suất ra mặt 6 của xúc xắc cân đối là 1/6.
    4. Vì 1/5 khác 1/6 nên chắc chắn xúc xắc này không cân đối.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vì 1/5 khác 1/6 nên chắc chắn xúc xắc này không cân đối.
  - **Vì sao sai, và bước đúng:**
    1. Tần suất sau một số lần thử có hạn luôn dao động quanh xác suất, không trùng khít với nó.
    2. Với 60 lần gieo, xúc xắc cân đối trung bình cho 10 lần mặt 6; ra 12 lần là chênh lệch rất bình thường.
    3. Chỉ khi gieo rất nhiều lần mà tần suất vẫn lệch xa 1/6 mới có cơ sở nghi xúc xắc không cân đối.
- `xs_g2_uoc_luong_so_ca` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Để ước lượng số cá trong một hồ, người ta bắt 60 con, đánh dấu rồi thả lại. Ít ngày sau bắt 80 con thì thấy 6 con có dấu. Coi tần suất cá có dấu trong lần bắt sau bằng tỷ lệ cá có dấu trong cả hồ. Ước lượng số cá trong hồ.
  - **Đáp án:** 800
    1. Tần suất cá có dấu ở lần bắt sau là 6/80.
    2. Nếu hồ có N con thì tỷ lệ cá có dấu là 60/N, nên 60/N = 6/80.
    3. N = 60 . 80 / 6 = 800.
  - **Câu hỏi:** Để ước lượng số cá trong một hồ, người ta bắt 50 con, đánh dấu rồi thả lại. Ít ngày sau bắt 50 con thì thấy 5 con có dấu. Coi tần suất cá có dấu trong lần bắt sau bằng tỷ lệ cá có dấu trong cả hồ. Ước lượng số cá trong hồ.
  - **Đáp án:** 500
    1. Tần suất cá có dấu ở lần bắt sau là 5/50.
    2. Nếu hồ có N con thì tỷ lệ cá có dấu là 50/N, nên 50/N = 5/50.
    3. N = 50 . 50 / 5 = 500.
  - **Câu hỏi:** Để ước lượng số cá trong một hồ, người ta bắt 110 con, đánh dấu rồi thả lại. Ít ngày sau bắt 130 con thì thấy 20 con có dấu. Coi tần suất cá có dấu trong lần bắt sau bằng tỷ lệ cá có dấu trong cả hồ. Ước lượng số cá trong hồ.
  - **Đáp án:** 715
    1. Tần suất cá có dấu ở lần bắt sau là 20/130.
    2. Nếu hồ có N con thì tỷ lệ cá có dấu là 110/N, nên 110/N = 20/130.
    3. N = 110 . 130 / 20 = 715.

## Tầng 3: Công thức cộng, nhân, xác suất có điều kiện và Bernoulli

48 dạng câu (39 câu viết tay, 9 bộ sinh câu); 48 chưa duyệt.

### Công thức cộng xác suất (`xs_t3_cong_thuc_cong`)

- `xs_t3_cc_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với hai sự kiện bất kỳ A và B của cùng một phép thử, P(A + B) = P(A) + P(B).
  - **Đáp án:** Sai
    1. Công thức đúng cho mọi A, B là P(A + B) = P(A) + P(B) - P(AB).
    2. Chỉ khi A, B xung khắc (P(AB) = 0) mới được bỏ số hạng cuối.
    3. Ví dụ gieo xúc xắc, A = B = {6}: P(A + B) = 1/6, còn P(A) + P(B) = 1/3. Mệnh đề sai.
- `xs_t3_cc_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai sự kiện A, B với P(A) = 1/2, P(B) = 1/3 và P(AB) = 1/6. Tính P(A + B).
  - **Đáp án:** 2/3
    1. Công thức cộng: P(A + B) = P(A) + P(B) - P(AB).
    2. = 1/2 + 1/3 - 1/6 = 3/6 + 2/6 - 1/6 = 4/6 = 2/3.
- `xs_t3_cc_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lớp có 40 học sinh: 25 bạn học tiếng Anh, 15 bạn học tiếng Pháp, trong đó 8 bạn học cả hai thứ tiếng. Chọn ngẫu nhiên một bạn. Xác suất bạn đó học ít nhất một trong hai thứ tiếng là bao nhiêu?
    - **(đúng)** 4/5
    - 1
    - 3/5
    - 1/5
  - **Đáp án:** 4/5
    1. A: học tiếng Anh, P(A) = 25/40; B: học tiếng Pháp, P(B) = 15/40; P(AB) = 8/40.
    2. P(A + B) = (25 + 15 - 8)/40 = 32/40 = 4/5.
    3. Đáp án 1 sai vì cộng 25 + 15 = 40 đã đếm 8 bạn học cả hai hai lần.
- `xs_t3_cc_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Rút ngẫu nhiên một lá từ bộ bài tây 52 lá. Tính xác suất lá đó là lá cơ hoặc là lá K. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi A: rút được lá cơ, B: rút được lá K. Cần tính P(A + B).
    2. P(A) = 13/52 và P(B) = 4/52.
    3. A và B xung khắc nên P(A + B) = 13/52 + 4/52 = 17/52.   **<- bước sai đầu tiên**
    4. Vậy xác suất cần tìm là 17/52.
  - **Đáp án:** Bước 3: A và B xung khắc nên P(A + B) = 13/52 + 4/52 = 17/52.
  - **Vì sao sai, và bước đúng:**
    1. A và B không xung khắc: lá K cơ vừa là lá cơ vừa là lá K, P(AB) = 1/52.
    2. P(A + B) = 13/52 + 4/52 - 1/52 = 16/52 = 4/13.
- `xs_g3_chia_het` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chọn ngẫu nhiên một số nguyên từ 1 đến 28, mỗi số cùng khả năng được chọn. Tính xác suất số được chọn chia hết cho 2 hoặc chia hết cho 5.
  - **Đáp án:** 17/28
    1. A: chia hết cho 2, B: chia hết cho 5. Cần P(A + B) = P(A) + P(B) - P(AB).
    2. Từ 1 đến 28 có 14 số chia hết cho 2 và 5 số chia hết cho 5.
    3. AB là chia hết cho cả 2 và 5, tức chia hết cho 10: có 2 số.
    4. P(A + B) = (14 + 5 - 2)/28 = 17/28 = 17/28.
  - **Câu hỏi:** Chọn ngẫu nhiên một số nguyên từ 1 đến 15, mỗi số cùng khả năng được chọn. Tính xác suất số được chọn chia hết cho 2 hoặc chia hết cho 7.
  - **Đáp án:** 8/15
    1. A: chia hết cho 2, B: chia hết cho 7. Cần P(A + B) = P(A) + P(B) - P(AB).
    2. Từ 1 đến 15 có 7 số chia hết cho 2 và 2 số chia hết cho 7.
    3. AB là chia hết cho cả 2 và 7, tức chia hết cho 14: có 1 số.
    4. P(A + B) = (7 + 2 - 1)/15 = 8/15 = 8/15.
  - **Câu hỏi:** Chọn ngẫu nhiên một số nguyên từ 1 đến 20, mỗi số cùng khả năng được chọn. Tính xác suất số được chọn chia hết cho 4 hoặc chia hết cho 6.
  - **Đáp án:** 7/20
    1. A: chia hết cho 4, B: chia hết cho 6. Cần P(A + B) = P(A) + P(B) - P(AB).
    2. Từ 1 đến 20 có 5 số chia hết cho 4 và 3 số chia hết cho 6.
    3. AB là chia hết cho cả 4 và 6, tức chia hết cho 12: có 1 số.
    4. P(A + B) = (5 + 3 - 1)/20 = 7/20 = 7/20.
- `xs_t3_cc_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chọn ngẫu nhiên một số nguyên từ 1 đến 30, mỗi số cùng khả năng được chọn. Tính xác suất số đó chia hết cho 2, cho 3 hoặc cho 5 (chia hết cho ít nhất một trong ba số).
  - **Đáp án:** 11/15
    1. Gọi A, B, C là chia hết cho 2, 3, 5: có 15, 10, 6 số.
    2. Chia hết cho từng cặp: cho 6 có 5 số, cho 10 có 3 số, cho 15 có 2 số; chia hết cho cả ba (cho 30) có 1 số.
    3. Công thức cộng cho ba sự kiện: 15 + 10 + 6 - 5 - 3 - 2 + 1 = 22 số.
    4. P = 22/30 = 11/15.
- `xs_t3_cc_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu hai sự kiện A, B của cùng một phép thử có P(A) = 3/5 và P(B) = 1/2 thì A và B không thể xung khắc.
  - **Đáp án:** Đúng
    1. Nếu A, B xung khắc thì P(A + B) = P(A) + P(B) = 3/5 + 1/2 = 11/10.
    2. Một xác suất không thể lớn hơn 1, nên giả sử xung khắc là vô lý.
    3. Từ công thức cộng còn suy ra P(AB) = P(A) + P(B) - P(A + B) >= 11/10 - 1 = 1/10 > 0. Mệnh đề đúng.
- `xs_t3_cc_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho P(A) = 1/2, P(B) = 2/5 và P(A + B) = 7/10. Sắp xếp các bước tính P(AB).
  - **Đáp án (thứ tự đúng):**
    1. Viết công thức cộng: P(A + B) = P(A) + P(B) - P(AB).
    2. Thay số: 7/10 = 1/2 + 2/5 - P(AB).
    3. Gom vế phải: 7/10 = 9/10 - P(AB).
    4. Suy ra P(AB) = 9/10 - 7/10 = 1/5.
  - **Lời giải:**
    1. Công thức cộng liên hệ bốn đại lượng; biết ba thì tìm được cái thứ tư.
    2. 1/2 + 2/5 = 9/10, nên P(AB) = 9/10 - 7/10 = 1/5.
- `xs_t3_cc_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ba sự kiện A, B, C đôi một xung khắc với P(A) = 1/6, P(B) = 1/4 và P(C) = 1/3. P(A + B + C) bằng bao nhiêu?
    - **(đúng)** 3/4
    - 1/72
    - 1/2
    - 11/12
  - **Đáp án:** 3/4
    1. Đôi một xung khắc nên xác suất của tổng bằng tổng các xác suất.
    2. 1/6 + 1/4 + 1/3 = 2/12 + 3/12 + 4/12 = 9/12 = 3/4.
    3. 1/72 là tích các xác suất, không phải công thức cộng.
- `xs_g3_cong_tim_giao` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai sự kiện A, B với P(A) = 5/6, P(B) = 1/6 và P(A + B) = 11/12. Tính P(AB).
  - **Đáp án:** 1/12
    1. Công thức cộng: P(A + B) = P(A) + P(B) - P(AB), nên P(AB) = P(A) + P(B) - P(A + B).
    2. P(AB) = 5/6 + 1/6 - 11/12 = 1/12.
  - **Câu hỏi:** Cho hai sự kiện A, B với P(A) = 1/5, P(B) = 1/5 và P(A + B) = 3/10. Tính P(AB).
  - **Đáp án:** 1/10
    1. Công thức cộng: P(A + B) = P(A) + P(B) - P(AB), nên P(AB) = P(A) + P(B) - P(A + B).
    2. P(AB) = 1/5 + 1/5 - 3/10 = 1/10.
  - **Câu hỏi:** Cho hai sự kiện A, B với P(A) = 5/6, P(B) = 3/4 và P(AB) = 7/12. Tính xác suất để cả A và B đều không xảy ra.
  - **Đáp án:** 0
    1. 'Cả A và B đều không xảy ra' là sự kiện đối của A + B.
    2. P(A + B) = 5/6 + 3/4 - 7/12 = 1.
    3. Xác suất cần tìm là 1 - 1 = 0.

### Xác suất có điều kiện (`xs_t3_dieu_kien`)

- `xs_t3_dk_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối. Biết kết quả là số chẵn, xác suất kết quả đó là 2 bằng 1/3.
  - **Đáp án:** Đúng
    1. Điều kiện 'số chẵn' thu hẹp không gian mẫu còn {2, 4, 6}, ba kết quả đồng khả năng.
    2. Trong đó chỉ có kết quả 2: P = 1/3. Mệnh đề đúng.
- `xs_t3_dk_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai sự kiện A, B với P(A) = 1/2, P(B) = 2/5 và P(AB) = 1/5. Tính P(A|B).
  - **Đáp án:** 1/2
    1. P(A|B) = P(AB)/P(B): chia cho xác suất của sự kiện đứng sau dấu |.
    2. P(A|B) = (1/5)/(2/5) = 1/2.
- `xs_t3_dk_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Biết tổng số chấm bằng 8. Xác suất có một xúc xắc ra mặt 6 là bao nhiêu?
    - **(đúng)** 2/5
    - 1/6
    - 1/18
    - 1/3
  - **Đáp án:** 2/5
    1. Biết tổng bằng 8, chỉ còn các cặp (2, 6), (3, 5), (4, 4), (5, 3), (6, 2): 5 cặp đồng khả năng.
    2. Có mặt 6: (2, 6) và (6, 2), 2 cặp.
    3. P = 2/5. Đáp án 1/18 = 2/36 sai vì đã quên thu hẹp không gian mẫu.
- `xs_t3_dk_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một lớp có 30 học sinh, trong đó 18 bạn nữ. Có 12 bạn đeo kính, trong đó 8 bạn nữ. Chọn ngẫu nhiên một bạn. Biết bạn đó là nữ, tính xác suất bạn đó đeo kính. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi A: bạn được chọn đeo kính, B: bạn được chọn là nữ. Cần tính P(A|B).
    2. P(AB) = 8/30 vì có 8 bạn nữ đeo kính.
    3. P(A|B) = P(AB)/P(A) = (8/30)/(12/30) = 2/3.   **<- bước sai đầu tiên**
    4. Vậy xác suất cần tìm là 2/3.
  - **Đáp án:** Bước 3: P(A|B) = P(AB)/P(A) = (8/30)/(12/30) = 2/3.
  - **Vì sao sai, và bước đúng:**
    1. P(A|B) chia cho P(B), xác suất của điều kiện đã biết; chia cho P(A) là tính P(B|A), xác suất một bạn đeo kính là nữ.
    2. P(B) = 18/30, nên P(A|B) = (8/30)/(18/30) = 8/18 = 4/9.
- `xs_g3_bang_dieu_kien` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Kết quả một kỳ thi của một lớp: nam có 8 bạn đạt và 22 bạn không đạt; nữ có 29 bạn đạt và 28 bạn không đạt. Chọn ngẫu nhiên một bạn trong lớp. Biết bạn đó là nữ, tính xác suất bạn đó thi đạt.
  - **Đáp án:** 29/57
    1. Điều kiện 'nữ' thu hẹp lớp (87 bạn) lại còn 57 bạn.
    2. Trong 57 bạn đó, có 29 bạn đạt.
    3. P(đạt | nữ) = 29/57 = 29/57.
  - **Câu hỏi:** Kết quả một kỳ thi của một lớp: nam có 5 bạn đạt và 6 bạn không đạt; nữ có 6 bạn đạt và 15 bạn không đạt. Chọn ngẫu nhiên một bạn trong lớp. Biết bạn đó là nam, tính xác suất bạn đó thi đạt.
  - **Đáp án:** 5/11
    1. Điều kiện 'nam' thu hẹp lớp (32 bạn) lại còn 11 bạn.
    2. Trong 11 bạn đó, có 5 bạn đạt.
    3. P(đạt | nam) = 5/11 = 5/11.
  - **Câu hỏi:** Kết quả một kỳ thi của một lớp: nam có 11 bạn đạt và 22 bạn không đạt; nữ có 21 bạn đạt và 8 bạn không đạt. Chọn ngẫu nhiên một bạn trong lớp. Biết bạn đó thi đạt, tính xác suất bạn đó là nữ.
  - **Đáp án:** 21/32
    1. Điều kiện 'đạt' thu hẹp lớp (62 bạn) lại còn 32 bạn.
    2. Trong 32 bạn đó, có 21 bạn nữ.
    3. P(nữ | đạt) = 21/32 = 21/32.
- `xs_t3_dk_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khảo sát 200 người: 120 người dùng điện thoại hãng X và 80 người dùng hãng Y (mỗi người dùng đúng một hãng). Trong số người dùng hãng X có 90 người hài lòng; trong số người dùng hãng Y có 50 người hài lòng. Chọn ngẫu nhiên một người trong 200 người và thấy người đó hài lòng. Tính xác suất người đó dùng hãng Y.
  - **Đáp án:** 5/14
    1. Điều kiện 'hài lòng' thu hẹp về 90 + 50 = 140 người.
    2. Trong 140 người đó có 50 người dùng hãng Y.
    3. P(hãng Y | hài lòng) = 50/140 = 5/14.
- `xs_t3_dk_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai sự kiện A, B có xác suất dương, P(A|B) = P(B|A).
  - **Đáp án:** Sai
    1. P(A|B) = P(AB)/P(B) và P(B|A) = P(AB)/P(A): cùng tử số nhưng khác mẫu số.
    2. Hai số chỉ bằng nhau khi P(A) = P(B).
    3. Ví dụ gieo xúc xắc, A = {6}, B = {2, 4, 6}: P(A|B) = 1/3 còn P(B|A) = 1. Mệnh đề sai.
- `xs_t3_dk_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một gia đình có hai con; mỗi con là trai (T) hay gái (G) đồng khả năng và độc lập với nhau. Biết gia đình có ít nhất một con gái. Sắp xếp các bước tính xác suất cả hai con đều là gái.
  - **Đáp án (thứ tự đúng):**
    1. Không gian mẫu theo thứ tự sinh: TT, TG, GT, GG, bốn kết quả đồng khả năng.
    2. Điều kiện 'có ít nhất một con gái' thu hẹp không gian mẫu còn TG, GT, GG.
    3. Trong ba kết quả còn lại, chỉ có GG là cả hai con đều gái.
    4. Xác suất cần tìm là 1/3.
  - **Lời giải:**
    1. Viết không gian mẫu có thứ tự để các kết quả đồng khả năng.
    2. Bỏ TT vì trái với điều kiện, còn ba kết quả.
    3. Chỉ GG thỏa mãn: P = 1/3, không phải 1/2.
- `xs_t3_dk_08` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một trường có 100 sinh viên: khoa Toán có 30 nam và 20 nữ, khoa Lý có 10 nam và 40 nữ. Chọn ngẫu nhiên một sinh viên. Ghép mỗi xác suất với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - P(nữ) — 3/5
    - P(nữ | khoa Toán) — 2/5
    - P(khoa Toán | nữ) — 1/3
    - P(nam | khoa Lý) — 1/5
  - **Lời giải:**
    1. P(nữ) = (20 + 40)/100 = 3/5.
    2. P(nữ | khoa Toán): trong 50 sinh viên khoa Toán có 20 nữ, 20/50 = 2/5.
    3. P(khoa Toán | nữ): trong 60 sinh viên nữ có 20 ở khoa Toán, 20/60 = 1/3. Đổi chỗ hai sự kiện thì đổi mẫu số.
    4. P(nam | khoa Lý) = 10/50 = 1/5.
- `xs_g3_dieu_kien_xuc_xac` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt xúc xắc thứ nhất và thứ hai. Biết tổng số chấm bằng 5, tính xác suất hai xúc xắc ra cùng số chấm.
  - **Đáp án:** 0
    1. Biết tổng bằng 5, chỉ còn các cặp đồng khả năng: (1, 4), (2, 3), (3, 2), (4, 1); có 4 cặp.
    2. Trong đó có 0 cặp thỏa mãn.
    3. Xác suất có điều kiện là 0/4 = 0.
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt xúc xắc thứ nhất và thứ hai. Biết tổng số chấm bằng 10, tính xác suất hai xúc xắc ra cùng số chấm.
  - **Đáp án:** 1/3
    1. Biết tổng bằng 10, chỉ còn các cặp đồng khả năng: (4, 6), (5, 5), (6, 4); có 3 cặp.
    2. Trong đó có 1 cặp thỏa mãn.
    3. Xác suất có điều kiện là 1/3 = 1/3.
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt xúc xắc thứ nhất và thứ hai. Biết tổng số chấm bằng 5, tính xác suất có ít nhất một xúc xắc ra mặt 6.
  - **Đáp án:** 0
    1. Biết tổng bằng 5, chỉ còn các cặp đồng khả năng: (1, 4), (2, 3), (3, 2), (4, 1); có 4 cặp.
    2. Trong đó có 0 cặp thỏa mãn.
    3. Xác suất có điều kiện là 0/4 = 0.

### Công thức nhân xác suất (`xs_t3_cong_thuc_nhan`)

- `xs_t3_cn_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 2 bi xanh. Lấy lần lượt 2 bi không hoàn lại. Xác suất cả hai bi đều đỏ là 3/5 . 2/4 = 3/10.
  - **Đáp án:** Đúng
    1. Lần 1 đỏ: 3/5.
    2. Biết lần 1 đã lấy một bi đỏ, hộp còn 4 bi với 2 bi đỏ: lần 2 đỏ có xác suất 2/4.
    3. Công thức nhân: 3/5 . 2/4 = 6/20 = 3/10. Mệnh đề đúng.
- `xs_t3_cn_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lô có 10 sản phẩm, trong đó 3 phế phẩm. Lấy lần lượt 2 sản phẩm không hoàn lại. Tính xác suất lần thứ nhất lấy được phế phẩm và lần thứ hai lấy được chính phẩm.
  - **Đáp án:** 7/30
    1. Lần 1 phế phẩm: 3/10.
    2. Biết lần 1 đã lấy đi một phế phẩm, còn 9 sản phẩm với 7 chính phẩm: 7/9.
    3. Nhân lại: 3/10 . 7/9 = 21/90 = 7/30.
- `xs_t3_cn_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Công thức nhân xác suất cho hai sự kiện bất kỳ A, B với P(A) > 0 là công thức nào?
    - **(đúng)** P(AB) = P(A) P(B|A)
    - P(AB) = P(A) P(B)
    - P(AB) = P(A) + P(B)
    - P(AB) = P(A|B) P(B|A)
  - **Đáp án:** P(AB) = P(A) P(B|A)
    1. Từ định nghĩa P(B|A) = P(AB)/P(A), nhân hai vế với P(A) được P(AB) = P(A) P(B|A).
    2. P(AB) = P(A) P(B) chỉ đúng khi A, B độc lập; P(A) + P(B) là công thức của tổng xung khắc, không phải của tích.
- `xs_t3_cn_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một người có 5 chìa khóa trông giống nhau, chỉ đúng 1 chìa mở được cửa. Người đó thử lần lượt từng chìa, chìa nào không mở được thì bỏ ra ngoài. Tính xác suất người đó mở được cửa ở lần thử thứ ba. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Cần xác suất để lần 1 không mở được, lần 2 không mở được và lần 3 mở được.
    2. Lần 1 không mở được với xác suất 4/5.
    3. Biết lần 1 không mở được, lần 2 không mở được với xác suất 4/5.   **<- bước sai đầu tiên**
    4. Biết hai lần đầu không mở được, lần 3 mở được với xác suất 1/3.
    5. Xác suất cần tìm là 4/5 . 4/5 . 1/3 = 16/75.
  - **Đáp án:** Bước 3: Biết lần 1 không mở được, lần 2 không mở được với xác suất 4/5.
  - **Vì sao sai, và bước đúng:**
    1. Chìa đã thử bị bỏ ra, nên ở lần 2 chỉ còn 4 chìa, trong đó 3 chìa sai: xác suất là 3/4.
    2. Đúng là 4/5 . 3/4 . 1/3 = 1/5: mỗi lần thử từ 1 đến 5 đều có cùng xác suất 1/5.
- `xs_g3_khong_hoan_lai` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một lô có 7 sản phẩm, trong đó 3 phế phẩm. Lấy lần lượt 3 sản phẩm không hoàn lại. Tính xác suất cả 3 sản phẩm lấy ra đều là chính phẩm.
  - **Đáp án:** 4/35
    1. Công thức nhân: xác suất của các lần lấy nối tiếp bằng tích các xác suất có điều kiện, mỗi lần tính trên số sản phẩm còn lại.
    2. Lần 1: còn 7 sản phẩm, trong đó 4 chính phẩm, xác suất 4/7.
    3. Lần 2: còn 6 sản phẩm, trong đó 3 chính phẩm, xác suất 3/6.
    4. Lần 3: còn 5 sản phẩm, trong đó 2 chính phẩm, xác suất 2/5.
    5. Nhân lại: (4/7) . (1/2) . (2/5) = 4/35.
  - **Câu hỏi:** Một lô có 12 sản phẩm, trong đó 1 phế phẩm. Lấy lần lượt 2 sản phẩm không hoàn lại. Tính xác suất cả 2 sản phẩm lấy ra đều là chính phẩm.
  - **Đáp án:** 5/6
    1. Công thức nhân: xác suất của các lần lấy nối tiếp bằng tích các xác suất có điều kiện, mỗi lần tính trên số sản phẩm còn lại.
    2. Lần 1: còn 12 sản phẩm, trong đó 11 chính phẩm, xác suất 11/12.
    3. Lần 2: còn 11 sản phẩm, trong đó 10 chính phẩm, xác suất 10/11.
    4. Nhân lại: (11/12) . (10/11) = 5/6.
  - **Câu hỏi:** Một lô có 7 sản phẩm, trong đó 3 phế phẩm. Lấy lần lượt 3 sản phẩm không hoàn lại. Tính xác suất cả 3 sản phẩm lấy ra đều là chính phẩm.
  - **Đáp án:** 4/35
    1. Công thức nhân: xác suất của các lần lấy nối tiếp bằng tích các xác suất có điều kiện, mỗi lần tính trên số sản phẩm còn lại.
    2. Lần 1: còn 7 sản phẩm, trong đó 4 chính phẩm, xác suất 4/7.
    3. Lần 2: còn 6 sản phẩm, trong đó 3 chính phẩm, xác suất 3/6.
    4. Lần 3: còn 5 sản phẩm, trong đó 2 chính phẩm, xác suất 2/5.
    5. Nhân lại: (4/7) . (1/2) . (2/5) = 4/35.
- `xs_t3_cn_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 4 bi đỏ và 6 bi xanh. Lấy lần lượt 3 bi không hoàn lại. Tính xác suất được bi đỏ, bi xanh, bi đỏ theo đúng thứ tự đó.
  - **Đáp án:** 1/10
    1. Lần 1 đỏ: 4/10.
    2. Biết lần 1 đỏ, còn 9 bi với 6 xanh: lần 2 xanh 6/9.
    3. Biết hai lần đầu đỏ, xanh, còn 8 bi với 3 đỏ: lần 3 đỏ 3/8.
    4. Nhân lại: 4/10 . 6/9 . 3/8 = 72/720 = 1/10.
- `xs_t3_cn_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Rút lần lượt 2 lá không hoàn lại từ bộ bài tây 52 lá có 4 lá át. Xác suất cả hai lá đều là át bằng 4/52 . 4/52.
  - **Đáp án:** Sai
    1. Không hoàn lại nên lần 2 phụ thuộc lần 1: biết lần 1 là át, còn 51 lá với 3 lá át.
    2. P = 4/52 . 3/51 = 12/2652 = 1/221.
    3. 4/52 . 4/52 là kết quả của rút có hoàn lại. Mệnh đề sai.
- `xs_t3_cn_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lô có 8 sản phẩm, trong đó 2 phế phẩm. Lấy lần lượt 3 sản phẩm không hoàn lại. Sắp xếp các bước tính xác suất cả 3 sản phẩm đều tốt.
  - **Đáp án (thứ tự đúng):**
    1. Gọi T_i là sự kiện sản phẩm lấy lần thứ i tốt; cần tính P(T_1 T_2 T_3).
    2. Lần 1: P(T_1) = 6/8.
    3. Biết lần 1 tốt, lô còn 7 sản phẩm với 5 sản phẩm tốt: P(T_2 | T_1) = 5/7.
    4. Biết hai lần đầu tốt, lô còn 6 sản phẩm với 4 sản phẩm tốt: P(T_3 | T_1 T_2) = 4/6.
    5. Nhân lại: 6/8 . 5/7 . 4/6 = 5/14.
  - **Lời giải:**
    1. Công thức nhân cho nhiều sự kiện: P(T_1 T_2 T_3) = P(T_1) P(T_2 | T_1) P(T_3 | T_1 T_2).
    2. Mỗi xác suất có điều kiện tính trên lô đã bớt đi các sản phẩm lấy trước.
    3. 6/8 . 5/7 . 4/6 = 120/336 = 5/14.

### Sự kiện độc lập (`xs_t3_doc_lap`)

- `xs_t3_dl_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai sự kiện xung khắc A và B, mỗi sự kiện có xác suất dương, thì không thể độc lập.
  - **Đáp án:** Đúng
    1. Xung khắc nên P(AB) = 0.
    2. Còn P(A) P(B) > 0 vì cả hai xác suất đều dương.
    3. P(AB) khác P(A) P(B) nên A, B không độc lập. Mệnh đề đúng: biết A đã xảy ra thì chắc chắn B không xảy ra, đó là phụ thuộc rất mạnh.
- `xs_t3_dl_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai xạ thủ cùng bắn một phát vào bia, độc lập với nhau. Xác suất bắn trúng của họ lần lượt là 4/5 và 7/10. Tính xác suất cả hai đều bắn trúng.
  - **Đáp án:** 14/25
    1. Hai lần bắn độc lập nên xác suất của tích bằng tích các xác suất.
    2. P = 4/5 . 7/10 = 28/50 = 14/25.
- `xs_t3_dl_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối và tung một đồng xu cân đối. A: xúc xắc ra mặt 6. B: đồng xu ra mặt ngửa. Khẳng định nào đúng?
    - **(đúng)** A và B độc lập, P(AB) = 1/12
    - A và B xung khắc
    - P(AB) = 1/6 + 1/2
    - P(AB) = 1/8
  - **Đáp án:** A và B độc lập, P(AB) = 1/12
    1. Xúc xắc và đồng xu không ảnh hưởng nhau: 12 cặp (số chấm, mặt) đồng khả năng.
    2. AB chỉ có kết quả (6, ngửa): P(AB) = 1/12 = 1/6 . 1/2, nên A, B độc lập.
    3. A, B có thể cùng xảy ra nên không xung khắc.
- `xs_t3_dl_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai sự kiện độc lập A, B với P(A) = 1/3 và P(B) = 1/4. Ghép mỗi sự kiện với xác suất của nó.
  - **Đáp án (ghép đúng):**
    - A và B cùng xảy ra — 1/12
    - A xảy ra, B không xảy ra — 1/4
    - B xảy ra, A không xảy ra — 1/6
    - Cả A và B đều không xảy ra — 1/2
  - **Lời giải:**
    1. A, B độc lập thì A với sự kiện đối của B, Ā với B, Ā với sự kiện đối của B cũng độc lập.
    2. 1/3 . 1/4 = 1/12; 1/3 . 3/4 = 1/4; 2/3 . 1/4 = 1/6; 2/3 . 3/4 = 1/2.
    3. Bốn trường hợp phủ hết mọi khả năng: 1/12 + 3/12 + 2/12 + 6/12 = 1.
- `xs_t3_dl_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Gieo một con xúc xắc cân đối. A: ra mặt chẵn, B: ra mặt lẻ. Hỏi A và B có độc lập không? Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. A = {2, 4, 6} và B = {1, 3, 5}, nên P(A) = P(B) = 1/2.
    2. A và B không có kết quả chung, nên P(AB) = 0.
    3. Hai sự kiện không có kết quả chung thì độc lập.   **<- bước sai đầu tiên**
    4. Vậy A và B độc lập.
  - **Đáp án:** Bước 3: Hai sự kiện không có kết quả chung thì độc lập.
  - **Vì sao sai, và bước đúng:**
    1. Không có kết quả chung là xung khắc, không phải độc lập. Độc lập phải kiểm tra P(AB) = P(A) P(B).
    2. Ở đây P(A) P(B) = 1/4 khác P(AB) = 0, nên A và B không độc lập: biết A xảy ra thì chắc chắn B không xảy ra.
- `xs_g3_doc_lap_ban` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hai xạ thủ cùng bắn một phát vào bia, độc lập với nhau. Xác suất bắn trúng của người thứ nhất là 3/4, của người thứ hai là 2/3. Tính xác suất có đúng một người bắn trúng.
  - **Đáp án:** 5/12
    1. Đúng một người trúng gồm hai trường hợp xung khắc: người 1 trúng, người 2 trượt; hoặc người 1 trượt, người 2 trúng.
    2. 3/4 . 1/3 + 1/4 . 2/3 = 1/4 + 1/6 = 5/12.
  - **Câu hỏi:** Hai xạ thủ cùng bắn một phát vào bia, độc lập với nhau. Xác suất bắn trúng của người thứ nhất là 1/2, của người thứ hai là 2/3. Tính xác suất có ít nhất một người bắn trúng.
  - **Đáp án:** 5/6
    1. Sự kiện đối là cả hai cùng trượt: 1/2 . 1/3 = 1/6 (nhân vì độc lập).
    2. Xác suất cần tìm là 1 - 1/6 = 5/6.
  - **Câu hỏi:** Hai xạ thủ cùng bắn một phát vào bia, độc lập với nhau. Xác suất bắn trúng của người thứ nhất là 3/5, của người thứ hai là 3/4. Tính xác suất có đúng một người bắn trúng.
  - **Đáp án:** 9/20
    1. Đúng một người trúng gồm hai trường hợp xung khắc: người 1 trúng, người 2 trượt; hoặc người 1 trượt, người 2 trúng.
    2. 3/5 . 1/4 + 2/5 . 3/4 = 3/20 + 3/10 = 9/20.
- `xs_t3_dl_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ba bóng đèn hoạt động độc lập với nhau. Xác suất mỗi bóng hỏng trong một tháng lần lượt là 1/10, 1/5 và 1/4. Tính xác suất trong tháng có đúng một bóng hỏng.
  - **Đáp án:** 3/8
    1. Đúng một bóng hỏng gồm ba trường hợp xung khắc: chỉ bóng 1 hỏng, chỉ bóng 2 hỏng, chỉ bóng 3 hỏng.
    2. Chỉ bóng 1 hỏng: 1/10 . 4/5 . 3/4 = 12/200. Chỉ bóng 2: 9/10 . 1/5 . 3/4 = 27/200. Chỉ bóng 3: 9/10 . 4/5 . 1/4 = 36/200.
    3. Cộng lại: 75/200 = 3/8.
- `xs_t3_dl_07` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. A: xúc xắc thứ nhất ra mặt chẵn. B: tổng số chấm bằng 7. Hai sự kiện A và B độc lập.
  - **Đáp án:** Đúng
    1. P(A) = 18/36 = 1/2. B gồm 6 cặp (1, 6), (2, 5), ..., (6, 1), nên P(B) = 1/6.
    2. AB: xúc xắc thứ nhất chẵn và tổng 7, gồm (2, 5), (4, 3), (6, 1): P(AB) = 3/36 = 1/12.
    3. P(A) P(B) = 1/2 . 1/6 = 1/12 = P(AB), nên A và B độc lập. Mệnh đề đúng.
- `xs_t3_dl_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một mạch điện gồm hai linh kiện mắc song song, hoạt động độc lập; mỗi linh kiện tốt với xác suất 9/10. Mạch thông khi có ít nhất một linh kiện tốt. Xác suất mạch thông là bao nhiêu?
    - **(đúng)** 99/100
    - 81/100
    - 9/5
    - 1/100
  - **Đáp án:** 99/100
    1. Mạch không thông khi cả hai linh kiện cùng hỏng: 1/10 . 1/10 = 1/100 (nhân vì độc lập).
    2. P(mạch thông) = 1 - 1/100 = 99/100.
    3. 81/100 là xác suất cả hai cùng tốt, ứng với mạch mắc nối tiếp.
- `xs_g3_doc_lap_tf` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối. A là sự kiện ra số chấm chia hết cho 3, B là sự kiện số chấm nhỏ hơn hoặc bằng 5. Hai sự kiện A và B độc lập.
  - **Đáp án:** Sai
    1. P(A) = 1/3, P(B) = 5/6, nên P(A) P(B) = 5/18.
    2. AB = {3}, nên P(AB) = 1/6.
    3. P(AB) != P(A) P(B), nên A và B không độc lập.
  - **Câu hỏi:** Gieo một con xúc xắc cân đối. A là sự kiện ra số chấm chẵn, B là sự kiện số chấm nhỏ hơn hoặc bằng 1. Hai sự kiện A và B độc lập.
  - **Đáp án:** Sai
    1. P(A) = 1/2, P(B) = 1/6, nên P(A) P(B) = 1/12.
    2. A và B không có kết quả chung, nên P(AB) = 0.
    3. P(AB) != P(A) P(B), nên A và B không độc lập.
  - **Câu hỏi:** Gieo một con xúc xắc cân đối. A là sự kiện ra số chấm chia hết cho 3, B là sự kiện số chấm nhỏ hơn hoặc bằng 5. Hai sự kiện A và B độc lập.
  - **Đáp án:** Sai
    1. P(A) = 1/3, P(B) = 5/6, nên P(A) P(B) = 5/18.
    2. AB = {3}, nên P(AB) = 1/6.
    3. P(AB) != P(A) P(B), nên A và B không độc lập.

### Công thức Bernoulli (`xs_t3_bernoulli`)

- `xs_t3_bn_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu cân đối 4 lần. Xác suất được đúng 2 lần ngửa là C(4, 2) (1/2)^4 = 3/8.
  - **Đáp án:** Đúng
    1. 4 lần tung độc lập, mỗi lần ngửa với p = 1/2: công thức Bernoulli với n = 4, k = 2.
    2. C(4, 2) (1/2)^2 (1/2)^2 = 6/16 = 3/8. Mệnh đề đúng.
- `xs_t3_bn_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ bắn 3 phát độc lập, xác suất trúng mỗi phát là 2/3. Tính xác suất có đúng 2 phát trúng.
  - **Đáp án:** 4/9
    1. Công thức Bernoulli với n = 3, k = 2, p = 2/3.
    2. C(3, 2) (2/3)^2 (1/3)^1 = 3 . 4/9 . 1/3 = 12/27 = 4/9.
- `xs_t3_bn_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điều nào sau đây KHÔNG cần có để một dãy phép thử là dãy phép thử Bernoulli?
    - **(đúng)** Sự kiện A và Ā có cùng xác suất 1/2
    - Các phép thử độc lập với nhau
    - Mỗi phép thử chỉ quan tâm A xảy ra hay không
    - Xác suất của A như nhau ở mọi phép thử
  - **Đáp án:** Sự kiện A và Ā có cùng xác suất 1/2
    1. Dãy Bernoulli cần: các phép thử độc lập, mỗi lần chỉ xét A xảy ra hay không, và P(A) = p như nhau ở mọi lần.
    2. p có thể là bất kỳ số nào trong khoảng (0, 1), không cần bằng 1/2: ví dụ gieo xúc xắc và xét mặt 6 có p = 1/6.
- `xs_t3_bn_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Gieo một con xúc xắc cân đối 4 lần. Tính xác suất có đúng 1 lần ra mặt 6. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Bốn lần gieo độc lập, mỗi lần ra mặt 6 với xác suất p = 1/6.
    2. Xác suất mặt 6 ra ở lần thứ nhất và không ra ở ba lần sau là (1/6)(5/6)^3.
    3. Vậy xác suất có đúng 1 lần ra mặt 6 là (1/6)(5/6)^3 = 125/1296.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Vậy xác suất có đúng 1 lần ra mặt 6 là (1/6)(5/6)^3 = 125/1296.
  - **Vì sao sai, và bước đúng:**
    1. Lần ra mặt 6 có thể là lần 1, 2, 3 hoặc 4: có C(4, 1) = 4 trường hợp xung khắc, mỗi trường hợp có cùng xác suất (1/6)(5/6)^3.
    2. Đúng là 4 . 125/1296 = 500/1296 = 125/324.
- `xs_g3_bernoulli` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một phép thử là: một xạ thủ bắn một phát, trúng với xác suất 1/3. Làm phép thử đó 3 lần độc lập. Tính xác suất có đúng 2 phát bắn trúng.
  - **Đáp án:** 2/9
    1. Đây là 3 phép thử Bernoulli với xác suất thành công p = 1/3 ở mỗi lần.
    2. Công thức Bernoulli: P = C(3, 2) p^2 (1 - p)^1.
    3. P = 3 . (1/3)^2 . (2/3)^1 = 2/9.
  - **Câu hỏi:** Một phép thử là: tung một đồng xu cân đối. Làm phép thử đó 3 lần độc lập. Tính xác suất có đúng 0 lần tung ra mặt ngửa.
  - **Đáp án:** 1/8
    1. Đây là 3 phép thử Bernoulli với xác suất thành công p = 1/2 ở mỗi lần.
    2. Công thức Bernoulli: P = C(3, 0) p^0 (1 - p)^3.
    3. P = 1 . (1/2)^0 . (1/2)^3 = 1/8.
  - **Câu hỏi:** Một phép thử là: một xạ thủ bắn một phát, trúng với xác suất 1/3. Làm phép thử đó 4 lần độc lập. Tính xác suất có đúng 2 phát bắn trúng.
  - **Đáp án:** 8/27
    1. Đây là 4 phép thử Bernoulli với xác suất thành công p = 1/3 ở mỗi lần.
    2. Công thức Bernoulli: P = C(4, 2) p^2 (1 - p)^2.
    3. P = 6 . (1/3)^2 . (2/3)^2 = 8/27.
- `xs_t3_bn_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bài thi có 5 câu trắc nghiệm, mỗi câu có 4 phương án trong đó chỉ 1 phương án đúng. Một thí sinh chọn ngẫu nhiên một phương án ở mỗi câu, độc lập giữa các câu. Tính xác suất thí sinh trả lời đúng ít nhất 4 câu.
  - **Đáp án:** 1/64
    1. Đây là 5 phép thử Bernoulli với p = 1/4.
    2. Đúng 4 câu: C(5, 4) (1/4)^4 (3/4) = 5 . 3/1024 = 15/1024. Đúng 5 câu: (1/4)^5 = 1/1024.
    3. Cộng lại: 16/1024 = 1/64.
- `xs_t3_bn_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu cân đối 6 lần. Trong các giá trị k = 0, 1, 2, ..., 6, xác suất có đúng k lần ngửa lớn nhất khi k = 3.
  - **Đáp án:** Đúng
    1. P(đúng k lần ngửa) = C(6, k)/64.
    2. C(6, k) với k = 0..6 là 1, 6, 15, 20, 15, 6, 1, lớn nhất tại k = 3.
    3. Vậy k = 3 có xác suất lớn nhất, 20/64 = 5/16. Mệnh đề đúng.
- `xs_t3_bn_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi sản phẩm của một máy là phế phẩm với xác suất 1/10, độc lập với các sản phẩm khác. Sắp xếp các bước tính xác suất trong 3 sản phẩm có ít nhất 1 phế phẩm.
  - **Đáp án (thứ tự đúng):**
    1. Xét 3 phép thử Bernoulli, với p = 1/10 là xác suất một sản phẩm là phế phẩm.
    2. Với p đó, xác suất một sản phẩm tốt là 1 - p = 9/10.
    3. Sự kiện đối của 'ít nhất 1 phế phẩm' là 'cả 3 sản phẩm đều tốt', có xác suất (9/10)^3 = 729/1000.
    4. Xác suất cần tìm là 1 - 729/1000 = 271/1000.
  - **Lời giải:**
    1. Nhận ra mô hình Bernoulli với n = 3, p = 1/10.
    2. 'Ít nhất 1' tính nhanh qua sự kiện đối: cả 3 đều tốt, (9/10)^3.
    3. P = 1 - 729/1000 = 271/1000.
- `xs_t3_bn_08` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ bắn 3 phát độc lập, mỗi phát trúng với xác suất 1/3. Ghép số phát trúng với xác suất của nó.
  - **Đáp án (ghép đúng):**
    - Không phát nào trúng — 8/27
    - Đúng 1 phát trúng — 4/9
    - Đúng 2 phát trúng — 2/9
    - Cả 3 phát trúng — 1/27
  - **Lời giải:**
    1. Công thức Bernoulli với n = 3, p = 1/3, 1 - p = 2/3.
    2. k = 0: (2/3)^3 = 8/27. k = 1: 3 . (1/3)(4/9) = 12/27 = 4/9.
    3. k = 2: 3 . (1/9)(2/3) = 6/27 = 2/9. k = 3: (1/3)^3 = 1/27.
    4. Kiểm tra: 8 + 12 + 6 + 1 = 27, tổng các xác suất bằng 1.
- `xs_g3_bernoulli_it_nhat` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một phép thử là: một xạ thủ bắn một phát, trúng với xác suất 1/3. Làm phép thử đó 3 lần độc lập. Tính xác suất có ít nhất 2 phát bắn trúng.
  - **Đáp án:** 7/27
    1. Đây là 3 phép thử Bernoulli với p = 1/3.
    2. Cộng các trường hợp xung khắc j = 2, ..., 3, mỗi trường hợp tính bằng C(3, j) p^j (1 - p)^(3 - j).
    3. P = 2/9 + 1/27 = 7/27.
  - **Câu hỏi:** Một phép thử là: tung một đồng xu cân đối. Làm phép thử đó 3 lần độc lập. Tính xác suất có ít nhất 1 lần tung ra mặt ngửa.
  - **Đáp án:** 7/8
    1. Đây là 3 phép thử Bernoulli với p = 1/2.
    2. Sự kiện đối là không lần tung nào ra mặt ngửa: (1 - p)^3 = (1/2)^3 = 1/8.
    3. Xác suất cần tìm là 1 - 1/8 = 7/8.
  - **Câu hỏi:** Một phép thử là: một xạ thủ bắn một phát, trúng với xác suất 1/3. Làm phép thử đó 4 lần độc lập. Tính xác suất có ít nhất 3 phát bắn trúng.
  - **Đáp án:** 1/9
    1. Đây là 4 phép thử Bernoulli với p = 1/3.
    2. Cộng các trường hợp xung khắc j = 3, ..., 4, mỗi trường hợp tính bằng C(4, j) p^j (1 - p)^(4 - j).
    3. P = 8/81 + 1/81 = 1/9.

## Tầng 4: Công thức xác suất đầy đủ và công thức Bayes

46 dạng câu (40 câu viết tay, 6 bộ sinh câu); 46 chưa duyệt.

### Hệ đầy đủ các sự kiện (`xs_t4_he_day_du`)

- `xs_t4_hd_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt. H_1 = {1, 2}, H_2 = {3, 4}, H_3 = {5, 6}. Ba sự kiện H_1, H_2, H_3 lập thành một hệ đầy đủ.
  - **Đáp án:** Đúng
    1. Hệ đầy đủ cần hai điều: các sự kiện đôi một xung khắc, và tổng của chúng là sự kiện chắc chắn.
    2. Ba tập không có phần tử chung, nên đôi một xung khắc.
    3. Hợp của chúng là {1, 2, 3, 4, 5, 6}, cả không gian mẫu. Mệnh đề đúng.
- `xs_t4_hd_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt. Họ sự kiện nào dưới đây là một hệ đầy đủ?
    - **(đúng)** {1}, {2, 3}, {4, 5, 6}
    - {1, 2}, {2, 3, 4}, {5, 6}
    - {1, 2}, {3, 4}
    - {1, 3, 5}, {2, 4}
  - **Đáp án:** {1}, {2, 3}, {4, 5, 6}
    1. {1}, {2, 3}, {4, 5, 6} không có phần tử chung và phủ đủ 1 đến 6: là hệ đầy đủ.
    2. {1, 2}, {2, 3, 4}, {5, 6}: mặt 2 thuộc hai sự kiện, nên không xung khắc.
    3. {1, 2}, {3, 4} thiếu mặt 5, 6; {1, 3, 5}, {2, 4} thiếu mặt 6: tổng chưa phải sự kiện chắc chắn.
- `xs_t4_hd_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** H_1, H_2, H_3 là một hệ đầy đủ các sự kiện với P(H_1) = 1/4 và P(H_2) = 1/3. Tính P(H_3).
  - **Đáp án:** 5/12
    1. Các sự kiện của một hệ đầy đủ đôi một xung khắc và tổng là sự kiện chắc chắn, nên P(H_1) + P(H_2) + P(H_3) = 1.
    2. P(H_3) = 1 - 1/4 - 1/3 = 12/12 - 3/12 - 4/12 = 5/12.
- `xs_t4_hd_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Trong một lớp, 3/5 số sinh viên học tiếng Anh, 1/2 số sinh viên học tiếng Pháp, và mỗi sinh viên học ít nhất một trong hai thứ tiếng. Chọn ngẫu nhiên một sinh viên. Một bạn lập luận như dưới đây. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi H_1: sinh viên đó học tiếng Anh, H_2: sinh viên đó học tiếng Pháp.
    2. Mỗi sinh viên học ít nhất một thứ tiếng, nên H_1 + H_2 là sự kiện chắc chắn.
    3. Vậy H_1, H_2 là một hệ đầy đủ, nên P(H_1) + P(H_2) = 1.   **<- bước sai đầu tiên**
    4. Nhưng 3/5 + 1/2 = 11/10 > 1, nên đề bài vô lý.
  - **Đáp án:** Bước 3: Vậy H_1, H_2 là một hệ đầy đủ, nên P(H_1) + P(H_2) = 1.
  - **Vì sao sai, và bước đúng:**
    1. Tổng là sự kiện chắc chắn chưa đủ: hệ đầy đủ còn cần các sự kiện đôi một xung khắc.
    2. Ở đây có người học cả hai thứ tiếng: P(H_1 H_2) = 3/5 + 1/2 - 1 = 1/10 > 0, nên H_1, H_2 không xung khắc và đề không vô lý.
    3. Một hệ đầy đủ đúng là: chỉ học tiếng Anh (1/2), chỉ học tiếng Pháp (2/5), học cả hai (1/10); tổng bằng 1.
- `xs_g4_he_day_du_tf` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt và ghi số chấm. Xét họ sự kiện H_1 = {1, 3, 4, 6}, H_2 = {5}, H_3 = {2, 6}. Họ này là một hệ đầy đủ các sự kiện.
  - **Đáp án:** Sai
    1. Hệ đầy đủ: các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn.
    2. Mặt 6 thuộc hai sự kiện của họ.
    3. Hai sự kiện đó không xung khắc, nên họ này không là hệ đầy đủ.
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt và ghi số chấm. Xét họ sự kiện H_1 = {2, 3, 4}, H_2 = {5}, H_3 = {6}, H_4 = {1}. Họ này là một hệ đầy đủ các sự kiện.
  - **Đáp án:** Đúng
    1. Hệ đầy đủ: các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn.
    2. Mỗi mặt từ 1 đến 6 nằm trong đúng một sự kiện của họ.
    3. Vậy các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn: đó là hệ đầy đủ.
  - **Câu hỏi:** Gieo một con xúc xắc sáu mặt và ghi số chấm. Xét họ sự kiện H_1 = {1}, H_2 = {3, 4}, H_3 = {5, 6}, H_4 = {2}. Họ này là một hệ đầy đủ các sự kiện.
  - **Đáp án:** Đúng
    1. Hệ đầy đủ: các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn.
    2. Mỗi mặt từ 1 đến 6 nằm trong đúng một sự kiện của họ.
    3. Vậy các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn: đó là hệ đầy đủ.
- `xs_t4_hd_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi sự kiện A của một phép thử, hai sự kiện A và Ā (sự kiện đối của A) lập thành một hệ đầy đủ.
  - **Đáp án:** Đúng
    1. A và Ā không thể cùng xảy ra, nên xung khắc.
    2. Trong mỗi lần thử, A xảy ra hoặc không xảy ra, nên A + Ā là sự kiện chắc chắn.
    3. Vậy {A, Ā} luôn là một hệ đầy đủ; đó là hệ đầy đủ đơn giản nhất, hay dùng nhất trong công thức xác suất đầy đủ. Mệnh đề đúng.
- `xs_t4_hd_06` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Rút ngẫu nhiên một lá từ bộ bài tây 52 lá (4 chất cơ, rô, bích, nhép; cơ và rô màu đỏ, bích và nhép màu đen). Ghép mỗi họ sự kiện với nhận xét đúng về nó.
  - **Đáp án (ghép đúng):**
    - Lá đỏ; lá đen — Hệ đầy đủ gồm 2 sự kiện
    - Lá cơ; lá rô; lá bích; lá nhép — Hệ đầy đủ gồm 4 sự kiện
    - Lá cơ; lá rô; lá bích — Đôi một xung khắc nhưng tổng chưa là sự kiện chắc chắn
    - Lá đỏ; lá cơ; lá đen — Tổng là sự kiện chắc chắn nhưng không đôi một xung khắc
  - **Lời giải:**
    1. Mỗi lá có đúng một màu và đúng một chất: {đỏ, đen} và {cơ, rô, bích, nhép} là hai hệ đầy đủ.
    2. {cơ, rô, bích} đôi một xung khắc nhưng một lá nhép không thuộc sự kiện nào.
    3. {đỏ, cơ, đen} phủ hết bộ bài, nhưng mỗi lá cơ vừa là lá đỏ vừa là lá cơ, nên không xung khắc.
- `xs_t4_hd_07` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** H_1, H_2, H_3 là một hệ đầy đủ các sự kiện, trong đó P(H_1) = 2P(H_2) và P(H_2) = 2P(H_3). Tính P(H_1).
  - **Đáp án:** 4/7
    1. Đặt P(H_3) = t, thì P(H_2) = 2t và P(H_1) = 4t.
    2. Hệ đầy đủ nên 4t + 2t + t = 1, tức t = 1/7.
    3. P(H_1) = 4/7.
- `xs_t4_hd_08` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. H_1: tổng số chấm <= 5; H_2: tổng từ 6 đến 8; H_3: tổng >= 9. Sắp xếp các bước chứng tỏ đây là hệ đầy đủ rồi tính P(H_2).
  - **Đáp án (thứ tự đúng):**
    1. Tổng số chấm nhận các giá trị từ 2 đến 12.
    2. Mỗi giá trị tổng thuộc đúng một trong ba nhóm (<= 5, từ 6 đến 8, >= 9), nên H_1, H_2, H_3 đôi một xung khắc và tổng của chúng là sự kiện chắc chắn.
    3. Vậy H_1, H_2, H_3 là hệ đầy đủ, nên P(H_1) + P(H_2) + P(H_3) = 1.
    4. Đếm trong 36 cặp: H_1 có 10 cặp và H_3 có 10 cặp, nên P(H_2) = 1 - 20/36 = 4/9.
  - **Lời giải:**
    1. Trước hết biết tổng có thể nhận những giá trị nào, rồi thấy mỗi giá trị rơi vào đúng một nhóm.
    2. Từ đó ba sự kiện là hệ đầy đủ và xác suất của chúng cộng lại bằng 1.
    3. Tổng 2, 3, 4, 5 có 1 + 2 + 3 + 4 = 10 cặp; tổng 9, 10, 11, 12 có 4 + 3 + 2 + 1 = 10 cặp; P(H_2) = 16/36 = 4/9.

### Sơ đồ cây cho phép thử nhiều giai đoạn (`xs_t4_so_do_cay`)

- `xs_t4_sc_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 2 bi đỏ và 3 bi xanh; hộp II có 4 bi đỏ và 1 bi xanh. Tung một đồng xu cân đối: ngửa thì chọn hộp I, sấp thì chọn hộp II; rồi lấy ngẫu nhiên 1 bi từ hộp đã chọn. Xác suất chọn hộp I và lấy được bi đỏ là 1/2 . 2/5 = 1/5.
  - **Đáp án:** Đúng
    1. Trên sơ đồ cây, nhánh đầu là chọn hộp I với xác suất 1/2.
    2. Nhánh tiếp theo ghi xác suất có điều kiện P(đỏ | hộp I) = 2/5.
    3. Nhân dọc đường đi: 1/2 . 2/5 = 1/5. Mệnh đề đúng.
- `xs_t4_sc_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ chọn ngẫu nhiên 1 trong 3 khẩu súng: 1 khẩu loại A, bắn trúng với xác suất 4/5, và 2 khẩu loại B, bắn trúng với xác suất 1/2. Xạ thủ bắn một phát bằng khẩu đã chọn. Tính xác suất xạ thủ chọn khẩu loại B và bắn trượt.
  - **Đáp án:** 1/3
    1. Nhánh đầu: chọn khẩu loại B với xác suất 2/3.
    2. Nhánh sau: với khẩu loại B, bắn trượt có xác suất 1 - 1/2 = 1/2.
    3. Nhân dọc đường đi: 2/3 . 1/2 = 1/3.
- `xs_t4_sc_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phép thử: chọn một hộp rồi lấy một bi từ hộp đó. Trên sơ đồ cây, con số ghi trên nhánh đi từ nút 'hộp I' đến nút 'bi đỏ' là gì?
    - **(đúng)** P(bi đỏ | hộp I)
    - P(hộp I | bi đỏ)
    - P(chọn hộp I và lấy bi đỏ)
    - P(bi đỏ)
  - **Đáp án:** P(bi đỏ | hộp I)
    1. Mỗi nhánh ở tầng sau ghi xác suất của bước đó khi đã biết các bước trước: đã chọn hộp I, lấy được bi đỏ có xác suất P(bi đỏ | hộp I).
    2. P(chọn hộp I và lấy bi đỏ) là tích dọc cả đường đi, không phải số trên một nhánh.
    3. P(hộp I | bi đỏ) là câu hỏi ngược chiều, cần công thức Bayes.
- `xs_t4_sc_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ngày mai nắng với xác suất 3/5, mưa với xác suất 2/5. Nếu nắng, An đi bộ đến trường với xác suất 3/4; nếu mưa, An đi bộ với xác suất 1/4; không đi bộ thì An đi xe buýt. Ghép mỗi đường đi trên sơ đồ cây với xác suất của nó.
  - **Đáp án (ghép đúng):**
    - Nắng và An đi bộ — 9/20
    - Nắng và An đi xe buýt — 3/20
    - Mưa và An đi bộ — 1/10
    - Mưa và An đi xe buýt — 3/10
  - **Lời giải:**
    1. Nhân dọc mỗi đường đi: xác suất của thời tiết nhân xác suất có điều kiện của cách đi.
    2. 3/5 . 3/4 = 9/20; 3/5 . 1/4 = 3/20; 2/5 . 1/4 = 1/10; 2/5 . 3/4 = 3/10.
    3. Kiểm tra: 9/20 + 3/20 + 2/20 + 6/20 = 1, các đường đi phủ hết mọi khả năng.
- `xs_g4_cay_hai_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 5 bi đỏ và 1 bi xanh; hộp II có 3 bi đỏ và 1 bi xanh. Gieo một con xúc xắc cân đối: nếu ra mặt từ 1 đến 2 thì chọn hộp I, còn lại chọn hộp II; rồi lấy ngẫu nhiên 1 bi từ hộp đã chọn. Tính xác suất chọn được hộp II và lấy được bi xanh.
  - **Đáp án:** 1/6
    1. Nhánh thứ nhất của sơ đồ cây: chọn hộp II với xác suất 2/3.
    2. Nhánh thứ hai: hộp II có 3 bi đỏ, 1 bi xanh, nên lấy được bi xanh với xác suất có điều kiện 1/4.
    3. Nhân dọc đường đi: (2/3) . (1/4) = 1/6.
  - **Câu hỏi:** Hộp I có 1 bi đỏ và 1 bi xanh; hộp II có 3 bi đỏ và 2 bi xanh. Gieo một con xúc xắc cân đối: nếu ra mặt 1 thì chọn hộp I, còn lại chọn hộp II; rồi lấy ngẫu nhiên 1 bi từ hộp đã chọn. Tính xác suất chọn được hộp II và lấy được bi xanh.
  - **Đáp án:** 1/3
    1. Nhánh thứ nhất của sơ đồ cây: chọn hộp II với xác suất 5/6.
    2. Nhánh thứ hai: hộp II có 3 bi đỏ, 2 bi xanh, nên lấy được bi xanh với xác suất có điều kiện 2/5.
    3. Nhân dọc đường đi: (5/6) . (2/5) = 1/3.
  - **Câu hỏi:** Hộp I có 5 bi đỏ và 5 bi xanh; hộp II có 2 bi đỏ và 3 bi xanh. Gieo một con xúc xắc cân đối: nếu ra mặt từ 1 đến 2 thì chọn hộp I, còn lại chọn hộp II; rồi lấy ngẫu nhiên 1 bi từ hộp đã chọn. Tính xác suất chọn được hộp II và lấy được bi đỏ.
  - **Đáp án:** 4/15
    1. Nhánh thứ nhất của sơ đồ cây: chọn hộp II với xác suất 2/3.
    2. Nhánh thứ hai: hộp II có 2 bi đỏ, 3 bi xanh, nên lấy được bi đỏ với xác suất có điều kiện 2/5.
    3. Nhân dọc đường đi: (2/3) . (2/5) = 4/15.
- `xs_t4_sc_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đệ tử thi ba vòng để vào nội môn, thi trượt vòng nào thì dừng ở vòng đó. Đệ tử qua vòng 1 với xác suất 4/5; nếu đã qua vòng 1 thì qua vòng 2 với xác suất 3/4; nếu đã qua hai vòng đầu thì qua vòng 3 với xác suất 2/3. Tính xác suất đệ tử bị loại ở vòng 3.
  - **Đáp án:** 1/5
    1. Bị loại ở vòng 3 là đường đi: qua vòng 1, qua vòng 2, trượt vòng 3.
    2. Các nhánh: 4/5, rồi 3/4, rồi 1 - 2/3 = 1/3.
    3. Nhân dọc đường đi: 4/5 . 3/4 . 1/3 = 12/60 = 1/5.
- `xs_t4_sc_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 3 bi đỏ và 2 bi xanh. Lấy lần lượt 2 bi không hoàn lại. Tính xác suất hai bi khác màu. Lời giải dưới đây dùng sơ đồ cây và có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Tầng thứ nhất của cây: bi đầu đỏ với xác suất 3/5, xanh với xác suất 2/5.
    2. Từ nhánh đỏ: còn 4 bi với 2 bi xanh, nên bi sau xanh với xác suất 2/4.
    3. Từ nhánh xanh: bi sau đỏ với xác suất 3/5.   **<- bước sai đầu tiên**
    4. P(khác màu) = 3/5 . 2/4 + 2/5 . 3/5 = 3/10 + 6/25 = 27/50.
  - **Đáp án:** Bước 3: Từ nhánh xanh: bi sau đỏ với xác suất 3/5.
  - **Vì sao sai, và bước đúng:**
    1. Số ghi trên nhánh tầng hai phải tính trên hộp sau khi đã lấy bi đầu: sau khi lấy 1 bi xanh, hộp còn 4 bi với 3 bi đỏ, xác suất là 3/4.
    2. P(khác màu) = 3/5 . 2/4 + 2/5 . 3/4 = 3/10 + 3/10 = 3/5.
- `xs_t4_sc_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 3 bi trắng và 1 bi đen; hộp II có 1 bi trắng và 3 bi đen. Gieo một con xúc xắc cân đối: ra mặt 1 hoặc 2 thì chọn hộp I, còn lại chọn hộp II; rồi lấy 1 bi từ hộp đã chọn. Sắp xếp các bước tính xác suất lấy được bi trắng bằng sơ đồ cây.
  - **Đáp án (thứ tự đúng):**
    1. Tầng thứ nhất của cây: hộp I với xác suất 1/3, hộp II với xác suất 2/3.
    2. Tầng thứ hai: từ hộp I, bi trắng với xác suất 3/4; từ hộp II, bi trắng với xác suất 1/4.
    3. Nhân dọc hai đường đi kết thúc ở bi trắng: 1/3 . 3/4 = 1/4 và 2/3 . 1/4 = 1/6.
    4. Cộng hai đường đi đó: 1/4 + 1/6 = 5/12.
  - **Lời giải:**
    1. Vẽ cây theo đúng thứ tự của phép thử: chọn hộp trước, lấy bi sau.
    2. Nhân dọc mỗi đường đi, rồi cộng các đường đi dẫn đến bi trắng.
    3. Kết quả 5/12.
- `xs_t4_sc_08` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 2 bi đỏ và 2 bi xanh. Lấy lần lượt từng bi, không hoàn lại, cho đến khi lấy được bi đỏ thì dừng. Xác suất phải lấy đúng 3 lần là 1/6.
  - **Đáp án:** Đúng
    1. Lấy đúng 3 lần là đường đi: xanh, xanh, rồi đỏ.
    2. Các nhánh: xanh 2/4; còn 3 bi với 1 xanh, xanh 1/3; còn 2 bi đều đỏ, đỏ 2/2 = 1.
    3. Nhân dọc: 2/4 . 1/3 . 1 = 1/6. Mệnh đề đúng.

### Công thức xác suất đầy đủ (`xs_t4_day_du`)

- `xs_t4_dd_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một nhà máy có hai phân xưởng. Phân xưởng I làm 3/5 số sản phẩm, với tỉ lệ phế phẩm 1/20; phân xưởng II làm 2/5 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm của nhà máy. Tính xác suất sản phẩm đó là phế phẩm.
  - **Đáp án:** 7/100
    1. Hệ đầy đủ: H_1, H_2 là sản phẩm do phân xưởng I, II làm ra; A là phế phẩm.
    2. P(A) = P(H_1) P(A|H_1) + P(H_2) P(A|H_2) = 3/5 . 1/20 + 2/5 . 1/10.
    3. = 3/100 + 4/100 = 7/100.
- `xs_t4_dd_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi sự kiện A và mọi hai sự kiện H_1, H_2 có xác suất dương (không cần xung khắc, không cần tổng là sự kiện chắc chắn), ta có P(A) = P(H_1) P(A|H_1) + P(H_2) P(A|H_2).
  - **Đáp án:** Sai
    1. Công thức xác suất đầy đủ chỉ đúng khi H_1, H_2 là một hệ đầy đủ.
    2. Phản ví dụ: lấy H_1 = H_2 = sự kiện chắc chắn. Vế phải là P(A) + P(A) = 2P(A), khác P(A) khi P(A) > 0.
    3. Mệnh đề sai.
- `xs_t4_dd_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 2 bi đỏ và 2 bi xanh; hộp II có 3 bi đỏ và 1 bi xanh. Chọn ngẫu nhiên một hộp (mỗi hộp xác suất 1/2), rồi lấy ngẫu nhiên 1 bi từ hộp đó. Xác suất lấy được bi đỏ là bao nhiêu?
    - **(đúng)** 5/8
    - 5/16
    - 1/2
    - 3/4
  - **Đáp án:** 5/8
    1. Hệ đầy đủ: chọn hộp I hoặc hộp II, mỗi hộp xác suất 1/2.
    2. P(đỏ) = 1/2 . 2/4 + 1/2 . 3/4 = 1/4 + 3/8 = 5/8.
    3. 5/16 là quên nhân 2 nhánh lại đủ, 3/4 là chỉ nhìn hộp II.
- `xs_t4_dd_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Ba máy làm lần lượt 1/2, 3/10 và 1/5 số sản phẩm của một xưởng, với tỉ lệ phế phẩm lần lượt 1/50, 1/25 và 1/20. Lấy ngẫu nhiên một sản phẩm. Tính xác suất A: sản phẩm đó là phế phẩm. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi H_1, H_2, H_3: sản phẩm do máy 1, 2, 3 làm ra; đây là một hệ đầy đủ.
    2. P(H_1) = 1/2, P(H_2) = 3/10, P(H_3) = 1/5.
    3. P(A) bằng trung bình cộng của ba tỉ lệ phế phẩm: (1/50 + 1/25 + 1/20)/3 = 11/300.   **<- bước sai đầu tiên**
    4. Vậy P(A) = 11/300.
  - **Đáp án:** Bước 3: P(A) bằng trung bình cộng của ba tỉ lệ phế phẩm: (1/50 + 1/25 + 1/20)/3 = 11/300.
  - **Vì sao sai, và bước đúng:**
    1. Ba máy làm số sản phẩm khác nhau, nên mỗi tỉ lệ phế phẩm phải được nhân với P(H_i) của máy đó, không chia đều cho 3.
    2. P(A) = 1/2 . 1/50 + 3/10 . 1/25 + 1/5 . 1/20 = 1/100 + 3/250 + 1/100 = 4/125.
- `xs_g4_day_du` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 7/10 số sản phẩm, với tỉ lệ phế phẩm 1/50; phân xưởng II làm 3/10 số sản phẩm, với tỉ lệ phế phẩm 3/100. Lấy ngẫu nhiên một sản phẩm của nhà máy. Tính xác suất sản phẩm đó là phế phẩm.
  - **Đáp án:** 23/1000
    1. Hệ đầy đủ: H_i là sản phẩm do phân xưởng thứ i làm ra; A là sản phẩm là phế phẩm.
    2. Công thức xác suất đầy đủ: P(A) = tổng của P(H_i) P(A|H_i).
    3. P(A) = (7/10) . (1/50) + (3/10) . (3/100) = 7/500 + 9/1000 = 23/1000.
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 1/2 số sản phẩm, với tỉ lệ phế phẩm 1/50; phân xưởng II làm 1/2 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm của nhà máy. Tính xác suất sản phẩm đó là phế phẩm.
  - **Đáp án:** 3/50
    1. Hệ đầy đủ: H_i là sản phẩm do phân xưởng thứ i làm ra; A là sản phẩm là phế phẩm.
    2. Công thức xác suất đầy đủ: P(A) = tổng của P(H_i) P(A|H_i).
    3. P(A) = (1/2) . (1/50) + (1/2) . (1/10) = 1/100 + 1/20 = 3/50.
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 7/10 số sản phẩm, với tỉ lệ phế phẩm 1/25; phân xưởng II làm 3/10 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm của nhà máy. Tính xác suất sản phẩm đó là phế phẩm.
  - **Đáp án:** 29/500
    1. Hệ đầy đủ: H_i là sản phẩm do phân xưởng thứ i làm ra; A là sản phẩm là phế phẩm.
    2. Công thức xác suất đầy đủ: P(A) = tổng của P(H_i) P(A|H_i).
    3. P(A) = (7/10) . (1/25) + (3/10) . (1/10) = 7/250 + 3/100 = 29/500.
- `xs_t4_dd_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong một kỳ thi, đề dễ chiếm 1/2, đề trung bình chiếm 1/3 và đề khó chiếm 1/6 tổng số đề. An làm được đề dễ với xác suất 9/10, đề trung bình với xác suất 3/5 và đề khó với xác suất 1/5. An bốc ngẫu nhiên một đề. Tính xác suất An làm được đề đó.
  - **Đáp án:** 41/60
    1. Hệ đầy đủ theo loại đề: dễ 1/2, trung bình 1/3, khó 1/6 (tổng bằng 1).
    2. P(làm được) = 1/2 . 9/10 + 1/3 . 3/5 + 1/6 . 1/5 = 9/20 + 1/5 + 1/30.
    3. Quy đồng mẫu 60: 27/60 + 12/60 + 2/60 = 41/60.
- `xs_t4_dd_06` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ba máy làm lần lượt 1/4, 1/4 và 1/2 số sản phẩm của một xưởng, với tỉ lệ phế phẩm lần lượt 1/20, 1/25 và 1/50. Sắp xếp các bước tính xác suất một sản phẩm lấy ngẫu nhiên là phế phẩm.
  - **Đáp án (thứ tự đúng):**
    1. Gọi A: sản phẩm là phế phẩm; H_1, H_2, H_3: sản phẩm do máy 1, 2, 3 làm ra.
    2. Mỗi sản phẩm do đúng một máy làm ra, nên H_1, H_2, H_3 là một hệ đầy đủ.
    3. Ghi P(H_i) và P(A|H_i): 1/4 và 1/20; 1/4 và 1/25; 1/2 và 1/50.
    4. Công thức đầy đủ: P(A) = 1/80 + 1/100 + 1/100 = 13/400.
  - **Lời giải:**
    1. Đặt tên sự kiện, kiểm tra hệ đầy đủ, ghi số liệu theo từng giả thuyết, rồi cộng các tích.
    2. 1/4 . 1/20 = 1/80, 1/4 . 1/25 = 1/100, 1/2 . 1/50 = 1/100.
    3. 5/400 + 4/400 + 4/400 = 13/400.
- `xs_t4_dd_07` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối; ra mặt k chấm thì tung một đồng xu cân đối đúng k lần. Xác suất không có lần tung nào ra mặt ngửa là 21/128.
  - **Đáp án:** Đúng
    1. Hệ đầy đủ theo mặt xúc xắc: H_k là ra mặt k, P(H_k) = 1/6 với k = 1, ..., 6.
    2. Biết ra mặt k, không lần nào ngửa có xác suất (1/2)^k.
    3. P = (1/6)(1/2 + 1/4 + 1/8 + 1/16 + 1/32 + 1/64) = (1/6)(63/64) = 63/384 = 21/128. Mệnh đề đúng.
- `xs_t4_dd_08` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai phân xưởng I và II làm lần lượt 2/3 và 1/3 số sản phẩm của một nhà máy. Tỉ lệ phế phẩm của phân xưởng I là 1/30, còn tỉ lệ phế phẩm chung của cả nhà máy là 1/20. Tìm tỉ lệ phế phẩm của phân xưởng II.
  - **Đáp án:** 1/12
    1. Gọi x là tỉ lệ phế phẩm của phân xưởng II. Công thức đầy đủ: 1/20 = 2/3 . 1/30 + 1/3 . x.
    2. 2/3 . 1/30 = 1/45, nên x/3 = 1/20 - 1/45 = 9/180 - 4/180 = 1/36.
    3. x = 3/36 = 1/12.
- `xs_g4_chuyen_bi` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 2 bi trắng và 5 bi đen; hộp II có 1 bi trắng và 3 bi đen. Lấy ngẫu nhiên 1 bi từ hộp I bỏ sang hộp II, rồi từ hộp II lấy ngẫu nhiên 1 bi. Tính xác suất bi lấy từ hộp II là bi trắng.
  - **Đáp án:** 9/35
    1. Hệ đầy đủ theo bi được chuyển: H_1 là bi trắng, P(H_1) = 2/7; H_2 là bi đen, P(H_2) = 5/7.
    2. Sau khi chuyển, hộp II có 5 bi: P(A|H_1) = 2/5, P(A|H_2) = 1/5.
    3. P(A) = (2/7) . (2/5) + (5/7) . (1/5) = 9/35.
  - **Câu hỏi:** Hộp I có 1 bi trắng và 1 bi đen; hộp II có 1 bi trắng và 3 bi đen. Lấy ngẫu nhiên 1 bi từ hộp I bỏ sang hộp II, rồi từ hộp II lấy ngẫu nhiên 1 bi. Tính xác suất bi lấy từ hộp II là bi trắng.
  - **Đáp án:** 3/10
    1. Hệ đầy đủ theo bi được chuyển: H_1 là bi trắng, P(H_1) = 1/2; H_2 là bi đen, P(H_2) = 1/2.
    2. Sau khi chuyển, hộp II có 5 bi: P(A|H_1) = 2/5, P(A|H_2) = 1/5.
    3. P(A) = (1/2) . (2/5) + (1/2) . (1/5) = 3/10.
  - **Câu hỏi:** Hộp I có 2 bi trắng và 5 bi đen; hộp II có 5 bi trắng và 2 bi đen. Lấy ngẫu nhiên 1 bi từ hộp I bỏ sang hộp II, rồi từ hộp II lấy ngẫu nhiên 1 bi. Tính xác suất bi lấy từ hộp II là bi trắng.
  - **Đáp án:** 37/56
    1. Hệ đầy đủ theo bi được chuyển: H_1 là bi trắng, P(H_1) = 2/7; H_2 là bi đen, P(H_2) = 5/7.
    2. Sau khi chuyển, hộp II có 8 bi: P(A|H_1) = 6/8, P(A|H_2) = 5/8.
    3. P(A) = (2/7) . (3/4) + (5/7) . (5/8) = 37/56.

### Công thức Bayes (`xs_t4_bayes`)

- `xs_t4_by_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một nhà máy có hai phân xưởng. Phân xưởng I làm 3/5 số sản phẩm, với tỉ lệ phế phẩm 1/20; phân xưởng II làm 2/5 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm và thấy nó là phế phẩm. Tính xác suất nó do phân xưởng II làm ra.
  - **Đáp án:** 4/7
    1. Công thức đầy đủ: P(A) = 3/5 . 1/20 + 2/5 . 1/10 = 3/100 + 4/100 = 7/100.
    2. Bayes: P(H_2|A) = P(H_2) P(A|H_2) / P(A) = (4/100)/(7/100) = 4/7.
    3. Phân xưởng II làm ít sản phẩm hơn nhưng chiếm hơn nửa số phế phẩm.
- `xs_t4_by_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 2 bi đỏ và 2 bi xanh; hộp II có 3 bi đỏ và 1 bi xanh. Chọn ngẫu nhiên một hộp (mỗi hộp xác suất 1/2), lấy ngẫu nhiên 1 bi từ hộp đó và được bi đỏ. Xác suất bi đó lấy từ hộp II là 3/5.
  - **Đáp án:** Đúng
    1. P(đỏ) = 1/2 . 2/4 + 1/2 . 3/4 = 5/8.
    2. Bayes: P(hộp II | đỏ) = (1/2 . 3/4)/(5/8) = (3/8)/(5/8) = 3/5. Mệnh đề đúng.
- `xs_t4_by_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** H_1, H_2 là một hệ đầy đủ và A là một sự kiện có P(A) > 0. Công thức nào cho P(H_1|A)?
    - **(đúng)** P(H_1) P(A|H_1) / (P(H_1) P(A|H_1) + P(H_2) P(A|H_2))
    - P(A|H_1)
    - P(A|H_1) / (P(A|H_1) + P(A|H_2))
    - P(H_1) P(A|H_1)
  - **Đáp án:** P(H_1) P(A|H_1) / (P(H_1) P(A|H_1) + P(H_2) P(A|H_2))
    1. P(H_1|A) = P(H_1 A)/P(A), với P(H_1 A) = P(H_1) P(A|H_1) (công thức nhân).
    2. P(A) ở mẫu số tính bằng công thức đầy đủ trên hệ H_1, H_2.
    3. Bỏ P(H_i) đi (đáp án thứ ba) là bỏ qua xác suất ban đầu của các giả thuyết; P(A|H_1) là xác suất theo chiều ngược lại.
- `xs_t4_by_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Phân xưởng I làm 3/4 số sản phẩm với tỉ lệ phế phẩm 1/25; phân xưởng II làm 1/4 số sản phẩm với tỉ lệ phế phẩm 2/25. Lấy ngẫu nhiên một sản phẩm thì thấy là phế phẩm. Tính xác suất nó do phân xưởng II làm ra. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi H_1, H_2: sản phẩm do phân xưởng I, II làm ra; A: sản phẩm là phế phẩm.
    2. Theo đề, P(H_1) = 3/4, P(H_2) = 1/4, P(A|H_1) = 1/25, P(A|H_2) = 2/25.
    3. Cần tìm xác suất sản phẩm do phân xưởng II làm ra khi đã biết nó là phế phẩm, tức là P(A|H_2).   **<- bước sai đầu tiên**
    4. Vậy xác suất đó là 2/25.
  - **Đáp án:** Bước 3: Cần tìm xác suất sản phẩm do phân xưởng II làm ra khi đã biết nó là phế phẩm, tức là P(A|H_2).
  - **Vì sao sai, và bước đúng:**
    1. Điều đã biết là A (phế phẩm), nên cần P(H_2|A), không phải P(A|H_2) là tỉ lệ phế phẩm của phân xưởng II.
    2. P(A) = 3/4 . 1/25 + 1/4 . 2/25 = 3/100 + 2/100 = 1/20.
    3. P(H_2|A) = (2/100)/(5/100) = 2/5.
- `xs_t4_by_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ba máy làm lần lượt 1/2, 3/10 và 1/5 số sản phẩm của một xưởng, với tỉ lệ phế phẩm lần lượt 1/50, 1/25 và 1/20. Lấy ngẫu nhiên một sản phẩm và thấy nó là phế phẩm. Tính xác suất nó do máy thứ ba làm ra.
  - **Đáp án:** 5/16
    1. Công thức đầy đủ: P(A) = 1/2 . 1/50 + 3/10 . 1/25 + 1/5 . 1/20 = 1/100 + 3/250 + 1/100 = 4/125.
    2. Bayes: P(H_3|A) = (1/5 . 1/20)/(4/125) = (1/100)/(4/125).
    3. = 125/400 = 5/16.
- `xs_t4_by_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp loại I có 1 bi đỏ và 9 bi xanh; hộp loại II có 9 bi đỏ và 1 bi xanh. Có 9 hộp loại I và 1 hộp loại II. Chọn ngẫu nhiên một trong 10 hộp, lấy ngẫu nhiên 1 bi và được bi đỏ. Xác suất hộp đã chọn là hộp loại II lớn hơn 1/2.
  - **Đáp án:** Sai
    1. Xác suất ban đầu: loại I là 9/10, loại II là 1/10.
    2. P(đỏ) = 9/10 . 1/10 + 1/10 . 9/10 = 18/100.
    3. P(loại II | đỏ) = (9/100)/(18/100) = 1/2, đúng bằng 1/2 chứ không lớn hơn. Bi đỏ rất hay gặp ở hộp loại II, nhưng hộp loại II lại hiếm: hai điều cân nhau. Mệnh đề sai.
- `xs_t4_by_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hộp I có 4 bi trắng và 1 bi đen; hộp II có 3 bi trắng và 3 bi đen. Lấy ngẫu nhiên 1 bi từ hộp I bỏ sang hộp II, rồi lấy ngẫu nhiên 1 bi từ hộp II thì được bi trắng (sự kiện A). Sắp xếp các bước tính xác suất bi đã chuyển sang là bi trắng.
  - **Đáp án (thứ tự đúng):**
    1. Hệ đầy đủ: H_1 bi chuyển sang là trắng, H_2 bi chuyển sang là đen; P(H_1) = 4/5, P(H_2) = 1/5.
    2. Sau khi chuyển, hộp II có 7 bi: P(A|H_1) = 4/7, P(A|H_2) = 3/7.
    3. Công thức đầy đủ: P(A) = 4/5 . 4/7 + 1/5 . 3/7 = 19/35.
    4. Công thức Bayes: P(H_1|A) = (16/35)/(19/35) = 16/19.
  - **Lời giải:**
    1. Giả thuyết là màu bi được chuyển, vì nó quyết định hộp II trông thế nào.
    2. P(A) cần trước, vì nó là mẫu số của công thức Bayes.
    3. P(H_1|A) = 16/19.
- `xs_t4_by_08` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phân xưởng I làm 2/3 số sản phẩm với tỉ lệ phế phẩm 1/10; phân xưởng II làm 1/3 số sản phẩm với tỉ lệ phế phẩm 3/10. Lấy ngẫu nhiên một sản phẩm. Ghép mỗi xác suất với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - P(phế phẩm) — 1/6
    - P(phân xưởng I | phế phẩm) — 2/5
    - P(phân xưởng II | phế phẩm) — 3/5
    - P(phân xưởng I | chính phẩm) — 18/25
  - **Lời giải:**
    1. P(phế phẩm) = 2/3 . 1/10 + 1/3 . 3/10 = 1/15 + 1/10 = 1/6.
    2. P(I | phế) = (1/15)/(1/6) = 2/5 và P(II | phế) = (1/10)/(1/6) = 3/5; hai số cộng lại bằng 1.
    3. P(chính phẩm) = 5/6 và P(I và chính phẩm) = 2/3 . 9/10 = 3/5, nên P(I | chính phẩm) = (3/5)/(5/6) = 18/25.
- `xs_g4_bayes` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 7/10 số sản phẩm, với tỉ lệ phế phẩm 1/50; phân xưởng II làm 3/10 số sản phẩm, với tỉ lệ phế phẩm 3/100. Lấy ngẫu nhiên một sản phẩm của nhà máy và thấy nó là phế phẩm. Tính xác suất sản phẩm đó do phân xưởng I làm ra.
  - **Đáp án:** 14/23
    1. H_i: sản phẩm do phân xưởng thứ i làm ra; A: sản phẩm là phế phẩm.
    2. Công thức đầy đủ: P(A) = 7/500 + 9/1000 = 23/1000.
    3. Công thức Bayes: P(H_1|A) = P(H_1) P(A|H_1) / P(A) = (7/500)/(23/1000) = 14/23.
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 1/2 số sản phẩm, với tỉ lệ phế phẩm 1/50; phân xưởng II làm 1/2 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm của nhà máy và thấy nó là phế phẩm. Tính xác suất sản phẩm đó do phân xưởng I làm ra.
  - **Đáp án:** 1/6
    1. H_i: sản phẩm do phân xưởng thứ i làm ra; A: sản phẩm là phế phẩm.
    2. Công thức đầy đủ: P(A) = 1/100 + 1/20 = 3/50.
    3. Công thức Bayes: P(H_1|A) = P(H_1) P(A|H_1) / P(A) = (1/100)/(3/50) = 1/6.
  - **Câu hỏi:** Một nhà máy có 2 phân xưởng: phân xưởng I làm 7/10 số sản phẩm, với tỉ lệ phế phẩm 1/25; phân xưởng II làm 3/10 số sản phẩm, với tỉ lệ phế phẩm 1/10. Lấy ngẫu nhiên một sản phẩm của nhà máy và thấy nó là phế phẩm. Tính xác suất sản phẩm đó do phân xưởng II làm ra.
  - **Đáp án:** 15/29
    1. H_i: sản phẩm do phân xưởng thứ i làm ra; A: sản phẩm là phế phẩm.
    2. Công thức đầy đủ: P(A) = 7/250 + 3/100 = 29/500.
    3. Công thức Bayes: P(H_2|A) = P(H_2) P(A|H_2) / P(A) = (3/100)/(29/500) = 15/29.

### Bayes trong xét nghiệm và phân loại (`xs_t4_bayes_ung_dung`)

- `xs_t4_bu_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bệnh có tỉ lệ mắc là 1/100. Xét nghiệm cho kết quả dương tính với xác suất 9/10 nếu người đó mắc bệnh và với xác suất 1/10 nếu người đó không mắc bệnh. Một người chọn ngẫu nhiên có kết quả dương tính. Tính xác suất người đó mắc bệnh.
  - **Đáp án:** 1/12
    1. P(dương tính) = 1/100 . 9/10 + 99/100 . 1/10 = 9/1000 + 99/1000 = 108/1000.
    2. Bayes: P(bệnh | dương tính) = (9/1000)/(108/1000) = 9/108 = 1/12.
    3. Trong 1000 người, chỉ 9 người bệnh có dương tính, còn 99 người khỏe bị dương tính nhầm.
- `xs_t4_bu_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xét nghiệm có P(dương tính | mắc bệnh) = 99/100. Chỉ từ thông tin này đã suy ra được: người có kết quả dương tính mắc bệnh với xác suất 99/100.
  - **Đáp án:** Sai
    1. 99/100 là P(dương tính | bệnh); câu hỏi là P(bệnh | dương tính), chiều ngược lại.
    2. Muốn tính chiều ngược lại cần thêm tỉ lệ mắc bệnh và tỉ lệ dương tính nhầm ở người khỏe (công thức Bayes).
    3. Với bệnh hiếm, P(bệnh | dương tính) có thể rất nhỏ. Mệnh đề sai.
- `xs_t4_bu_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thư rác chiếm 1/5 số thư gửi đến một hòm thư. Từ 'khuyến mãi' có trong 1/2 số thư rác và trong 1/20 số thư thường. Một thư có từ 'khuyến mãi'. Xác suất thư đó là thư rác là bao nhiêu?
    - **(đúng)** 5/7
    - 1/2
    - 1/10
    - 7/50
  - **Đáp án:** 5/7
    1. P(có từ) = 1/5 . 1/2 + 4/5 . 1/20 = 1/10 + 1/25 = 7/50.
    2. Bayes: P(rác | có từ) = (1/10)/(7/50) = 5/7.
    3. 1/2 là P(có từ | rác), 7/50 là P(có từ): đều không phải điều được hỏi.
- `xs_t4_bu_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một bệnh có tỉ lệ mắc 1/1000. Xét nghiệm luôn dương tính với người mắc bệnh, và dương tính nhầm với xác suất 1/50 ở người không mắc bệnh. Một người chọn ngẫu nhiên có kết quả dương tính. Tính xác suất người đó mắc bệnh. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi B: người đó mắc bệnh, D: kết quả dương tính.
    2. Theo đề, P(B) = 1/1000, P(D|B) = 1, và P(D | không mắc bệnh) = 1/50.
    3. Xét nghiệm chỉ sai với 1/50 số người khỏe, nên người có kết quả dương tính mắc bệnh với xác suất 1 - 1/50 = 49/50.   **<- bước sai đầu tiên**
    4. Vậy P(B|D) = 49/50.
  - **Đáp án:** Bước 3: Xét nghiệm chỉ sai với 1/50 số người khỏe, nên người có kết quả dương tính mắc bệnh với xác suất 1 - 1/50 = 49/50.
  - **Vì sao sai, và bước đúng:**
    1. Bước này bỏ qua tỉ lệ nền: bệnh rất hiếm nên số người khỏe dương tính nhầm lấn át số người bệnh.
    2. P(D) = 1/1000 . 1 + 999/1000 . 1/50 = 50/50000 + 999/50000 = 1049/50000.
    3. P(B|D) = (50/50000)/(1049/50000) = 50/1049, chưa đến 1/20.
- `xs_t4_bu_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bệnh có tỉ lệ mắc 1/100. Mỗi lần xét nghiệm dương tính với xác suất 9/10 nếu người đó mắc bệnh và 1/10 nếu không mắc bệnh; khi đã biết người đó mắc bệnh hay không, kết quả hai lần xét nghiệm độc lập với nhau. Một người chọn ngẫu nhiên được xét nghiệm hai lần và cả hai lần đều dương tính. Tính xác suất người đó mắc bệnh.
  - **Đáp án:** 9/20
    1. Biết mắc bệnh: hai lần dương tính có xác suất (9/10)^2 = 81/100; biết không mắc: (1/10)^2 = 1/100.
    2. P(hai lần dương tính) = 1/100 . 81/100 + 99/100 . 1/100 = 81/10000 + 99/10000 = 180/10000.
    3. Bayes: P(bệnh | hai lần dương tính) = 81/180 = 9/20, lớn hơn nhiều so với 1/12 sau một lần.
- `xs_t4_bu_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng cùng một xét nghiệm (P(dương tính | bệnh) và P(dương tính | khỏe) là hai số dương cố định) ở hai nhóm người có tỉ lệ mắc bệnh khác nhau, cả hai tỉ lệ đều trong khoảng (0, 1). Ở nhóm có tỉ lệ mắc bệnh cao hơn, P(mắc bệnh | dương tính) lớn hơn.
  - **Đáp án:** Đúng
    1. Gọi p là tỉ lệ mắc, s = P(dương | bệnh), f = P(dương | khỏe). Bayes: P(bệnh | dương) = ps / (ps + (1 - p) f) = 1 / (1 + (1 - p) f / (p s)).
    2. Khi p tăng, (1 - p)/p giảm, nên mẫu số giảm và P(bệnh | dương) tăng.
    3. Mệnh đề đúng: cùng một kết quả dương tính có ý nghĩa khác nhau tùy tỉ lệ nền.
- `xs_t4_bu_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thư rác chiếm 1/4 số thư. Từ 'trúng thưởng' có trong 2/5 số thư rác và trong 1/30 số thư thường. Một thư có từ 'trúng thưởng'. Sắp xếp các bước tính xác suất thư đó là thư rác.
  - **Đáp án (thứ tự đúng):**
    1. Hệ đầy đủ: H_1 là thư rác, H_2 là thư thường; P(H_1) = 1/4, P(H_2) = 3/4.
    2. Gọi A: thư có từ 'trúng thưởng'; P(A|H_1) = 2/5, P(A|H_2) = 1/30.
    3. Công thức đầy đủ: P(A) = 1/4 . 2/5 + 3/4 . 1/30 = 1/10 + 1/40 = 1/8.
    4. Bayes: P(H_1|A) = (1/10)/(1/8) = 4/5.
  - **Lời giải:**
    1. Chọn giả thuyết (rác hay thường), ghi số liệu theo từng giả thuyết.
    2. Tính P(A) bằng công thức đầy đủ trước, vì nó là mẫu số.
    3. P(thư rác | có từ) = 4/5.
- `xs_t4_bu_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xét nghiệm có P(dương tính | bệnh) = 19/20 và P(dương tính | khỏe) = 1/20. Ở vùng A tỉ lệ mắc bệnh là 1/2, ở vùng B là 1/20. Với một người dương tính, xác suất người đó mắc bệnh ở mỗi vùng là bao nhiêu?
    - **(đúng)** Vùng A: 19/20, vùng B: 1/2
    - Cả hai vùng: 19/20
    - Vùng A: 1/2, vùng B: 19/20
    - Cả hai vùng: 1/2
  - **Đáp án:** Vùng A: 19/20, vùng B: 1/2
    1. Vùng A: (1/2 . 19/20)/(1/2 . 19/20 + 1/2 . 1/20) = 19/20.
    2. Vùng B: (1/20 . 19/20)/(1/20 . 19/20 + 19/20 . 1/20) = 1/2.
    3. Cùng xét nghiệm, cùng kết quả, nhưng tỉ lệ nền khác nhau cho kết luận khác nhau.
- `xs_g4_xet_nghiem` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một bệnh có tỉ lệ mắc trong cộng đồng là 1/50. Một xét nghiệm cho kết quả dương tính với xác suất 1 nếu người được xét nghiệm mắc bệnh, và với xác suất 1/10 nếu người đó không mắc bệnh. Chọn ngẫu nhiên một người trong cộng đồng, xét nghiệm và được kết quả dương tính. Tính xác suất người đó mắc bệnh.
  - **Đáp án:** 10/59
    1. Hệ đầy đủ: B là mắc bệnh, P(B) = 1/50; không mắc bệnh có xác suất 49/50.
    2. P(dương tính) = (1/50) . 1 + (49/50) . (1/10) = 1/50 + 49/500 = 59/500.
    3. Bayes: P(B | dương tính) = (1/50)/(59/500) = 10/59.
    4. Tỉ lệ mắc bệnh (tỉ lệ nền) càng nhỏ thì số người khỏe bị dương tính nhầm càng lấn át.
  - **Câu hỏi:** Một bệnh có tỉ lệ mắc trong cộng đồng là 1/100. Một xét nghiệm cho kết quả dương tính với xác suất 9/10 nếu người được xét nghiệm mắc bệnh, và với xác suất 1/10 nếu người đó không mắc bệnh. Chọn ngẫu nhiên một người trong cộng đồng, xét nghiệm và được kết quả dương tính. Tính xác suất người đó mắc bệnh.
  - **Đáp án:** 1/12
    1. Hệ đầy đủ: B là mắc bệnh, P(B) = 1/100; không mắc bệnh có xác suất 99/100.
    2. P(dương tính) = (1/100) . (9/10) + (99/100) . (1/10) = 9/1000 + 99/1000 = 27/250.
    3. Bayes: P(B | dương tính) = (9/1000)/(27/250) = 1/12.
    4. Tỉ lệ mắc bệnh (tỉ lệ nền) càng nhỏ thì số người khỏe bị dương tính nhầm càng lấn át.
  - **Câu hỏi:** Một bệnh có tỉ lệ mắc trong cộng đồng là 1/50. Một xét nghiệm cho kết quả dương tính với xác suất 1 nếu người được xét nghiệm mắc bệnh, và với xác suất 3/100 nếu người đó không mắc bệnh. Chọn ngẫu nhiên một người trong cộng đồng, xét nghiệm và được kết quả dương tính. Tính xác suất người đó mắc bệnh.
  - **Đáp án:** 100/247
    1. Hệ đầy đủ: B là mắc bệnh, P(B) = 1/50; không mắc bệnh có xác suất 49/50.
    2. P(dương tính) = (1/50) . 1 + (49/50) . (3/100) = 1/50 + 147/5000 = 247/5000.
    3. Bayes: P(B | dương tính) = (1/50)/(247/5000) = 100/247.
    4. Tỉ lệ mắc bệnh (tỉ lệ nền) càng nhỏ thì số người khỏe bị dương tính nhầm càng lấn át.

## Tầng 5: Biến ngẫu nhiên, bảng phân phối và hàm phân phối

44 dạng câu (38 câu viết tay, 6 bộ sinh câu); 44 chưa duyệt.

### Biến ngẫu nhiên rời rạc và liên tục (`xs_t5_bien_ngau_nhien`)

- `xs_t5_bn_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đại lượng nào dưới đây là một biến ngẫu nhiên liên tục?
    - **(đúng)** Thời gian chờ xe buýt tại một bến, tính bằng phút
    - Số chấm khi gieo một con xúc xắc
    - Số sản phẩm hỏng trong một lô 10 sản phẩm
    - Số cuộc gọi đến một tổng đài trong một giờ
  - **Đáp án:** Thời gian chờ xe buýt tại một bến, tính bằng phút
    1. Biến rời rạc nhận các giá trị đếm được, tách rời nhau (0, 1, 2, ...); biến liên tục nhận mọi giá trị trong một khoảng.
    2. Thời gian chờ có thể là bất kỳ số nào trong một khoảng, như 2.5 hay 3.14 phút: liên tục.
    3. Ba đại lượng còn lại là kết quả của việc đếm: rời rạc, kể cả số cuộc gọi không bị chặn trên.
- `xs_t5_bn_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu X là một biến ngẫu nhiên liên tục (có hàm mật độ) thì P(X = 2) = 0.
  - **Đáp án:** Đúng
    1. Với biến liên tục, xác suất rơi vào [a, b] là tích phân của hàm mật độ trên [a, b].
    2. Khi a = b = 2, tích phân trên một điểm bằng 0.
    3. Mệnh đề đúng; vì vậy với biến liên tục, viết < hay <= ở hai đầu khoảng không làm đổi xác suất.
- `xs_t5_bn_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu 3 lần. Gọi X là số lần ra mặt ngửa trừ đi số lần ra mặt sấp. X nhận bao nhiêu giá trị khác nhau?
  - **Đáp án:** 4
    1. Nếu có k lần ngửa thì có 3 - k lần sấp, nên X = k - (3 - k) = 2k - 3.
    2. k nhận 0, 1, 2, 3, nên X nhận -3, -1, 1, 3.
    3. Có 4 giá trị khác nhau.
- `xs_t5_bn_04` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi biến ngẫu nhiên với tập các giá trị nó có thể nhận.
  - **Đáp án (ghép đúng):**
    - Số lần ngửa khi tung 2 đồng xu — {0, 1, 2}
    - Tổng số chấm khi gieo 2 xúc xắc — {2, 3, ..., 12}
    - Số lần gieo một xúc xắc cho đến khi ra mặt 6 lần đầu tiên — {1, 2, 3, ...}, vô hạn đếm được
    - Chiều cao (cm) của một người chọn ngẫu nhiên — Mọi số trong một khoảng
  - **Lời giải:**
    1. Hai đồng xu: 0, 1 hoặc 2 lần ngửa. Hai xúc xắc: tổng nhỏ nhất 2, lớn nhất 12.
    2. Số lần gieo đến khi ra mặt 6 có thể là 1, 2, 3, ... không có giới hạn trên: rời rạc nhưng vô hạn.
    3. Chiều cao đo trên một thang liên tục: biến liên tục.
- `xs_t5_bn_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 2 bi đỏ và 3 bi xanh. Lấy ngẫu nhiên cùng lúc 2 bi. Gọi X là số bi đỏ lấy được. Tính P(X = 2). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. X là số bi đỏ trong 2 bi lấy ra, nên X nhận các giá trị 0, 1, 2.
    2. X có 3 giá trị, nên mỗi giá trị có xác suất 1/3.   **<- bước sai đầu tiên**
    3. Vậy P(X = 2) = 1/3.
  - **Đáp án:** Bước 2: X có 3 giá trị, nên mỗi giá trị có xác suất 1/3.
  - **Vì sao sai, và bước đúng:**
    1. Các giá trị của một biến ngẫu nhiên không nhất thiết đồng khả năng; phải tính từ không gian mẫu.
    2. Có C(5, 2) = 10 cách lấy đồng khả năng: X = 0 có C(3, 2) = 3 cách, X = 1 có 2 . 3 = 6 cách, X = 2 có 1 cách.
    3. P(X = 2) = 1/10.
- `xs_t5_bn_06` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Gọi X là giá trị tuyệt đối của hiệu hai số chấm. P(X = 0) lớn hơn P(X = 1).
  - **Đáp án:** Sai
    1. X = 0 khi hai số chấm bằng nhau: 6 cặp, P(X = 0) = 6/36.
    2. X = 1 khi hai số chấm hơn kém 1: (1, 2), (2, 3), (3, 4), (4, 5), (5, 6) và năm cặp đảo lại, 10 cặp, P(X = 1) = 10/36.
    3. 6/36 < 10/36. Mệnh đề sai.
- `xs_t5_bn_07` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Gọi X là số chấm lớn hơn trong hai số chấm (bằng nhau thì lấy số đó). Tính P(X = 4).
  - **Đáp án:** 7/36
    1. X <= 4 khi cả hai số chấm <= 4: 4 . 4 = 16 cặp. X <= 3 khi cả hai <= 3: 9 cặp.
    2. X = 4 là X <= 4 trừ đi X <= 3: 16 - 9 = 7 cặp.
    3. P(X = 4) = 7/36.

### Bảng phân phối xác suất (`xs_t5_bang_phan_phoi`)

- `xs_t5_bp_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2, 3 với xác suất lần lượt 1/10, 3/10, 2/5, a. Tìm a.
  - **Đáp án:** 1/5
    1. Tổng các xác suất trong bảng phân phối bằng 1.
    2. a = 1 - 1/10 - 3/10 - 2/5 = 1 - 8/10 = 1/5.
- `xs_t5_bp_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng: X nhận các giá trị -1, 0, 1 với xác suất lần lượt 1/3, 1/2, 1/4. Đây là bảng phân phối xác suất của một biến ngẫu nhiên.
  - **Đáp án:** Sai
    1. Một bảng phân phối cần các xác suất không âm và có tổng bằng 1.
    2. 1/3 + 1/2 + 1/4 = 4/12 + 6/12 + 3/12 = 13/12 > 1.
    3. Mệnh đề sai.
- `xs_t5_bp_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 2 bi xanh. Lấy ngẫu nhiên cùng lúc 2 bi. Gọi X là số bi đỏ lấy được. Bảng phân phối của X là bảng nào?
    - **(đúng)** P(X = 0) = 1/10, P(X = 1) = 3/5, P(X = 2) = 3/10
    - P(X = 0) = 1/3, P(X = 1) = 1/3, P(X = 2) = 1/3
    - P(X = 0) = 4/25, P(X = 1) = 12/25, P(X = 2) = 9/25
    - P(X = 0) = 1/10, P(X = 1) = 3/10, P(X = 2) = 3/5
  - **Đáp án:** P(X = 0) = 1/10, P(X = 1) = 3/5, P(X = 2) = 3/10
    1. Có C(5, 2) = 10 cách lấy đồng khả năng.
    2. X = 0: C(2, 2) = 1 cách; X = 1: 3 . 2 = 6 cách; X = 2: C(3, 2) = 3 cách. Bảng: 1/10, 6/10 = 3/5, 3/10.
    3. 4/25, 12/25, 9/25 là bảng của lấy có hoàn lại, không phải lấy cùng lúc.
- `xs_t5_bp_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xạ thủ có 3 viên đạn, bắn lần lượt cho đến khi trúng thì dừng hoặc hết đạn; mỗi phát trúng với xác suất 2/3, các phát độc lập. Gọi X là số viên đạn đã dùng. Sắp xếp các bước lập bảng phân phối của X.
  - **Đáp án (thứ tự đúng):**
    1. X nhận các giá trị 1, 2, 3.
    2. X = 1 khi phát đầu trúng: P(X = 1) = 2/3.
    3. Nếu phát đầu trượt (xác suất 1/3) thì bắn tiếp, nên P(X = 2) = 1/3 . 2/3 = 2/9.
    4. Còn lại X = 3, dù phát thứ ba trúng hay trượt: P(X = 3) = 1 - 2/3 - 2/9 = 1/9.
    5. Bảng phân phối: X = 1, 2, 3 với xác suất 2/3, 2/9, 1/9.
  - **Lời giải:**
    1. Xác định các giá trị trước, rồi tính lần lượt từng xác suất.
    2. X = 3 chỉ cần hai phát đầu trượt: 1/3 . 1/3 = 1/9, khớp với cách lấy phần còn lại.
    3. Tổng 6/9 + 2/9 + 1/9 = 1.
- `xs_g5_bang_thieu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 2, 3 với xác suất lần lượt 1/8, p, 5/8. Tìm p.
  - **Đáp án:** 1/4
    1. Trong một bảng phân phối, các xác suất cộng lại bằng 1.
    2. p = 1 - (1/8 + 5/8) = 1 - 3/4 = 1/4.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị -1, 0, 1 với xác suất lần lượt 1/8, 1/4, p. Tìm p.
  - **Đáp án:** 5/8
    1. Trong một bảng phân phối, các xác suất cộng lại bằng 1.
    2. p = 1 - (1/8 + 1/4) = 1 - 3/8 = 5/8.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 2, 3, 4 với xác suất lần lượt p, 1/5, 1/5. Tìm p.
  - **Đáp án:** 3/5
    1. Trong một bảng phân phối, các xác suất cộng lại bằng 1.
    2. p = 1 - (1/5 + 1/5) = 1 - 2/5 = 3/5.
- `xs_g5_rut_bi_bang` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 2 bi xanh. Lấy ngẫu nhiên cùng lúc 3 bi. Gọi X là số bi đỏ lấy được. Tính P(X = 1) trong bảng phân phối của X.
  - **Đáp án:** 3/10
    1. Không gian mẫu: C(5, 3) = 10 cách lấy đồng khả năng.
    2. X = 1: chọn 1 bi đỏ trong 3 và 2 bi xanh trong 2: C(3, 1) . C(2, 2) = 3 cách.
    3. P(X = 1) = 3/10 = 3/10.
  - **Câu hỏi:** Một hộp có 2 bi đỏ và 2 bi xanh. Lấy ngẫu nhiên cùng lúc 2 bi. Gọi X là số bi đỏ lấy được. Tính P(X = 1) trong bảng phân phối của X.
  - **Đáp án:** 2/3
    1. Không gian mẫu: C(4, 2) = 6 cách lấy đồng khả năng.
    2. X = 1: chọn 1 bi đỏ trong 2 và 1 bi xanh trong 2: C(2, 1) . C(2, 1) = 4 cách.
    3. P(X = 1) = 4/6 = 2/3.
  - **Câu hỏi:** Một hộp có 3 bi đỏ và 3 bi xanh. Lấy ngẫu nhiên cùng lúc 3 bi. Gọi X là số bi đỏ lấy được. Tính P(X = 3) trong bảng phân phối của X.
  - **Đáp án:** 1/20
    1. Không gian mẫu: C(6, 3) = 20 cách lấy đồng khả năng.
    2. X = 3: chọn 3 bi đỏ trong 3 và 0 bi xanh trong 3: C(3, 3) . C(3, 0) = 1 cách.
    3. P(X = 3) = 1/20 = 1/20.
- `xs_t5_bp_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung một đồng xu cân đối 3 lần. Gọi X là số lần ra mặt ngửa. Lập bảng phân phối của X. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. X nhận các giá trị 0, 1, 2, 3.
    2. P(X = 0) = P(X = 3) = 1/8, vì chỉ có một dãy SSS và một dãy NNN.
    3. P(X = 1) = P(X = 2) = 1/8, vì mỗi giá trị ứng với một dãy kết quả.   **<- bước sai đầu tiên**
    4. Bảng phân phối: X = 0, 1, 2, 3 với xác suất 1/8, 1/8, 1/8, 1/8.
  - **Đáp án:** Bước 3: P(X = 1) = P(X = 2) = 1/8, vì mỗi giá trị ứng với một dãy kết quả.
  - **Vì sao sai, và bước đúng:**
    1. X = 1 ứng với ba dãy NSS, SNS, SSN, không phải một dãy; tương tự X = 2 có ba dãy.
    2. P(X = 1) = P(X = 2) = 3/8.
    3. Dấu hiệu nhận ra sai: bảng 1/8 x 4 có tổng 1/2, khác 1.
- `xs_t5_bp_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 2, 3, 4 với P(X = k) = ck, trong đó c là một hằng số. Tính P(X >= 3).
  - **Đáp án:** 7/10
    1. Tổng các xác suất bằng 1: c(1 + 2 + 3 + 4) = 10c = 1, nên c = 1/10.
    2. P(X >= 3) = P(X = 3) + P(X = 4) = 3/10 + 4/10 = 7/10.
- `xs_t5_bp_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai xạ thủ bắn độc lập, mỗi người một phát, trúng với xác suất lần lượt 1/2 và 2/3. Gọi X là số phát trúng. Trong bảng phân phối của X, P(X = 1) = 1/2.
  - **Đáp án:** Đúng
    1. X = 1 gồm hai trường hợp xung khắc: người 1 trúng, người 2 trượt; hoặc người 1 trượt, người 2 trúng.
    2. P(X = 1) = 1/2 . 1/3 + 1/2 . 2/3 = 1/6 + 1/3 = 1/2.
    3. Cả bảng: P(X = 0) = 1/6, P(X = 1) = 1/2, P(X = 2) = 1/3, tổng bằng 1. Mệnh đề đúng.
- `xs_t5_bp_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2, 3 với xác suất lần lượt 1/8, a, 3/8, b. Biết P(X >= 2) = 1/2. Hàm phân phối F(x) = P(X < x).
  - **Phần a** (Điền số): a) Tìm b.
    - **Đáp án a:** 1/8
  - **Phần b** (Điền số): b) Tìm a.
    - **Đáp án b:** 3/8
  - **Phần c** (Đúng/Sai): c) F(2) = 1/2.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) P(X >= 2) = P(X = 2) + P(X = 3) = 3/8 + b = 1/2, nên b = 1/8.
    2. b) Tổng các xác suất bằng 1: 1/8 + a + 3/8 + 1/8 = 1, nên a = 3/8.
    3. c) F(2) = P(X < 2) = P(X = 0) + P(X = 1) = 1/8 + 3/8 = 1/2, không tính P(X = 2). Mệnh đề đúng.

### Hàm phân phối F(x) (`xs_t5_ham_phan_phoi`)

- `xs_t5_hp_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 2, 3 với xác suất lần lượt 1/5, 1/2, 3/10. Với hàm phân phối F(x) = P(X < x), tính F(3).
  - **Đáp án:** 7/10
    1. F(3) = P(X < 3): chỉ cộng các giá trị nhỏ hơn hẳn 3.
    2. F(3) = P(X = 1) + P(X = 2) = 1/5 + 1/2 = 7/10.
- `xs_t5_hp_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đệ tử bốc thăm nhận 1, 2 hoặc 3 viên linh thạch, với xác suất lần lượt 1/4, 1/2, 1/4; X là số viên nhận được. Theo quy ước hàm phân phối F(x) = P(X < x), giá trị F(2) bằng 3/4.
  - **Đáp án:** Sai
    1. F(2) = P(X < 2): giá trị 2 không được tính.
    2. F(2) = P(X = 1) = 1/4.
    3. 3/4 là P(X <= 2), tức là F(x) với x hơi lớn hơn 2, chẳng hạn F(2.5). Mệnh đề sai.
- `xs_t5_hp_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X nhận giá trị 0 với xác suất 1/3 và giá trị 1 với xác suất 2/3. Với quy ước F(x) = P(X < x), hàm phân phối của X là hàm nào?
    - **(đúng)** F(x) = 0 khi x <= 0; F(x) = 1/3 khi 0 < x <= 1; F(x) = 1 khi x > 1
    - F(x) = 0 khi x < 0; F(x) = 1/3 khi 0 <= x < 1; F(x) = 1 khi x >= 1
    - F(x) = 0 khi x <= 0; F(x) = 2/3 khi 0 < x <= 1; F(x) = 1 khi x > 1
    - F(x) = 1/3 với mọi x
  - **Đáp án:** F(x) = 0 khi x <= 0; F(x) = 1/3 khi 0 < x <= 1; F(x) = 1 khi x > 1
    1. Với x <= 0, không có giá trị nào của X nhỏ hơn hẳn x: F(x) = 0. Riêng F(0) = P(X < 0) = 0.
    2. Với 0 < x <= 1, chỉ giá trị 0 nhỏ hơn x: F(x) = 1/3. Riêng F(1) = P(X < 1) = 1/3.
    3. Với x > 1 thì F(x) = 1. Đáp án thứ hai là hàm P(X <= x), theo quy ước khác.
- `xs_t5_hp_04` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X có hàm phân phối F(x) = P(X < x) như sau: F(x) = 0 khi x <= 1; F(x) = 1/5 khi 1 < x <= 2; F(x) = 7/10 khi 2 < x <= 4; F(x) = 1 khi x > 4. Ghép mỗi xác suất với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - P(X = 1) — 1/5
    - P(X = 2) — 1/2
    - P(X = 4) — 3/10
    - P(X = 3) — 0
  - **Lời giải:**
    1. Mỗi bước nhảy của F nằm ở một giá trị của X, và độ cao bước nhảy là xác suất của giá trị đó.
    2. Tại 1: nhảy từ 0 lên 1/5. Tại 2: từ 1/5 lên 7/10, cao 1/2. Tại 4: từ 7/10 lên 1, cao 3/10.
    3. F không nhảy tại 3, nên P(X = 3) = 0.
- `xs_g5_ham_phan_phoi` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 2, 3 với xác suất lần lượt 1/8, 1/4, 5/8. Với hàm phân phối F(x) = P(X < x), tính F(4).
  - **Đáp án:** 1
    1. F(4) = P(X < 4): cộng xác suất của các giá trị nhỏ hơn hẳn 4, không tính giá trị bằng 4.
    2. Các giá trị nhỏ hơn hẳn 4 là 1, 2, 3, nên F(4) = 1/8 + 1/4 + 5/8 = 1.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị -1, 0, 1 với xác suất lần lượt 1/8, 1/4, 5/8. Với hàm phân phối F(x) = P(X < x), tính F(1).
  - **Đáp án:** 3/8
    1. F(1) = P(X < 1): cộng xác suất của các giá trị nhỏ hơn hẳn 1, không tính giá trị bằng 1.
    2. Các giá trị nhỏ hơn hẳn 1 là -1, 0, nên F(1) = 1/8 + 1/4 = 3/8.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 2, 3, 4 với xác suất lần lượt 3/5, 1/5, 1/5. Với hàm phân phối F(x) = P(X < x), tính F(2).
  - **Đáp án:** 0
    1. F(2) = P(X < 2): cộng xác suất của các giá trị nhỏ hơn hẳn 2, không tính giá trị bằng 2.
    2. Không có giá trị nào của X nhỏ hơn 2, nên F(2) = 0.
- `xs_t5_hp_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm F(x) = 0 khi x <= 0, F(x) = kx^3 khi 0 < x <= 2, F(x) = 1 khi x > 2 là hàm phân phối của một biến ngẫu nhiên liên tục X. Tìm k.
  - **Đáp án:** 1/8
    1. Hàm phân phối của biến liên tục là hàm liên tục, nên tại x = 2 hai mảnh phải nối nhau.
    2. k . 2^3 = 1, tức 8k = 1.
    3. k = 1/8.
- `xs_t5_hp_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2 với xác suất lần lượt 1/4, 1/2, 1/4. Với hàm phân phối F(x) = P(X < x), tính F(1) rồi tính P(X >= 1). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Theo định nghĩa, F(1) = P(X < 1).
    2. F(1) = P(X = 0) + P(X = 1) = 1/4 + 1/2 = 3/4.   **<- bước sai đầu tiên**
    3. P(X >= 1) là sự kiện đối của X < 1, nên P(X >= 1) = 1 - F(1).
    4. Vậy P(X >= 1) = 1 - 3/4 = 1/4.
  - **Đáp án:** Bước 2: F(1) = P(X = 0) + P(X = 1) = 1/4 + 1/2 = 3/4.
  - **Vì sao sai, và bước đúng:**
    1. F(1) = P(X < 1) không chứa giá trị 1: F(1) = P(X = 0) = 1/4.
    2. Bước 3 vẫn đúng, nên P(X >= 1) = 1 - 1/4 = 3/4.
    3. Kiểm tra: P(X >= 1) = 1/2 + 1/4 = 3/4.
- `xs_t5_hp_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi biến ngẫu nhiên X (rời rạc hay liên tục) có hàm phân phối F(x) = P(X < x), và mọi số thực a < b, ta có P(a <= X < b) = F(b) - F(a).
  - **Đáp án:** Đúng
    1. Sự kiện X < b là tổng của hai sự kiện xung khắc X < a và a <= X < b.
    2. Nên F(b) = F(a) + P(a <= X < b), tức P(a <= X < b) = F(b) - F(a).
    3. Công thức đúng với mọi biến, nhờ quy ước X < x; với hai đầu khác (như <= ở bên phải) thì biến rời rạc phải cộng thêm một bước nhảy. Mệnh đề đúng.

### Hàm mật độ xác suất (`xs_t5_mat_do`)

- `xs_t5_md_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2]. Tìm k.
  - **Đáp án:** 1/2
    1. Tích phân của hàm mật độ trên cả trục số bằng 1.
    2. Tích phân của kx từ 0 đến 2 là k . 2^2/2 = 2k.
    3. 2k = 1, nên k = 1/2.
- `xs_t5_md_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1] là hàm mật độ của một biến ngẫu nhiên liên tục.
  - **Đáp án:** Đúng
    1. Kiểm tra f(x) >= 0 với mọi x: đúng, vì 2x >= 0 trên [0, 1] và f bằng 0 ở nơi khác.
    2. Tích phân của 2x từ 0 đến 1 bằng 1^2 - 0 = 1.
    3. Cả hai điều kiện đều thỏa. Mệnh đề đúng.
- `xs_t5_md_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào dưới đây là hàm mật độ của một biến ngẫu nhiên liên tục (mỗi hàm bằng 0 ngoài đoạn được nêu)?
    - **(đúng)** f(x) = 3x^2 trên [0, 1]
    - f(x) = x trên [0, 1]
    - f(x) = 2 - 4x trên [0, 1]
    - f(x) = 2x trên [0, 2]
  - **Đáp án:** f(x) = 3x^2 trên [0, 1]
    1. 3x^2 >= 0 và tích phân từ 0 đến 1 bằng 1: là hàm mật độ.
    2. x trên [0, 1] có tích phân 1/2; 2x trên [0, 2] có tích phân 4: tổng khác 1.
    3. 2 - 4x âm khi x > 1/2 (và tích phân bằng 0): không được.
- `xs_t5_md_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = k(1 - x^2) khi -1 <= x <= 1 và f(x) = 0 nơi khác. Sắp xếp các bước tìm k.
  - **Đáp án (thứ tự đúng):**
    1. Hàm mật độ phải không âm và có tích phân trên cả trục số bằng 1.
    2. f bằng 0 ngoài [-1, 1], nên chỉ cần tính tích phân trên [-1, 1].
    3. Tích phân của 1 - x^2 từ -1 đến 1 bằng 2 - 2/3 = 4/3.
    4. Đặt k . 4/3 = 1, được k = 3/4; khi đó f >= 0 trên [-1, 1].
  - **Lời giải:**
    1. Điều kiện chuẩn hóa: tích phân của f bằng 1.
    2. Nguyên hàm của 1 - x^2 là x - x^3/3; từ -1 đến 1 được (1 - 1/3) - (-1 + 1/3) = 4/3.
    3. k = 3/4.
- `xs_g5_hang_so` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tìm hằng số k.
  - **Đáp án:** 2
    1. Tích phân của hàm mật độ trên cả trục số phải bằng 1; ngoài [0, 1] f bằng 0.
    2. Tích phân của kx từ 0 đến 1 là k . 1^2/2 = k . 1/2.
    3. Cho bằng 1: k = 2.
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tìm hằng số k.
  - **Đáp án:** 2
    1. Tích phân của hàm mật độ trên cả trục số phải bằng 1; ngoài [0, 1] f bằng 0.
    2. Tích phân của kx từ 0 đến 1 là k . 1^2/2 = k . 1/2.
    3. Cho bằng 1: k = 2.
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2]. Tìm hằng số k.
  - **Đáp án:** 1/2
    1. Tích phân của hàm mật độ trên cả trục số phải bằng 1; ngoài [0, 2] f bằng 0.
    2. Tích phân của kx từ 0 đến 2 là k . 2^2/2 = k . 2.
    3. Cho bằng 1: k = 1/2.
- `xs_g5_mat_do_tf` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = 4x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1] là hàm mật độ của một biến ngẫu nhiên liên tục.
  - **Đáp án:** Sai
    1. Hàm mật độ cần f(x) >= 0 với mọi x (ở đây đúng) và tích phân trên cả trục số bằng 1.
    2. Tích phân của 4x từ 0 đến 1 là 4 . 1^2/2 = 2.
    3. Tích phân bằng 2, khác 1, nên f không là hàm mật độ.
  - **Câu hỏi:** Hàm f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1] là hàm mật độ của một biến ngẫu nhiên liên tục.
  - **Đáp án:** Đúng
    1. Hàm mật độ cần f(x) >= 0 với mọi x (ở đây đúng) và tích phân trên cả trục số bằng 1.
    2. Tích phân của 2x từ 0 đến 1 là 2 . 1^2/2 = 1.
    3. Tích phân bằng 1 nên f là hàm mật độ.
  - **Câu hỏi:** Hàm f(x) = x khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2] là hàm mật độ của một biến ngẫu nhiên liên tục.
  - **Đáp án:** Sai
    1. Hàm mật độ cần f(x) >= 0 với mọi x (ở đây đúng) và tích phân trên cả trục số bằng 1.
    2. Tích phân của x từ 0 đến 2 là 1 . 2^2/2 = 2.
    3. Tích phân bằng 2, khác 1, nên f không là hàm mật độ.
- `xs_t5_md_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm phân phối F(x) = 0 khi x <= 0, F(x) = x^2(3 - 2x) khi 0 < x <= 1, F(x) = 1 khi x > 1. Tính giá trị của hàm mật độ f tại x = 1/2.
  - **Đáp án:** 3/2
    1. Hàm mật độ là đạo hàm của hàm phân phối: f(x) = F'(x) ở những chỗ F khả vi.
    2. Trên (0, 1): F(x) = 3x^2 - 2x^3, nên f(x) = 6x - 6x^2.
    3. f(1/2) = 3 - 3/2 = 3/2. Hàm mật độ lớn hơn 1 ở một điểm là bình thường.
- `xs_t5_md_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tìm k để f(x) = kx^2 khi 0 <= x <= 1/2 và f(x) = 0 nơi khác là hàm mật độ. Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Điều kiện: f không âm và tích phân của f trên [0, 1/2] bằng 1.
    2. Tích phân của kx^2 từ 0 đến 1/2 bằng k . (1/2)^3/3 = k/24.
    3. k/24 = 1, nên k = 24.
    4. Nhưng khi đó f(1/2) = 6 > 1, mà hàm mật độ không được lớn hơn 1, nên không có k nào thỏa mãn.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Nhưng khi đó f(1/2) = 6 > 1, mà hàm mật độ không được lớn hơn 1, nên không có k nào thỏa mãn.
  - **Vì sao sai, và bước đúng:**
    1. Hàm mật độ không phải là xác suất: nó chỉ cần không âm và có tích phân bằng 1, có thể lớn hơn 1 tại nhiều điểm.
    2. Xác suất là diện tích dưới đồ thị f, và diện tích đó vẫn bằng 1.
    3. Vậy k = 24 là đáp số đúng.
- `xs_t5_md_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu X là biến ngẫu nhiên liên tục với hàm mật độ f liên tục thì với mọi số thực x, f(x) = P(X = x).
  - **Đáp án:** Sai
    1. Với biến liên tục, P(X = x) = 0 với mọi x.
    2. Còn f(x) có thể dương, ví dụ f(x) = 2x trên [0, 1] có f(1/2) = 1.
    3. f(x) chỉ cho biết xác suất gần x: P(x <= X < x + h) xấp xỉ f(x) h khi h nhỏ. Mệnh đề sai.
- `xs_t5_md_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = k(2 - x) khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2]. Hàm phân phối F(x) = P(X < x).
  - **Phần a** (Điền số): a) Tìm k.
    - **Đáp án a:** 1/2
  - **Phần b** (Điền số): b) Tính F(1).
    - **Đáp án b:** 3/4
  - **Phần c** (Đúng/Sai): c) P(X > 1) = 1/4.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Tích phân của 2 - x từ 0 đến 2 bằng 4 - 2 = 2, nên 2k = 1, k = 1/2.
    2. b) F(1) = tích phân của (2 - x)/2 từ 0 đến 1 = (2 - 1/2)/2 = 3/4.
    3. c) P(X > 1) = 1 - F(1) = 1/4 (với biến liên tục, P(X = 1) = 0). Mệnh đề đúng.

### Xác suất rơi vào một khoảng (`xs_t5_xac_suat_khoang`)

- `xs_t5_xk_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2, 3 với xác suất lần lượt 1/10, 2/5, 3/10, 1/5. Tính P(1 <= X < 3).
  - **Đáp án:** 7/10
    1. Các giá trị thỏa 1 <= X < 3 là 1 và 2; giá trị 3 không được tính.
    2. P(1 <= X < 3) = 2/5 + 3/10 = 7/10.
    3. Cũng bằng F(3) - F(1) = 8/10 - 1/10 = 7/10.
- `xs_t5_xk_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi biến ngẫu nhiên liên tục X (có hàm mật độ), P(1 <= X <= 2) = P(1 < X < 2).
  - **Đáp án:** Đúng
    1. Hai sự kiện chỉ khác nhau ở hai điểm X = 1 và X = 2.
    2. Với biến liên tục, P(X = 1) = P(X = 2) = 0.
    3. Vậy hai xác suất bằng nhau. Mệnh đề đúng (với biến rời rạc thì nói chung không đúng).
- `xs_t5_xk_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tính P(1/2 < X < 1).
  - **Đáp án:** 3/4
    1. P(1/2 < X < 1) = tích phân của 2x từ 1/2 đến 1.
    2. = 1^2 - (1/2)^2 = 1 - 1/4 = 3/4.
- `xs_t5_xk_04` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm phân phối F(x) = 0 khi x <= 0, F(x) = x^2/4 khi 0 < x <= 2, F(x) = 1 khi x > 2. Ghép mỗi xác suất với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - P(X < 1) — 1/4
    - P(1 <= X < 2) — 3/4
    - P(X >= 1.5) — 7/16
    - P(0.5 <= X < 1) — 3/16
  - **Lời giải:**
    1. P(X < 1) = F(1) = 1/4; P(1 <= X < 2) = F(2) - F(1) = 1 - 1/4 = 3/4.
    2. P(X >= 1.5) = 1 - F(1.5) = 1 - 2.25/4 = 1 - 9/16 = 7/16.
    3. P(0.5 <= X < 1) = F(1) - F(0.5) = 1/4 - 1/16 = 3/16.
- `xs_t5_xk_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X có hàm phân phối F(x) = P(X < x): F(x) = 0 khi x <= -1; 1/5 khi -1 < x <= 0; 1/2 khi 0 < x <= 2; 9/10 khi 2 < x <= 3; 1 khi x > 3. Tính P(0 <= X < 3).
  - **Đáp án:** 7/10
    1. Với quy ước F(x) = P(X < x): P(a <= X < b) = F(b) - F(a).
    2. P(0 <= X < 3) = F(3) - F(0) = 9/10 - 1/5 = 7/10.
    3. Kiểm tra bằng bước nhảy: P(X = 0) = 1/2 - 1/5 = 3/10, P(X = 2) = 9/10 - 1/2 = 2/5, cộng lại 7/10.
- `xs_t5_xk_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 2, 3, 4 với xác suất lần lượt 1/10, 1/5, 3/10, 2/5, và F(x) = P(X < x). Tính P(2 <= X <= 3). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Với mọi a < b: P(a <= X < b) = F(b) - F(a).
    2. Áp dụng: P(2 <= X <= 3) = F(3) - F(2).   **<- bước sai đầu tiên**
    3. F(3) = P(X < 3) = 3/10 và F(2) = P(X < 2) = 1/10.
    4. Vậy P(2 <= X <= 3) = 1/5.
  - **Đáp án:** Bước 2: Áp dụng: P(2 <= X <= 3) = F(3) - F(2).
  - **Vì sao sai, và bước đúng:**
    1. F(3) - F(2) là P(2 <= X < 3), không chứa giá trị 3. Biến rời rạc có P(X = 3) = 3/10 khác 0, nên dấu <= ở đầu phải quan trọng.
    2. Đúng là P(2 <= X <= 3) = P(2 <= X < 4) = F(4) - F(2) = 3/5 - 1/10 = 1/2.
    3. Kiểm tra: 1/5 + 3/10 = 1/2.
- `xs_t5_xk_07` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = (3/8)x^2 khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2]. P(X > 1) bằng bao nhiêu?
    - **(đúng)** 7/8
    - 1/8
    - 3/8
    - 1/2
  - **Đáp án:** 7/8
    1. Hàm phân phối trên [0, 2]: F(x) = tích phân của (3/8)t^2 từ 0 đến x = x^3/8.
    2. P(X > 1) = 1 - F(1) = 1 - 1/8 = 7/8.
    3. 1/8 là P(X < 1); 1/2 là nhầm mật độ thành đều.
- `xs_t5_xk_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx^2 khi 0 <= x <= 3 và f(x) = 0 khi x nằm ngoài [0, 3]. Hàm phân phối F(x) = P(X < x).
  - **Phần a** (Điền số): a) Tìm k.
    - **Đáp án a:** 1/9
  - **Phần b** (Điền số): b) Tính F(2).
    - **Đáp án b:** 8/27
  - **Phần c** (Điền số): c) Tính P(1 <= X < 2).
    - **Đáp án c:** 7/27
  - **Lời giải:**
    1. a) Tích phân của kx^2 từ 0 đến 3 bằng k . 27/3 = 9k = 1, nên k = 1/9.
    2. b) Trên [0, 3]: F(x) = tích phân của t^2/9 từ 0 đến x = x^3/27, nên F(2) = 8/27.
    3. c) P(1 <= X < 2) = F(2) - F(1) = 8/27 - 1/27 = 7/27.
- `xs_g5_khoang` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tính P(0 <= X < 0.5).
  - **Đáp án:** 1/4
    1. Hàm phân phối trên [0, 1]: F(x) = tích phân của f từ 0 đến x = (x/1)^2; F(x) = 0 khi x <= 0 và F(x) = 1 khi x > 1.
    2. P(0 <= X < 0.5) = F(0.5) - F(0) = 1/4 - 0 = 1/4.
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tính P(0 <= X < 0.5).
  - **Đáp án:** 1/4
    1. Hàm phân phối trên [0, 1]: F(x) = tích phân của f từ 0 đến x = (x/1)^2; F(x) = 0 khi x <= 0 và F(x) = 1 khi x > 1.
    2. P(0 <= X < 0.5) = F(0.5) - F(0) = 1/4 - 0 = 1/4.
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = (1/2)x khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2]. Tính P(1 <= X < 1.5).
  - **Đáp án:** 5/16
    1. Hàm phân phối trên [0, 2]: F(x) = tích phân của f từ 0 đến x = (x/2)^2; F(x) = 0 khi x <= 0 và F(x) = 1 khi x > 2.
    2. P(1 <= X < 1.5) = F(1.5) - F(1) = 9/16 - 1/4 = 5/16.

## Tầng 6: Các số đặc trưng và các phân phối thông dụng

47 dạng câu (40 câu viết tay, 7 bộ sinh câu); 47 chưa duyệt.

### Kỳ vọng (`xs_t6_ky_vong`)

- `xs_t6_kv_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị -1, 0, 2 với xác suất lần lượt 1/5, 1/2, 3/10. Tính E(X).
  - **Đáp án:** 2/5
    1. E(X) = tổng của x_i p_i.
    2. E(X) = (-1) . 1/5 + 0 . 1/2 + 2 . 3/10 = -1/5 + 3/5 = 2/5.
- `xs_t6_kv_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi biến ngẫu nhiên X có kỳ vọng, E(3X - 2) = 3E(X) - 2.
  - **Đáp án:** Đúng
    1. Kỳ vọng tuyến tính: E(aX + b) = aE(X) + b với mọi hằng số a, b.
    2. Với a = 3, b = -2: E(3X - 2) = 3E(X) - 2. Mệnh đề đúng.
- `xs_t6_kv_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = 2x khi 0 <= x <= 1 và f(x) = 0 khi x nằm ngoài [0, 1]. Tính E(X).
  - **Đáp án:** 2/3
    1. Với biến liên tục, E(X) = tích phân của x f(x) trên cả trục số.
    2. E(X) = tích phân của 2x^2 từ 0 đến 1 = 2/3.
- `xs_t6_kv_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đệ tử trả 2 linh thạch để chơi một lần: gieo một con xúc xắc cân đối, ra mặt 6 thì nhận 9 linh thạch, ra mặt 5 thì nhận 3 linh thạch, các mặt khác không nhận gì. Kỳ vọng số linh thạch lãi (số nhận trừ số trả) sau một lần chơi là bao nhiêu?
    - **(đúng)** 0
    - 2
    - -2
    - 1/3
  - **Đáp án:** 0
    1. Số linh thạch nhận được có kỳ vọng 9 . 1/6 + 3 . 1/6 + 0 . 4/6 = 12/6 = 2.
    2. Lãi = nhận - 2, nên E(lãi) = 2 - 2 = 0.
    3. Trò chơi công bằng: chơi nhiều lần thì trung bình không lãi không lỗ.
- `xs_g6_ky_vong` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 4, 5 với xác suất lần lượt 1/4, 1/4, 1/2. Tính kỳ vọng E(X).
  - **Đáp án:** 15/4
    1. E(X) = tổng của x_i p_i theo mọi giá trị.
    2. E(X) = 1 . (1/4) + 4 . (1/4) + 5 . (1/2) = 15/4.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 3, 4 với xác suất lần lượt 1/4, 1/4, 1/2. Tính kỳ vọng E(X).
  - **Đáp án:** 11/4
    1. E(X) = tổng của x_i p_i theo mọi giá trị.
    2. E(X) = 0 . (1/4) + 3 . (1/4) + 4 . (1/2) = 11/4.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 2, 3, 5 với xác suất lần lượt 3/5, 1/5, 1/5. Tính kỳ vọng E(X).
  - **Đáp án:** 14/5
    1. E(X) = tổng của x_i p_i theo mọi giá trị.
    2. E(X) = 2 . (3/5) + 3 . (1/5) + 5 . (1/5) = 14/5.
- `xs_t6_kv_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo hai con xúc xắc cân đối, phân biệt được với nhau. Gọi X là số chấm lớn hơn trong hai số chấm (bằng nhau thì lấy số đó). Tính E(X).
  - **Đáp án:** 161/36
    1. P(X = k) = (k^2 - (k - 1)^2)/36 = (2k - 1)/36 với k = 1, ..., 6.
    2. E(X) = (1 . 1 + 2 . 3 + 3 . 5 + 4 . 7 + 5 . 9 + 6 . 11)/36.
    3. = (1 + 6 + 15 + 28 + 45 + 66)/36 = 161/36.
- `xs_t6_kv_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X nhận các giá trị 1 và 2, mỗi giá trị với xác suất 1/2. Tính E(1/X). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. E(X) = 1 . 1/2 + 2 . 1/2 = 3/2.
    2. Kỳ vọng giữ nguyên qua mọi hàm số, nên E(1/X) = 1/E(X).   **<- bước sai đầu tiên**
    3. Vậy E(1/X) = 2/3.
  - **Đáp án:** Bước 2: Kỳ vọng giữ nguyên qua mọi hàm số, nên E(1/X) = 1/E(X).
  - **Vì sao sai, và bước đúng:**
    1. Chỉ hàm bậc nhất aX + b mới đi qua kỳ vọng được; với hàm khác phải tính theo bảng: E(g(X)) = tổng của g(x_i) p_i.
    2. E(1/X) = 1 . 1/2 + 1/2 . 1/2 = 3/4, khác 2/3.
- `xs_t6_kv_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo 10 con xúc xắc cân đối và gọi S là tổng số chấm. Khi đó E(S) = 35.
  - **Đáp án:** Đúng
    1. S = X_1 + ... + X_10, với X_i là số chấm của xúc xắc thứ i.
    2. E(X_i) = (1 + 2 + ... + 6)/6 = 7/2.
    3. Kỳ vọng của tổng bằng tổng các kỳ vọng (không cần độc lập): E(S) = 10 . 7/2 = 35. Mệnh đề đúng.
- `xs_t6_kv_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = kx khi 0 <= x <= 2 và f(x) = 0 khi x nằm ngoài [0, 2].
  - **Phần a** (Điền số): a) Tìm k.
    - **Đáp án a:** 1/2
  - **Phần b** (Điền số): b) Tính E(X).
    - **Đáp án b:** 4/3
  - **Phần c** (Điền số): c) Tính V(X).
    - **Đáp án c:** 2/9
  - **Lời giải:**
    1. a) Tích phân của kx từ 0 đến 2 bằng 2k = 1, nên k = 1/2.
    2. b) E(X) = tích phân của x . x/2 từ 0 đến 2 = (1/2)(8/3) = 4/3.
    3. c) E(X^2) = tích phân của x^2 . x/2 từ 0 đến 2 = (1/2)(16/4) = 2; V(X) = 2 - (4/3)^2 = 2 - 16/9 = 2/9.

### Phương sai và độ lệch chuẩn (`xs_t6_phuong_sai`)

- `xs_t6_ps_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2 với xác suất lần lượt 1/4, 1/2, 1/4. Tính V(X).
  - **Đáp án:** 1/2
    1. E(X) = 0 . 1/4 + 1 . 1/2 + 2 . 1/4 = 1.
    2. E(X^2) = 0 . 1/4 + 1 . 1/2 + 4 . 1/4 = 3/2.
    3. V(X) = E(X^2) - (E(X))^2 = 3/2 - 1 = 1/2.
- `xs_t6_ps_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu V(X) = 4 thì V(3X + 1) = 13.
  - **Đáp án:** Sai
    1. V(aX + b) = a^2 V(X): hằng số b không làm đổi độ phân tán, còn hệ số a được bình phương.
    2. V(3X + 1) = 9 . 4 = 36.
    3. 13 = 3 . 4 + 1 là áp dụng nhầm V(aX + b) = aV(X) + b. Mệnh đề sai.
- `xs_t6_ps_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có V(X) = 9. Độ lệch chuẩn của Y = -2X + 5 là bao nhiêu?
    - **(đúng)** 6
    - -6
    - 36
    - 13
  - **Đáp án:** 6
    1. V(Y) = (-2)^2 V(X) = 4 . 9 = 36.
    2. Độ lệch chuẩn là căn bậc hai của phương sai: căn của 36 = 6.
    3. Độ lệch chuẩn không bao giờ âm, nên -6 sai; 36 là phương sai.
- `xs_t6_ps_04` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có E(X) = 2 và V(X) = 3. Ghép mỗi đại lượng với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - E(2X + 1) — 5
    - V(2X + 1) — 12
    - E(X^2) — 7
    - V(-X) — 3
  - **Lời giải:**
    1. E(2X + 1) = 2 . 2 + 1 = 5; V(2X + 1) = 4 . 3 = 12.
    2. Từ V(X) = E(X^2) - (E(X))^2: E(X^2) = 3 + 4 = 7.
    3. V(-X) = (-1)^2 V(X) = 3: đổi dấu không làm đổi độ phân tán.
- `xs_g6_phuong_sai` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 4, 5 với xác suất lần lượt 1/4, 1/4, 1/2. Tính phương sai V(X).
  - **Đáp án:** 43/16
    1. E(X) = 15/4.
    2. E(X^2) = 1 . (1/4) + 16 . (1/4) + 25 . (1/2) = 67/4.
    3. V(X) = E(X^2) - (E(X))^2 = 67/4 - (15/4)^2 = 43/16.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 3, 4 với xác suất lần lượt 1/4, 1/4, 1/2. Tính phương sai V(X).
  - **Đáp án:** 43/16
    1. E(X) = 11/4.
    2. E(X^2) = 0 . (1/4) + 9 . (1/4) + 16 . (1/2) = 41/4.
    3. V(X) = E(X^2) - (E(X))^2 = 41/4 - (11/4)^2 = 43/16.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 2, 3, 5 với xác suất lần lượt 3/5, 1/5, 1/5. Tính phương sai V(X).
  - **Đáp án:** 34/25
    1. E(X) = 14/5.
    2. E(X^2) = 4 . (3/5) + 9 . (1/5) + 25 . (1/5) = 46/5.
    3. V(X) = E(X^2) - (E(X))^2 = 46/5 - (14/5)^2 = 34/25.
- `xs_t6_ps_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X nhận giá trị -1 và 1, mỗi giá trị với xác suất 1/2. Tính V(X). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. E(X) = (-1) . 1/2 + 1 . 1/2 = 0.
    2. E(X^2) = (E(X))^2 = 0.   **<- bước sai đầu tiên**
    3. V(X) = E(X^2) - (E(X))^2 = 0 - 0 = 0.
    4. Phương sai bằng 0, nên X luôn nhận cùng một giá trị.
  - **Đáp án:** Bước 2: E(X^2) = (E(X))^2 = 0.
  - **Vì sao sai, và bước đúng:**
    1. E(X^2) phải tính theo bảng: (-1)^2 . 1/2 + 1^2 . 1/2 = 1. Nói chung E(X^2) khác (E(X))^2, hiệu của chúng chính là V(X).
    2. V(X) = 1 - 0 = 1, đúng với việc X lúc là -1 lúc là 1.
- `xs_t6_ps_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung một đồng xu cân đối một lần. X là số lần ra mặt ngửa (0 hoặc 1), và Y = X. Tính V(X + Y). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. X nhận 0 và 1, mỗi giá trị với xác suất 1/2, nên E(X) = 1/2 và V(X) = 1/2 - 1/4 = 1/4.
    2. Y = X nên V(Y) = 1/4.
    3. Phương sai của tổng bằng tổng các phương sai: V(X + Y) = 1/4 + 1/4 = 1/2.   **<- bước sai đầu tiên**
    4. Vậy V(X + Y) = 1/2.
  - **Đáp án:** Bước 3: Phương sai của tổng bằng tổng các phương sai: V(X + Y) = 1/4 + 1/4 = 1/2.
  - **Vì sao sai, và bước đúng:**
    1. V(X + Y) = V(X) + V(Y) chỉ đúng khi X, Y độc lập; ở đây Y = X, phụ thuộc hoàn toàn.
    2. X + Y = 2X, nên V(X + Y) = 4 V(X) = 1.
- `xs_t6_ps_07` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X và Y là hai biến ngẫu nhiên độc lập với V(X) = 2 và V(Y) = 3. Tính V(2X - Y + 4).
  - **Đáp án:** 11
    1. X, Y độc lập nên V(aX + bY + c) = a^2 V(X) + b^2 V(Y).
    2. V(2X - Y + 4) = 4 . 2 + (-1)^2 . 3 = 8 + 3 = 11.
    3. Dấu trừ trước Y không làm phương sai bị trừ đi.
- `xs_t6_ps_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 1, 2, 3 với xác suất lần lượt 1/10, a, 2/5, 1/5.
  - **Phần a** (Điền số): a) Tìm a.
    - **Đáp án a:** 3/10
  - **Phần b** (Điền số): b) Tính E(X).
    - **Đáp án b:** 17/10
  - **Phần c** (Điền số): c) Tính V(X).
    - **Đáp án c:** 81/100
  - **Lời giải:**
    1. a) a = 1 - 1/10 - 2/5 - 1/5 = 3/10.
    2. b) E(X) = 0 . 1/10 + 1 . 3/10 + 2 . 2/5 + 3 . 1/5 = 3/10 + 8/10 + 6/10 = 17/10.
    3. c) E(X^2) = 1 . 3/10 + 4 . 2/5 + 9 . 1/5 = 3/10 + 16/10 + 18/10 = 37/10; V(X) = 37/10 - 289/100 = 81/100.
- `xs_g6_bien_doi` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 1, 4, 5 với xác suất lần lượt 1/4, 1/4, 1/2. Đặt Y = 2X + 5. Tính V(Y).
  - **Đáp án:** 43/4
    1. E(X) = 15/4, V(X) = E(X^2) - (E(X))^2 = 43/16.
    2. Hằng số cộng thêm không làm đổi phương sai, còn hệ số nhân ra ngoài thì bình phương lên: V(2X + 5) = 2^2 V(X) = 4 . (43/16) = 43/4.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 0, 3, 4 với xác suất lần lượt 1/4, 1/4, 1/2. Đặt Y = -X - 1. Tính E(Y).
  - **Đáp án:** -15/4
    1. E(X) = 11/4.
    2. E(-X - 1) = -1 E(X) - 1 = -15/4.
  - **Câu hỏi:** Biến ngẫu nhiên rời rạc X nhận các giá trị 2, 3, 5 với xác suất lần lượt 3/5, 1/5, 1/5. Đặt Y = -3X + 4. Tính E(Y).
  - **Đáp án:** -22/5
    1. E(X) = 14/5.
    2. E(-3X + 4) = -3 E(X) + 4 = -22/5.

### Phân phối nhị thức và Poisson (`xs_t6_nhi_thuc_poisson`)

- `xs_t6_np_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối nhị thức B(10, 1/5). Tính V(X).
  - **Đáp án:** 8/5
    1. Với X ~ B(n, p): V(X) = np(1 - p).
    2. V(X) = 10 . 1/5 . 4/5 = 8/5.
- `xs_t6_np_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu X có phân phối Poisson với tham số lambda = 3 thì E(X) = V(X) = 3.
  - **Đáp án:** Đúng
    1. Phân phối Poisson tham số lambda có kỳ vọng và phương sai đều bằng lambda.
    2. Với lambda = 3: E(X) = V(X) = 3. Mệnh đề đúng.
- `xs_t6_np_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tổng đài nhận trung bình 4 cuộc gọi mỗi phút; các cuộc gọi đến ngẫu nhiên và độc lập với nhau. Phân phối nào là mô hình hợp lý cho số cuộc gọi X đến trong một phút?
    - **(đúng)** Poisson với lambda = 4
    - Nhị thức B(4, 1/2)
    - Đều trên đoạn [0, 4]
    - Poisson với lambda = 1/4
  - **Đáp án:** Poisson với lambda = 4
    1. Đếm số lần một sự kiện hiếm, độc lập xảy ra trong một khoảng thời gian: phân phối Poisson.
    2. Tham số lambda là số trung bình trong khoảng đó: lambda = 4.
    3. B(4, 1/2) chỉ cho tối đa 4 cuộc gọi; phân phối đều là liên tục, không đếm được số cuộc gọi.
- `xs_t6_np_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số lỗi in X trên một trang sách có phân phối Poisson với tham số lambda = 2. Dùng giá trị e^(-2) = 0.1353. Tính P(X = 2) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1353/5000
    1. P(X = k) = e^(-lambda) lambda^k / k!.
    2. P(X = 2) = e^(-2) . 2^2/2! = 2 e^(-2).
    3. = 2 . 0.1353 = 0.2706.
- `xs_g6_nhi_thuc` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối nhị thức B(8, 1/10): số lần thành công trong 8 phép thử độc lập, mỗi lần thành công với xác suất 1/10. Tính kỳ vọng E(X).
  - **Đáp án:** 4/5
    1. X ~ B(n, p) với n = 8, p = 1/10.
    2. E(X) = np = 8 . (1/10) = 4/5.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối nhị thức B(5, 1/2): số lần thành công trong 5 phép thử độc lập, mỗi lần thành công với xác suất 1/2. Tính kỳ vọng E(X).
  - **Đáp án:** 5/2
    1. X ~ B(n, p) với n = 5, p = 1/2.
    2. E(X) = np = 5 . (1/2) = 5/2.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối nhị thức B(6, 1/10): số lần thành công trong 6 phép thử độc lập, mỗi lần thành công với xác suất 1/10. Tính xác suất P(X = 1).
  - **Đáp án:** 177147/500000
    1. X ~ B(n, p) với n = 6, p = 1/10.
    2. P(X = 1) = C(6, 1) p^1 (1 - p)^5 = 6 . (1/10)^1 . (9/10)^5 = 177147/500000.
- `xs_t6_np_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X có phân phối nhị thức B(20, 1/4). Tính V(X). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. X có phân phối nhị thức với n = 20, p = 1/4.
    2. E(X) = np = 20 . 1/4 = 5.
    3. Với phân phối nhị thức, phương sai bằng kỳ vọng, nên V(X) = 5.   **<- bước sai đầu tiên**
    4. Độ lệch chuẩn của X là căn của 5.
  - **Đáp án:** Bước 3: Với phân phối nhị thức, phương sai bằng kỳ vọng, nên V(X) = 5.
  - **Vì sao sai, và bước đúng:**
    1. Phương sai bằng kỳ vọng là tính chất của phân phối Poisson, không phải nhị thức.
    2. Với nhị thức: V(X) = np(1 - p) = 20 . 1/4 . 3/4 = 15/4, nhỏ hơn kỳ vọng.
- `xs_t6_np_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối Poisson với tham số lambda = 6, tức P(X = k) = e^(-6) 6^k / k! với k = 0, 1, 2, ... Tính tỉ số P(X = 3) / P(X = 2).
  - **Đáp án:** 2
    1. P(X = 3) / P(X = 2) = (6^3/3!) / (6^2/2!), vì e^(-6) giản ước.
    2. = 6 . 2!/3! = 6/3 = 2.
    3. Tổng quát P(X = k)/P(X = k - 1) = lambda/k.
- `xs_t6_np_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lô có 1000 sản phẩm, mỗi sản phẩm hỏng với xác suất 1/500, độc lập với nhau. Số sản phẩm hỏng X xấp xỉ được bằng phân phối Poisson với tham số lambda = 500.
  - **Đáp án:** Sai
    1. X ~ B(1000, 1/500): n lớn, p nhỏ, nên xấp xỉ được bằng Poisson.
    2. Tham số Poisson phải bằng kỳ vọng: lambda = np = 1000 . 1/500 = 2.
    3. 500 là 1/p, lẫn giữa các tham số. Mệnh đề sai.
- `xs_t6_np_08` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi sản phẩm của một máy là phế phẩm với xác suất 1/10, độc lập với nhau. Kiểm tra 20 sản phẩm và gọi X là số phế phẩm.
  - **Phần a** (Điền số): a) Tính E(X).
    - **Đáp án a:** 2
  - **Phần b** (Điền số): b) Tính V(X).
    - **Đáp án b:** 9/5
  - **Phần c** (Trắc nghiệm): c) Nếu xấp xỉ X bằng một phân phối Poisson thì tham số nên chọn là gì?
    - **(đúng)** lambda = 2
    - lambda = 9/5
    - lambda = 20
    - lambda = 1/10
    - **Đáp án c:** lambda = 2
  - **Lời giải:**
    1. a) X ~ B(20, 1/10): E(X) = np = 2.
    2. b) V(X) = np(1 - p) = 20 . 1/10 . 9/10 = 9/5.
    3. c) Xấp xỉ Poisson giữ nguyên kỳ vọng: lambda = np = 2 (phương sai của Poisson cũng là 2, gần 9/5 khi p nhỏ).
- `xs_g6_poisson_ti_so` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Số khách X đến một quầy trong một phút có phân phối Poisson với tham số lambda = 3/2, tức P(X = j) = e^(-lambda) lambda^j / j! với j = 0, 1, 2, ... Tính tỉ số P(X = 5) / P(X = 4).
  - **Đáp án:** 3/10
    1. P(X = 5) / P(X = 4) = [e^(-lambda) lambda^5/5!] / [e^(-lambda) lambda^4/4!].
    2. e^(-lambda) giản ước, còn lại lambda/5 = (3/2)/5 = 3/10.
  - **Câu hỏi:** Số khách X đến một quầy trong một phút có phân phối Poisson với tham số lambda = 1/2, tức P(X = j) = e^(-lambda) lambda^j / j! với j = 0, 1, 2, ... Tính tỉ số P(X = 1) / P(X = 0).
  - **Đáp án:** 1/2
    1. P(X = 1) / P(X = 0) = [e^(-lambda) lambda^1/1!] / [e^(-lambda) lambda^0/0!].
    2. e^(-lambda) giản ước, còn lại lambda/1 = (1/2)/1 = 1/2.
  - **Câu hỏi:** Số khách X đến một quầy trong một phút có phân phối Poisson với tham số lambda = 2, tức P(X = j) = e^(-lambda) lambda^j / j! với j = 0, 1, 2, ... Tính tỉ số P(X = 5) / P(X = 4).
  - **Đáp án:** 2/5
    1. P(X = 5) / P(X = 4) = [e^(-lambda) lambda^5/5!] / [e^(-lambda) lambda^4/4!].
    2. e^(-lambda) giản ước, còn lại lambda/5 = 2/5 = 2/5.

### Phân phối đều và phân phối mũ (`xs_t6_deu_mu`)

- `xs_t6_dm_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên đoạn [2, 10]. Tính P(3 < X < 7).
  - **Đáp án:** 1/2
    1. Mật độ của X bằng 1/8 trên [2, 10].
    2. P(3 < X < 7) = (7 - 3)/8 = 4/8 = 1/2.
- `xs_t6_dm_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu X có phân phối đều trên đoạn [0, 6] thì V(X) = 3.
  - **Đáp án:** Đúng
    1. Với X đều trên [a, b]: V(X) = (b - a)^2/12.
    2. V(X) = 36/12 = 3. Mệnh đề đúng.
- `xs_t6_dm_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian chờ X (phút) của một khách hàng có phân phối mũ với tham số lambda = 1/5, tức hàm mật độ f(x) = (1/5)e^(-x/5) khi x > 0 và f(x) = 0 khi x <= 0. Tính E(X).
  - **Đáp án:** 5
    1. Phân phối mũ tham số lambda có E(X) = 1/lambda.
    2. E(X) = 1/(1/5) = 5 phút.
- `xs_t6_dm_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian chờ X (phút) có phân phối mũ với tham số lambda = 1/5 (hàm mật độ (1/5)e^(-x/5) khi x > 0). P(X > 10) bằng bao nhiêu?
    - **(đúng)** e^(-2)
    - 1 - e^(-2)
    - e^(-1/2)
    - 2
  - **Đáp án:** e^(-2)
    1. Hàm phân phối của phân phối mũ: F(x) = 1 - e^(-lambda x) khi x > 0.
    2. P(X > 10) = 1 - F(10) = e^(-10/5) = e^(-2).
    3. 1 - e^(-2) là P(X < 10); một xác suất không thể bằng 2.
- `xs_g6_deu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên đoạn [-2, 1]. Tính V(X).
  - **Đáp án:** 3/4
    1. X đều trên [-2, 1]: mật độ f(x) = 1/3 trên đoạn đó, bằng 0 ngoài đoạn.
    2. V(X) = (b - a)^2/12 = 3^2/12 = 3/4.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên đoạn [-4, -1]. Tính E(X).
  - **Đáp án:** -5/2
    1. X đều trên [-4, -1]: mật độ f(x) = 1/3 trên đoạn đó, bằng 0 ngoài đoạn.
    2. E(X) = (a + b)/2 = (-4 + -1)/2 = -5/2.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên đoạn [-1, 9]. Tính E(X).
  - **Đáp án:** 4
    1. X đều trên [-1, 9]: mật độ f(x) = 1/10 trên đoạn đó, bằng 0 ngoài đoạn.
    2. E(X) = (a + b)/2 = (-1 + 9)/2 = 4.
- `xs_t6_dm_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X có phân phối đều trên đoạn [2, 8]. Tính V(X). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm mật độ của X bằng 1/6 trên [2, 8] và bằng 0 nơi khác.
    2. E(X) = (2 + 8)/2 = 5.
    3. V(X) = (8 - 2)/12 = 1/2.   **<- bước sai đầu tiên**
    4. Độ lệch chuẩn của X là căn của 1/2.
  - **Đáp án:** Bước 3: V(X) = (8 - 2)/12 = 1/2.
  - **Vì sao sai, và bước đúng:**
    1. Công thức đúng là V(X) = (b - a)^2/12: độ dài đoạn phải bình phương.
    2. V(X) = 36/12 = 3.
    3. Kiểm tra: E(X^2) = (4 + 16 + 64)/3 = 28, V(X) = 28 - 25 = 3.
- `xs_t6_dm_06` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối mũ với tham số lambda > 0. Với mọi s > 0 và t > 0, P(X > s + t | X > s) = P(X > t).
  - **Đáp án:** Đúng
    1. P(X > x) = e^(-lambda x) với x > 0.
    2. P(X > s + t | X > s) = e^(-lambda(s + t)) / e^(-lambda s) = e^(-lambda t) = P(X > t).
    3. Đây là tính chất không nhớ của phân phối mũ: đã chờ s phút rồi thì thời gian chờ thêm vẫn như lúc đầu. Mệnh đề đúng.
- `xs_t6_dm_07` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên đoạn [1, 4]. Tính E(X^2).
  - **Đáp án:** 7
    1. Mật độ bằng 1/3 trên [1, 4].
    2. E(X^2) = tích phân của x^2/3 từ 1 đến 4 = (64 - 1)/9 = 7.
    3. Kiểm tra: E(X) = 5/2, V(X) = 9/12 = 3/4, và 3/4 + 25/4 = 7.
- `xs_t6_dm_08` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi đại lượng với giá trị của nó. Phân phối mũ tham số lambda có hàm mật độ lambda e^(-lambda x) khi x > 0.
  - **Đáp án (ghép đúng):**
    - E(X), với X đều trên [0, 4] — 2
    - V(X), với X đều trên [0, 4] — 4/3
    - E(X), với X có phân phối mũ, lambda = 1/3 — 3
    - V(X), với X có phân phối mũ, lambda = 1/3 — 9
  - **Lời giải:**
    1. Đều trên [a, b]: E = (a + b)/2 = 2, V = (b - a)^2/12 = 16/12 = 4/3.
    2. Mũ tham số lambda: E = 1/lambda = 3, V = 1/lambda^2 = 9.

### Phân phối chuẩn (`xs_t6_chuan`)

- `xs_t6_ch_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối chuẩn N(10, 4) (kỳ vọng 10, phương sai 4). Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1) = 0.3413. Tính P(8 < X < 12) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 3413/5000
    1. Độ lệch chuẩn sigma = căn của 4 = 2.
    2. Chuẩn hóa: (8 - 10)/2 = -1 và (12 - 10)/2 = 1.
    3. P(8 < X < 12) = Phi(1) - Phi(-1) = 2 Phi(1) = 0.6826.
- `xs_t6_ch_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu X có phân phối chuẩn N(mu, sigma^2) với sigma > 0 thì Z = (X - mu)/sigma có phân phối chuẩn N(0, 1).
  - **Đáp án:** Đúng
    1. Một hàm bậc nhất của biến chuẩn vẫn có phân phối chuẩn.
    2. E(Z) = (E(X) - mu)/sigma = 0 và V(Z) = V(X)/sigma^2 = 1.
    3. Vậy Z ~ N(0, 1): đó là phép chuẩn hóa. Mệnh đề đúng.
- `xs_t6_ch_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối chuẩn N(50, 25) (kỳ vọng 50, phương sai 25) và Z có phân phối N(0, 1). P(X < 60) bằng xác suất nào?
    - **(đúng)** P(Z < 2)
    - P(Z < 10)
    - P(Z < 2/5)
    - P(Z < 12)
  - **Đáp án:** P(Z < 2)
    1. Độ lệch chuẩn sigma = căn của 25 = 5.
    2. Chuẩn hóa: (60 - 50)/5 = 2, nên P(X < 60) = P(Z < 2).
    3. P(Z < 2/5) là chia cho phương sai 25 thay vì độ lệch chuẩn 5.
- `xs_t6_ch_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điểm thi X có phân phối chuẩn với kỳ vọng 100 và độ lệch chuẩn 10. Dùng hàm Laplace Phi với Phi(1) = 0.3413. Tính P(X > 110) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1587/10000
    1. Chuẩn hóa: (110 - 100)/10 = 1.
    2. P(X > 110) = P(Z > 1) = 0.5 - Phi(1).
    3. = 0.5 - 0.3413 = 0.1587.
- `xs_t6_ch_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X có phân phối chuẩn N(20, 9) (kỳ vọng 20, phương sai 9). Dùng Phi(1) = 0.3413, tính P(17 < X < 23). Lời giải dưới đây có chỗ sai. Bước nào là bước đầu tiên bị sai?
  - **Lời giải đưa ra (có một bước sai):**
    1. X có kỳ vọng 20 và phương sai 9.
    2. Chuẩn hóa: Z = (X - 20)/9 có phân phối N(0, 1).   **<- bước sai đầu tiên**
    3. P(17 < X < 23) = P(-1/3 < Z < 1/3).
    4. Tra bảng Phi(1/3) rồi nhân đôi.
  - **Đáp án:** Bước 2: Chuẩn hóa: Z = (X - 20)/9 có phân phối N(0, 1).
  - **Vì sao sai, và bước đúng:**
    1. Chuẩn hóa phải chia cho độ lệch chuẩn sigma = căn của 9 = 3, không chia cho phương sai.
    2. Z = (X - 20)/3, nên P(17 < X < 23) = P(-1 < Z < 1) = 2 Phi(1) = 0.6826.
- `xs_t6_ch_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối chuẩn N(70, 25) (kỳ vọng 70, phương sai 25). Dùng hàm Laplace Phi với Phi(1.5) = 0.4332 và Phi(2) = 0.4772. Tính P(60 < X < 77.5) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 569/625
    1. sigma = 5. Chuẩn hóa: (60 - 70)/5 = -2 và (77.5 - 70)/5 = 1.5.
    2. P(60 < X < 77.5) = Phi(1.5) - Phi(-2) = Phi(1.5) + Phi(2).
    3. = 0.4332 + 0.4772 = 0.9104.
- `xs_t6_ch_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối chuẩn N(5, 4) (kỳ vọng 5, phương sai 4). Dùng hàm Laplace với Phi(2) = 0.4772, ta có P(X > 9) = 0.0228.
  - **Đáp án:** Đúng
    1. sigma = 2; chuẩn hóa (9 - 5)/2 = 2.
    2. P(X > 9) = 0.5 - Phi(2) = 0.5 - 0.4772 = 0.0228.
    3. Mệnh đề đúng: một giá trị cách kỳ vọng hơn 2 độ lệch chuẩn về một phía chỉ có xác suất khoảng 2.3%.
- `xs_t6_ch_08` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chiều cao X (cm) của nam sinh một trường có phân phối chuẩn N(165, 36) (kỳ vọng 165, phương sai 36). Dùng hàm Laplace với Phi(1.5) = 0.4332. Sắp xếp các bước tính P(X > 174).
  - **Đáp án (thứ tự đúng):**
    1. Độ lệch chuẩn sigma = căn của 36 = 6.
    2. Chuẩn hóa mốc 174: (174 - 165)/6 = 1.5.
    3. P(X > 174) = P(Z > 1.5) = 0.5 - Phi(1.5).
    4. Thay số: 0.5 - 0.4332 = 0.0668.
  - **Lời giải:**
    1. Cần sigma trước để chuẩn hóa.
    2. Đổi sang Z ~ N(0, 1), rồi dùng nửa trục phải có xác suất 0.5.
    3. P(X > 174) = 0.0668.
- `xs_g6_chuan` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối chuẩn với kỳ vọng 20 và độ lệch chuẩn 2, tức X ~ N(20, 4). Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(0.5) = 0.1915. Tính P(X > 19) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1383/2000
    1. Với X ~ N(mu, sigma^2): P(a < X < b) = Phi((b - mu)/sigma) - Phi((a - mu)/sigma).
    2. Chuẩn hóa: (19 - 20)/2 = -0.5.
    3. P(X > 19) = 0.5 - Phi(-0.5) = 0.5 - (-0.1915) = 0.6915.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối chuẩn với kỳ vọng 10 và độ lệch chuẩn 2, tức X ~ N(10, 4). Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1) = 0.3413, Phi(1.5) = 0.4332. Tính P(7 < X < 12) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1549/2000
    1. Với X ~ N(mu, sigma^2): P(a < X < b) = Phi((b - mu)/sigma) - Phi((a - mu)/sigma).
    2. Chuẩn hóa: (7 - 10)/2 = -1.5 và (12 - 10)/2 = 1.
    3. P(7 < X < 12) = Phi(1) - Phi(-1.5), với Phi(-x) = -Phi(x).
    4. = 0.3413 - (-0.4332) = 0.7745.
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối chuẩn với kỳ vọng 20 và độ lệch chuẩn 4, tức X ~ N(20, 16). Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2.5) = 0.4938. Tính P(X > 10) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 4969/5000
    1. Với X ~ N(mu, sigma^2): P(a < X < b) = Phi((b - mu)/sigma) - Phi((a - mu)/sigma).
    2. Chuẩn hóa: (10 - 20)/4 = -2.5.
    3. P(X > 10) = 0.5 - Phi(-2.5) = 0.5 - (-0.4938) = 0.9938.

## Tầng 7: Tổng thể, mẫu và ước lượng điểm

35 dạng câu (30 câu viết tay, 5 bộ sinh câu); 35 chưa duyệt.

### Tổng thể và mẫu ngẫu nhiên (`xs_t7_tong_the_mau`)

- `xs_t7_tm_01` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tông môn muốn biết chiều cao trung bình của toàn bộ 3000 đệ tử. Trưởng lão chọn ngẫu nhiên 120 đệ tử, đo chiều cao và tính được trung bình 165.2 cm. Ghép mỗi đối tượng với tên gọi của nó trong thống kê.
  - **Đáp án (ghép đúng):**
    - Toàn bộ 3000 đệ tử của tông môn — Tổng thể
    - 120 đệ tử được chọn ngẫu nhiên — Mẫu
    - Chiều cao trung bình mu của cả 3000 đệ tử — Tham số: một hằng số chưa biết
    - Con số 165.2 cm tính từ 120 người được chọn — Giá trị của một thống kê
    - Số 120 — Cỡ mẫu
  - **Lời giải:**
    1. Tổng thể là toàn bộ các đối tượng cần nghiên cứu (3000 đệ tử); mẫu là phần được chọn ra để đo (120 người), số phần tử của mẫu là cỡ mẫu n = 120.
    2. Tham số là một con số của tổng thể (mu): cố định nhưng chưa biết.
    3. Thống kê là một con số tính từ mẫu; 165.2 là giá trị của trung bình mẫu với mẫu cụ thể này, chọn mẫu khác sẽ được số khác.
- `xs_t7_tm_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_n là một mẫu ngẫu nhiên từ một tổng thể có kỳ vọng mu. Trước khi lấy mẫu, trung bình mẫu X_tb = (X_1 + ... + X_n)/n là một biến ngẫu nhiên, còn mu là một hằng số (có thể chưa biết).
  - **Đáp án:** Đúng
    1. Mỗi X_i là kết quả của một lần chọn ngẫu nhiên nên là biến ngẫu nhiên; X_tb là hàm của chúng nên cũng là biến ngẫu nhiên: mỗi mẫu cho một giá trị khác.
    2. mu là một con số của cả tổng thể, không đổi theo mẫu. Mệnh đề đúng.
- `xs_t7_tm_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cần ước lượng tỷ lệ đệ tử từng luyện đan trong một tông môn có danh sách đầy đủ 3000 người. Cách chọn 100 người nào dưới đây cho một mẫu ngẫu nhiên đơn giản?
    - **(đúng)** Đánh số 3000 người rồi bốc thăm 100 số, sao cho mọi nhóm 100 người đều có cùng khả năng được chọn
    - Hỏi 100 người đầu tiên bước vào Đan phòng sáng nay
    - Hỏi 100 người tự nguyện trả lời khi được thông báo
    - Hỏi 100 người có tu vi cao nhất tông môn
  - **Đáp án:** Đánh số 3000 người rồi bốc thăm 100 số, sao cho mọi nhóm 100 người đều có cùng khả năng được chọn
    1. Mẫu ngẫu nhiên đơn giản: mỗi nhóm cùng cỡ đều có cùng khả năng được chọn, nên mẫu không thiên về phía nào.
    2. Người vào Đan phòng thì hay luyện đan hơn, người tự nguyện và người tu vi cao cũng là những nhóm riêng: ba cách đó cho mẫu bị lệch.
    3. Chỉ cách bốc thăm theo danh sách là đúng.
- `xs_t7_tm_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Lấy ngẫu nhiên 200 viên đan từ một lô rất lớn thì thấy 14 viên hỏng. Nói gì về tỷ lệ hỏng p của cả lô? Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Tổng thể là cả lô đan, mẫu là 200 viên được lấy ra.
    2. Tần suất mẫu f = 14/200 = 0.07 là một ước lượng của p.
    3. Vì mẫu được lấy ngẫu nhiên nên f đúng bằng tỷ lệ hỏng của cả lô: p = 0.07.   **<- bước sai đầu tiên**
    4. Lấy một mẫu 200 viên khác thì chắc chắn cũng được đúng 14 viên hỏng.
  - **Đáp án:** Bước 3: Vì mẫu được lấy ngẫu nhiên nên f đúng bằng tỷ lệ hỏng của cả lô: p = 0.07.
  - **Vì sao sai, và bước đúng:**
    1. f là một thống kê: nó thay đổi theo mẫu. Lấy ngẫu nhiên làm f không thiên lệch (E(f) = p), nhưng không làm f bằng p.
    2. Đúng phải nói: p được ước lượng bằng 0.07, kèm một sai số (tầng này và tầng sau học cách đo sai số đó).
- `xs_t7_tm_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một hộp có 3 thẻ ghi 1, 3, 8 (tổng thể gồm 3 số). Rút ngẫu nhiên lần lượt 2 thẻ, không hoàn lại; X_tb là trung bình hai số rút được. Tính V(X_tb). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_06`, `xs_t6_ps_07`, `xs_t7_pm_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Tổng thể có mu = (1 + 3 + 8)/3 = 4 và sigma^2 = (9 + 1 + 16)/3 = 26/3.
    2. Gọi X_1, X_2 là số trên thẻ thứ nhất, thứ hai; mỗi X_i có cùng phân phối với tổng thể, nên E(X_tb) = 4.
    3. X_1 và X_2 độc lập, nên V(X_tb) = (V(X_1) + V(X_2))/4 = sigma^2/2.   **<- bước sai đầu tiên**
    4. Vậy V(X_tb) = 13/3.
  - **Đáp án:** Bước 3: X_1 và X_2 độc lập, nên V(X_tb) = (V(X_1) + V(X_2))/4 = sigma^2/2.
  - **Vì sao sai, và bước đúng:**
    1. Rút không hoàn lại thì X_1, X_2 không độc lập: biết thẻ đầu là 8 thì thẻ sau không thể là 8. Công thức sigma^2/n chỉ đúng cho mẫu độc lập (có hoàn lại).
    2. Liệt kê: 3 cặp {1, 3}, {1, 8}, {3, 8} đồng khả năng, trung bình 2, 4.5, 5.5; kỳ vọng 4.
    3. V(X_tb) = ((2 - 4)^2 + (4.5 - 4)^2 + (5.5 - 4)^2)/3 = (4 + 0.25 + 2.25)/3 = 13/6, chỉ bằng một nửa 13/3.
- `xs_t7_tm_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tổng thể gồm 3 đệ tử có số linh thạch là 1, 2 và 6. Chọn ngẫu nhiên có hoàn lại 2 lần (mỗi lần ba người cùng khả năng, hai lần độc lập), được mẫu (X_1, X_2); X_tb = (X_1 + X_2)/2 là trung bình mẫu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_kv_01`, `xs_t6_ps_01`, `xs_t7_pm_01`
  - **Phần a** (Điền số): a) Tính trung bình tổng thể mu.
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Có bao nhiêu mẫu có thứ tự (X_1, X_2) khác nhau, mỗi mẫu cùng khả năng?
    - **Đáp án b:** 9
  - **Phần c** (Điền số): c) Tính P(X_tb > mu).
    - **Đáp án c:** 5/9
  - **Phần d** (Điền số): d) Tính V(X_tb).
    - **Đáp án d:** 7/3
  - **Lời giải:**
    1. a) mu = (1 + 2 + 6)/3 = 3.
    2. b) Mỗi lần có 3 khả năng, hai lần độc lập: 3 . 3 = 9 mẫu có thứ tự, mỗi mẫu xác suất 1/9.
    3. c) X_tb > 3 khi X_1 + X_2 > 6: các mẫu (1, 6), (6, 1), (2, 6), (6, 2), (6, 6); P = 5/9.
    4. d) sigma^2 = ((1 - 3)^2 + (2 - 3)^2 + (6 - 3)^2)/3 = 14/3; mẫu có hoàn lại nên X_1, X_2 độc lập và V(X_tb) = sigma^2/2 = 7/3.

### Trung bình mẫu và phương sai mẫu (`xs_t7_dac_trung_mau`)

- `xs_t7_dt_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian (phút) một đệ tử luyện xong một lò đan, đo 6 lần: 2, 4, 4, 5, 7, 8. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của (x_i - x_tb)^2]/(n - 1). Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 5, 24/5
    1. x_tb = (2 + 4 + 4 + 5 + 7 + 8)/6 = 30/6 = 5.
    2. Các độ lệch -3, -1, -1, 0, 2, 3; bình phương 9, 1, 1, 0, 4, 9, tổng 24.
    3. s^2 = 24/(6 - 1) = 24/5.
- `xs_t7_dt_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu gồm ba số liệu 3, 5, 7. Phương sai mẫu hiệu chỉnh (chia cho n - 1) của mẫu này là s^2 = 8/3.
  - **Đáp án:** Sai
    1. x_tb = 5; tổng bình phương độ lệch = 4 + 0 + 4 = 8.
    2. s^2 = 8/(3 - 1) = 4. Số 8/3 là phương sai chưa hiệu chỉnh (chia cho n = 3). Mệnh đề sai.
- `xs_t7_dt_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng tần số của một mẫu: giá trị 1 xuất hiện 2 lần, giá trị 2 xuất hiện 5 lần, giá trị 3 xuất hiện 3 lần. Phương sai mẫu hiệu chỉnh s^2 = [tổng của n_i (x_i - x_tb)^2]/(n - 1) bằng bao nhiêu?
    - **(đúng)** 49/90
    - 49/100
    - 49/10
    - 21/10
  - **Đáp án:** 49/90
    1. n = 2 + 5 + 3 = 10; x_tb = (1 . 2 + 2 . 5 + 3 . 3)/10 = 21/10.
    2. Tổng n_i x_i^2 = 2 + 20 + 27 = 49; tổng n_i (x_i - x_tb)^2 = 49 - 10 . (21/10)^2 = 49 - 441/10 = 49/10.
    3. s^2 = (49/10)/9 = 49/90. (49/100 là chia cho n, 49/10 là quên chia, 21/10 là x_tb.)
- `xs_t7_dt_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tính phương sai mẫu hiệu chỉnh s^2 của mẫu 1, 2, 3, 6. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. x_tb = (1 + 2 + 3 + 6)/4 = 3.
    2. Các độ lệch x_i - x_tb là -2, -1, 0, 3; bình phương lên được 4, 1, 0, 9, tổng là 14.
    3. s^2 = 14/4 = 7/2.   **<- bước sai đầu tiên**
    4. Độ lệch chuẩn mẫu s = sqrt(7/2).
  - **Đáp án:** Bước 3: s^2 = 14/4 = 7/2.
  - **Vì sao sai, và bước đúng:**
    1. Phương sai mẫu hiệu chỉnh chia cho n - 1 = 3, không chia cho n = 4.
    2. s^2 = 14/3, s = sqrt(14/3). Chia cho n cho một ước lượng hơi nhỏ hơn sigma^2 (bị chệch).
- `xs_g7_bang_tan_so` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đo một đại lượng trên một mẫu, được bảng tần số: giá trị 2 xuất hiện 4 lần; giá trị 4 xuất hiện 4 lần; giá trị 5 xuất hiện 6 lần. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của n_i (x_i - x_tb)^2]/(n - 1), với n là cỡ mẫu. Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 27/7, 152/91
    1. Cỡ mẫu n = 4 + 4 + 6 = 14.
    2. x_tb = (2 . 4 + 4 . 4 + 5 . 6)/14 = 54/14 = 27/7.
    3. Tổng n_i x_i^2 = 4 . 4 + 16 . 4 + 25 . 6 = 230.
    4. Tổng n_i (x_i - x_tb)^2 = 230 - 14 . (27/7)^2 = 152/7.
    5. s^2 = (152/7)/13 = 152/91.
  - **Câu hỏi:** Đo một đại lượng trên một mẫu, được bảng tần số: giá trị 2 xuất hiện 2 lần; giá trị 6 xuất hiện 6 lần; giá trị 7 xuất hiện 6 lần. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của n_i (x_i - x_tb)^2]/(n - 1), với n là cỡ mẫu. Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 41/7, 264/91
    1. Cỡ mẫu n = 2 + 6 + 6 = 14.
    2. x_tb = (2 . 2 + 6 . 6 + 7 . 6)/14 = 82/14 = 41/7.
    3. Tổng n_i x_i^2 = 4 . 2 + 36 . 6 + 49 . 6 = 518.
    4. Tổng n_i (x_i - x_tb)^2 = 518 - 14 . (41/7)^2 = 264/7.
    5. s^2 = (264/7)/13 = 264/91.
  - **Câu hỏi:** Đo một đại lượng trên một mẫu, được bảng tần số: giá trị 12 xuất hiện 5 lần; giá trị 16 xuất hiện 1 lần; giá trị 18 xuất hiện 5 lần. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của n_i (x_i - x_tb)^2]/(n - 1), với n là cỡ mẫu. Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 166/11, 100/11
    1. Cỡ mẫu n = 5 + 1 + 5 = 11.
    2. x_tb = (12 . 5 + 16 . 1 + 18 . 5)/11 = 166/11.
    3. Tổng n_i x_i^2 = 144 . 5 + 256 . 1 + 324 . 5 = 2596.
    4. Tổng n_i (x_i - x_tb)^2 = 2596 - 11 . (166/11)^2 = 1000/11.
    5. s^2 = (1000/11)/10 = 100/11.
- `xs_g7_phuong_sai_mau` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Số viên linh thạch một đệ tử thu được trong 5 ngày là: 2, 8, 3, 15, 14. Coi đây là một mẫu cỡ n = 5. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của (x_i - x_tb)^2]/(n - 1). Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 42/5, 363/10
    1. x_tb = (2 + 8 + 3 + 15 + 14)/5 = 42/5.
    2. Tổng các x_i^2 = 4 + 64 + 9 + 225 + 196 = 498.
    3. Tổng của (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2 = 498 - 5 . (42/5)^2 = 726/5.
    4. s^2 = (726/5)/4 = 363/10 (chia cho n - 1, không chia cho n).
  - **Câu hỏi:** Số viên linh thạch một đệ tử thu được trong 4 ngày là: 2, 2, 11, 5. Coi đây là một mẫu cỡ n = 4. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của (x_i - x_tb)^2]/(n - 1). Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 5, 18
    1. x_tb = (2 + 2 + 11 + 5)/4 = 20/4 = 5.
    2. Tổng các x_i^2 = 4 + 4 + 121 + 25 = 154.
    3. Tổng của (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2 = 154 - 4 . 5^2 = 54.
    4. s^2 = 54/3 = 18 (chia cho n - 1, không chia cho n).
  - **Câu hỏi:** Số viên linh thạch một đệ tử thu được trong 5 ngày là: 4, 11, 15, 2, 0. Coi đây là một mẫu cỡ n = 5. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh s^2 = [tổng của (x_i - x_tb)^2]/(n - 1). Nhập hai số theo thứ tự x_tb, s^2.
  - **Đáp án:** 32/5, 403/10
    1. x_tb = (4 + 11 + 15 + 2 + 0)/5 = 32/5.
    2. Tổng các x_i^2 = 16 + 121 + 225 + 4 + 0 = 366.
    3. Tổng của (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2 = 366 - 5 . (32/5)^2 = 806/5.
    4. s^2 = (806/5)/4 = 403/10 (chia cho n - 1, không chia cho n).
- `xs_t7_dt_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian (phút) 9 đệ tử hoàn thành một bài luyện được ghi thành bảng tần số: 15 phút có 4 người, 20 phút có 1 người, 25 phút có 4 người.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_03`, `xs_t6_ps_04`
  - **Phần a** (Điền số): a) Tính trung bình mẫu x_tb.
    - **Đáp án a:** 20
  - **Phần b** (Điền số): b) Tính phương sai mẫu hiệu chỉnh s^2 (chia cho n - 1).
    - **Đáp án b:** 25
  - **Phần c** (Điền số): c) Tính độ lệch chuẩn mẫu hiệu chỉnh s.
    - **Đáp án c:** 5
  - **Phần d** (Trắc nghiệm): d) Nếu mỗi người được tính thêm 3 phút chuẩn bị (mọi số liệu cộng thêm 3) thì x_tb và s^2 thay đổi thế nào?
    - **(đúng)** x_tb tăng 3, s^2 không đổi
    - Cả x_tb và s^2 cùng tăng 3
    - x_tb tăng 3, s^2 tăng 9
    - x_tb không đổi, s^2 tăng 3
    - **Đáp án d:** x_tb tăng 3, s^2 không đổi
  - **Lời giải:**
    1. a) x_tb = (15 . 4 + 20 . 1 + 25 . 4)/9 = 180/9 = 20.
    2. b) Tổng n_i (x_i - x_tb)^2 = 4 . 25 + 1 . 0 + 4 . 25 = 200; s^2 = 200/8 = 25.
    3. c) s = sqrt(25) = 5.
    4. d) Cộng 3 vào mọi số liệu thì x_tb cũng tăng 3, còn mọi độ lệch x_i - x_tb giữ nguyên, nên s^2 không đổi.
- `xs_t7_dt_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chứng minh công thức tính nhanh s^2 = (tổng x_i^2 - n x_tb^2)/(n - 1) cho phương sai mẫu hiệu chỉnh, với x_tb = (x_1 + ... + x_n)/n. Sắp xếp các bước.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_04`, `xs_t7_dt_01`
  - **Đáp án (thứ tự đúng):**
    1. Khai triển từng số hạng: (x_i - x_tb)^2 = x_i^2 - 2 x_tb x_i + x_tb^2.
    2. Cộng theo i từ 1 đến n: tổng (x_i - x_tb)^2 = tổng x_i^2 - 2 x_tb (tổng x_i) + n x_tb^2.
    3. Thay tổng x_i = n x_tb: vế phải bằng tổng x_i^2 - 2n x_tb^2 + n x_tb^2.
    4. Rút gọn: tổng (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2.
    5. Chia hai vế cho n - 1: s^2 = (tổng x_i^2 - n x_tb^2)/(n - 1).
  - **Lời giải:**
    1. Khai triển bình phương, cộng lại, dùng định nghĩa x_tb để thay tổng x_i, rút gọn, rồi chia cho n - 1.
    2. Ví dụ mẫu 2, 4, 4, 5, 7, 8: tổng x_i^2 = 174, n x_tb^2 = 150, hiệu 24, s^2 = 24/5.

### Phân phối của trung bình mẫu (`xs_t7_phan_phoi_mau`)

- `xs_t7_pm_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tổng thể có kỳ vọng mu = 50 và độ lệch chuẩn sigma = 12. Lấy mẫu ngẫu nhiên cỡ n = 36 (các lần lấy độc lập). Tính kỳ vọng và độ lệch chuẩn của trung bình mẫu X_tb. Nhập hai số theo thứ tự E(X_tb), độ lệch chuẩn của X_tb.
  - **Đáp án:** 50, 2
    1. E(X_tb) = (E(X_1) + ... + E(X_n))/n = mu = 50.
    2. Các X_i độc lập nên V(X_tb) = n sigma^2/n^2 = sigma^2/n = 144/36 = 4.
    3. Độ lệch chuẩn của X_tb = sigma/sqrt(n) = 12/6 = 2.
- `xs_t7_pm_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lấy mẫu ngẫu nhiên (các quan sát độc lập) từ một tổng thể có độ lệch chuẩn sigma > 0. Khi tăng cỡ mẫu từ 25 lên 100, độ lệch chuẩn của trung bình mẫu giảm còn một nửa.
  - **Đáp án:** Đúng
    1. Độ lệch chuẩn của X_tb là sigma/sqrt(n).
    2. n = 25 cho sigma/5, n = 100 cho sigma/10: đúng một nửa. Muốn giảm một nửa phải tăng cỡ mẫu gấp 4. Mệnh đề đúng.
- `xs_t7_pm_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tổng thể có phân phối chuẩn N(100, 36) (kỳ vọng 100, phương sai 36). Lấy mẫu ngẫu nhiên cỡ n = 9. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2) = 0.4772. P(X_tb > 104) bằng bao nhiêu?
    - **(đúng)** 0.0228
    - 0.4772
    - 0.9772
    - 0.0456
  - **Đáp án:** 0.0228
    1. X_tb có phân phối chuẩn với kỳ vọng 100 và độ lệch chuẩn 6/sqrt(9) = 2.
    2. Chuẩn hóa: (104 - 100)/2 = 2.
    3. P(X_tb > 104) = 0.5 - Phi(2) = 0.5 - 0.4772 = 0.0228.
- `xs_t7_pm_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Khối lượng (g) một gói linh trà có phân phối chuẩn với kỳ vọng 500 và độ lệch chuẩn 16. Lấy ngẫu nhiên 16 gói, X_tb là khối lượng trung bình. Dùng Phi(0.5) = 0.1915 và Phi(2) = 0.4772 (Phi là hàm Laplace), tính P(X_tb < 492). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. X_tb có phân phối chuẩn với kỳ vọng 500.
    2. Chuẩn hóa mốc 492 bằng độ lệch chuẩn của một gói: (492 - 500)/16 = -0.5.   **<- bước sai đầu tiên**
    3. P(X_tb < 492) = 0.5 + Phi(-0.5) = 0.5 - 0.1915 = 0.3085.
  - **Đáp án:** Bước 2: Chuẩn hóa mốc 492 bằng độ lệch chuẩn của một gói: (492 - 500)/16 = -0.5.
  - **Vì sao sai, và bước đúng:**
    1. X_tb phân tán ít hơn một gói: độ lệch chuẩn của X_tb là sigma/sqrt(n) = 16/4 = 4, không phải 16.
    2. Chuẩn hóa đúng: (492 - 500)/4 = -2, nên P(X_tb < 492) = 0.5 - Phi(2) = 0.0228.
- `xs_g7_trung_binh_mau_chuan` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tổng thể có phân phối chuẩn với kỳ vọng mu = 500 và độ lệch chuẩn sigma = 20. Lấy một mẫu ngẫu nhiên cỡ n = 16 và gọi X_tb là trung bình mẫu. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(0.5) = 0.1915, Phi(1.5) = 0.4332. Tính P(492.5 < X_tb < 502.5) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 6247/10000
    1. X_tb có phân phối chuẩn với kỳ vọng 500 và độ lệch chuẩn sigma/sqrt(n) = 20/4 = 5.
    2. Chuẩn hóa: (492.5 - 500)/5 = -1.5 và (502.5 - 500)/5 = 0.5.
    3. P(492.5 < X_tb < 502.5) = Phi(0.5) - Phi(-1.5) = 0.1915 + 0.4332 = 0.6247.
  - **Câu hỏi:** Tổng thể có phân phối chuẩn với kỳ vọng mu = 20 và độ lệch chuẩn sigma = 2. Lấy một mẫu ngẫu nhiên cỡ n = 4 và gọi X_tb là trung bình mẫu. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1) = 0.3413. Tính P(X_tb > 19) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 8413/10000
    1. X_tb có phân phối chuẩn với kỳ vọng 20 và độ lệch chuẩn sigma/sqrt(n) = 2/2 = 1.
    2. Chuẩn hóa: (19 - 20)/1 = -1.
    3. P(X_tb > 19) = 0.5 - Phi(-1) = 0.5 - (-0.3413) = 0.8413.
  - **Câu hỏi:** Tổng thể có phân phối chuẩn với kỳ vọng mu = 120 và độ lệch chuẩn sigma = 25. Lấy một mẫu ngẫu nhiên cỡ n = 25 và gọi X_tb là trung bình mẫu. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1.5) = 0.4332, Phi(2.5) = 0.4938. Tính P(112.5 < X_tb < 132.5) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 927/1000
    1. X_tb có phân phối chuẩn với kỳ vọng 120 và độ lệch chuẩn sigma/sqrt(n) = 25/5 = 5.
    2. Chuẩn hóa: (112.5 - 120)/5 = -1.5 và (132.5 - 120)/5 = 2.5.
    3. P(112.5 < X_tb < 132.5) = Phi(2.5) - Phi(-1.5) = 0.4938 + 0.4332 = 0.9270.
- `xs_t7_pm_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tuổi thọ (giờ) của một loại đèn linh hỏa có kỳ vọng 400 và độ lệch chuẩn 40 (không biết phân phối). Lấy ngẫu nhiên n = 64 đèn, các đèn độc lập; với cỡ mẫu lớn như vậy, coi trung bình mẫu X_tb có phân phối xấp xỉ chuẩn. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2) = 0.4772.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_01`, `xs_t7_pm_03`, `xs_t6_ch_04`
  - **Phần a** (Điền số): a) Tính E(X_tb).
    - **Đáp án a:** 400
  - **Phần b** (Điền số): b) Tính độ lệch chuẩn của X_tb.
    - **Đáp án b:** 5
  - **Phần c** (Điền số): c) Tính xấp xỉ P(390 < X_tb < 410) (số thập phân đúng, không làm tròn thêm).
    - **Đáp án c:** 1193/1250
  - **Phần d** (Điền số): d) Cỡ mẫu n nhỏ nhất bằng bao nhiêu để độ lệch chuẩn của X_tb không vượt quá 2?
    - **Đáp án d:** 400
  - **Lời giải:**
    1. a) E(X_tb) = mu = 400.
    2. b) sigma/sqrt(n) = 40/8 = 5.
    3. c) Chuẩn hóa 390 và 410 thành -2 và 2: P = Phi(2) - Phi(-2) = 2 . 0.4772 = 0.9544.
    4. d) 40/sqrt(n) <= 2 khi sqrt(n) >= 20, tức n >= 400; n nhỏ nhất là 400.
- `xs_t7_pm_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tổng thể có kỳ vọng mu = 20 và phương sai sigma^2 = 36. X_1, ..., X_9 là mẫu ngẫu nhiên (độc lập, cùng phân phối với tổng thể), S = X_1 + ... + X_9 và X_tb = S/9. Ghép mỗi đại lượng với giá trị của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_04`, `xs_t7_pm_01`, `xs_t7_pm_02`
  - **Đáp án (ghép đúng):**
    - E(X_tb) — 20
    - V(X_tb) — 4
    - E(S) — 180
    - V(S) — 324
    - E(X_tb^2) — 404
  - **Lời giải:**
    1. E(S) = 9 . 20 = 180 và E(X_tb) = 180/9 = 20.
    2. Các X_i độc lập: V(S) = 9 . 36 = 324, V(X_tb) = V(S)/81 = 4.
    3. E(X_tb^2) = V(X_tb) + (E(X_tb))^2 = 4 + 400 = 404.

### Ước lượng điểm không chệch (`xs_t7_uoc_luong_diem`)

- `xs_t7_ud_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_n (n >= 2) là mẫu ngẫu nhiên từ tổng thể có phương sai sigma^2 > 0. Phương sai mẫu chưa hiệu chỉnh [tổng của (X_i - X_tb)^2]/n là một ước lượng không chệch của sigma^2.
  - **Đáp án:** Sai
    1. E(tổng của (X_i - X_tb)^2) = (n - 1) sigma^2, nên chia cho n được kỳ vọng (n - 1) sigma^2/n, nhỏ hơn sigma^2.
    2. Ước lượng này bị chệch; chia cho n - 1 (phương sai mẫu hiệu chỉnh s^2) mới không chệch. Mệnh đề sai.
- `xs_t7_ud_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, X_2, X_3 là mẫu ngẫu nhiên từ tổng thể có kỳ vọng mu chưa biết. Thống kê nào dưới đây là ước lượng không chệch của mu (E(T) = mu với mọi mu)?
    - **(đúng)** (X_1 + 2X_2 + X_3)/4
    - (X_1 + X_2 + X_3)/4
    - (2X_1 + X_2)/2
    - X_1 - X_2 + X_3/2
  - **Đáp án:** (X_1 + 2X_2 + X_3)/4
    1. E(c_1 X_1 + c_2 X_2 + c_3 X_3) = (c_1 + c_2 + c_3) mu: không chệch khi tổng các hệ số bằng 1.
    2. Tổng hệ số: 1/4 + 2/4 + 1/4 = 1; 3/4; 3/2; 1 - 1 + 1/2 = 1/2. Chỉ thống kê đầu không chệch.
- `xs_t7_ud_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tổng thể có phương sai sigma^2 = 10. Với mẫu ngẫu nhiên cỡ n = 5, gọi S_n^2 = [tổng của (X_i - X_tb)^2]/5 là phương sai mẫu chưa hiệu chỉnh. Tính E(S_n^2).
  - **Đáp án:** 8
    1. Phương sai mẫu hiệu chỉnh s^2 = [tổng của (X_i - X_tb)^2]/4 có E(s^2) = sigma^2 = 10.
    2. S_n^2 = (4/5) s^2, nên E(S_n^2) = (4/5) . 10 = 8: thấp hơn sigma^2, tức bị chệch.
- `xs_t7_ud_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X_1, X_2, X_3, X_4 là mẫu ngẫu nhiên từ tổng thể có kỳ vọng mu. Tìm hằng số a để T = a(X_1 + X_2 + X_3) + X_4/4 là ước lượng không chệch của mu. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. T không chệch nghĩa là E(T) = mu với mọi mu.
    2. Theo tính tuyến tính, E(T) = a(E(X_1) + E(X_2) + E(X_3)) + E(X_4)/4.
    3. Thay E(X_i) = mu: E(T) = a mu + mu/4.   **<- bước sai đầu tiên**
    4. a mu + mu/4 = mu với mọi mu khi a = 3/4.
  - **Đáp án:** Bước 3: Thay E(X_i) = mu: E(T) = a mu + mu/4.
  - **Vì sao sai, và bước đúng:**
    1. Trong ngoặc có ba số hạng, mỗi số hạng bằng mu: E(T) = 3a mu + mu/4.
    2. 3a + 1/4 = 1 cho a = 1/4 (lúc đó T chính là trung bình mẫu).
- `xs_g7_khong_chech_tf` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_3 là một mẫu ngẫu nhiên (độc lập, cùng phân phối) từ một tổng thể có kỳ vọng mu chưa biết. Thống kê T = (2/5)X_1 + (2/5)X_2 + (7/10)X_3 là một ước lượng không chệch của mu (tức E(T) = mu với mọi giá trị của mu).
  - **Đáp án:** Sai
    1. Kỳ vọng tuyến tính và E(X_i) = mu với mọi i, nên E(T) = (tổng các hệ số) . mu.
    2. Tổng các hệ số = (2/5) + (2/5) + (7/10) = 3/2.
    3. Tổng khác 1 nên E(T) = 3/2 mu khác mu (khi mu khác 0): T bị chệch. Mệnh đề sai.
  - **Câu hỏi:** X_1, ..., X_3 là một mẫu ngẫu nhiên (độc lập, cùng phân phối) từ một tổng thể có kỳ vọng mu chưa biết. Thống kê T = (2/3)X_1 + (1/4)X_2 + (1/12)X_3 là một ước lượng không chệch của mu (tức E(T) = mu với mọi giá trị của mu).
  - **Đáp án:** Đúng
    1. Kỳ vọng tuyến tính và E(X_i) = mu với mọi i, nên E(T) = (tổng các hệ số) . mu.
    2. Tổng các hệ số = (2/3) + (1/4) + (1/12) = 1.
    3. Tổng bằng 1 nên E(T) = mu với mọi mu: T không chệch. Mệnh đề đúng.
  - **Câu hỏi:** X_1, ..., X_3 là một mẫu ngẫu nhiên (độc lập, cùng phân phối) từ một tổng thể có kỳ vọng mu chưa biết. Thống kê T = (1/4)X_1 + (2/3)X_2 + (1/4)X_3 là một ước lượng không chệch của mu (tức E(T) = mu với mọi giá trị của mu).
  - **Đáp án:** Sai
    1. Kỳ vọng tuyến tính và E(X_i) = mu với mọi i, nên E(T) = (tổng các hệ số) . mu.
    2. Tổng các hệ số = (1/4) + (2/3) + (1/4) = 7/6.
    3. Tổng khác 1 nên E(T) = 7/6 mu khác mu (khi mu khác 0): T bị chệch. Mệnh đề sai.
- `xs_t7_ud_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_n là mẫu ngẫu nhiên từ tổng thể có kỳ vọng mu và phương sai sigma^2; s^2 = [tổng của (X_i - X_tb)^2]/(n - 1). Sắp xếp các bước chứng minh E(s^2) = sigma^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_ud_03`, `xs_t6_ps_04`, `xs_t7_pm_01`
  - **Đáp án (thứ tự đúng):**
    1. Viết tổng của (X_i - X_tb)^2 = tổng của X_i^2 - n X_tb^2.
    2. Với mỗi i: E(X_i^2) = V(X_i) + (E(X_i))^2 = sigma^2 + mu^2.
    3. Tương tự cho trung bình mẫu: E(X_tb^2) = V(X_tb) + (E(X_tb))^2 = sigma^2/n + mu^2.
    4. Lấy kỳ vọng hai vế ở bước đầu: E(tổng của (X_i - X_tb)^2) = n(sigma^2 + mu^2) - n(sigma^2/n + mu^2) = (n - 1) sigma^2.
    5. Chia cho n - 1: E(s^2) = sigma^2, nên s^2 là ước lượng không chệch của sigma^2.
  - **Lời giải:**
    1. Dùng công thức tính nhanh, rồi V(Y) = E(Y^2) - (E(Y))^2 cho X_i và cho X_tb (với V(X_tb) = sigma^2/n).
    2. Hiệu hai kỳ vọng còn (n - 1) sigma^2: đó là lý do chia cho n - 1.
- `xs_t7_ud_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, X_2, X_3 là mẫu ngẫu nhiên (độc lập) từ tổng thể có kỳ vọng mu chưa biết và phương sai sigma^2 = 8. Xét hai ước lượng của mu: T_1 = (X_1 + X_2 + X_3)/3 và T_2 = (X_1 + 2X_2 + X_3)/4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_ud_02`, `xs_t6_ps_07`, `xs_g7_khong_chech_tf`
  - **Phần a** (Đúng/Sai): a) T_2 là ước lượng không chệch của mu.
    - **Đáp án a:** Đúng
  - **Phần b** (Điền số): b) Tính V(T_1).
    - **Đáp án b:** 8/3
  - **Phần c** (Điền số): c) Tính V(T_2).
    - **Đáp án c:** 3
  - **Phần d** (Trắc nghiệm): d) Trong hai ước lượng không chệch này, ước lượng nào tốt hơn (hiệu quả hơn)?
    - **(đúng)** T_1, vì có phương sai nhỏ hơn
    - T_2, vì có phương sai lớn hơn
    - T_2, vì đặt trọng số lớn hơn cho X_2
    - Hai ước lượng tốt như nhau vì cùng không chệch
    - **Đáp án d:** T_1, vì có phương sai nhỏ hơn
  - **Lời giải:**
    1. a) E(T_2) = (1 + 2 + 1) mu/4 = mu: không chệch.
    2. b) V(T_1) = 3 . 8/9 = 8/3.
    3. c) V(T_2) = (1 + 4 + 1) . 8/16 = 3 (các X_i độc lập, hệ số được bình phương).
    4. d) Cùng không chệch thì ước lượng có phương sai nhỏ hơn sẽ dao động ít hơn quanh mu: 8/3 < 3, nên T_1 tốt hơn.

### Ước lượng hợp lý cực đại (`xs_t7_hop_ly_cuc_dai`)

- `xs_t7_hl_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lò đan cho ra viên đan tốt với xác suất p chưa biết (0 < p < 1), các lần luyện độc lập. Đệ tử luyện cho đến khi được viên tốt đầu tiên rồi ghi lại số lần luyện X, nên P(X = k) = p(1 - p)^(k - 1) với k = 1, 2, 3, ... Làm 5 đợt, được X = 3, 1, 4, 2, 5. Tìm ước lượng hợp lý cực đại p* của p.
  - **Đáp án:** 1/3
    1. L(p) = tích của p(1 - p)^(x_i - 1) = p^5 (1 - p)^(15 - 5), vì tổng x_i = 15.
    2. ln L = 5 ln p + 10 ln(1 - p); đạo hàm 5/p - 10/(1 - p) = 0 cho 5(1 - p) = 10p.
    3. p* = 5/15 = 1/3 (bằng 1/x_tb).
- `xs_t7_hl_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian chờ (phút) có phân phối mũ với mật độ lambda e^(-lambda x) khi x > 0, lambda > 0 chưa biết. Một mẫu cho các giá trị 2, 3, 5, 6. Ước lượng hợp lý cực đại của lambda là
    - **(đúng)** 1/4
    - 4
    - 16
    - 1/16
  - **Đáp án:** 1/4
    1. ln L(lambda) = n ln lambda - lambda (tổng x_i) với n = 4, tổng x_i = 16.
    2. Đạo hàm 4/lambda - 16 = 0 cho lambda* = 4/16 = 1/4, tức 1/x_tb (x_tb = 4 là thời gian chờ trung bình).
- `xs_t7_hl_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong n phép thử Bernoulli độc lập có k lần thành công, với 0 < k < n. Hàm hợp lý L(p) = p^k (1 - p)^(n - k) đạt giá trị lớn nhất trên khoảng (0, 1) tại p = k/n.
  - **Đáp án:** Đúng
    1. ln L = k ln p + (n - k) ln(1 - p); đạo hàm k/p - (n - k)/(1 - p) = 0 cho p = k/n.
    2. Đạo hàm cấp hai -k/p^2 - (n - k)/(1 - p)^2 < 0 nên đó là điểm lớn nhất. Mệnh đề đúng.
- `xs_t7_hl_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tìm ước lượng hợp lý cực đại của tham số lambda của phân phối Poisson (P(X = k) = e^(-lambda) lambda^k / k!) từ mẫu x_1, ..., x_n không phải tất cả bằng 0. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. L(lambda) = tích của e^(-lambda) lambda^(x_i)/x_i! = e^(-n lambda) lambda^(x_1 + ... + x_n)/(x_1! ... x_n!).
    2. ln L(lambda) = -n lambda + (x_1 + ... + x_n) ln lambda - ln(x_1! ... x_n!).
    3. Đạo hàm theo lambda: (ln L)' = -n + (x_1 + ... + x_n) lambda.   **<- bước sai đầu tiên**
    4. Cho đạo hàm bằng 0: lambda* = n/(x_1 + ... + x_n).
  - **Đáp án:** Bước 3: Đạo hàm theo lambda: (ln L)' = -n + (x_1 + ... + x_n) lambda.
  - **Vì sao sai, và bước đúng:**
    1. Đạo hàm của ln lambda là 1/lambda: (ln L)' = -n + (x_1 + ... + x_n)/lambda.
    2. Cho bằng 0: lambda* = (x_1 + ... + x_n)/n = x_tb, hợp lý vì E(X) = lambda.
- `xs_g7_hop_ly` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong một tổng thể, X có phân phối Poisson: P(X = k) = e^(-lambda) lambda^k / k! với k = 0, 1, 2, ..., tham số lambda > 0 chưa biết. Một mẫu ngẫu nhiên cỡ n = 5 cho các giá trị: 2, 0, 3, 6, 3. Tìm ước lượng hợp lý cực đại lambda* của lambda (nhập một số hoặc phân số tối giản).
  - **Đáp án:** 14/5
    1. Hàm hợp lý L(lambda) là tích các xác suất (hay mật độ) tại 5 giá trị của mẫu; lấy logarit để tích thành tổng.
    2. ln L(lambda) = -n lambda + (tổng x_i) ln lambda - ln(x_1! ... x_n!).
    3. (ln L)'(lambda) = -n + (tổng x_i)/lambda = 0 cho lambda = x_tb.
    4. lambda* = 14/5 = 14/5.
  - **Câu hỏi:** Trong một tổng thể, X có phân phối Bernoulli: P(X = 1) = p, P(X = 0) = 1 - p, với 0 < p < 1 chưa biết (X = 1 là một lần thành công). Một mẫu ngẫu nhiên cỡ n = 6 cho các giá trị: 0, 1, 0, 1, 1, 0. Tìm ước lượng hợp lý cực đại p* của p (nhập một số hoặc phân số tối giản).
  - **Đáp án:** 1/2
    1. Hàm hợp lý L(p) là tích các xác suất (hay mật độ) tại 6 giá trị của mẫu; lấy logarit để tích thành tổng.
    2. ln L(p) = k ln p + (n - k) ln(1 - p), với k = 3 lần thành công trong n = 6 lần.
    3. (ln L)'(p) = k/p - (n - k)/(1 - p) = 0 cho p = k/n.
    4. p* = 3/6 = 1/2.
  - **Câu hỏi:** Trong một tổng thể, X có phân phối Poisson: P(X = k) = e^(-lambda) lambda^k / k! với k = 0, 1, 2, ..., tham số lambda > 0 chưa biết. Một mẫu ngẫu nhiên cỡ n = 6 cho các giá trị: 2, 4, 3, 5, 4, 0. Tìm ước lượng hợp lý cực đại lambda* của lambda (nhập một số hoặc phân số tối giản).
  - **Đáp án:** 3
    1. Hàm hợp lý L(lambda) là tích các xác suất (hay mật độ) tại 6 giá trị của mẫu; lấy logarit để tích thành tổng.
    2. ln L(lambda) = -n lambda + (tổng x_i) ln lambda - ln(x_1! ... x_n!).
    3. (ln L)'(lambda) = -n + (tổng x_i)/lambda = 0 cho lambda = x_tb.
    4. lambda* = 18/6 = 3.
- `xs_t7_hl_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian chờ có phân phối mũ với mật độ lambda e^(-lambda x) khi x > 0 (lambda > 0 chưa biết). Từ mẫu x_1, ..., x_n (các x_i > 0), sắp xếp các bước tìm ước lượng hợp lý cực đại của lambda.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_hl_02`, `xs_t7_hl_04`
  - **Đáp án (thứ tự đúng):**
    1. Hàm hợp lý: L(lambda) = tích của lambda e^(-lambda x_i) = lambda^n e^(-lambda (x_1 + ... + x_n)).
    2. Lấy logarit: ln L(lambda) = n ln lambda - lambda (x_1 + ... + x_n).
    3. Đạo hàm: (ln L)'(lambda) = n/lambda - (x_1 + ... + x_n).
    4. Đạo hàm bằng 0 khi lambda = n/(x_1 + ... + x_n) = 1/x_tb.
    5. (ln L)''(lambda) = -n/lambda^2 < 0 nên đó là điểm cực đại: lambda* = 1/x_tb.
  - **Lời giải:**
    1. Lập L, lấy logarit để tích thành tổng, đạo hàm, giải phương trình, rồi kiểm tra đạo hàm cấp hai.
    2. Kết quả hợp lý: E(X) = 1/lambda, nên lambda được ước lượng bằng 1/x_tb.
- `xs_t7_hl_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi đệ tử thử một chiêu hai lần, mỗi lần thành công với xác suất theta (0 < theta < 1) chưa biết, các lần độc lập; X là số lần thành công, nên P(X = 0) = (1 - theta)^2, P(X = 1) = 2theta(1 - theta), P(X = 2) = theta^2. Với 10 đệ tử: 4 người được X = 0, 4 người được X = 1, 2 người được X = 2. Hàm hợp lý có dạng L(theta) = C theta^a (1 - theta)^b, C là một hằng số dương.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_bn_05`, `xs_t7_hl_03`, `xs_t7_hl_01`
  - **Phần a** (Điền số): a) Tìm số mũ a.
    - **Đáp án a:** 8
  - **Phần b** (Điền số): b) Tìm số mũ b.
    - **Đáp án b:** 12
  - **Phần c** (Điền số): c) Tìm ước lượng hợp lý cực đại theta*.
    - **Đáp án c:** 2/5
  - **Phần d** (Đúng/Sai): d) theta* bằng một nửa trung bình mẫu x_tb của 10 giá trị X.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) theta xuất hiện 1 lần trong mỗi P(X = 1) và 2 lần trong mỗi P(X = 2): a = 4 . 1 + 2 . 2 = 8.
    2. b) (1 - theta) xuất hiện 2 lần trong mỗi P(X = 0) và 1 lần trong mỗi P(X = 1): b = 4 . 2 + 4 . 1 = 12.
    3. c) ln L = ln C + 8 ln theta + 12 ln(1 - theta); đạo hàm 8/theta - 12/(1 - theta) = 0 cho theta* = 8/20 = 2/5.
    4. d) x_tb = (0 . 4 + 1 . 4 + 2 . 2)/10 = 4/5, một nửa là 2/5 = theta*. Đúng (E(X) = 2 theta).

## Tầng 8: Khoảng tin cậy, luật số lớn và định lý giới hạn trung tâm

35 dạng câu (29 câu viết tay, 6 bộ sinh câu); 35 chưa duyệt.

### Khoảng tin cậy cho trung bình (`xs_t8_tin_cay_trung_binh`)

- `xs_t8_tc_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khối lượng (g) một viên linh đan có phân phối chuẩn với độ lệch chuẩn sigma = 10 đã biết. Cân 25 viên được trung bình mẫu x_tb = 48. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho khối lượng trung bình mu, dùng z = 1.96 (Phi(1.96) = 0.475). Nhập hai đầu mút, đầu nhỏ trước.
  - **Đáp án:** 1102/25, 1298/25
    1. Biết sigma: khoảng (x_tb - epsilon; x_tb + epsilon) với epsilon = z sigma/sqrt(n).
    2. sigma/sqrt(n) = 10/5 = 2; epsilon = 1.96 . 2 = 3.92.
    3. Khoảng tin cậy: (48 - 3.92; 48 + 3.92) = (44.08; 51.92).
- `xs_t8_tc_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một mẫu cỡ n = 16 lấy từ tổng thể có phân phối chuẩn, phương sai chưa biết, cho x_tb và độ lệch chuẩn mẫu hiệu chỉnh s. Để lập khoảng tin cậy đối xứng 95% cho mu, ta dùng epsilon = c . s/sqrt(n). Hằng số c là giá trị nào? (t(k; a) là số mà P(T > t(k; a)) = a với T có phân phối Student k bậc tự do.)
    - **(đúng)** t(15; 0.025) = 2.131
    - t(16; 0.025) = 2.120
    - z = 1.96
    - t(15; 0.05) = 1.753
  - **Đáp án:** t(15; 0.025) = 2.131
    1. Chưa biết sigma và thay bằng s: (X_tb - mu)/(s/sqrt(n)) có phân phối Student n - 1 = 15 bậc tự do (không phải 16).
    2. Khoảng đối xứng 95% để lại 5% chia đều hai phía, mỗi phía 0.025: c = t(15; 0.025) = 2.131.
    3. z = 1.96 chỉ dùng khi biết sigma (hoặc mẫu rất lớn); t(15; 0.05) là giá trị một phía.
- `xs_t8_tc_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ một mẫu, khoảng tin cậy 95% cho kỳ vọng mu tính được là (44.08; 51.92). Điều đó có nghĩa là khoảng 95% số liệu trong mẫu nằm trong khoảng (44.08; 51.92).
  - **Đáp án:** Sai
    1. Khoảng tin cậy nói về tham số mu, không nói về từng số liệu: nếu lặp lại việc lấy mẫu rất nhiều lần, khoảng 95% các khoảng lập được sẽ chứa mu.
    2. Số liệu riêng lẻ phân tán rộng hơn nhiều (độ lệch chuẩn sigma, còn khoảng tin cậy co lại theo sigma/sqrt(n)). Mệnh đề sai.
- `xs_g8_khoang_biet_sigma` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 20 đã biết. Một mẫu cỡ n = 25 có trung bình mẫu x_tb = 176.4. Lập khoảng tin cậy đối xứng độ tin cậy 90% cho kỳ vọng mu, dùng z = 1.645 (Phi(1.645) = 0.45). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 8491/50, 9149/50
    1. Biết sigma: khoảng tin cậy (x_tb - epsilon; x_tb + epsilon) với epsilon = z sigma/sqrt(n).
    2. sigma/sqrt(n) = 20/5 = 4; epsilon = 1.645 . 4 = 6.58.
    3. Khoảng tin cậy: (176.4 - 6.58; 176.4 + 6.58) = (169.82; 182.98).
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 1.5 đã biết. Một mẫu cỡ n = 9 có trung bình mẫu x_tb = 37.3. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho kỳ vọng mu, dùng z = 1.96 (Phi(1.96) = 0.475). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 908/25, 957/25
    1. Biết sigma: khoảng tin cậy (x_tb - epsilon; x_tb + epsilon) với epsilon = z sigma/sqrt(n).
    2. sigma/sqrt(n) = 1.5/3 = 0.5; epsilon = 1.96 . 0.5 = 0.98.
    3. Khoảng tin cậy: (37.3 - 0.98; 37.3 + 0.98) = (36.32; 38.28).
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 24 đã biết. Một mẫu cỡ n = 36 có trung bình mẫu x_tb = 131.4. Lập khoảng tin cậy đối xứng độ tin cậy 90% cho kỳ vọng mu, dùng z = 1.645 (Phi(1.645) = 0.45). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 6241/50, 6899/50
    1. Biết sigma: khoảng tin cậy (x_tb - epsilon; x_tb + epsilon) với epsilon = z sigma/sqrt(n).
    2. sigma/sqrt(n) = 24/6 = 4; epsilon = 1.645 . 4 = 6.58.
    3. Khoảng tin cậy: (131.4 - 6.58; 131.4 + 6.58) = (124.82; 137.98).
- `xs_g8_khoang_t` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Một mẫu cỡ n = 9 có trung bình mẫu x_tb = 88.2 và độ lệch chuẩn mẫu hiệu chỉnh s = 9. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho kỳ vọng mu, dùng giá trị tới hạn Student t(8; 0.025) = 2.306 (tức P(T > 2.306) = 0.025 với T có phân phối Student 8 bậc tự do). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 40641/500, 47559/500
    1. Chưa biết sigma, mẫu nhỏ: dùng phân phối Student n - 1 = 8 bậc tự do, mức (1 - 95%)/2 = 0.025 mỗi phía.
    2. s/sqrt(n) = 9/3 = 3; epsilon = 2.306 . 3 = 6.918.
    3. Khoảng tin cậy: (81.282; 95.118).
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Một mẫu cỡ n = 4 có trung bình mẫu x_tb = 18.6 và độ lệch chuẩn mẫu hiệu chỉnh s = 1. Lập khoảng tin cậy đối xứng độ tin cậy 90% cho kỳ vọng mu, dùng giá trị tới hạn Student t(3; 0.05) = 2.353 (tức P(T > 2.353) = 0.05 với T có phân phối Student 3 bậc tự do). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 34847/2000, 39553/2000
    1. Chưa biết sigma, mẫu nhỏ: dùng phân phối Student n - 1 = 3 bậc tự do, mức (1 - 90%)/2 = 0.05 mỗi phía.
    2. s/sqrt(n) = 1/2 = 0.5; epsilon = 2.353 . 0.5 = 1.1765.
    3. Khoảng tin cậy: (17.4235; 19.7765).
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Một mẫu cỡ n = 9 có trung bình mẫu x_tb = 65.7 và độ lệch chuẩn mẫu hiệu chỉnh s = 9. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho kỳ vọng mu, dùng giá trị tới hạn Student t(8; 0.025) = 2.306 (tức P(T > 2.306) = 0.025 với T có phân phối Student 8 bậc tự do). Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 29391/500, 36309/500
    1. Chưa biết sigma, mẫu nhỏ: dùng phân phối Student n - 1 = 8 bậc tự do, mức (1 - 95%)/2 = 0.025 mỗi phía.
    2. s/sqrt(n) = 9/3 = 3; epsilon = 2.306 . 3 = 6.918.
    3. Khoảng tin cậy: (58.782; 72.618).
- `xs_t8_tc_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian (phút) để 9 đệ tử vượt qua một trận pháp: 15, 16, 19, 20, 20, 21, 22, 23, 24. Giả sử thời gian có phân phối chuẩn, phương sai chưa biết. Cần khoảng tin cậy đối xứng độ tin cậy 95% cho thời gian trung bình mu. (t(k; a) là số mà P(T > t(k; a)) = a với T có phân phối Student k bậc tự do.)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t8_tc_02`, `xs_t8_tc_01`
  - **Phần a** (Điền số): a) Tính trung bình mẫu x_tb.
    - **Đáp án a:** 20
  - **Phần b** (Điền số): b) Tính độ lệch chuẩn mẫu hiệu chỉnh s (chia cho n - 1).
    - **Đáp án b:** 3
  - **Phần c** (Trắc nghiệm): c) Giá trị tới hạn cần dùng là
    - **(đúng)** t(8; 0.025) = 2.306
    - t(9; 0.025) = 2.262
    - t(8; 0.05) = 1.860
    - z = 1.96
    - **Đáp án c:** t(8; 0.025) = 2.306
  - **Phần d** (Điền số): d) Nhập hai đầu mút của khoảng tin cậy, đầu nhỏ trước (số thập phân đúng).
    - **Đáp án d:** 8847/500, 11153/500
  - **Lời giải:**
    1. a) Tổng 180, x_tb = 180/9 = 20.
    2. b) Các độ lệch -5, -4, -1, 0, 0, 1, 2, 3, 4; tổng bình phương 72; s^2 = 72/8 = 9, s = 3.
    3. c) Chưa biết sigma, n = 9: Student n - 1 = 8 bậc tự do, mỗi phía 0.025: t(8; 0.025) = 2.306.
    4. d) epsilon = 2.306 . 3/sqrt(9) = 2.306; khoảng (20 - 2.306; 20 + 2.306) = (17.694; 22.306).
- `xs_t8_tc_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một mẫu cỡ n = 16 từ tổng thể có phân phối chuẩn (phương sai chưa biết) cho x_tb = 30 và s = 8. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho mu, biết t(15; 0.025) = 2.131 và t(15; 0.05) = 1.753, với P(T > t(15; a)) = a khi T có phân phối Student 15 bậc tự do. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_02`, `xs_g8_khoang_t`
  - **Lời giải đưa ra (có một bước sai):**
    1. Chưa biết sigma, tổng thể chuẩn, mẫu nhỏ: dùng phân phối Student n - 1 = 15 bậc tự do.
    2. Sai số chuẩn s/sqrt(n) = 8/4 = 2.
    3. Độ tin cậy 95% nên chọn giá trị tới hạn t(15; 0.05) = 1.753.   **<- bước sai đầu tiên**
    4. epsilon = 1.753 . 2 = 3.506.
    5. Khoảng tin cậy (26.494; 33.506).
  - **Đáp án:** Bước 3: Độ tin cậy 95% nên chọn giá trị tới hạn t(15; 0.05) = 1.753.
  - **Vì sao sai, và bước đúng:**
    1. Khoảng đối xứng hai phía: 5% còn lại chia đôi, mỗi phía 0.025. t(15; 0.05) là giá trị của khoảng một phía (chỉ có 90% cho khoảng hai phía).
    2. Đúng: epsilon = 2.131 . 2 = 4.262, khoảng (25.738; 34.262).

### Khoảng tin cậy cho tỷ lệ (`xs_t8_tin_cay_ty_le`)

- `xs_t8_ty_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hỏi ngẫu nhiên 400 đệ tử thì có 80 người muốn học thêm trận pháp. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho tỷ lệ p đệ tử của cả tông môn muốn học thêm trận pháp, dùng xấp xỉ chuẩn với z = 1.96 và sai số chuẩn sqrt(f(1 - f)/n), f là tần suất mẫu. Nhập hai đầu mút, đầu nhỏ trước.
  - **Đáp án:** 201/1250, 299/1250
    1. f = 80/400 = 0.2.
    2. Sai số chuẩn sqrt(0.2 . 0.8/400) = sqrt(0.0004) = 0.02.
    3. epsilon = 1.96 . 0.02 = 0.0392; khoảng (0.2 - 0.0392; 0.2 + 0.0392) = (0.1608; 0.2392).
- `xs_t8_ty_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong n phép thử độc lập, mỗi phép thử thành công với xác suất p, gọi m là số lần thành công và f = m/n là tần suất thành công. Khi đó E(f) = p và V(f) = p(1 - p)/n.
  - **Đáp án:** Đúng
    1. m có phân phối nhị thức B(n, p): E(m) = np, V(m) = np(1 - p).
    2. f = m/n: E(f) = p, V(f) = np(1 - p)/n^2 = p(1 - p)/n. Mệnh đề đúng; vì thế sai số chuẩn của f là sqrt(p(1 - p)/n), ước lượng bằng sqrt(f(1 - f)/n).
- `xs_t8_ty_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một mẫu 100 viên đan có 50 viên đạt chuẩn. Với độ tin cậy 95% (z = 1.96) và sai số chuẩn sqrt(f(1 - f)/n), sai số epsilon của khoảng tin cậy đối xứng cho tỷ lệ đạt chuẩn bằng bao nhiêu?
    - **(đúng)** 0.098
    - 0.0049
    - 0.05
    - 0.196
  - **Đáp án:** 0.098
    1. f = 0.5; sai số chuẩn sqrt(0.5 . 0.5/100) = 0.5/10 = 0.05.
    2. epsilon = 1.96 . 0.05 = 0.098. (0.0049 là quên căn bậc hai, 0.05 là quên nhân z.)
- `xs_t8_ty_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Trong 100 hạt linh mễ gieo thử có 36 hạt nảy mầm. Lập khoảng tin cậy đối xứng độ tin cậy 95% cho tỷ lệ nảy mầm p, dùng z = 1.96 và sai số chuẩn sqrt(f(1 - f)/n). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Tần suất mẫu f = 36/100 = 0.36.
    2. Sai số chuẩn: sqrt(f(1 - f))/n = sqrt(0.36 . 0.64)/100 = 0.48/100 = 0.0048.   **<- bước sai đầu tiên**
    3. epsilon = 1.96 . 0.0048 = 0.009408.
    4. Khoảng tin cậy (0.350592; 0.369408).
  - **Đáp án:** Bước 2: Sai số chuẩn: sqrt(f(1 - f))/n = sqrt(0.36 . 0.64)/100 = 0.48/100 = 0.0048.
  - **Vì sao sai, và bước đúng:**
    1. Chia cho n nằm trong căn: sqrt(f(1 - f)/n) = 0.48/sqrt(100) = 0.48/10 = 0.048.
    2. epsilon = 1.96 . 0.048 = 0.09408; khoảng (0.26592; 0.45408).
- `xs_g8_ty_le` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong một mẫu ngẫu nhiên 100 phần tử có 64 trường hợp sản phẩm là phế phẩm. Lập khoảng tin cậy đối xứng độ tin cậy 99% cho tỷ lệ p của tổng thể, dùng xấp xỉ chuẩn với z = 2.58 và sai số chuẩn sqrt(f(1 - f)/n), f là tần suất mẫu. Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 1613/3125, 2387/3125
    1. f = 64/100 = 0.64.
    2. Sai số chuẩn sqrt(f(1 - f)/n) = sqrt(0.64 . 0.36/100) = 0.048.
    3. epsilon = 2.58 . 0.048 = 0.12384.
    4. Khoảng tin cậy: (0.51616; 0.76384).
  - **Câu hỏi:** Trong một mẫu ngẫu nhiên 100 phần tử có 20 trường hợp sản phẩm là phế phẩm. Lập khoảng tin cậy đối xứng độ tin cậy 90% cho tỷ lệ p của tổng thể, dùng xấp xỉ chuẩn với z = 1.645 (Phi(1.645) = 0.45) và sai số chuẩn sqrt(f(1 - f)/n), f là tần suất mẫu. Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 671/5000, 1329/5000
    1. f = 20/100 = 0.2.
    2. Sai số chuẩn sqrt(f(1 - f)/n) = sqrt(0.2 . 0.8/100) = 0.04.
    3. epsilon = 1.645 . 0.04 = 0.0658.
    4. Khoảng tin cậy: (0.1342; 0.2658).
  - **Câu hỏi:** Trong một mẫu ngẫu nhiên 150 phần tử có 60 trường hợp hạt giống nảy mầm. Lập khoảng tin cậy đối xứng độ tin cậy 99% cho tỷ lệ p của tổng thể, dùng xấp xỉ chuẩn với z = 2.58 và sai số chuẩn sqrt(f(1 - f)/n), f là tần suất mẫu. Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, không làm tròn).
  - **Đáp án:** 371/1250, 629/1250
    1. f = 60/150 = 0.4.
    2. Sai số chuẩn sqrt(f(1 - f)/n) = sqrt(0.4 . 0.6/150) = 0.04.
    3. epsilon = 2.58 . 0.04 = 0.1032.
    4. Khoảng tin cậy: (0.2968; 0.5032).
- `xs_t8_ty_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hỏi ngẫu nhiên 900 cư dân một thành thì có 90 người từng gặp yêu thú. Dùng xấp xỉ chuẩn, sai số chuẩn sqrt(f(1 - f)/n) với f là tần suất mẫu, và z = 1.96 cho độ tin cậy 95%.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_03`
  - **Phần a** (Điền số): a) Tính tần suất mẫu f.
    - **Đáp án a:** 1/10
  - **Phần b** (Điền số): b) Tính sai số chuẩn sqrt(f(1 - f)/n).
    - **Đáp án b:** 1/100
  - **Phần c** (Điền số): c) Nhập hai đầu mút của khoảng tin cậy đối xứng 95% cho tỷ lệ p của cả thành, đầu nhỏ trước.
    - **Đáp án c:** 201/2500, 299/2500
  - **Phần d** (Đúng/Sai): d) Cả khoảng tin cậy này nằm dưới 0.12, nên với độ tin cậy 95% có thể nói tỷ lệ p của cả thành nhỏ hơn 0.12.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) f = 90/900 = 0.1.
    2. b) sqrt(0.1 . 0.9/900) = sqrt(0.0001) = 0.01.
    3. c) epsilon = 1.96 . 0.01 = 0.0196; khoảng (0.0804; 0.1196).
    4. d) Đầu mút trên 0.1196 < 0.12, nên khoảng tin cậy 95% nằm trọn dưới 0.12: kết luận đúng ở độ tin cậy đó.
- `xs_t8_ty_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong 150 viên đan kiểm tra có 60 viên đạt thượng phẩm. Sắp xếp các bước lập khoảng tin cậy đối xứng 95% cho tỷ lệ thượng phẩm p (z = 1.96, sai số chuẩn sqrt(f(1 - f)/n)).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_04`, `xs_t8_ty_01`
  - **Đáp án (thứ tự đúng):**
    1. Tần suất mẫu f = 60/150 = 0.4.
    2. Sai số chuẩn sqrt(f(1 - f)/n) = sqrt(0.4 . 0.6/150) = sqrt(0.0016) = 0.04.
    3. Sai số epsilon = 1.96 . 0.04 = 0.0784.
    4. Khoảng tin cậy (0.4 - 0.0784; 0.4 + 0.0784) = (0.3216; 0.4784).
  - **Lời giải:**
    1. Mỗi bước dùng kết quả của bước trước: f, rồi sai số chuẩn, rồi epsilon, rồi khoảng.
    2. nf = 60 và n(1 - f) = 90 đều lớn nên xấp xỉ chuẩn dùng được.

### Chọn cỡ mẫu theo độ chính xác (`xs_t8_co_mau`)

- `xs_t8_cm_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chiều dài (cm) một loại phù lục có phân phối chuẩn với độ lệch chuẩn sigma = 15 đã biết. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng 95% cho chiều dài trung bình có sai số epsilon = 1.96 sigma/sqrt(n) không vượt quá 3. Tìm n.
  - **Đáp án:** 97
    1. 1.96 . 15/sqrt(n) <= 3 tương đương sqrt(n) >= 1.96 . 5 = 9.8.
    2. n >= 9.8^2 = 96.04.
    3. n nguyên nhỏ nhất là 97 (làm tròn lên, không làm tròn xuống).
- `xs_t8_cm_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giữ nguyên độ tin cậy và độ lệch chuẩn sigma (đã biết). Muốn sai số epsilon = z sigma/sqrt(n) của khoảng tin cậy cho trung bình giảm còn một nửa thì chỉ cần tăng cỡ mẫu lên gấp đôi.
  - **Đáp án:** Sai
    1. epsilon tỉ lệ với 1/sqrt(n): tăng n gấp đôi chỉ chia epsilon cho sqrt(2), khoảng 1.41.
    2. Muốn epsilon giảm một nửa phải tăng n gấp 4. Mệnh đề sai.
- `xs_t8_cm_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cần ước lượng một tỷ lệ p khi chưa có thông tin gì trước về p, với độ tin cậy 95% (z = 1.96) và sai số z sqrt(p(1 - p)/n) không vượt quá 0.05. Dùng p(1 - p) <= 1/4 (đúng với mọi p), cỡ mẫu nhỏ nhất bảo đảm điều đó với mọi p là bao nhiêu?
    - **(đúng)** 385
    - 384
    - 196
    - 20
  - **Đáp án:** 385
    1. Trường hợp xấu nhất p(1 - p) = 1/4: cần 1.96 . sqrt(1/(4n)) <= 0.05, tức n >= 1.96^2 . 0.25/0.05^2.
    2. 1.96^2 . 0.25/0.0025 = 3.8416 . 100 = 384.16.
    3. n nhỏ nhất là 385; 384 còn thiếu vì 384 < 384.16.
- `xs_t8_cm_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Độ lệch chuẩn đã biết sigma = 20. Tìm cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng 95% cho trung bình có sai số epsilon = 1.96 sigma/sqrt(n) không vượt quá 5. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. 1.96 . 20/sqrt(n) <= 5 tương đương sqrt(n) >= 1.96 . 20/5 = 7.84.
    2. Bình phương hai vế không âm: n >= 7.84^2 = 61.4656.
    3. Làm tròn theo quy tắc thông thường: n nhỏ nhất là 61.   **<- bước sai đầu tiên**
    4. Vậy cần lấy mẫu 61 phần tử.
  - **Đáp án:** Bước 3: Làm tròn theo quy tắc thông thường: n nhỏ nhất là 61.
  - **Vì sao sai, và bước đúng:**
    1. n phải thỏa n >= 61.4656; 61 nhỏ hơn 61.4656 nên với n = 61 sai số vẫn vượt 5.
    2. Cỡ mẫu luôn làm tròn lên: n = 62.
- `xs_g8_co_mau` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một mẫu thử cho tần suất f = 0.1; coi f(1 - f) = 0.09 không đổi khi lấy mẫu chính thức. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy 90% cho tỷ lệ có sai số epsilon = z sqrt(f(1 - f)/n) không vượt quá 0.04, dùng z = 1.645 (Phi(1.645) = 0.45). Tìm n.
  - **Đáp án:** 153
    1. z sqrt(f(1 - f)/n) <= epsilon tương đương n >= z^2 f(1 - f)/epsilon^2.
    2. z^2 f(1 - f)/epsilon^2 = 1.645^2 . 0.09/0.04^2 = 152.21390625.
    3. n là số nguyên nhỏ nhất không nhỏ hơn 152.21390625: n = 153.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 5 đã biết. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy 90% cho kỳ vọng có sai số epsilon = z sigma/sqrt(n) không vượt quá 2, dùng z = 1.645 (Phi(1.645) = 0.45). Tìm n.
  - **Đáp án:** 17
    1. z sigma/sqrt(n) <= 2 tương đương n >= (z sigma/epsilon)^2.
    2. (z sigma/epsilon)^2 = (1.645 . 5/2)^2 = 4.1125^2 = 16.91265625.
    3. n là số nguyên nhỏ nhất không nhỏ hơn 16.91265625: n = 17.
  - **Câu hỏi:** Một mẫu thử cho tần suất f = 0.5; coi f(1 - f) = 0.25 không đổi khi lấy mẫu chính thức. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy 90% cho tỷ lệ có sai số epsilon = z sqrt(f(1 - f)/n) không vượt quá 0.02, dùng z = 1.645 (Phi(1.645) = 0.45). Tìm n.
  - **Đáp án:** 1692
    1. z sqrt(f(1 - f)/n) <= epsilon tương đương n >= z^2 f(1 - f)/epsilon^2.
    2. z^2 f(1 - f)/epsilon^2 = 1.645^2 . 0.25/0.02^2 = 1691.265625.
    3. n là số nguyên nhỏ nhất không nhỏ hơn 1691.265625: n = 1692.
- `xs_t8_cm_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Năng suất (cân) một ruộng linh thảo có phân phối chuẩn với độ lệch chuẩn sigma = 10 đã biết. Thu hoạch thử 25 ruộng được trung bình x_tb = 60. Dùng z = 1.96 cho độ tin cậy 95%.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_01`, `xs_t8_cm_01`, `xs_t8_cm_04`
  - **Phần a** (Điền số): a) Tính sai số epsilon = 1.96 sigma/sqrt(n) của khoảng tin cậy 95% từ 25 ruộng này.
    - **Đáp án a:** 98/25
  - **Phần b** (Điền số): b) Nhập hai đầu mút của khoảng tin cậy đó, đầu nhỏ trước.
    - **Đáp án b:** 1402/25, 1598/25
  - **Phần c** (Điền số): c) Cần tổng cộng ít nhất bao nhiêu ruộng để sai số không vượt quá 2?
    - **Đáp án c:** 97
  - **Phần d** (Điền số): d) Vậy phải thu hoạch thêm ít nhất bao nhiêu ruộng nữa, ngoài 25 ruộng đã có?
    - **Đáp án d:** 72
  - **Lời giải:**
    1. a) epsilon = 1.96 . 10/5 = 3.92.
    2. b) (60 - 3.92; 60 + 3.92) = (56.08; 63.92).
    3. c) 1.96 . 10/sqrt(n) <= 2 cho sqrt(n) >= 9.8, n >= 96.04; n = 97.
    4. d) 97 - 25 = 72 ruộng nữa.
- `xs_t8_cm_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Độ lệch chuẩn đã biết sigma = 10. Tìm cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng 95% cho trung bình (z = 1.96) có độ dài không vượt quá 4. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_cm_01`, `xs_t8_cm_04`
  - **Lời giải đưa ra (có một bước sai):**
    1. Khoảng tin cậy là (x_tb - epsilon; x_tb + epsilon) với epsilon = 1.96 . 10/sqrt(n).
    2. Độ dài khoảng không vượt quá 4 nghĩa là epsilon <= 4.   **<- bước sai đầu tiên**
    3. 1.96 . 10/sqrt(n) <= 4 cho sqrt(n) >= 4.9, tức n >= 24.01.
    4. Vậy n nhỏ nhất là 25.
  - **Đáp án:** Bước 2: Độ dài khoảng không vượt quá 4 nghĩa là epsilon <= 4.
  - **Vì sao sai, và bước đúng:**
    1. Độ dài khoảng (x_tb - epsilon; x_tb + epsilon) là 2 epsilon, không phải epsilon.
    2. 2 epsilon <= 4 cho epsilon <= 2: sqrt(n) >= 9.8, n >= 96.04, nên n = 97.

### Luật số lớn (`xs_t8_luat_so_lon`)

- `xs_t8_sl_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu cân đối n lần, các lần độc lập. Theo luật số lớn, khi n tăng mãi thì hiệu (số lần ngửa) - (số lần sấp) dần tiến về 0.
  - **Đáp án:** Sai
    1. Luật số lớn nói về tần suất: (số lần ngửa)/n dần tiến về 1/2.
    2. Hiệu số lần ngửa trừ số lần sấp có kỳ vọng 0 nhưng phương sai n, nên độ lệch chuẩn sqrt(n) tăng dần: hiệu thường ngày càng xa 0 dù tần suất ngày càng gần 1/2. Mệnh đề sai.
- `xs_t8_sl_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tung một đồng xu cân đối, các lần độc lập. Năm lần đầu đều ra mặt sấp. Xác suất lần tung thứ sáu ra mặt ngửa là bao nhiêu?
    - **(đúng)** 1/2
    - Lớn hơn 1/2, vì luật số lớn buộc mặt ngửa phải bù lại
    - 31/32
    - 1/64
  - **Đáp án:** 1/2
    1. Các lần tung độc lập: kết quả cũ không làm đổi xác suất lần sau, vẫn là 1/2.
    2. Luật số lớn không bù trừ: tần suất tiến về 1/2 vì năm lần đầu bị pha loãng bởi rất nhiều lần sau, không phải vì đồng xu nhớ.
    3. 31/32 là xác suất có ít nhất một mặt ngửa trong năm lần, 1/64 là xác suất cả sáu lần cùng ra sấp: đều không phải câu hỏi.
- `xs_t8_sl_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_100 độc lập, cùng phân phối với kỳ vọng mu và phương sai 4; X_tb là trung bình của chúng. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2 để tìm cận trên của P(|X_tb - mu| >= 0.5) (nhập phân số tối giản).
  - **Đáp án:** 4/25
    1. E(X_tb) = mu và V(X_tb) = 4/100 = 1/25.
    2. P(|X_tb - mu| >= 0.5) <= (1/25)/0.25 = 4/25.
- `xs_t8_sl_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Biến ngẫu nhiên X có E(X) = 20 và V(X) = 16. Dùng bất đẳng thức Chebyshev, tìm một cận dưới của P(12 < X < 28). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. 12 < X < 28 tương đương |X - 20| < 8.
    2. Chebyshev: P(|X - 20| < 8) >= 1 - V(X)/8.   **<- bước sai đầu tiên**
    3. = 1 - 16/8 = -1.
    4. Cận dưới âm nên không rút ra được gì.
  - **Đáp án:** Bước 2: Chebyshev: P(|X - 20| < 8) >= 1 - V(X)/8.
  - **Vì sao sai, và bước đúng:**
    1. Bất đẳng thức Chebyshev chia cho bình phương khoảng cách: P(|X - mu| < epsilon) >= 1 - V(X)/epsilon^2.
    2. Đúng: 1 - 16/64 = 3/4, nên P(12 < X < 28) >= 3/4.
- `xs_g8_chebyshev` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** X_1, ..., X_400 độc lập, cùng phân phối với kỳ vọng mu và phương sai 4; X_tb là trung bình của chúng. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2, tìm cận trên của P(|X_tb - mu| >= 1) (nhập phân số tối giản).
  - **Đáp án:** 1/100
    1. V(X_tb) = sigma^2/n = 4/400 = 1/100.
    2. P(|X_tb - mu| >= 1) <= V(X_tb)/epsilon^2 = (1/100)/1^2 = 1/100.
  - **Câu hỏi:** X_1, ..., X_500 độc lập, cùng phân phối với kỳ vọng mu và phương sai 1; X_tb là trung bình của chúng. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2, tìm cận trên của P(|X_tb - mu| >= 0.1) (nhập phân số tối giản).
  - **Đáp án:** 1/5
    1. V(X_tb) = sigma^2/n = 1/500 = 1/500.
    2. P(|X_tb - mu| >= 0.1) <= V(X_tb)/epsilon^2 = (1/500)/0.1^2 = 1/5.
  - **Câu hỏi:** X_1, ..., X_500 độc lập, cùng phân phối với kỳ vọng mu và phương sai 5; X_tb là trung bình của chúng. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2, tìm cận trên của P(|X_tb - mu| >= 1) (nhập phân số tối giản).
  - **Đáp án:** 1/100
    1. V(X_tb) = sigma^2/n = 5/500 = 1/100.
    2. P(|X_tb - mu| >= 1) <= V(X_tb)/epsilon^2 = (1/100)/1^2 = 1/100.
- `xs_t8_sl_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gieo một con xúc xắc cân đối n lần độc lập; f là tần suất ra mặt 6 (số lần ra mặt 6 chia cho n). Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_np_01`, `xs_t8_sl_03`, `xs_t8_sl_04`
  - **Phần a** (Điền số): a) Tính E(f).
    - **Đáp án a:** 1/6
  - **Phần b** (Điền số): b) Với n = 500, tính V(f).
    - **Đáp án b:** 1/3600
  - **Phần c** (Điền số): c) Với n = 500, tìm cận trên Chebyshev của P(|f - 1/6| >= 0.05).
    - **Đáp án c:** 1/9
  - **Phần d** (Điền số): d) Tìm n nhỏ nhất để cận trên Chebyshev của P(|f - 1/6| >= 0.05) không vượt quá 0.05.
    - **Đáp án d:** 1112
  - **Lời giải:**
    1. a) Số lần ra mặt 6 có phân phối B(n, 1/6), nên E(f) = 1/6.
    2. b) V(f) = (1/6)(5/6)/n = 5/(36 . 500) = 1/3600.
    3. c) (1/3600)/0.05^2 = 400/3600 = 1/9.
    4. d) (5/36)/(n . 0.0025) <= 0.05 tương đương n >= (5/36)/0.000125 = 10000/9, khoảng 1111.1; n nhỏ nhất là 1112.
- `xs_t8_sl_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X_1, X_2, ... độc lập, cùng phân phối, có kỳ vọng mu và phương sai sigma^2; X_tb = (X_1 + ... + X_n)/n. Sắp xếp các bước chứng minh luật số lớn: với mọi epsilon > 0, P(|X_tb - mu| >= epsilon) dần về 0 khi n tăng mãi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_01`, `xs_t8_sl_03`, `xs_t8_sl_04`
  - **Đáp án (thứ tự đúng):**
    1. Tính các số đặc trưng của X_tb: E(X_tb) = mu, và vì các X_i độc lập nên V(X_tb) = sigma^2/n.
    2. Áp dụng bất đẳng thức Chebyshev cho biến X_tb, có kỳ vọng mu: P(|X_tb - mu| >= epsilon) <= V(X_tb)/epsilon^2.
    3. Thay V(X_tb) vào: cận trên bằng sigma^2/(n epsilon^2).
    4. Khi n tăng mãi, sigma^2/(n epsilon^2) dần về 0, nên P(|X_tb - mu| >= epsilon) cũng dần về 0.
  - **Lời giải:**
    1. Cần E và V của X_tb trước, rồi Chebyshev, rồi thay số, rồi cho n lớn dần.
    2. Chứng minh chỉ cần phương sai hữu hạn; nó cũng cho tốc độ: xác suất lệch giảm ít nhất như 1/n.

### Định lý giới hạn trung tâm (`xs_t8_gioi_han_trung_tam`)

- `xs_t8_gh_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số linh thạch một đệ tử nộp mỗi tháng là một biến ngẫu nhiên có kỳ vọng 2 và độ lệch chuẩn 2 (không có phân phối chuẩn), các đệ tử độc lập. Gọi S là tổng số linh thạch 100 đệ tử nộp trong một tháng. Dùng định lý giới hạn trung tâm và hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2) = 0.4772, tính xấp xỉ P(S > 240) (số thập phân đúng).
  - **Đáp án:** 57/2500
    1. E(S) = 100 . 2 = 200; V(S) = 100 . 4 = 400, độ lệch chuẩn 20.
    2. Theo định lý giới hạn trung tâm S xấp xỉ N(200, 400); chuẩn hóa (240 - 200)/20 = 2.
    3. P(S > 240) xấp xỉ 0.5 - Phi(2) = 0.0228.
- `xs_t8_gh_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho X_1, ..., X_n độc lập, cùng phân phối, có phương sai hữu hạn và dương. Định lý giới hạn trung tâm (tổng X_1 + ... + X_n xấp xỉ phân phối chuẩn khi n lớn) chỉ dùng được khi mỗi X_i có phân phối chuẩn.
  - **Đáp án:** Sai
    1. Điều kỳ diệu của định lý là X_i có phân phối gì cũng được (nhị thức, Poisson, đều, mũ, ...), miễn độc lập, cùng phân phối, phương sai hữu hạn.
    2. Nếu các X_i đã chuẩn thì tổng chuẩn đúng chứ không cần xấp xỉ. Mệnh đề sai.
- `xs_t8_gh_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X là số lần ngửa khi tung một đồng xu cân đối 400 lần. Dùng xấp xỉ chuẩn (định lý giới hạn trung tâm, không hiệu chỉnh liên tục) và Phi(1) = 0.3413 (Phi là hàm Laplace), P(X < 210) xấp xỉ bằng
    - **(đúng)** 0.8413
    - 0.3413
    - 0.1587
    - 0.6826
  - **Đáp án:** 0.8413
    1. X ~ B(400, 1/2): E(X) = 200, V(X) = 100, độ lệch chuẩn 10.
    2. Chuẩn hóa (210 - 200)/10 = 1.
    3. P(X < 210) xấp xỉ 0.5 + Phi(1) = 0.8413.
- `xs_t8_gh_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Mỗi bao linh mễ có khối lượng (kg) với kỳ vọng 5 và độ lệch chuẩn 0.8, các bao độc lập. Một xe chở 64 bao; T là tổng khối lượng. Dùng định lý giới hạn trung tâm và Phi(0.5) = 0.1915 (Phi là hàm Laplace), tính xấp xỉ P(T > 323.2). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. E(T) = 64 . 5 = 320.
    2. Độ lệch chuẩn của T = 64 . 0.8 = 51.2.   **<- bước sai đầu tiên**
    3. Chuẩn hóa: (323.2 - 320)/51.2 = 0.0625.
    4. P(T > 323.2) xấp xỉ 0.5 - Phi(0.0625), gần bằng 0.5.
  - **Đáp án:** Bước 2: Độ lệch chuẩn của T = 64 . 0.8 = 51.2.
  - **Vì sao sai, và bước đúng:**
    1. Cộng phương sai chứ không cộng độ lệch chuẩn: V(T) = 64 . 0.64 = 40.96, độ lệch chuẩn = 0.8 . sqrt(64) = 6.4.
    2. Chuẩn hóa (323.2 - 320)/6.4 = 0.5; P(T > 323.2) xấp xỉ 0.5 - 0.1915 = 0.3085.
- `xs_g8_tong_clt` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Số linh thạch một đệ tử nộp mỗi tháng là một biến ngẫu nhiên có kỳ vọng 2 và độ lệch chuẩn 5 (không nhất thiết có phân phối chuẩn), và giá trị này ở các cá thể khác nhau độc lập với nhau. Gọi S là tổng số linh thạch 36 đệ tử nộp. Dùng định lý giới hạn trung tâm (xấp xỉ S bằng phân phối chuẩn) và hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2) = 0.4772, tính xấp xỉ P(12 < S < 132) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1193/1250
    1. E(S) = n . 2 = 72; V(S) = n . 5^2 = 900, độ lệch chuẩn của S = 5 . sqrt(36) = 30.
    2. Chuẩn hóa: (12 - 72)/30 = -2, (132 - 72)/30 = 2.
    3. P xấp xỉ Phi(2) - Phi(-2) = 0.4772 + 0.4772 = 0.9544.
  - **Câu hỏi:** Số linh thạch một đệ tử nộp mỗi tháng là một biến ngẫu nhiên có kỳ vọng 2 và độ lệch chuẩn 1 (không nhất thiết có phân phối chuẩn), và giá trị này ở các cá thể khác nhau độc lập với nhau. Gọi S là tổng số linh thạch 25 đệ tử nộp. Dùng định lý giới hạn trung tâm (xấp xỉ S bằng phân phối chuẩn) và hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1.5) = 0.4332, tính xấp xỉ P(42.5 < S < 57.5) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 1083/1250
    1. E(S) = n . 2 = 50; V(S) = n . 1^2 = 25, độ lệch chuẩn của S = 1 . sqrt(25) = 5.
    2. Chuẩn hóa: (42.5 - 50)/5 = -1.5, (57.5 - 50)/5 = 1.5.
    3. P xấp xỉ Phi(1.5) - Phi(-1.5) = 0.4332 + 0.4332 = 0.8664.
  - **Câu hỏi:** Khối lượng mỗi bao gạo (kg) là một biến ngẫu nhiên có kỳ vọng 20 và độ lệch chuẩn 5 (không nhất thiết có phân phối chuẩn), và giá trị này ở các cá thể khác nhau độc lập với nhau. Gọi S là tổng khối lượng của 36 bao. Dùng định lý giới hạn trung tâm (xấp xỉ S bằng phân phối chuẩn) và hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2.5) = 0.4938, tính xấp xỉ P(S > 645) (đáp số là số thập phân đúng, không làm tròn thêm).
  - **Đáp án:** 4969/5000
    1. E(S) = n . 20 = 720; V(S) = n . 5^2 = 900, độ lệch chuẩn của S = 5 . sqrt(36) = 30.
    2. Chuẩn hóa: (645 - 720)/30 = -2.5.
    3. P xấp xỉ 0.5 - Phi(-2.5) = 0.5 - (-0.4938) = 0.9938.
- `xs_t8_gh_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một thang máy trận pháp chở được tối đa 2304 cân. Cân nặng một đệ tử có kỳ vọng 60 và độ lệch chuẩn 12 (cân), các đệ tử độc lập. 36 đệ tử cùng bước vào; T là tổng cân nặng. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(2) = 0.4772.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_gh_04`, `xs_t8_gh_01`, `xs_t6_ch_04`
  - **Phần a** (Điền số): a) Tính E(T).
    - **Đáp án a:** 2160
  - **Phần b** (Điền số): b) Tính độ lệch chuẩn của T.
    - **Đáp án b:** 72
  - **Phần c** (Điền số): c) Dùng định lý giới hạn trung tâm, tính xấp xỉ xác suất thang máy quá tải P(T > 2304) (số thập phân đúng).
    - **Đáp án c:** 57/2500
  - **Phần d** (Đúng/Sai): d) Cách tính ở câu c chỉ dùng được khi cân nặng mỗi đệ tử có phân phối chuẩn.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) E(T) = 36 . 60 = 2160.
    2. b) V(T) = 36 . 144, độ lệch chuẩn 12 . 6 = 72.
    3. c) (2304 - 2160)/72 = 2; P(T > 2304) xấp xỉ 0.5 - 0.4772 = 0.0228.
    4. d) Sai: định lý giới hạn trung tâm chỉ cần các cân nặng độc lập, cùng phân phối, phương sai hữu hạn; 36 người đã đủ để xấp xỉ.
- `xs_t8_gh_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số lỗi trên một trang phù lục có phân phối Poisson với tham số 4 (kỳ vọng 4, phương sai 4); 100 trang độc lập. S là tổng số lỗi của 100 trang, X_tb = S/100. Dùng định lý giới hạn trung tâm và hàm Laplace với Phi(1) = 0.3413, Phi(2) = 0.4772. Ghép mỗi đại lượng với giá trị của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_np_02`, `xs_t8_gh_01`, `xs_t7_pm_01`
  - **Đáp án (ghép đúng):**
    - E(S) — 400
    - Độ lệch chuẩn của S — 20
    - V(X_tb) — 1/25
    - P(S > 440), xấp xỉ — 0.0228
    - P(3.8 < X_tb < 4.2), xấp xỉ — 0.6826
  - **Lời giải:**
    1. E(S) = 100 . 4 = 400; V(S) = 400, độ lệch chuẩn 20; V(X_tb) = 4/100 = 1/25, độ lệch chuẩn 0.2.
    2. P(S > 440): (440 - 400)/20 = 2, xấp xỉ 0.5 - 0.4772 = 0.0228.
    3. P(3.8 < X_tb < 4.2): chuẩn hóa thành -1 và 1, xấp xỉ 2 . 0.3413 = 0.6826.

## Tầng 9: Kiểm định giả thuyết thống kê

35 dạng câu (30 câu viết tay, 5 bộ sinh câu); 35 chưa duyệt.

### Giả thuyết, mức ý nghĩa và hai loại sai lầm (`xs_t9_gia_thuyet`)

- `xs_t9_gt_01` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nhà sản xuất nói khối lượng trung bình một gói linh trà là 500 g. Kiểm định H0: mu = 500 với đối thuyết H1: mu != 500 ở mức ý nghĩa 5% cho z = 1.2, nên không bác bỏ H0. Từ đó có thể khẳng định khối lượng trung bình của các gói đúng bằng 500 g.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_03`, `xs_t7_tm_04`
  - **Đáp án:** Sai
    1. |z| = 1.2 < 1.96 chỉ nói rằng dữ liệu chưa đủ bằng chứng chống lại H0.
    2. Không bác bỏ H0 không chứng minh H0 đúng: mu = 501 hay 499 cũng rất có thể cho z như vậy, và xác suất sai lầm loại hai chưa được kiểm soát. Mệnh đề sai.
- `xs_t9_gt_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một kiểm định trung bình cho p-giá trị bằng 0.03 (p-giá trị: xác suất, khi H0 đúng, được một thống kê lệch khỏi H0 ít nhất như giá trị quan sát). Điều đó có nghĩa là xác suất để giả thuyết H0 đúng bằng 0.03.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_03`, `xs_t7_pm_03`
  - **Đáp án:** Sai
    1. p-giá trị được tính khi đã giả sử H0 đúng: nó là xác suất của dữ liệu (cực đoan như vậy) dưới H0, không phải xác suất của H0.
    2. Trong cách nhìn này H0 đúng hay sai chứ không có xác suất; p = 0.03 < 0.05 chỉ có nghĩa là bác bỏ H0 ở mức 5%. Mệnh đề sai.
- `xs_t9_gt_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một trạm kiểm tra đan dược kiểm định H0: lô đan đạt chuẩn với đối thuyết H1: lô đan không đạt chuẩn; bác bỏ H0 thì lô bị tiêu hủy, không bác bỏ thì lô được cho qua. Sai lầm loại hai trong tình huống này là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_tm_04`, `xs_t8_tc_03`
    - **(đúng)** Cho một lô không đạt chuẩn qua trạm
    - Tiêu hủy một lô đạt chuẩn
    - Tiêu hủy một lô không đạt chuẩn
    - Cho một lô đạt chuẩn qua trạm
  - **Đáp án:** Cho một lô không đạt chuẩn qua trạm
    1. Sai lầm loại một: bác bỏ H0 khi H0 đúng (tiêu hủy lô đạt chuẩn), xác suất là mức ý nghĩa alpha.
    2. Sai lầm loại hai: không bác bỏ H0 khi H0 sai, tức cho một lô không đạt chuẩn qua trạm.
    3. Hai phương án còn lại là quyết định đúng.
- `xs_t9_gt_04` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi tình huống với cặp giả thuyết H0, H1 phù hợp (mu là trung bình, p là tỷ lệ của tổng thể).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_tm_01`, `xs_t8_tc_03`
  - **Đáp án (ghép đúng):**
    - Khách hàng nghi gói linh trà ghi 500 g bị đóng thiếu — H0: mu = 500, H1: mu < 500
    - Thợ máy muốn biết máy đóng gói có lệch khỏi 500 g, thừa hoặc thiếu, hay không — H0: mu = 500, H1: mu != 500
    - Một công thức mới được kỳ vọng làm năng suất trung bình vượt 500 — H0: mu = 500, H1: mu > 500
    - Trạm kiểm tra nghi tỷ lệ phế phẩm đã vượt 5% — H0: p = 0.05, H1: p > 0.05
  - **Lời giải:**
    1. H0 luôn là đẳng thức với giá trị được công bố; H1 là điều người kiểm định muốn tìm bằng chứng.
    2. Nghi thiếu: một phía trái; nghi lệch cả hai chiều: hai phía; kỳ vọng tăng: một phía phải.
    3. Câu về phế phẩm nói về tỷ lệ p, không phải trung bình.
- `xs_t9_gt_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một đại lượng có phân phối chuẩn với sigma đã biết. Kiểm định H0: mu = 100 với đối thuyết H1: mu != 100 ở mức ý nghĩa 5%; thống kê z tính từ mẫu bằng 1.8. Biết Phi(1.645) = 0.45 và Phi(1.96) = 0.475 (Phi là hàm Laplace). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_02`, `xs_t8_tc_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Đối thuyết mu != 100 nên đây là kiểm định hai phía.
    2. Thống kê kiểm định z = 1.8.
    3. Mức ý nghĩa 5%: miền bác bỏ là z > 1.645.   **<- bước sai đầu tiên**
    4. 1.8 > 1.645 nên bác bỏ H0.
  - **Đáp án:** Bước 3: Mức ý nghĩa 5%: miền bác bỏ là z > 1.645.
  - **Vì sao sai, và bước đúng:**
    1. Kiểm định hai phía chia 5% cho hai đuôi, mỗi đuôi 0.025: miền bác bỏ là |z| > 1.96 (Phi(1.96) = 0.475). 1.645 là giá trị của kiểm định một phía.
    2. |z| = 1.8 < 1.96 nên chưa đủ cơ sở bác bỏ H0 ở mức 5%.
- `xs_t9_gt_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 4. Lấy mẫu cỡ n = 16 để kiểm định H0: mu = 50 với đối thuyết H1: mu = 53, theo quy tắc: bác bỏ H0 khi x_tb > 52. Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) với Phi(1) = 0.3413 và Phi(2) = 0.4772.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_03`, `xs_t7_pm_04`, `xs_g7_trung_binh_mau_chuan`
  - **Phần a** (Điền số): a) Tính xác suất sai lầm loại một alpha = P(X_tb > 52) khi mu = 50 (số thập phân đúng).
    - **Đáp án a:** 57/2500
  - **Phần b** (Điền số): b) Tính xác suất sai lầm loại hai beta = P(X_tb <= 52) khi mu = 53 (số thập phân đúng).
    - **Đáp án b:** 1587/10000
  - **Phần c** (Điền số): c) Tính lực của kiểm định 1 - beta.
    - **Đáp án c:** 8413/10000
  - **Phần d** (Đúng/Sai): d) Nếu đổi ngưỡng thành 52.5 (bác bỏ H0 khi x_tb > 52.5) thì alpha giảm còn beta tăng.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) X_tb có độ lệch chuẩn 4/sqrt(16) = 1. Khi mu = 50: (52 - 50)/1 = 2, alpha = 0.5 - 0.4772 = 0.0228.
    2. b) Khi mu = 53: (52 - 53)/1 = -1, beta = P(Z <= -1) = 0.5 - 0.3413 = 0.1587.
    3. c) 1 - beta = 0.8413.
    4. d) Ngưỡng cao hơn thì khó bác bỏ H0 hơn: alpha = P(X_tb > 52.5 | mu = 50) nhỏ đi, beta = P(X_tb <= 52.5 | mu = 53) lớn lên. Đúng: với cỡ mẫu cố định, giảm loại sai lầm này thì tăng loại kia.
- `xs_g9_quyet_dinh` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 25 đã biết. Kiểm định H0: mu = 30 với đối thuyết H1: mu > 30 ở mức ý nghĩa 0.05, dùng thống kê z = (x_tb - mu_0)/(sigma/sqrt(n)) và giá trị tới hạn 1.645 (Phi(1.645) = 0.45). Một mẫu cỡ n = 25 có x_tb = 16. Khẳng định: với mẫu này, kiểm định bác bỏ H0.
  - **Đáp án:** Sai
    1. z = (16 - 30)/(25/5) = -14/5 = -2.8.
    2. Miền bác bỏ phía phải: bác bỏ H0 khi z > 1.645.
    3. z = -2.8 < 1.645: chưa đủ cơ sở bác bỏ H0, khẳng định sai.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 1.5 đã biết. Kiểm định H0: mu = 30 với đối thuyết H1: mu > 30 ở mức ý nghĩa 0.05, dùng thống kê z = (x_tb - mu_0)/(sigma/sqrt(n)) và giá trị tới hạn 1.645 (Phi(1.645) = 0.45). Một mẫu cỡ n = 9 có x_tb = 29.1. Khẳng định: với mẫu này, kiểm định bác bỏ H0.
  - **Đáp án:** Sai
    1. z = (29.1 - 30)/(1.5/3) = -0.9/0.5 = -1.8.
    2. Miền bác bỏ phía phải: bác bỏ H0 khi z > 1.645.
    3. z = -1.8 < 1.645: chưa đủ cơ sở bác bỏ H0, khẳng định sai.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 30 đã biết. Kiểm định H0: mu = 200 với đối thuyết H1: mu != 200 ở mức ý nghĩa 0.01, dùng thống kê z = (x_tb - mu_0)/(sigma/sqrt(n)) và giá trị tới hạn 2.58 (Phi(2.58) = 0.495). Một mẫu cỡ n = 36 có x_tb = 214. Khẳng định: với mẫu này, kiểm định bác bỏ H0.
  - **Đáp án:** Đúng
    1. z = (214 - 200)/(30/6) = 14/5 = 2.8.
    2. Miền bác bỏ hai phía: bác bỏ H0 khi |z| > 2.58.
    3. |z| = 2.8 > 2.58: bác bỏ H0, khẳng định đúng.

### Kiểm định trung bình một tổng thể (`xs_t9_kiem_dinh_trung_binh`)

- `xs_t9_kt_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khối lượng (g) một gói linh trà có phân phối chuẩn với sigma = 9 đã biết; nhà sản xuất ghi 500 g. Một đoàn kiểm tra nghi gói bị đóng thiếu, cân 36 gói được x_tb = 497. Mức ý nghĩa 5%, giá trị tới hạn một phía 1.645 (Phi(1.645) = 0.45, Phi là hàm Laplace).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_04`, `xs_t8_tc_01`
  - **Phần a** (Trắc nghiệm): a) Cặp giả thuyết phù hợp là
    - **(đúng)** H0: mu = 500, H1: mu < 500
    - H0: mu = 500, H1: mu != 500
    - H0: mu < 500, H1: mu = 500
    - H0: mu = 497, H1: mu < 497
    - **Đáp án a:** H0: mu = 500, H1: mu < 500
  - **Phần b** (Điền số): b) Tính z = (x_tb - 500)/(sigma/sqrt(n)).
    - **Đáp án b:** -2
  - **Phần c** (Trắc nghiệm): c) Kết luận đúng là
    - **(đúng)** z = -2 < -1.645: bác bỏ H0, gói bị đóng thiếu ở mức ý nghĩa 5%
    - |z| = 2 > 1.96: bác bỏ H0 vì đây là kiểm định hai phía
    - z = -2 < 1.645: chưa đủ cơ sở bác bỏ H0
    - z = -2 cho thấy H0 sai với xác suất 98%
    - **Đáp án c:** z = -2 < -1.645: bác bỏ H0, gói bị đóng thiếu ở mức ý nghĩa 5%
  - **Lời giải:**
    1. a) H0 là giá trị được công bố 500; nghi thiếu nên H1: mu < 500 (một phía trái). Giả thuyết nói về mu của tổng thể, không về con số 497 của mẫu.
    2. b) sigma/sqrt(n) = 9/6 = 1.5; z = (497 - 500)/1.5 = -2.
    3. c) Miền bác bỏ phía trái: z < -1.645. z = -2 rơi vào đó: bác bỏ H0.
- `xs_t9_kt_02` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thời gian (phút) luyện xong một mẻ đan của 4 lò: 7, 11, 11, 11. Giả sử thời gian có phân phối chuẩn, phương sai chưa biết. Kiểm định H0: mu = 8 với đối thuyết H1: mu != 8 ở mức ý nghĩa 5%, biết t(3; 0.025) = 3.182 (P(T > 3.182) = 0.025 với T có phân phối Student 3 bậc tự do).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t8_tc_02`, `xs_g8_khoang_t`
  - **Phần a** (Điền số): a) Tính trung bình mẫu x_tb.
    - **Đáp án a:** 10
  - **Phần b** (Điền số): b) Tính độ lệch chuẩn mẫu hiệu chỉnh s (chia cho n - 1).
    - **Đáp án b:** 2
  - **Phần c** (Điền số): c) Tính thống kê t = (x_tb - 8)/(s/sqrt(n)).
    - **Đáp án c:** 2
  - **Phần d** (Đúng/Sai): d) Ở mức ý nghĩa 5%, kiểm định bác bỏ H0.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) x_tb = 40/4 = 10.
    2. b) Độ lệch -3, 1, 1, 1; tổng bình phương 12; s^2 = 12/3 = 4, s = 2.
    3. c) s/sqrt(n) = 2/2 = 1; t = (10 - 8)/1 = 2.
    4. d) Hai phía: bác bỏ khi |t| > 3.182. |t| = 2 < 3.182 nên chưa đủ cơ sở bác bỏ H0 (mẫu quá nhỏ để thấy chênh lệch 2 phút).
- `xs_t9_kt_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Một đại lượng có phân phối chuẩn với sigma = 6 đã biết. Kiểm định H0: mu = 20 với đối thuyết H1: mu != 20 ở mức ý nghĩa 5% (giá trị tới hạn 1.96). Mẫu cỡ n = 36 có x_tb = 22. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_04`, `xs_t8_tc_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Biết sigma nên dùng thống kê z, kiểm định hai phía.
    2. z = (x_tb - 20)/sigma = (22 - 20)/6 = 1/3.   **<- bước sai đầu tiên**
    3. |z| = 1/3 < 1.96 nên không bác bỏ H0.
  - **Đáp án:** Bước 2: z = (x_tb - 20)/sigma = (22 - 20)/6 = 1/3.
  - **Vì sao sai, và bước đúng:**
    1. Thống kê chia cho độ lệch chuẩn của X_tb là sigma/sqrt(n) = 6/6 = 1, không chia cho sigma.
    2. z = (22 - 20)/1 = 2 > 1.96: bác bỏ H0. Dùng sigma thay cho sigma/sqrt(n) làm kiểm định mất gần hết sức mạnh.
- `xs_t9_kt_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điểm thi luyện đan có phân phối chuẩn với sigma = 10 đã biết. Một lớp 25 đệ tử học theo phương pháp mới được điểm trung bình 79. Kiểm định ở mức ý nghĩa 5% xem phương pháp mới có làm điểm trung bình vượt 75 không (giá trị tới hạn một phía 1.645). Sắp xếp các bước.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_pm_03`, `xs_t8_tc_01`
  - **Đáp án (thứ tự đúng):**
    1. Đặt H0: mu = 75 với đối thuyết H1: mu > 75 (kiểm định một phía phải).
    2. Khi H0 đúng, X_tb có phân phối chuẩn với kỳ vọng 75 và độ lệch chuẩn 10/sqrt(25) = 2.
    3. Tính thống kê z = (79 - 75)/2 = 2.
    4. So sánh: z = 2 > 1.645, rơi vào miền bác bỏ.
    5. Kết luận: bác bỏ H0; ở mức 5%, phương pháp mới làm điểm trung bình vượt 75.
  - **Lời giải:**
    1. Đặt giả thuyết trước, rồi tìm phân phối của X_tb khi H0 đúng, tính thống kê, so với giá trị tới hạn, kết luận.
    2. z = 2 > 1.645 nên bác bỏ H0.
- `xs_t9_kt_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Mẫu cỡ n = 16 cho x_tb = 103 và độ lệch chuẩn mẫu hiệu chỉnh s = 4. Kiểm định H0: mu = 100 với đối thuyết H1: mu != 100 ở mức ý nghĩa 5%, biết t(15; 0.025) = 2.131 (P(T > 2.131) = 0.025 với T có phân phối Student 15 bậc tự do). Thống kê kiểm định và kết luận đúng là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_02`, `xs_g8_khoang_t`
    - **(đúng)** t = 3 > 2.131: bác bỏ H0
    - t = 0.75 < 2.131: chưa đủ cơ sở bác bỏ H0
    - t = 3/16 < 2.131: chưa đủ cơ sở bác bỏ H0
    - t = 12 > 2.131: bác bỏ H0
  - **Đáp án:** t = 3 > 2.131: bác bỏ H0
    1. t = (x_tb - mu_0)/(s/sqrt(n)) = (103 - 100)/(4/4) = 3.
    2. |t| = 3 > 2.131 nên bác bỏ H0.
    3. 0.75 là chia cho s thay vì s/sqrt(n); 3/16 là chia thêm cho n; 12 là chia cho s/n.
- `xs_t9_kt_06` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với sigma đã biết. Từ một mẫu, khoảng tin cậy đối xứng 95% cho mu (dùng z = 1.96) là (48.2; 53.6). Với cùng mẫu đó, kiểm định H0: mu = 54 với đối thuyết H1: mu != 54 ở mức ý nghĩa 5% (giá trị tới hạn 1.96) bác bỏ H0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_01`, `xs_t8_tc_03`
  - **Đáp án:** Đúng
    1. Khoảng tin cậy là (x_tb - epsilon; x_tb + epsilon) với epsilon = 1.96 sigma/sqrt(n); ở đây x_tb = 50.9, epsilon = 2.7.
    2. Bác bỏ H0: mu = mu_0 ở mức 5% (hai phía) đúng khi |x_tb - mu_0| > epsilon, tức khi mu_0 nằm ngoài khoảng tin cậy.
    3. 54 nằm ngoài (48.2; 53.6): |50.9 - 54| = 3.1 > 2.7, bác bỏ H0. Mệnh đề đúng.
- `xs_g9_t_trung_binh` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Kiểm định H0: mu = 61 với đối thuyết H1: mu != 61 từ một mẫu cỡ n = 4: 60, 60, 52, 60. Tính giá trị của thống kê kiểm định t = (x_tb - mu_0)/(s/sqrt(n)), trong đó s là độ lệch chuẩn mẫu hiệu chỉnh (chia cho n - 1). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -3/2
    1. x_tb = 232/4 = 58.
    2. Tổng của (x_i - x_tb)^2 = 48; s^2 = 48/3 = 16, s = 4.
    3. s/sqrt(n) = 4/2 = 2.
    4. t = (58 - 61)/2 = -3/2.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Kiểm định H0: mu = 56 với đối thuyết H1: mu != 56 từ một mẫu cỡ n = 4: 59, 59, 59, 51. Tính giá trị của thống kê kiểm định t = (x_tb - mu_0)/(s/sqrt(n)), trong đó s là độ lệch chuẩn mẫu hiệu chỉnh (chia cho n - 1). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 1/2
    1. x_tb = 228/4 = 57.
    2. Tổng của (x_i - x_tb)^2 = 48; s^2 = 48/3 = 16, s = 4.
    3. s/sqrt(n) = 4/2 = 2.
    4. t = (57 - 56)/2 = 1/2.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn, phương sai chưa biết. Kiểm định H0: mu = 55 với đối thuyết H1: mu != 55 từ một mẫu cỡ n = 4: 47, 51, 51, 51. Tính giá trị của thống kê kiểm định t = (x_tb - mu_0)/(s/sqrt(n)), trong đó s là độ lệch chuẩn mẫu hiệu chỉnh (chia cho n - 1). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -5
    1. x_tb = 200/4 = 50.
    2. Tổng của (x_i - x_tb)^2 = 12; s^2 = 12/3 = 4, s = 2.
    3. s/sqrt(n) = 2/2 = 1.
    4. t = (50 - 55)/1 = -5.
- `xs_g9_z_trung_binh` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 20 đã biết. Kiểm định H0: mu = 40 với đối thuyết H1: mu != 40. Một mẫu cỡ n = 25 có trung bình mẫu x_tb = 34. Tính giá trị của thống kê kiểm định z = (x_tb - mu_0)/(sigma/sqrt(n)) (số thập phân đúng).
  - **Đáp án:** -3/2
    1. sigma/sqrt(n) = 20/5 = 4.
    2. z = (34 - 40)/4 = -6/4 = -1.5.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 1.5 đã biết. Kiểm định H0: mu = 40 với đối thuyết H1: mu != 40. Một mẫu cỡ n = 9 có trung bình mẫu x_tb = 39.625. Tính giá trị của thống kê kiểm định z = (x_tb - mu_0)/(sigma/sqrt(n)) (số thập phân đúng).
  - **Đáp án:** -3/4
    1. sigma/sqrt(n) = 1.5/3 = 0.5.
    2. z = (39.625 - 40)/0.5 = -0.375/0.5 = -0.75.
  - **Câu hỏi:** Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = 24 đã biết. Kiểm định H0: mu = 50 với đối thuyết H1: mu < 50. Một mẫu cỡ n = 36 có trung bình mẫu x_tb = 47. Tính giá trị của thống kê kiểm định z = (x_tb - mu_0)/(sigma/sqrt(n)) (số thập phân đúng).
  - **Đáp án:** -3/4
    1. sigma/sqrt(n) = 24/6 = 4.
    2. z = (47 - 50)/4 = -3/4 = -0.75.

### Kiểm định tỷ lệ một tổng thể (`xs_t9_kiem_dinh_ty_le`)

- `xs_t9_ky_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một xưởng luyện khí công bố tỷ lệ phế phẩm là 20%. Kiểm tra ngẫu nhiên 400 món thì có 100 phế phẩm. Kiểm định H0: p = 0.2 với đối thuyết H1: p > 0.2 ở mức ý nghĩa 5%, dùng z = (f - p0)/sqrt(p0(1 - p0)/n) với f là tần suất mẫu, và giá trị tới hạn một phía 1.645.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_04`
  - **Phần a** (Điền số): a) Tính tần suất mẫu f.
    - **Đáp án a:** 1/4
  - **Phần b** (Điền số): b) Tính z.
    - **Đáp án b:** 5/2
  - **Phần c** (Đúng/Sai): c) Kiểm định bác bỏ H0: có cơ sở nói tỷ lệ phế phẩm vượt 20%.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) f = 100/400 = 0.25.
    2. b) Khi H0 đúng, sqrt(0.2 . 0.8/400) = 0.02; z = (0.25 - 0.2)/0.02 = 2.5.
    3. c) Một phía phải: bác bỏ khi z > 1.645; 2.5 > 1.645 nên bác bỏ H0.
- `xs_t9_ky_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tung một đồng xu 100 lần được 58 lần ngửa. Kiểm định ở mức ý nghĩa 5% (giá trị tới hạn hai phía 1.96) xem đồng xu có cân đối không. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_02`, `xs_t8_ty_04`
  - **Lời giải đưa ra (có một bước sai):**
    1. H0: p = 0.5, H1: p != 0.5; tần suất mẫu f = 58/100 = 0.58.
    2. Khi H0 đúng, độ lệch chuẩn của f là sqrt(0.5 . 0.5/100) = 0.05.
    3. z = (0.58 - 0.5)/0.05 = 1.6.
    4. |z| = 1.6 < 1.96 nên chưa đủ cơ sở bác bỏ H0 ở mức 5%.
    5. Vậy đã chứng minh được xác suất ra mặt ngửa đúng bằng 0.5.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 5: Vậy đã chứng minh được xác suất ra mặt ngửa đúng bằng 0.5.
  - **Vì sao sai, và bước đúng:**
    1. Bốn bước đầu đúng. Không bác bỏ H0 chỉ có nghĩa dữ liệu phù hợp với H0, không chứng minh H0 đúng.
    2. Một đồng xu có p = 0.55 cũng rất dễ cho 58 lần ngửa; đúng phải nói: chưa có bằng chứng đồng xu lệch.
- `xs_t9_ky_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Kiểm định H0: p = 0.2 với đối thuyết H1: p > 0.2 ở mức ý nghĩa 1%, từ mẫu 625 phần tử có 150 phần tử có tính chất đang xét, dùng z = (f - p0)/sqrt(p0(1 - p0)/n). Giá trị tới hạn một phía mức 1% là 2.33 (Phi(2.33) = 0.49), giá trị tới hạn hai phía mức 1% là 2.58. Thống kê và kết luận đúng là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_03`, `xs_t8_ty_01`
    - **(đúng)** z = 2.5 > 2.33: bác bỏ H0
    - z = 2.5 < 2.58: chưa đủ cơ sở bác bỏ H0
    - z = 0.1 < 2.33: chưa đủ cơ sở bác bỏ H0
    - z = 156.25 > 2.33: bác bỏ H0
  - **Đáp án:** z = 2.5 > 2.33: bác bỏ H0
    1. f = 150/625 = 0.24; sqrt(0.2 . 0.8/625) = 0.4/25 = 0.016; z = 0.04/0.016 = 2.5.
    2. Đối thuyết p > 0.2 là một phía: so với 2.33, không phải 2.58. 2.5 > 2.33 nên bác bỏ H0.
    3. 0.1 là quên chia n trong căn, 156.25 là quên lấy căn.
- `xs_t9_ky_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong kiểm định H0: p = 0.3 với đối thuyết H1: p > 0.3 bằng tần suất mẫu, p-giá trị bằng 0.01 có nghĩa là: nếu H0 đúng thì xác suất được một tần suất mẫu lớn ít nhất bằng tần suất đã quan sát là 0.01.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_02`, `xs_t7_pm_03`
  - **Đáp án:** Đúng
    1. Đó chính là định nghĩa p-giá trị cho đối thuyết phía phải: xác suất, tính khi H0 đúng, của một kết quả lệch về phía H1 ít nhất như kết quả đã thấy.
    2. p = 0.01 nhỏ hơn mức 5% nên bác bỏ H0 ở mức 5%; nó không phải xác suất để H0 đúng. Mệnh đề đúng.
- `xs_t9_ky_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Năm trước tỷ lệ đệ tử bỏ tu là 10%. Năm nay, trong 900 đệ tử chọn ngẫu nhiên có 117 người bỏ tu. Kiểm định ở mức ý nghĩa 5% xem tỷ lệ có tăng không (giá trị tới hạn một phía 1.645). Sắp xếp các bước.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_04`
  - **Đáp án (thứ tự đúng):**
    1. Đặt H0: p = 0.1 với đối thuyết H1: p > 0.1.
    2. Khi H0 đúng, tần suất mẫu có độ lệch chuẩn sqrt(0.1 . 0.9/900) = 0.01.
    3. Tần suất mẫu f = 117/900 = 0.13, nên z = (0.13 - 0.1)/0.01 = 3.
    4. So sánh: z = 3 > 1.645, rơi vào miền bác bỏ.
    5. Kết luận: bác bỏ H0; ở mức 5%, tỷ lệ bỏ tu đã tăng.
  - **Lời giải:**
    1. Giả thuyết trước, rồi độ lệch chuẩn tính theo p0 của H0, rồi thống kê, so sánh và kết luận.
    2. z = 3 > 1.645: bác bỏ H0.
- `xs_t9_ky_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồng xu được tung 400 lần, ra 180 lần ngửa. Kiểm định đồng xu cân đối: H0: p = 0.5 với đối thuyết H1: p != 0.5, dùng z = (f - p0)/sqrt(p0(1 - p0)/n) với f là tần suất mẫu. Giá trị tới hạn hai phía là 1.96 ở mức 5% và 2.58 ở mức 1%; hàm Laplace có Phi(2) = 0.4772.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_gh_03`
  - **Phần a** (Điền số): a) Tính z.
    - **Đáp án a:** -2
  - **Phần b** (Đúng/Sai): b) Ở mức ý nghĩa 5%, kiểm định bác bỏ H0.
    - **Đáp án b:** Đúng
  - **Phần c** (Đúng/Sai): c) Ở mức ý nghĩa 1%, kiểm định bác bỏ H0.
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Tính p-giá trị P(|Z| >= 2) với Z có phân phối N(0, 1) (số thập phân đúng).
    - **Đáp án d:** 57/1250
  - **Lời giải:**
    1. a) f = 0.45; sqrt(0.5 . 0.5/400) = 0.025; z = (0.45 - 0.5)/0.025 = -2.
    2. b) |z| = 2 > 1.96: bác bỏ H0 ở mức 5%.
    3. c) |z| = 2 < 2.58: chưa đủ cơ sở bác bỏ ở mức 1%.
    4. d) p-giá trị = 2(0.5 - Phi(2)) = 2 . 0.0228 = 0.0456: nằm giữa 0.01 và 0.05, khớp với b và c.
- `xs_g9_ty_le` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một nhà sản xuất công bố tỷ lệ p0 = 0.2. Kiểm định H0: p = 0.2 từ một mẫu ngẫu nhiên 400 phần tử, trong đó có 96 phần tử có tính chất đang xét. Tính giá trị của thống kê kiểm định z = (f - p0)/sqrt(p0(1 - p0)/n), f là tần suất mẫu (số thập phân đúng).
  - **Đáp án:** 2
    1. f = 96/400 = 0.24.
    2. Khi H0 đúng: sqrt(p0(1 - p0)/n) = sqrt(0.2 . 0.8/400) = 0.02.
    3. z = (0.24 - 0.2)/0.02 = 2.
  - **Câu hỏi:** Một nhà sản xuất công bố tỷ lệ p0 = 0.1. Kiểm định H0: p = 0.1 từ một mẫu ngẫu nhiên 400 phần tử, trong đó có 25 phần tử có tính chất đang xét. Tính giá trị của thống kê kiểm định z = (f - p0)/sqrt(p0(1 - p0)/n), f là tần suất mẫu (số thập phân đúng).
  - **Đáp án:** -5/2
    1. f = 25/400 = 0.0625.
    2. Khi H0 đúng: sqrt(p0(1 - p0)/n) = sqrt(0.1 . 0.9/400) = 0.015.
    3. z = (0.0625 - 0.1)/0.015 = -2.5.
  - **Câu hỏi:** Một nhà sản xuất công bố tỷ lệ p0 = 0.2. Kiểm định H0: p = 0.2 từ một mẫu ngẫu nhiên 400 phần tử, trong đó có 76 phần tử có tính chất đang xét. Tính giá trị của thống kê kiểm định z = (f - p0)/sqrt(p0(1 - p0)/n), f là tần suất mẫu (số thập phân đúng).
  - **Đáp án:** -1/2
    1. f = 76/400 = 0.19.
    2. Khi H0 đúng: sqrt(p0(1 - p0)/n) = sqrt(0.2 . 0.8/400) = 0.02.
    3. z = (0.19 - 0.2)/0.02 = -0.5.

### So sánh hai trung bình (`xs_t9_so_sanh_trung_binh`)

- `xs_t9_st_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai giống linh thảo có chiều cao (cm) phân phối chuẩn với độ lệch chuẩn đã biết sigma_1 = 3 và sigma_2 = 4. Đo 25 cây mỗi giống (hai mẫu độc lập), được trung bình 52 cm và 50 cm. Kiểm định H0: mu_1 = mu_2 với đối thuyết H1: mu_1 != mu_2 ở mức ý nghĩa 5% (giá trị tới hạn 1.96).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t8_tc_01`
  - **Phần a** (Điền số): a) Tính sai số chuẩn của hiệu sqrt(sigma_1^2/n_1 + sigma_2^2/n_2).
    - **Đáp án a:** 1
  - **Phần b** (Điền số): b) Tính z = (x_tb1 - x_tb2)/sqrt(sigma_1^2/n_1 + sigma_2^2/n_2).
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) Kiểm định bác bỏ H0: chiều cao trung bình hai giống khác nhau ở mức 5%.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Hai mẫu độc lập nên phương sai của hiệu là tổng hai phương sai: 9/25 + 16/25 = 1, căn bằng 1.
    2. b) z = (52 - 50)/1 = 2.
    3. c) |z| = 2 > 1.96: bác bỏ H0.
- `xs_t9_st_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Hai tổng thể có phân phối chuẩn với sigma_1 = 15 và sigma_2 = 20 đã biết. Hai mẫu độc lập, mỗi mẫu 25 phần tử, có trung bình chênh nhau 12. Kiểm định H0: mu_1 = mu_2 ở mức 5% (giá trị tới hạn hai phía 1.96). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t7_pm_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. H0: mu_1 = mu_2, H1: mu_1 != mu_2; hiệu hai trung bình mẫu là 12.
    2. Độ lệch chuẩn của từng trung bình mẫu: 15/sqrt(25) = 3 và 20/sqrt(25) = 4.
    3. Độ lệch chuẩn của hiệu hai trung bình: 3 + 4 = 7.   **<- bước sai đầu tiên**
    4. z = 12/7, khoảng 1.71 < 1.96: không bác bỏ H0.
  - **Đáp án:** Bước 3: Độ lệch chuẩn của hiệu hai trung bình: 3 + 4 = 7.
  - **Vì sao sai, và bước đúng:**
    1. Với hai biến độc lập, phương sai của hiệu là tổng hai phương sai: 9 + 16 = 25; độ lệch chuẩn của hiệu là sqrt(25) = 5, không phải 3 + 4.
    2. z = 12/5 = 2.4 > 1.96: bác bỏ H0. Cộng độ lệch chuẩn đã đổi kết luận.
- `xs_t9_st_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai tổng thể có phân phối chuẩn với cùng phương sai (chưa biết). Mẫu 1 cỡ n_1 = 5 có phương sai mẫu hiệu chỉnh s_1^2 = 10; mẫu 2 cỡ n_2 = 7 có s_2^2 = 4 (hai mẫu độc lập). Để kiểm định H0: mu_1 = mu_2 bằng phân phối Student, ta gộp hai phương sai thành s^2 = [(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2]/(n_1 + n_2 - 2). Giá trị của s^2 và số bậc tự do của thống kê t là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_03`, `xs_t8_tc_02`
    - **(đúng)** 32/5 và 10 bậc tự do
    - 7 và 10 bậc tự do
    - 32/5 và 12 bậc tự do
    - 13/2 và 12 bậc tự do
  - **Đáp án:** 32/5 và 10 bậc tự do
    1. s^2 = (4 . 10 + 6 . 4)/(5 + 7 - 2) = 64/10 = 32/5.
    2. Số bậc tự do n_1 + n_2 - 2 = 10 (mỗi mẫu mất một bậc vì đã ước lượng trung bình của nó).
    3. 7 là trung bình cộng không có trọng số; 13/2 = (5 . 10 + 7 . 4)/12 là gộp sai trọng số.
- `xs_t9_st_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai phương pháp luyện khí, mỗi phương pháp thử trên 8 đệ tử (hai mẫu độc lập); điểm có phân phối chuẩn với cùng phương sai chưa biết. Mẫu 1: x_tb1 = 25, s_1^2 = 10; mẫu 2: x_tb2 = 20, s_2^2 = 22. Kiểm định H0: mu_1 = mu_2 với đối thuyết H1: mu_1 != mu_2 ở mức 5%, biết t(14; 0.025) = 2.145 (P(T > 2.145) = 0.025 với T có phân phối Student 14 bậc tự do).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t8_tc_02`
  - **Phần a** (Điền số): a) Tính phương sai gộp s^2 = [(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2]/(n_1 + n_2 - 2).
    - **Đáp án a:** 16
  - **Phần b** (Điền số): b) Tính sai số chuẩn sqrt(s^2 (1/n_1 + 1/n_2)).
    - **Đáp án b:** 2
  - **Phần c** (Điền số): c) Tính t = (x_tb1 - x_tb2)/sqrt(s^2 (1/n_1 + 1/n_2)).
    - **Đáp án c:** 5/2
  - **Phần d** (Đúng/Sai): d) Ở mức ý nghĩa 5%, kiểm định bác bỏ H0.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) s^2 = (7 . 10 + 7 . 22)/14 = 224/14 = 16.
    2. b) sqrt(16 . (1/8 + 1/8)) = sqrt(4) = 2.
    3. c) t = (25 - 20)/2 = 2.5.
    4. d) Student 8 + 8 - 2 = 14 bậc tự do, hai phía: |t| = 2.5 > 2.145, bác bỏ H0.
- `xs_t9_st_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nhóm 1 gồm 100 đệ tử có điểm trung bình 74, độ lệch chuẩn mẫu 10; nhóm 2 gồm 75 đệ tử có điểm trung bình 70, độ lệch chuẩn mẫu 15 (hai mẫu độc lập, đủ lớn để dùng xấp xỉ chuẩn). Kiểm định ở mức 5% xem nhóm 1 có trung bình cao hơn không (giá trị tới hạn một phía 1.645). Sắp xếp các bước.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t8_gh_01`
  - **Đáp án (thứ tự đúng):**
    1. Đặt H0: mu_1 = mu_2 với đối thuyết H1: mu_1 > mu_2.
    2. Khi H0 đúng, hiệu X_tb1 - X_tb2 có kỳ vọng 0 và phương sai xấp xỉ s_1^2/n_1 + s_2^2/n_2 = 100/100 + 225/75 = 4.
    3. Sai số chuẩn của hiệu bằng sqrt(4) = 2.
    4. Thống kê z = (74 - 70)/2 = 2.
    5. z = 2 > 1.645: bác bỏ H0; ở mức 5%, nhóm 1 có trung bình cao hơn.
  - **Lời giải:**
    1. Giả thuyết, phương sai của hiệu (cộng hai phương sai), căn lấy sai số chuẩn, thống kê z, so sánh và kết luận.
    2. z = 2 > 1.645 nên bác bỏ H0.
- `xs_t9_st_06` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai nhóm đệ tử (hai mẫu độc lập, đủ lớn) có điểm trung bình 51 và 50; sai số chuẩn của hiệu hai trung bình mẫu là 2. Vì trung bình mẫu thứ nhất lớn hơn, kiểm định H0: mu_1 = mu_2 với đối thuyết H1: mu_1 > mu_2 ở mức ý nghĩa 5% (giá trị tới hạn 1.645) bác bỏ H0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_tc_03`, `xs_t7_pm_02`
  - **Đáp án:** Sai
    1. z = (51 - 50)/2 = 0.5 < 1.645: chưa đủ cơ sở bác bỏ H0.
    2. Trung bình mẫu khác nhau luôn xảy ra do ngẫu nhiên; chỉ khi chênh lệch lớn so với sai số chuẩn mới kết luận hai tổng thể khác nhau. Mệnh đề sai.
- `xs_g9_hai_trung_binh` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hai tổng thể có phân phối chuẩn với độ lệch chuẩn đã biết sigma_1 = 25, sigma_2 = 96. Hai mẫu độc lập: mẫu 1 cỡ n_1 = 25 có trung bình x_tb1 = 32.8; mẫu 2 cỡ n_2 = 64 có trung bình x_tb2 = 65.3. Kiểm định H0: mu_1 = mu_2. Tính giá trị của thống kê z = (x_tb1 - x_tb2)/sqrt(sigma_1^2/n_1 + sigma_2^2/n_2) (số thập phân đúng).
  - **Đáp án:** -5/2
    1. sigma_1^2/n_1 = 625/25 = 25; sigma_2^2/n_2 = 9216/64 = 144.
    2. Sai số chuẩn của hiệu: sqrt(25 + 144) = sqrt(169) = 13 (cộng phương sai, không cộng độ lệch chuẩn).
    3. z = (32.8 - 65.3)/13 = -32.5/13 = -2.5.
  - **Câu hỏi:** Hai tổng thể có phân phối chuẩn với độ lệch chuẩn đã biết sigma_1 = 15, sigma_2 = 20. Hai mẫu độc lập: mẫu 1 cỡ n_1 = 25 có trung bình x_tb1 = 80.2; mẫu 2 cỡ n_2 = 25 có trung bình x_tb2 = 82.7. Kiểm định H0: mu_1 = mu_2. Tính giá trị của thống kê z = (x_tb1 - x_tb2)/sqrt(sigma_1^2/n_1 + sigma_2^2/n_2) (số thập phân đúng).
  - **Đáp án:** -1/2
    1. sigma_1^2/n_1 = 225/25 = 9; sigma_2^2/n_2 = 400/25 = 16.
    2. Sai số chuẩn của hiệu: sqrt(9 + 16) = sqrt(25) = 5 (cộng phương sai, không cộng độ lệch chuẩn).
    3. z = (80.2 - 82.7)/5 = -2.5/5 = -0.5.
  - **Câu hỏi:** Hai tổng thể có phân phối chuẩn với độ lệch chuẩn đã biết sigma_1 = 9, sigma_2 = 16. Hai mẫu độc lập: mẫu 1 cỡ n_1 = 36 có trung bình x_tb1 = 69.2; mẫu 2 cỡ n_2 = 64 có trung bình x_tb2 = 64.2. Kiểm định H0: mu_1 = mu_2. Tính giá trị của thống kê z = (x_tb1 - x_tb2)/sqrt(sigma_1^2/n_1 + sigma_2^2/n_2) (số thập phân đúng).
  - **Đáp án:** 2
    1. sigma_1^2/n_1 = 81/36 = 2.25; sigma_2^2/n_2 = 256/64 = 4.
    2. Sai số chuẩn của hiệu: sqrt(2.25 + 4) = sqrt(6.25) = 2.5 (cộng phương sai, không cộng độ lệch chuẩn).
    3. z = (69.2 - 64.2)/2.5 = 5/2.5 = 2.

### So sánh hai tỷ lệ (`xs_t9_so_sanh_ty_le`)

- `xs_t9_sy_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai phương pháp luyện đan, mỗi phương pháp luyện 200 viên (hai mẫu độc lập): phương pháp A có 50 viên hỏng, phương pháp B có 30 viên hỏng. Kiểm định H0: p_1 = p_2 (tỷ lệ hỏng như nhau) với đối thuyết H1: p_1 != p_2, dùng tần suất chung f = (m_1 + m_2)/(n_1 + n_2) và z = (f_1 - f_2)/sqrt(f(1 - f)(1/n_1 + 1/n_2)).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_02`
  - **Phần a** (Điền số): a) Tính tần suất chung f.
    - **Đáp án a:** 1/5
  - **Phần b** (Điền số): b) Tính sai số chuẩn sqrt(f(1 - f)(1/n_1 + 1/n_2)).
    - **Đáp án b:** 1/25
  - **Phần c** (Điền số): c) Tính z.
    - **Đáp án c:** 5/2
  - **Phần d** (Đúng/Sai): d) Ở mức ý nghĩa 1% (giá trị tới hạn hai phía 2.58), kiểm định bác bỏ H0.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) f = (50 + 30)/(200 + 200) = 0.2.
    2. b) sqrt(0.2 . 0.8 . (1/200 + 1/200)) = sqrt(0.16 . 0.01) = 0.04.
    3. c) f_1 = 0.25, f_2 = 0.15; z = 0.1/0.04 = 2.5.
    4. d) |z| = 2.5 < 2.58: chưa đủ cơ sở bác bỏ ở mức 1% (ở mức 5%, với 1.96, thì bác bỏ).
- `xs_t9_sy_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Mẫu 1 có 100 phần tử, trong đó 50 phần tử có tính chất A; mẫu 2 có 200 phần tử, trong đó 70 phần tử có tính chất A (hai mẫu độc lập). Kiểm định H0: p_1 = p_2 ở mức 5% (giá trị tới hạn hai phía 1.96). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_04`, `xs_t8_ty_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. f_1 = 50/100 = 0.5 và f_2 = 70/200 = 0.35.
    2. Khi H0 đúng, tần suất chung f = (0.5 + 0.35)/2 = 0.425.   **<- bước sai đầu tiên**
    3. Sai số chuẩn sqrt(0.425 . 0.575 . (1/100 + 1/200)).
    4. Tính z = (f_1 - f_2)/sai số chuẩn rồi so với 1.96.
  - **Đáp án:** Bước 2: Khi H0 đúng, tần suất chung f = (0.5 + 0.35)/2 = 0.425.
  - **Vì sao sai, và bước đúng:**
    1. Hai mẫu khác cỡ: tần suất chung phải gộp số đếm, f = (50 + 70)/(100 + 200) = 0.4, không phải trung bình cộng hai tần suất.
    2. Sai số chuẩn sqrt(0.4 . 0.6 . 0.015) = sqrt(0.0036) = 0.06; z = 0.15/0.06 = 2.5 > 1.96: bác bỏ H0.
- `xs_t9_sy_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai mẫu độc lập: mẫu 1 có 150 đệ tử, 45 người đạt Trúc Cơ; mẫu 2 có 150 đệ tử, 30 người đạt Trúc Cơ. Kiểm định H0: p_1 = p_2, dùng tần suất chung f = (m_1 + m_2)/(n_1 + n_2). Tính thống kê z = (f_1 - f_2)/sqrt(f(1 - f)(1/n_1 + 1/n_2)) (số thập phân đúng).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_03`
  - **Đáp án:** 2
    1. f_1 = 0.3, f_2 = 0.2; f = 75/300 = 0.25.
    2. Sai số chuẩn sqrt(0.25 . 0.75 . (2/150)) = sqrt(0.0025) = 0.05.
    3. z = (0.3 - 0.2)/0.05 = 2.
- `xs_t9_sy_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi kiểm định H0: p_1 = p_2 từ hai mẫu độc lập, nếu H0 đúng thì hai tổng thể có chung một tỷ lệ p, và tần suất chung f = (m_1 + m_2)/(n_1 + n_2) (tổng số phần tử có tính chất chia tổng cỡ hai mẫu) được dùng để ước lượng p khi tính sai số chuẩn của f_1 - f_2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_02`, `xs_t7_ud_02`
  - **Đáp án:** Đúng
    1. Thống kê được tính khi giả sử H0 đúng; lúc đó hai mẫu là n_1 + n_2 phép thử cùng xác suất p, nên ước lượng tốt nhất của p là tần suất chung.
    2. V(f_1 - f_2) = p(1 - p)(1/n_1 + 1/n_2), thay p bằng f. Mệnh đề đúng.
- `xs_t9_sy_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khảo sát hai tông môn: 200 đệ tử tông A có 60 người biết luyện khí, 400 đệ tử tông B có 90 người biết luyện khí (hai mẫu độc lập). Kiểm định ở mức ý nghĩa 5% xem tỷ lệ ở tông A có cao hơn tông B không (giá trị tới hạn một phía 1.645). Sắp xếp các bước.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_04`
  - **Đáp án (thứ tự đúng):**
    1. Đặt H0: p_1 = p_2 với đối thuyết H1: p_1 > p_2.
    2. Tần suất từng mẫu: f_1 = 60/200 = 0.3, f_2 = 90/400 = 0.225.
    3. Khi H0 đúng, gộp hai mẫu: tần suất chung f = (60 + 90)/(200 + 400) = 0.25, nằm giữa f_1 và f_2.
    4. Sai số chuẩn sqrt(0.25 . 0.75 . (1/200 + 1/400)) = 0.0375.
    5. z = (0.3 - 0.225)/0.0375 = 2 > 1.645: bác bỏ H0.
  - **Lời giải:**
    1. Giả thuyết, các tần suất, tần suất chung khi H0 đúng, sai số chuẩn, rồi z và kết luận.
    2. 0.25 . 0.75 . 0.0075 = 0.00140625, căn bằng 0.0375.
- `xs_t9_sy_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai mẫu độc lập, mỗi mẫu 300 người: mẫu 1 có 135 người, mẫu 2 có 105 người ủng hộ một môn quy mới. Kiểm định H0: p_1 = p_2 với tần suất chung f = (m_1 + m_2)/(n_1 + n_2) và z = (f_1 - f_2)/sqrt(f(1 - f)(1/n_1 + 1/n_2)). Ghép mỗi đại lượng với giá trị của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t8_ty_01`, `xs_t8_ty_03`
  - **Đáp án (ghép đúng):**
    - f_1 — 0.45
    - f_2 — 0.35
    - Tần suất chung f — 0.4
    - Sai số chuẩn sqrt(f(1 - f)(1/n_1 + 1/n_2)) — 0.04
    - Thống kê z — 2.5
  - **Lời giải:**
    1. f_1 = 135/300 = 0.45, f_2 = 105/300 = 0.35, f = 240/600 = 0.4.
    2. Sai số chuẩn sqrt(0.4 . 0.6 . 2/300) = sqrt(0.0016) = 0.04.
    3. z = 0.1/0.04 = 2.5.

## Tầng 10: Tài Năng: hàm của biến ngẫu nhiên, tương quan và hồi quy

55 dạng câu (49 câu viết tay, 6 bộ sinh câu); 55 chưa duyệt.

### Hàm của biến ngẫu nhiên (`xs_t10_ham_bien_ngau_nhien`)

- `xs_t10_hb_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị -1, 0, 1, 2, 3 với xác suất lần lượt 1/10, 2/5, 1/5, 1/10, 1/5. Đặt Y = (X - 1)^2. Tính P(Y = 1). Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_bp_01`, `xs_t6_kv_05`
  - **Đáp án:** 1/2
    1. Y = (X - 1)^2 nhận các giá trị: X = -1 cho 4, X = 0 cho 1, X = 1 cho 0, X = 2 cho 1, X = 3 cho 4.
    2. Y = 1 xảy ra khi X = 0 hoặc X = 2: hai giá trị khác nhau của X cho cùng một giá trị của Y, nên phải cộng xác suất.
    3. P(Y = 1) = P(X = 0) + P(X = 2) = 2/5 + 1/10 = 1/2. Viết P(Y = 1) = P(X = 1) = 1/5 là nhầm Y = 1 với X = 1.
- `xs_t10_hb_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị 0, 1, 2 với xác suất lần lượt 1/2, 1/3, 1/6. Giá trị của E(X^2) là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_kv_06`, `xs_t6_kv_01`
    - **(đúng)** 1
    - 4/9
    - 5/3
    - 2/3
  - **Đáp án:** 1
    1. E(g(X)) = tổng của g(x) P(X = x): E(X^2) = 0 . 1/2 + 1 . 1/3 + 4 . 1/6 = 1/3 + 2/3 = 1.
    2. 4/9 = (E(X))^2 với E(X) = 2/3: nhầm E(g(X)) với g(E(X)), hai số này nói chung khác nhau (hiệu E(X^2) - (E(X))^2 chính là V(X)).
    3. 5/3 = (0 + 1 + 4)/3: lấy trung bình các giá trị x^2 mà quên trọng số xác suất.
    4. 2/3 = E(X): tính kỳ vọng của X thay vì của X^2.
- `xs_t10_hb_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có phân phối đều trên (0, 1), tức mật độ f_X(x) = 1 với 0 < x < 1 và bằng 0 nơi khác. Khi đó Y = 2X + 1 có mật độ f_Y(y) = 1/2 với 1 < y < 3 và bằng 0 nơi khác.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_md_07`, `xs_g5_mat_do_tf`
  - **Đáp án:** Đúng
    1. Hàm phân phối: F_Y(y) = P(2X + 1 < y) = P(X < (y - 1)/2) = (y - 1)/2 với 1 < y < 3.
    2. Đạo hàm: f_Y(y) = 1/2 trên (1, 3). Tổng quát Y = aX + b (a khác 0) có mật độ f_X((y - b)/a)/|a|: đoạn dài ra gấp |a| lần nên mật độ giảm |a| lần để tổng xác suất vẫn bằng 1.
    3. Mệnh đề đúng.
- `xs_t10_hb_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X là biến ngẫu nhiên liên tục có mật độ f_X và Y = X^2. Khi đó với mọi y > 0, mật độ của Y là f_Y(y) = f_X(sqrt(y)).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_md_07`, `xs_t5_hp_07`
  - **Đáp án:** Sai
    1. Hai chỗ sai: giá trị y có hai nguồn là X = sqrt(y) và X = -sqrt(y), và phép đổi biến phải nhân thêm 1/(2 sqrt(y)) (đạo hàm của sqrt(y)).
    2. Đúng là f_Y(y) = (f_X(sqrt(y)) + f_X(-sqrt(y)))/(2 sqrt(y)) với y > 0. Ví dụ X đều trên (-1, 1): f_Y(y) = 1/(2 sqrt(y)) trên (0, 1), còn f_X(sqrt(y)) = 1/2 không là mật độ của Y (tích phân 1/2 trên (0, 1) chỉ bằng 1/2).
    3. Mệnh đề sai.
- `xs_t10_hb_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: X có phân phối đều trên (-1, 1) và Y = X^2. Tìm mật độ của Y. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_md_05`, `xs_t5_xk_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. X có mật độ 1/2 trên (-1, 1), nên Y = X^2 nhận giá trị trong (0, 1).
    2. Với 0 < y < 1: F_Y(y) = P(X^2 < y) = P(X < sqrt(y)).   **<- bước sai đầu tiên**
    3. P(X < sqrt(y)) = (sqrt(y) + 1)/2.
    4. Đạo hàm: f_Y(y) = 1/(4 sqrt(y)) với 0 < y < 1.
  - **Đáp án:** Bước 2: Với 0 < y < 1: F_Y(y) = P(X^2 < y) = P(X < sqrt(y)).
  - **Vì sao sai, và bước đúng:**
    1. X^2 < y tương đương -sqrt(y) < X < sqrt(y): phải lấy cả hai phía của 0, không chỉ X < sqrt(y).
    2. Đúng: F_Y(y) = P(-sqrt(y) < X < sqrt(y)) = 2 sqrt(y)/2 = sqrt(y), nên f_Y(y) = 1/(2 sqrt(y)) trên (0, 1).
    3. Kiểm tra bằng tích phân: mật độ 1/(4 sqrt(y)) chỉ có tổng xác suất 1/2, không thể đúng.
- `xs_t10_hb_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối đều trên (0, 1) và Y = X^2. Sắp xếp các bước tìm mật độ của Y bằng cách lập hàm phân phối.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_hp_05`, `xs_t5_md_01`
  - **Đáp án (thứ tự đúng):**
    1. Y nhận giá trị trong (0, 1); với 0 < y < 1 viết F_Y(y) = P(Y < y) = P(X^2 < y).
    2. Vì X > 0 nên X^2 < y tương đương X < sqrt(y).
    3. P(X < sqrt(y)) = sqrt(y), do X đều trên (0, 1).
    4. Lấy đạo hàm theo y: f_Y(y) = 1/(2 sqrt(y)) với 0 < y < 1.
    5. Kiểm tra: tích phân của 1/(2 sqrt(y)) trên (0, 1) bằng sqrt(1) - sqrt(0) = 1.
  - **Lời giải:**
    1. Cách làm chung: đưa sự kiện về biến cũ (X^2 < y thành X < sqrt(y)), tính xác suất để có F_Y, rồi đạo hàm để có f_Y.
    2. Bước kiểm tra cuối dùng chính tính chất của mật độ: tích phân bằng 1.
- `xs_t10_hb_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối đều trên (0, 1). Ghép mỗi biến Y với phân phối của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_dm_03`, `xs_t5_md_05`
  - **Đáp án (ghép đúng):**
    - Y = 2X + 1 — Đều trên (1, 3), mật độ 1/2
    - Y = 1 - X — Đều trên (0, 1), cùng phân phối với X
    - Y = X^2 — Mật độ 1/(2 sqrt(y)) trên (0, 1)
    - Y = -ln(X) — Phân phối mũ với tham số 1
  - **Lời giải:**
    1. Y = 2X + 1: F_Y(y) = (y - 1)/2 trên (1, 3). Y = 1 - X: P(1 - X < y) = P(X > 1 - y) = y.
    2. Y = X^2: F_Y(y) = sqrt(y), đạo hàm 1/(2 sqrt(y)).
    3. Y = -ln(X): P(Y > y) = P(X < e^(-y)) = e^(-y), tức F_Y(y) = 1 - e^(-y), là phân phối mũ tham số 1.
- `xs_t10_hb_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị -2, -1, 0, 1, 2 với xác suất lần lượt 1/10, 1/5, 3/10, 1/5, 1/5. Đặt Y = X^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_08`, `xs_t6_kv_05`
  - **Phần a** (Điền số): a) Tính P(Y = 1).
    - **Đáp án a:** 2/5
  - **Phần b** (Điền số): b) Tính E(Y).
    - **Đáp án b:** 8/5
  - **Phần c** (Điền số): c) Tính V(Y).
    - **Đáp án c:** 66/25
  - **Phần d** (Đúng/Sai): d) E(Y) = (E(X))^2.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) Y = 1 khi X = -1 hoặc X = 1: P(Y = 1) = 1/5 + 1/5 = 2/5. Cả bảng của Y: P(Y = 0) = 3/10, P(Y = 1) = 2/5, P(Y = 4) = 1/10 + 1/5 = 3/10.
    2. b) E(Y) = 0 . 3/10 + 1 . 2/5 + 4 . 3/10 = 2/5 + 6/5 = 8/5 (cũng bằng E(X^2) tính trực tiếp từ bảng của X).
    3. c) E(Y^2) = 1 . 2/5 + 16 . 3/10 = 26/5; V(Y) = 26/5 - (8/5)^2 = 130/25 - 64/25 = 66/25.
    4. d) E(X) = -2/10 - 2/10 + 0 + 2/10 + 4/10 = 1/5 nên (E(X))^2 = 1/25, khác 8/5: E(g(X)) khác g(E(X)).
- `xs_t10_hb_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X có mật độ f_X(x) = 2x với 0 < x < 1 và bằng 0 nơi khác. Đặt Y = X^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_md_08`, `xs_t5_xk_08`
  - **Phần a** (Điền số): a) Tính P(X < 1/2).
    - **Đáp án a:** 1/4
  - **Phần b** (Điền số): b) Tính P(Y < 1/4).
    - **Đáp án b:** 1/4
  - **Phần c** (Trắc nghiệm): c) Phân phối của Y là
    - **(đúng)** Đều trên (0, 1)
    - Mật độ 2y trên (0, 1), giống X
    - Mật độ 2 sqrt(y) trên (0, 1)
    - Mật độ 1/(2 sqrt(y)) trên (0, 1)
    - **Đáp án c:** Đều trên (0, 1)
  - **Phần d** (Điền số): d) Tính E(Y).
    - **Đáp án d:** 1/2
  - **Lời giải:**
    1. a) P(X < 1/2) = tích phân của 2x từ 0 đến 1/2 = (1/2)^2 = 1/4.
    2. b) Vì X > 0: Y < 1/4 tương đương X < 1/2, nên P(Y < 1/4) = 1/4. Tổng quát F_Y(y) = P(X < sqrt(y)) = (sqrt(y))^2 = y.
    3. c) F_Y(y) = y trên (0, 1) là hàm phân phối của phân phối đều. 2y là mật độ của X (nhầm Y cùng luật với X); 2 sqrt(y) là f_X(sqrt(y)) thiếu thừa số 1/(2 sqrt(y)); 1/(2 sqrt(y)) là mật độ của X^2 khi X đều, không phải khi f_X = 2x.
    4. d) E(Y) = E(X^2) = tích phân của x^2 . 2x từ 0 đến 1 = 1/2, khớp với kỳ vọng 1/2 của phân phối đều trên (0, 1).
- `xs_t10_hb_10` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X có phân phối chuẩn N(0, 1) và Y = X^2. Biết hàm Laplace Phi(1) = 0.3413 (Phi(x) là tích phân của mật độ N(0, 1) từ 0 đến x). P(Y < 1) bằng
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ch_06`, `xs_t6_ch_01`
    - **(đúng)** 0.6826
    - 0.3413
    - 0.8413
    - 0.1587
  - **Đáp án:** 0.6826
    1. Y < 1 tương đương -1 < X < 1, nên P(Y < 1) = Phi(1) - Phi(-1) = 2 Phi(1) = 0.6826.
    2. 0.3413 chỉ là P(0 < X < 1): quên nhánh X âm.
    3. 0.8413 = 0.5 + Phi(1) là P(X < 1): quên cận dưới X > -1.
    4. 0.1587 = 0.5 - Phi(1) là P(X > 1).
- `xs_g10_ham_roi_rac` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị -3, -2, 0, 2 với xác suất lần lượt 1/20, 13/20, 3/20, 3/20. Đặt Y = X^2. Tính P(Y = 4). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 4/5
    1. Giá trị của Y: X = -3 cho 9, X = -2 cho 4, X = 0 cho 0, X = 2 cho 4.
    2. Y = 4 xảy ra khi X = -2 hoặc X = 2: các giá trị khác nhau của X cho cùng một giá trị của Y thì cộng xác suất.
    3. P(Y = 4) = 13/20 + 3/20 = 4/5.
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị -3, -2, -1, 4 với xác suất lần lượt 7/20, 1/10, 1/20, 1/2. Đặt Y = (X + 2)^2. Tính E(Y). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 92/5
    1. Giá trị của Y: X = -3 cho 1, X = -2 cho 0, X = -1 cho 1, X = 4 cho 36.
    2. E(Y) = tổng của g(x) P(X = x): lấy giá trị của Y ở từng x nhân với xác suất của chính x đó (không cần lập bảng của Y).
    3. E(Y) = 1 . 7/20 + 0 . 1/10 + 1 . 1/20 + 36 . 1/2 = 92/5.
  - **Câu hỏi:** Biến ngẫu nhiên X nhận các giá trị -1, 0, 1, 4 với xác suất lần lượt 1/20, 1/10, 4/5, 1/20. Đặt Y = |X - 1|. Tính E(Y). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/20
    1. Giá trị của Y: X = -1 cho 2, X = 0 cho 1, X = 1 cho 0, X = 4 cho 3.
    2. E(Y) = tổng của g(x) P(X = x): lấy giá trị của Y ở từng x nhân với xác suất của chính x đó (không cần lập bảng của Y).
    3. E(Y) = 2 . 1/20 + 1 . 1/10 + 0 . 4/5 + 3 . 1/20 = 7/20.

### Vectơ ngẫu nhiên hai chiều (`xs_t10_vecto_ngau_nhien`)

- `xs_t10_vt_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai biến ngẫu nhiên X (nhận 0, 1) và Y (nhận 0, 1, 2) có bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng 1 ứng với X = 0, hàng 2 ứng với X = 1; cột 1, 2, 3 ứng với Y = 0, 1, 2. Ô a chưa biết. Tính P(Y = 1). Nhập một số hoặc phân số tối giản.
  - P = (1/10, a, 1/10); (1/5, 1/10, 3/10)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t5_bp_01`, `xs_t5_bn_07`
  - **Đáp án:** 3/10
    1. Tổng mọi ô bằng 1: a = 1 - (1/10 + 1/10 + 1/5 + 1/10 + 3/10) = 1 - 4/5 = 1/5.
    2. P(Y = 1) là phân phối biên của Y tại 1: cộng cả cột 2, gồm hai ô P(X = 0, Y = 1) = a và P(X = 1, Y = 1) = 1/10.
    3. P(Y = 1) = 1/5 + 1/10 = 3/10. (Chỉ lấy ô a = 1/5 là bỏ quên trường hợp X = 1.)
- `xs_t10_vt_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với giá trị của X, cột ứng với giá trị của Y. X nhận 0, 1 (hai hàng), Y nhận 0, 1, 2 (ba cột). Xác suất P(Y = 1 | X = 0) bằng
  - P = (1/12, 1/6, 1/12); (1/4, 1/12, 1/3)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dk_05`, `xs_t5_bn_07`
    - **(đúng)** 1/2
    - 1/6
    - 2/3
    - 1/3
  - **Đáp án:** 1/2
    1. P(Y = 1 | X = 0) = P(X = 0, Y = 1)/P(X = 0) = (1/6)/(1/3) = 1/2, với P(X = 0) là tổng hàng 1: 1/12 + 1/6 + 1/12 = 1/3.
    2. 1/6 là ô P(X = 0, Y = 1) chưa chia cho P(X = 0).
    3. 2/3 = (1/6)/(1/4) là P(X = 0 | Y = 1): chia cho tổng cột thay vì tổng hàng, tức đổi chỗ điều kiện.
    4. 1/3 là P(X = 0), một xác suất biên.
- `xs_t10_vt_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với giá trị của X, cột ứng với giá trị của Y. X và Y độc lập.
  - P = (1/6, 1/12, 1/12); (1/3, 1/6, 1/6)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dl_07`, `xs_t5_bp_07`
  - **Đáp án:** Đúng
    1. Phân phối biên: P(X = 0) = 1/3, P(X = 1) = 2/3; P(Y = 0) = 1/2, P(Y = 1) = 1/4, P(Y = 2) = 1/4.
    2. Cả sáu ô đều bằng tích hai xác suất biên của nó: 1/3 . 1/2 = 1/6, 1/3 . 1/4 = 1/12, 2/3 . 1/2 = 1/3, 2/3 . 1/4 = 1/6.
    3. Độc lập đòi hỏi mọi ô thoả công thức tích, và ở đây đều thoả: mệnh đề đúng.
- `xs_t10_vt_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với giá trị của X, cột ứng với giá trị của Y. Hỏi X (hai hàng) và Y (ba cột) có độc lập không. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - P = (1/6, 1/4, 1/12); (1/6, 1/12, 1/4)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_g3_doc_lap_tf`, `xs_t5_bp_07`
  - **Lời giải đưa ra (có một bước sai):**
    1. Cộng hàng: P(X = 0) = P(X = 1) = 1/2. Cộng cột: P(Y = 0) = P(Y = 1) = P(Y = 2) = 1/3.
    2. Ô đầu tiên: P(X = 0, Y = 0) = 1/6 và P(X = 0) P(Y = 0) = 1/2 . 1/3 = 1/6, bằng nhau.
    3. Vậy công thức tích P(X = i, Y = j) = P(X = i) P(Y = j) thoả, nên X và Y độc lập.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Vậy công thức tích P(X = i, Y = j) = P(X = i) P(Y = j) thoả, nên X và Y độc lập.
  - **Vì sao sai, và bước đúng:**
    1. Độc lập đòi hỏi công thức tích đúng với mọi ô; một ô thoả không chứng minh được gì (một ô vi phạm là đủ để bác bỏ).
    2. Ô P(X = 0, Y = 1) = 1/4 nhưng P(X = 0) P(Y = 1) = 1/2 . 1/3 = 1/6: không bằng, nên X và Y không độc lập.
- `xs_t10_vt_05` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời của (X, Y) có hàng ứng với giá trị của X, cột ứng với giá trị của Y. Ghép mỗi đối tượng với cách đọc nó từ bảng.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dk_08`, `xs_t5_bn_06`
  - **Đáp án (ghép đúng):**
    - Phân phối biên của X — Cộng các ô trên mỗi hàng
    - Phân phối biên của Y — Cộng các ô trên mỗi cột
    - P(Y = j | X = i) — Ô (i, j) chia cho tổng của hàng i
    - X và Y độc lập — Mọi ô bằng tích xác suất biên của hàng và của cột chứa nó
  - **Lời giải:**
    1. Phân phối biên là xác suất của một biến khi bỏ qua biến kia, nên cộng theo biến bị bỏ: cộng trên hàng được biên của X, cộng trên cột được biên của Y.
    2. Xác suất có điều kiện thu hẹp về hàng i (điều kiện X = i), nên chia cho tổng của hàng i, không phải của cột j.
    3. Độc lập: P(X = i, Y = j) = P(X = i) P(Y = j) với mọi i, j.
- `xs_t10_vt_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với giá trị của X, cột ứng với giá trị của Y. X và Y đều nhận hai giá trị 0, 1. Sắp xếp các bước kiểm tra X và Y có độc lập không.
  - P = (1/8, 1/8); (3/8, 3/8)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dl_06`, `xs_t5_bp_07`
  - **Đáp án (thứ tự đúng):**
    1. Cộng từng hàng: P(X = 0) = 1/4, P(X = 1) = 3/4.
    2. Cộng từng cột: P(Y = 0) = 1/2, P(Y = 1) = 1/2.
    3. Với mỗi ô tính tích hai xác suất biên của nó: 1/4 . 1/2 = 1/8 ở hàng 1 và 3/4 . 1/2 = 3/8 ở hàng 2.
    4. So từng ô của bảng với tích của nó: cả bốn ô đều bằng.
    5. Kết luận: X và Y độc lập.
  - **Lời giải:**
    1. Phải có hai biên trước mới có tích; phải có tích của mọi ô trước mới so được; kết luận sau cùng.
    2. Nếu một ô lệch thì dừng và kết luận không độc lập; ở đây cả bốn ô đều khớp.
- `xs_t10_vt_07` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai biến ngẫu nhiên X (nhận 0, 1) và Y (nhận 0, 1, 2) có bảng phân phối đồng thời ở ma trận P: hàng 1 ứng với X = 0, hàng 2 ứng với X = 1; cột 1, 2, 3 ứng với Y = 0, 1, 2. Ô a chưa biết.
  - P = (1/10, 1/5, a); (1/5, 1/10, 3/10)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_g5_bang_thieu`, `xs_t5_bp_08`
  - **Phần a** (Điền số): a) Tìm a.
    - **Đáp án a:** 1/10
  - **Phần b** (Điền số): b) Tính P(X + Y = 2).
    - **Đáp án b:** 1/5
  - **Phần c** (Điền số): c) Tính P(Y = 1 | X = 0).
    - **Đáp án c:** 1/2
  - **Phần d** (Đúng/Sai): d) X và Y độc lập.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) Tổng các ô bằng 1: a = 1 - (1/10 + 1/5 + 1/5 + 1/10 + 3/10) = 1/10.
    2. b) X + Y = 2 xảy ra ở hai ô (X = 0, Y = 2) và (X = 1, Y = 1): 1/10 + 1/10 = 1/5.
    3. c) P(X = 0) = 1/10 + 1/5 + 1/10 = 2/5; P(Y = 1 | X = 0) = (1/5)/(2/5) = 1/2.
    4. d) P(X = 0) P(Y = 0) = 2/5 . 3/10 = 3/25 khác P(X = 0, Y = 0) = 1/10: một ô lệch là đủ, X và Y không độc lập.
- `xs_t10_vt_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai biến ngẫu nhiên X (nhận 0, 1, 2) và Y (nhận 0, 1) có bảng phân phối đồng thời ở ma trận P: hàng 1, 2, 3 ứng với X = 0, 1, 2; cột 1, 2 ứng với Y = 0, 1.
  - P = (1/4, 1/8); (1/8, 1/4); (1/8, 1/8)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dk_05`, `xs_t5_bp_08`
  - **Phần a** (Điền số): a) Tính P(X = 1).
    - **Đáp án a:** 3/8
  - **Phần b** (Điền số): b) Tính P(X = 0 | Y = 1).
    - **Đáp án b:** 1/4
  - **Phần c** (Đúng/Sai): c) P(Y = 1 | X = 2) = P(Y = 1).
    - **Đáp án c:** Đúng
  - **Phần d** (Đúng/Sai): d) X và Y độc lập.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) P(X = 1) = 1/8 + 1/4 = 3/8 (tổng hàng 2).
    2. b) P(Y = 1) = 1/8 + 1/4 + 1/8 = 1/2; P(X = 0 | Y = 1) = (1/8)/(1/2) = 1/4.
    3. c) P(Y = 1 | X = 2) = (1/8)/(1/4) = 1/2 = P(Y = 1): đúng, nhưng chỉ cho hàng X = 2.
    4. d) Độc lập đòi hỏi điều đó cho mọi hàng: ở hàng X = 0, P(Y = 1 | X = 0) = (1/8)/(3/8) = 1/3 khác 1/2. Một điều kiện đúng ở một hàng không đủ để độc lập.
- `xs_t10_vt_09` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai biến X và Y cùng nhận hai giá trị 0, 1, cả hai đều có P(0) = P(1) = 1/2. Biết hai phân phối biên này là đủ để suy ra duy nhất bảng phân phối đồng thời của (X, Y).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_dl_07`, `xs_t5_bn_06`
  - **Đáp án:** Sai
    1. Hai bảng khác nhau cùng có các biên đó: bảng độc lập với mọi ô bằng 1/4, và bảng [[1/2, 0], [0, 1/2]] (X = Y).
    2. Phân phối biên chỉ cho tổng theo hàng và theo cột; cách chia từng tổng vào các ô (mức phụ thuộc giữa X và Y) là thông tin thêm. Chỉ khi biết thêm X và Y độc lập thì tích hai biên mới cho bảng.
    3. Mệnh đề sai.
- `xs_g10_bang_bien` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của hai biến ngẫu nhiên ở ma trận P: hàng ứng với X = 0, 1, 2, cột ứng với Y = 0, 1. Tính P(X = 0 | Y = 0). Nhập một số hoặc phân số tối giản.
  - P = (1/6, 5/24); (1/4, 1/24); (5/24, 1/8)  (từng hàng)
  - **Đáp án:** 4/15
    1. P(Y = 0) = tổng cột Y = 0 = 5/8.
    2. P(X = 0 | Y = 0) = P(X = 0, Y = 0)/P(Y = 0) = 1/6/5/8 = 4/15.
    3. Chia cho tổng của cột chứa điều kiện, không chia cho tổng của hàng.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của hai biến ngẫu nhiên ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1, 2. Tính P(Y = 2 | X = 0). Nhập một số hoặc phân số tối giản.
  - P = (1/8, 1/8, 1/6); (1/12, 5/12, 1/12)  (từng hàng)
  - **Đáp án:** 2/5
    1. P(X = 0) = tổng hàng X = 0 = 5/12.
    2. P(Y = 2 | X = 0) = P(X = 0, Y = 2)/P(X = 0) = 1/6/5/12 = 2/5.
    3. Chia cho tổng của hàng chứa điều kiện, không chia cho tổng của cột.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của hai biến ngẫu nhiên ở ma trận P: hàng ứng với X = 0, 1, 2, cột ứng với Y = 0, 1. Tính P(X = 2). Nhập một số hoặc phân số tối giản.
  - P = (2/5, 2/15); (1/10, 1/30); (1/30, 3/10)  (từng hàng)
  - **Đáp án:** 1/3
    1. Phân phối biên của X: cộng các ô trên hàng X = 2.
    2. P(X = 2) = 1/30 + 3/10 = 1/3.
- `xs_g10_doc_lap_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1, 2. X và Y độc lập.
  - P = (1/12, 1/4, 1/6); (1/12, 1/4, 1/6)  (từng hàng)
  - **Đáp án:** Đúng
    1. Phân phối biên: P(X = 0) = 1/2, P(X = 1) = 1/2; P(Y = 0) = 1/6, P(Y = 1) = 1/2, P(Y = 2) = 1/3.
    2. Cả sáu ô đều bằng tích hai xác suất biên của nó, nên X và Y độc lập. Mệnh đề đúng.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1, 2. X và Y độc lập.
  - P = (1/8, 0, 1/8); (1/24, 1/3, 3/8)  (từng hàng)
  - **Đáp án:** Sai
    1. Phân phối biên: P(X = 0) = 1/4, P(X = 1) = 3/4; P(Y = 0) = 1/6, P(Y = 1) = 1/3, P(Y = 2) = 1/2.
    2. Ô (X = 0, Y = 0): P(X = 0) P(Y = 0) = 1/24 nhưng P(X = 0, Y = 0) = 1/8. Một ô lệch là đủ để kết luận X và Y không độc lập (kiểm tra mọi ô, không chỉ một ô). Mệnh đề sai.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1, 2. X và Y độc lập.
  - P = (1/8, 1/16, 1/16); (3/8, 3/16, 3/16)  (từng hàng)
  - **Đáp án:** Đúng
    1. Phân phối biên: P(X = 0) = 1/4, P(X = 1) = 3/4; P(Y = 0) = 1/2, P(Y = 1) = 1/4, P(Y = 2) = 1/4.
    2. Cả sáu ô đều bằng tích hai xác suất biên của nó, nên X và Y độc lập. Mệnh đề đúng.

### Hiệp phương sai và hệ số tương quan (`xs_t10_tuong_quan`)

- `xs_t10_tq_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng 1, 2 ứng với X = 0, 1; cột 1, 2, 3 ứng với Y = 0, 1, 2. Tính hiệp phương sai Cov(X, Y). Nhập một số hoặc phân số tối giản.
  - P = (1/4, 1/6, 1/12); (1/12, 1/6, 1/4)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t5_bn_07`
  - **Đáp án:** 1/6
    1. E(X) = P(X = 1) = 1/12 + 1/6 + 1/4 = 1/2. Cột: P(Y = 0) = P(Y = 1) = P(Y = 2) = 1/3, nên E(Y) = 1/3 + 2/3 = 1.
    2. E(XY) chỉ cộng các ô có X = 1 (X = 0 cho tích 0): 1 . 1 . 1/6 + 1 . 2 . 1/4 = 1/6 + 1/2 = 2/3.
    3. Cov(X, Y) = E(XY) - E(X) E(Y) = 2/3 - 1/2 . 1 = 1/6.
- `xs_t10_tq_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai biến ngẫu nhiên X, Y có V(X) = 4, V(Y) = 9 và Cov(X, Y) = -3. Tính hệ số tương quan rho(X, Y) = Cov(X, Y)/(sigma_X sigma_Y). Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_phuong_sai`
  - **Đáp án:** -1/2
    1. Độ lệch chuẩn: sigma_X = sqrt(4) = 2, sigma_Y = sqrt(9) = 3.
    2. rho = -3/(2 . 3) = -1/2. Chia cho tích hai độ lệch chuẩn, không phải tích hai phương sai (-3/36).
- `xs_t10_tq_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu Cov(X, Y) = 0 thì X và Y độc lập.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_g3_doc_lap_tf`, `xs_t6_ps_07`
  - **Đáp án:** Sai
    1. Phản ví dụ: X nhận -1, 0, 1 với xác suất 1/3 mỗi giá trị, Y = X^2. Khi đó E(X) = 0 và E(XY) = E(X^3) = 0, nên Cov(X, Y) = 0.
    2. Nhưng Y xác định hoàn toàn bởi X: P(X = 1, Y = 0) = 0 khác P(X = 1) P(Y = 0) = 1/9. Hiệp phương sai chỉ đo quan hệ tuyến tính.
    3. Chiều ngược lại đúng: độc lập thì Cov = 0. Mệnh đề đang xét sai.
- `xs_t10_tq_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với hai biến ngẫu nhiên bất kỳ X, Y có phương sai hữu hạn, V(X + Y) = V(X) + V(Y) + 2 Cov(X, Y).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_bien_doi`
  - **Đáp án:** Đúng
    1. V(X + Y) = E[(X - E(X) + Y - E(Y))^2] = V(X) + V(Y) + 2 E[(X - E(X))(Y - E(Y))].
    2. Số hạng cuối là 2 Cov(X, Y). Khi X, Y độc lập thì Cov = 0 và còn lại V(X) + V(Y). Mệnh đề đúng.
- `xs_t10_tq_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** V(X) = 3, V(Y) = 5 và Cov(X, Y) = 1. Giá trị của V(2X - Y) là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_bien_doi`
    - **(đúng)** 13
    - 17
    - 21
    - 3
  - **Đáp án:** 13
    1. V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y). Với a = 2, b = -1: 4 . 3 + 5 + 2 . 2 . (-1) . 1 = 12 + 5 - 4 = 13.
    2. 17 = 12 + 5 bỏ qua hiệp phương sai, tức coi X và Y độc lập.
    3. 21 = 12 + 5 + 4: sai dấu của số hạng chéo (hệ số của Y là -1 nên 2ab = -4).
    4. 3 = 12 - 5 - 4: coi V(-Y) = -V(Y), trong khi V(-Y) = (-1)^2 V(Y) = V(Y).
- `xs_t10_tq_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Bảng phân phối đồng thời của (X, Y) ở ma trận P: hàng 1, 2 ứng với X = 0, 1; cột 1, 2 ứng với Y = 0, 1. Tính Cov(X, Y). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - P = (1/3, 1/6); (1/6, 1/3)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t5_bn_07`
  - **Lời giải đưa ra (có một bước sai):**
    1. E(X) = 1/2 và E(Y) = 1/2 (cộng hàng, cộng cột).
    2. E(XY) = E(X) E(Y) = 1/4.   **<- bước sai đầu tiên**
    3. Cov(X, Y) = E(XY) - E(X) E(Y) = 1/4 - 1/4 = 0.
    4. Cov = 0 nên X và Y không tương quan.
  - **Đáp án:** Bước 2: E(XY) = E(X) E(Y) = 1/4.
  - **Vì sao sai, và bước đúng:**
    1. E(XY) = E(X) E(Y) chỉ đúng khi X, Y không tương quan (chẳng hạn độc lập); ở đây phải tính từ bảng, không được giả sử.
    2. E(XY) = tổng của i j P(X = i, Y = j) = 1 . 1 . 1/3 = 1/3 (chỉ ô X = 1, Y = 1 khác 0 ở tích).
    3. Cov(X, Y) = 1/3 - 1/4 = 1/12, khác 0: X và Y có tương quan dương.
- `xs_t10_tq_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi tình huống với hệ số tương quan tương ứng.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_bien_doi`
  - **Đáp án (ghép đúng):**
    - Y = 5X + 1 — rho(X, Y) = 1
    - Y = -X/2 + 3 — rho(X, Y) = -1
    - X và Y độc lập, cả hai có phương sai dương — rho(X, Y) = 0
    - Biết rho(X, Y) = 0.6, và Z = -2Y — rho(X, Z) = -0.6
  - **Lời giải:**
    1. Y = aX + b với a > 0 cho rho = 1, với a < 0 cho rho = -1 (độ lớn của a không ảnh hưởng, chỉ dấu).
    2. Độc lập suy ra Cov = 0 nên rho = 0.
    3. Nhân Y với số âm đổi dấu hiệp phương sai nhưng giữ nguyên tỉ số với độ lệch chuẩn: rho(X, Z) = -rho(X, Y).
- `xs_t10_tq_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời của (X, Y) ở ma trận P: hàng 1, 2 ứng với X = 0, 1; cột 1, 2 ứng với Y = 0, 1. Sắp xếp các bước tính hệ số tương quan rho(X, Y).
  - P = (1/2, 1/8); (1/8, 1/4)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_t5_bn_07`
  - **Đáp án (thứ tự đúng):**
    1. Cộng hàng và cột: P(X = 1) = P(Y = 1) = 3/8, nên E(X) = E(Y) = 3/8.
    2. E(XY) chỉ có ô (X = 1, Y = 1) khác 0 ở tích: E(XY) = 1/4.
    3. Cov(X, Y) = E(XY) - E(X) E(Y) = 1/4 - 9/64 = 7/64.
    4. V(X) = V(Y) = 3/8 . 5/8 = 15/64 (biến chỉ nhận 0 và 1).
    5. rho = Cov/sqrt(V(X) V(Y)) = (7/64)/(15/64) = 7/15.
  - **Lời giải:**
    1. Tính kỳ vọng trước, rồi E(XY), rồi hiệp phương sai, rồi phương sai, cuối cùng mới chia ra hệ số tương quan.
    2. rho = 7/15 nằm giữa 0 và 1: tương quan dương vừa phải.
- `xs_t10_tq_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời của (X, Y) ở ma trận P: hàng 1, 2 ứng với X = 0, 1; cột 1, 2 ứng với Y = 0, 1.
  - P = (3/8, 1/8); (1/8, 3/8)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_phuong_sai`
  - **Phần a** (Điền số): a) Tính E(XY).
    - **Đáp án a:** 3/8
  - **Phần b** (Điền số): b) Tính Cov(X, Y).
    - **Đáp án b:** 1/8
  - **Phần c** (Điền số): c) Tính hệ số tương quan rho(X, Y).
    - **Đáp án c:** 1/2
  - **Phần d** (Đúng/Sai): d) Vì rho(X, Y) = 1/2 nên tồn tại a > 0 và b sao cho Y = aX + b.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) Chỉ ô (X = 1, Y = 1) cho tích khác 0: E(XY) = 1 . 1 . 3/8 = 3/8.
    2. b) P(X = 1) = P(Y = 1) = 1/2 nên E(X) = E(Y) = 1/2; Cov = 3/8 - 1/4 = 1/8.
    3. c) V(X) = V(Y) = 1/2 . 1/2 = 1/4; rho = (1/8)/sqrt(1/4 . 1/4) = (1/8)/(1/4) = 1/2.
    4. d) Y = aX + b chỉ khi |rho| = 1. Ở đây X = 0 vẫn cho cả Y = 0 lẫn Y = 1 (xác suất 3/8 và 1/8) nên Y không xác định bởi X; rho = 1/2 chỉ nói quan hệ tuyến tính ở mức vừa phải.
- `xs_t10_tq_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** X nhận các giá trị -1, 0, 1 với xác suất 1/3 mỗi giá trị, và Y = X^2. Bảng phân phối đồng thời của (X, Y) ở ma trận P: hàng 1, 2, 3 ứng với X = -1, 0, 1; cột 1, 2 ứng với Y = 0, 1.
  - P = (0, 1/3); (1/3, 0); (0, 1/3)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g3_doc_lap_tf`
  - **Phần a** (Điền số): a) Tính E(XY).
    - **Đáp án a:** 0
  - **Phần b** (Điền số): b) Tính Cov(X, Y).
    - **Đáp án b:** 0
  - **Phần c** (Đúng/Sai): c) X và Y độc lập.
    - **Đáp án c:** Sai
  - **Phần d** (Trắc nghiệm): d) Kết luận đúng là
    - **(đúng)** Cov = 0 chỉ cho biết không có quan hệ tuyến tính; Y vẫn hoàn toàn phụ thuộc X
    - Cov = 0 nên X và Y độc lập
    - rho = 0 nên Y không phụ thuộc X theo bất kỳ cách nào
    - Cov = 0 chứng tỏ Y = 0 chắc chắn
    - **Đáp án d:** Cov = 0 chỉ cho biết không có quan hệ tuyến tính; Y vẫn hoàn toàn phụ thuộc X
  - **Lời giải:**
    1. a) XY = X^3 nhận -1, 0, 1 với xác suất 1/3 mỗi giá trị: E(XY) = 0.
    2. b) E(X) = 0 nên Cov = E(XY) - E(X) E(Y) = 0 - 0 = 0.
    3. c) P(X = 1, Y = 0) = 0 nhưng P(X = 1) P(Y = 0) = 1/3 . 1/3 = 1/9: không độc lập.
    4. d) Y = X^2 là hàm của X nhưng hiệp phương sai (và hệ số tương quan) chỉ đo mức tuyến tính; khi đối xứng như ở đây chúng triệt tiêu. Hai đáp án sau lặp lại hai ngộ nhận đã gặp, đáp án cuối vô nghĩa (Y = 1 với xác suất 2/3).
- `xs_t10_tq_11` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biết Cov(X, Y) = 5. Tính Cov(3X - 1, 2 - Y). Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t6_ps_07`, `xs_g6_bien_doi`
  - **Đáp án:** -15
    1. Cov(aX + b, cY + d) = a c Cov(X, Y): hằng số cộng thêm không đổi độ lệch quanh kỳ vọng.
    2. Ở đây a = 3 và c = -1: Cov = 3 . (-1) . 5 = -15.
- `xs_g10_hiep_phuong_sai` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 1, 2, cột ứng với Y = 0, 1. Tính hiệp phương sai Cov(X, Y) = E(XY) - E(X)E(Y). Nhập một số hoặc phân số tối giản.
  - P = (1/12, 5/12); (1/3, 1/6)  (từng hàng)
  - **Đáp án:** -1/8
    1. E(X) = 3/2 (cộng hàng rồi nhân với giá trị của X) và E(Y) = 7/12 (cộng cột rồi nhân với giá trị của Y).
    2. E(XY) = tổng của x y P(X = x, Y = y) trên mọi ô = 3/4.
    3. Cov(X, Y) = 3/4 - (3/2) . (7/12) = -1/8.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1. Tính hiệp phương sai Cov(X, Y) = E(XY) - E(X)E(Y). Nhập một số hoặc phân số tối giản.
  - P = (1/4, 1/8); (0, 5/8)  (từng hàng)
  - **Đáp án:** 5/32
    1. E(X) = 5/8 (cộng hàng rồi nhân với giá trị của X) và E(Y) = 3/4 (cộng cột rồi nhân với giá trị của Y).
    2. E(XY) = tổng của x y P(X = x, Y = y) trên mọi ô = 5/8.
    3. Cov(X, Y) = 5/8 - (5/8) . (3/4) = 5/32.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 1, 2, cột ứng với Y = 1, 2. Tính hiệp phương sai Cov(X, Y) = E(XY) - E(X)E(Y). Nhập một số hoặc phân số tối giản.
  - P = (7/12, 1/12); (1/3, 0)  (từng hàng)
  - **Đáp án:** -1/36
    1. E(X) = 4/3 (cộng hàng rồi nhân với giá trị của X) và E(Y) = 13/12 (cộng cột rồi nhân với giá trị của Y).
    2. E(XY) = tổng của x y P(X = x, Y = y) trên mọi ô = 17/12.
    3. Cov(X, Y) = 17/12 - (4/3) . (13/12) = -1/36.
- `xs_g10_phuong_sai_tong` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 1, 2, cột ứng với Y = 0, 1. Tính V(X + Y). Nhập một số hoặc phân số tối giản.
  - P = (1/12, 5/12); (1/3, 1/6)  (từng hàng)
  - **Đáp án:** 35/144
    1. E(X) = 3/2, E(Y) = 7/12, E(XY) = 3/4, nên Cov(X, Y) = -1/8.
    2. V(X) = 1/4 và V(Y) = 35/144 (E(X^2) - (E(X))^2, E(Y^2) - (E(Y))^2).
    3. V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y) với a = 1, b = 1: 1 . (1/4) + 1 . (35/144) + 2 . (-1/8) = 35/144.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1. Tính V(-X + 2Y). Nhập một số hoặc phân số tối giản.
  - P = (1/4, 1/8); (0, 5/8)  (từng hàng)
  - **Đáp án:** 23/64
    1. E(X) = 5/8, E(Y) = 3/4, E(XY) = 5/8, nên Cov(X, Y) = 5/32.
    2. V(X) = 15/64 và V(Y) = 3/16 (E(X^2) - (E(X))^2, E(Y^2) - (E(Y))^2).
    3. V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y) với a = -1, b = 2: 1 . (15/64) + 4 . (3/16) + -4 . (5/32) = 23/64.
  - **Câu hỏi:** Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = 1, 2, cột ứng với Y = 1, 2. Tính V(3X + 2Y). Nhập một số hoặc phân số tối giản.
  - P = (7/12, 1/12); (1/3, 0)  (từng hàng)
  - **Đáp án:** 71/36
    1. E(X) = 4/3, E(Y) = 13/12, E(XY) = 17/12, nên Cov(X, Y) = -1/36.
    2. V(X) = 2/9 và V(Y) = 11/144 (E(X^2) - (E(X))^2, E(Y^2) - (E(Y))^2).
    3. V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y) với a = 3, b = 2: 9 . (2/9) + 4 . (11/144) + 12 . (-1/36) = 71/36.

### Hồi quy tuyến tính đơn (`xs_t10_hoi_quy`)

- `xs_t10_hq_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 5 điểm (x, y): (1, 2), (2, 3), (3, 5), (4, 4), (5, 6). Hệ số góc b của đường hồi quy tuyến tính y theo x (bình phương tối thiểu) là bao nhiêu? Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_g7_phuong_sai_mau`
  - **Đáp án:** 9/10
    1. x_tb = 15/5 = 3 và y_tb = 20/5 = 4.
    2. Sxx = (-2)^2 + (-1)^2 + 0 + 1^2 + 2^2 = 10; Sxy = (-2)(-2) + (-1)(-1) + 0 . 1 + 1 . 0 + 2 . 2 = 9.
    3. b = Sxy/Sxx = 9/10.
- `xs_t10_hq_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 4 điểm (x, y): (2, 3), (4, 5), (6, 4), (8, 8). Dùng đường hồi quy tuyến tính y theo x, dự đoán y khi x = 10. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_04`
  - **Đáp án:** 17/2
    1. x_tb = 5, y_tb = 5; Sxx = 9 + 1 + 1 + 9 = 20; Sxy = (-3)(-2) + (-1)(0) + 1 . (-1) + 3 . 3 = 14.
    2. b = 14/20 = 7/10; a = y_tb - b x_tb = 5 - 7/10 . 5 = 3/2, đường thẳng y = 3/2 + 7x/10.
    3. Tại x = 10: y = 3/2 + 7 = 17/2.
- `xs_t10_hq_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đường hồi quy tuyến tính y = a + bx tìm bằng bình phương tối thiểu luôn đi qua điểm (x_tb, y_tb) của mẫu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_04`
  - **Đáp án:** Đúng
    1. Hệ số chặn là a = y_tb - b x_tb, nên tại x = x_tb: y = y_tb - b x_tb + b x_tb = y_tb.
    2. Đây cũng là một cách nhớ công thức của a. Mệnh đề đúng.
- `xs_t10_hq_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ cùng một mẫu, đường hồi quy x theo y có hệ số góc (đối với y) bằng nghịch đảo hệ số góc b của đường hồi quy y theo x, với mọi mẫu có b khác 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t6_ps_07`
  - **Đáp án:** Sai
    1. Hệ số góc của y theo x là Sxy/Sxx, còn của x theo y là Sxy/Syy: tích hai hệ số là Sxy^2/(Sxx Syy) = r^2, nhỏ hơn 1 trừ khi các điểm nằm đúng trên một đường thẳng.
    2. Hai đường hồi quy nói chung khác nhau: một đường làm nhỏ nhất bình phương độ lệch theo trục y, đường kia theo trục x. Mệnh đề sai.
- `xs_t10_hq_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 5 điểm (x, y) có x_tb = 3, y_tb = 4, Sxx = tổng (x - x_tb)^2 = 10, Syy = tổng (y - y_tb)^2 = 12 và Sxy = tổng (x - x_tb)(y - y_tb) = 9. Hệ số góc b của đường hồi quy y theo x là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_g7_phuong_sai_mau`
    - **(đúng)** 9/10
    - 3/4
    - 9/sqrt(120)
    - 9/5
  - **Đáp án:** 9/10
    1. b = Sxy/Sxx = 9/10: bình phương tối thiểu trên độ lệch theo trục y, mẫu số là độ phân tán của biến giải thích x.
    2. 3/4 = Sxy/Syy là hệ số góc của đường hồi quy x theo y: nhầm biến nào giải thích biến nào.
    3. 9/sqrt(120) = Sxy/sqrt(Sxx Syy) là hệ số tương quan mẫu r (khoảng 0.82), không phải hệ số góc.
    4. 9/5 = Sxy/n: chia cho cỡ mẫu thay vì cho Sxx.
- `xs_t10_hq_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Mẫu 5 điểm (x, y): (1, 1), (2, 3), (3, 2), (4, 5), (5, 4). Tìm đường hồi quy tuyến tính y theo x. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_04`, `xs_g7_phuong_sai_mau`
  - **Lời giải đưa ra (có một bước sai):**
    1. x_tb = 3, y_tb = 3.
    2. Sxx = 4 + 1 + 0 + 1 + 4 = 10 và Sxy = (-2)(-2) + (-1) . 0 + 0 . (-1) + 1 . 2 + 2 . 1 = 8.
    3. Hệ số góc b = Sxx/Sxy = 10/8 = 5/4.   **<- bước sai đầu tiên**
    4. Hệ số chặn a = y_tb - b x_tb = 3 - 15/4 = -3/4. Đường hồi quy: y = -3/4 + 5x/4.
  - **Đáp án:** Bước 3: Hệ số góc b = Sxx/Sxy = 10/8 = 5/4.
  - **Vì sao sai, và bước đúng:**
    1. Hệ số góc là Sxy/Sxx = 8/10 = 4/5: tử là hiệp phương sai (cộng của tích hai độ lệch), mẫu là Sxx. Ở bước 3 hai số bị đổi chỗ.
    2. Đúng: a = 3 - 4/5 . 3 = 3/5, đường hồi quy y = 3/5 + 4x/5. Bước cuối chỉ sai vì mang lỗi của bước trước.
- `xs_t10_hq_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mẫu (x_i, y_i) và đường hồi quy y = a + bx, ghép mỗi đại lượng với công thức hay ý nghĩa của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_04`
  - **Đáp án (ghép đúng):**
    - Hệ số góc b — Sxy/Sxx
    - Hệ số chặn a — y_tb - b x_tb
    - Phần dư của điểm thứ i — y_i - (a + b x_i): độ lệch dọc từ điểm tới đường
    - Hệ số xác định r^2 — Tỷ lệ biến thiên của y được quan hệ tuyến tính với x giải thích
  - **Lời giải:**
    1. Bình phương tối thiểu chọn a, b làm nhỏ nhất tổng bình phương các phần dư. Điều kiện cực trị cho b = Sxy/Sxx và a = y_tb - b x_tb.
    2. r^2 = 1 - (tổng bình phương phần dư)/Syy, nằm giữa 0 và 1.
- `xs_t10_hq_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 5 điểm (x, y): (0, 0), (1, 2), (2, 2), (3, 3), (4, 3). Sắp xếp các bước tìm đường hồi quy tuyến tính y theo x.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_04`
  - **Đáp án (thứ tự đúng):**
    1. Tính trung bình: x_tb = 10/5 = 2, y_tb = 10/5 = 2.
    2. Tính độ lệch: x - x_tb là -2, -1, 0, 1, 2 và y - y_tb là -2, 0, 0, 1, 1.
    3. Sxx = 10 và Sxy = 4 + 0 + 0 + 1 + 2 = 7.
    4. Hệ số góc b = 7/10, rồi hệ số chặn a = 2 - 7/10 . 2 = 3/5.
    5. Đường hồi quy y = 3/5 + 7x/10.
  - **Lời giải:**
    1. Trung bình trước, rồi độ lệch, rồi hai tổng Sxx, Sxy, rồi b (cần Sxy và Sxx), rồi a (cần b và các trung bình).
    2. Kiểm tra: đường thẳng đi qua (x_tb, y_tb) = (2, 2): 3/5 + 14/10 = 2.
- `xs_t10_hq_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 4 điểm (x, y): (1, 2), (2, 2), (3, 4), (4, 4). Tìm đường hồi quy tuyến tính y = a + bx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_g7_phuong_sai_mau`
  - **Phần a** (Điền số): a) Tính Sxy = tổng (x - x_tb)(y - y_tb), biết x_tb = 5/2 và y_tb = 3.
    - **Đáp án a:** 4
  - **Phần b** (Điền số): b) Tính hệ số góc b.
    - **Đáp án b:** 4/5
  - **Phần c** (Điền số): c) Tính hệ số chặn a.
    - **Đáp án c:** 1
  - **Phần d** (Điền số): d) Dự đoán y khi x = 5.
    - **Đáp án d:** 5
  - **Lời giải:**
    1. a) x - x_tb = -3/2, -1/2, 1/2, 3/2 và y - y_tb = -1, -1, 1, 1: Sxy = 3/2 + 1/2 + 1/2 + 3/2 = 4.
    2. b) Sxx = 9/4 + 1/4 + 1/4 + 9/4 = 5; b = 4/5.
    3. c) a = y_tb - b x_tb = 3 - 4/5 . 5/2 = 3 - 2 = 1.
    4. d) y = 1 + 4/5 . 5 = 5. (Điểm x = 5 nằm ngoài mẫu: dự đoán ngoài khoảng dữ liệu kém tin cậy hơn.)
- `xs_t10_hq_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ một mẫu hai chiều ta biết x_tb = 10, y_tb = 20, độ lệch chuẩn mẫu s_x = 2, s_y = 6 và hệ số tương quan mẫu r = 1/2. Đường hồi quy y theo x có hệ số góc b = r s_y/s_x.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t6_ps_07`
  - **Phần a** (Điền số): a) Tính hệ số góc b.
    - **Đáp án a:** 3/2
  - **Phần b** (Điền số): b) Tính hệ số chặn a.
    - **Đáp án b:** 5
  - **Phần c** (Đúng/Sai): c) r^2 = 1/4, nên khoảng 25% sự biến thiên của y được quan hệ tuyến tính với x giải thích.
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Dự đoán y khi x = 12.
    - **Đáp án d:** 23
  - **Lời giải:**
    1. a) b = (1/2) . 6/2 = 3/2. Công thức này đúng vì Sxy = r s_x s_y (n - 1) và Sxx = s_x^2 (n - 1).
    2. b) a = y_tb - b x_tb = 20 - 3/2 . 10 = 5.
    3. c) r^2 là hệ số xác định: phần phương sai của y mà đường hồi quy giải thích được; 1/4 = 25%. 75% còn lại là biến thiên quanh đường.
    4. d) y = 5 + 3/2 . 12 = 23.
- `xs_t10_hq_11` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với đường hồi quy tuyến tính y = a + bx tìm bằng bình phương tối thiểu (có hệ số chặn a), tổng các phần dư y_i - (a + b x_i) của mẫu bằng 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t7_dt_01`, `xs_t7_dt_04`
  - **Đáp án:** Đúng
    1. Đạo hàm theo a của tổng bình phương phần dư bằng 0 cho đúng điều kiện: tổng của y_i - a - b x_i bằng 0.
    2. Cách khác: tổng phần dư = n y_tb - n a - b n x_tb = n (y_tb - a - b x_tb) = 0 vì a = y_tb - b x_tb. Mệnh đề đúng.
- `xs_g10_hoi_quy` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Mẫu 4 điểm (x, y): (0, 1), (1, 7), (2, 12), (3, 7). Tìm hệ số chặn a của đường hồi quy tuyến tính y = a + bx (bình phương tối thiểu). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 33/10
    1. x_tb = 6/4 = 3/2 và y_tb = 27/4.
    2. Sxx = tổng (x - x_tb)^2 = 5; Sxy = tổng (x - x_tb)(y - y_tb) = 23/2.
    3. Hệ số góc b = Sxy/Sxx = 23/10.
    4. Hệ số chặn a = y_tb - b x_tb = 27/4 - (23/10) . (3/2) = 33/10.
  - **Câu hỏi:** Mẫu 4 điểm (x, y): (0, 5), (1, 2), (2, 11), (3, 12). Dùng đường hồi quy tuyến tính y theo x (bình phương tối thiểu) để dự đoán y khi x = 5. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 18
    1. x_tb = 6/4 = 3/2 và y_tb = 30/4 = 15/2.
    2. Sxx = tổng (x - x_tb)^2 = 5; Sxy = tổng (x - x_tb)(y - y_tb) = 15.
    3. Hệ số góc b = Sxy/Sxx = 3.
    4. Hệ số chặn a = y_tb - b x_tb = 3; y = 3 + 3 x.
    5. Tại x = 5: y = 3 + 3 . 5 = 18.
  - **Câu hỏi:** Mẫu 4 điểm (x, y): (1, 9), (2, 7), (3, 10), (4, 9). Tìm hệ số góc b của đường hồi quy tuyến tính y theo x (bình phương tối thiểu). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 3/10
    1. x_tb = 10/4 = 5/2 và y_tb = 35/4.
    2. Sxx = tổng (x - x_tb)^2 = 5; Sxy = tổng (x - x_tb)(y - y_tb) = 3/2.
    3. Hệ số góc b = Sxy/Sxx = 3/10.

### Tiên đề xác suất (`xs_t10_tien_de`)

- `xs_t10_td_01` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Không gian mẫu Omega = {a, b, c}, xác suất đặt trên mọi tập con theo tính cộng. Bộ giá trị P({a}), P({b}), P({c}) nào xác định một xác suất thoả ba tiên đề?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_08`, `xs_t5_hp_07`
    - **(đúng)** 1/2, 1/3, 1/6
    - 1/2, 1/2, 1/2
    - 3/4, -1/4, 1/2
    - 1/3, 1/3, 1/4
  - **Đáp án:** 1/2, 1/3, 1/6
    1. Cần P({k}) >= 0 (tiên đề không âm) và tổng bằng P(Omega) = 1 (tiên đề chuẩn hoá): 1/2 + 1/3 + 1/6 = 1.
    2. 1/2, 1/2, 1/2 có tổng 3/2: P(Omega) = P({a}) + P({b}) + P({c}) = 3/2 khác 1.
    3. 3/4, -1/4, 1/2 có tổng 1 nhưng có một giá trị âm, vi phạm tiên đề không âm.
    4. 1/3, 1/3, 1/4 không âm nhưng tổng 11/12 khác 1.
- `xs_t10_td_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ ba tiên đề của xác suất (không âm, P(Omega) = 1, cộng tính cho các sự kiện xung khắc) có thể suy ra xác suất của sự kiện không thể (tập rỗng) bằng 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_06`, `xs_t5_hp_07`
  - **Đáp án:** Đúng
    1. Omega và tập rỗng xung khắc, và Omega + rỗng = Omega: P(Omega) = P(Omega) + P(rỗng) theo tiên đề cộng.
    2. Suy ra P(rỗng) = 0. Đây là hệ quả, không cần thêm tiên đề. Mệnh đề đúng.
- `xs_t10_td_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai sự kiện A, B có P(A) = 1/2, P(B) = 1/3 và P(A + B) = 3/4 (A + B là hợp của A và B). Tính P(AB), xác suất A và B cùng xảy ra. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_05`, `xs_t5_hp_07`
  - **Đáp án:** 1/12
    1. Công thức cộng suy ra từ tiên đề cộng: P(A + B) = P(A) + P(B) - P(AB).
    2. P(AB) = P(A) + P(B) - P(A + B) = 1/2 + 1/3 - 3/4 = 6/12 + 4/12 - 9/12 = 1/12.
- `xs_t10_td_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chứng minh từ ba tiên đề rằng nếu A kéo theo B (A nằm trong B) thì P(A) <= P(B). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_08`, `xs_t5_xk_06`
  - **Lời giải đưa ra (có một bước sai):**
    1. Vì A nằm trong B nên B = A + (B \ A), hai sự kiện A và B \ A xung khắc.
    2. Theo tiên đề cộng: P(B) = P(A) + P(B \ A).
    3. Theo tiên đề không âm P(B \ A) <= 0, nên P(B) <= P(A).   **<- bước sai đầu tiên**
    4. Vậy P(A) <= P(B) khi đổi tên A và B.
  - **Đáp án:** Bước 3: Theo tiên đề không âm P(B \ A) <= 0, nên P(B) <= P(A).
  - **Vì sao sai, và bước đúng:**
    1. Tiên đề không âm nói P(B \ A) >= 0, không phải <= 0: chiều bất đẳng thức bị viết ngược.
    2. Đúng: P(B) = P(A) + P(B \ A) >= P(A) vì P(B \ A) >= 0. Bước cuối "đổi tên" là vá lỗi, không phải chứng minh.
- `xs_t10_td_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước suy ra công thức cộng P(A + B) = P(A) + P(B) - P(AB) từ ba tiên đề.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_05`, `xs_t5_hp_07`
  - **Đáp án (thứ tự đúng):**
    1. Viết A + B = A + (B \ A), hai sự kiện A và B \ A xung khắc.
    2. Theo tiên đề cộng: P(A + B) = P(A) + P(B \ A).
    3. Viết B = AB + (B \ A), hai sự kiện AB và B \ A xung khắc.
    4. Theo tiên đề cộng: P(B) = P(AB) + P(B \ A), nên P(B \ A) = P(B) - P(AB).
    5. Thay vào bước hai: P(A + B) = P(A) + P(B) - P(AB).
  - **Lời giải:**
    1. Cả hai lần tách đều dùng tiên đề cộng trên sự kiện xung khắc; kết quả của lần tách thứ hai (P(B \ A)) được thế vào lần tách thứ nhất.
    2. Không dùng đến giả thiết A, B xung khắc: công thức đúng cho mọi A, B.
- `xs_t10_td_06` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Không gian mẫu Omega = {1, 2, 3, 4}. Một xác suất P trên mọi tập con của Omega được xác định bởi P({k}) = c k với k = 1, 2, 3, 4 và một hằng số c.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_05`, `xs_t5_hp_07`
  - **Phần a** (Điền số): a) Tìm c để P thoả tiên đề chuẩn hoá P(Omega) = 1.
    - **Đáp án a:** 1/10
  - **Phần b** (Điền số): b) Tính P({1, 2}).
    - **Đáp án b:** 3/10
  - **Phần c** (Điền số): c) Tính P({3, 4}).
    - **Đáp án c:** 7/10
  - **Phần d** (Đúng/Sai): d) P({1, 2}) + P({3, 4}) = P(Omega) khớp với tiên đề cộng.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Tiên đề cộng cho P(Omega) = c (1 + 2 + 3 + 4) = 10 c = 1, nên c = 1/10.
    2. b) P({1, 2}) = P({1}) + P({2}) = 1/10 + 2/10 = 3/10.
    3. c) P({3, 4}) = 3/10 + 4/10 = 7/10.
    4. d) {1, 2} và {3, 4} xung khắc và hợp của chúng là Omega: 3/10 + 7/10 = 1 = P(Omega).
- `xs_t10_td_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi mệnh đề với vai trò của nó trong lý thuyết xác suất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_08`, `xs_t5_hp_07`
  - **Đáp án (ghép đúng):**
    - P(A) >= 0 với mọi sự kiện A — Tiên đề không âm
    - P(Omega) = 1 — Tiên đề chuẩn hoá
    - A và B xung khắc thì P(A + B) = P(A) + P(B) — Tiên đề cộng
    - P(A') = 1 - P(A) với A' là sự kiện đối — Hệ quả chứng minh được, không phải tiên đề
  - **Lời giải:**
    1. Ba tiên đề đầu là các luật chơi: không âm, tổng bằng 1, cộng cho sự kiện xung khắc.
    2. Công thức xác suất của sự kiện đối suy ra từ tiên đề cộng và chuẩn hoá: P(A) + P(A') = P(Omega) = 1.
- `xs_t10_td_08` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** "P(A) <= 1 với mọi sự kiện A" là một trong ba tiên đề của xác suất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `xs_t3_cc_06`, `xs_t5_hp_07`
  - **Đáp án:** Sai
    1. Ba tiên đề là: P(A) >= 0, P(Omega) = 1 và tính cộng. Bất đẳng thức P(A) <= 1 được chứng minh từ chúng: P(A) + P(A') = 1 và P(A') >= 0.
    2. Mệnh đề sai (vì nó là một hệ quả, không phải tiên đề).
