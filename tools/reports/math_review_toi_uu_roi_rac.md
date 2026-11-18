# Bảng duyệt câu hỏi: Tối Ưu và Toán Rời Rạc

Tạo bởi `python tools/math_review.py`. Đánh dấu đã duyệt bằng `"reviewed": true` trong `server/data/math/items/toi_uu_roi_rac.json`.

## Tầng 1: Lý thuyết tổ hợp mở đầu, logic mệnh đề và quy nạp

47 dạng câu (37 câu viết tay, 10 bộ sinh câu); 47 chưa duyệt.

### Cấu hình tổ hợp (`tr_t1_cau_hinh`)

- `tr_t1_ch_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Liệt kê mọi cách xếp ba đệ tử An, Bình, Chi thành một hàng dọc. Có tất cả bao nhiêu cách?
  - **Đáp án:** 6
    1. Liệt kê theo người đứng đầu hàng, mỗi lần đứng đầu còn hai cách xếp hai người sau.
    2. An đứng đầu: An Bình Chi, An Chi Bình. Bình đứng đầu: Bình An Chi, Bình Chi An.
    3. Chi đứng đầu: Chi An Bình, Chi Bình An.
    4. Đếm lại danh sách: có 6 cách.
- `tr_t1_ch_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi liệt kê các tập con của {1, 2, 3}, tập {1, 2} và tập {2, 1} được tính là hai cấu hình khác nhau.
  - **Đáp án:** Sai
    1. Một tập hợp chỉ quan tâm phần tử nào có mặt, không quan tâm thứ tự viết.
    2. {1, 2} và {2, 1} có cùng các phần tử nên là một tập.
    3. Vì vậy chúng là cùng một cấu hình; chỉ khi đếm dãy có thứ tự, như (1, 2) và (2, 1), mới tính là hai.
- `tr_t1_ch_03` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi bài toán với loại cấu hình mà một lời giải của nó là.
  - **Đáp án (ghép đúng):**
    - Xếp 5 đệ tử vào 5 ghế thành một hàng — một hoán vị của 5 người
    - Chọn 3 trong 5 đệ tử vào một tổ, không phân vai — một tập con 3 phần tử
    - Đánh Đúng hoặc Sai cho mỗi câu trong 4 câu — một xâu nhị phân độ dài 4
    - Chọn chưởng môn và phó chưởng môn trong 5 đệ tử — một cặp có thứ tự gồm 2 người khác nhau
  - **Lời giải:**
    1. Xếp đủ 5 người vào 5 chỗ có thứ tự: mỗi cách là một hoán vị.
    2. Chọn một nhóm không phân vai: thứ tự không quan trọng, đó là một tập con.
    3. Mỗi câu nhận một trong hai giá trị Đúng, Sai: ghi Đúng là 1, Sai là 0 được một xâu nhị phân.
    4. Hai chức khác nhau nên (An, Bình) khác (Bình, An): đó là một cặp có thứ tự.
- `tr_g1_xau_nhi_phan` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 7 bắt đầu bằng chữ số 1?
  - **Đáp án:** 64
    1. Một xâu nhị phân độ dài n là một dãy n chữ số, mỗi chữ số là 0 hoặc 1.
    2. Vị trí đầu đã cố định là 1, còn 6 vị trí tự do.
    3. Theo quy tắc nhân có 2^6 = 64 xâu.
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 3?
  - **Đáp án:** 8
    1. Một xâu nhị phân độ dài n là một dãy n chữ số, mỗi chữ số là 0 hoặc 1.
    2. Mỗi vị trí trong 3 vị trí có 2 cách: 0 hoặc 1.
    3. Theo quy tắc nhân có 2^3 = 8 xâu.
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 7 bắt đầu bằng chữ số 1?
  - **Đáp án:** 64
    1. Một xâu nhị phân độ dài n là một dãy n chữ số, mỗi chữ số là 0 hoặc 1.
    2. Vị trí đầu đã cố định là 1, còn 6 vị trí tự do.
    3. Theo quy tắc nhân có 2^6 = 64 xâu.
- `tr_t1_ch_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Liệt kê các tập con có đúng 2 phần tử của tập {a, b, c, d}. Có bao nhiêu tập như vậy?
  - **Đáp án:** 6
    1. Liệt kê có hệ thống: ghép a với từng chữ đứng sau nó, rồi b với từng chữ đứng sau nó, và cứ thế.
    2. {a, b}, {a, c}, {a, d}, {b, c}, {b, d}, {c, d}.
    3. Không ghép ngược lại (như {b, a}) vì đó là tập đã có.
    4. Có 6 tập.
- `tr_t1_ch_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Danh sách nào liệt kê đúng và đủ các xâu nhị phân độ dài 3 có đúng hai chữ số 1?
    - **(đúng)** 011, 101, 110
    - 011, 110
    - 011, 101, 110, 111
    - 001, 010, 100
  - **Đáp án:** 011, 101, 110
    1. Chọn vị trí cho chữ số 0 duy nhất: đầu, giữa hoặc cuối.
    2. Ba lựa chọn cho ba xâu 011, 101, 110.
    3. 111 có ba chữ số 1, còn 001, 010, 100 chỉ có một chữ số 1.
- `tr_t1_ch_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tô 3 ô xếp thẳng hàng, mỗi ô màu xanh hoặc đỏ, sao cho hai ô cạnh nhau luôn khác màu. Sắp xếp các bước đếm số cách tô.
  - **Đáp án (thứ tự đúng):**
    1. Ô thứ nhất được tô tự do: 2 cách.
    2. Ô thứ hai phải khác màu ô thứ nhất: chỉ còn 1 cách.
    3. Ô thứ ba phải khác màu ô thứ hai: cũng chỉ 1 cách.
    4. Nhân lại: 2 . 1 . 1 = 2 cách, đó là xanh đỏ xanh và đỏ xanh đỏ.
  - **Lời giải:**
    1. Tô lần lượt từ trái sang phải, vì màu của mỗi ô phụ thuộc vào ô ngay trước nó.
    2. Chỉ ô đầu có lựa chọn; mỗi ô sau bị buộc phải đổi màu.
    3. Có 2 cách: xanh đỏ xanh và đỏ xanh đỏ.
- `tr_t1_ch_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đếm số xâu nhị phân độ dài 3 không có hai chữ số 1 đứng liền nhau.
  - **Lời giải đưa ra (có một bước sai):**
    1. Có tất cả 2^3 = 8 xâu nhị phân độ dài 3.
    2. Các xâu có hai chữ số 1 đứng liền nhau là 011 và 110.   **<- bước sai đầu tiên**
    3. Bỏ chúng đi, còn 8 - 2 = 6 xâu.
    4. Vậy có 6 xâu thỏa mãn.
  - **Đáp án:** Bước 2: Các xâu có hai chữ số 1 đứng liền nhau là 011 và 110.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 bỏ sót xâu 111: nó cũng có hai chữ số 1 liền nhau.
    2. Các xâu bị loại là 011, 110, 111, nên còn 8 - 3 = 5 xâu.
    3. Kiểm tra bằng cách liệt kê: 000, 001, 010, 100, 101.
- `tr_g1_dem_cau_hinh` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một bảng chữ gồm 2 chữ cái A, B. Có bao nhiêu xâu độ dài 4 lập từ các chữ cái đó (được lặp lại) mà có chữ cái đầu và chữ cái cuối giống nhau?
  - **Đáp án:** 8
    1. Lập xâu từ trái sang phải, đếm số cách ở mỗi vị trí.
    2. Chọn tự do 3 chữ cái đầu: 2^3 cách.
    3. Chữ cái cuối buộc phải bằng chữ cái đầu: 1 cách.
    4. Theo quy tắc nhân có 2^3 = 8 xâu.
  - **Câu hỏi:** Một bảng chữ gồm 2 chữ cái A, B. Có bao nhiêu xâu độ dài 3 lập từ các chữ cái đó (được lặp lại) mà có chữ cái đầu và chữ cái cuối giống nhau?
  - **Đáp án:** 4
    1. Lập xâu từ trái sang phải, đếm số cách ở mỗi vị trí.
    2. Chọn tự do 2 chữ cái đầu: 2^2 cách.
    3. Chữ cái cuối buộc phải bằng chữ cái đầu: 1 cách.
    4. Theo quy tắc nhân có 2^2 = 4 xâu.
  - **Câu hỏi:** Một bảng chữ gồm 3 chữ cái A, B, C. Có bao nhiêu xâu độ dài 4 lập từ các chữ cái đó (được lặp lại) mà có chữ cái đầu và chữ cái cuối giống nhau?
  - **Đáp án:** 27
    1. Lập xâu từ trái sang phải, đếm số cách ở mỗi vị trí.
    2. Chọn tự do 3 chữ cái đầu: 3^3 cách.
    3. Chữ cái cuối buộc phải bằng chữ cái đầu: 1 cách.
    4. Theo quy tắc nhân có 3^3 = 27 xâu.

### Quy tắc cộng và quy tắc nhân (`tr_t1_cong_nhan`)

- `tr_t1_cn_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tàng Thư Các có 5 cuốn sách về trận pháp và 7 cuốn về luyện đan, không cuốn nào thuộc cả hai loại. Một đệ tử chọn 1 cuốn để đọc. Có bao nhiêu cách chọn?
  - **Đáp án:** 12
    1. Cuốn được chọn hoặc là sách trận pháp, hoặc là sách luyện đan: hai trường hợp không có cuốn nào chung.
    2. Theo quy tắc cộng: 5 + 7 = 12 cách.
- `tr_t1_cn_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quy tắc cộng chỉ dùng được khi các trường hợp được chia ra không có cách làm nào chung.
  - **Đáp án:** Đúng
    1. Quy tắc cộng đếm hợp của các trường hợp bằng tổng số cách của từng trường hợp.
    2. Nếu hai trường hợp có cách làm chung thì cách đó bị đếm hai lần, tổng sẽ lớn hơn số thật.
    3. Khi các trường hợp có phần chung phải dùng nguyên lý bù trừ (tầng 2).
- `tr_t1_cn_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lệnh bài gồm 1 chữ cái (chọn trong 26 chữ cái) rồi đến 2 chữ số (mỗi chữ số từ 0 đến 9, được lặp lại). Có bao nhiêu lệnh bài khác nhau?
    - **(đúng)** 2600
    - 126
    - 2340
    - 46
  - **Đáp án:** 2600
    1. Lập lệnh bài qua ba bước nối tiếp: chọn chữ cái, chọn chữ số thứ nhất, chọn chữ số thứ hai.
    2. Số cách lần lượt là 26, 10 và 10.
    3. Theo quy tắc nhân: 26 . 10 . 10 = 2600.
- `tr_t1_cn_08` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp 3 đệ tử vào 5 ghế xếp thành hàng, mỗi ghế nhiều nhất một người. Sắp xếp các bước đếm số cách xếp.
  - **Đáp án (thứ tự đúng):**
    1. Đệ tử thứ nhất chọn một ghế: 5 cách.
    2. Đệ tử thứ hai chọn một ghế còn trống: 4 cách.
    3. Đệ tử thứ ba chọn một ghế còn trống: 3 cách.
    4. Theo quy tắc nhân: 5 . 4 . 3 = 60 cách.
  - **Lời giải:**
    1. Cho từng người ngồi xuống theo thứ tự; mỗi người ngồi rồi thì bớt đi một ghế trống.
    2. Số cách ở mỗi bước là 5, 4, 3 và không phụ thuộc người trước ngồi ghế nào.
    3. Nhân lại được 60 cách.
- `tr_g1_quy_tac_nhan` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đan sư có 6 loại linh thảo chính, 2 loại phụ dược và 4 kiểu lò. Mỗi mẻ đan dùng một linh thảo chính, một phụ dược và một kiểu lò. Có bao nhiêu cách chọn cho một mẻ?
  - **Đáp án:** 48
    1. Việc chọn gồm ba bước nối tiếp nhau, mỗi bước chọn một thứ.
    2. chọn linh thảo chính: 6 cách; chọn phụ dược: 2 cách; chọn kiểu lò: 4 cách.
    3. Số cách ở mỗi bước không phụ thuộc vào lựa chọn ở bước trước, nên dùng quy tắc nhân.
    4. 6 . 2 . 4 = 48.
  - **Câu hỏi:** Một đan sư có 2 loại linh thảo chính, 2 loại phụ dược và 4 kiểu lò. Mỗi mẻ đan dùng một linh thảo chính, một phụ dược và một kiểu lò. Có bao nhiêu cách chọn cho một mẻ?
  - **Đáp án:** 16
    1. Việc chọn gồm ba bước nối tiếp nhau, mỗi bước chọn một thứ.
    2. chọn linh thảo chính: 2 cách; chọn phụ dược: 2 cách; chọn kiểu lò: 4 cách.
    3. Số cách ở mỗi bước không phụ thuộc vào lựa chọn ở bước trước, nên dùng quy tắc nhân.
    4. 2 . 2 . 4 = 16.
  - **Câu hỏi:** Một đan sư có 6 loại linh thảo chính, 6 loại phụ dược và 3 kiểu lò. Mỗi mẻ đan dùng một linh thảo chính, một phụ dược và một kiểu lò. Có bao nhiêu cách chọn cho một mẻ?
  - **Đáp án:** 108
    1. Việc chọn gồm ba bước nối tiếp nhau, mỗi bước chọn một thứ.
    2. chọn linh thảo chính: 6 cách; chọn phụ dược: 6 cách; chọn kiểu lò: 3 cách.
    3. Số cách ở mỗi bước không phụ thuộc vào lựa chọn ở bước trước, nên dùng quy tắc nhân.
    4. 6 . 6 . 3 = 108.
- `tr_t1_cn_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số tự nhiên có 3 chữ số mà ba chữ số đôi một khác nhau?
  - **Đáp án:** 648
    1. Chọn chữ số hàng trăm trước: khác 0, nên có 9 cách.
    2. Chữ số hàng chục khác chữ số hàng trăm, được bằng 0: 9 cách.
    3. Chữ số hàng đơn vị khác hai chữ số đã chọn: 8 cách.
    4. Theo quy tắc nhân: 9 . 9 . 8 = 648.
- `tr_t1_cn_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số chẵn có 3 chữ số mà ba chữ số đôi một khác nhau?
  - **Đáp án:** 328
    1. Chia theo chữ số hàng đơn vị, vì chữ số 0 làm thay đổi số cách chọn hàng trăm.
    2. Hàng đơn vị là 0: hàng trăm có 9 cách (1 đến 9), hàng chục có 8 cách, được 9 . 8 = 72 số.
    3. Hàng đơn vị là 2, 4, 6 hoặc 8 (4 cách): hàng trăm khác 0 và khác hàng đơn vị nên có 8 cách, hàng chục có 8 cách, được 4 . 8 . 8 = 256 số.
    4. Hai trường hợp rời nhau, theo quy tắc cộng: 72 + 256 = 328.
- `tr_t1_cn_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đếm các số tự nhiên có 4 chữ số khác nhau lập từ các chữ số 0, 1, 2, 3, 4.
  - **Lời giải đưa ra (có một bước sai):**
    1. Số cần lập có dạng abcd với a, b, c, d khác nhau, lấy từ {0, 1, 2, 3, 4}.
    2. Chữ số a đứng đầu nên khác 0: có 4 cách chọn.
    3. Chữ số b khác a và được phép bằng 0: có 4 cách chọn.
    4. Chữ số c khác a và b: có 4 cách chọn.   **<- bước sai đầu tiên**
    5. Chữ số d khác a, b, c: có 2 cách chọn.
    6. Theo quy tắc nhân có 4 . 4 . 4 . 2 = 128 số.
  - **Đáp án:** Bước 4: Chữ số c khác a và b: có 4 cách chọn.
  - **Vì sao sai, và bước đúng:**
    1. Ở bước 4, c phải khác hai chữ số đã dùng là a và b, nên chỉ còn 5 - 2 = 3 cách.
    2. Bước 5 cũng vì thế mà đúng: d khác ba chữ số đã dùng, còn 2 cách.
    3. Kết quả đúng là 4 . 4 . 3 . 2 = 96 số.
- `tr_t1_cn_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nhà bếp tông môn có 3 món chay và 4 món mặn, các món đều khác nhau. Ghép mỗi cách chọn với số cách của nó.
  - **Đáp án (ghép đúng):**
    - Chọn 1 món, chay hoặc mặn — 3 + 4 = 7 cách
    - Chọn 1 món chay và 1 món mặn — 3 . 4 = 12 cách
    - Chọn món chay cho bữa sáng và món chay khác cho bữa tối — 3 . 2 = 6 cách
    - Chọn món chay cho bữa sáng và bữa tối, được ăn lại món cũ — 3 . 3 = 9 cách
  - **Lời giải:**
    1. Một món, chay hoặc mặn: hai trường hợp rời nhau, dùng quy tắc cộng.
    2. Một chay và một mặn: hai bước nối tiếp, dùng quy tắc nhân.
    3. Hai bữa khác món: bữa sáng 3 cách, bữa tối còn 2 cách.
    4. Hai bữa được lặp món: mỗi bữa đều có 3 cách.
- `tr_g1_quy_tac_cong` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Từ động phủ A đến trấn B có 3 con đường, từ trấn B đến tông môn C có 6 con đường, và có 1 con đường đi thẳng từ A đến C không qua B. Có bao nhiêu cách đi từ A đến C?
  - **Đáp án:** 19
    1. Chia thành hai trường hợp rời nhau: đi qua B, hoặc đi thẳng không qua B.
    2. Đi qua B: chọn đường A đến B rồi đường B đến C, theo quy tắc nhân có 3 . 6 = 18 cách.
    3. Đi thẳng: có 1 cách.
    4. Hai trường hợp không có cách đi nào chung, theo quy tắc cộng: 18 + 1 = 19.
  - **Câu hỏi:** Từ động phủ A đến trấn B có 2 con đường, từ trấn B đến tông môn C có 2 con đường, và có 1 con đường đi thẳng từ A đến C không qua B. Có bao nhiêu cách đi từ A đến C?
  - **Đáp án:** 5
    1. Chia thành hai trường hợp rời nhau: đi qua B, hoặc đi thẳng không qua B.
    2. Đi qua B: chọn đường A đến B rồi đường B đến C, theo quy tắc nhân có 2 . 2 = 4 cách.
    3. Đi thẳng: có 1 cách.
    4. Hai trường hợp không có cách đi nào chung, theo quy tắc cộng: 4 + 1 = 5.
  - **Câu hỏi:** Từ động phủ A đến trấn B có 3 con đường, từ trấn B đến tông môn C có 6 con đường, và có 5 con đường đi thẳng từ A đến C không qua B. Có bao nhiêu cách đi từ A đến C?
  - **Đáp án:** 23
    1. Chia thành hai trường hợp rời nhau: đi qua B, hoặc đi thẳng không qua B.
    2. Đi qua B: chọn đường A đến B rồi đường B đến C, theo quy tắc nhân có 3 . 6 = 18 cách.
    3. Đi thẳng: có 5 cách.
    4. Hai trường hợp không có cách đi nào chung, theo quy tắc cộng: 18 + 5 = 23.

### Mệnh đề và các phép nối (`tr_t1_menh_de`)

- `tr_t1_md_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Câu "Hãy ngồi xuống luyện công!" là một mệnh đề.
  - **Đáp án:** Sai
    1. Mệnh đề là một câu khẳng định có giá trị đúng hoặc sai, và chỉ một trong hai.
    2. Đây là một câu mệnh lệnh: hỏi nó đúng hay sai là vô nghĩa.
    3. Vậy nó không phải là mệnh đề.
- `tr_t1_md_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho p là mệnh đề đúng và q là mệnh đề sai. Mệnh đề nào sau đây đúng?
    - **(đúng)** p hoặc q
    - p và q
    - p => q
    - p <=> q
  - **Đáp án:** p hoặc q
    1. p hoặc q chỉ sai khi cả hai đều sai; ở đây p đúng nên nó đúng.
    2. p và q cần cả hai đúng, mà q sai, nên sai.
    3. p => q sai vì vế trước đúng mà vế sau sai.
    4. p <=> q sai vì p và q khác chân trị.
- `tr_t1_md_03` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mệnh đề "Nếu 2 + 2 = 5 thì 3 là số chẵn" là mệnh đề đúng.
  - **Đáp án:** Đúng
    1. Đây là mệnh đề kéo theo p => q với p: "2 + 2 = 5" và q: "3 là số chẵn".
    2. p sai và q cũng sai.
    3. Kéo theo chỉ sai khi vế trước đúng và vế sau sai; ở đây vế trước sai nên cả mệnh đề đúng.
- `tr_t1_md_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi mệnh đề với điều kiện để nó sai.
  - **Đáp án (ghép đúng):**
    - p và q — sai khi ít nhất một trong p, q sai
    - p hoặc q — chỉ sai khi cả p và q đều sai
    - p => q — chỉ sai khi p đúng và q sai
    - p <=> q — sai khi p và q khác chân trị
  - **Lời giải:**
    1. Hội p và q đúng khi cả hai đều đúng, nên chỉ cần một vế sai là nó sai.
    2. Tuyển p hoặc q đúng khi có ít nhất một vế đúng, nên nó chỉ sai khi cả hai cùng sai.
    3. Kéo theo chỉ sai trong đúng một trường hợp: vế trước đúng, vế sau sai.
    4. Tương đương đúng khi hai vế cùng chân trị, sai khi chúng khác nhau.
- `tr_g1_chan_tri` · bậc 1 (Nhập môn) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho p là mệnh đề đúng và q là mệnh đề sai. Mệnh đề (không p) và q đúng.
  - **Đáp án:** Sai
    1. p đúng, mà phủ định đổi chân trị: không p sai.
    2. không p sai và q sai, mà hội chỉ đúng khi cả hai vế đều đúng: (không p) và q sai.
    3. Vậy mệnh đề (không p) và q sai, nên câu đã cho sai.
  - **Câu hỏi:** Cho p là mệnh đề sai và q là mệnh đề sai. Mệnh đề (không p) và q đúng.
  - **Đáp án:** Sai
    1. p sai, mà phủ định đổi chân trị: không p đúng.
    2. không p đúng và q sai, mà hội chỉ đúng khi cả hai vế đều đúng: (không p) và q sai.
    3. Vậy mệnh đề (không p) và q sai, nên câu đã cho sai.
  - **Câu hỏi:** Cho p là mệnh đề đúng và q là mệnh đề sai. Mệnh đề p => q đúng.
  - **Đáp án:** Sai
    1. p đúng và q sai, mà kéo theo chỉ sai khi vế trước đúng và vế sau sai: p => q sai.
    2. Vậy mệnh đề p => q sai, nên câu đã cho sai.
- `tr_t1_md_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phủ định của mệnh đề "Mọi đệ tử đều đã luyện xong công pháp" là mệnh đề nào?
    - **(đúng)** Có ít nhất một đệ tử chưa luyện xong công pháp
    - Mọi đệ tử đều chưa luyện xong công pháp
    - Không có đệ tử nào luyện xong công pháp
    - Có ít nhất một đệ tử đã luyện xong công pháp
  - **Đáp án:** Có ít nhất một đệ tử chưa luyện xong công pháp
    1. Mệnh đề "mọi x đều có tính chất P" sai khi chỉ cần một x không có tính chất P.
    2. Vậy phủ định của nó là "có ít nhất một x không có tính chất P".
    3. "Mọi đệ tử đều chưa luyện xong" mạnh hơn nhiều so với phủ định: nó sai ngay khi có một người đã luyện xong.
- `tr_t1_md_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Biết mệnh đề p => q sai. Khi đó q là mệnh đề sai.
  - **Đáp án:** Đúng
    1. Kéo theo p => q chỉ sai trong đúng một trường hợp: p đúng và q sai.
    2. Biết p => q sai thì phải đang ở trường hợp đó.
    3. Vậy q sai (và p đúng).
- `tr_t1_md_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: cho p đúng, q sai, r đúng; tìm chân trị của (p => q) hoặc (q <=> r).
  - **Lời giải đưa ra (có một bước sai):**
    1. p đúng và q sai nên p => q sai.
    2. q sai và r đúng nên q <=> r đúng.   **<- bước sai đầu tiên**
    3. Một vế sai, một vế đúng nên phép hoặc cho giá trị đúng.
    4. Vậy (p => q) hoặc (q <=> r) đúng.
  - **Đáp án:** Bước 2: q sai và r đúng nên q <=> r đúng.
  - **Vì sao sai, và bước đúng:**
    1. Tương đương chỉ đúng khi hai vế cùng chân trị; q sai còn r đúng nên q <=> r sai.
    2. Khi đó cả hai vế của phép hoặc đều sai.
    3. Vậy (p => q) hoặc (q <=> r) sai.
- `tr_g1_chan_tri_hop` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho p đúng, q sai, r sai. Mệnh đề (q <=> p) <=> (không r) đúng.
  - **Đáp án:** Sai
    1. Tính từ trong ngoặc ra ngoài.
    2. q sai và p đúng, mà tương đương đúng khi hai vế cùng chân trị: q <=> p sai.
    3. r sai, mà phủ định đổi chân trị: không r đúng.
    4. q <=> p sai và không r đúng, mà tương đương đúng khi hai vế cùng chân trị: (q <=> p) <=> (không r) sai.
    5. Vậy câu đã cho sai.
  - **Câu hỏi:** Cho p sai, q sai, r đúng. Mệnh đề (p => q) => r đúng.
  - **Đáp án:** Đúng
    1. Tính từ trong ngoặc ra ngoài.
    2. p sai và q sai, mà kéo theo chỉ sai khi vế trước đúng và vế sau sai: p => q đúng.
    3. p => q đúng và r đúng, mà kéo theo chỉ sai khi vế trước đúng và vế sau sai: (p => q) => r đúng.
    4. Vậy câu đã cho đúng.
  - **Câu hỏi:** Cho p đúng, q sai, r đúng. Mệnh đề (r <=> (không q)) và p đúng.
  - **Đáp án:** Đúng
    1. Tính từ trong ngoặc ra ngoài.
    2. q sai, mà phủ định đổi chân trị: không q đúng.
    3. r đúng và không q đúng, mà tương đương đúng khi hai vế cùng chân trị: r <=> (không q) đúng.
    4. r <=> (không q) đúng và p đúng, mà hội chỉ đúng khi cả hai vế đều đúng: (r <=> (không q)) và p đúng.
    5. Vậy câu đã cho đúng.

### Bảng chân trị và tương đương logic (`tr_t1_bang_chan_tri`)

- `tr_t1_bc_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bảng chân trị của một mệnh đề theo ba biến p, q, r có bao nhiêu dòng?
  - **Đáp án:** 8
    1. Mỗi dòng ứng với một cách gán chân trị cho p, q, r.
    2. Mỗi biến có 2 giá trị: đúng hoặc sai.
    3. Theo quy tắc nhân có 2 . 2 . 2 = 8 dòng.
- `tr_t1_bc_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mệnh đề p hoặc (không p) là một hằng đúng.
  - **Đáp án:** Đúng
    1. Hằng đúng là mệnh đề đúng ở mọi dòng của bảng chân trị.
    2. Nếu p đúng thì vế p đúng; nếu p sai thì vế không p đúng.
    3. Dòng nào cũng có một vế đúng, nên phép hoặc luôn đúng.
- `tr_t1_bc_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mệnh đề nào tương đương logic với không (p và q)?
    - **(đúng)** (không p) hoặc (không q)
    - (không p) và (không q)
    - p hoặc q
    - (không p) và q
  - **Đáp án:** (không p) hoặc (không q)
    1. Theo luật De Morgan, phủ định của một hội là tuyển của các phủ định.
    2. Vậy không (p và q) tương đương với (không p) hoặc (không q).
    3. Kiểm tra một dòng: p đúng, q sai thì không (p và q) đúng, còn (không p) và (không q) sai, nên phương án thứ hai sai.
- `tr_g1_tuong_duong` · bậc 1 (Nhập môn) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hai mệnh đề q => p và (không p) => (không q) tương đương logic.
  - **Đáp án:** Đúng
    1. Lập bảng chân trị theo p, q: ở mọi dòng hai mệnh đề có cùng chân trị.
    2. Đây chính là mệnh đề phản đảo.
    3. Vậy hai mệnh đề tương đương logic.
  - **Câu hỏi:** Hai mệnh đề (không p) <=> q và không (p <=> q) tương đương logic.
  - **Đáp án:** Đúng
    1. Lập bảng chân trị theo p, q: ở mọi dòng hai mệnh đề có cùng chân trị.
    2. Đây chính là phủ định của tương đương.
    3. Vậy hai mệnh đề tương đương logic.
  - **Câu hỏi:** Hai mệnh đề q => p và (không q) => (không p) tương đương logic.
  - **Đáp án:** Sai
    1. Chỉ cần một dòng của bảng chân trị mà hai mệnh đề khác chân trị: p đúng, q sai.
    2. Khi đó q => p đúng, còn (không q) => (không p) sai.
    3. Vậy hai mệnh đề không tương đương logic.
- `tr_t1_bc_04` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mệnh đề phản đảo của p => q là mệnh đề nào?
    - **(đúng)** (không q) => (không p)
    - q => p
    - (không p) => (không q)
    - p => (không q)
  - **Đáp án:** (không q) => (không p)
    1. Phản đảo của p => q là (không q) => (không p): đổi chỗ hai vế và phủ định cả hai.
    2. Phản đảo luôn tương đương logic với mệnh đề ban đầu.
    3. q => p là mệnh đề đảo, còn (không p) => (không q) là mệnh đề phản; cả hai đều không tương đương với p => q.
- `tr_t1_bc_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mệnh đề p => q tương đương logic với mệnh đề q => p.
  - **Đáp án:** Sai
    1. Tìm một dòng mà hai mệnh đề khác chân trị: lấy p sai, q đúng.
    2. Khi đó p => q đúng (vế trước sai), còn q => p sai (vế trước đúng, vế sau sai).
    3. Vậy hai mệnh đề không tương đương: đổi chỗ hai vế của kéo theo làm đổi nghĩa.
- `tr_t1_bc_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng tỏ (p và (p => q)) => q là một hằng đúng mà không cần lập cả bảng chân trị.
  - **Đáp án (thứ tự đúng):**
    1. Giả sử có một dòng làm mệnh đề sai.
    2. Kéo theo chỉ sai khi vế trước đúng và vế sau sai, nên ở dòng đó q sai và p và (p => q) đúng.
    3. Từ p và (p => q) đúng suy ra p đúng và p => q đúng.
    4. Nhưng p đúng mà q sai thì p => q sai, mâu thuẫn.
    5. Vậy không có dòng nào làm mệnh đề sai: nó là hằng đúng.
  - **Lời giải:**
    1. Cách làm là phản chứng: giả sử mệnh đề sai ở một dòng rồi suy ra điều vô lý.
    2. Mệnh đề ngoài cùng là một kéo theo, nên sai buộc vế trước đúng, vế sau sai.
    3. Vế trước đúng cho p đúng và p => q đúng; cùng với q sai thì p => q lại sai: mâu thuẫn.
    4. Đây là quy tắc suy luận quen thuộc: có p và có p => q thì có q.
- `tr_t1_bc_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi mệnh đề bên trái với mệnh đề tương đương logic với nó.
  - **Đáp án (ghép đúng):**
    - p => q — (không p) hoặc q
    - không (p hoặc q) — (không p) và (không q)
    - không (không p) — p
    - p <=> q — (p => q) và (q => p)
  - **Lời giải:**
    1. p => q chỉ sai khi p đúng và q sai, đúng như (không p) hoặc q.
    2. Luật De Morgan: phủ định của tuyển là hội của các phủ định.
    3. Phủ định hai lần trả lại chân trị ban đầu.
    4. Tương đương là kéo theo theo cả hai chiều.
- `tr_t1_bc_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: viết mệnh đề không (p => q) mà không dùng dấu kéo theo.
  - **Lời giải đưa ra (có một bước sai):**
    1. p => q tương đương với (không p) hoặc q.
    2. Phủ định hai vế: không (p => q) tương đương với không ((không p) hoặc q).
    3. Theo luật De Morgan, không ((không p) hoặc q) tương đương với (không (không p)) hoặc (không q).   **<- bước sai đầu tiên**
    4. Bỏ phủ định kép: không (p => q) tương đương với p hoặc (không q).
  - **Đáp án:** Bước 3: Theo luật De Morgan, không ((không p) hoặc q) tương đương với (không (không p)) hoặc (không q).
  - **Vì sao sai, và bước đúng:**
    1. Luật De Morgan đổi phép hoặc thành phép và khi đưa phủ định vào trong.
    2. Đúng là: không ((không p) hoặc q) tương đương với (không (không p)) và (không q).
    3. Bỏ phủ định kép: không (p => q) tương đương với p và (không q). Kiểm tra: p => q sai đúng khi p đúng và q sai.
- `tr_g1_dem_dong_dung` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Lập bảng chân trị của mệnh đề (p <=> r) và q theo ba biến p, q, r. Có bao nhiêu dòng mà mệnh đề đó đúng?
  - **Đáp án:** 2
    1. Ba biến cho 2 . 2 . 2 = 8 dòng, mỗi dòng là một bộ chân trị của (p, q, r).
    2. Với từng dòng, tính phần trong ngoặc trước rồi đến phép nối ngoài cùng.
    3. Các dòng làm mệnh đề đúng, viết (p, q, r) với Đ là đúng, S là sai: (Đ, Đ, Đ); (S, Đ, S).
    4. Có 2 dòng.
  - **Câu hỏi:** Lập bảng chân trị của mệnh đề p => (r hoặc q) theo ba biến p, q, r. Có bao nhiêu dòng mà mệnh đề đó đúng?
  - **Đáp án:** 7
    1. Ba biến cho 2 . 2 . 2 = 8 dòng, mỗi dòng là một bộ chân trị của (p, q, r).
    2. Với từng dòng, tính phần trong ngoặc trước rồi đến phép nối ngoài cùng.
    3. Các dòng làm mệnh đề đúng, viết (p, q, r) với Đ là đúng, S là sai: (Đ, Đ, Đ); (Đ, Đ, S); (Đ, S, Đ); (S, Đ, Đ); (S, Đ, S); (S, S, Đ); (S, S, S).
    4. Có 7 dòng.
  - **Câu hỏi:** Lập bảng chân trị của mệnh đề p <=> (r và q) theo ba biến p, q, r. Có bao nhiêu dòng mà mệnh đề đó đúng?
  - **Đáp án:** 4
    1. Ba biến cho 2 . 2 . 2 = 8 dòng, mỗi dòng là một bộ chân trị của (p, q, r).
    2. Với từng dòng, tính phần trong ngoặc trước rồi đến phép nối ngoài cùng.
    3. Các dòng làm mệnh đề đúng, viết (p, q, r) với Đ là đúng, S là sai: (Đ, Đ, Đ); (S, Đ, S); (S, S, Đ); (S, S, S).
    4. Có 4 dòng.

### Chứng minh bằng quy nạp (`tr_t1_quy_nap`)

- `tr_t1_qn_01` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi chứng minh bằng quy nạp rằng mệnh đề P(n) đúng với mọi số nguyên n >= 1, bước cơ sở là gì?
    - **(đúng)** Kiểm tra P(1) đúng
    - Kiểm tra P(0) đúng
    - Giả sử P(n) đúng với mọi n
    - Kiểm tra P(n) đúng với vài giá trị n lớn
  - **Đáp án:** Kiểm tra P(1) đúng
    1. Bước cơ sở kiểm tra mệnh đề tại giá trị nhỏ nhất của n mà ta cần, ở đây là n = 1.
    2. Giả sử P(n) đúng với mọi n là đem điều cần chứng minh làm giả thiết, không được phép.
    3. Thử vài giá trị lớn không chứng minh được gì cho mọi n.
- `tr_t1_qn_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong bước quy nạp, ta giả sử P(k) đúng với một số k bất kỳ (k >= 1) rồi chứng minh P(k + 1) đúng.
  - **Đáp án:** Đúng
    1. Bước quy nạp chứng minh phép kéo theo P(k) => P(k + 1) cho mọi k >= 1.
    2. Giả thiết P(k) đúng gọi là giả thiết quy nạp.
    3. Cùng với bước cơ sở P(1), ta đi được từ 1 lên 2, từ 2 lên 3, và cứ thế đến mọi n.
- `tr_t1_qn_03` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh 1 + 2 + ... + n = n(n + 1)/2 với mọi n >= 1 bằng quy nạp.
  - **Đáp án (thứ tự đúng):**
    1. Bước cơ sở: với n = 1, vế trái là 1, vế phải là 1 . 2/2 = 1.
    2. Giả thiết quy nạp: giả sử 1 + 2 + ... + k = k(k + 1)/2 với một k >= 1.
    3. Cộng k + 1 vào hai vế: 1 + 2 + ... + (k + 1) = k(k + 1)/2 + (k + 1).
    4. Rút gọn vế phải thành (k + 1)(k + 2)/2, chính là công thức với n = k + 1.
    5. Theo nguyên lý quy nạp, đẳng thức đúng với mọi n >= 1.
  - **Lời giải:**
    1. Một chứng minh quy nạp luôn có thứ tự: cơ sở, giả thiết, biến đổi để đi tới k + 1, kết luận.
    2. Phép rút gọn: k(k + 1)/2 + (k + 1) = (k + 1)(k/2 + 1) = (k + 1)(k + 2)/2.
    3. Kết luận chỉ được viết sau khi đã làm xong cả hai bước.
- `tr_g1_tong_quy_nap` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1 + 2 + 3 + ... + n = n(n + 1)/2 với mọi n >= 1. Dùng công thức đó, tính 1 + 2 + 3 + ... + 9.
  - **Đáp án:** 45
    1. Tổng cần tính là vế trái của công thức với n = 9.
    2. Thay n = 9 vào vế phải: 9 . 10/2 = 45.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1 + 2 + 3 + ... + n = n(n + 1)/2 với mọi n >= 1. Dùng công thức đó, tính 1 + 2 + 3 + ... + 10.
  - **Đáp án:** 55
    1. Tổng cần tính là vế trái của công thức với n = 10.
    2. Thay n = 10 vào vế phải: 10 . 11/2 = 55.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1 + 2 + 3 + ... + n = n(n + 1)/2 với mọi n >= 1. Dùng công thức đó, tính 1 + 2 + 3 + ... + 39.
  - **Đáp án:** 780
    1. Tổng cần tính là vế trái của công thức với n = 39.
    2. Thay n = 39 vào vế phải: 39 . 40/2 = 780.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.
- `tr_t1_qn_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm số nguyên dương n_0 nhỏ nhất sao cho bất đẳng thức 2^n > n^2 đúng với mọi số nguyên n >= n_0.
  - **Đáp án:** 5
    1. Thử các giá trị nhỏ: n = 1: 2 > 1 đúng; n = 2: 4 > 4 sai; n = 3: 8 > 9 sai; n = 4: 16 > 16 sai; n = 5: 32 > 25 đúng.
    2. Vì n = 4 sai nên n_0 không thể nhỏ hơn 5.
    3. Từ n = 5 trở đi bất đẳng thức đúng, chứng minh bằng quy nạp: nếu 2^k > k^2 với k >= 5 thì 2^(k + 1) > 2k^2, và 2k^2 >= (k + 1)^2 khi k >= 3.
    4. Vậy n_0 = 5.
- `tr_t1_qn_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: chứng minh 3^n - 1 chia hết cho 2 với mọi n >= 1.
  - **Lời giải đưa ra (có một bước sai):**
    1. Bước cơ sở: n = 1 thì 3^1 - 1 = 2, chia hết cho 2.
    2. Giả sử 3^k - 1 chia hết cho 2 với một k >= 1.
    3. Ta có 3^(k + 1) - 1 = 3 . 3^k - 1 = 3(3^k - 1) + 4.   **<- bước sai đầu tiên**
    4. 3(3^k - 1) chia hết cho 2 theo giả thiết quy nạp, và 4 chia hết cho 2, nên 3^(k + 1) - 1 chia hết cho 2.
    5. Theo nguyên lý quy nạp, 3^n - 1 chia hết cho 2 với mọi n >= 1.
  - **Đáp án:** Bước 3: Ta có 3^(k + 1) - 1 = 3 . 3^k - 1 = 3(3^k - 1) + 4.
  - **Vì sao sai, và bước đúng:**
    1. Khai triển lại: 3(3^k - 1) + 4 = 3^(k + 1) - 3 + 4 = 3^(k + 1) + 1, không phải 3^(k + 1) - 1.
    2. Viết đúng là 3^(k + 1) - 1 = 3(3^k - 1) + 2.
    3. Vì 2 chia hết cho 2 nên kết luận vẫn đúng; chỉ bước biến đổi bị sai.
- `tr_t1_qn_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Để chứng minh P(n) đúng với mọi n >= 1, chỉ cần chứng minh P(k) => P(k + 1) với mọi k >= 1, không cần bước cơ sở.
  - **Đáp án:** Sai
    1. Lấy P(n): "n = n + 1". Nếu k = k + 1 thì cộng 1 vào hai vế được k + 1 = k + 2, nên bước quy nạp đúng.
    2. Nhưng P(1): "1 = 2" sai, và thực ra P(n) sai với mọi n.
    3. Bước quy nạp chỉ chuyển cái đúng đi tiếp; phải có bước cơ sở để có cái đúng ban đầu.
- `tr_t1_qn_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi chứng minh mỗi đẳng thức sau bằng quy nạp, ở bước từ n = k sang n = k + 1 ta cộng thêm vào vế trái một số hạng. Ghép mỗi đẳng thức với số hạng đó.
  - **Đáp án (ghép đúng):**
    - 1 + 3 + ... + (2n - 1) = n^2 — 2k + 1
    - 1 + 2 + ... + n = n(n + 1)/2 — k + 1
    - 1^2 + 2^2 + ... + n^2 = n(n + 1)(2n + 1)/6 — (k + 1)^2
    - 1 + 2 + 4 + ... + 2^(n - 1) = 2^n - 1 — 2^k
  - **Lời giải:**
    1. Số hạng thêm vào là số hạng cuối của vế trái khi thay n = k + 1.
    2. Số lẻ thứ k + 1 là 2(k + 1) - 1 = 2k + 1; số tự nhiên thứ k + 1 là k + 1.
    3. Bình phương thứ k + 1 là (k + 1)^2; lũy thừa cuối 2^(n - 1) với n = k + 1 là 2^k.
- `tr_g1_tong_quy_nap_2` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1^3 + 2^3 + ... + n^3 = (n(n + 1)/2)^2 với mọi n >= 1. Dùng công thức đó, tính 1^3 + 2^3 + ... + 5^3.
  - **Đáp án:** 225
    1. Tổng cần tính là vế trái của công thức với n = 5.
    2. Thay n = 5 vào vế phải: (5 . 6/2)^2 = 225.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1^2 + 2^2 + ... + n^2 = n(n + 1)(2n + 1)/6 với mọi n >= 1. Dùng công thức đó, tính 1^2 + 2^2 + ... + 5^2.
  - **Đáp án:** 55
    1. Tổng cần tính là vế trái của công thức với n = 5.
    2. Thay n = 5 vào vế phải: 5 . 6 . 11/6 = 55.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.
  - **Câu hỏi:** Bằng quy nạp ta chứng minh được 1^3 + 2^3 + ... + n^3 = (n(n + 1)/2)^2 với mọi n >= 1. Dùng công thức đó, tính 1^3 + 2^3 + ... + 12^3.
  - **Đáp án:** 6084
    1. Tổng cần tính là vế trái của công thức với n = 12.
    2. Thay n = 12 vào vế phải: (12 . 13/2)^2 = 6084.
    3. Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng.

## Tầng 2: Bài toán đếm

54 dạng câu (41 câu viết tay, 13 bộ sinh câu); 54 chưa duyệt.

### Chỉnh hợp lặp và không lặp (`tr_t2_chinh_hop`)

- `tr_t2_ch_01` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một mật lệnh gồm 3 ký tự, mỗi ký tự là một trong 5 phù văn, được dùng lặp lại. Có bao nhiêu mật lệnh?
    - **(đúng)** 125
    - 60
    - 10
    - 243
  - **Đáp án:** 125
    1. Mật lệnh là một dãy 3 ký tự có thứ tự, được lặp: chỉnh hợp lặp chập 3 của 5.
    2. Mỗi vị trí có 5 cách chọn.
    3. 5^3 = 125. (60 là số mật lệnh khi không được lặp, 243 = 3^5 là nhầm vai trò của 3 và 5.)
- `tr_t2_ch_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với 0 <= k <= n, số chỉnh hợp không lặp chập k của n phần tử là A_n^k = n!/(n - k)!.
  - **Đáp án:** Đúng
    1. Chọn lần lượt k phần tử khác nhau có thứ tự: n cách, rồi n - 1 cách, ..., đến n - k + 1 cách.
    2. Tích n(n - 1)...(n - k + 1) bằng n! chia cho (n - k)!, vì (n - k)! là phần đuôi bị thiếu.
    3. Vậy A_n^k = n!/(n - k)!.
- `tr_t2_ch_05` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi biểu thức với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - A_5^2 — 20
    - A_4^3 — 24
    - 2^4 — 16
    - A_7^2 — 42
  - **Lời giải:**
    1. A_n^k là tích của k số nguyên liên tiếp giảm dần bắt đầu từ n.
    2. A_5^2 = 5 . 4 = 20; A_4^3 = 4 . 3 . 2 = 24; A_7^2 = 7 . 6 = 42.
    3. 2^4 = 16 là số chỉnh hợp lặp chập 4 của 2 phần tử.
- `tr_g2_chinh_hop_lap` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một mật lệnh gồm 4 ký tự viết liền nhau, mỗi ký tự là một trong 4 phù văn và một phù văn được dùng nhiều lần. Có bao nhiêu mật lệnh khác nhau?
  - **Đáp án:** 256
    1. Mật lệnh là một dãy có thứ tự 4 ký tự, được lặp lại: một chỉnh hợp lặp chập 4 của 4.
    2. Mỗi vị trí có 4 cách chọn, không phụ thuộc các vị trí khác.
    3. Số mật lệnh là 4^4 = 256.
  - **Câu hỏi:** Một mật lệnh gồm 2 ký tự viết liền nhau, mỗi ký tự là một trong 2 phù văn và một phù văn được dùng nhiều lần. Có bao nhiêu mật lệnh khác nhau?
  - **Đáp án:** 4
    1. Mật lệnh là một dãy có thứ tự 2 ký tự, được lặp lại: một chỉnh hợp lặp chập 2 của 2.
    2. Mỗi vị trí có 2 cách chọn, không phụ thuộc các vị trí khác.
    3. Số mật lệnh là 2^2 = 4.
  - **Câu hỏi:** Một mật lệnh gồm 4 ký tự viết liền nhau, mỗi ký tự là một trong 5 phù văn và một phù văn được dùng nhiều lần. Có bao nhiêu mật lệnh khác nhau?
  - **Đáp án:** 625
    1. Mật lệnh là một dãy có thứ tự 4 ký tự, được lặp lại: một chỉnh hợp lặp chập 4 của 5.
    2. Mỗi vị trí có 5 cách chọn, không phụ thuộc các vị trí khác.
    3. Số mật lệnh là 5^4 = 625.
- `tr_t2_ch_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đại hội có 8 tông môn tranh tài. Có bao nhiêu cách trao ba giải nhất, nhì, ba cho ba tông môn khác nhau?
  - **Đáp án:** 336
    1. Ba giải khác nhau nên thứ tự có ý nghĩa, và một tông môn không nhận hai giải: chỉnh hợp không lặp chập 3 của 8.
    2. Giải nhất 8 cách, giải nhì 7 cách, giải ba 6 cách.
    3. A_8^3 = 8 . 7 . 6 = 336.
- `tr_t2_ch_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: xếp 4 đệ tử vào 6 phòng, mỗi phòng nhiều nhất một người; có bao nhiêu cách?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi cách xếp cho mỗi đệ tử một phòng, các phòng khác nhau và có thứ tự theo người.
    2. Đó là một chỉnh hợp không lặp chập 4 của 6 phòng.
    3. A_6^4 = 6!/4! = 30.   **<- bước sai đầu tiên**
    4. Vậy có 30 cách xếp.
  - **Đáp án:** Bước 3: A_6^4 = 6!/4! = 30.
  - **Vì sao sai, và bước đúng:**
    1. Công thức là A_n^k = n!/(n - k)!, nên A_6^4 = 6!/2!, không phải 6!/4!.
    2. A_6^4 = 6 . 5 . 4 . 3 = 360.
    3. Vậy có 360 cách xếp.
- `tr_g2_chinh_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Từ 7 đệ tử, chọn ra 4 người giữ 4 chức vụ khác nhau (chưởng môn, đại trưởng lão, nhị trưởng lão, chấp sự), mỗi người giữ một chức. Có bao nhiêu cách?
  - **Đáp án:** 840
    1. Chức vụ khác nhau nên thứ tự chọn có ý nghĩa, và một người không giữ hai chức: đây là chỉnh hợp không lặp chập 4 của 7.
    2. Chức thứ nhất có 7 cách, mỗi chức sau ít hơn một cách.
    3. A_7^4 = 7 . 6 . 5 . 4 = 840.
  - **Câu hỏi:** Từ 5 đệ tử, chọn ra 2 người giữ 2 chức vụ khác nhau (chưởng môn, đại trưởng lão), mỗi người giữ một chức. Có bao nhiêu cách?
  - **Đáp án:** 20
    1. Chức vụ khác nhau nên thứ tự chọn có ý nghĩa, và một người không giữ hai chức: đây là chỉnh hợp không lặp chập 2 của 5.
    2. Chức thứ nhất có 5 cách, mỗi chức sau ít hơn một cách.
    3. A_5^2 = 5 . 4 = 20.
  - **Câu hỏi:** Từ 8 đệ tử, chọn ra 4 người giữ 4 chức vụ khác nhau (chưởng môn, đại trưởng lão, nhị trưởng lão, chấp sự), mỗi người giữ một chức. Có bao nhiêu cách?
  - **Đáp án:** 1680
    1. Chức vụ khác nhau nên thứ tự chọn có ý nghĩa, và một người không giữ hai chức: đây là chỉnh hợp không lặp chập 4 của 8.
    2. Chức thứ nhất có 8 cách, mỗi chức sau ít hơn một cách.
    3. A_8^4 = 8 . 7 . 6 . 5 = 1680.

### Hoán vị và hoán vị lặp (`tr_t2_hoan_vi`)

- `tr_t2_hv_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu cách xếp 5 cuốn bí kíp khác nhau lên một giá sách thành một hàng?
  - **Đáp án:** 120
    1. Mỗi cách xếp là một hoán vị của 5 cuốn sách.
    2. Vị trí đầu 5 cách, rồi 4, 3, 2, 1 cách.
    3. 5! = 5 . 4 . 3 . 2 . 1 = 120.
- `tr_t2_hv_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Theo quy ước, 0! = 0, vì tích của không số nào bằng 0.
  - **Đáp án:** Sai
    1. Quy ước là 0! = 1.
    2. Có đúng một cách xếp 0 vật: không làm gì cả. Tích rỗng bằng 1, như tổng rỗng bằng 0.
    3. Quy ước này giữ được công thức n! = n . (n - 1)! khi n = 1, và A_n^n = n!/0! = n!.
- `tr_g2_hoan_vi` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu cách xếp 4 lá cờ khác màu thành một hàng?
  - **Đáp án:** 24
    1. Mỗi cách xếp là một hoán vị của 4 vật khác nhau.
    2. Vị trí đầu có 4 cách, vị trí sau ít hơn một cách, cho đến vị trí cuối còn 1 cách.
    3. 4! = 4 . 3 . 2 . 1 = 24.
  - **Câu hỏi:** Có bao nhiêu cách xếp 3 đệ tử thành một hàng dọc?
  - **Đáp án:** 6
    1. Mỗi cách xếp là một hoán vị của 3 vật khác nhau.
    2. Vị trí đầu có 3 cách, vị trí sau ít hơn một cách, cho đến vị trí cuối còn 1 cách.
    3. 3! = 3 . 2 . 1 = 6.
  - **Câu hỏi:** Có bao nhiêu cách xếp 4 lá cờ khác màu thành một hàng?
  - **Đáp án:** 24
    1. Mỗi cách xếp là một hoán vị của 4 vật khác nhau.
    2. Vị trí đầu có 4 cách, vị trí sau ít hơn một cách, cho đến vị trí cuối còn 1 cách.
    3. 4! = 4 . 3 . 2 . 1 = 24.
- `tr_t2_hv_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp 3 viên linh thạch đỏ giống hệt nhau và 2 viên xanh giống hệt nhau thành một hàng. Có bao nhiêu hàng khác nhau?
  - **Đáp án:** 10
    1. Nếu 5 viên đều khác nhau thì có 5! = 120 cách.
    2. Đổi chỗ 3 viên đỏ cho nhau (3! cách) hay 2 viên xanh cho nhau (2! cách) không tạo hàng mới.
    3. Số hàng là 5!/(3! . 2!) = 120/12 = 10.
    4. Cũng có thể nghĩ: chọn 2 trong 5 vị trí cho viên xanh, C_5^2 = 10.
- `tr_t2_hv_04` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu cách xếp 6 người ngồi quanh một bàn tròn, nếu hai cách được coi là như nhau khi xoay bàn thì trùng nhau?
    - **(đúng)** 120
    - 720
    - 60
    - 360
  - **Đáp án:** 120
    1. Xếp thành hàng có 6! = 720 cách.
    2. Mỗi cách xếp quanh bàn ứng với 6 cách xếp hàng khác nhau (cắt vòng tròn ở 6 chỗ), vì xoay không đổi cách ngồi.
    3. Số cách là 720/6 = 5! = 120.
- `tr_t2_hv_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước đếm số cách xếp 5 người thành hàng sao cho An và Bình đứng cạnh nhau.
  - **Đáp án (thứ tự đúng):**
    1. Buộc An và Bình thành một khối, coi khối đó như một người.
    2. Còn 4 đối tượng để xếp thành hàng: 4! = 24 cách.
    3. Với mỗi cách xếp đó, An và Bình trong khối còn đổi chỗ được cho nhau: 2 cách.
    4. Theo quy tắc nhân: 24 . 2 = 48 cách.
  - **Lời giải:**
    1. Ý chính: hai người luôn cạnh nhau thì có thể dán họ lại thành một khối.
    2. Khối cùng 3 người còn lại là 4 đối tượng, có 4! cách xếp.
    3. Trong khối có 2 thứ tự (An Bình hoặc Bình An), nên nhân thêm 2: 48 cách.
- `tr_t2_hv_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: xếp 6 người thành hàng sao cho An và Bình không đứng cạnh nhau.
  - **Lời giải đưa ra (có một bước sai):**
    1. Số cách xếp 6 người tùy ý là 6! = 720.
    2. Đếm các cách An và Bình đứng cạnh nhau: buộc hai người thành một khối, xếp 5 đối tượng được 5! = 120 cách.
    3. Vậy có 120 cách An và Bình đứng cạnh nhau.   **<- bước sai đầu tiên**
    4. Số cách hai người không đứng cạnh nhau là 720 - 120 = 600.
  - **Đáp án:** Bước 3: Vậy có 120 cách An và Bình đứng cạnh nhau.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 quên rằng trong khối An và Bình còn đổi chỗ được: An Bình hoặc Bình An.
    2. Số cách đứng cạnh nhau là 2 . 120 = 240.
    3. Số cách không đứng cạnh nhau là 720 - 240 = 480.
- `tr_t2_hv_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi cách xếp với số cách của nó.
  - **Đáp án (ghép đúng):**
    - Xếp 4 người khác nhau thành hàng — 24
    - Xếp 4 người quanh bàn tròn, xoay bàn coi như không đổi — 6
    - Xếp các chữ A, A, A, B thành một xâu — 4
    - Xếp 5 người khác nhau thành hàng — 120
  - **Lời giải:**
    1. 4 người thành hàng: 4! = 24; 5 người thành hàng: 5! = 120.
    2. Quanh bàn tròn: chia số cách xếp hàng cho số người, 24/4 = 3! = 6.
    3. A, A, A, B: chỉ cần chọn vị trí cho chữ B, 4 cách (bằng 4!/3!).
- `tr_g2_canh_nhau` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xếp 5 đệ tử, trong đó có Lam và Mai, thành một hàng ngang. Có bao nhiêu cách xếp mà Lam và Mai đứng cạnh nhau?
  - **Đáp án:** 48
    1. Buộc Lam và Mai thành một khối, coi như một người.
    2. Xếp 4 'người' thành hàng: 4! = 24 cách; trong khối, hai người đổi chỗ được: 2 cách.
    3. Số cách hai người đứng cạnh nhau là 2 . 24 = 48.
  - **Câu hỏi:** Xếp 4 đệ tử, trong đó có An và Bình, thành một hàng ngang. Có bao nhiêu cách xếp mà An và Bình không đứng cạnh nhau?
  - **Đáp án:** 12
    1. Buộc An và Bình thành một khối, coi như một người.
    2. Xếp 3 'người' thành hàng: 3! = 6 cách; trong khối, hai người đổi chỗ được: 2 cách.
    3. Số cách hai người đứng cạnh nhau là 2 . 6 = 12.
    4. Lấy tổng số cách xếp trừ đi: 4! - 12 = 24 - 12 = 12.
  - **Câu hỏi:** Xếp 5 đệ tử, trong đó có Lam và Mai, thành một hàng ngang. Có bao nhiêu cách xếp mà Lam và Mai đứng cạnh nhau?
  - **Đáp án:** 48
    1. Buộc Lam và Mai thành một khối, coi như một người.
    2. Xếp 4 'người' thành hàng: 4! = 24 cách; trong khối, hai người đổi chỗ được: 2 cách.
    3. Số cách hai người đứng cạnh nhau là 2 . 24 = 48.
- `tr_g2_hoan_vi_lap` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xếp 4 viên linh thạch thành một hàng: 1 viên đỏ, 3 viên xanh; các viên cùng màu giống hệt nhau. Có bao nhiêu hàng khác nhau?
  - **Đáp án:** 4
    1. Nếu mọi viên đều khác nhau thì có 4! cách xếp.
    2. Đổi chỗ các viên cùng màu cho nhau không tạo ra hàng mới, nên chia cho giai thừa của số viên mỗi màu.
    3. 4!/(1! . 3!) = 4.
  - **Câu hỏi:** Xếp 5 viên linh thạch thành một hàng: 3 viên đỏ, 2 viên xanh; các viên cùng màu giống hệt nhau. Có bao nhiêu hàng khác nhau?
  - **Đáp án:** 10
    1. Nếu mọi viên đều khác nhau thì có 5! cách xếp.
    2. Đổi chỗ các viên cùng màu cho nhau không tạo ra hàng mới, nên chia cho giai thừa của số viên mỗi màu.
    3. 5!/(3! . 2!) = 10.
  - **Câu hỏi:** Xếp 5 viên linh thạch thành một hàng: 2 viên đỏ, 3 viên xanh; các viên cùng màu giống hệt nhau. Có bao nhiêu hàng khác nhau?
  - **Đáp án:** 10
    1. Nếu mọi viên đều khác nhau thì có 5! cách xếp.
    2. Đổi chỗ các viên cùng màu cho nhau không tạo ra hàng mới, nên chia cho giai thừa của số viên mỗi màu.
    3. 5!/(2! . 3!) = 10.

### Tổ hợp (`tr_t2_to_hop`)

- `tr_t2_th_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ 7 đệ tử chọn ra 3 người đi hái thuốc, không phân biệt vai trò. Có bao nhiêu cách chọn?
  - **Đáp án:** 35
    1. Nhóm 3 người không có thứ tự, nên mỗi cách chọn là một tổ hợp chập 3 của 7.
    2. C_7^3 = A_7^3/3! = (7 . 6 . 5)/6.
    3. C_7^3 = 210/6 = 35.
- `tr_t2_th_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi 0 <= k <= n ta có C_n^k = C_n^(n - k).
  - **Đáp án:** Đúng
    1. Chọn k phần tử để lấy cũng là chọn n - k phần tử để bỏ lại.
    2. Hai cách chọn đó tương ứng một một với nhau, nên số cách bằng nhau.
    3. Ví dụ C_7^2 = C_7^5 = 21.
- `tr_t2_th_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tập hợp có 6 phần tử có bao nhiêu tập con gồm đúng 2 phần tử?
    - **(đúng)** 15
    - 30
    - 12
    - 36
  - **Đáp án:** 15
    1. Tập con không có thứ tự: đó là C_6^2.
    2. C_6^2 = (6 . 5)/2 = 15.
    3. 30 = A_6^2 là số cặp có thứ tự, đếm mỗi tập con hai lần.
- `tr_t2_th_08` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi số tổ hợp với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - C_5^2 — 10
    - C_6^3 — 20
    - C_7^1 — 7
    - C_4^4 — 1
  - **Lời giải:**
    1. C_n^k = A_n^k/k!.
    2. C_5^2 = 20/2 = 10; C_6^3 = 120/6 = 20.
    3. C_7^1 = 7 (chọn 1 trong 7); C_4^4 = 1 (lấy cả 4).
- `tr_g2_to_hop` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Từ 7 đệ tử, chọn 4 người cùng đi hái thuốc (không phân biệt vai trò). Có bao nhiêu cách?
  - **Đáp án:** 35
    1. Nhóm được chọn không có thứ tự, nên mỗi cách chọn là một tổ hợp.
    2. C_7^4 = A_7^4/4! = 840/24 = 35.
  - **Câu hỏi:** Từ 5 đệ tử, chọn 2 người cùng đi hái thuốc (không phân biệt vai trò). Có bao nhiêu cách?
  - **Đáp án:** 10
    1. Nhóm được chọn không có thứ tự, nên mỗi cách chọn là một tổ hợp.
    2. C_5^2 = A_5^2/2! = 20/2 = 10.
  - **Câu hỏi:** Từ 8 đệ tử, chọn 4 người cùng đi hái thuốc (không phân biệt vai trò). Có bao nhiêu cách?
  - **Đáp án:** 70
    1. Nhóm được chọn không có thứ tự, nên mỗi cách chọn là một tổ hợp.
    2. C_8^4 = A_8^4/4! = 1680/24 = 70.
- `tr_t2_th_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tổ có 6 nam và 4 nữ. Chọn 3 người sao cho có ít nhất 1 nữ. Có bao nhiêu cách?
  - **Đáp án:** 100
    1. Đếm phần bù cho gọn: lấy mọi cách chọn 3 người trừ đi các cách chọn toàn nam.
    2. Mọi cách chọn: C_10^3 = 120. Toàn nam: C_6^3 = 20.
    3. Số cách có ít nhất 1 nữ: 120 - 20 = 100.
- `tr_t2_th_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: một đa giác lồi 8 cạnh có bao nhiêu đường chéo?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi đoạn nối hai đỉnh ứng với một cách chọn 2 trong 8 đỉnh, không kể thứ tự.
    2. Số đoạn nối hai đỉnh là C_8^2 = 8 . 7 = 56.   **<- bước sai đầu tiên**
    3. Trong các đoạn đó có 8 đoạn là cạnh của đa giác.
    4. Số đường chéo là 56 - 8 = 48.
  - **Đáp án:** Bước 2: Số đoạn nối hai đỉnh là C_8^2 = 8 . 7 = 56.
  - **Vì sao sai, và bước đúng:**
    1. C_8^2 = (8 . 7)/2 = 28: phải chia cho 2! vì đoạn AB và đoạn BA là một.
    2. Số đường chéo là 28 - 8 = 20.
    3. Kiểm tra bằng công thức n(n - 3)/2 = 8 . 5/2 = 20.
- `tr_t2_th_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm hệ số của x^2 trong khai triển (1 + x)^5.
  - **Đáp án (thứ tự đúng):**
    1. Theo nhị thức Newton, (1 + x)^5 là tổng các số hạng C_5^k . x^k với k từ 0 đến 5.
    2. Số hạng chứa x^2 ứng với k = 2.
    3. Hệ số của nó là C_5^2.
    4. C_5^2 = (5 . 4)/2 = 10.
  - **Lời giải:**
    1. Khi nhân 5 thừa số (1 + x), mỗi số hạng x^2 sinh ra từ cách chọn x ở đúng 2 thừa số.
    2. Có C_5^2 cách chọn 2 thừa số đó.
    3. Vậy hệ số của x^2 là C_5^2 = 10.
- `tr_t2_th_07` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số nguyên n >= 0, ta có C_n^0 + C_n^1 + ... + C_n^n = 2^n.
  - **Đáp án:** Đúng
    1. Vế trái đếm mọi tập con của một tập n phần tử, chia theo số phần tử k = 0, 1, ..., n.
    2. Mỗi phần tử được chọn hoặc không, nên số tập con là 2^n.
    3. Cũng có thể thay x = 1 vào khai triển nhị thức của (1 + x)^n.
- `tr_g2_hai_nhom` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một tông môn có 4 kiếm tu và 7 pháp tu. Chọn một đội gồm đúng 1 kiếm tu và 2 pháp tu. Có bao nhiêu cách?
  - **Đáp án:** 84
    1. Chọn đội theo hai bước nối tiếp: chọn kiếm tu, rồi chọn pháp tu.
    2. Chọn 1 trong 4 kiếm tu: C_4^1 = 4. Chọn 2 trong 7 pháp tu: C_7^2 = 21.
    3. Theo quy tắc nhân: 4 . 21 = 84.
  - **Câu hỏi:** Một tông môn có 3 kiếm tu và 3 pháp tu. Chọn một đội gồm đúng 1 kiếm tu và 2 pháp tu. Có bao nhiêu cách?
  - **Đáp án:** 9
    1. Chọn đội theo hai bước nối tiếp: chọn kiếm tu, rồi chọn pháp tu.
    2. Chọn 1 trong 3 kiếm tu: C_3^1 = 3. Chọn 2 trong 3 pháp tu: C_3^2 = 3.
    3. Theo quy tắc nhân: 3 . 3 = 9.
  - **Câu hỏi:** Một tông môn có 4 kiếm tu và 7 pháp tu. Chọn một đội gồm đúng 3 kiếm tu và 1 pháp tu. Có bao nhiêu cách?
  - **Đáp án:** 28
    1. Chọn đội theo hai bước nối tiếp: chọn kiếm tu, rồi chọn pháp tu.
    2. Chọn 3 trong 4 kiếm tu: C_4^3 = 4. Chọn 1 trong 7 pháp tu: C_7^1 = 7.
    3. Theo quy tắc nhân: 4 . 7 = 28.

### Tổ hợp lặp và nghiệm nguyên (`tr_t2_to_hop_lap`)

- `tr_t2_tl_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x_1 + x_2 + x_3 = 5 có bao nhiêu nghiệm nguyên không âm?
  - **Đáp án:** 21
    1. Mỗi nghiệm ứng với một hàng gồm 5 viên đá và 2 vách ngăn: số đá ở ba ngăn là x_1, x_2, x_3.
    2. Hàng có 7 vị trí, chọn 2 vị trí cho vách.
    3. C_7^2 = 21.
- `tr_t2_tl_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số cách chọn k vật từ n loại, mỗi loại có rất nhiều vật giống nhau và một loại được chọn nhiều lần, là C_(n + k - 1)^k.
  - **Đáp án:** Đúng
    1. Gọi x_i là số vật lấy ở loại thứ i: cần đếm nghiệm nguyên không âm của x_1 + ... + x_n = k.
    2. Xếp k viên đá và n - 1 vách ngăn thành hàng: n + k - 1 vị trí, chọn k vị trí cho đá.
    3. Số cách là C_(n + k - 1)^k.
- `tr_t2_tl_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tiệm bán 4 loại đan dược, loại nào cũng còn rất nhiều viên. Mua 2 viên, có thể cùng loại. Có bao nhiêu cách mua (chỉ quan tâm mua mấy viên mỗi loại)?
    - **(đúng)** 10
    - 16
    - 6
    - 12
  - **Đáp án:** 10
    1. Đây là tổ hợp lặp chập 2 của 4 loại: C_(4 + 2 - 1)^2 = C_5^2 = 10.
    2. Kiểm tra: 2 viên cùng loại có 4 cách, 2 viên khác loại có C_4^2 = 6 cách, cộng lại 10.
    3. 16 = 4^2 đếm có thứ tự, nên đếm hai lần mỗi cặp khác loại.
- `tr_g2_nghiem_nguyen` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x_1 + x_2 = 4 có bao nhiêu nghiệm nguyên không âm?
  - **Đáp án:** 5
    1. Mỗi nghiệm ứng với một cách xếp 4 viên đá và 1 vách ngăn thành một hàng: số đá giữa các vách là các x_i.
    2. Hàng có 5 vị trí, chọn 1 vị trí cho vách.
    3. C_5^1 = 5.
  - **Câu hỏi:** Phương trình x_1 + x_2 = 4 có bao nhiêu nghiệm nguyên không âm?
  - **Đáp án:** 5
    1. Mỗi nghiệm ứng với một cách xếp 4 viên đá và 1 vách ngăn thành một hàng: số đá giữa các vách là các x_i.
    2. Hàng có 5 vị trí, chọn 1 vị trí cho vách.
    3. C_5^1 = 5.
  - **Câu hỏi:** Phương trình x_1 + x_2 = 5 có bao nhiêu nghiệm nguyên không âm?
  - **Đáp án:** 6
    1. Mỗi nghiệm ứng với một cách xếp 5 viên đá và 1 vách ngăn thành một hàng: số đá giữa các vách là các x_i.
    2. Hàng có 6 vị trí, chọn 1 vị trí cho vách.
    3. C_6^1 = 6.
- `tr_t2_tl_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x_1 + x_2 + x_3 + x_4 = 10 có bao nhiêu nghiệm nguyên thỏa mãn x_i >= 2 với mọi i?
  - **Đáp án:** 10
    1. Đặt y_i = x_i - 2 thì y_i >= 0.
    2. Phương trình trở thành y_1 + y_2 + y_3 + y_4 = 10 - 8 = 2.
    3. Số nghiệm nguyên không âm: C_(2 + 3)^3 = C_5^3 = 10.
- `tr_t2_tl_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đếm số nghiệm nguyên dương của x_1 + x_2 + x_3 = 8.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt y_i = x_i - 1 thì y_i >= 0.
    2. Phương trình trở thành y_1 + y_2 + y_3 = 5.
    3. Số nghiệm nguyên không âm của nó là C_(5 + 3)^2 = C_8^2.   **<- bước sai đầu tiên**
    4. C_8^2 = 28, vậy có 28 nghiệm.
  - **Đáp án:** Bước 3: Số nghiệm nguyên không âm của nó là C_(5 + 3)^2 = C_8^2.
  - **Vì sao sai, và bước đúng:**
    1. Với tổng 5 và 3 ẩn, hàng gồm 5 viên đá và 2 vách có 5 + 2 = 7 vị trí, không phải 8.
    2. Số nghiệm là C_7^2 = 21.
    3. Công thức: tổng n, k ẩn cho C_(n + k - 1)^(k - 1).
- `tr_t2_tl_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chia 6 viên linh thạch giống nhau cho 3 đệ tử, có người có thể không được viên nào. Sắp xếp các bước đếm số cách chia.
  - **Đáp án (thứ tự đúng):**
    1. Gọi x_1, x_2, x_3 là số viên của từng đệ tử: x_1 + x_2 + x_3 = 6 với x_i >= 0.
    2. Mỗi nghiệm ứng với một hàng gồm 6 viên đá và 2 vách ngăn.
    3. Hàng có 8 vị trí, chọn 2 vị trí cho vách: C_8^2 cách.
    4. C_8^2 = 28.
  - **Lời giải:**
    1. Đưa bài toán chia quà về đếm nghiệm nguyên không âm.
    2. Hai vách chia hàng đá thành ba phần cho ba người; phần rỗng nghĩa là người đó không được viên nào.
    3. Có C_8^2 = 28 cách đặt vách.
- `tr_t2_tl_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phương trình với số nghiệm của nó.
  - **Đáp án (ghép đúng):**
    - x_1 + x_2 = 4, nghiệm nguyên không âm — 5
    - x_1 + x_2 + x_3 = 3, nghiệm nguyên không âm — 10
    - x_1 + x_2 + x_3 = 4, nghiệm nguyên dương — 3
    - x_1 + x_2 + x_3 + x_4 = 3, nghiệm nguyên không âm — 20
  - **Lời giải:**
    1. Nghiệm không âm của tổng n với k ẩn: C_(n + k - 1)^(k - 1).
    2. C_5^1 = 5; C_5^2 = 10; C_6^3 = 20.
    3. Nghiệm dương: trừ 1 ở mỗi ẩn, x_1 + x_2 + x_3 = 4 thành tổng 1 với 3 ẩn không âm, C_3^2 = 3.
- `tr_g2_nghiem_can_duoi` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x_1 + x_2 = 5 có bao nhiêu nghiệm nguyên thỏa mãn x_i >= 1 với mọi i?
  - **Đáp án:** 4
    1. Đặt y_i = x_i - 1 thì y_i >= 0.
    2. Phương trình trở thành y_1 + y_2 = 5 - 2 . 1 = 3.
    3. Số nghiệm nguyên không âm là C_4^1 = 4.
  - **Câu hỏi:** Phương trình x_1 + x_2 = 3 có bao nhiêu nghiệm nguyên thỏa mãn x_i >= 1 với mọi i?
  - **Đáp án:** 2
    1. Đặt y_i = x_i - 1 thì y_i >= 0.
    2. Phương trình trở thành y_1 + y_2 = 3 - 2 . 1 = 1.
    3. Số nghiệm nguyên không âm là C_2^1 = 2.
  - **Câu hỏi:** Phương trình x_1 + x_2 = 5 có bao nhiêu nghiệm nguyên thỏa mãn x_i >= 1 với mọi i?
  - **Đáp án:** 4
    1. Đặt y_i = x_i - 1 thì y_i >= 0.
    2. Phương trình trở thành y_1 + y_2 = 5 - 2 . 1 = 3.
    3. Số nghiệm nguyên không âm là C_4^1 = 4.

### Nguyên lý bù trừ (`tr_t2_bu_tru`)

- `tr_t2_bt_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong 40 đệ tử, 25 người luyện kiếm, 18 người luyện đan và 10 người luyện cả hai. Có bao nhiêu người luyện ít nhất một môn?
  - **Đáp án:** 33
    1. Gọi K, D là tập người luyện kiếm, luyện đan: cần |K hợp D|.
    2. Cộng 25 + 18 thì 10 người luyện cả hai bị đếm hai lần.
    3. |K hợp D| = 25 + 18 - 10 = 33.
- `tr_t2_bt_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi tập hữu hạn A và B ta có |A hợp B| = |A| + |B|.
  - **Đáp án:** Sai
    1. Lấy A = {1, 2} và B = {2, 3}: |A hợp B| = 3, còn |A| + |B| = 4.
    2. Phần tử 2 thuộc cả hai tập nên bị đếm hai lần.
    3. Công thức đúng là |A hợp B| = |A| + |B| - |A giao B|; chỉ khi A, B rời nhau mới cộng thẳng được.
- `tr_t2_bt_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 30 chia hết cho 2 hoặc chia hết cho 3?
    - **(đúng)** 20
    - 25
    - 15
    - 5
  - **Đáp án:** 20
    1. Chia hết cho 2: 15 số. Chia hết cho 3: 10 số.
    2. Chia hết cho cả 2 và 3, tức là cho 6: 5 số.
    3. Theo nguyên lý bù trừ: 15 + 10 - 5 = 20.
- `tr_g2_bu_tru_hai_so` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 46 chia hết cho 4 hoặc chia hết cho 6?
  - **Đáp án:** 15
    1. Gọi A là tập các số chia hết cho 4, B là tập các số chia hết cho 6: cần |A hợp B|.
    2. |A| = phần nguyên của 46/4 = 11; |B| = phần nguyên của 46/6 = 7.
    3. Số chia hết cho cả hai là số chia hết cho BCNN(4, 6) = 12: |A giao B| = 3.
    4. |A hợp B| = 11 + 7 - 3 = 15.
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 51 chia hết cho 2 hoặc chia hết cho 9?
  - **Đáp án:** 28
    1. Gọi A là tập các số chia hết cho 2, B là tập các số chia hết cho 9: cần |A hợp B|.
    2. |A| = phần nguyên của 51/2 = 25; |B| = phần nguyên của 51/9 = 5.
    3. Số chia hết cho cả hai là số chia hết cho BCNN(2, 9) = 18: |A giao B| = 2.
    4. |A hợp B| = 25 + 5 - 2 = 28.
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 169 chia hết cho 5 hoặc chia hết cho 6?
  - **Đáp án:** 56
    1. Gọi A là tập các số chia hết cho 5, B là tập các số chia hết cho 6: cần |A hợp B|.
    2. |A| = phần nguyên của 169/5 = 33; |B| = phần nguyên của 169/6 = 28.
    3. Số chia hết cho cả hai là số chia hết cho BCNN(5, 6) = 30: |A giao B| = 5.
    4. |A hợp B| = 33 + 28 - 5 = 56.
- `tr_t2_bt_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 100 không chia hết cho 2, không chia hết cho 3 và không chia hết cho 5?
  - **Đáp án:** 26
    1. Đếm các số chia hết cho ít nhất một trong 2, 3, 5 rồi lấy 100 trừ đi.
    2. Chia hết cho 2, 3, 5: 50, 33, 20. Cho 6, 10, 15: 16, 10, 6. Cho 30: 3.
    3. Theo nguyên lý bù trừ: 50 + 33 + 20 - 16 - 10 - 6 + 3 = 74.
    4. Đáp số: 100 - 74 = 26.
- `tr_t2_bt_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: 15 đệ tử học trận pháp, 12 học luyện đan, 10 học luyện khí; 5 người học trận pháp và luyện đan, 4 học trận pháp và luyện khí, 3 học luyện đan và luyện khí, 2 học cả ba. Có bao nhiêu người học ít nhất một môn?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi T, D, K là tập người học trận pháp, luyện đan, luyện khí; cần |T hợp D hợp K|.
    2. Cộng ba tập: 15 + 12 + 10 = 37.
    3. Trừ các phần chung từng đôi: 37 - (5 + 4 + 3) = 25.
    4. Trừ tiếp phần chung của cả ba: 25 - 2 = 23.   **<- bước sai đầu tiên**
    5. Vậy có 23 người học ít nhất một môn.
  - **Đáp án:** Bước 4: Trừ tiếp phần chung của cả ba: 25 - 2 = 23.
  - **Vì sao sai, và bước đúng:**
    1. Người học cả ba môn được cộng 3 lần ở bước 2 và bị trừ 3 lần ở bước 3, nên lúc này chưa được đếm lần nào.
    2. Vì vậy phải cộng lại phần chung của cả ba: 25 + 2 = 27.
    3. Công thức: |T hợp D hợp K| = tổng ba tập - tổng ba phần chung từng đôi + phần chung cả ba.
- `tr_t2_bt_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước đếm số xâu nhị phân độ dài 8 bắt đầu bằng 1 hoặc kết thúc bằng 00.
  - **Đáp án (thứ tự đúng):**
    1. Gọi A là tập xâu bắt đầu bằng 1, B là tập xâu kết thúc bằng 00; cần |A hợp B|.
    2. Tính |A| = 2^7 = 128 và |B| = 2^6 = 64.
    3. Xâu thuộc cả A và B có 5 vị trí ở giữa tự do: |A giao B| = 2^5 = 32.
    4. |A hợp B| = 128 + 64 - 32 = 160.
  - **Lời giải:**
    1. Điều kiện có chữ "hoặc" nên cần hợp của hai tập, dùng nguyên lý bù trừ.
    2. A cố định 1 vị trí, B cố định 2 vị trí, A giao B cố định 3 vị trí.
    3. Kết quả 128 + 64 - 32 = 160.
- `tr_t2_bt_07` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi tập hữu hạn A, B, C: |A hợp B hợp C| = |A| + |B| + |C| - |A giao B| - |A giao C| - |B giao C| + |A giao B giao C|.
  - **Đáp án:** Đúng
    1. Xét một phần tử thuộc đúng m tập (m = 1, 2 hoặc 3) và đếm số lần vế phải tính nó.
    2. m = 1: tính 1 lần. m = 2: cộng 2 lần, trừ 1 lần, còn 1. m = 3: cộng 3, trừ 3, cộng 1, còn 1.
    3. Phần tử nào của hợp cũng được tính đúng một lần, nên công thức đúng.
- `tr_g2_bu_tru_ba_so` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 115 không chia hết cho số nào trong các số 2, 3, 5?
  - **Đáp án:** 31
    1. Đếm phần bù: lấy 115 trừ đi số các số chia hết cho ít nhất một trong 2, 3, 5.
    2. Chia hết cho từng số: 57, 38, 23.
    3. Chia hết cho cả hai số của từng cặp, tức là chia hết cho 6, 10, 15: 19, 11, 7; chia hết cho cả ba (30): 3.
    4. Theo nguyên lý bù trừ: 118 - 37 + 3 = 84 số chia hết cho ít nhất một số.
    5. Đáp số: 115 - 84 = 31.
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 142 không chia hết cho số nào trong các số 2, 5, 7?
  - **Đáp án:** 49
    1. Đếm phần bù: lấy 142 trừ đi số các số chia hết cho ít nhất một trong 2, 5, 7.
    2. Chia hết cho từng số: 71, 28, 20.
    3. Chia hết cho cả hai số của từng cặp, tức là chia hết cho 10, 14, 35: 14, 10, 4; chia hết cho cả ba (70): 2.
    4. Theo nguyên lý bù trừ: 119 - 28 + 2 = 93 số chia hết cho ít nhất một số.
    5. Đáp số: 142 - 93 = 49.
  - **Câu hỏi:** Có bao nhiêu số nguyên từ 1 đến 144 không chia hết cho số nào trong các số 2, 3, 5?
  - **Đáp án:** 39
    1. Đếm phần bù: lấy 144 trừ đi số các số chia hết cho ít nhất một trong 2, 3, 5.
    2. Chia hết cho từng số: 72, 48, 28.
    3. Chia hết cho cả hai số của từng cặp, tức là chia hết cho 6, 10, 15: 24, 14, 9; chia hết cho cả ba (30): 4.
    4. Theo nguyên lý bù trừ: 148 - 47 + 4 = 105 số chia hết cho ít nhất một số.
    5. Đáp số: 144 - 105 = 39.

### Hệ thức truy hồi (`tr_t2_truy_hoi`)

- `tr_t2_tr_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n thỏa mãn a_0 = 1 và a_n = 3a_(n - 1) với n >= 1. Tính a_4.
  - **Đáp án:** 81
    1. Tính lần lượt: a_1 = 3, a_2 = 9, a_3 = 27, a_4 = 81.
    2. Nhìn ra quy luật a_n = 3^n, nên a_4 = 3^4 = 81.
- `tr_t2_tr_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy Fibonacci F_1 = F_2 = 1, F_n = F_(n - 1) + F_(n - 2) với n >= 3 có F_7 = 13.
  - **Đáp án:** Đúng
    1. Tính lần lượt: F_3 = 2, F_4 = 3, F_5 = 5, F_6 = 8, F_7 = 13.
    2. Vậy F_7 = 13.
- `tr_t2_tr_03` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gọi h_n là số lần chuyển đĩa ít nhất để giải bài tháp Hà Nội với n đĩa. Hệ thức truy hồi nào đúng?
    - **(đúng)** h_n = 2h_(n - 1) + 1
    - h_n = h_(n - 1) + 2
    - h_n = 2h_(n - 1)
    - h_n = h_(n - 1) + h_(n - 2)
  - **Đáp án:** h_n = 2h_(n - 1) + 1
    1. Muốn chuyển đĩa lớn nhất, phải dời n - 1 đĩa trên nó sang cọc trung gian: h_(n - 1) lần.
    2. Chuyển đĩa lớn nhất: 1 lần. Rồi đưa n - 1 đĩa về trên nó: thêm h_(n - 1) lần.
    3. Vậy h_n = 2h_(n - 1) + 1, với h_1 = 1.
- `tr_t2_tr_07` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dãy với giá trị a_3 của nó.
  - **Đáp án (ghép đúng):**
    - a_0 = 1, a_n = 2a_(n - 1) — 8
    - a_0 = 2, a_n = a_(n - 1) + 3 — 11
    - a_0 = 1, a_n = 3a_(n - 1) - 1 — 14
    - a_0 = 0, a_n = a_(n - 1) + n — 6
  - **Lời giải:**
    1. Tính lần lượt a_1, a_2, a_3 cho từng dãy.
    2. 1, 2, 4, 8 và 2, 5, 8, 11.
    3. 1, 2, 5, 14 và 0, 1, 3, 6.
- `tr_g2_truy_hoi` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n thỏa mãn a_0 = 2, a_1 = 1 và a_n = 2a_(n - 1) + a_(n - 2) với n >= 2. Tính a_5.
  - **Đáp án:** 53
    1. Tính lần lượt từng số hạng, mỗi số hạng dùng hai số hạng đứng ngay trước nó.
    2. a_2 = 4; a_3 = 9; a_4 = 22; a_5 = 53.
    3. Vậy a_5 = 53.
  - **Câu hỏi:** Dãy a_n thỏa mãn a_0 = 0, a_1 = 3 và a_n = a_(n - 1) + a_(n - 2) với n >= 2. Tính a_4.
  - **Đáp án:** 9
    1. Tính lần lượt từng số hạng, mỗi số hạng dùng hai số hạng đứng ngay trước nó.
    2. a_2 = 3; a_3 = 6; a_4 = 9.
    3. Vậy a_4 = 9.
  - **Câu hỏi:** Dãy a_n thỏa mãn a_0 = 2, a_1 = 4 và a_n = 2a_(n - 1) + 2a_(n - 2) với n >= 2. Tính a_6.
  - **Đáp án:** 656
    1. Tính lần lượt từng số hạng, mỗi số hạng dùng hai số hạng đứng ngay trước nó.
    2. a_2 = 12; a_3 = 32; a_4 = 88; a_5 = 240; a_6 = 656.
    3. Vậy a_6 = 656.
- `tr_t2_tr_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ thức a_n = 5a_(n - 1) - 6a_(n - 2) có phương trình đặc trưng r^2 = 5r - 6. Tìm các nghiệm của phương trình đặc trưng đó.
  - **Đáp án:** 2, 3  (thứ tự nào cũng được)
    1. Viết lại: r^2 - 5r + 6 = 0.
    2. Phân tích: (r - 2)(r - 3) = 0.
    3. Hai nghiệm là 2 và 3, nên nghiệm tổng quát của hệ thức là a_n = A . 2^n + B . 3^n.
- `tr_t2_tr_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: giải hệ thức a_n = a_(n - 1) + 2a_(n - 2) với a_0 = 2, a_1 = 1.
  - **Lời giải đưa ra (có một bước sai):**
    1. Phương trình đặc trưng: r^2 - r - 2 = 0.
    2. Nghiệm r = 2 và r = -1, nên a_n = A . 2^n + B . (-1)^n.
    3. Từ a_0 = 2: A + B = 2. Từ a_1 = 1: 2A + B = 1.   **<- bước sai đầu tiên**
    4. Giải ra A = -1, B = 3.
    5. Vậy a_n = -2^n + 3 . (-1)^n.
  - **Đáp án:** Bước 3: Từ a_0 = 2: A + B = 2. Từ a_1 = 1: 2A + B = 1.
  - **Vì sao sai, và bước đúng:**
    1. Thay n = 1: a_1 = 2A + B . (-1)^1 = 2A - B, không phải 2A + B.
    2. Hệ đúng là A + B = 2 và 2A - B = 1, cho A = 1, B = 1.
    3. Vậy a_n = 2^n + (-1)^n. Kiểm tra: a_2 = a_1 + 2a_0 = 5 và 2^2 + 1 = 5.
- `tr_t2_tr_06` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Gọi s_n là số xâu nhị phân độ dài n không có hai chữ số 1 đứng liền nhau. Sắp xếp các bước lập hệ thức truy hồi cho s_n (với n >= 3).
  - **Đáp án (thứ tự đúng):**
    1. Chia các xâu cần đếm theo chữ số cuối cùng của chúng.
    2. Thứ nhất, xâu kết thúc bằng 0: bỏ chữ số cuối được một xâu tốt độ dài n - 1, nên có s_(n - 1) xâu.
    3. Thứ hai, xâu kết thúc bằng 1: chữ số đứng trước phải là 0, bỏ hai chữ số cuối được một xâu tốt độ dài n - 2, nên có s_(n - 2) xâu.
    4. Cộng hai trường hợp: s_n = s_(n - 1) + s_(n - 2).
  - **Lời giải:**
    1. Lập hệ thức truy hồi là chia bài toán cỡ n thành những bài toán cùng loại nhưng nhỏ hơn.
    2. Chữ số cuối là 0 thì phần trước tùy ý (miễn là tốt); là 1 thì bắt buộc có 0 đứng trước.
    3. Được s_n = s_(n - 1) + s_(n - 2), với s_1 = 2 và s_2 = 3.
- `tr_g2_xau_cam` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 5 không chứa 2 chữ số 1 đứng liền nhau (không chứa 11)?
  - **Đáp án:** 13
    1. Gọi s_n là số xâu cần đếm có độ dài n. Xâu tốt kết thúc bằng 0 hoặc bằng 01, bỏ phần đuôi đó đi vẫn là xâu tốt.
    2. Vậy s_n = s_(n - 1) + s_(n - 2), với s_0 = 1, s_1 = 2.
    3. Tính dần: 1, 2, 3, 5, 8, 13.
    4. s_5 = 13.
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 5 không chứa 2 chữ số 1 đứng liền nhau (không chứa 11)?
  - **Đáp án:** 13
    1. Gọi s_n là số xâu cần đếm có độ dài n. Xâu tốt kết thúc bằng 0 hoặc bằng 01, bỏ phần đuôi đó đi vẫn là xâu tốt.
    2. Vậy s_n = s_(n - 1) + s_(n - 2), với s_0 = 1, s_1 = 2.
    3. Tính dần: 1, 2, 3, 5, 8, 13.
    4. s_5 = 13.
  - **Câu hỏi:** Có bao nhiêu xâu nhị phân độ dài 12 không chứa 2 chữ số 1 đứng liền nhau (không chứa 11)?
  - **Đáp án:** 377
    1. Gọi s_n là số xâu cần đếm có độ dài n. Xâu tốt kết thúc bằng 0 hoặc bằng 01, bỏ phần đuôi đó đi vẫn là xâu tốt.
    2. Vậy s_n = s_(n - 1) + s_(n - 2), với s_0 = 1, s_1 = 2.
    3. Tính dần: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377.
    4. s_12 = 377.

## Tầng 3: Bài toán tồn tại và bài toán liệt kê

49 dạng câu (35 câu viết tay, 14 bộ sinh câu); 49 chưa duyệt.

### Nguyên lý Dirichlet (`tr_t3_dirichlet`)

- `tr_t3_dr_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong 13 người bất kỳ luôn có ít nhất 2 người sinh cùng một tháng.
  - **Đáp án:** Đúng
    1. Coi 12 tháng là 12 hộp và xếp mỗi người vào hộp tháng sinh của mình.
    2. 13 người mà chỉ có 12 hộp, nên theo nguyên lý Dirichlet có một hộp chứa ít nhất 2 người.
    3. Với 12 người thì chưa chắc: mỗi người có thể sinh một tháng khác nhau.
- `tr_t3_dr_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một túi có linh thạch 4 màu, màu nào cũng rất nhiều viên. Bịt mắt lấy ra từng viên. Phải lấy ít nhất bao nhiêu viên để chắc chắn có 3 viên cùng màu?
    - **(đúng)** 9
    - 12
    - 8
    - 13
  - **Đáp án:** 9
    1. Coi 4 màu là 4 hộp. 8 viên vẫn có thể chia đều mỗi màu 2 viên, chưa có 3 viên cùng màu.
    2. Lấy thêm 1 viên, tức là 9 viên, thì có một màu có ít nhất trần(9/4) = 3 viên.
    3. Vậy cần ít nhất 4 . 2 + 1 = 9 viên.
- `tr_t3_dr_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh: trong 6 số nguyên bất kỳ luôn có hai số có hiệu chia hết cho 5.
  - **Đáp án (thứ tự đúng):**
    1. Mỗi số nguyên chia cho 5 có số dư là một trong 5 giá trị 0, 1, 2, 3, 4.
    2. Coi 5 số dư là 5 hộp và đặt mỗi số vào hộp ứng với số dư của nó.
    3. Có 6 số mà chỉ có 5 hộp, nên có một hộp chứa ít nhất 2 số.
    4. Hai số cùng số dư khi chia cho 5 có hiệu chia hết cho 5.
  - **Lời giải:**
    1. Lập luận Dirichlet luôn gồm: chọn hộp, đặt vật vào hộp, so số vật với số hộp, rồi đọc ra kết luận.
    2. Ở đây hộp là số dư khi chia cho 5.
    3. Hai số a, b cùng số dư r thì a - b = 5(thương của a - thương của b), chia hết cho 5.
- `tr_g3_dirichlet_min` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một túi đựng linh thạch 7 màu, màu nào cũng rất nhiều viên. Bịt mắt lấy ra từng viên. Phải lấy ít nhất bao nhiêu viên để chắc chắn có 2 viên cùng màu?
  - **Đáp án:** 8
    1. Coi mỗi màu là một hộp: có 7 hộp.
    2. Với 7 . 1 = 7 vật vẫn có thể xếp mỗi hộp đúng 1 vật, chưa có hộp nào đủ 2.
    3. Thêm một vật nữa, tức là 8 vật, thì theo nguyên lý Dirichlet có một hộp chứa ít nhất trần(8/7) = 2 vật.
    4. Vậy cần ít nhất 8.
  - **Câu hỏi:** Một túi đựng linh thạch 3 màu, màu nào cũng rất nhiều viên. Bịt mắt lấy ra từng viên. Phải lấy ít nhất bao nhiêu viên để chắc chắn có 2 viên cùng màu?
  - **Đáp án:** 4
    1. Coi mỗi màu là một hộp: có 3 hộp.
    2. Với 3 . 1 = 3 vật vẫn có thể xếp mỗi hộp đúng 1 vật, chưa có hộp nào đủ 2.
    3. Thêm một vật nữa, tức là 4 vật, thì theo nguyên lý Dirichlet có một hộp chứa ít nhất trần(4/3) = 2 vật.
    4. Vậy cần ít nhất 4.
  - **Câu hỏi:** Một túi đựng linh thạch 7 màu, màu nào cũng rất nhiều viên. Bịt mắt lấy ra từng viên. Phải lấy ít nhất bao nhiêu viên để chắc chắn có 3 viên cùng màu?
  - **Đáp án:** 15
    1. Coi mỗi màu là một hộp: có 7 hộp.
    2. Với 7 . 2 = 14 vật vẫn có thể xếp mỗi hộp đúng 2 vật, chưa có hộp nào đủ 3.
    3. Thêm một vật nữa, tức là 15 vật, thì theo nguyên lý Dirichlet có một hộp chứa ít nhất trần(15/7) = 3 vật.
    4. Vậy cần ít nhất 15.
- `tr_g3_dirichlet_tran` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cất 24 viên đan dược vào 4 bình. Dù cất thế nào, chắc chắn có một bình chứa ít nhất bao nhiêu viên? (Tìm số lớn nhất có thể khẳng định.)
  - **Đáp án:** 6
    1. Theo nguyên lý Dirichlet, có một bình chứa ít nhất trần(24/4) viên.
    2. 24 = 4 . 6 + 0, nên trần(24/4) = 6.
    3. Không khẳng định được nhiều hơn: chia đều càng tốt (mỗi bình 6 hoặc 7 viên) thì bình nhiều nhất chỉ có 6 viên.
  - **Câu hỏi:** Cất 14 viên đan dược vào 9 bình. Dù cất thế nào, chắc chắn có một bình chứa ít nhất bao nhiêu viên? (Tìm số lớn nhất có thể khẳng định.)
  - **Đáp án:** 2
    1. Theo nguyên lý Dirichlet, có một bình chứa ít nhất trần(14/9) viên.
    2. 14 = 9 . 1 + 5, nên trần(14/9) = 2.
    3. Không khẳng định được nhiều hơn: chia đều càng tốt (mỗi bình 1 hoặc 2 viên) thì bình nhiều nhất chỉ có 2 viên.
  - **Câu hỏi:** Cất 24 viên đan dược vào 4 bình. Dù cất thế nào, chắc chắn có một bình chứa ít nhất bao nhiêu viên? (Tìm số lớn nhất có thể khẳng định.)
  - **Đáp án:** 6
    1. Theo nguyên lý Dirichlet, có một bình chứa ít nhất trần(24/4) viên.
    2. 24 = 4 . 6 + 0, nên trần(24/4) = 6.
    3. Không khẳng định được nhiều hơn: chia đều càng tốt (mỗi bình 6 hoặc 7 viên) thì bình nhiều nhất chỉ có 6 viên.
- `tr_t3_dr_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chọn các số khác nhau từ tập {1, 2, ..., 20}. Phải chọn ít nhất bao nhiêu số để chắc chắn có hai số mà số này chia hết cho số kia?
  - **Đáp án:** 11
    1. Mọi số viết được duy nhất dưới dạng 2^a . m với m lẻ. Từ 1 đến 20 có 10 số lẻ m: 1, 3, ..., 19, đó là 10 hộp.
    2. Chọn 11 số thì có hai số cùng hộp: 2^a . m và 2^b . m với a < b, và số nhỏ chia hết số lớn.
    3. Chọn 10 số 11, 12, ..., 20 thì không số nào chia hết số khác (thương ít nhất là 2 mà 2 . 11 > 20).
    4. Vậy cần ít nhất 11 số.
- `tr_t3_dr_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: cho 5 điểm nằm trong một hình vuông cạnh 2; chứng minh có hai điểm cách nhau không quá căn bậc hai của 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. Chia hình vuông cạnh 2 thành 4 hình vuông nhỏ cạnh 1.
    2. Có 5 điểm và 4 hình vuông nhỏ, nên theo nguyên lý Dirichlet có một hình vuông nhỏ chứa ít nhất 2 điểm.
    3. Hai điểm trong một hình vuông cạnh 1 cách nhau không quá độ dài cạnh, tức là không quá 1.   **<- bước sai đầu tiên**
    4. Vậy hai điểm đó cách nhau không quá 1, càng không quá căn bậc hai của 2.
  - **Đáp án:** Bước 3: Hai điểm trong một hình vuông cạnh 1 cách nhau không quá độ dài cạnh, tức là không quá 1.
  - **Vì sao sai, và bước đúng:**
    1. Hai điểm xa nhau nhất trong hình vuông cạnh 1 là hai đỉnh đối diện, cách nhau bằng đường chéo, tức là căn bậc hai của 2, lớn hơn 1.
    2. Bước đúng là: hai điểm đó cách nhau không quá căn bậc hai của 2, và đó chính là điều cần chứng minh.
    3. Thật ra không thể khẳng định không quá 1: 4 đỉnh và tâm của hình vuông lớn là 5 điểm, cặp gần nhất cách nhau đúng căn bậc hai của 2.
- `tr_t3_dr_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một giải đấu có 6 tông môn, mỗi cặp đấu với nhau nhiều nhất một trận. Ở bất kỳ thời điểm nào cũng có hai tông môn đã đấu cùng một số trận.
  - **Đáp án:** Đúng
    1. Mỗi tông môn đã đấu một số trận từ 0 đến 5: có 6 giá trị có thể.
    2. Hai giá trị 0 và 5 không thể cùng xuất hiện: tông môn đã đấu 5 trận đã gặp mọi đội, nên không đội nào có 0 trận.
    3. Vậy 6 tông môn chỉ nhận nhiều nhất 5 giá trị, theo nguyên lý Dirichlet có hai tông môn cùng số trận.
- `tr_g3_dirichlet_cap` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chọn các số khác nhau từ tập {1, 2, ..., 14}. Phải chọn ít nhất bao nhiêu số để chắc chắn trong đó có hai số có tổng bằng 15?
  - **Đáp án:** 8
    1. Chia 14 số thành 7 hộp, mỗi hộp là một cặp số có tổng bằng 15: {1, 14}; {2, 13}; {3, 12}; {4, 11}; {5, 10}; {6, 9}; {7, 8}.
    2. Chọn 8 số thì theo nguyên lý Dirichlet có hai số rơi vào cùng một hộp, tức là thành một cặp như vậy.
    3. Chọn 7 số thì chưa chắc: ví dụ 1, 2, ..., 7 không có cặp nào như vậy.
    4. Vậy cần ít nhất 8 số.
  - **Câu hỏi:** Chọn các số khác nhau từ tập {1, 2, ..., 6}. Phải chọn ít nhất bao nhiêu số để chắc chắn trong đó có hai số có tổng bằng 7?
  - **Đáp án:** 4
    1. Chia 6 số thành 3 hộp, mỗi hộp là một cặp số có tổng bằng 7: {1, 6}; {2, 5}; {3, 4}.
    2. Chọn 4 số thì theo nguyên lý Dirichlet có hai số rơi vào cùng một hộp, tức là thành một cặp như vậy.
    3. Chọn 3 số thì chưa chắc: ví dụ 1, 2, ..., 3 không có cặp nào như vậy.
    4. Vậy cần ít nhất 4 số.
  - **Câu hỏi:** Chọn các số khác nhau từ tập {1, 2, ..., 14}. Phải chọn ít nhất bao nhiêu số để chắc chắn trong đó có hai số có tổng bằng 15?
  - **Đáp án:** 8
    1. Chia 14 số thành 7 hộp, mỗi hộp là một cặp số có tổng bằng 15: {1, 14}; {2, 13}; {3, 12}; {4, 11}; {5, 10}; {6, 9}; {7, 8}.
    2. Chọn 8 số thì theo nguyên lý Dirichlet có hai số rơi vào cùng một hộp, tức là thành một cặp như vậy.
    3. Chọn 7 số thì chưa chắc: ví dụ 1, 2, ..., 7 không có cặp nào như vậy.
    4. Vậy cần ít nhất 8 số.

### Chẵn lẻ và bất biến (`tr_t3_bat_bien`)

- `tr_t3_bb_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một bàn cờ 8 x 8 bị cắt mất hai ô ở hai góc đối diện. Phần còn lại lát kín được bằng 31 quân domino, mỗi quân phủ đúng 2 ô kề nhau.
  - **Đáp án:** Sai
    1. Tô bàn cờ trắng đen xen kẽ. Hai ô ở hai góc đối diện cùng màu, giả sử là trắng.
    2. Phần còn lại có 30 ô trắng và 32 ô đen.
    3. Mỗi quân domino phủ một ô trắng và một ô đen, nên 31 quân phủ 31 ô mỗi màu: không khớp, không lát được.
- `tr_t3_bb_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên bảng có các số 1, 2, ..., 10. Mỗi lượt xóa hai số a, b và viết thêm số a + b. Sau 9 lượt trên bảng còn một số. Số đó là bao nhiêu?
    - **(đúng)** 55
    - 45
    - 50
    - Còn tùy cách chọn a, b ở mỗi lượt
  - **Đáp án:** 55
    1. Mỗi lượt bớt a và b nhưng thêm a + b, nên tổng các số trên bảng không đổi: đó là bất biến.
    2. Tổng lúc đầu là 1 + 2 + ... + 10 = 55.
    3. Số cuối cùng chính là tổng lúc cuối, luôn bằng 55 dù chọn thế nào.
- `tr_t3_bb_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh bàn cờ 8 x 8 bị cắt hai ô ở hai góc đối diện không lát được bằng domino.
  - **Đáp án (thứ tự đúng):**
    1. Tô bàn cờ trắng đen xen kẽ như thường lệ.
    2. Hai ô góc đối diện cùng màu, nên phần còn lại có 32 ô màu này và 30 ô màu kia.
    3. Mỗi quân domino phủ đúng một ô trắng và một ô đen.
    4. 31 quân domino phủ 31 ô trắng và 31 ô đen, không khớp với 32 và 30, nên không lát được.
  - **Lời giải:**
    1. Bất biến ở đây là: số ô trắng và số ô đen được phủ luôn bằng nhau.
    2. Phải tô màu trước thì mới đếm được số ô mỗi màu.
    3. Hai số 32 và 30 khác nhau nên không có cách lát nào.
- `tr_g3_bat_bien` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trên bảng có các số 1, 2, ..., 8. Mỗi lượt xóa hai số a, b bất kỳ và viết thêm số a + b. Sau 7 lượt trên bảng còn một số. Số đó chắc chắn là số lẻ.
  - **Đáp án:** Sai
    1. Tìm đại lượng không đổi: tính chẵn lẻ của tổng các số trên bảng.
    2. Khi thay a, b bằng a + b: Tổng mới bằng tổng cũ, nên tổng không đổi.
    3. Lúc đầu tổng là 1 + 2 + ... + 8 = 36, là số chẵn.
    4. Số cuối cùng chính là tổng lúc cuối, nên luôn là số chẵn; câu đã cho sai.
  - **Câu hỏi:** Trên bảng có các số 1, 2, ..., 5. Mỗi lượt xóa hai số a, b bất kỳ và viết thêm số a + b. Sau 4 lượt trên bảng còn một số. Số đó chắc chắn là số lẻ.
  - **Đáp án:** Đúng
    1. Tìm đại lượng không đổi: tính chẵn lẻ của tổng các số trên bảng.
    2. Khi thay a, b bằng a + b: Tổng mới bằng tổng cũ, nên tổng không đổi.
    3. Lúc đầu tổng là 1 + 2 + ... + 5 = 15, là số lẻ.
    4. Số cuối cùng chính là tổng lúc cuối, nên luôn là số lẻ; câu đã cho đúng.
  - **Câu hỏi:** Trên bảng có các số 1, 2, ..., 11. Mỗi lượt xóa hai số a, b bất kỳ và viết thêm số a + b. Sau 10 lượt trên bảng còn một số. Số đó chắc chắn là số lẻ.
  - **Đáp án:** Sai
    1. Tìm đại lượng không đổi: tính chẵn lẻ của tổng các số trên bảng.
    2. Khi thay a, b bằng a + b: Tổng mới bằng tổng cũ, nên tổng không đổi.
    3. Lúc đầu tổng là 1 + 2 + ... + 11 = 66, là số chẵn.
    4. Số cuối cùng chính là tổng lúc cuối, nên luôn là số chẵn; câu đã cho sai.
- `tr_t3_bb_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một con châu chấu bắt đầu ở điểm 0 trên trục số. Lần nhảy thứ k nó nhảy đúng k đơn vị, sang trái hoặc sang phải tùy ý. Sau 10 lần nhảy, nó có thể đứng ở bao nhiêu vị trí khác nhau?
  - **Đáp án:** 56
    1. Nếu nhảy cả 10 lần sang phải, nó tới 1 + 2 + ... + 10 = 55.
    2. Đổi chiều các bước nhảy thuộc một tập S thì vị trí là 55 - 2 . (tổng các số trong S): mọi vị trí đều là số lẻ, đó là bất biến chẵn lẻ.
    3. Tổng các phần tử của một tập con của {1, ..., 10} nhận đủ mọi giá trị từ 0 đến 55, nên vị trí nhận đủ các số lẻ từ -55 đến 55.
    4. Có 56 số lẻ như vậy.
- `tr_t3_bb_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: có 7 cái cốc đều đang úp; mỗi lượt lật đúng 2 cốc. Có thể làm cả 7 cốc ngửa lên không?
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi d là số cốc đang úp; lúc đầu d = 7.
    2. Lật 2 cốc đang úp thì d giảm 2; lật 2 cốc đang ngửa thì d tăng 2.
    3. Lật 1 cốc úp và 1 cốc ngửa thì d giảm 1.   **<- bước sai đầu tiên**
    4. Như vậy d có thể đổi tính chẵn lẻ, nên có thể đưa d từ 7 về 0.
    5. Vậy có thể làm cả 7 cốc ngửa lên.
  - **Đáp án:** Bước 3: Lật 1 cốc úp và 1 cốc ngửa thì d giảm 1.
  - **Vì sao sai, và bước đúng:**
    1. Lật 1 cốc úp và 1 cốc ngửa: cốc úp thành ngửa, cốc ngửa thành úp, nên d không đổi.
    2. Vậy mỗi lượt d đổi 0 hoặc 2: tính chẵn lẻ của d là bất biến.
    3. d = 7 lẻ, còn mục tiêu d = 0 chẵn, nên không thể làm cả 7 cốc ngửa lên.
- `tr_t3_bb_06` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một vòng tròn chia làm 6 ô, ghi theo vòng các số 1, 0, 1, 0, 0, 0. Mỗi lượt cộng thêm 1 vào hai ô kề nhau. Có thể làm cho 6 số bằng nhau không?
    - **(đúng)** Không, vì hiệu giữa tổng ba ô ở vị trí lẻ và tổng ba ô ở vị trí chẵn luôn bằng 2
    - Có, chỉ cần 2 lượt
    - Có, vì tổng các số luôn tăng
    - Không, vì tổng các số luôn là số chẵn
  - **Đáp án:** Không, vì hiệu giữa tổng ba ô ở vị trí lẻ và tổng ba ô ở vị trí chẵn luôn bằng 2
    1. Hai ô kề nhau luôn gồm một ô vị trí lẻ và một ô vị trí chẵn, nên mỗi lượt hai tổng cùng tăng 1: hiệu của chúng không đổi.
    2. Lúc đầu tổng các ô lẻ là 1 + 1 + 0 = 2, tổng các ô chẵn là 0: hiệu bằng 2.
    3. Nếu 6 số bằng nhau thì hai tổng bằng nhau, hiệu bằng 0: không bao giờ đạt được.
    4. Tổng luôn chẵn là đúng nhưng không cản được gì, vì 6 số bằng nhau có tổng chẵn.
- `tr_g3_lat_coc` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trên bàn có 6 cái cốc, trong đó 3 cốc đang úp, còn lại ngửa. Mỗi lượt phải lật đúng 2 cốc khác nhau. Có thể sau một số lượt làm cho mọi cốc đều ngửa.
  - **Đáp án:** Sai
    1. Gọi d là số cốc đang úp. Lật 2 cốc: d giảm 2, tăng 2 hoặc giữ nguyên (một úp, một ngửa).
    2. Vậy tính chẵn lẻ của d không bao giờ đổi: đó là bất biến.
    3. Lúc đầu d = 3 là số lẻ, còn mục tiêu d = 0 là số chẵn, nên không thể đạt tới.
  - **Câu hỏi:** Trên bàn có 5 cái cốc, trong đó 1 cốc đang úp, còn lại ngửa. Mỗi lượt phải lật đúng 2 cốc khác nhau. Có thể sau một số lượt làm cho mọi cốc đều ngửa.
  - **Đáp án:** Sai
    1. Gọi d là số cốc đang úp. Lật 2 cốc: d giảm 2, tăng 2 hoặc giữ nguyên (một úp, một ngửa).
    2. Vậy tính chẵn lẻ của d không bao giờ đổi: đó là bất biến.
    3. Lúc đầu d = 1 là số lẻ, còn mục tiêu d = 0 là số chẵn, nên không thể đạt tới.
  - **Câu hỏi:** Trên bàn có 6 cái cốc, trong đó 3 cốc đang úp, còn lại ngửa. Mỗi lượt phải lật đúng 2 cốc khác nhau. Có thể sau một số lượt làm cho mọi cốc đều ngửa.
  - **Đáp án:** Sai
    1. Gọi d là số cốc đang úp. Lật 2 cốc: d giảm 2, tăng 2 hoặc giữ nguyên (một úp, một ngửa).
    2. Vậy tính chẵn lẻ của d không bao giờ đổi: đó là bất biến.
    3. Lúc đầu d = 3 là số lẻ, còn mục tiêu d = 0 là số chẵn, nên không thể đạt tới.

### Thứ tự từ điển (`tr_t3_tu_dien`)

- `tr_t3_td_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Theo thứ tự từ điển, xâu 0110 đứng trước xâu 0101.
  - **Đáp án:** Sai
    1. So từng chữ số từ trái sang phải: hai xâu giống nhau ở hai chữ số đầu 0, 1.
    2. Chữ số thứ ba: 1 và 0. Xâu có chữ số nhỏ hơn ở vị trí khác nhau đầu tiên đứng trước.
    3. Vậy 0101 đứng trước 0110.
- `tr_t3_td_02` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước so sánh hai hoán vị (2, 4, 1, 3) và (2, 3, 4, 1) theo thứ tự từ điển.
  - **Đáp án (thứ tự đúng):**
    1. So sánh thành phần thứ nhất: cả hai đều là 2, chưa phân định.
    2. So sánh thành phần thứ hai: 4 và 3 khác nhau.
    3. Vị trí khác nhau đầu tiên quyết định thứ tự: 3 nhỏ hơn 4.
    4. Vậy (2, 3, 4, 1) đứng trước (2, 4, 1, 3).
  - **Lời giải:**
    1. Thứ tự từ điển so sánh từ trái sang phải và dừng ở vị trí khác nhau đầu tiên.
    2. Các thành phần sau vị trí đó không còn ảnh hưởng gì: 4, 1 hay 1, 3 đều không cần xét.
    3. (2, 3, ...) đứng trước (2, 4, ...).
- `tr_t3_td_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong bốn xâu sau, xâu nào đứng đầu tiên theo thứ tự từ điển (a < b < c < d)?
    - **(đúng)** abca
    - abcb
    - abda
    - acaa
  - **Đáp án:** abca
    1. Ba xâu đầu cùng bắt đầu bằng ab, còn acaa có chữ thứ hai là c, lớn hơn b, nên acaa đứng sau ba xâu kia.
    2. Trong ba xâu bắt đầu bằng ab: abda có chữ thứ ba là d, lớn hơn c, nên đứng sau abca và abcb.
    3. So abca với abcb: chữ thứ tư a nhỏ hơn b, nên abca đứng đầu.
- `tr_g3_so_sanh` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Theo thứ tự từ điển, hoán vị (1, 2, 4, 3) đứng trước hoán vị (4, 2, 3, 1).
  - **Đáp án:** Đúng
    1. So sánh từng thành phần từ trái sang phải; vị trí khác nhau đầu tiên quyết định thứ tự.
    2. Hai hoán vị giống nhau ở 0 thành phần đầu và khác nhau ở thành phần thứ 1: 1 và 4.
    3. 1 nhỏ hơn, nên (1, 2, 4, 3) đứng trước; câu đã cho đúng.
  - **Câu hỏi:** Theo thứ tự từ điển, hoán vị (1, 4, 2, 3) đứng trước hoán vị (3, 2, 1, 4).
  - **Đáp án:** Đúng
    1. So sánh từng thành phần từ trái sang phải; vị trí khác nhau đầu tiên quyết định thứ tự.
    2. Hai hoán vị giống nhau ở 0 thành phần đầu và khác nhau ở thành phần thứ 1: 1 và 3.
    3. 1 nhỏ hơn, nên (1, 4, 2, 3) đứng trước; câu đã cho đúng.
  - **Câu hỏi:** Theo thứ tự từ điển, hoán vị (2, 4, 3, 1) đứng trước hoán vị (1, 2, 3, 4).
  - **Đáp án:** Sai
    1. So sánh từng thành phần từ trái sang phải; vị trí khác nhau đầu tiên quyết định thứ tự.
    2. Hai hoán vị giống nhau ở 0 thành phần đầu và khác nhau ở thành phần thứ 1: 2 và 1.
    3. 1 nhỏ hơn, nên (1, 2, 3, 4) đứng trước; câu đã cho sai.
- `tr_t3_td_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các tập con k phần tử của {1, 2, ..., n} theo thứ tự từ điển, mỗi tập viết các phần tử tăng dần (1 <= k <= n). Tập đứng cuối cùng là {n - k + 1, n - k + 2, ..., n}.
  - **Đáp án:** Đúng
    1. Phần tử thứ i của một tập viết tăng dần nhiều nhất là n - k + i, vì sau nó còn k - i phần tử lớn hơn.
    2. Tập {n - k + 1, ..., n} đạt giá trị lớn nhất ở mọi vị trí cùng lúc.
    3. Nên nó lớn hơn mọi tập khác ở vị trí khác nhau đầu tiên: nó đứng cuối.
- `tr_t3_td_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: xếp bốn xâu 1021, 1102, 1012, 0221 theo thứ tự từ điển.
  - **Lời giải đưa ra (có một bước sai):**
    1. Xâu bắt đầu bằng 0 đứng trước mọi xâu bắt đầu bằng 1, nên 0221 đứng đầu.
    2. Trong ba xâu còn lại, so chữ số thứ hai: 1021 và 1012 có 0, còn 1102 có 1, nên 1102 đứng cuối.
    3. So 1021 với 1012: chữ số thứ ba là 2 và 1, nên 1021 đứng trước 1012.   **<- bước sai đầu tiên**
    4. Thứ tự là 0221, 1021, 1012, 1102.
  - **Đáp án:** Bước 3: So 1021 với 1012: chữ số thứ ba là 2 và 1, nên 1021 đứng trước 1012.
  - **Vì sao sai, và bước đúng:**
    1. Ở vị trí khác nhau đầu tiên, xâu có chữ số nhỏ hơn đứng trước; 1 nhỏ hơn 2.
    2. Vậy 1012 đứng trước 1021.
    3. Thứ tự đúng là 0221, 1012, 1021, 1102.

### Phương pháp sinh (`tr_t3_sinh_ke_tiep`)

- `tr_t3_sk_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các xâu nhị phân độ dài 5 theo thứ tự từ điển. Xâu liền sau xâu 10111 là xâu nào?
    - **(đúng)** 11000
    - 10110
    - 11111
    - 01000
  - **Đáp án:** 11000
    1. Từ phải sang trái tìm chữ số 0 đầu tiên: đó là chữ số thứ hai.
    2. Đổi nó thành 1 và đổi mọi chữ số bên phải nó thành 0.
    3. Được 11000. Giống như cộng 1 vào số nhị phân 10111 = 23 được 24 = 11000.
- `tr_t3_sk_02` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm hoán vị liền sau của (1, 3, 5, 4, 2) theo thứ tự từ điển.
  - **Đáp án (thứ tự đúng):**
    1. Từ phải sang trái, tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: đó là số 3 ở vị trí thứ hai.
    2. Trong đoạn bên phải nó là (5, 4, 2), tìm số nhỏ nhất còn lớn hơn 3: đó là số 4.
    3. Đổi chỗ 3 và 4: được (1, 4, 5, 3, 2).
    4. Đảo ngược đoạn sau vị trí thứ hai: được (1, 4, 2, 3, 5).
  - **Lời giải:**
    1. Đoạn (5, 4, 2) đã giảm dần, tức là đã lớn nhất có thể; phải tăng số đứng ngay trước nó.
    2. Tăng 3 lên ít nhất có thể: thay bằng 4, số nhỏ nhất bên phải còn lớn hơn 3.
    3. Đoạn sau đó phải nhỏ nhất có thể, tức là tăng dần: (2, 3, 5).
- `tr_t3_sk_03` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi sinh các xâu nhị phân độ dài 4 theo thứ tự từ điển, xâu 1111 là cấu hình cuối cùng, nên nó không có xâu liền sau.
  - **Đáp án:** Đúng
    1. Phương pháp sinh tìm chữ số 0 đầu tiên từ phải sang trái để đổi thành 1.
    2. Xâu 1111 không có chữ số 0 nào, nên không sinh được xâu tiếp theo.
    3. Đó là dấu hiệu dừng của thuật toán: 1111 ứng với số 15, lớn nhất trong 0 đến 15.
- `tr_g3_tap_con_ke_tiep` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các tập con 4 phần tử của {1, 2, ..., 6} theo thứ tự từ điển, mỗi tập viết các phần tử tăng dần. Tìm tập liền sau {1, 2, 3, 6}. Nhập các phần tử theo thứ tự tăng dần.
  - **Đáp án:** 1, 2, 4, 5
    1. Phần tử ở vị trí thứ j (tính từ 1) lớn nhất được phép là 6 - 4 + j.
    2. Từ phải sang trái, phần tử đầu tiên chưa đạt giá trị lớn nhất của nó là 3 (vị trí thứ 3).
    3. Tăng nó lên 4, các phần tử sau nó lấy các số liền tiếp: {1, 2, 4, 5}.
  - **Câu hỏi:** Sinh các tập con 2 phần tử của {1, 2, ..., 5} theo thứ tự từ điển, mỗi tập viết các phần tử tăng dần. Tìm tập liền sau {1, 3}. Nhập các phần tử theo thứ tự tăng dần.
  - **Đáp án:** 1, 4
    1. Phần tử ở vị trí thứ j (tính từ 1) lớn nhất được phép là 5 - 2 + j.
    2. Từ phải sang trái, phần tử đầu tiên chưa đạt giá trị lớn nhất của nó là 3 (vị trí thứ 2).
    3. Tăng nó lên 4, các phần tử sau nó lấy các số liền tiếp: {1, 4}.
  - **Câu hỏi:** Sinh các tập con 4 phần tử của {1, 2, ..., 6} theo thứ tự từ điển, mỗi tập viết các phần tử tăng dần. Tìm tập liền sau {2, 3, 4, 5}. Nhập các phần tử theo thứ tự tăng dần.
  - **Đáp án:** 2, 3, 4, 6
    1. Phần tử ở vị trí thứ j (tính từ 1) lớn nhất được phép là 6 - 4 + j.
    2. Từ phải sang trái, phần tử đầu tiên chưa đạt giá trị lớn nhất của nó là 5 (vị trí thứ 4).
    3. Tăng nó lên 6, các phần tử sau nó lấy các số liền tiếp: {2, 3, 4, 6}.
- `tr_g3_xau_ke_tiep` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các xâu nhị phân độ dài 6 theo thứ tự từ điển. Tìm xâu liền sau xâu 010111. Nhập các chữ số của nó, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 1, 1, 0, 0, 0
    1. Từ phải sang trái, tìm chữ số 0 đầu tiên gặp được.
    2. Đó là chữ số thứ 3. Đổi nó thành 1, và đổi mọi chữ số bên phải nó thành 0.
    3. Xâu liền sau là 011000.
  - **Câu hỏi:** Sinh các xâu nhị phân độ dài 5 theo thứ tự từ điển. Tìm xâu liền sau xâu 00101. Nhập các chữ số của nó, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 0, 1, 1, 0
    1. Từ phải sang trái, tìm chữ số 0 đầu tiên gặp được.
    2. Đó là chữ số thứ 4. Đổi nó thành 1, và đổi mọi chữ số bên phải nó thành 0.
    3. Xâu liền sau là 00110.
  - **Câu hỏi:** Sinh các xâu nhị phân độ dài 6 theo thứ tự từ điển. Tìm xâu liền sau xâu 011001. Nhập các chữ số của nó, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 1, 1, 0, 1, 0
    1. Từ phải sang trái, tìm chữ số 0 đầu tiên gặp được.
    2. Đó là chữ số thứ 5. Đổi nó thành 1, và đổi mọi chữ số bên phải nó thành 0.
    3. Xâu liền sau là 011010.
- `tr_t3_sk_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các tập con 3 phần tử của {1, 2, 3, 4, 5, 6} theo thứ tự từ điển, mỗi tập viết tăng dần. Tìm tập liền sau {1, 5, 6}. Nhập ba phần tử theo thứ tự tăng dần.
  - **Đáp án:** 2, 3, 4
    1. Giá trị lớn nhất được phép ở ba vị trí là 4, 5, 6.
    2. Từ phải sang trái: 6 và 5 đã đạt giá trị lớn nhất; phần tử đầu tiên chưa đạt là 1 (lớn nhất là 4).
    3. Tăng 1 lên 2, hai phần tử sau lấy các số liền tiếp 3, 4.
    4. Tập liền sau là {2, 3, 4}.
- `tr_t3_sk_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tìm hoán vị liền sau của (2, 4, 3, 1) theo thứ tự từ điển.
  - **Lời giải đưa ra (có một bước sai):**
    1. Từ phải sang trái, đoạn (4, 3, 1) giảm dần, nên vị trí cần đổi là số 2 ở đầu.
    2. Trong (4, 3, 1), số nhỏ nhất còn lớn hơn 2 là 3.
    3. Đổi chỗ 2 và 3: được (3, 4, 2, 1).
    4. Giữ nguyên đoạn sau vị trí đầu: hoán vị liền sau là (3, 4, 2, 1).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Giữ nguyên đoạn sau vị trí đầu: hoán vị liền sau là (3, 4, 2, 1).
  - **Vì sao sai, và bước đúng:**
    1. Sau khi đổi chỗ, đoạn sau vị trí đầu là (4, 2, 1), vẫn giảm dần; phải đảo ngược nó thành (1, 2, 4).
    2. Hoán vị liền sau là (3, 1, 2, 4).
    3. Nếu giữ (3, 4, 2, 1) thì đã bỏ qua các hoán vị (3, 1, 2, 4), (3, 1, 4, 2), ... nằm giữa.
- `tr_t3_sk_06` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các tập con 2 phần tử của {1, 2, 3, 4, 5} theo thứ tự từ điển. Ghép mỗi tập với tập liền sau nó.
  - **Đáp án (ghép đúng):**
    - {1, 2} — {1, 3}
    - {1, 5} — {2, 3}
    - {2, 5} — {3, 4}
    - {3, 5} — {4, 5}
  - **Lời giải:**
    1. Phần tử thứ hai lớn nhất là 5, phần tử thứ nhất lớn nhất là 4.
    2. Nếu phần tử thứ hai chưa bằng 5 thì tăng nó: {1, 2} thành {1, 3}.
    3. Nếu phần tử thứ hai đã bằng 5 thì tăng phần tử thứ nhất lên 1 và lấy số liền sau: {1, 5} thành {2, 3}, {2, 5} thành {3, 4}, {3, 5} thành {4, 5}.
- `tr_g3_hoan_vi_ke_tiep` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Sinh các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển. Tìm hoán vị liền sau (1, 2, 4, 3). Nhập các số theo thứ tự.
  - **Đáp án:** 1, 3, 2, 4
    1. Từ phải sang trái, tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: số 2 ở vị trí 2.
    2. Trong đoạn bên phải nó, số nhỏ nhất còn lớn hơn 2 là 3; đổi chỗ hai số này.
    3. Đoạn bên phải lúc này giảm dần; đảo ngược nó để thành tăng dần.
    4. Hoán vị liền sau là (1, 3, 2, 4).
  - **Câu hỏi:** Sinh các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển. Tìm hoán vị liền sau (1, 4, 2, 3). Nhập các số theo thứ tự.
  - **Đáp án:** 1, 4, 3, 2
    1. Từ phải sang trái, tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: số 2 ở vị trí 3.
    2. Trong đoạn bên phải nó, số nhỏ nhất còn lớn hơn 2 là 3; đổi chỗ hai số này.
    3. Đoạn bên phải lúc này giảm dần; đảo ngược nó để thành tăng dần.
    4. Hoán vị liền sau là (1, 4, 3, 2).
  - **Câu hỏi:** Sinh các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển. Tìm hoán vị liền sau (2, 4, 3, 1). Nhập các số theo thứ tự.
  - **Đáp án:** 3, 1, 2, 4
    1. Từ phải sang trái, tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: số 2 ở vị trí 1.
    2. Trong đoạn bên phải nó, số nhỏ nhất còn lớn hơn 2 là 3; đổi chỗ hai số này.
    3. Đoạn bên phải lúc này giảm dần; đảo ngược nó để thành tăng dần.
    4. Hoán vị liền sau là (3, 1, 2, 4).

### Thứ hạng của cấu hình (`tr_t3_thu_hang`)

- `tr_t3_th_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp mọi xâu nhị phân độ dài 5 theo thứ tự từ điển, xâu 00000 đứng thứ 1. Xâu 01101 đứng thứ mấy?
  - **Đáp án:** 14
    1. Các xâu độ dài 5 xếp theo thứ tự từ điển đúng như các số 0 đến 31 viết trong hệ nhị phân.
    2. 01101 biểu diễn số 8 + 4 + 1 = 13.
    3. Có 13 xâu đứng trước nó (ứng với 0 đến 12), nên nó đứng thứ 14.
- `tr_t3_th_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các hoán vị của {1, 2, 3, 4} theo thứ tự từ điển thì hoán vị (4, 3, 2, 1) đứng thứ 24.
  - **Đáp án:** Đúng
    1. Có 4! = 24 hoán vị.
    2. (4, 3, 2, 1) giảm dần ở mọi chỗ, nên ở mọi vị trí nó mang số lớn nhất còn lại: nó đứng cuối.
    3. Vậy nó đứng thứ 24.
- `tr_t3_th_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: xếp các xâu nhị phân độ dài 4 theo thứ tự từ điển, xâu 0000 đứng thứ 1; xâu 1011 đứng thứ mấy?
  - **Lời giải đưa ra (có một bước sai):**
    1. Theo thứ tự từ điển, các xâu độ dài 4 được xếp đúng như các số 0, 1, ..., 15 viết trong hệ nhị phân.
    2. Đổi 1011 sang hệ mười: 8 + 2 + 1 = 11.
    3. Xâu 0000 ứng với số 0 và đứng thứ 1, nên xâu ứng với số m đứng thứ m.   **<- bước sai đầu tiên**
    4. Vậy 1011 đứng thứ 11.
  - **Đáp án:** Bước 3: Xâu 0000 ứng với số 0 và đứng thứ 1, nên xâu ứng với số m đứng thứ m.
  - **Vì sao sai, và bước đúng:**
    1. Số 0 đứng thứ 1, số 1 đứng thứ 2, ..., nên số m đứng thứ m + 1.
    2. 1011 ứng với số 11, nên đứng thứ 12.
    3. Lỗi lệch một vị trí này rất hay gặp khi đánh số từ 1 mà đếm từ 0.
- `tr_g3_hang_xau` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xếp mọi xâu nhị phân độ dài 5 theo thứ tự từ điển, xâu 00000 đứng thứ 1. Xâu 01011 đứng thứ mấy?
  - **Đáp án:** 12
    1. Theo thứ tự từ điển, các xâu độ dài n xếp đúng như các số 0, 1, 2, ... viết trong hệ nhị phân.
    2. Xâu 01011 biểu diễn số 2^3 + 2^1 + 2^0 = 11.
    3. Có 11 xâu đứng trước nó (ứng với 0, 1, ..., 10) nên nó đứng thứ 12.
  - **Câu hỏi:** Xếp mọi xâu nhị phân độ dài 4 theo thứ tự từ điển, xâu 0000 đứng thứ 1. Xâu 0010 đứng thứ mấy?
  - **Đáp án:** 3
    1. Theo thứ tự từ điển, các xâu độ dài n xếp đúng như các số 0, 1, 2, ... viết trong hệ nhị phân.
    2. Xâu 0010 biểu diễn số 2^1 = 2.
    3. Có 2 xâu đứng trước nó (ứng với 0, 1, ..., 1) nên nó đứng thứ 3.
  - **Câu hỏi:** Xếp mọi xâu nhị phân độ dài 5 theo thứ tự từ điển, xâu 00000 đứng thứ 1. Xâu 01100 đứng thứ mấy?
  - **Đáp án:** 13
    1. Theo thứ tự từ điển, các xâu độ dài n xếp đúng như các số 0, 1, 2, ... viết trong hệ nhị phân.
    2. Xâu 01100 biểu diễn số 2^3 + 2^2 = 12.
    3. Có 12 xâu đứng trước nó (ứng với 0, 1, ..., 11) nên nó đứng thứ 13.
- `tr_t3_th_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu hoán vị của {1, 2, 3, 4, 5} đứng trước hoán vị (3, 1, 2, 4, 5) theo thứ tự từ điển?
  - **Đáp án:** 48
    1. Các hoán vị bắt đầu bằng 1 hoặc 2 đều đứng trước: 2 . 4! = 48.
    2. Trong các hoán vị bắt đầu bằng 3, phần sau (1, 2, 4, 5) đã tăng dần, tức là nhỏ nhất: không có hoán vị nào bắt đầu bằng 3 đứng trước nó.
    3. Vậy có 48 hoán vị đứng trước, và (3, 1, 2, 4, 5) đứng thứ 49.
- `tr_t3_th_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các hoán vị của {1, 2, 3, 4} theo thứ tự từ điển. Sắp xếp các bước tìm vị trí của hoán vị (2, 3, 1, 4).
  - **Đáp án (thứ tự đúng):**
    1. Đếm các hoán vị bắt đầu bằng số nhỏ hơn 2: chỉ có số 1, được 1 . 3! = 6 hoán vị.
    2. Giữ số đầu là 2, đếm các hoán vị có số thứ hai nhỏ hơn 3 trong {1, 3, 4}: chỉ có số 1, được 1 . 2! = 2 hoán vị.
    3. Giữ (2, 3), số thứ ba là 1 đã nhỏ nhất trong {1, 4}: không có thêm hoán vị nào.
    4. Có 6 + 2 = 8 hoán vị đứng trước, nên (2, 3, 1, 4) đứng thứ 9.
  - **Lời giải:**
    1. Thứ hạng đếm từ trái sang phải: ở mỗi vị trí, đặt một số nhỏ hơn số đang có thì mọi cách xếp phần còn lại đều đứng trước.
    2. Vị trí 1 cho 6, vị trí 2 cho 2, vị trí 3 cho 0 hoán vị đứng trước.
    3. Thêm 1 vì vị trí bắt đầu từ 1: đứng thứ 9.
- `tr_t3_th_05` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các tập con 2 phần tử của {1, 2, 3, 4, 5} theo thứ tự từ điển, mỗi tập viết tăng dần, {1, 2} đứng thứ 1. Tập đứng thứ 7 là tập nào?
    - **(đúng)** {2, 5}
    - {2, 4}
    - {3, 4}
    - {1, 5}
  - **Đáp án:** {2, 5}
    1. Các tập bắt đầu bằng 1: {1, 2}, {1, 3}, {1, 4}, {1, 5}, chiếm vị trí 1 đến 4.
    2. Các tập bắt đầu bằng 2: {2, 3}, {2, 4}, {2, 5} ở vị trí 5, 6, 7.
    3. Vậy tập thứ 7 là {2, 5}.
- `tr_g3_hang_hoan_vi` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển, hoán vị (1, 2, 3, 4) đứng thứ 1. Hoán vị (1, 2, 4, 3) đứng thứ mấy?
  - **Đáp án:** 2
    1. Đếm các hoán vị đứng trước: ở mỗi vị trí, đặt một số nhỏ hơn chưa dùng thì mọi cách xếp phần còn lại đều đứng trước.
    2. vị trí 1 là 1: còn 0 số nhỏ hơn chưa dùng, 0 . 3! = 0; vị trí 2 là 2: còn 0 số nhỏ hơn chưa dùng, 0 . 2! = 0; vị trí 3 là 4: còn 1 số nhỏ hơn chưa dùng, 1 . 1! = 1.
    3. Có 1 hoán vị đứng trước, nên (1, 2, 4, 3) đứng thứ 2.
  - **Câu hỏi:** Xếp các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển, hoán vị (1, 2, 3, 4) đứng thứ 1. Hoán vị (1, 4, 2, 3) đứng thứ mấy?
  - **Đáp án:** 5
    1. Đếm các hoán vị đứng trước: ở mỗi vị trí, đặt một số nhỏ hơn chưa dùng thì mọi cách xếp phần còn lại đều đứng trước.
    2. vị trí 1 là 1: còn 0 số nhỏ hơn chưa dùng, 0 . 3! = 0; vị trí 2 là 4: còn 2 số nhỏ hơn chưa dùng, 2 . 2! = 4; vị trí 3 là 2: còn 0 số nhỏ hơn chưa dùng, 0 . 1! = 0.
    3. Có 4 hoán vị đứng trước, nên (1, 4, 2, 3) đứng thứ 5.
  - **Câu hỏi:** Xếp các hoán vị của {1, 2, ..., 4} theo thứ tự từ điển, hoán vị (1, 2, 3, 4) đứng thứ 1. Hoán vị (2, 4, 3, 1) đứng thứ mấy?
  - **Đáp án:** 12
    1. Đếm các hoán vị đứng trước: ở mỗi vị trí, đặt một số nhỏ hơn chưa dùng thì mọi cách xếp phần còn lại đều đứng trước.
    2. vị trí 1 là 2: còn 1 số nhỏ hơn chưa dùng, 1 . 3! = 6; vị trí 2 là 4: còn 2 số nhỏ hơn chưa dùng, 2 . 2! = 4; vị trí 3 là 3: còn 1 số nhỏ hơn chưa dùng, 1 . 1! = 1.
    3. Có 11 hoán vị đứng trước, nên (2, 4, 3, 1) đứng thứ 12.
- `tr_g3_hang_tap_con` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xếp các tập con 2 phần tử của {1, 2, ..., 6} theo thứ tự từ điển (mỗi tập viết tăng dần), tập {1, 2} đứng thứ 1. Tập {1, 3} đứng thứ mấy?
  - **Đáp án:** 2
    1. Đếm các tập đứng trước: giữ nguyên các phần tử đầu, đặt ở một vị trí một số nhỏ hơn rồi đếm mọi cách chọn các phần tử còn lại lớn hơn nó.
    2. vị trí 2 đặt số từ 2 đến 2 thay cho 3: 1 tập.
    3. Có 1 tập đứng trước, nên {1, 3} đứng thứ 2.
  - **Câu hỏi:** Xếp các tập con 2 phần tử của {1, 2, ..., 5} theo thứ tự từ điển (mỗi tập viết tăng dần), tập {1, 2} đứng thứ 1. Tập {1, 3} đứng thứ mấy?
  - **Đáp án:** 2
    1. Đếm các tập đứng trước: giữ nguyên các phần tử đầu, đặt ở một vị trí một số nhỏ hơn rồi đếm mọi cách chọn các phần tử còn lại lớn hơn nó.
    2. vị trí 2 đặt số từ 2 đến 2 thay cho 3: 1 tập.
    3. Có 1 tập đứng trước, nên {1, 3} đứng thứ 2.
  - **Câu hỏi:** Xếp các tập con 2 phần tử của {1, 2, ..., 6} theo thứ tự từ điển (mỗi tập viết tăng dần), tập {1, 2} đứng thứ 1. Tập {3, 5} đứng thứ mấy?
  - **Đáp án:** 11
    1. Đếm các tập đứng trước: giữ nguyên các phần tử đầu, đặt ở một vị trí một số nhỏ hơn rồi đếm mọi cách chọn các phần tử còn lại lớn hơn nó.
    2. vị trí 1 đặt số từ 1 đến 2 thay cho 3: 9 tập; vị trí 2 đặt số từ 4 đến 4 thay cho 5: 1 tập.
    3. Có 10 tập đứng trước, nên {3, 5} đứng thứ 11.

### Thuật toán quay lui (`tr_t3_quay_lui`)

- `tr_t3_ql_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thuật toán quay lui liệt kê các xâu nhị phân độ dài n (thử 0 rồi 1 ở mỗi vị trí, không có ràng buộc nào) in ra đúng 2^n xâu.
  - **Đáp án:** Đúng
    1. Không có ràng buộc thì không nhánh nào bị cắt: mọi lựa chọn đều đi tới cuối.
    2. Mỗi vị trí có 2 lựa chọn, n vị trí cho 2^n lá trên cây tìm kiếm.
    3. Mỗi lá là một xâu được in ra đúng một lần.
- `tr_t3_ql_02` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước của thủ tục quay lui Try(i) chọn thành phần x_i khi liệt kê các xâu nhị phân x_1 x_2 ... x_n.
  - **Đáp án (thứ tự đúng):**
    1. Với mỗi giá trị v lần lượt là 0 rồi 1, gán x_i = v.
    2. Nếu i = n thì xâu đã đủ dài: in ra x_1 x_2 ... x_n.
    3. Ngược lại, nếu i < n thì gọi Try(i + 1) để chọn thành phần tiếp theo.
    4. Thử xong cả hai giá trị của x_i thì kết thúc Try(i), quay lui về lời gọi trước.
  - **Lời giải:**
    1. Quay lui xây cấu hình từng thành phần một: chọn x_i, rồi hoặc in ra, hoặc đi tiếp.
    2. Khi lời gọi sâu hơn kết thúc, vòng lặp ở Try(i) thử giá trị tiếp theo của x_i.
    3. Hết giá trị để thử thì Try(i) trả về: đó chính là bước quay lui.
- `tr_t3_ql_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quay lui liệt kê các hoán vị của {1, 2, 3}. Khi đã chọn x_1 = 2, những giá trị nào còn được thử cho x_2?
    - **(đúng)** 1 và 3
    - 1, 2 và 3
    - Chỉ 3
    - Chỉ 1
  - **Đáp án:** 1 và 3
    1. Một hoán vị không dùng một số hai lần, nên x_2 chỉ nhận các số chưa dùng.
    2. Số 2 đã dùng cho x_1, còn lại 1 và 3.
    3. Quay lui thử x_2 = 1 (được 2, 1, 3) rồi x_2 = 3 (được 2, 3, 1).
- `tr_g3_quay_lui_tong` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi bộ (x_1, x_2, x_3) gồm các số nguyên với 0 <= x_i <= 3 và x_1 + x_2 + x_3 = 7. Nó in ra bao nhiêu bộ?
  - **Đáp án:** 6
    1. Quay lui chọn x_1, rồi x_2; khi đó x_3 = tổng còn lại, chỉ nhận nếu 0 <= x_3 <= 3.
    2. Số bộ in ra theo từng giá trị x_1 = 0, 1, ...: 0, 1, 2, 3.
    3. Cộng lại: 0 + 1 + 2 + 3 = 6.
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi bộ (x_1, x_2, x_3) gồm các số nguyên với 0 <= x_i <= 2 và x_1 + x_2 + x_3 = 2. Nó in ra bao nhiêu bộ?
  - **Đáp án:** 6
    1. Quay lui chọn x_1, rồi x_2; khi đó x_3 = tổng còn lại, chỉ nhận nếu 0 <= x_3 <= 2.
    2. Số bộ in ra theo từng giá trị x_1 = 0, 1, ...: 3, 2, 1.
    3. Cộng lại: 3 + 2 + 1 = 6.
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi bộ (x_1, x_2, x_3) gồm các số nguyên với 0 <= x_i <= 3 và x_1 + x_2 + x_3 = 7. Nó in ra bao nhiêu bộ?
  - **Đáp án:** 6
    1. Quay lui chọn x_1, rồi x_2; khi đó x_3 = tổng còn lại, chỉ nhận nếu 0 <= x_3 <= 3.
    2. Số bộ in ra theo từng giá trị x_1 = 0, 1, ...: 0, 1, 2, 3.
    3. Cộng lại: 0 + 1 + 2 + 3 = 6.
- `tr_t3_ql_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đặt 4 quân hậu lên bàn cờ 4 x 4 sao cho không hai quân nào cùng hàng, cùng cột hay cùng đường chéo. Thuật toán quay lui, đặt mỗi hàng một quân, tìm được bao nhiêu cách đặt?
  - **Đáp án:** 2
    1. Ghi cột của quân hậu ở hàng 1, 2, 3, 4 thành một dãy; hàng 1 thử lần lượt cột 1 đến 4.
    2. Hàng 1 ở cột 1 hay cột 4: mọi nhánh đều tới ngõ cụt ở hàng 3 hoặc hàng 4.
    3. Hàng 1 ở cột 2 cho đúng một cách: (2, 4, 1, 3). Hàng 1 ở cột 3 cho đúng một cách: (3, 1, 4, 2).
    4. Vậy có 2 cách đặt, hai cách này đối xứng nhau qua trục giữa bàn cờ.
- `tr_t3_ql_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: liệt kê các tập con của {1, 2, 3, 4, 5} có tổng các phần tử bằng 6.
  - **Lời giải đưa ra (có một bước sai):**
    1. Xét các tập theo phần tử nhỏ nhất, chọn các phần tử tăng dần và cắt nhánh khi tổng vượt 6.
    2. Phần tử nhỏ nhất là 1: cần thêm tổng 5 từ các số 2, 3, 4, 5, được {1, 5} và {1, 2, 3}.
    3. Phần tử nhỏ nhất là 2: cần thêm tổng 4 từ các số 3, 4, 5, được {2, 4}.
    4. Phần tử nhỏ nhất là 3: cần thêm tổng 3 từ các số 4, 5, được {3, 3}.   **<- bước sai đầu tiên**
    5. Vậy có 4 tập con có tổng bằng 6.
  - **Đáp án:** Bước 4: Phần tử nhỏ nhất là 3: cần thêm tổng 3 từ các số 4, 5, được {3, 3}.
  - **Vì sao sai, và bước đúng:**
    1. Khi phần tử nhỏ nhất là 3, các phần tử còn lại phải lấy trong 4, 5, mà số nào cũng lớn hơn 3: nhánh này không cho tập nào. {3, 3} không phải là tập con hai phần tử, vì một phần tử không được dùng hai lần.
    2. Phần tử nhỏ nhất là 4 hay 5 cũng không cho tập nào (4 cần thêm 2, 5 cần thêm 1).
    3. Vậy có 3 tập: {1, 5}, {1, 2, 3}, {2, 4}.
- `tr_t3_ql_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong thuật toán quay lui, nếu một cấu hình bộ phận x_1, ..., x_i đã vi phạm ràng buộc của bài toán (ràng buộc mà thêm thành phần nào cũng không sửa được) thì có thể bỏ qua mọi cấu hình mở rộng từ nó.
  - **Đáp án:** Đúng
    1. Mọi cấu hình đầy đủ mở rộng từ x_1, ..., x_i đều chứa phần đầu đã vi phạm đó.
    2. Vì ràng buộc không sửa được bằng các thành phần sau, không cấu hình nào trong nhánh là lời giải.
    3. Cắt nhánh như vậy là điều làm quay lui nhanh hơn hẳn duyệt toàn bộ.
- `tr_g3_quay_lui_tap_con` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi tập con của {1, 2, ..., 7} có tổng các phần tử bằng 16. Nó in ra bao nhiêu tập?
  - **Đáp án:** 8
    1. Quay lui xét lần lượt từng số 1, 2, ..., n: chọn hoặc không chọn, và cắt nhánh ngay khi tổng đã vượt 16.
    2. Đếm gọn hơn: gọi T(v, t) là số tập con của {1, ..., v} có tổng t; T(v, t) = T(v - 1, t) + T(v - 1, t - v) (không chọn v, hoặc chọn v).
    3. Tính bảng đó đến v = 7, t = 16 được 8 tập.
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi tập con của {1, 2, ..., 6} có tổng các phần tử bằng 7. Nó in ra bao nhiêu tập?
  - **Đáp án:** 4
    1. Quay lui xét lần lượt từng số 1, 2, ..., n: chọn hoặc không chọn, và cắt nhánh ngay khi tổng đã vượt 7.
    2. Đếm gọn hơn: gọi T(v, t) là số tập con của {1, ..., v} có tổng t; T(v, t) = T(v - 1, t) + T(v - 1, t - v) (không chọn v, hoặc chọn v).
    3. Tính bảng đó đến v = 6, t = 7 được 4 tập.
  - **Câu hỏi:** Thuật toán quay lui liệt kê mọi tập con của {1, 2, ..., 7} có tổng các phần tử bằng 16. Nó in ra bao nhiêu tập?
  - **Đáp án:** 8
    1. Quay lui xét lần lượt từng số 1, 2, ..., n: chọn hoặc không chọn, và cắt nhánh ngay khi tổng đã vượt 16.
    2. Đếm gọn hơn: gọi T(v, t) là số tập con của {1, ..., v} có tổng t; T(v, t) = T(v - 1, t) + T(v - 1, t - v) (không chọn v, hoặc chọn v).
    3. Tính bảng đó đến v = 7, t = 16 được 8 tập.
