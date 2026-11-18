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
