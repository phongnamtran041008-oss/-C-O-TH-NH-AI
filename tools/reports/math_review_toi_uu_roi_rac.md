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

## Tầng 4: Bài toán tối ưu tổ hợp và độ phức tạp thuật toán

36 dạng câu (27 câu viết tay, 9 bộ sinh câu); 36 chưa duyệt.

### Phát biểu bài toán tối ưu tổ hợp (`tr_t4_phat_bieu`)

- `tr_t4_pb_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán cái túi: có n đồ vật, đồ vật i nặng a_i và có giá trị c_i; túi chịu được khối lượng tối đa b; mỗi đồ vật lấy hoặc không lấy. Một phương án chấp nhận được của bài toán là gì?
    - **(đúng)** Một xâu nhị phân x_1 x_2 ... x_n với a_1 x_1 + a_2 x_2 + ... + a_n x_n <= b
    - Một hoán vị của n đồ vật
    - Một xâu nhị phân x_1 x_2 ... x_n bất kỳ, không cần điều kiện gì
    - Một số thực x giữa 0 và b
  - **Đáp án:** Một xâu nhị phân x_1 x_2 ... x_n với a_1 x_1 + a_2 x_2 + ... + a_n x_n <= b
    1. Mỗi đồ vật chỉ có hai khả năng: lấy (x_i = 1) hoặc không lấy (x_i = 0), nên một cách chọn là một xâu nhị phân độ dài n.
    2. Cách chọn chỉ chấp nhận được khi tổng khối lượng các đồ vật đã lấy không vượt sức chứa: a_1 x_1 + ... + a_n x_n <= b.
    3. Thứ tự bỏ đồ vật vào túi không quan trọng, nên phương án không phải là một hoán vị.
- `tr_t4_pb_02` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi bài toán tối ưu tổ hợp với tập phương án của nó.
  - **Đáp án (ghép đúng):**
    - Bài toán cái túi với n đồ vật — các xâu nhị phân độ dài n có tổng khối lượng không vượt sức chứa
    - Người du lịch qua n thành phố, xuất phát và trở về thành phố 1 — các hoán vị của n - 1 thành phố 2, 3, ..., n
    - Phân n việc cho n người, mỗi người đúng một việc — các hoán vị của n việc
    - Chọn đúng k trong n dự án để đầu tư — các tập con k phần tử của tập n dự án
  - **Lời giải:**
    1. Cái túi: mỗi đồ vật lấy hoặc không, cộng thêm ràng buộc khối lượng.
    2. Người du lịch: thành phố 1 đã cố định ở đầu và cuối, chỉ còn chọn thứ tự đi qua n - 1 thành phố kia.
    3. Phân việc: người i nhận việc j_i, các j_i đôi một khác nhau, nên (j_1, ..., j_n) là một hoán vị.
    4. Chọn k dự án không kể thứ tự: một tập con k phần tử.
- `tr_t4_pb_03` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong bài toán người du lịch, hàm mục tiêu của một hành trình là tổng độ dài các đoạn đường của nó, kể cả đoạn trở về thành phố xuất phát.
  - **Đáp án:** Đúng
    1. Hành trình 1, j_2, ..., j_n đi lần lượt qua các thành phố rồi quay về 1.
    2. Độ dài của nó là d(1, j_2) + d(j_2, j_3) + ... + d(j_n, 1).
    3. Bỏ quên đoạn cuối d(j_n, 1) là tính sai hàm mục tiêu.
- `tr_t4_pb_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán cái túi có 4 đồ vật với khối lượng (3, 4, 5, 2), giá trị (4, 5, 7, 3), sức chứa 9. Trong bốn phương án x = (x_1, x_2, x_3, x_4) sau, phương án nào chấp nhận được và có giá trị lớn nhất?
    - **(đúng)** (0, 1, 1, 0)
    - (1, 0, 1, 0)
    - (0, 0, 1, 1)
    - (1, 0, 1, 1)
  - **Đáp án:** (0, 1, 1, 0)
    1. Tính khối lượng và giá trị từng phương án.
    2. (0, 1, 1, 0): nặng 4 + 5 = 9, giá trị 5 + 7 = 12. (1, 0, 1, 0): nặng 8, giá trị 11. (0, 0, 1, 1): nặng 7, giá trị 10.
    3. (1, 0, 1, 1): nặng 3 + 5 + 2 = 10 > 9, không chấp nhận được dù giá trị 14 lớn nhất.
    4. Trong các phương án chấp nhận được, (0, 1, 1, 0) có giá trị lớn nhất là 12.
- `tr_t4_pb_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: phát biểu bài toán phân n việc cho n đệ tử (mỗi người làm đúng một việc, mỗi việc do đúng một người làm, c_ij là chi phí khi người i làm việc j) và đếm số phương án.
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm mục tiêu là tổng chi phí, cần làm cho nhỏ nhất.
    2. Một phương án là một cách gán cho mỗi người một việc, hai người có thể nhận cùng một việc.   **<- bước sai đầu tiên**
    3. Mỗi người có n việc để chọn, nên có n^n phương án.
    4. Phương án (j_1, ..., j_n) có chi phí c_1j_1 + c_2j_2 + ... + c_nj_n.
  - **Đáp án:** Bước 2: Một phương án là một cách gán cho mỗi người một việc, hai người có thể nhận cùng một việc.
  - **Vì sao sai, và bước đúng:**
    1. Đề bài đòi mỗi việc do đúng một người làm, nên hai người không được nhận cùng một việc.
    2. Một phương án là một song ánh từ tập người sang tập việc, tức là một hoán vị (j_1, ..., j_n) của 1, 2, ..., n.
    3. Vì vậy có n! phương án chứ không phải n^n.
- `tr_g4_phan_viec` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ba đệ tử nhận ba việc, mỗi người đúng một việc, mỗi việc đúng một người. Phần tử hàng i cột j của ma trận C là chi phí khi đệ tử i làm việc j. Tìm cách phân việc có tổng chi phí nhỏ nhất. Tổng chi phí nhỏ nhất là bao nhiêu?
  - C = (3, 2, 5); (2, 8, 8); (8, 7, 4)  (từng hàng)
  - **Đáp án:** 8
    1. Tập phương án là các hoán vị (j_1, j_2, j_3) của 1, 2, 3: đệ tử i làm việc j_i. Hàm mục tiêu là C(1, j_1) + C(2, j_2) + C(3, j_3).
    2. Xét cả 3! = 6 hoán vị: việc (1, 2, 3): 3 + 8 + 4 = 15; việc (1, 3, 2): 3 + 8 + 7 = 18; việc (2, 1, 3): 2 + 2 + 4 = 8; việc (2, 3, 1): 2 + 8 + 8 = 18; việc (3, 1, 2): 5 + 2 + 7 = 14; việc (3, 2, 1): 5 + 8 + 8 = 21.
    3. Giá trị nhỏ nhất là 8.
  - **Câu hỏi:** Ba đệ tử nhận ba việc, mỗi người đúng một việc, mỗi việc đúng một người. Phần tử hàng i cột j của ma trận C là chi phí khi đệ tử i làm việc j. Tìm cách phân việc có tổng chi phí nhỏ nhất. Tổng chi phí nhỏ nhất là bao nhiêu?
  - C = (1, 2, 2); (6, 3, 5); (5, 4, 1)  (từng hàng)
  - **Đáp án:** 5
    1. Tập phương án là các hoán vị (j_1, j_2, j_3) của 1, 2, 3: đệ tử i làm việc j_i. Hàm mục tiêu là C(1, j_1) + C(2, j_2) + C(3, j_3).
    2. Xét cả 3! = 6 hoán vị: việc (1, 2, 3): 1 + 3 + 1 = 5; việc (1, 3, 2): 1 + 5 + 4 = 10; việc (2, 1, 3): 2 + 6 + 1 = 9; việc (2, 3, 1): 2 + 5 + 5 = 12; việc (3, 1, 2): 2 + 6 + 4 = 12; việc (3, 2, 1): 2 + 3 + 5 = 10.
    3. Giá trị nhỏ nhất là 5.
  - **Câu hỏi:** Ba đệ tử nhận ba việc, mỗi người đúng một việc, mỗi việc đúng một người. Phần tử hàng i cột j của ma trận C là chi phí khi đệ tử i làm việc j. Tìm cách phân việc có tổng chi phí nhỏ nhất. Tổng chi phí nhỏ nhất là bao nhiêu?
  - C = (4, 9, 3); (6, 8, 2); (1, 8, 5)  (từng hàng)
  - **Đáp án:** 12
    1. Tập phương án là các hoán vị (j_1, j_2, j_3) của 1, 2, 3: đệ tử i làm việc j_i. Hàm mục tiêu là C(1, j_1) + C(2, j_2) + C(3, j_3).
    2. Xét cả 3! = 6 hoán vị: việc (1, 2, 3): 4 + 8 + 5 = 17; việc (1, 3, 2): 4 + 2 + 8 = 14; việc (2, 1, 3): 9 + 6 + 5 = 20; việc (2, 3, 1): 9 + 2 + 1 = 12; việc (3, 1, 2): 3 + 6 + 8 = 17; việc (3, 2, 1): 3 + 8 + 1 = 12.
    3. Giá trị nhỏ nhất là 12.

### Duyệt toàn bộ (`tr_t4_duyet_toan_bo`)

- `tr_t4_dt_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Túi chịu được khối lượng tối đa 6. Có ba đồ vật nặng 2, 3 và 4. Có bao nhiêu cách chọn một tập đồ vật (kể cả không lấy gì) có tổng khối lượng không vượt quá 6?
  - **Đáp án:** 6
    1. Duyệt toàn bộ 2^3 = 8 tập con và tính khối lượng.
    2. Không lấy gì: 0; {2}: 2; {3}: 3; {4}: 4; {2, 3}: 5; {2, 4}: 6 đều được.
    3. {3, 4}: 7 và {2, 3, 4}: 9 vượt sức chứa.
    4. Có 6 tập chấp nhận được.
- `tr_t4_dt_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu một bài toán tối ưu tổ hợp có hữu hạn phương án và có ít nhất một phương án chấp nhận được, thì duyệt toàn bộ luôn tìm được một phương án tối ưu.
  - **Đáp án:** Đúng
    1. Duyệt toàn bộ tính hàm mục tiêu tại từng phương án chấp nhận được và giữ lại phương án tốt nhất.
    2. Tập phương án hữu hạn nên việc duyệt kết thúc, và không phương án nào bị bỏ sót.
    3. Vì vậy phương án được giữ lại là tối ưu. Điều duyệt toàn bộ không bảo đảm là thời gian: số phương án có thể rất lớn.
- `tr_t4_dt_06` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Duyệt toàn bộ bài toán phân 8 việc cho 8 người (mỗi người đúng một việc, mỗi việc đúng một người) phải xét bao nhiêu phương án?
    - **(đúng)** 40320
    - 16777216
    - 256
    - 64
  - **Đáp án:** 40320
    1. Mỗi phương án là một hoán vị của 8 việc.
    2. Số hoán vị là 8! = 40320.
    3. 16777216 = 8^8 là số cách khi hai người được nhận cùng một việc; 256 = 2^8 là số tập con, không phải số cách phân việc.
- `tr_g4_so_phuong_an` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Duyệt toàn bộ bài toán cái túi với 6 đồ vật: mỗi phương án là một xâu nhị phân x_1 x_2 ... x_6 (x_i = 1 khi lấy đồ vật i). Có tất cả bao nhiêu xâu phải xét, chưa kể ràng buộc khối lượng?
  - **Đáp án:** 64
    1. Mỗi đồ vật có 2 khả năng: lấy hoặc không lấy.
    2. Theo quy tắc nhân có 2^6 = 64 xâu nhị phân độ dài 6.
  - **Câu hỏi:** Duyệt toàn bộ bài toán cái túi với 6 đồ vật: mỗi phương án là một xâu nhị phân x_1 x_2 ... x_6 (x_i = 1 khi lấy đồ vật i). Có tất cả bao nhiêu xâu phải xét, chưa kể ràng buộc khối lượng?
  - **Đáp án:** 64
    1. Mỗi đồ vật có 2 khả năng: lấy hoặc không lấy.
    2. Theo quy tắc nhân có 2^6 = 64 xâu nhị phân độ dài 6.
  - **Câu hỏi:** Duyệt toàn bộ bài toán cái túi với 7 đồ vật: mỗi phương án là một xâu nhị phân x_1 x_2 ... x_7 (x_i = 1 khi lấy đồ vật i). Có tất cả bao nhiêu xâu phải xét, chưa kể ràng buộc khối lượng?
  - **Đáp án:** 128
    1. Mỗi đồ vật có 2 khả năng: lấy hoặc không lấy.
    2. Theo quy tắc nhân có 2^7 = 128 xâu nhị phân độ dài 7.
- `tr_t4_dt_03` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước giải bài toán người du lịch qua n thành phố bằng duyệt toàn bộ.
  - **Đáp án (thứ tự đúng):**
    1. Cố định thành phố xuất phát là thành phố 1 và đặt kỷ lục bằng một số rất lớn.
    2. Sinh lần lượt từng hoán vị của các thành phố 2, 3, ..., n bằng phương pháp sinh hoặc quay lui.
    3. Với mỗi hoán vị, tính độ dài hành trình kể cả đoạn trở về thành phố 1.
    4. Nếu độ dài đó nhỏ hơn kỷ lục thì gán kỷ lục bằng nó và ghi lại hành trình.
    5. Khi đã sinh hết các hoán vị, hành trình được ghi lại là hành trình ngắn nhất.
  - **Lời giải:**
    1. Trước hết phải có tập phương án và một kỷ lục ban đầu.
    2. Sau đó đi qua từng phương án, tính hàm mục tiêu và so với kỷ lục.
    3. Chỉ khi đã xét hết mọi phương án mới kết luận được.
- `tr_t4_dt_04` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bốn thành phố có khoảng cách d(1, 2) = 5, d(1, 3) = 9, d(1, 4) = 4, d(2, 3) = 3, d(2, 4) = 8, d(3, 4) = 6. Ghép mỗi hành trình với độ dài của nó.
  - **Đáp án (ghép đúng):**
    - 1 - 2 - 3 - 4 - 1 — 18
    - 1 - 2 - 4 - 3 - 1 — 28
    - 1 - 3 - 2 - 4 - 1 — 24
  - **Lời giải:**
    1. 1 - 2 - 3 - 4 - 1: 5 + 3 + 6 + 4 = 18.
    2. 1 - 2 - 4 - 3 - 1: 5 + 8 + 6 + 9 = 28.
    3. 1 - 3 - 2 - 4 - 1: 9 + 3 + 8 + 4 = 24.
    4. Ba hành trình này cùng ba hành trình ngược chiều là đủ cả 3! = 6 hoán vị, nên hành trình ngắn nhất dài 18.
- `tr_t4_dt_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: một máy xét được 10^6 phương án mỗi giây; duyệt toàn bộ bài toán cái túi với 40 đồ vật mất khoảng bao lâu?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi đồ vật lấy hoặc không lấy: 2 khả năng.
    2. Có 40 đồ vật nên số phương án phải xét là 40^2 = 1600.   **<- bước sai đầu tiên**
    3. Máy xét 10^6 phương án mỗi giây nên xong trong chưa tới một giây.
    4. Vậy với 40 đồ vật, duyệt toàn bộ là đủ nhanh.
  - **Đáp án:** Bước 2: Có 40 đồ vật nên số phương án phải xét là 40^2 = 1600.
  - **Vì sao sai, và bước đúng:**
    1. Theo quy tắc nhân, 40 lựa chọn hai khả năng cho 2^40 phương án, không phải 40^2.
    2. 2^40 = 1099511627776, hơn 10^12; chia cho 10^6 được hơn 10^6 giây, tức gần 13 ngày.
    3. Đó là lý do cần nhánh cận hoặc các thuật toán khác thay cho duyệt toàn bộ.
- `tr_g4_cai_tui` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán cái túi: túi chịu được khối lượng tối đa 16; đồ vật 1 nặng 3, giá trị 15; đồ vật 2 nặng 6, giá trị 10; đồ vật 3 nặng 3, giá trị 10; đồ vật 4 nặng 9, giá trị 13. Mỗi đồ vật lấy hoặc không lấy. Chọn các đồ vật có tổng khối lượng không vượt quá sức chứa và tổng giá trị lớn nhất. Tổng giá trị lớn nhất đó là bao nhiêu?
  - **Đáp án:** 38
    1. Có 2^4 = 16 tập đồ vật; chỉ xét các tập có tổng khối lượng không quá 16.
    2. Một cách xét gọn: bỏ ngay các tập quá nặng, so giá trị các tập còn lại, giữ tập có giá trị lớn nhất.
    3. Một phương án tốt nhất là lấy các đồ vật {1, 3, 4}: khối lượng 15, giá trị 38.
    4. Không tập nào nặng không quá 16 có giá trị lớn hơn, nên đáp số là 38.
  - **Câu hỏi:** Bài toán cái túi: túi chịu được khối lượng tối đa 12; đồ vật 1 nặng 3, giá trị 14; đồ vật 2 nặng 3, giá trị 15; đồ vật 3 nặng 7, giá trị 13; đồ vật 4 nặng 4, giá trị 7. Mỗi đồ vật lấy hoặc không lấy. Chọn các đồ vật có tổng khối lượng không vượt quá sức chứa và tổng giá trị lớn nhất. Tổng giá trị lớn nhất đó là bao nhiêu?
  - **Đáp án:** 36
    1. Có 2^4 = 16 tập đồ vật; chỉ xét các tập có tổng khối lượng không quá 12.
    2. Một cách xét gọn: bỏ ngay các tập quá nặng, so giá trị các tập còn lại, giữ tập có giá trị lớn nhất.
    3. Một phương án tốt nhất là lấy các đồ vật {1, 2, 4}: khối lượng 10, giá trị 36.
    4. Không tập nào nặng không quá 12 có giá trị lớn hơn, nên đáp số là 36.
  - **Câu hỏi:** Bài toán cái túi: túi chịu được khối lượng tối đa 18; đồ vật 1 nặng 4, giá trị 12; đồ vật 2 nặng 7, giá trị 3; đồ vật 3 nặng 9, giá trị 10; đồ vật 4 nặng 3, giá trị 7. Mỗi đồ vật lấy hoặc không lấy. Chọn các đồ vật có tổng khối lượng không vượt quá sức chứa và tổng giá trị lớn nhất. Tổng giá trị lớn nhất đó là bao nhiêu?
  - **Đáp án:** 29
    1. Có 2^4 = 16 tập đồ vật; chỉ xét các tập có tổng khối lượng không quá 18.
    2. Một cách xét gọn: bỏ ngay các tập quá nặng, so giá trị các tập còn lại, giữ tập có giá trị lớn nhất.
    3. Một phương án tốt nhất là lấy các đồ vật {1, 3, 4}: khối lượng 16, giá trị 29.
    4. Không tập nào nặng không quá 18 có giá trị lớn hơn, nên đáp số là 29.
- `tr_g4_nguoi_du_lich` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bốn thành phố 1, 2, 3, 4 có khoảng cách hai chiều: d(1, 2) = 6; d(1, 3) = 20; d(1, 4) = 4; d(2, 3) = 10; d(2, 4) = 5; d(3, 4) = 17. Một người xuất phát từ thành phố 1, đi qua mỗi thành phố còn lại đúng một lần rồi trở về 1. Hành trình ngắn nhất dài bao nhiêu?
  - **Đáp án:** 37
    1. Cố định thành phố 1. Có 3! = 6 hoán vị của 2, 3, 4, nhưng mỗi hành trình và hành trình ngược chiều của nó dài bằng nhau, nên chỉ cần xét 3 hành trình.
    2. 1-2-3-4-1: 6 + 10 + 17 + 4 = 37; 1-2-4-3-1: 6 + 5 + 17 + 20 = 48; 1-3-2-4-1: 20 + 10 + 5 + 4 = 39.
    3. Hành trình ngắn nhất dài 37.
  - **Câu hỏi:** Bốn thành phố 1, 2, 3, 4 có khoảng cách hai chiều: d(1, 2) = 3; d(1, 3) = 4; d(1, 4) = 4; d(2, 3) = 13; d(2, 4) = 7; d(3, 4) = 11. Một người xuất phát từ thành phố 1, đi qua mỗi thành phố còn lại đúng một lần rồi trở về 1. Hành trình ngắn nhất dài bao nhiêu?
  - **Đáp án:** 25
    1. Cố định thành phố 1. Có 3! = 6 hoán vị của 2, 3, 4, nhưng mỗi hành trình và hành trình ngược chiều của nó dài bằng nhau, nên chỉ cần xét 3 hành trình.
    2. 1-2-3-4-1: 3 + 13 + 11 + 4 = 31; 1-2-4-3-1: 3 + 7 + 11 + 4 = 25; 1-3-2-4-1: 4 + 13 + 7 + 4 = 28.
    3. Hành trình ngắn nhất dài 25.
  - **Câu hỏi:** Bốn thành phố 1, 2, 3, 4 có khoảng cách hai chiều: d(1, 2) = 9; d(1, 3) = 20; d(1, 4) = 19; d(2, 3) = 6; d(2, 4) = 13; d(3, 4) = 17. Một người xuất phát từ thành phố 1, đi qua mỗi thành phố còn lại đúng một lần rồi trở về 1. Hành trình ngắn nhất dài bao nhiêu?
  - **Đáp án:** 51
    1. Cố định thành phố 1. Có 3! = 6 hoán vị của 2, 3, 4, nhưng mỗi hành trình và hành trình ngược chiều của nó dài bằng nhau, nên chỉ cần xét 3 hành trình.
    2. 1-2-3-4-1: 9 + 6 + 17 + 19 = 51; 1-2-4-3-1: 9 + 13 + 17 + 20 = 59; 1-3-2-4-1: 20 + 6 + 13 + 19 = 58.
    3. Hành trình ngắn nhất dài 51.

### Thuật toán nhánh cận (`tr_t4_nhanh_can`)

- `tr_t4_nc_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi giải một bài toán tìm giá trị nhỏ nhất bằng nhánh cận, nếu cận dưới của một nhánh lớn hơn hoặc bằng kỷ lục hiện có thì bỏ nhánh đó đi cũng không làm mất giá trị tối ưu.
  - **Đáp án:** Đúng
    1. Cận dưới g của nhánh nghĩa là mọi phương án trong nhánh có giá trị ít nhất là g.
    2. Nếu g >= kỷ lục thì không phương án nào trong nhánh nhỏ hơn kỷ lục.
    3. Phương án ứng với kỷ lục đã được ghi lại, nên bỏ nhánh đi không làm mất giá trị tối ưu.
- `tr_t4_nc_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong thuật toán nhánh cận, kỷ lục là gì?
    - **(đúng)** Giá trị hàm mục tiêu của phương án tốt nhất đã tìm được cho đến lúc đó
    - Giá trị tối ưu của bài toán, biết trước khi chạy thuật toán
    - Số nhánh đã bị cắt
    - Cận của nhánh đang xét
  - **Đáp án:** Giá trị hàm mục tiêu của phương án tốt nhất đã tìm được cho đến lúc đó
    1. Kỷ lục được cập nhật mỗi khi tìm thấy một phương án đầy đủ tốt hơn.
    2. Nó dùng để so với cận của mỗi nhánh: nhánh nào chắc chắn không tốt hơn kỷ lục thì bị cắt.
    3. Giá trị tối ưu chỉ biết được khi thuật toán kết thúc: lúc đó kỷ lục chính là giá trị tối ưu.
- `tr_t4_nc_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận, sức chứa 10. Bốn đồ vật đã xếp theo tỉ số giá trị/khối lượng giảm dần: (khối lượng, giá trị) = (4, 12), (3, 6), (5, 9), (2, 3). Nhánh đang xét đã chọn x_1 = 1, x_2 = 0. Cận trên của nhánh bằng giá trị đã có cộng sức chứa còn lại nhân tỉ số c_3/a_3. Tính cận trên đó.
  - **Đáp án:** 114/5
    1. Đã lấy đồ vật 1: giá trị 12, khối lượng 4; sức chứa còn lại 10 - 4 = 6.
    2. Tỉ số của đồ vật 3 là 9/5, lớn nhất trong các đồ vật chưa quyết định.
    3. Cận trên: 12 + 6 . 9/5 = 12 + 54/5 = 114/5.
- `tr_t4_nc_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước của thuật toán nhánh cận cho một bài toán tìm giá trị nhỏ nhất.
  - **Đáp án (thứ tự đúng):**
    1. Đặt kỷ lục bằng giá trị của một phương án biết trước, hoặc bằng một số rất lớn.
    2. Mở rộng cấu hình bộ phận x_1, ..., x_k bằng một giá trị của thành phần x_(k + 1).
    3. Tính cận dưới g cho mọi phương án mở rộng từ cấu hình vừa có.
    4. Nếu g lớn hơn hoặc bằng kỷ lục thì cắt nhánh; ngược lại đi tiếp sang thành phần sau.
    5. Khi được một phương án đầy đủ có giá trị nhỏ hơn kỷ lục thì cập nhật kỷ lục.
  - **Lời giải:**
    1. Nhánh cận là quay lui có thêm một phép thử ở mỗi nút.
    2. Phải có kỷ lục trước thì mới so được cận với nó.
    3. Ở mỗi nút: mở rộng, tính cận, rồi cắt hoặc đi tiếp; kỷ lục giảm dần mỗi khi gặp phương án tốt hơn.
- `tr_t4_nc_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đến lúc này phương án tốt nhất đã tìm được có giá trị 20, nên kỷ lục là 20.
    2. Nhánh đang xét có cận trên 23: mọi phương án trong nhánh có giá trị không quá 23.
    3. Vì 23 >= 20 nên nhánh này không thể cho phương án tốt hơn kỷ lục: cắt nhánh.   **<- bước sai đầu tiên**
    4. Chuyển sang xét nhánh tiếp theo.
  - **Đáp án:** Bước 3: Vì 23 >= 20 nên nhánh này không thể cho phương án tốt hơn kỷ lục: cắt nhánh.
  - **Vì sao sai, và bước đúng:**
    1. Với bài toán tìm giá trị lớn nhất, nhánh chỉ bị cắt khi cận trên nhỏ hơn hoặc bằng kỷ lục.
    2. Cận trên 23 lớn hơn kỷ lục 20: trong nhánh có thể có phương án giá trị 21, 22 hoặc 23, tốt hơn kỷ lục.
    3. Phải xét tiếp nhánh này. Lỗi ở đây là dùng điều kiện cắt của bài toán tìm giá trị nhỏ nhất.
- `tr_g4_nhanh_can` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận. Sức chứa 22; đồ vật 1 nặng 8, giá trị 18; đồ vật 2 nặng 6, giá trị 11; đồ vật 3 nặng 3, giá trị 5; đồ vật 4 nặng 8, giá trị 6; các đồ vật đã xếp theo tỉ số giá trị/khối lượng giảm dần. Nhánh đang xét đã chọn x_1 = 1, x_2 = 1. Cận trên của nhánh là giá trị đã có cộng sức chứa còn lại nhân tỉ số c_3/a_3 = 5/3. Kỷ lục hiện có là 35. Khẳng định: nhánh này bị cắt.
  - **Đáp án:** Sai
    1. Giá trị đã có: 29; khối lượng đã dùng: 14; sức chứa còn lại: 22 - 14 = 8.
    2. Cận trên: 29 + 8 . 5/3 = 127/3.
    3. Cận trên 127/3 lớn hơn kỷ lục 35: nhánh có thể còn phương án tốt hơn, phải xét tiếp. Khẳng định sai.
  - **Câu hỏi:** Giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận. Sức chứa 8; đồ vật 1 nặng 2, giá trị 12; đồ vật 2 nặng 2, giá trị 8; đồ vật 3 nặng 8, giá trị 14; đồ vật 4 nặng 8, giá trị 5; các đồ vật đã xếp theo tỉ số giá trị/khối lượng giảm dần. Nhánh đang xét đã chọn x_1 = 0, x_2 = 0. Cận trên của nhánh là giá trị đã có cộng sức chứa còn lại nhân tỉ số c_3/a_3 = 14/8. Kỷ lục hiện có là 5. Khẳng định: nhánh này bị cắt.
  - **Đáp án:** Sai
    1. Giá trị đã có: 0; khối lượng đã dùng: 0; sức chứa còn lại: 8 - 0 = 8.
    2. Cận trên: 0 + 8 . 14/8 = 14.
    3. Cận trên 14 lớn hơn kỷ lục 5: nhánh có thể còn phương án tốt hơn, phải xét tiếp. Khẳng định sai.
  - **Câu hỏi:** Giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận. Sức chứa 15; đồ vật 1 nặng 3, giá trị 14; đồ vật 2 nặng 6, giá trị 18; đồ vật 3 nặng 3, giá trị 3; đồ vật 4 nặng 6, giá trị 5; các đồ vật đã xếp theo tỉ số giá trị/khối lượng giảm dần. Nhánh đang xét đã chọn x_1 = 1, x_2 = 0. Cận trên của nhánh là giá trị đã có cộng sức chứa còn lại nhân tỉ số c_3/a_3 = 3/3. Kỷ lục hiện có là 37. Khẳng định: nhánh này bị cắt.
  - **Đáp án:** Đúng
    1. Giá trị đã có: 14; khối lượng đã dùng: 3; sức chứa còn lại: 15 - 3 = 12.
    2. Cận trên: 14 + 12 . 3/3 = 26.
    3. Cận trên 26 không lớn hơn kỷ lục 37: nhánh không thể cho phương án tốt hơn, nên bị cắt. Khẳng định đúng.

### Thuật toán tham lam (`tr_t4_tham_lam`)

- `tr_t4_tl_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Túi chịu được khối lượng 7. Ba đồ vật có (khối lượng, giá trị) = (5, 10), (4, 7), (3, 5). Thuật toán tham lam xét các đồ vật theo tỉ số giá trị/khối lượng giảm dần và lấy đồ vật nào còn vừa túi. Tổng giá trị nó lấy được là bao nhiêu?
  - **Đáp án:** 10
    1. Tỉ số: 10/5 = 2, rồi 7/4, rồi 5/3 (2 > 7/4 > 5/3); thứ tự xét là đồ vật 1, 2, 3.
    2. Lấy đồ vật 1 (khối lượng 5), sức chứa còn 2.
    3. Đồ vật 2 nặng 4 và đồ vật 3 nặng 3 đều không vừa.
    4. Tham lam được giá trị 10. (Lấy đồ vật 2 và 3 được 12, tốt hơn: tham lam không tối ưu ở đây.)
- `tr_t4_tl_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thuật toán tham lam ở mỗi bước chọn lựa chọn tốt nhất trước mắt và không bao giờ quay lại sửa một lựa chọn đã làm.
  - **Đáp án:** Đúng
    1. Đó chính là đặc điểm của tham lam: quyết định một lần, theo một tiêu chí cục bộ.
    2. Vì không quay lui nên tham lam chạy rất nhanh.
    3. Cũng vì thế mà nó có thể bỏ lỡ phương án tối ưu; quay lui và nhánh cận thì quay lại thử các lựa chọn khác.
- `tr_g4_lich` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một phòng luyện công chỉ dùng được cho một buổi tại mỗi lúc. Có 5 buổi xin dùng phòng, buổi [s, f] bắt đầu lúc s giờ và kết thúc lúc f giờ: [3, 4], [4, 5], [7, 8], [7, 11], [9, 10]. Hai buổi xếp được cùng nhau khi buổi này kết thúc không muộn hơn lúc buổi kia bắt đầu. Xếp được nhiều nhất bao nhiêu buổi?
  - **Đáp án:** 4
    1. Tham lam đúng cho bài này: mỗi bước chọn buổi kết thúc sớm nhất trong các buổi còn xếp được.
    2. Các buổi được chọn lần lượt: [3, 4], [4, 5], [7, 8], [9, 10].
    3. Xếp được nhiều nhất 4 buổi. (Chọn buổi kết thúc sớm nhất để lại nhiều thời gian nhất cho các buổi sau, nên không phương án nào xếp được nhiều hơn.)
  - **Câu hỏi:** Một phòng luyện công chỉ dùng được cho một buổi tại mỗi lúc. Có 5 buổi xin dùng phòng, buổi [s, f] bắt đầu lúc s giờ và kết thúc lúc f giờ: [1, 2], [4, 6], [5, 7], [9, 10], [10, 13]. Hai buổi xếp được cùng nhau khi buổi này kết thúc không muộn hơn lúc buổi kia bắt đầu. Xếp được nhiều nhất bao nhiêu buổi?
  - **Đáp án:** 4
    1. Tham lam đúng cho bài này: mỗi bước chọn buổi kết thúc sớm nhất trong các buổi còn xếp được.
    2. Các buổi được chọn lần lượt: [1, 2], [4, 6], [9, 10], [10, 13].
    3. Xếp được nhiều nhất 4 buổi. (Chọn buổi kết thúc sớm nhất để lại nhiều thời gian nhất cho các buổi sau, nên không phương án nào xếp được nhiều hơn.)
  - **Câu hỏi:** Một phòng luyện công chỉ dùng được cho một buổi tại mỗi lúc. Có 5 buổi xin dùng phòng, buổi [s, f] bắt đầu lúc s giờ và kết thúc lúc f giờ: [5, 9], [7, 10], [9, 10], [9, 11], [10, 11]. Hai buổi xếp được cùng nhau khi buổi này kết thúc không muộn hơn lúc buổi kia bắt đầu. Xếp được nhiều nhất bao nhiêu buổi?
  - **Đáp án:** 3
    1. Tham lam đúng cho bài này: mỗi bước chọn buổi kết thúc sớm nhất trong các buổi còn xếp được.
    2. Các buổi được chọn lần lượt: [5, 9], [9, 10], [10, 11].
    3. Xếp được nhiều nhất 3 buổi. (Chọn buổi kết thúc sớm nhất để lại nhiều thời gian nhất cho các buổi sau, nên không phương án nào xếp được nhiều hơn.)
- `tr_t4_tl_02` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: có đủ nhiều đồng linh thạch mệnh giá 1, 3 và 4; trả đúng 6 với số đồng ít nhất.
  - **Lời giải đưa ra (có một bước sai):**
    1. Tham lam: mỗi bước lấy đồng có mệnh giá lớn nhất không vượt số còn phải trả.
    2. Còn 6: lấy đồng 4, còn phải trả 2.
    3. Còn 2: lấy đồng 1 hai lần. Tham lam dùng 3 đồng.
    4. Tham lam luôn cho số đồng ít nhất, nên số đồng ít nhất là 3.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Tham lam luôn cho số đồng ít nhất, nên số đồng ít nhất là 3.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu chạy đúng thuật toán tham lam.
    2. Nhưng tham lam không phải lúc nào cũng tối ưu: 6 = 3 + 3 chỉ cần 2 đồng.
    3. Số đồng ít nhất là 2. Muốn tin một thuật toán tham lam phải chứng minh nó tối ưu, hoặc so với duyệt toàn bộ.
- `tr_t4_tl_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cần trả đúng 8 bằng các đồng xu, mỗi mệnh giá có đủ nhiều đồng. Thuật toán tham lam lấy đồng lớn nhất không vượt số còn phải trả. Với hệ mệnh giá nào sau đây tham lam KHÔNG cho số đồng ít nhất khi trả 8?
    - **(đúng)** {1, 4, 6}
    - {1, 2, 4}
    - {1, 5, 10}
    - {1, 2, 5}
  - **Đáp án:** {1, 4, 6}
    1. {1, 4, 6}: tham lam trả 6 + 1 + 1 (3 đồng) nhưng 4 + 4 chỉ cần 2 đồng.
    2. {1, 2, 4}: 4 + 4, 2 đồng, tối ưu. {1, 5, 10}: 5 + 1 + 1 + 1, 4 đồng, không có cách nào ít hơn.
    3. {1, 2, 5}: 5 + 2 + 1, 3 đồng, cũng là ít nhất.
    4. Vậy chỉ hệ {1, 4, 6} làm tham lam sai.
- `tr_g4_tham_lam_xu` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có đủ nhiều đồng linh thạch mệnh giá 1, 2 và 7. Cần trả đúng 11. Thuật toán tham lam: mỗi bước lấy đồng có mệnh giá lớn nhất không vượt quá số còn phải trả. Khẳng định: với số tiền 11, thuật toán tham lam dùng ít đồng nhất có thể.
  - **Đáp án:** Đúng
    1. Tham lam trả 11 = 7 + 2 + 2: dùng 3 đồng.
    2. Số đồng ít nhất có thể (xét mọi cách trả) là 3.
    3. Hai số bằng nhau: khẳng định đúng.
  - **Câu hỏi:** Có đủ nhiều đồng linh thạch mệnh giá 1, 3 và 4. Cần trả đúng 10. Thuật toán tham lam: mỗi bước lấy đồng có mệnh giá lớn nhất không vượt quá số còn phải trả. Khẳng định: với số tiền 10, thuật toán tham lam dùng ít đồng nhất có thể.
  - **Đáp án:** Sai
    1. Tham lam trả 10 = 4 + 4 + 1 + 1: dùng 4 đồng.
    2. Số đồng ít nhất có thể (xét mọi cách trả) là 3.
    3. 4 > 3: tham lam không tối ưu ở đây, khẳng định sai.
  - **Câu hỏi:** Có đủ nhiều đồng linh thạch mệnh giá 1, 2 và 12. Cần trả đúng 13. Thuật toán tham lam: mỗi bước lấy đồng có mệnh giá lớn nhất không vượt quá số còn phải trả. Khẳng định: với số tiền 13, thuật toán tham lam dùng ít đồng nhất có thể.
  - **Đáp án:** Đúng
    1. Tham lam trả 13 = 12 + 1: dùng 2 đồng.
    2. Số đồng ít nhất có thể (xét mọi cách trả) là 2.
    3. Hai số bằng nhau: khẳng định đúng.

### Ký hiệu O lớn (`tr_t4_ky_hieu_o`)

- `tr_t4_o_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho T(n) = 3n^2 + 5n + 100. Trong các hàm g sau, với hàm nào ta có T(n) = O(g(n))?
    - **(đúng)** g(n) = n^2
    - g(n) = n
    - g(n) = log n
    - g(n) = 1
  - **Đáp án:** g(n) = n^2
    1. Với n >= 1: 5n <= 5n^2 và 100 <= 100n^2, nên T(n) <= 108n^2. Vậy T(n) = O(n^2).
    2. T(n)/n >= 3n tăng mãi, nên T(n) không là O(n); càng không là O(log n) hay O(1).
    3. Chỉ số hạng bậc cao nhất quyết định lớp O; hệ số 3 và các số hạng nhỏ hơn bị bỏ.
- `tr_t4_o_02` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi đoạn chương trình (với dữ liệu kích thước n) với số phép toán của nó theo ký hiệu O.
  - **Đáp án (ghép đúng):**
    - Một vòng for i = 1 to n — O(n)
    - Hai vòng for lồng nhau, mỗi vòng chạy từ 1 đến n — O(n^2)
    - Vòng while bắt đầu với j = 1, mỗi lượt nhân đôi j, dừng khi j > n — O(log n)
    - Duyệt mọi tập con của một tập n phần tử — O(2^n)
  - **Lời giải:**
    1. Một vòng chạy n lần: O(n).
    2. Hai vòng lồng nhau: n . n = n^2 lượt.
    3. j = 1, 2, 4, ..., cần khoảng log_2 n lượt để vượt n: O(log n).
    4. Có 2^n tập con, mỗi tập xét ít nhất một lần: O(2^n).
- `tr_t4_o_07` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một thuật toán làm đúng T(n) = n^2 + n phép toán. Trong các đánh giá sau, đánh giá nào vừa đúng vừa chặt nhất (không thể thay bằng một lớp nhỏ hơn trong danh sách)?
    - **(đúng)** O(n^2)
    - O(n^3)
    - O(n)
    - O(n log n)
  - **Đáp án:** O(n^2)
    1. n^2 + n <= 2n^2 với n >= 1, nên T(n) = O(n^2).
    2. T(n) = O(n^3) cũng đúng, nhưng lỏng: viết O(n^3) cho chắc là đánh giá thừa, làm thuật toán có vẻ chậm hơn thật.
    3. T(n) không là O(n) hay O(n log n), vì T(n)/(n log n) >= n/log n tăng mãi.
    4. Vậy đánh giá chặt nhất là O(n^2).
- `tr_g4_dem_vong_lap` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đoạn chương trình sau chạy với n = 7: for i = 1 to n: for j = i to n: x = x + 1. Lệnh x = x + 1 được thực hiện bao nhiêu lần?
  - **Đáp án:** 28
    1. Đếm theo công thức: n + (n - 1) + ... + 1 = n(n + 1)/2.
    2. Với n = 7: lệnh x = x + 1 chạy 28 lần.
  - **Câu hỏi:** Đoạn chương trình sau chạy với n = 7: for i = 1 to n: for j = 1 to n: x = x + 1. Lệnh x = x + 1 được thực hiện bao nhiêu lần?
  - **Đáp án:** 49
    1. Đếm theo công thức: n . n = n^2.
    2. Với n = 7: lệnh x = x + 1 chạy 49 lần.
  - **Câu hỏi:** Đoạn chương trình sau chạy với n = 9: for i = 1 to n: for j = i to n: x = x + 1. Lệnh x = x + 1 được thực hiện bao nhiêu lần?
  - **Đáp án:** 45
    1. Đếm theo công thức: n + (n - 1) + ... + 1 = n(n + 1)/2.
    2. Với n = 9: lệnh x = x + 1 chạy 45 lần.
- `tr_t4_o_03` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đánh giá 3n^2 + 5n và 4^n bằng ký hiệu O.
  - **Lời giải đưa ra (có một bước sai):**
    1. f(n) = O(g(n)) nghĩa là có hằng số C > 0 và n_0 để f(n) <= C . g(n) với mọi n >= n_0.
    2. Với n >= 1 ta có 5n <= 5n^2, nên 3n^2 + 5n <= 8n^2.
    3. Vậy 3n^2 + 5n = O(n^2), với C = 8 và n_0 = 1.
    4. Tương tự, 4^n = 2^(2n); hằng số 2 trong số mũ bỏ đi được như một hằng số nhân, nên 4^n = O(2^n).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Tương tự, 4^n = 2^(2n); hằng số 2 trong số mũ bỏ đi được như một hằng số nhân, nên 4^n = O(2^n).
  - **Vì sao sai, và bước đúng:**
    1. Chỉ hằng số nhân phía trước mới bỏ được; hằng số trong số mũ thì không.
    2. 4^n/2^n = 2^n tăng mãi, nên không có hằng số C nào để 4^n <= C . 2^n với mọi n lớn.
    3. Vậy 4^n không là O(2^n); đánh giá đúng là 4^n = O(4^n).
- `tr_t4_o_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đoạn chương trình: j = 1; while j <= 100: (j = 2j; dem = dem + 1). Lệnh dem = dem + 1 được thực hiện bao nhiêu lần?
  - **Đáp án:** 7
    1. Vòng lặp chạy khi j lần lượt là 1, 2, 4, 8, 16, 32, 64: đều không vượt 100.
    2. Sau lượt j = 64, j thành 128 > 100 và vòng dừng.
    3. Có 7 lượt. Tổng quát, số lượt là phần nguyên của log_2 n cộng 1, tức O(log n).
- `tr_t4_o_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: so sánh độ phức tạp của hai thuật toán A và B theo ký hiệu O.
  - **Lời giải đưa ra (có một bước sai):**
    1. Thuật toán A làm 2n phép so sánh và 2n phép gán, tổng cộng 4n phép toán.
    2. Thuật toán B làm n phép so sánh và n phép gán, tổng cộng 2n phép toán.
    3. Vì vậy A có độ phức tạp O(4n), B có độ phức tạp O(2n), và lớp O(4n) lớn gấp đôi lớp O(2n).   **<- bước sai đầu tiên**
    4. Kết luận: theo ký hiệu O, A thuộc một lớp chậm hơn B.
  - **Đáp án:** Bước 3: Vì vậy A có độ phức tạp O(4n), B có độ phức tạp O(2n), và lớp O(4n) lớn gấp đôi lớp O(2n).
  - **Vì sao sai, và bước đúng:**
    1. Ký hiệu O bỏ qua hằng số nhân: 4n <= 4 . n và 2n <= 2 . n, nên cả hai đều là O(n).
    2. O(4n), O(2n) và O(n) là cùng một lớp hàm, không có lớp nào lớn gấp đôi lớp nào.
    3. A và B cùng độ phức tạp O(n). A làm nhiều phép toán gấp đôi, nhưng sự khác biệt hằng số đó không thấy được qua ký hiệu O.
- `tr_t4_o_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** n! = O(2^n).
  - **Đáp án:** Sai
    1. n!/2^n = (1/2)(2/2)(3/2)...(n/2) >= (1/2) . (3/2)^(n - 2) với n >= 2.
    2. Biểu thức đó tăng mãi theo n, nên không có hằng số C nào để n! <= C . 2^n với mọi n lớn.
    3. Vậy n! tăng nhanh hơn hẳn 2^n: khẳng định sai.
- `tr_g4_o_lon` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(n) = 3n + 33. Khẳng định: f(n) = O(n^4).
  - **Đáp án:** Đúng
    1. Số hạng tăng nhanh nhất của f(n) = 3n + 33 là 3n; khi n >= 1 thì f(n) <= 36n.
    2. Vì 1 <= 4 nên n <= n^4 với n >= 1, do đó f(n) <= 36n^4: f(n) = O(n^4). Khẳng định đúng.
  - **Câu hỏi:** Cho f(n) = 7n + 12. Khẳng định: f(n) = O(n^3).
  - **Đáp án:** Đúng
    1. Số hạng tăng nhanh nhất của f(n) = 7n + 12 là 7n; khi n >= 1 thì f(n) <= 19n.
    2. Vì 1 <= 3 nên n <= n^3 với n >= 1, do đó f(n) <= 19n^3: f(n) = O(n^3). Khẳng định đúng.
  - **Câu hỏi:** Cho f(n) = 9n^2 + 42n. Khẳng định: f(n) = O(n).
  - **Đáp án:** Sai
    1. Số hạng tăng nhanh nhất của f(n) = 9n^2 + 42n là 9n^2; khi n >= 1 thì f(n) <= 51n^2.
    2. f(n)/n >= 9n tăng mãi, không bị chặn bởi hằng số nào: f(n) không là O(n). Khẳng định sai.

## Tầng 5: Đồ thị: khái niệm cơ bản và biểu diễn trên máy tính

36 dạng câu (27 câu viết tay, 9 bộ sinh câu); 36 chưa duyệt.

### Đỉnh, cạnh và các loại đồ thị (`tr_t5_khai_niem`)

- `tr_t5_kn_01` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi mô tả với loại đồ thị của nó.
  - **Đáp án (ghép đúng):**
    - Mỗi cạnh có một chiều, đi từ đỉnh đầu đến đỉnh cuối — đồ thị có hướng
    - Giữa hai đỉnh có thể có nhiều cạnh cùng nối chúng — đa đồ thị
    - Đồ thị đơn, mọi cặp đỉnh khác nhau đều kề nhau — đồ thị đầy đủ
    - Tập đỉnh chia được thành hai phần, mỗi cạnh nối hai đỉnh ở hai phần khác nhau — đồ thị hai phía
  - **Lời giải:**
    1. Cạnh có chiều gọi là cung; đồ thị có các cung là đồ thị có hướng.
    2. Đồ thị đơn không có cạnh bội; cho phép cạnh bội thì được đa đồ thị.
    3. Đồ thị đầy đủ n đỉnh K_n có đủ C_n^2 cạnh.
    4. Đồ thị hai phía không có cạnh nào nằm trong cùng một phần.
- `tr_t5_kn_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đầy đủ K_4 là một đồ thị hai phía.
  - **Đáp án:** Sai
    1. Trong đồ thị hai phía, ba đỉnh đôi một kề nhau không thể có: hai trong ba đỉnh phải cùng một phần.
    2. K_4 có tam giác, ví dụ các đỉnh 1, 2, 3.
    3. Vậy K_4 không là đồ thị hai phía.
- `tr_t5_kn_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị có hướng 5 đỉnh không có khuyên, và với mỗi cặp đỉnh có thứ tự (u, v), u khác v, có nhiều nhất một cung đi từ u đến v. Đồ thị có nhiều nhất bao nhiêu cung?
    - **(đúng)** 20
    - 10
    - 25
    - 32
  - **Đáp án:** 20
    1. Mỗi cung ứng với một cặp có thứ tự gồm hai đỉnh khác nhau.
    2. Số cặp như vậy là A_5^2 = 5 . 4 = 20.
    3. 10 = C_5^2 là số cạnh tối đa của đồ thị vô hướng; 25 tính cả khuyên.
- `tr_t5_kn_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đơn vô hướng G có 7 đỉnh và 12 cạnh. Đồ thị bù của G (cùng tập đỉnh, hai đỉnh kề nhau khi và chỉ khi chúng không kề nhau trong G) có bao nhiêu cạnh?
  - **Đáp án:** 9
    1. Mỗi cặp đỉnh là cạnh của đúng một trong hai đồ thị G và đồ thị bù.
    2. Số cặp đỉnh là C_7^2 = 21.
    3. Đồ thị bù có 21 - 12 = 9 cạnh.
- `tr_g5_day_du` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị hai phía đầy đủ K_(6, 2) có một phần 6 đỉnh, một phần 2 đỉnh, và mỗi đỉnh phần này kề mọi đỉnh phần kia (không có cạnh trong cùng một phần). Nó có bao nhiêu cạnh?
  - **Đáp án:** 12
    1. Mỗi cạnh nối một trong 6 đỉnh phần thứ nhất với một trong 2 đỉnh phần thứ hai.
    2. Theo quy tắc nhân có 6 . 2 = 12 cạnh.
  - **Câu hỏi:** Đồ thị đầy đủ K_5 (đồ thị đơn vô hướng 5 đỉnh, mọi cặp đỉnh khác nhau đều kề nhau) có bao nhiêu cạnh?
  - **Đáp án:** 10
    1. Mỗi cạnh ứng với một cặp hai đỉnh không kể thứ tự: C_5^2 cạnh.
    2. C_5^2 = 5 . 4/2 = 10.
  - **Câu hỏi:** Đồ thị hai phía đầy đủ K_(6, 6) có một phần 6 đỉnh, một phần 6 đỉnh, và mỗi đỉnh phần này kề mọi đỉnh phần kia (không có cạnh trong cùng một phần). Nó có bao nhiêu cạnh?
  - **Đáp án:** 36
    1. Mỗi cạnh nối một trong 6 đỉnh phần thứ nhất với một trong 6 đỉnh phần thứ hai.
    2. Theo quy tắc nhân có 6 . 6 = 36 cạnh.
- `tr_t5_kn_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có các đỉnh 1, 2, 3, 4, 5 và các cạnh 1-2, 2-3, 3-4, 4-5, 5-1; nó có là đồ thị hai phía không?
  - **Lời giải đưa ra (có một bước sai):**
    1. Tô đỉnh 1 màu xanh; đỉnh 2 kề 1 nên tô đỏ.
    2. Đỉnh 3 kề 2 nên tô xanh; đỉnh 4 kề 3 nên tô đỏ.
    3. Đỉnh 5 kề 4 (màu đỏ) nên tô xanh.
    4. Mọi cạnh đều nối hai đỉnh khác màu, nên đồ thị là đồ thị hai phía.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Mọi cạnh đều nối hai đỉnh khác màu, nên đồ thị là đồ thị hai phía.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước tô màu đầu đều đúng quy tắc.
    2. Nhưng cạnh 5-1 nối hai đỉnh cùng màu xanh, nên câu ở bước 4 sai.
    3. Đồ thị là một chu trình 5 đỉnh, độ dài lẻ, nên không thể tô hai màu: nó không là đồ thị hai phía.
- `tr_t5_kn_06` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số nguyên n >= 2, đồ thị đầy đủ K_n là đồ thị hai phía khi và chỉ khi n = 2.
  - **Đáp án:** Đúng
    1. K_2 (hai đỉnh, một cạnh) là hai phía: đặt mỗi đỉnh vào một phần.
    2. Với n >= 3, K_n chứa tam giác trên ba đỉnh bất kỳ, mà đồ thị hai phía không có chu trình độ dài lẻ.
    3. Vậy với n >= 2, K_n hai phía đúng khi n = 2.
- `tr_g5_hai_phia` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-3, 1-5, 2-4, 2-5, 2-6, 3-4, 3-6, 4-5, 4-6. Khẳng định: G là đồ thị hai phía.
  - **Đáp án:** Sai
    1. Đồ thị hai phía không thể có chu trình độ dài lẻ: đi quanh chu trình, màu phải đổi ở mỗi cạnh.
    2. Thử tô hai màu theo BFS thì gặp một cạnh có hai đầu cùng màu: G có chu trình độ dài lẻ (chu trình lẻ ngắn nhất của G có 3 đỉnh).
    3. Vậy G không là đồ thị hai phía: khẳng định sai.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 2-6, 3-5, 3-6. Khẳng định: G là đồ thị hai phía.
  - **Đáp án:** Đúng
    1. Tô màu dần theo BFS: một đỉnh màu A thì mọi đỉnh kề nó màu B, và ngược lại.
    2. Được hai phần {1, 4, 5, 6} và {2, 3}, mỗi cạnh nối hai phần khác nhau.
    3. Vậy G là đồ thị hai phía: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-5, 1-6, 2-3, 2-4, 3-5, 5-6. Khẳng định: G là đồ thị hai phía.
  - **Đáp án:** Sai
    1. Đồ thị hai phía không thể có chu trình độ dài lẻ: đi quanh chu trình, màu phải đổi ở mỗi cạnh.
    2. Thử tô hai màu theo BFS thì gặp một cạnh có hai đầu cùng màu: G có chu trình độ dài lẻ (chu trình lẻ ngắn nhất của G có 3 đỉnh).
    3. Vậy G không là đồ thị hai phía: khẳng định sai.

### Bậc của đỉnh và định lý bắt tay (`tr_t5_bac`)

- `tr_t5_b_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị đơn vô hướng có 10 đỉnh, đỉnh nào cũng có bậc 3. Đồ thị có bao nhiêu cạnh?
  - **Đáp án:** 15
    1. Định lý bắt tay: tổng các bậc bằng hai lần số cạnh.
    2. Tổng các bậc là 10 . 3 = 30.
    3. Số cạnh là 30/2 = 15.
- `tr_t5_b_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có một đồ thị vô hướng (được phép có cạnh bội) gồm 5 đỉnh, mỗi đỉnh có bậc 3.
  - **Đáp án:** Sai
    1. Mỗi cạnh góp 2 vào tổng các bậc, nên tổng các bậc của mọi đồ thị vô hướng luôn chẵn.
    2. Ở đây tổng các bậc là 5 . 3 = 15, một số lẻ.
    3. Vậy không có đồ thị nào như vậy, kể cả khi cho phép cạnh bội.
- `tr_t5_b_05` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy nào sau đây là dãy bậc của một đồ thị đơn vô hướng?
    - **(đúng)** 3, 3, 2, 2, 2
    - 4, 4, 4, 1, 1
    - 3, 3, 3, 1
    - 5, 2, 2, 2, 1
  - **Đáp án:** 3, 3, 2, 2, 2
    1. 5, 2, 2, 2, 1: đồ thị đơn 5 đỉnh có bậc lớn nhất 4, không thể có bậc 5.
    2. 4, 4, 4, 1, 1: ba đỉnh bậc 4 đều kề mọi đỉnh khác, nên hai đỉnh còn lại có bậc ít nhất 3, mâu thuẫn. 3, 3, 3, 1: ba đỉnh bậc 3 đều kề đỉnh cuối, nên nó có bậc 3 chứ không phải 1.
    3. 3, 3, 2, 2, 2 dựng được: các đỉnh A, B bậc 3 và C, D, E bậc 2 với các cạnh A-B, A-C, A-D, B-C, B-E, D-E.
- `tr_g5_bat_tay` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị đơn vô hướng có 6 đỉnh; bậc của các đỉnh 1, 2, ..., 6 lần lượt là 3, 3, 3, 2, 4, 5. Đồ thị có bao nhiêu cạnh?
  - **Đáp án:** 10
    1. Định lý bắt tay: tổng các bậc bằng hai lần số cạnh, vì mỗi cạnh góp 1 vào bậc của mỗi đầu.
    2. Tổng các bậc: 3 + 3 + 3 + 2 + 4 + 5 = 20.
    3. Số cạnh: 20/2 = 10.
  - **Câu hỏi:** Một đồ thị đơn vô hướng có 6 đỉnh; bậc của các đỉnh 1, 2, ..., 6 lần lượt là 3, 1, 4, 1, 1, 2. Đồ thị có bao nhiêu cạnh?
  - **Đáp án:** 6
    1. Định lý bắt tay: tổng các bậc bằng hai lần số cạnh, vì mỗi cạnh góp 1 vào bậc của mỗi đầu.
    2. Tổng các bậc: 3 + 1 + 4 + 1 + 1 + 2 = 12.
    3. Số cạnh: 12/2 = 6.
  - **Câu hỏi:** Một đồ thị đơn vô hướng có 6 đỉnh; bậc của các đỉnh 1, 2, ..., 6 lần lượt là 4, 5, 4, 3, 2, 2. Đồ thị có bao nhiêu cạnh?
  - **Đáp án:** 10
    1. Định lý bắt tay: tổng các bậc bằng hai lần số cạnh, vì mỗi cạnh góp 1 vào bậc của mỗi đầu.
    2. Tổng các bậc: 4 + 5 + 4 + 3 + 2 + 2 = 20.
    3. Số cạnh: 20/2 = 10.
- `tr_t5_b_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: một nhóm 9 đệ tử, có thể nào mỗi người bắt tay đúng 3 người khác trong nhóm không?
  - **Lời giải đưa ra (có một bước sai):**
    1. Lập đồ thị: mỗi đỉnh là một đệ tử, mỗi cạnh là một cái bắt tay giữa hai người.
    2. Mỗi đỉnh có bậc 3.
    3. Số cạnh bằng tổng các bậc: 9 . 3 = 27 cái bắt tay.   **<- bước sai đầu tiên**
    4. Vậy có thể, với tất cả 27 cái bắt tay.
  - **Đáp án:** Bước 3: Số cạnh bằng tổng các bậc: 9 . 3 = 27 cái bắt tay.
  - **Vì sao sai, và bước đúng:**
    1. Mỗi cạnh được đếm ở cả hai đầu, nên tổng các bậc bằng hai lần số cạnh: số cạnh là 27/2.
    2. 27/2 không phải số nguyên; nói cách khác, số đỉnh bậc lẻ (ở đây là 9) phải là số chẵn.
    3. Vậy không thể có cách bắt tay như vậy.
- `tr_t5_b_04` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong mọi đồ thị đơn vô hướng có ít nhất 2 đỉnh, luôn có hai đỉnh cùng bậc.
  - **Đáp án:** Đúng
    1. Với n đỉnh, mỗi bậc là một trong n giá trị 0, 1, ..., n - 1.
    2. Bậc 0 và bậc n - 1 không cùng có mặt: một đỉnh kề mọi đỉnh khác thì không đỉnh nào có bậc 0.
    3. Vậy n đỉnh nhận nhiều nhất n - 1 giá trị, và theo nguyên lý Dirichlet có hai đỉnh cùng bậc.
- `tr_t5_b_06` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đơn vô hướng G có 7 đỉnh và 9 cạnh. Bậc của sáu đỉnh là 4, 3, 3, 2, 2, 2; bậc của đỉnh thứ bảy là x.
  - **Phần a** (Điền số): a) Tổng các bậc của G bằng bao nhiêu?
    - **Đáp án a:** 18
  - **Phần b** (Điền số): b) x bằng bao nhiêu?
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) G có đúng 2 đỉnh bậc lẻ.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Định lý bắt tay: tổng các bậc bằng 2 . 9 = 18.
    2. b) 4 + 3 + 3 + 2 + 2 + 2 = 16, nên x = 18 - 16 = 2.
    3. c) Các bậc là 4, 3, 3, 2, 2, 2, 2: chỉ hai đỉnh bậc 3 là bậc lẻ, đúng như số đỉnh bậc lẻ luôn chẵn. Dãy này dựng được, ví dụ các cạnh 1-2, 1-3, 1-4, 1-5, 2-3, 2-6, 3-7, 4-6, 5-7 với đỉnh 1 bậc 4.
- `tr_g5_day_bac` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Khẳng định: có một đồ thị đơn vô hướng 5 đỉnh mà bậc của các đỉnh là 3, 3, 2, 2, 2.
  - **Đáp án:** Đúng
    1. Tổng các bậc 12 là số chẵn, nên phải thử dựng (thuật toán Havel-Hakimi): nối đỉnh bậc lớn nhất với các đỉnh có bậc lớn nhất tiếp theo.
    2. Bỏ đỉnh bậc 3, trừ 1 ở 3 bậc lớn nhất còn lại: 2, 2, 1, 1.
    3. Bỏ đỉnh bậc 2, trừ 1 ở 2 bậc lớn nhất còn lại: 1, 1, 0.
    4. Bỏ đỉnh bậc 1, trừ 1 ở 1 bậc lớn nhất còn lại: 0, 0.
    5. Còn lại toàn số 0: dựng được.
    6. Khẳng định đúng.
  - **Câu hỏi:** Khẳng định: có một đồ thị đơn vô hướng 5 đỉnh mà bậc của các đỉnh là 2, 2, 2, 1, 1.
  - **Đáp án:** Đúng
    1. Tổng các bậc 8 là số chẵn, nên phải thử dựng (thuật toán Havel-Hakimi): nối đỉnh bậc lớn nhất với các đỉnh có bậc lớn nhất tiếp theo.
    2. Bỏ đỉnh bậc 2, trừ 1 ở 2 bậc lớn nhất còn lại: 1, 1, 1, 1.
    3. Bỏ đỉnh bậc 1, trừ 1 ở 1 bậc lớn nhất còn lại: 1, 1, 0.
    4. Bỏ đỉnh bậc 1, trừ 1 ở 1 bậc lớn nhất còn lại: 0, 0.
    5. Còn lại toàn số 0: dựng được.
    6. Khẳng định đúng.
  - **Câu hỏi:** Khẳng định: có một đồ thị đơn vô hướng 5 đỉnh mà bậc của các đỉnh là 3, 3, 2, 2, 2.
  - **Đáp án:** Đúng
    1. Tổng các bậc 12 là số chẵn, nên phải thử dựng (thuật toán Havel-Hakimi): nối đỉnh bậc lớn nhất với các đỉnh có bậc lớn nhất tiếp theo.
    2. Bỏ đỉnh bậc 3, trừ 1 ở 3 bậc lớn nhất còn lại: 2, 2, 1, 1.
    3. Bỏ đỉnh bậc 2, trừ 1 ở 2 bậc lớn nhất còn lại: 1, 1, 0.
    4. Bỏ đỉnh bậc 1, trừ 1 ở 1 bậc lớn nhất còn lại: 0, 0.
    5. Còn lại toàn số 0: dựng được.
    6. Khẳng định đúng.

### Đường đi, chu trình và liên thông (`tr_t5_duong_di_lien_thong`)

- `tr_t5_dd_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong một đồ thị vô hướng, nếu có một hành trình (dãy đỉnh liền nhau kề nhau, được lặp đỉnh) từ u đến v với u khác v, thì có một đường đi đơn (không lặp đỉnh) từ u đến v.
  - **Đáp án:** Đúng
    1. Nếu hành trình đi qua một đỉnh w hai lần, cắt bỏ đoạn giữa hai lần gặp w: vẫn được một hành trình từ u đến v, ngắn hơn.
    2. Lặp lại cho đến khi không còn đỉnh nào lặp: quá trình dừng vì hành trình ngắn dần.
    3. Kết quả là một đường đi đơn từ u đến v.
- `tr_t5_dd_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6 và các cạnh 1-2, 2-3, 3-4, 4-1, 3-5, 5-6. Khẳng định nào đúng?
    - **(đúng)** 1, 2, 3, 4, 1 là một chu trình của G
    - 1, 3, 5, 6 là một đường đi của G
    - 2, 3, 5, 3, 4 là một đường đi đơn của G
    - 5, 6, 5 là một chu trình của G
  - **Đáp án:** 1, 2, 3, 4, 1 là một chu trình của G
    1. 1-2, 2-3, 3-4, 4-1 đều là cạnh, các cạnh khác nhau và dãy quay về đỉnh đầu: đó là chu trình.
    2. 1-3 không phải là cạnh, nên 1, 3, 5, 6 không là đường đi.
    3. 2, 3, 5, 3, 4 đi qua đỉnh 3 hai lần nên không là đường đi đơn.
    4. 5, 6, 5 dùng một cạnh 5-6 hai lần, không là chu trình.
- `tr_t5_dd_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có các đỉnh 1, 2, ..., 7 và các cạnh 1-2, 2-3, 4-5, 5-6; đếm số thành phần liên thông.
  - **Lời giải đưa ra (có một bước sai):**
    1. Từ đỉnh 1 đi được tới 2 và 3: thành phần thứ nhất là {1, 2, 3}.
    2. Từ đỉnh 4 đi được tới 5 và 6: thành phần thứ hai là {4, 5, 6}.
    3. Đỉnh 7 không có cạnh nào nên không thuộc thành phần liên thông nào.   **<- bước sai đầu tiên**
    4. Vậy đồ thị có 2 thành phần liên thông.
  - **Đáp án:** Bước 3: Đỉnh 7 không có cạnh nào nên không thuộc thành phần liên thông nào.
  - **Vì sao sai, và bước đúng:**
    1. Mỗi đỉnh thuộc đúng một thành phần liên thông; một đỉnh cô lập tự nó là một thành phần.
    2. Vậy {7} là thành phần thứ ba.
    3. Đồ thị có 3 thành phần liên thông.
- `tr_t5_dd_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đơn G có 9 đỉnh và đúng 3 thành phần liên thông; mỗi thành phần là một đồ thị đầy đủ có 3 đỉnh. G có bao nhiêu cạnh?
  - **Đáp án:** 9
    1. Không có cạnh nào nối hai thành phần khác nhau.
    2. Mỗi thành phần là K_3 với C_3^2 = 3 cạnh.
    3. G có 3 . 3 = 9 cạnh.
- `tr_g5_lien_thong` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-5, 2-6, 3-5, 4-6, 5-7, 6-7. G có bao nhiêu thành phần liên thông?
  - **Đáp án:** 1
    1. Bắt đầu từ đỉnh nhỏ nhất chưa xét, đi theo các cạnh để gom mọi đỉnh nối được với nó; lặp lại với đỉnh nhỏ nhất còn lại. Đỉnh không có cạnh nào là một thành phần riêng.
    2. Các thành phần: {1, 2, 3, 4, 5, 6, 7}.
    3. G có 1 thành phần liên thông.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-5, 2-3, 2-6, 2-7, 4-5, 4-7, 6-7. G có bao nhiêu thành phần liên thông?
  - **Đáp án:** 1
    1. Bắt đầu từ đỉnh nhỏ nhất chưa xét, đi theo các cạnh để gom mọi đỉnh nối được với nó; lặp lại với đỉnh nhỏ nhất còn lại. Đỉnh không có cạnh nào là một thành phần riêng.
    2. Các thành phần: {1, 2, 3, 4, 5, 6, 7}.
    3. G có 1 thành phần liên thông.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-2, 2-6, 2-7, 3-4, 3-5, 4-5. G có bao nhiêu thành phần liên thông?
  - **Đáp án:** 2
    1. Bắt đầu từ đỉnh nhỏ nhất chưa xét, đi theo các cạnh để gom mọi đỉnh nối được với nó; lặp lại với đỉnh nhỏ nhất còn lại. Đỉnh không có cạnh nào là một thành phần riêng.
    2. Các thành phần: {1, 2, 6, 7}; {3, 4, 5}.
    3. G có 2 thành phần liên thông.
- `tr_t5_dd_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm số k nhỏ nhất sao cho mọi đồ thị đơn vô hướng có 6 đỉnh và k cạnh đều liên thông.
  - **Đáp án:** 11
    1. Đồ thị gồm K_5 và một đỉnh cô lập có C_5^2 = 10 cạnh mà không liên thông, nên k >= 11.
    2. Một đồ thị 6 đỉnh không liên thông có thể chia đỉnh thành hai nhóm a và 6 - a đỉnh không có cạnh nối giữa hai nhóm, nên có nhiều nhất C_a^2 + C_(6 - a)^2 cạnh.
    3. Với a = 1, 2, 3 giá trị đó là 10, 7, 6: luôn không quá 10. Vậy 11 cạnh thì chắc chắn liên thông, và k = 11.
- `tr_t5_dd_05` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh: nếu đồ thị đơn G không liên thông thì đồ thị bù của G liên thông.
  - **Đáp án (thứ tự đúng):**
    1. Lấy hai đỉnh u, v bất kỳ; cần chỉ ra trong đồ thị bù có đường đi từ u đến v.
    2. Nếu u, v ở hai thành phần khác nhau của G thì u-v không là cạnh của G, nên là cạnh của đồ thị bù.
    3. Nếu u, v cùng một thành phần, chọn một đỉnh w ở thành phần khác; có w vì G không liên thông.
    4. Khi đó u-w và w-v đều không là cạnh của G, nên u, w, v là đường đi trong đồ thị bù.
    5. Vậy mọi cặp đỉnh nối được với nhau trong đồ thị bù: nó liên thông.
  - **Lời giải:**
    1. Liên thông nghĩa là mọi cặp đỉnh có đường đi, nên bắt đầu bằng một cặp đỉnh bất kỳ.
    2. Chia hai trường hợp: khác thành phần (đi thẳng một cạnh) hoặc cùng thành phần (đi vòng qua một đỉnh của thành phần khác).
    3. Hai trường hợp phủ hết mọi khả năng, nên kết luận được.

### Ma trận kề (`tr_t5_ma_tran_ke`)

- `tr_t5_mt_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận kề của mọi đồ thị vô hướng là một ma trận đối xứng.
  - **Đáp án:** Đúng
    1. Phần tử (i, j) của ma trận kề là số cạnh nối i với j.
    2. Trong đồ thị vô hướng, cạnh nối i với j cũng là cạnh nối j với i, nên a_ij = a_ji.
    3. Vậy A^T = A. Với đồ thị có hướng thì điều này nói chung sai.
- `tr_t5_mt_02` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận kề của một đồ thị đơn vô hướng. Ghép mỗi đại lượng tính từ A với ý nghĩa của nó.
  - **Đáp án (ghép đúng):**
    - Tổng các phần tử trên hàng i của A — bậc của đỉnh i
    - Tổng mọi phần tử của A — hai lần số cạnh
    - Phần tử hàng i cột j của A^2 — số hành trình độ dài 2 từ i đến j
    - Tổng các phần tử trên đường chéo chính của A^3 — sáu lần số tam giác
  - **Lời giải:**
    1. Hàng i có số 1 ở đúng các cột của các đỉnh kề i.
    2. Mỗi cạnh cho hai số 1, ở (i, j) và (j, i).
    3. (A^2)_ij là tổng các a_ik . a_kj: đếm các đỉnh k kề cả i lẫn j.
    4. Mỗi tam giác cho 6 hành trình khép kín độ dài 3: 3 đỉnh xuất phát, mỗi đỉnh 2 chiều đi.
- `tr_g5_hanh_trinh_2` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-2, 1-3, 1-4, 1-5, 2-3, 2-4, 2-5, 3-5, 4-5. Gọi A là ma trận kề của G. Phần tử hàng 1 cột 4 của A^2 bằng bao nhiêu?
  - **Đáp án:** 2
    1. Phần tử (1, 4) của A^2 là tổng các tích a_1w . a_w4: nó đếm các đỉnh w kề cả 1 lẫn 4, tức số đường đi độ dài 2 từ 1 đến 4.
    2. Đỉnh kề 1: 2, 3, 4, 5; đỉnh kề 4: 1, 2, 5.
    3. Đỉnh kề cả hai: 2, 5; phần tử bằng 2.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-3, 1-4, 2-4, 2-5, 3-5. Gọi A là ma trận kề của G. Phần tử hàng 3 cột 5 của A^2 bằng bao nhiêu?
  - **Đáp án:** 0
    1. Phần tử (3, 5) của A^2 là tổng các tích a_3w . a_w5: nó đếm các đỉnh w kề cả 3 lẫn 5, tức số đường đi độ dài 2 từ 3 đến 5.
    2. Đỉnh kề 3: 1, 5; đỉnh kề 5: 2, 3.
    3. Đỉnh kề cả hai: không có; phần tử bằng 0.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-2, 1-4, 1-5, 2-3, 2-4, 2-5, 3-4, 3-5, 4-5. Gọi A là ma trận kề của G. Phần tử hàng 3 cột 4 của A^2 bằng bao nhiêu?
  - **Đáp án:** 2
    1. Phần tử (3, 4) của A^2 là tổng các tích a_3w . a_w4: nó đếm các đỉnh w kề cả 3 lẫn 4, tức số đường đi độ dài 2 từ 3 đến 4.
    2. Đỉnh kề 3: 2, 4, 5; đỉnh kề 4: 1, 2, 3, 5.
    3. Đỉnh kề cả hai: 2, 5; phần tử bằng 2.
- `tr_g5_ma_tran_canh` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận kề của một đồ thị đơn vô hướng có 4 đỉnh 1, 2, 3, 4. Đồ thị có bao nhiêu cạnh?
  - A = (0, 1, 0, 1); (1, 0, 0, 1); (0, 0, 0, 0); (1, 1, 0, 0)  (từng hàng)
  - **Đáp án:** 3
    1. Mỗi cạnh u-v cho hai số 1 trong A: ở vị trí (u, v) và (v, u).
    2. Tổng mọi phần tử của A là 6.
    3. Số cạnh: 6/2 = 3.
  - **Câu hỏi:** A là ma trận kề của một đồ thị đơn vô hướng có 4 đỉnh 1, 2, 3, 4. Đỉnh 2 có bậc bao nhiêu?
  - A = (0, 1, 0, 0); (1, 0, 0, 0); (0, 0, 0, 1); (0, 0, 1, 0)  (từng hàng)
  - **Đáp án:** 1
    1. Bậc của đỉnh 2 là số đỉnh kề nó, tức số số 1 trên hàng 2 của A.
    2. Hàng 2: 1 0 0 0; tổng bằng 1.
  - **Câu hỏi:** A là ma trận kề của một đồ thị đơn vô hướng có 4 đỉnh 1, 2, 3, 4. Đỉnh 4 có bậc bao nhiêu?
  - A = (0, 0, 1, 0); (0, 0, 0, 1); (1, 0, 0, 1); (0, 1, 1, 0)  (từng hàng)
  - **Đáp án:** 2
    1. Bậc của đỉnh 4 là số đỉnh kề nó, tức số số 1 trên hàng 4 của A.
    2. Hàng 4: 0 1 1 0; tổng bằng 2.
- `tr_t5_mt_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: B là ma trận kề của một đồ thị có hướng 4 đỉnh (phần tử hàng i cột j bằng 1 khi có cung đi từ i đến j); tìm số cung đi vào và đi ra khỏi đỉnh 2.
  - B = (0, 1, 1, 0); (0, 0, 0, 1); (0, 1, 0, 1); (1, 0, 0, 0)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàng 2 của B là 0 0 0 1, tổng bằng 1.
    2. Cột 2 của B là 1 0 1 0, tổng bằng 2.
    3. Vậy số cung đi vào đỉnh 2 bằng 1, là tổng hàng 2.   **<- bước sai đầu tiên**
    4. Số cung đi ra khỏi đỉnh 2 bằng 2, là tổng cột 2.
  - **Đáp án:** Bước 3: Vậy số cung đi vào đỉnh 2 bằng 1, là tổng hàng 2.
  - **Vì sao sai, và bước đúng:**
    1. Hàng i ghi các cung đi ra từ i; cột j ghi các cung đi vào j.
    2. Tổng hàng 2 bằng 1 là bán bậc ra: chỉ có cung 2 -> 4.
    3. Tổng cột 2 bằng 2 là bán bậc vào: các cung 1 -> 2 và 3 -> 2. Bài giải đã đổi lẫn hai vai trò.
- `tr_t5_mt_04` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận kề của một đồ thị đơn vô hướng G có 4 đỉnh 1, 2, 3, 4.
  - A = (0, 1, 1, 1); (1, 0, 1, 0); (1, 1, 0, 1); (1, 0, 1, 0)  (từng hàng)
  - **Phần a** (Điền số): a) G có bao nhiêu cạnh?
    - **Đáp án a:** 5
  - **Phần b** (Điền số): b) Phần tử hàng 2 cột 4 của A^2 bằng bao nhiêu?
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) Phần tử hàng 1 cột 1 của A^2 bằng 3, đúng bằng bậc của đỉnh 1.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Tổng mọi phần tử của A là 3 + 2 + 3 + 2 = 10, nên G có 10/2 = 5 cạnh: 1-2, 1-3, 1-4, 2-3, 3-4.
    2. b) (A^2)_24 đếm các đỉnh kề cả 2 lẫn 4. Đỉnh kề 2: 1, 3; đỉnh kề 4: 1, 3. Có 2 đỉnh chung nên phần tử bằng 2.
    3. c) (A^2)_11 = a_11 . a_11 + a_12 . a_21 + a_13 . a_31 + a_14 . a_41 = 0 + 1 + 1 + 1 = 3, bằng số đỉnh kề 1: đúng.
- `tr_g5_hanh_trinh_3` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-2, 1-3, 1-5, 2-3, 2-4, 4-5. Một hành trình độ dài 3 từ 4 đến 5 là một dãy đỉnh 4, a, b, 5 mà mỗi hai đỉnh liền nhau kề nhau (đỉnh được phép lặp lại). Có bao nhiêu hành trình như vậy? (Đó là phần tử hàng 4 cột 5 của A^3, A là ma trận kề.)
  - **Đáp án:** 4
    1. Chọn a kề 4, rồi b kề cả a lẫn 5.
    2. Đỉnh kề 4: 2, 5; đỉnh kề 5: 1, 4.
    3. a = 2: 2 cách chọn b; a = 5: 2 cách chọn b.
    4. Cộng lại: 4 hành trình.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-3, 2-4, 2-5, 3-5, 4-5. Một hành trình độ dài 3 từ 3 đến 5 là một dãy đỉnh 3, a, b, 5 mà mỗi hai đỉnh liền nhau kề nhau (đỉnh được phép lặp lại). Có bao nhiêu hành trình như vậy? (Đó là phần tử hàng 3 cột 5 của A^3, A là ma trận kề.)
  - **Đáp án:** 4
    1. Chọn a kề 3, rồi b kề cả a lẫn 5.
    2. Đỉnh kề 3: 1, 5; đỉnh kề 5: 2, 3, 4.
    3. a = 1: 1 cách chọn b; a = 5: 3 cách chọn b.
    4. Cộng lại: 4 hành trình.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-4, 1-5, 2-3, 3-4, 3-5, 4-5. Một hành trình độ dài 3 từ 1 đến 5 là một dãy đỉnh 1, a, b, 5 mà mỗi hai đỉnh liền nhau kề nhau (đỉnh được phép lặp lại). Có bao nhiêu hành trình như vậy? (Đó là phần tử hàng 1 cột 5 của A^3, A là ma trận kề.)
  - **Đáp án:** 5
    1. Chọn a kề 1, rồi b kề cả a lẫn 5.
    2. Đỉnh kề 1: 4, 5; đỉnh kề 5: 1, 3, 4.
    3. a = 4: 2 cách chọn b; a = 5: 3 cách chọn b.
    4. Cộng lại: 5 hành trình.

### Danh sách kề và danh sách cạnh (`tr_t5_danh_sach_ke`)

- `tr_t5_ds_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị đơn vô hướng 6 đỉnh, 9 cạnh được lưu bằng danh sách kề. Tổng độ dài của 6 danh sách kề là bao nhiêu?
  - **Đáp án:** 18
    1. Cạnh u-v xuất hiện hai lần: v trong danh sách của u và u trong danh sách của v.
    2. Độ dài danh sách của u là bậc của u, nên tổng độ dài là tổng các bậc.
    3. Theo định lý bắt tay, tổng đó là 2 . 9 = 18.
- `tr_t5_ds_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị đơn vô hướng có 1000 đỉnh và 3000 cạnh. Nhận xét nào về bộ nhớ là đúng?
    - **(đúng)** Danh sách kề cần khoảng 1000 đầu danh sách và 6000 phần tử, ít hơn nhiều so với ma trận kề
    - Ma trận kề chỉ cần 1000 ô nên ít tốn bộ nhớ nhất
    - Ma trận kề cần 10^6 ô nhưng vẫn ít hơn danh sách kề
    - Hai cách lưu luôn tốn bộ nhớ như nhau
  - **Đáp án:** Danh sách kề cần khoảng 1000 đầu danh sách và 6000 phần tử, ít hơn nhiều so với ma trận kề
    1. Ma trận kề có 1000 . 1000 = 10^6 ô, dù chỉ 6000 ô có số 1.
    2. Danh sách kề có 1000 danh sách với tổng độ dài 2 . 3000 = 6000 phần tử.
    3. Với đồ thị thưa như vậy, danh sách kề tiết kiệm bộ nhớ hơn hẳn; ma trận kề hợp với đồ thị dày hoặc khi cần hỏi nhanh hai đỉnh có kề nhau không.
- `tr_t5_ds_03` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chuyển một đồ thị vô hướng n đỉnh từ danh sách cạnh sang danh sách kề.
  - **Đáp án (thứ tự đúng):**
    1. Tạo n danh sách rỗng Ke(1), Ke(2), ..., Ke(n).
    2. Đọc lần lượt từng cạnh u-v trong danh sách cạnh.
    3. Thêm v vào cuối Ke(u).
    4. Thêm u vào cuối Ke(v), vì cạnh vô hướng đi được cả hai chiều.
    5. Khi đã đọc hết các cạnh, Ke(u) là danh sách các đỉnh kề u.
  - **Lời giải:**
    1. Phải có các danh sách rỗng trước khi thêm phần tử vào.
    2. Mỗi cạnh vô hướng được ghi vào cả hai danh sách của hai đầu.
    3. Thời gian làm việc này tỉ lệ với n + m (m là số cạnh).
- `tr_g5_ban_bac_vao` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị có hướng 5 đỉnh được lưu bằng danh sách kề, Ke(u) là danh sách các đỉnh v có cung đi từ u đến v: Ke(1) = 3, 4, 5; Ke(2) = 4, 5; Ke(3) = 1, 4; Ke(4) = 3, 5; Ke(5) = 2. Có bao nhiêu cung đi vào đỉnh 4?
  - **Đáp án:** 3
    1. Danh sách kề chỉ ghi các cung đi ra. Cung đi vào 4 là những lần 4 xuất hiện trong danh sách của một đỉnh khác.
    2. 4 có mặt trong danh sách của: 1, 2, 3.
    3. Bán bậc vào của 4 là 3.
  - **Câu hỏi:** Một đồ thị có hướng 5 đỉnh được lưu bằng danh sách kề, Ke(u) là danh sách các đỉnh v có cung đi từ u đến v: Ke(1) = 4; Ke(2) = 3; Ke(3) = 1, 2, 5; Ke(4) = rỗng; Ke(5) = 1. Có bao nhiêu cung đi vào đỉnh 2?
  - **Đáp án:** 1
    1. Danh sách kề chỉ ghi các cung đi ra. Cung đi vào 2 là những lần 2 xuất hiện trong danh sách của một đỉnh khác.
    2. 2 có mặt trong danh sách của: 3.
    3. Bán bậc vào của 2 là 1.
  - **Câu hỏi:** Một đồ thị có hướng 5 đỉnh được lưu bằng danh sách kề, Ke(u) là danh sách các đỉnh v có cung đi từ u đến v: Ke(1) = 2, 4; Ke(2) = 1, 5; Ke(3) = 1, 2, 5; Ke(4) = 5; Ke(5) = 2, 3. Có bao nhiêu cung đi vào đỉnh 2?
  - **Đáp án:** 3
    1. Danh sách kề chỉ ghi các cung đi ra. Cung đi vào 2 là những lần 2 xuất hiện trong danh sách của một đỉnh khác.
    2. 2 có mặt trong danh sách của: 1, 3, 5.
    3. Bán bậc vào của 2 là 3.
- `tr_t5_ds_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: một đồ thị vô hướng có danh sách kề Ke(1) = 2, 3; Ke(2) = 1, 3, 4; Ke(3) = 1, 2; Ke(4) = 2. Đồ thị có bao nhiêu cạnh?
  - **Lời giải đưa ra (có một bước sai):**
    1. Độ dài các danh sách là 2, 3, 2 và 1.
    2. Tổng độ dài các danh sách là 2 + 3 + 2 + 1 = 8.
    3. Mỗi phần tử của một danh sách là một cạnh khác nhau, nên đồ thị có 8 cạnh.   **<- bước sai đầu tiên**
    4. Vậy danh sách cạnh của đồ thị có 8 dòng.
  - **Đáp án:** Bước 3: Mỗi phần tử của một danh sách là một cạnh khác nhau, nên đồ thị có 8 cạnh.
  - **Vì sao sai, và bước đúng:**
    1. Trong đồ thị vô hướng, cạnh u-v có mặt hai lần: trong Ke(u) và trong Ke(v).
    2. Số cạnh là 8/2 = 4: đó là 1-2, 1-3, 2-3, 2-4.
    3. Chỉ với đồ thị có hướng thì tổng độ dài các danh sách kề mới bằng số cung.
- `tr_t5_ds_05` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị đơn vô hướng G có 6 đỉnh được lưu bằng danh sách kề: Ke(1) = 2, 4; Ke(2) = 1, 3, 4, 5; Ke(3) = 2, 6; Ke(4) = 1, 2, 5; Ke(5) = 2, 4; Ke(6) = 3.
  - **Phần a** (Điền số): a) G có bao nhiêu cạnh?
    - **Đáp án a:** 7
  - **Phần b** (Trắc nghiệm): b) Hàng của đỉnh 4 trong ma trận kề của G (các cột 1 đến 6) là
    - **(đúng)** 1 1 0 0 1 0
    - 1 1 0 1 1 0
    - 0 1 0 0 1 0
    - 1 0 0 0 1 0
    - **Đáp án b:** 1 1 0 0 1 0
  - **Phần c** (Điền số): c) Ma trận kề của G có 36 ô. Có bao nhiêu ô trong đó bằng 1?
    - **Đáp án c:** 14
  - **Lời giải:**
    1. a) Tổng độ dài các danh sách là 2 + 4 + 2 + 3 + 2 + 1 = 14; mỗi cạnh được ghi hai lần nên có 7 cạnh: 1-2, 1-4, 2-3, 2-4, 2-5, 3-6, 4-5.
    2. b) Ke(4) = 1, 2, 5 nên hàng 4 có số 1 ở các cột 1, 2, 5: 1 1 0 0 1 0. Đồ thị đơn không có khuyên nên ô (4, 4) bằng 0.
    3. c) Mỗi cạnh cho hai ô bằng 1, nên có 2 . 7 = 14 ô bằng 1, đúng bằng tổng độ dài các danh sách kề; 22 ô còn lại bằng 0.

## Tầng 6: Tìm kiếm trên đồ thị, đồ thị Euler và Hamilton

34 dạng câu (25 câu viết tay, 9 bộ sinh câu); 34 chưa duyệt.

### Tìm kiếm theo chiều rộng (`tr_t6_bfs`)

- `tr_t6_bfs_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thuật toán tìm kiếm theo chiều rộng (BFS) dùng cấu trúc dữ liệu nào để giữ các đỉnh đang chờ được xét?
    - **(đúng)** Hàng đợi: đỉnh vào trước được lấy ra trước
    - Ngăn xếp: đỉnh vào sau được lấy ra trước
    - Một mảng đã sắp xếp theo số hiệu đỉnh
    - Không cần cấu trúc nào, chỉ cần đệ quy
  - **Đáp án:** Hàng đợi: đỉnh vào trước được lấy ra trước
    1. BFS xét hết các đỉnh kề của đỉnh xuất phát rồi mới đến các đỉnh xa hơn.
    2. Hàng đợi bảo đảm đỉnh được phát hiện trước thì được xét trước, nên các đỉnh được thăm theo khoảng cách tăng dần.
    3. Ngăn xếp (hoặc đệ quy) cho tìm kiếm theo chiều sâu.
- `tr_t6_bfs_02` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước của thuật toán BFS từ đỉnh s.
  - **Đáp án (thứ tự đúng):**
    1. Đánh dấu s đã thăm và đưa s vào hàng đợi.
    2. Lấy đỉnh u ở đầu hàng đợi ra.
    3. Với mỗi đỉnh v kề u theo thứ tự số tăng dần, nếu v chưa thăm thì đánh dấu v, ghi trước(v) = u và đưa v vào cuối hàng đợi.
    4. Quay lại bước lấy đỉnh ở đầu hàng đợi, cho đến khi hàng đợi rỗng.
  - **Lời giải:**
    1. Khởi tạo hàng đợi với đỉnh xuất phát.
    2. Mỗi vòng lấy một đỉnh ra và đưa các đỉnh kề chưa thăm của nó vào.
    3. Ghi trước(v) để sau này lần ngược được đường đi ngắn nhất; dừng khi hàng đợi rỗng.
- `tr_t6_bfs_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi chạy BFS từ đỉnh s trên một đồ thị vô hướng, khoảng cách từ s đến các đỉnh, xếp theo thứ tự chúng được thăm, là một dãy không giảm.
  - **Đáp án:** Đúng
    1. Hàng đợi luôn chứa các đỉnh của một lớp d, có thể nối tiếp bởi các đỉnh lớp d + 1.
    2. Các đỉnh lớp d + 1 chỉ được đưa vào khi lấy các đỉnh lớp d ra, nên chúng luôn đứng sau.
    3. Vì vậy BFS thăm hết lớp 0, rồi lớp 1, lớp 2, ...: khoảng cách không giảm.
- `tr_g6_bfs_khoang_cach` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-4, 2-5, 3-5, 4-5, 5-6. Đường đi từ 4 đến 6 có ít cạnh nhất là bao nhiêu cạnh?
  - **Đáp án:** 2
    1. Chạy BFS từ 4: BFS thăm các đỉnh theo khoảng cách tăng dần, và khoảng cách của một đỉnh bằng khoảng cách của đỉnh đã đưa nó vào hàng đợi cộng 1.
    2. Lần ngược theo đỉnh đứng trước trên cây BFS: 4 - 5 - 6.
    3. Đường đi ngắn nhất có 2 cạnh.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-3, 2-5, 3-6, 4-6, 5-6. Đường đi từ 6 đến 2 có ít cạnh nhất là bao nhiêu cạnh?
  - **Đáp án:** 2
    1. Chạy BFS từ 6: BFS thăm các đỉnh theo khoảng cách tăng dần, và khoảng cách của một đỉnh bằng khoảng cách của đỉnh đã đưa nó vào hàng đợi cộng 1.
    2. Lần ngược theo đỉnh đứng trước trên cây BFS: 6 - 5 - 2.
    3. Đường đi ngắn nhất có 2 cạnh.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-4, 1-5, 1-6, 4-5. Đường đi từ 5 đến 2 có ít cạnh nhất là bao nhiêu cạnh?
  - **Đáp án:** 2
    1. Chạy BFS từ 5: BFS thăm các đỉnh theo khoảng cách tăng dần, và khoảng cách của một đỉnh bằng khoảng cách của đỉnh đã đưa nó vào hàng đợi cộng 1.
    2. Lần ngược theo đỉnh đứng trước trên cây BFS: 5 - 1 - 2.
    3. Đường đi ngắn nhất có 2 cạnh.
- `tr_g6_bfs_thu_tu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-4, 2-5, 2-6, 3-5, 4-5, 5-6. Chạy BFS từ đỉnh 4, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 1, 5, 2, 3, 6
    1. Đưa 4 vào hàng đợi. Mỗi lần lấy đỉnh đầu hàng đợi ra, đưa các đỉnh kề chưa thăm của nó vào cuối hàng đợi theo thứ tự tăng dần.
    2. Các đỉnh được thăm theo từng lớp: khoảng cách 0: 4; khoảng cách 1: 1, 5; khoảng cách 2: 2, 3, 6.
    3. Thứ tự thăm: 4, 1, 5, 2, 3, 6.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-3, 1-5, 2-5, 3-6, 4-6, 5-6. Chạy BFS từ đỉnh 4, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 6, 3, 5, 1, 2
    1. Đưa 4 vào hàng đợi. Mỗi lần lấy đỉnh đầu hàng đợi ra, đưa các đỉnh kề chưa thăm của nó vào cuối hàng đợi theo thứ tự tăng dần.
    2. Các đỉnh được thăm theo từng lớp: khoảng cách 0: 4; khoảng cách 1: 6; khoảng cách 2: 3, 5; khoảng cách 3: 1, 2.
    3. Thứ tự thăm: 4, 6, 3, 5, 1, 2.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-4, 1-5, 1-6, 4-5, 4-6. Chạy BFS từ đỉnh 5, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 5, 1, 4, 2, 3, 6
    1. Đưa 5 vào hàng đợi. Mỗi lần lấy đỉnh đầu hàng đợi ra, đưa các đỉnh kề chưa thăm của nó vào cuối hàng đợi theo thứ tự tăng dần.
    2. Các đỉnh được thăm theo từng lớp: khoảng cách 0: 5; khoảng cách 1: 1, 4; khoảng cách 2: 2, 3, 6.
    3. Thứ tự thăm: 5, 1, 4, 2, 3, 6.
- `tr_t6_bfs_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có các đỉnh 1, 2, ..., 7 và các cạnh 1-2, 1-3, 2-4, 2-5, 3-5, 4-6, 5-6, 6-7; tìm số cạnh của đường đi ngắn nhất từ 1 đến 5.
  - **Lời giải đưa ra (có một bước sai):**
    1. Chạy DFS từ 1, thăm các đỉnh kề theo thứ tự số tăng dần: thứ tự thăm là 1, 2, 4, 6, 5, 3, 7.
    2. Trên cây DFS, đường từ 1 đến 5 là 1 - 2 - 4 - 6 - 5.
    3. Vậy đường đi ngắn nhất từ 1 đến 5 có 4 cạnh.   **<- bước sai đầu tiên**
    4. Do đó 5 là đỉnh xa đỉnh 1 nhất trong đồ thị.
  - **Đáp án:** Bước 3: Vậy đường đi ngắn nhất từ 1 đến 5 có 4 cạnh.
  - **Vì sao sai, và bước đúng:**
    1. Thứ tự DFS và đường trên cây DFS ở hai bước đầu đều đúng.
    2. Nhưng đường trên cây DFS không nhất thiết ngắn nhất: 1 - 2 - 5 chỉ có 2 cạnh.
    3. Muốn có khoảng cách phải dùng BFS: từ 1, các lớp là {2, 3}, {4, 5}, {6}, {7}, nên 5 cách 1 hai cạnh.
- `tr_t6_bfs_04` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7 và các cạnh 1-3, 1-4, 2-5, 2-7, 3-5, 3-6, 4-6, 5-7, 6-7. Chạy BFS từ đỉnh 2, thăm các đỉnh kề theo thứ tự số tăng dần, và ghi trước(v) là đỉnh đã đưa v vào hàng đợi.
  - **Phần a** (Điền số): a) Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 2, 5, 7, 3, 6, 1, 4
  - **Phần b** (Điền số): b) Đường đi từ 2 đến 4 có ít cạnh nhất là bao nhiêu cạnh?
    - **Đáp án b:** 3
  - **Phần c** (Trắc nghiệm): c) Lần ngược theo trước(v) từ đỉnh 4 về 2, ta được đường đi nào?
    - **(đúng)** 2 - 7 - 6 - 4
    - 2 - 5 - 3 - 1 - 4
    - 2 - 5 - 3 - 6 - 4
    - 2 - 5 - 7 - 6 - 4
    - **Đáp án c:** 2 - 7 - 6 - 4
  - **Lời giải:**
    1. a) Danh sách kề: 2: 5, 7; 5: 2, 3, 7; 7: 2, 5, 6; 3: 1, 5, 6; 6: 3, 4, 7. Lấy 2 ra, đưa 5, 7 vào; lấy 5, đưa 3 vào; lấy 7, đưa 6 vào; lấy 3, đưa 1 vào; lấy 6, đưa 4 vào. Thứ tự: 2, 5, 7, 3, 6, 1, 4.
    2. b) Các lớp: {5, 7} cách 2 một cạnh, {3, 6} hai cạnh, {1, 4} ba cạnh. Vậy 4 cách 2 ba cạnh.
    3. c) trước(4) = 6, trước(6) = 7, trước(7) = 2: đường đi 2 - 7 - 6 - 4, có đúng 3 cạnh như khoảng cách ở câu b.

### Tìm kiếm theo chiều sâu (`tr_t6_dfs`)

- `tr_t6_dfs_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7 và các cạnh 1-3, 1-4, 2-5, 2-7, 3-5, 3-6, 4-6, 5-7, 6-7. Chạy DFS (đệ quy) từ đỉnh 4, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 1, 3, 5, 2, 7, 6
    1. Danh sách kề: 1: 3, 4; 2: 5, 7; 3: 1, 5, 6; 4: 1, 6; 5: 2, 3, 7; 6: 3, 4, 7; 7: 2, 5, 6.
    2. Từ 4 sang 1, từ 1 sang 3 (4 đã thăm), từ 3 sang 5, từ 5 sang 2, từ 2 sang 7.
    3. Từ 7: 2, 5 đã thăm, sang 6. Mọi đỉnh đã thăm, quay lui về 4 và kết thúc.
    4. Thứ tự thăm: 4, 1, 3, 5, 2, 7, 6.
- `tr_t6_dfs_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi viết DFS không dùng đệ quy, ta thay đệ quy bằng cấu trúc dữ liệu nào?
    - **(đúng)** Ngăn xếp
    - Hàng đợi
    - Hàng đợi ưu tiên theo số hiệu đỉnh
    - Ma trận kề
  - **Đáp án:** Ngăn xếp
    1. Đệ quy tự giữ các lời gọi đang dở trong ngăn xếp của chương trình.
    2. Khử đệ quy thì giữ các đỉnh chờ xét trong một ngăn xếp: đỉnh đưa vào sau được xét trước, nên đi sâu trước.
    3. Hàng đợi cho BFS; ma trận kề chỉ là một cách lưu đồ thị.
- `tr_t6_dfs_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với cùng một đồ thị vô hướng và cùng đỉnh xuất phát s, BFS và DFS thăm cùng một tập đỉnh (dù thứ tự thăm có thể khác nhau).
  - **Đáp án:** Đúng
    1. Cả hai thuật toán thăm một đỉnh khi và chỉ khi có đường đi từ s đến nó.
    2. Vậy cả hai thăm đúng thành phần liên thông chứa s.
    3. Chỉ thứ tự thăm và cây tìm kiếm là khác nhau.
- `tr_g6_dfs_thu_tu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-4, 2-5, 2-6, 3-5, 4-5, 5-6. Chạy DFS (đệ quy) từ đỉnh 4, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 1, 5, 2, 6, 3
    1. Danh sách kề (đã xếp tăng dần): 1: 4; 2: 5, 6; 3: 5; 4: 1, 5; 5: 2, 3, 4, 6; 6: 2, 5.
    2. DFS(u): thăm u, rồi lần lượt với mỗi đỉnh kề v chưa thăm gọi DFS(v). Khi u hết đỉnh kề chưa thăm thì quay lui về đỉnh đã gọi nó, không nhảy sang đỉnh không kề.
    3. Thứ tự thăm: 4, 1, 5, 2, 6, 3.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-3, 1-5, 2-5, 3-6, 4-6, 5-6. Chạy DFS (đệ quy) từ đỉnh 4, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 6, 3, 1, 5, 2
    1. Danh sách kề (đã xếp tăng dần): 1: 3, 5; 2: 5; 3: 1, 6; 4: 6; 5: 1, 2, 6; 6: 3, 4, 5.
    2. DFS(u): thăm u, rồi lần lượt với mỗi đỉnh kề v chưa thăm gọi DFS(v). Khi u hết đỉnh kề chưa thăm thì quay lui về đỉnh đã gọi nó, không nhảy sang đỉnh không kề.
    3. Thứ tự thăm: 4, 6, 3, 1, 5, 2.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-4, 1-5, 1-6, 4-5, 4-6. Chạy DFS (đệ quy) từ đỉnh 5, thăm các đỉnh kề theo thứ tự số tăng dần. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.
  - **Đáp án:** 5, 1, 2, 3, 4, 6
    1. Danh sách kề (đã xếp tăng dần): 1: 2, 3, 4, 5, 6; 2: 1; 3: 1; 4: 1, 5, 6; 5: 1, 4; 6: 1, 4.
    2. DFS(u): thăm u, rồi lần lượt với mỗi đỉnh kề v chưa thăm gọi DFS(v). Khi u hết đỉnh kề chưa thăm thì quay lui về đỉnh đã gọi nó, không nhảy sang đỉnh không kề.
    3. Thứ tự thăm: 5, 1, 2, 3, 4, 6.
- `tr_t6_dfs_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có các đỉnh 1, 2, ..., 6 và các cạnh 1-2, 1-5, 2-3, 4-5, 4-6; chạy DFS từ 1, thăm các đỉnh kề theo thứ tự số tăng dần.
  - **Lời giải đưa ra (có một bước sai):**
    1. Thăm 1. Đỉnh kề nhỏ nhất chưa thăm của 1 là 2: thăm 2.
    2. Đỉnh kề chưa thăm của 2 là 3: thăm 3.
    3. 3 không còn đỉnh kề nào chưa thăm. Đỉnh chưa thăm nhỏ nhất của đồ thị là 4: thăm 4.   **<- bước sai đầu tiên**
    4. Từ 4 thăm 5, quay lại 4 rồi thăm 6.
    5. Thứ tự thăm là 1, 2, 3, 4, 5, 6.
  - **Đáp án:** Bước 3: 3 không còn đỉnh kề nào chưa thăm. Đỉnh chưa thăm nhỏ nhất của đồ thị là 4: thăm 4.
  - **Vì sao sai, và bước đúng:**
    1. Khi 3 hết đỉnh kề chưa thăm, DFS quay lui về 2, rồi về 1; nó không nhảy sang đỉnh 4 vì 4 không kề 3.
    2. Ở đỉnh 1 còn đỉnh kề 5 chưa thăm: thăm 5, từ 5 thăm 4, từ 4 thăm 6.
    3. Thứ tự đúng là 1, 2, 3, 5, 4, 6.
- `tr_t6_dfs_04` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7 và các cạnh 1-2, 1-3, 2-4, 2-5, 3-5, 4-6, 5-6, 6-7. Lần này các đỉnh kề được xét theo một thứ tự bất kỳ. Dãy nào có thể là thứ tự thăm của DFS từ đỉnh 1?
    - **(đúng)** 1, 3, 5, 6, 7, 4, 2
    - 1, 2, 3, 5, 6, 4, 7
    - 1, 2, 4, 6, 7, 3, 5
    - 1, 3, 5, 2, 4, 7, 6
  - **Đáp án:** 1, 3, 5, 6, 7, 4, 2
    1. 1, 3, 5, 6, 7, 4, 2: đi 1 - 3 - 5 - 6 - 7; 7 hết đỉnh kề, quay lui về 6, đi tiếp 6 - 4 - 2. Hợp lệ.
    2. 1, 2, 3, ...: sau 2 còn đỉnh kề 4, 5 chưa thăm, DFS phải đi tiếp từ 2, không thể sang 3 (không kề 2).
    3. 1, 2, 4, 6, 7, 3, 5: sau 7 quay lui về 6, mà 6 còn đỉnh kề 5 chưa thăm, nên phải thăm 5 trước 3.
    4. 1, 3, 5, 2, 4, 7, 6: từ 4 chỉ còn 6 chưa thăm, không thể nhảy sang 7 (không kề 4).

### Ứng dụng của tìm kiếm (`tr_t6_ung_dung_tim_kiem`)

- `tr_t6_ud_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 9 và các cạnh 1-5, 2-6, 3-7, 5-9, 6-8. Chương trình duyệt v = 1, 2, ..., 9; gặp đỉnh v chưa thăm thì gọi DFS(v). DFS được gọi từ vòng duyệt này bao nhiêu lần?
  - **Đáp án:** 4
    1. v = 1: DFS(1) thăm 1, 5, 9. v = 2: DFS(2) thăm 2, 6, 8.
    2. v = 3: DFS(3) thăm 3, 7. v = 4: đỉnh 4 không có cạnh nào, DFS(4) chỉ thăm 4.
    3. Các đỉnh 5 đến 9 đã được thăm. Có 4 lần gọi, bằng số thành phần liên thông.
- `tr_t6_ud_02` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi bài toán với cách dùng BFS hoặc DFS để giải nó.
  - **Đáp án (ghép đúng):**
    - Đếm số thành phần liên thông — gọi BFS hoặc DFS từ mỗi đỉnh chưa thăm và đếm số lần gọi
    - Tìm đường đi ít cạnh nhất từ s đến t — chạy BFS từ s rồi lần ngược theo trước(t)
    - Kiểm tra hai đỉnh s và t có nối được với nhau không — chạy BFS hoặc DFS từ s và xem t có được thăm không
    - Kiểm tra cả đồ thị có liên thông không — chạy một lần duyệt từ một đỉnh bất kỳ và xem có thăm đủ n đỉnh không
  - **Lời giải:**
    1. Mỗi lần gọi duyệt từ một đỉnh chưa thăm thăm trọn một thành phần mới.
    2. Chỉ BFS cho đường đi ít cạnh nhất; DFS cho một đường đi nhưng không nhất thiết ngắn nhất.
    3. Duyệt từ s thăm đúng các đỉnh nối được với s.
    4. Đồ thị liên thông khi một lần duyệt thăm được mọi đỉnh.
- `tr_t6_ud_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm một đường đi ít cạnh nhất từ s đến t bằng BFS.
  - **Đáp án (thứ tự đúng):**
    1. Chạy BFS từ s, ghi trước(v) cho mỗi đỉnh v được thăm.
    2. Nếu t không được thăm thì không có đường đi từ s đến t; dừng.
    3. Ngược lại, bắt đầu từ t, lần lượt đi sang trước(t), trước(trước(t)), ... cho đến khi gặp s.
    4. Đảo ngược dãy đỉnh vừa thu được để có đường đi từ s đến t.
  - **Lời giải:**
    1. Phải chạy BFS trước để có các trước(v).
    2. Kiểm tra t có được thăm không trước khi lần ngược.
    3. Lần ngược cho dãy t, ..., s, nên cần đảo lại để được đường từ s.
- `tr_g6_noi_duoc` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-3, 1-5, 2-4, 2-5, 6-7. Khẳng định: có đường đi từ 1 đến 7.
  - **Đáp án:** Sai
    1. Chạy BFS (hoặc DFS) từ 1; có đường đi đến 7 khi và chỉ khi 7 được thăm.
    2. Các đỉnh được thăm: 1, 2, 3, 4, 5.
    3. 7 không có trong đó: khẳng định sai.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-3, 2-6, 4-5, 4-7, 6-7. Khẳng định: có đường đi từ 4 đến 5.
  - **Đáp án:** Đúng
    1. Chạy BFS (hoặc DFS) từ 4; có đường đi đến 5 khi và chỉ khi 5 được thăm.
    2. Các đỉnh được thăm: 2, 4, 5, 6, 7.
    3. 5 có trong đó: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-2, 2-6, 2-7, 3-4, 3-5, 4-5. Khẳng định: có đường đi từ 2 đến 6.
  - **Đáp án:** Đúng
    1. Chạy BFS (hoặc DFS) từ 2; có đường đi đến 6 khi và chỉ khi 6 được thăm.
    2. Các đỉnh được thăm: 1, 2, 6, 7.
    3. 6 có trong đó: khẳng định đúng.
- `tr_t6_ud_03` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 8 và các cạnh 1-4, 4-7, 2-5, 5-8, 2-8, 3-6.
  - **Phần a** (Điền số): a) G có bao nhiêu thành phần liên thông?
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Chạy BFS từ đỉnh 5. BFS thăm tất cả bao nhiêu đỉnh, kể cả đỉnh 5?
    - **Đáp án b:** 3
  - **Phần c** (Đúng/Sai): c) Có đường đi từ đỉnh 1 đến đỉnh 7 trong G.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Duyệt từ 1 được {1, 4, 7}; từ 2 được {2, 5, 8}; từ 3 được {3, 6}. Mọi đỉnh đã thăm: có 3 thành phần.
    2. b) BFS từ 5 thăm đúng thành phần {2, 5, 8}: 3 đỉnh.
    3. c) 1 và 7 cùng thành phần {1, 4, 7}, có đường đi 1 - 4 - 7: đúng.
- `tr_g6_thanh_phan` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-5, 2-6, 3-5, 4-6, 5-7, 6-7. Chương trình duyệt v = 1, 2, ..., 7; gặp đỉnh v chưa thăm thì gọi DFS(v). DFS được gọi từ vòng duyệt này bao nhiêu lần?
  - **Đáp án:** 1
    1. Một lần duyệt từ một đỉnh thăm đúng những đỉnh nối được với nó.
    2. Các thành phần liên thông của G: {1, 2, 3, 4, 5, 6, 7}.
    3. Mỗi lần gọi thăm trọn một thành phần liên thông, nên số lần gọi là số thành phần: 1.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-5, 2-3, 2-6, 2-7, 4-5, 4-7, 6-7. Chạy BFS từ đỉnh 1. BFS thăm tất cả bao nhiêu đỉnh, kể cả 1?
  - **Đáp án:** 7
    1. Một lần duyệt từ một đỉnh thăm đúng những đỉnh nối được với nó.
    2. Các thành phần liên thông của G: {1, 2, 3, 4, 5, 6, 7}.
    3. BFS từ 1 thăm đúng thành phần liên thông chứa 1, gồm 7 đỉnh.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-2, 2-6, 2-7, 3-4, 3-5, 4-5. Chương trình duyệt v = 1, 2, ..., 7; gặp đỉnh v chưa thăm thì gọi DFS(v). DFS được gọi từ vòng duyệt này bao nhiêu lần?
  - **Đáp án:** 2
    1. Một lần duyệt từ một đỉnh thăm đúng những đỉnh nối được với nó.
    2. Các thành phần liên thông của G: {1, 2, 6, 7}; {3, 4, 5}.
    3. Mỗi lần gọi thăm trọn một thành phần liên thông, nên số lần gọi là số thành phần: 2.

### Đồ thị Euler (`tr_t6_euler`)

- `tr_t6_eu_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đồ thị vô hướng liên thông có chu trình Euler khi và chỉ khi mọi đỉnh của nó có bậc chẵn.
  - **Đáp án:** Đúng
    1. Chiều thuận: mỗi lần chu trình đi qua một đỉnh nó dùng hai cạnh, một vào một ra, nên mỗi bậc là số chẵn.
    2. Chiều ngược: nếu mọi bậc chẵn và đồ thị liên thông, ta ghép dần các chu trình nhỏ thành một chu trình đi qua mọi cạnh.
    3. Đó là định lý Euler.
- `tr_t6_eu_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đầy đủ nào sau đây có chu trình Euler?
    - **(đúng)** K_5
    - K_4
    - K_6
    - K_8
  - **Đáp án:** K_5
    1. Trong K_n mỗi đỉnh có bậc n - 1, và K_n liên thông.
    2. K_n có chu trình Euler khi và chỉ khi n - 1 chẵn, tức n lẻ.
    3. Chỉ K_5 (bậc 4) thỏa; K_4, K_6, K_8 có bậc 3, 5, 7 là số lẻ.
- `tr_t6_eu_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đa đồ thị vô hướng liên thông có đúng 6 đỉnh bậc lẻ. Cần thêm ít nhất bao nhiêu cạnh (được phép thêm cạnh bội) để nó có chu trình Euler?
  - **Đáp án:** 3
    1. Thêm một cạnh làm đổi tính chẵn lẻ của đúng hai đỉnh, nên mỗi cạnh sửa được nhiều nhất hai đỉnh bậc lẻ.
    2. Có 6 đỉnh bậc lẻ nên cần ít nhất 6/2 = 3 cạnh.
    3. Ghép 6 đỉnh đó thành 3 cặp và nối mỗi cặp bằng một cạnh: mọi bậc thành chẵn, đồ thị vẫn liên thông. Vậy 3 cạnh là đủ.
- `tr_t6_eu_06` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm một chu trình Euler bằng cách ghép các chu trình.
  - **Đáp án (thứ tự đúng):**
    1. Kiểm tra đồ thị liên thông và mọi đỉnh có bậc chẵn.
    2. Từ một đỉnh bất kỳ, đi theo các cạnh chưa dùng cho đến khi quay về đỉnh đầu: được chu trình C.
    3. Nếu C chưa dùng hết các cạnh, chọn một đỉnh trên C còn cạnh chưa dùng.
    4. Từ đỉnh đó đi một chu trình mới bằng các cạnh chưa dùng, rồi chèn chu trình mới vào C tại đỉnh đó.
    5. Lặp lại hai bước trên cho đến khi C dùng hết mọi cạnh.
  - **Lời giải:**
    1. Điều kiện bậc chẵn bảo đảm đi theo cạnh chưa dùng thì luôn quay về được đỉnh xuất phát.
    2. Đồ thị liên thông bảo đảm còn cạnh chưa dùng thì có một đỉnh trên C chạm tới nó.
    3. Mỗi lần chèn, C dài thêm, cho đến khi chứa mọi cạnh.
- `tr_g6_euler` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-4, 1-5, 2-3, 3-5, 3-6, 4-5, 5-6. Khẳng định: G có chu trình Euler.
  - **Đáp án:** Đúng
    1. Đồ thị liên thông có chu trình Euler khi và chỉ khi mọi đỉnh có bậc chẵn. G liên thông (mọi đỉnh nối được với đỉnh 1).
    2. Bậc của các đỉnh 1, ..., 6: 4, 2, 4, 2, 4, 2.
    3. Mọi bậc đều chẵn: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-4, 2-4, 2-5, 2-6, 3-5, 3-6, 4-5, 4-6, 5-6. Khẳng định: G có chu trình Euler.
  - **Đáp án:** Đúng
    1. Đồ thị liên thông có chu trình Euler khi và chỉ khi mọi đỉnh có bậc chẵn. G liên thông (mọi đỉnh nối được với đỉnh 1).
    2. Bậc của các đỉnh 1, ..., 6: 2, 4, 2, 4, 4, 4.
    3. Mọi bậc đều chẵn: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-5, 1-6, 2-5, 3-5, 3-6, 4-5, 4-6, 5-6. Khẳng định: G có chu trình Euler.
  - **Đáp án:** Sai
    1. Đồ thị liên thông có chu trình Euler khi và chỉ khi mọi đỉnh có bậc chẵn. G liên thông (mọi đỉnh nối được với đỉnh 1).
    2. Bậc của các đỉnh 1, ..., 6: 4, 2, 3, 2, 5, 4.
    3. Các đỉnh 3, 5 có bậc lẻ: không có chu trình Euler, khẳng định sai.
- `tr_t6_eu_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị G có các đỉnh 1, 2, ..., 5 và các cạnh 1-2, 2-3, 3-4, 4-5, 5-1, 1-3; G có chu trình Euler không?
  - **Lời giải đưa ra (có một bước sai):**
    1. Dãy 1 - 2 - 3 - 4 - 5 - 1 dùng các cạnh 1-2, 2-3, 3-4, 4-5, 5-1 của G.
    2. Nó đi qua mỗi đỉnh đúng một lần rồi về đỉnh đầu: đó là một chu trình Hamilton.
    3. Một chu trình đi qua mọi đỉnh là chu trình Euler, nên G có chu trình Euler.   **<- bước sai đầu tiên**
    4. Vậy mọi đỉnh của G có bậc chẵn.
  - **Đáp án:** Bước 3: Một chu trình đi qua mọi đỉnh là chu trình Euler, nên G có chu trình Euler.
  - **Vì sao sai, và bước đúng:**
    1. Chu trình Euler phải đi qua mọi CẠNH đúng một lần, không phải mọi đỉnh. Chu trình ở trên bỏ sót cạnh 1-3.
    2. Bậc của các đỉnh 1, ..., 5 là 3, 2, 3, 2, 2: đỉnh 1 và 3 có bậc lẻ.
    3. Vậy G không có chu trình Euler (nhưng có đường đi Euler từ 1 đến 3), dù có chu trình Hamilton.
- `tr_t6_eu_04` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G vô hướng, liên thông, có 6 đỉnh; bậc của các đỉnh 1, 2, ..., 6 lần lượt là 2, 3, 4, 4, 3, 2.
  - **Phần a** (Điền số): a) G có bao nhiêu cạnh?
    - **Đáp án a:** 9
  - **Phần b** (Đúng/Sai): b) G có chu trình Euler.
    - **Đáp án b:** Sai
  - **Phần c** (Điền số): c) G có đường đi Euler. Mọi đường đi Euler của G phải bắt đầu ở một trong hai đỉnh nào? Nhập hai đỉnh đó.
    - **Đáp án c:** 2, 5  (thứ tự nào cũng được)
  - **Lời giải:**
    1. a) Tổng các bậc là 2 + 3 + 4 + 4 + 3 + 2 = 18, nên G có 18/2 = 9 cạnh.
    2. b) Đỉnh 2 và đỉnh 5 có bậc lẻ, nên không có chu trình Euler.
    3. c) G liên thông và có đúng hai đỉnh bậc lẻ, nên có đường đi Euler; nó phải bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia: 2 và 5. (Ví dụ G có các cạnh 1-2, 1-3, 2-3, 2-4, 3-4, 3-5, 4-5, 4-6, 5-6.)
- `tr_g6_euler_duong` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị liên thông G có các đỉnh 1, 2, ..., 6; các cạnh: 1-3, 1-4, 1-5, 2-3, 3-5, 3-6, 4-5, 5-6. G có đường đi Euler nhưng không có chu trình Euler. Mọi đường đi Euler của G phải bắt đầu ở một trong hai đỉnh nào? Nhập hai đỉnh đó.
  - **Đáp án:** 1, 2  (thứ tự nào cũng được)
    1. Bậc của các đỉnh 1, ..., 6: 3, 1, 4, 2, 4, 2.
    2. Có đúng hai đỉnh bậc lẻ: 1 và 2.
    3. Trên một đường đi Euler, mỗi lần đi qua một đỉnh ở giữa dùng hai cạnh của nó; chỉ hai đầu đường có bậc lẻ. Vậy đường đi Euler bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia: 1, 2.
  - **Câu hỏi:** Đồ thị liên thông G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-4, 2-3, 2-4, 2-5, 2-6, 3-5, 3-6, 4-5, 4-6, 5-6. G có đường đi Euler nhưng không có chu trình Euler. Mọi đường đi Euler của G phải bắt đầu ở một trong hai đỉnh nào? Nhập hai đỉnh đó.
  - **Đáp án:** 2, 3  (thứ tự nào cũng được)
    1. Bậc của các đỉnh 1, ..., 6: 2, 5, 3, 4, 4, 4.
    2. Có đúng hai đỉnh bậc lẻ: 2 và 3.
    3. Trên một đường đi Euler, mỗi lần đi qua một đỉnh ở giữa dùng hai cạnh của nó; chỉ hai đầu đường có bậc lẻ. Vậy đường đi Euler bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia: 2, 3.
  - **Câu hỏi:** Đồ thị liên thông G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 1-5, 1-6, 2-5, 4-5, 4-6, 5-6. G có đường đi Euler nhưng không có chu trình Euler. Mọi đường đi Euler của G phải bắt đầu ở một trong hai đỉnh nào? Nhập hai đỉnh đó.
  - **Đáp án:** 3, 6  (thứ tự nào cũng được)
    1. Bậc của các đỉnh 1, ..., 6: 4, 2, 1, 2, 4, 3.
    2. Có đúng hai đỉnh bậc lẻ: 3 và 6.
    3. Trên một đường đi Euler, mỗi lần đi qua một đỉnh ở giữa dùng hai cạnh của nó; chỉ hai đầu đường có bậc lẻ. Vậy đường đi Euler bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia: 3, 6.

### Đồ thị Hamilton (`tr_t6_hamilton`)

- `tr_t6_ha_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu một đồ thị đơn có ít nhất 3 đỉnh có chu trình Hamilton thì mọi đỉnh của nó có bậc ít nhất 2.
  - **Đáp án:** Đúng
    1. Chu trình Hamilton đi qua mọi đỉnh.
    2. Mỗi đỉnh trên chu trình có hai cạnh của chu trình chạm vào nó: một cạnh đi vào, một cạnh đi ra, và hai cạnh này khác nhau khi có ít nhất 3 đỉnh.
    3. Vậy mọi đỉnh có bậc ít nhất 2. Chiều ngược lại thì sai.
- `tr_t6_ha_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điều kiện nào sau đây là đủ để một đồ thị đơn n đỉnh (n >= 3) có chu trình Hamilton (định lý Dirac)?
    - **(đúng)** Mọi đỉnh có bậc ít nhất n/2
    - Mọi đỉnh có bậc chẵn
    - Đồ thị liên thông
    - Mọi đỉnh có bậc ít nhất 2
  - **Đáp án:** Mọi đỉnh có bậc ít nhất n/2
    1. Định lý Dirac: đồ thị đơn n >= 3 đỉnh mà mọi đỉnh có bậc ít nhất n/2 thì có chu trình Hamilton.
    2. Bậc chẵn là điều kiện của chu trình Euler, không phải Hamilton.
    3. Liên thông hay bậc ít nhất 2 không đủ: hai tam giác chung một đỉnh thỏa cả hai mà không có chu trình Hamilton.
- `tr_t6_ha_05` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi mô tả với tên gọi của nó.
  - **Đáp án (ghép đúng):**
    - Đi qua mỗi cạnh đúng một lần và trở về đỉnh xuất phát — chu trình Euler
    - Đi qua mỗi đỉnh đúng một lần và trở về đỉnh xuất phát — chu trình Hamilton
    - Đi qua mỗi cạnh đúng một lần, không cần trở về — đường đi Euler
    - Đi qua mỗi đỉnh đúng một lần, không cần trở về — đường đi Hamilton
  - **Lời giải:**
    1. Euler nói về cạnh: mỗi cạnh dùng đúng một lần.
    2. Hamilton nói về đỉnh: mỗi đỉnh gặp đúng một lần.
    3. Chu trình thì trở về đỉnh xuất phát, đường đi thì không cần.
- `tr_g6_dem_hamilton` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị đầy đủ K_8 có bao nhiêu chu trình Hamilton? Hai chu trình chỉ khác nhau ở đỉnh xuất phát hoặc ở chiều đi được coi là một.
  - **Đáp án:** 2520
    1. Cố định đỉnh xuất phát; thứ tự đi qua 7 đỉnh còn lại là một hoán vị bất kỳ: (8 - 1)! = 5040 cách.
    2. Mỗi chu trình được đếm hai lần, một lần cho mỗi chiều đi.
    3. Số chu trình Hamilton: 5040/2 = 2520.
  - **Câu hỏi:** Đồ thị đầy đủ K_4 có bao nhiêu chu trình Hamilton? Hai chu trình chỉ khác nhau ở đỉnh xuất phát hoặc ở chiều đi được coi là một.
  - **Đáp án:** 3
    1. Cố định đỉnh xuất phát; thứ tự đi qua 3 đỉnh còn lại là một hoán vị bất kỳ: (4 - 1)! = 6 cách.
    2. Mỗi chu trình được đếm hai lần, một lần cho mỗi chiều đi.
    3. Số chu trình Hamilton: 6/2 = 3.
  - **Câu hỏi:** Đồ thị đầy đủ K_8 có bao nhiêu chu trình Hamilton? Hai chu trình chỉ khác nhau ở đỉnh xuất phát hoặc ở chiều đi được coi là một.
  - **Đáp án:** 2520
    1. Cố định đỉnh xuất phát; thứ tự đi qua 7 đỉnh còn lại là một hoán vị bất kỳ: (8 - 1)! = 5040 cách.
    2. Mỗi chu trình được đếm hai lần, một lần cho mỗi chiều đi.
    3. Số chu trình Hamilton: 5040/2 = 2520.
- `tr_t6_ha_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có các đỉnh 1, 2, ..., 6 và các cạnh 1-2, 2-3, 3-4, 4-5, 5-6, 6-1; nó có chu trình Hamilton không?
  - **Lời giải đưa ra (có một bước sai):**
    1. Định lý Dirac: đồ thị đơn n >= 3 đỉnh mà mọi đỉnh có bậc ít nhất n/2 thì có chu trình Hamilton.
    2. Ở đây n = 6 và mọi đỉnh có bậc 2, nhỏ hơn 6/2 = 3.
    3. Điều kiện của định lý Dirac không thỏa, nên đồ thị không có chu trình Hamilton.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Điều kiện của định lý Dirac không thỏa, nên đồ thị không có chu trình Hamilton.
  - **Vì sao sai, và bước đúng:**
    1. Định lý Dirac chỉ là điều kiện đủ: không thỏa nó thì chưa kết luận được gì.
    2. Ở đây chính đồ thị là chu trình 1 - 2 - 3 - 4 - 5 - 6 - 1, đi qua mỗi đỉnh đúng một lần.
    3. Vậy đồ thị có chu trình Hamilton.
- `tr_t6_ha_04` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị hai phía đầy đủ K_(3, 3) (hai phần mỗi phần 3 đỉnh, mỗi đỉnh kề mọi đỉnh phần kia) có bao nhiêu chu trình Hamilton? Hai chu trình chỉ khác nhau ở đỉnh xuất phát hoặc ở chiều đi được coi là một.
  - **Đáp án:** 6
    1. Cố định đỉnh xuất phát a_1 ở phần thứ nhất. Chu trình đi xen kẽ hai phần: b, a, b, a, b rồi về a_1.
    2. 3 đỉnh phần thứ hai xếp theo 3! = 6 cách, 2 đỉnh còn lại của phần thứ nhất xếp theo 2! = 2 cách: 12 dãy.
    3. Mỗi chu trình được đếm hai lần (hai chiều đi), nên có 12/2 = 6 chu trình.
- `tr_g6_hamilton` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-2, 1-3, 1-4, 2-3, 2-5, 4-5. Khẳng định: G có chu trình Hamilton.
  - **Đáp án:** Đúng
    1. Chu trình Hamilton đi qua mỗi đỉnh đúng một lần rồi trở về đỉnh đầu.
    2. Chu trình 1 - 3 - 2 - 5 - 4 - 1 đi qua mỗi đỉnh đúng một lần rồi trở về: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-3, 1-4, 2-3, 2-5, 4-5. Khẳng định: G có chu trình Hamilton.
  - **Đáp án:** Đúng
    1. Chu trình Hamilton đi qua mỗi đỉnh đúng một lần rồi trở về đỉnh đầu.
    2. Chu trình 1 - 4 - 5 - 2 - 3 - 1 đi qua mỗi đỉnh đúng một lần rồi trở về: khẳng định đúng.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-3, 1-4, 2-4, 2-5, 3-4, 3-5. Khẳng định: G có chu trình Hamilton.
  - **Đáp án:** Đúng
    1. Chu trình Hamilton đi qua mỗi đỉnh đúng một lần rồi trở về đỉnh đầu.
    2. Chu trình 2 - 5 - 3 - 1 - 4 - 2 đi qua mỗi đỉnh đúng một lần rồi trở về: khẳng định đúng.

## Tầng 7: Cây, liệt kê cây và bài toán tối ưu trên đồ thị

35 dạng câu (25 câu viết tay, 10 bộ sinh câu); 35 chưa duyệt.

### Cây và tính chất của cây (`tr_t7_cay`)

- `tr_t7_cay_01` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** G là một đồ thị đơn vô hướng có n đỉnh (n >= 2). Điều kiện nào dưới đây KHÔNG đủ để kết luận G là một cây?
    - **(đúng)** G có đúng n - 1 cạnh
    - G liên thông và có đúng n - 1 cạnh
    - G không có chu trình và có đúng n - 1 cạnh
    - Giữa hai đỉnh bất kỳ của G có đúng một đường đi
    - G liên thông, và bỏ đi bất kỳ cạnh nào thì G mất liên thông
  - **Đáp án:** G có đúng n - 1 cạnh
    1. Cây là đồ thị liên thông không có chu trình. Bốn điều kiện cuối đều tương đương với định nghĩa đó (các tính chất tương đương của cây).
    2. Chỉ biết số cạnh là n - 1 thì chưa đủ: ví dụ 4 đỉnh, 3 cạnh 1-2, 2-3, 3-1 và đỉnh 4 đứng riêng. Đồ thị này có chu trình và không liên thông.
    3. Muốn dùng số cạnh n - 1 phải kèm thêm 'liên thông' hoặc 'không có chu trình'.
- `tr_t7_cay_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi cây có ít nhất 2 đỉnh đều có ít nhất hai lá (đỉnh bậc 1).
  - **Đáp án:** Đúng
    1. Xét một đường đi dài nhất v_1, v_2, ..., v_k trong cây (k >= 2 vì cây có cạnh).
    2. Nếu v_1 kề thêm một đỉnh w khác v_2: w không nằm trên đường đi (nếu không sẽ có chu trình), nên w, v_1, ..., v_k là đường đi dài hơn, mâu thuẫn.
    3. Vậy v_1 có bậc 1; tương tự v_k có bậc 1. Cây có ít nhất hai lá: khẳng định đúng.
- `tr_t7_cay_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một rừng (đồ thị không có chu trình) có 25 đỉnh và 19 cạnh. Cần thêm ít nhất bao nhiêu cạnh để được một cây có cùng 25 đỉnh đó?
  - **Đáp án:** 5
    1. Mỗi thành phần liên thông của rừng là một cây, nên số cạnh = số đỉnh - số thành phần: 19 = 25 - k, k = 6.
    2. Một cạnh mới nối hai thành phần khác nhau làm số thành phần giảm đúng 1 và không tạo chu trình.
    3. Từ 6 thành phần xuống 1 cần 5 cạnh; kiểm tra: cây 25 đỉnh có 24 = 19 + 5 cạnh.
- `tr_g7_dem_la` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một cây có 2 đỉnh bậc 4, 0 đỉnh bậc 3, 4 đỉnh bậc 2, các đỉnh còn lại đều là lá (bậc 1). Cây có bao nhiêu lá?
  - **Đáp án:** 6
    1. Gọi số lá là L. Cây có 6 + L đỉnh, nên có 6 + L - 1 cạnh.
    2. Tổng các bậc: 4 . 2 + 3 . 0 + 2 . 4 + L = 16 + L.
    3. Định lý bắt tay: 16 + L = 2(6 + L - 1), suy ra L = 6.
    4. Cây có 6 lá và 12 đỉnh; đáp số 6.
  - **Câu hỏi:** Một cây có 2 đỉnh bậc 4, 0 đỉnh bậc 3, 0 đỉnh bậc 2, các đỉnh còn lại đều là lá (bậc 1). Cây có bao nhiêu lá?
  - **Đáp án:** 6
    1. Gọi số lá là L. Cây có 2 + L đỉnh, nên có 2 + L - 1 cạnh.
    2. Tổng các bậc: 4 . 2 + 3 . 0 + 2 . 0 + L = 8 + L.
    3. Định lý bắt tay: 8 + L = 2(2 + L - 1), suy ra L = 6.
    4. Cây có 6 lá và 8 đỉnh; đáp số 6.
  - **Câu hỏi:** Một cây có 1 đỉnh bậc 4, 4 đỉnh bậc 3, 4 đỉnh bậc 2, các đỉnh còn lại đều là lá (bậc 1). Cây có bao nhiêu lá?
  - **Đáp án:** 8
    1. Gọi số lá là L. Cây có 9 + L đỉnh, nên có 9 + L - 1 cạnh.
    2. Tổng các bậc: 4 . 1 + 3 . 4 + 2 . 4 + L = 24 + L.
    3. Định lý bắt tay: 24 + L = 2(9 + L - 1), suy ra L = 8.
    4. Cây có 8 lá và 17 đỉnh; đáp số 8.
- `tr_t7_cay_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh bằng quy nạp theo n: mọi cây có n đỉnh có đúng n - 1 cạnh.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_cay_02`, `tr_t7_cay_01`
  - **Đáp án (thứ tự đúng):**
    1. Với n = 1: cây chỉ có một đỉnh và 0 cạnh, khẳng định đúng.
    2. Giả sử mọi cây có n đỉnh đều có n - 1 cạnh; xét một cây T có n + 1 đỉnh.
    3. Vì T có ít nhất 2 đỉnh nên T có ít nhất hai lá; chọn một lá v.
    4. Bỏ v cùng cạnh duy nhất nối với v, được T' vẫn liên thông và không có chu trình, tức là một cây có n đỉnh.
    5. Theo giả thiết quy nạp T' có n - 1 cạnh, nên T có (n - 1) + 1 = n cạnh.
  - **Lời giải:**
    1. Trước hết là bước cơ sở, rồi phát biểu giả thiết quy nạp và lấy cây n + 1 đỉnh.
    2. Muốn dùng giả thiết phải thu nhỏ T: cần một lá (tính chất 'cây có ít nhất hai lá').
    3. Bỏ lá không làm mất liên thông (lá không nằm giữa đường đi nào) và không tạo chu trình, nên được cây n đỉnh.
    4. Cuối cùng cộng lại cạnh đã bỏ.
- `tr_t7_cay_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị đơn G có 8 đỉnh, 7 cạnh, và bậc của các đỉnh là 3, 2, 2, 2, 2, 1, 1, 1. Có chắc G là một cây không?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_cay_01`, `tr_t7_cay_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Tổng các bậc là 3 + 2 + 2 + 2 + 2 + 1 + 1 + 1 = 14 = 2 . 7, khớp với số cạnh.
    2. Một cây có 8 đỉnh thì có đúng 7 cạnh, và G cũng có 7 cạnh.
    3. Mọi đồ thị n đỉnh có n - 1 cạnh đều là cây, nên G là một cây.   **<- bước sai đầu tiên**
    4. Vậy G liên thông, và G có đúng 3 lá.
  - **Đáp án:** Bước 3: Mọi đồ thị n đỉnh có n - 1 cạnh đều là cây, nên G là một cây.
  - **Vì sao sai, và bước đúng:**
    1. Hai bước đầu đúng. Bước 3 sai: n - 1 cạnh chỉ cho cây khi đồ thị còn liên thông (hoặc không có chu trình).
    2. Phản ví dụ có đúng dãy bậc đó: tam giác 1-2, 2-3, 3-1 cùng với 4-5, 4-6, 4-7, 5-8. Đỉnh 4 bậc 3; các đỉnh 1, 2, 3, 5 bậc 2; các đỉnh 6, 7, 8 bậc 1.
    3. Đồ thị này có 7 cạnh, có chu trình 1-2-3 và có 2 thành phần liên thông, nên không phải cây. Câu trả lời đúng: không chắc.

### Cây khung và liệt kê cây (`tr_t7_cay_khung`)

- `tr_t7_ck_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 5; các cạnh: 1-2, 1-3, 2-3, 3-4, 3-5, 4-5 (hai tam giác chung đỉnh 3). G có bao nhiêu cây khung?
  - **Đáp án:** 9
    1. Một cây khung có 4 cạnh, tức là bỏ 2 trong 6 cạnh, và không được còn chu trình nào.
    2. Hai chu trình 1-2-3 và 3-4-5 không có cạnh chung, nên phải bỏ đúng một cạnh của mỗi tam giác.
    3. Bỏ một cạnh của tam giác thứ nhất: 3 cách; của tam giác thứ hai: 3 cách. Phần còn lại vẫn liên thông qua đỉnh 3.
    4. Theo quy tắc nhân: 3 . 3 = 9 cây khung.
- `tr_t7_ck_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 2-4, 3-4, 3-5, 4-6, 5-6. Chạy BFS từ đỉnh 1, thăm các đỉnh kề theo thứ tự số tăng dần; cây khung BFS gồm các cạnh nối mỗi đỉnh với đỉnh đã đưa nó vào hàng đợi. Khẳng định: cây khung BFS chứa cạnh 3-4.
  - **Đáp án:** Sai
    1. Từ 1: đưa 2 và 3 vào hàng đợi (cạnh 1-2, 1-3).
    2. Lấy 2 ra: đỉnh kề chưa thăm là 4, đưa vào (cạnh 2-4). Lấy 3 ra: 4 đã thăm, đưa 5 vào (cạnh 3-5).
    3. Lấy 4 ra: đưa 6 vào (cạnh 4-6). Cây khung BFS: 1-2, 1-3, 2-4, 3-5, 4-6, đủ 5 cạnh cho 6 đỉnh.
    4. Đỉnh 4 được đưa vào từ 2 chứ không từ 3, nên cạnh 3-4 không thuộc cây: khẳng định sai.
- `tr_t7_ck_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi đồ thị với số cây khung của nó.
  - **Đáp án (ghép đúng):**
    - Đồ thị đầy đủ K_4 — 16
    - Chu trình 7 đỉnh C_7 — 7
    - Đồ thị hai phía đầy đủ K_(2, 3) — 12
    - Một cây bất kỳ có 6 đỉnh — 1
    - K_4 bỏ đi một cạnh — 8
  - **Lời giải:**
    1. K_n có n^(n - 2) cây khung (công thức Cayley): K_4 có 4^2 = 16.
    2. Chu trình n đỉnh: bỏ đúng một trong n cạnh, được n cây khung; C_7 có 7.
    3. K_(2, 3): định lý Kirchhoff (hay công thức m^(n - 1) n^(m - 1) với m = 2, n = 3) cho 2^2 . 3^1 = 12.
    4. Một cây chỉ có chính nó là cây khung: 1.
    5. K_4 có 16 cây khung, mỗi cạnh nằm trong 16 . 3/6 = 8 cây (mỗi cây có 3 trong 6 cạnh, các cạnh như nhau), nên bỏ một cạnh còn 16 - 8 = 8.
- `tr_g7_xoa_canh` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-3, 2-4, 2-5, 2-6, 4-5, 4-6, 5-6. Cần xóa ít nhất bao nhiêu cạnh để G không còn chu trình mà số thành phần liên thông không đổi (tức là còn lại một rừng khung của G)?
  - **Đáp án:** 3
    1. G có 7 cạnh. Các thành phần liên thông: {1, 3}; {2, 4, 5, 6}; {7}, tức k = 3.
    2. Rừng khung giữ mỗi thành phần n_i đỉnh bằng một cây n_i - 1 cạnh, nên có 7 - 3 = 4 cạnh.
    3. Phải xóa 7 - 4 = 3 cạnh (số này gọi là số chu trình độc lập của G).
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-2, 1-5, 1-7, 2-3, 2-6, 2-7, 4-5, 4-7, 5-6, 6-7. Cần xóa ít nhất bao nhiêu cạnh để G không còn chu trình mà số thành phần liên thông không đổi (tức là còn lại một rừng khung của G)?
  - **Đáp án:** 4
    1. G có 10 cạnh. Các thành phần liên thông: {1, 2, 3, 4, 5, 6, 7}, tức k = 1.
    2. Rừng khung giữ mỗi thành phần n_i đỉnh bằng một cây n_i - 1 cạnh, nên có 7 - 1 = 6 cạnh.
    3. Phải xóa 10 - 6 = 4 cạnh (số này gọi là số chu trình độc lập của G).
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh: 1-3, 1-4, 1-7, 2-5, 3-4, 3-7, 4-7. Cần xóa ít nhất bao nhiêu cạnh để G không còn chu trình mà số thành phần liên thông không đổi (tức là còn lại một rừng khung của G)?
  - **Đáp án:** 3
    1. G có 7 cạnh. Các thành phần liên thông: {1, 3, 4, 7}; {2, 5}; {6}, tức k = 3.
    2. Rừng khung giữ mỗi thành phần n_i đỉnh bằng một cây n_i - 1 cạnh, nên có 7 - 3 = 4 cạnh.
    3. Phải xóa 7 - 4 = 3 cạnh (số này gọi là số chu trình độc lập của G).
- `tr_t7_ck_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 1-3, 2-3, 2-4, 3-4, 4-5, 4-6, 5-6.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_ck_01`, `tr_g7_xoa_canh`, `tr_t7_ck_02`
  - **Phần a** (Điền số): a) Phải xóa ít nhất bao nhiêu cạnh của G để còn lại một cây khung?
    - **Đáp án a:** 3
  - **Phần b** (Đúng/Sai): b) Cây khung tạo bởi DFS từ đỉnh 1 (thăm các đỉnh kề theo thứ tự số tăng dần) chứa cạnh 3-4.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) G có tất cả bao nhiêu cây khung?
    - **Đáp án c:** 24
  - **Lời giải:**
    1. a) G liên thông, có 6 đỉnh và 8 cạnh; cây khung có 5 cạnh, nên phải xóa 8 - 5 = 3 cạnh.
    2. b) DFS từ 1: sang 2, từ 2 sang 3 (đỉnh kề nhỏ nhất chưa thăm), từ 3 sang 4, từ 4 sang 5, từ 5 sang 6. Cây DFS: 1-2, 2-3, 3-4, 4-5, 5-6, có cạnh 3-4: đúng.
    3. c) Đỉnh 4 tách G thành phần trái (các đỉnh 1, 2, 3, 4 với 5 cạnh 1-2, 1-3, 2-3, 2-4, 3-4, tức K_4 bỏ cạnh 1-4) và tam giác 4-5-6. Một cây khung của G là một cây khung của phần trái ghép với một cây khung của tam giác.
    4. Phần trái có 8 cây khung (K_4 bỏ một cạnh), tam giác có 3, nên G có 8 . 3 = 24 cây khung (khớp với định lý Kirchhoff).
- `tr_t7_ck_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** K_5 là đồ thị đầy đủ 5 đỉnh. Bỏ đi một cạnh của K_5 thì đồ thị còn lại có bao nhiêu cây khung?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_ck_03`, `tr_t7_ck_01`
  - **Đáp án:** 75
    1. Theo công thức Cayley, K_5 có 5^3 = 125 cây khung.
    2. Mỗi cây khung có 4 cạnh trong 10 cạnh của K_5; do mọi cạnh có vai trò như nhau, mỗi cạnh nằm trong 125 . 4/10 = 50 cây khung.
    3. Bỏ cạnh e đi thì mất đúng những cây chứa e: còn 125 - 50 = 75 cây khung.
    4. Kiểm tra bằng định lý Kirchhoff: định thức của ma trận Laplace bỏ một hàng một cột bằng 75.
- `tr_g7_dem_cay_khung` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 4; các cạnh: 1-2, 1-3, 1-4, 2-3, 2-4. G có bao nhiêu cây khung khác nhau (hai cây khác nhau khi tập cạnh khác nhau)?
  - **Đáp án:** 8
    1. Một cây khung có 3 cạnh, tức là giữ 3 trong 5 cạnh và bỏ 2 cạnh.
    2. Có C_5^2 = 10 cách bỏ 2 cạnh. Cách bỏ nào để lại một chu trình (khi đó phần còn lại cũng không liên thông) thì không cho cây.
    3. Kiểm tra từng cách: 2 cách để lại chu trình, còn 8 cách để lại một cây.
    4. G có 8 cây khung (kiểm tra lại bằng định lý Kirchhoff: định thức của ma trận Laplace bỏ một hàng một cột).
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 4; các cạnh: 1-2, 1-3, 2-3, 2-4, 3-4. G có bao nhiêu cây khung khác nhau (hai cây khác nhau khi tập cạnh khác nhau)?
  - **Đáp án:** 8
    1. Một cây khung có 3 cạnh, tức là giữ 3 trong 5 cạnh và bỏ 2 cạnh.
    2. Có C_5^2 = 10 cách bỏ 2 cạnh. Cách bỏ nào để lại một chu trình (khi đó phần còn lại cũng không liên thông) thì không cho cây.
    3. Kiểm tra từng cách: 2 cách để lại chu trình, còn 8 cách để lại một cây.
    4. G có 8 cây khung (kiểm tra lại bằng định lý Kirchhoff: định thức của ma trận Laplace bỏ một hàng một cột).
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 4; các cạnh: 1-2, 1-3, 1-4, 2-3, 2-4. G có bao nhiêu cây khung khác nhau (hai cây khác nhau khi tập cạnh khác nhau)?
  - **Đáp án:** 8
    1. Một cây khung có 3 cạnh, tức là giữ 3 trong 5 cạnh và bỏ 2 cạnh.
    2. Có C_5^2 = 10 cách bỏ 2 cạnh. Cách bỏ nào để lại một chu trình (khi đó phần còn lại cũng không liên thông) thì không cho cây.
    3. Kiểm tra từng cách: 2 cách để lại chu trình, còn 8 cách để lại một cây.
    4. G có 8 cây khung (kiểm tra lại bằng định lý Kirchhoff: định thức của ma trận Laplace bỏ một hàng một cột).

### Cây khung nhỏ nhất (`tr_t7_kruskal_prim`)

- `tr_t7_kp_01` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (6), 1-4 (1), 2-3 (3), 2-4 (4), 3-4 (2), 3-5 (7), 3-6 (9), 4-5 (8), 5-6 (5). Khi chạy thuật toán Kruskal, cạnh đầu tiên bị bỏ (vì tạo chu trình) là cạnh nào?
    - **(đúng)** 2-4 (4)
    - 1-2 (6)
    - 2-3 (3)
    - 3-5 (7)
    - 4-5 (8)
  - **Đáp án:** 2-4 (4)
    1. Xét các cạnh theo trọng số tăng dần: 1-4 (1) nhận; 3-4 (2) nhận; 2-3 (3) nhận.
    2. 2-4 (4): 2 và 4 đã nối với nhau qua 2-3-4, thêm vào sẽ tạo chu trình 2-3-4, nên bỏ. Đây là cạnh đầu tiên bị bỏ.
    3. Tiếp theo 5-6 (5) nhận, 1-2 (6) bỏ, 3-5 (7) nhận: đủ 5 cạnh, tổng trọng số 18.
- `tr_t7_kp_02` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tìm cây khung nhỏ nhất của đồ thị có các đỉnh 1, 2, ..., 5 và các cạnh (trọng số trong ngoặc): 1-2 (1), 2-3 (2), 1-3 (3), 3-4 (4), 4-5 (5), 2-5 (6), 1-5 (7), bằng thuật toán Kruskal.
  - **Lời giải đưa ra (có một bước sai):**
    1. Sắp các cạnh theo trọng số tăng dần: 1-2, 2-3, 1-3, 3-4, 4-5, 2-5, 1-5.
    2. Nhận 1-2 (1) và 2-3 (2) vì chưa tạo chu trình.
    3. Nhận 1-3 (3) vì đỉnh 3 đã có trong cây đang xây.   **<- bước sai đầu tiên**
    4. Nhận 3-4 (4): đã có 4 cạnh, đủ cho 5 đỉnh nên dừng.
    5. Tổng trọng số của cây khung nhỏ nhất là 1 + 2 + 3 + 4 = 10.
  - **Đáp án:** Bước 3: Nhận 1-3 (3) vì đỉnh 3 đã có trong cây đang xây.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: 1 và 3 đã nối với nhau qua 1-2-3, nên cạnh 1-3 khép chu trình 1-2-3 và phải bỏ. Kruskal chỉ nhận cạnh nối hai cây khác nhau của rừng đang xây.
    2. Làm đúng: nhận 1-2, 2-3, bỏ 1-3, nhận 3-4 và 4-5.
    3. Cây khung nhỏ nhất là 1-2, 2-3, 3-4, 4-5 với tổng trọng số 1 + 2 + 4 + 5 = 12 (bốn cạnh ở bước 3-4 của lời giải sai còn để đỉnh 5 ở ngoài).
- `tr_t7_kp_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu G là đồ thị vô hướng liên thông và các cạnh của G có trọng số đôi một khác nhau, thì G có đúng một cây khung nhỏ nhất, và Kruskal cũng như Prim (từ bất kỳ đỉnh nào) đều cho ra cây đó.
  - **Đáp án:** Đúng
    1. Giả sử có hai cây khung nhỏ nhất khác nhau T_1, T_2; gọi e là cạnh nhẹ nhất thuộc đúng một trong hai cây, chẳng hạn e thuộc T_1.
    2. Thêm e vào T_2 tạo một chu trình; chu trình có cạnh f không thuộc T_1, và w(f) > w(e) vì e nhẹ nhất trong các cạnh khác nhau (các trọng số đôi một khác nhau).
    3. T_2 + e - f là cây khung nhẹ hơn T_2, mâu thuẫn. Vậy cây khung nhỏ nhất là duy nhất.
    4. Kruskal và Prim đều cho một cây khung nhỏ nhất, nên cho đúng cây duy nhất đó: khẳng định đúng.
- `tr_g7_kruskal_tong` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (13), 1-3 (14), 1-4 (1), 2-4 (15), 2-5 (9), 2-6 (12), 3-6 (20), 4-5 (4). Cây khung nhỏ nhất của G có tổng trọng số bằng bao nhiêu?
  - **Đáp án:** 40
    1. Thuật toán Kruskal: xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình với các cạnh đã nhận, dừng khi đủ 5 cạnh.
    2. 1-4 (1): nhận; 4-5 (4): nhận; 2-5 (9): nhận; 2-6 (12): nhận; 1-2 (13): bỏ, vì 1 và 2 đã nối với nhau, thêm vào sẽ tạo chu trình; 1-3 (14): nhận.
    3. Cây khung nhỏ nhất: 1-4, 4-5, 2-5, 2-6, 1-3; tổng trọng số 1 + 4 + 9 + 12 + 14 = 40.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-4 (17), 1-6 (12), 2-4 (18), 2-6 (15), 3-5 (9), 3-6 (20), 4-5 (1), 4-6 (14). Cây khung nhỏ nhất của G có tổng trọng số bằng bao nhiêu?
  - **Đáp án:** 51
    1. Thuật toán Kruskal: xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình với các cạnh đã nhận, dừng khi đủ 5 cạnh.
    2. 4-5 (1): nhận; 3-5 (9): nhận; 1-6 (12): nhận; 4-6 (14): nhận; 2-6 (15): nhận.
    3. Cây khung nhỏ nhất: 4-5, 3-5, 1-6, 4-6, 2-6; tổng trọng số 1 + 9 + 12 + 14 + 15 = 51.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-3 (18), 1-4 (20), 2-3 (16), 2-4 (13), 3-5 (5), 4-5 (4), 4-6 (11), 5-6 (3). Cây khung nhỏ nhất của G có tổng trọng số bằng bao nhiêu?
  - **Đáp án:** 43
    1. Thuật toán Kruskal: xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình với các cạnh đã nhận, dừng khi đủ 5 cạnh.
    2. 5-6 (3): nhận; 4-5 (4): nhận; 3-5 (5): nhận; 4-6 (11): bỏ, vì 4 và 6 đã nối với nhau, thêm vào sẽ tạo chu trình; 2-4 (13): nhận; 2-3 (16): bỏ, vì 2 và 3 đã nối với nhau, thêm vào sẽ tạo chu trình; 1-3 (18): nhận.
    3. Cây khung nhỏ nhất: 5-6, 4-5, 3-5, 2-4, 1-3; tổng trọng số 3 + 4 + 5 + 13 + 18 = 43.
- `tr_t7_kp_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (4), 1-3 (2), 2-3 (5), 2-4 (10), 3-4 (9), 3-5 (3), 4-5 (7), 4-6 (6), 5-6 (8). Chạy thuật toán Kruskal trên G.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_kp_01`, `tr_g7_kruskal_tong`
  - **Phần a** (Điền số): a) Tổng trọng số của cây khung nhỏ nhất bằng bao nhiêu?
    - **Đáp án a:** 22
  - **Phần b** (Điền số): b) Cạnh được nhận cuối cùng có trọng số bao nhiêu?
    - **Đáp án b:** 7
  - **Phần c** (Điền số): c) Trước khi dừng, Kruskal đã bỏ bao nhiêu cạnh vì chúng tạo chu trình?
    - **Đáp án c:** 1
  - **Phần d** (Đúng/Sai): d) Cạnh 3-4 (9) thuộc cây khung nhỏ nhất.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. Theo trọng số tăng dần: 1-3 (2) nhận; 3-5 (3) nhận; 1-2 (4) nhận; 2-3 (5) bỏ vì 2 và 3 đã nối qua 1; 4-6 (6) nhận; 4-5 (7) nhận. Đã đủ 5 cạnh nên dừng.
    2. a) Tổng 2 + 3 + 4 + 6 + 7 = 22.
    3. b) Cạnh nhận cuối là 4-5 (7).
    4. c) Chỉ một cạnh bị bỏ: 2-3 (5); các cạnh 5-6, 3-4, 2-4 nặng hơn và không cần xét.
    5. d) 3-4 (9) không có trong cây: sai. Nếu thêm 3-4 vào cây, chu trình 3-4-5 cho thấy nó nặng hơn 3-5 (3) và 4-5 (7).
- `tr_t7_kp_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh thuật toán Kruskal cho cây khung nhỏ nhất (trọng số đôi một khác nhau).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_kp_03`, `tr_t7_kp_02`
  - **Đáp án (thứ tự đúng):**
    1. Gọi T là cây Kruskal tạo ra; giả sử T không nhỏ nhất, chọn một cây khung nhỏ nhất T* có nhiều cạnh chung với T nhất.
    2. Gọi e là cạnh đầu tiên (theo thứ tự Kruskal nhận) thuộc T mà không thuộc T*.
    3. Thêm e vào T* được đúng một chu trình; trên chu trình đó có một cạnh f không thuộc T.
    4. Các cạnh Kruskal nhận trước e đều thuộc T*, cùng với f chúng không tạo chu trình; nếu w(f) < w(e) thì Kruskal đã nhận f trước e, vô lý, nên w(f) > w(e).
    5. T* + e - f là cây khung nhẹ hơn T*, mâu thuẫn với T* nhỏ nhất; vậy T là cây khung nhỏ nhất.
  - **Lời giải:**
    1. Đây là chứng minh bằng phản chứng và trao đổi cạnh.
    2. Phải có T* trước để chọn e, có e mới có chu trình trong T* + e và cạnh f.
    3. So sánh w(f) với w(e) dựa vào cách Kruskal chọn cạnh, rồi trao đổi e lấy f để ra mâu thuẫn.
- `tr_t7_kp_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (7), 1-3 (3), 2-3 (6), 2-4 (2), 3-4 (8), 3-5 (4), 4-5 (10), 4-6 (5), 5-6 (9). Chạy thuật toán Prim từ đỉnh 1. Nhập các đỉnh theo thứ tự chúng được đưa vào cây, bắt đầu bằng 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_kp_01`, `tr_g7_kruskal_tong`
  - **Đáp án:** 1, 3, 5, 2, 4, 6
    1. Cây = {1}. Các cạnh ra ngoài: 1-2 (7), 1-3 (3); nhẹ nhất 1-3, thêm 3.
    2. Cây = {1, 3}: ứng viên 1-2 (7), 2-3 (6), 3-4 (8), 3-5 (4); thêm 5 qua 3-5.
    3. Cây = {1, 3, 5}: ứng viên 1-2 (7), 2-3 (6), 3-4 (8), 4-5 (10), 5-6 (9); thêm 2 qua 2-3.
    4. Cây = {1, 2, 3, 5}: ứng viên 2-4 (2), 5-6 (9), ...; thêm 4 qua 2-4. Rồi 4-6 (5) đưa 6 vào.
    5. Thứ tự: 1, 3, 5, 2, 4, 6; tổng trọng số 3 + 4 + 6 + 2 + 5 = 20, đúng bằng cây Kruskal.
- `tr_g7_kruskal_cuoi` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh (trọng số trong ngoặc): 1-6 (14), 2-4 (20), 2-7 (1), 3-4 (15), 4-5 (9), 4-6 (8), 4-7 (19), 5-7 (4), 6-7 (11). Chạy thuật toán Kruskal trên G. Nhập hai số: tổng trọng số của cây khung nhỏ nhất, rồi trọng số của cạnh được nhận cuối cùng.
  - **Đáp án:** 51, 15
    1. Xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình, dừng khi đủ 6 cạnh.
    2. 2-7 (1): nhận; 5-7 (4): nhận; 4-6 (8): nhận; 4-5 (9): nhận; 6-7 (11): bỏ, vì 6 và 7 đã nối với nhau, thêm vào sẽ tạo chu trình; 1-6 (14): nhận; 3-4 (15): nhận.
    3. Đã bỏ 1 cạnh. Cây: 2-7, 5-7, 4-6, 4-5, 1-6, 3-4; tổng 1 + 4 + 8 + 9 + 14 + 15 = 51.
    4. Cạnh nhận cuối cùng là 3-4 (15), cũng là cạnh nặng nhất của cây. Đáp số: 51, 15.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh (trọng số trong ngoặc): 1-4 (13), 1-7 (24), 2-4 (17), 2-5 (12), 3-5 (18), 3-6 (15), 3-7 (23), 4-6 (9), 5-6 (2). Chạy thuật toán Kruskal trên G. Nhập hai số: tổng trọng số của cây khung nhỏ nhất, rồi trọng số của cạnh được nhận cuối cùng.
  - **Đáp án:** 74, 23
    1. Xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình, dừng khi đủ 6 cạnh.
    2. 5-6 (2): nhận; 4-6 (9): nhận; 2-5 (12): nhận; 1-4 (13): nhận; 3-6 (15): nhận; 2-4 (17): bỏ, vì 2 và 4 đã nối với nhau, thêm vào sẽ tạo chu trình; 3-5 (18): bỏ, vì 3 và 5 đã nối với nhau, thêm vào sẽ tạo chu trình; 3-7 (23): nhận.
    3. Đã bỏ 2 cạnh. Cây: 5-6, 4-6, 2-5, 1-4, 3-6, 3-7; tổng 2 + 9 + 12 + 13 + 15 + 23 = 74.
    4. Cạnh nhận cuối cùng là 3-7 (23), cũng là cạnh nặng nhất của cây. Đáp số: 74, 23.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 7; các cạnh (trọng số trong ngoặc): 1-4 (18), 1-6 (25), 1-7 (16), 2-4 (13), 2-7 (21), 3-4 (5), 3-6 (8), 4-6 (20), 5-6 (17). Chạy thuật toán Kruskal trên G. Nhập hai số: tổng trọng số của cây khung nhỏ nhất, rồi trọng số của cạnh được nhận cuối cùng.
  - **Đáp án:** 77, 18
    1. Xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình, dừng khi đủ 6 cạnh.
    2. 3-4 (5): nhận; 3-6 (8): nhận; 2-4 (13): nhận; 1-7 (16): nhận; 5-6 (17): nhận; 1-4 (18): nhận.
    3. Đã bỏ 0 cạnh. Cây: 3-4, 3-6, 2-4, 1-7, 5-6, 1-4; tổng 5 + 8 + 13 + 16 + 17 + 18 = 77.
    4. Cạnh nhận cuối cùng là 1-4 (18), cũng là cạnh nặng nhất của cây. Đáp số: 77, 18.
- `tr_g7_prim` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (13), 1-3 (14), 1-4 (1), 2-4 (15), 2-5 (9), 2-6 (12), 3-6 (20), 4-5 (4). Chạy thuật toán Prim từ đỉnh 5. Nhập các đỉnh theo thứ tự chúng được đưa vào cây, bắt đầu bằng 5.
  - **Đáp án:** 5, 4, 1, 2, 6, 3
    1. Bắt đầu với cây chỉ có đỉnh 5. Mỗi bước thêm cạnh nhẹ nhất nối một đỉnh trong cây với một đỉnh ngoài cây.
    2. thêm 4 qua cạnh 5-4 (4); thêm 1 qua cạnh 4-1 (1); thêm 2 qua cạnh 5-2 (9); thêm 6 qua cạnh 2-6 (12); thêm 3 qua cạnh 1-3 (14).
    3. Thứ tự các đỉnh được thêm: 5, 4, 1, 2, 6, 3; tổng trọng số 40.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-4 (17), 1-6 (12), 2-4 (18), 2-6 (15), 3-5 (9), 3-6 (20), 4-5 (1), 4-6 (14). Chạy thuật toán Prim từ đỉnh 3. Nhập các đỉnh theo thứ tự chúng được đưa vào cây, bắt đầu bằng 3.
  - **Đáp án:** 3, 5, 4, 6, 1, 2
    1. Bắt đầu với cây chỉ có đỉnh 3. Mỗi bước thêm cạnh nhẹ nhất nối một đỉnh trong cây với một đỉnh ngoài cây.
    2. thêm 5 qua cạnh 3-5 (9); thêm 4 qua cạnh 5-4 (1); thêm 6 qua cạnh 4-6 (14); thêm 1 qua cạnh 6-1 (12); thêm 2 qua cạnh 6-2 (15).
    3. Thứ tự các đỉnh được thêm: 3, 5, 4, 6, 1, 2; tổng trọng số 51.
  - **Câu hỏi:** Đồ thị G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-3 (18), 1-4 (20), 2-3 (16), 2-4 (13), 3-5 (5), 4-5 (4), 4-6 (11), 5-6 (3). Chạy thuật toán Prim từ đỉnh 5. Nhập các đỉnh theo thứ tự chúng được đưa vào cây, bắt đầu bằng 5.
  - **Đáp án:** 5, 6, 4, 3, 2, 1
    1. Bắt đầu với cây chỉ có đỉnh 5. Mỗi bước thêm cạnh nhẹ nhất nối một đỉnh trong cây với một đỉnh ngoài cây.
    2. thêm 6 qua cạnh 5-6 (3); thêm 4 qua cạnh 5-4 (4); thêm 3 qua cạnh 5-3 (5); thêm 2 qua cạnh 4-2 (13); thêm 1 qua cạnh 3-1 (18).
    3. Thứ tự các đỉnh được thêm: 5, 6, 4, 3, 2, 1; tổng trọng số 43.

### Đường đi ngắn nhất (`tr_t7_dijkstra`)

- `tr_t7_dj_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (7), 1-3 (2), 2-3 (4), 2-4 (1), 3-4 (8), 3-5 (10), 4-5 (3), 4-6 (9), 5-6 (2). Độ dài đường đi ngắn nhất từ đỉnh 1 đến đỉnh 6 bằng bao nhiêu?
  - **Đáp án:** 12
    1. Dijkstra từ 1: cố định 1 (0); nhãn 2: 7, 3: 2.
    2. Cố định 3 (2): nhãn 2 giảm còn 2 + 4 = 6, 4: 10, 5: 12. Cố định 2 (6): nhãn 4 giảm còn 7.
    3. Cố định 4 (7): nhãn 5 giảm còn 10, 6: 16. Cố định 5 (10): nhãn 6 giảm còn 12. Cố định 6 (12).
    4. Đường đi ngắn nhất 1 - 3 - 2 - 4 - 5 - 6, độ dài 2 + 4 + 1 + 3 + 2 = 12.
- `tr_t7_dj_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (5), 1-3 (1), 2-3 (3), 2-4 (2), 2-5 (6), 3-4 (7), 4-5 (5), 4-6 (3), 5-6 (1). Chạy thuật toán Dijkstra từ đỉnh 1. Các đỉnh được cố định nhãn theo thứ tự nào?
    - **(đúng)** 1, 3, 2, 4, 6, 5
    - 1, 3, 2, 4, 5, 6
    - 1, 2, 3, 4, 5, 6
    - 1, 3, 4, 2, 6, 5
  - **Đáp án:** 1, 3, 2, 4, 6, 5
    1. Cố định 1 (0): nhãn 2: 5, 3: 1. Cố định 3 (1): nhãn 2 giảm còn 4, 4: 8.
    2. Cố định 2 (4): nhãn 4 giảm còn 6, 5: 10. Cố định 4 (6): nhãn 6: 9, nhãn 5 giữ 10 (vì 6 + 5 = 11).
    3. Cố định 6 (9): nhãn 5 vẫn 10 (9 + 1 = 10 không nhỏ hơn). Cố định 5 (10).
    4. Thứ tự: 1, 3, 2, 4, 6, 5. Đỉnh được cố định theo nhãn tăng dần, không theo số thứ tự của đỉnh.
- `tr_t7_dj_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho đồ thị vô hướng có trọng số dương. Nếu cộng cùng một số c > 0 vào trọng số của mọi cạnh, thì đường đi ngắn nhất giữa hai đỉnh s, t bất kỳ vẫn là đường đi ngắn nhất cũ.
  - **Đáp án:** Sai
    1. Cộng c vào mọi cạnh làm một đường đi k cạnh dài thêm k . c: đường nhiều cạnh bị phạt nặng hơn.
    2. Phản ví dụ: các cạnh 1-2 (1), 2-3 (1), 1-3 (3). Đường ngắn nhất từ 1 đến 3 là 1-2-3 với độ dài 2.
    3. Cộng c = 2: 1-2-3 dài 3 + 3 = 6, còn 1-3 dài 5. Đường ngắn nhất đổi thành 1-3: khẳng định sai.
- `tr_g7_dijkstra` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (15), 1-3 (14), 1-4 (7), 2-4 (13), 2-5 (10), 2-6 (1), 3-6 (8), 4-5 (5). Độ dài đường đi ngắn nhất từ đỉnh 1 đến đỉnh 5 bằng bao nhiêu?
  - **Đáp án:** 12
    1. Thuật toán Dijkstra từ đỉnh 1: mỗi bước cố định đỉnh chưa cố định có nhãn nhỏ nhất, rồi giảm nhãn các đỉnh kề nó.
    2. Thứ tự cố định và nhãn cuối: 1 (0), 4 (7), 5 (12), 3 (14), 2 (15), 6 (16).
    3. Đường đi ngắn nhất: 1 - 4 - 5, độ dài 12.
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-4 (13), 1-6 (12), 2-4 (9), 2-6 (6), 3-5 (15), 3-6 (8), 4-5 (11), 4-6 (5). Độ dài đường đi ngắn nhất từ đỉnh 1 đến đỉnh 2 bằng bao nhiêu?
  - **Đáp án:** 18
    1. Thuật toán Dijkstra từ đỉnh 1: mỗi bước cố định đỉnh chưa cố định có nhãn nhỏ nhất, rồi giảm nhãn các đỉnh kề nó.
    2. Thứ tự cố định và nhãn cuối: 1 (0), 6 (12), 4 (13), 2 (18), 3 (20), 5 (24).
    3. Đường đi ngắn nhất: 1 - 6 - 2, độ dài 18.
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-3 (9), 1-4 (14), 2-3 (15), 2-4 (8), 3-5 (7), 4-5 (3), 4-6 (4), 5-6 (10). Độ dài đường đi ngắn nhất từ đỉnh 1 đến đỉnh 6 bằng bao nhiêu?
  - **Đáp án:** 18
    1. Thuật toán Dijkstra từ đỉnh 1: mỗi bước cố định đỉnh chưa cố định có nhãn nhỏ nhất, rồi giảm nhãn các đỉnh kề nó.
    2. Thứ tự cố định và nhãn cuối: 1 (0), 3 (9), 4 (14), 5 (16), 6 (18), 2 (22).
    3. Đường đi ngắn nhất: 1 - 4 - 6, độ dài 18.
- `tr_t7_dj_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: đồ thị có hướng có các cung (trọng số trong ngoặc): 1->2 (2), 1->3 (4), 3->2 (-4), 2->4 (3). Tìm độ dài đường đi ngắn nhất từ 1 đến 4; một đệ tử dùng cách làm của Dijkstra.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_dj_02`, `tr_t7_dj_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Khởi tạo d(1) = 0, các nhãn khác bằng vô cùng.
    2. Cố định 1; cập nhật d(2) = 2 và d(3) = 4.
    3. Nhãn 2 nhỏ nhất, và vì đi qua một đỉnh khác chỉ làm đường dài thêm, nhãn 2 không thể giảm nữa: cố định d(2) = 2.   **<- bước sai đầu tiên**
    4. Từ 2 cập nhật d(4) = 2 + 3 = 5, rồi cố định 3 và 4.
    5. Kết luận: đường đi ngắn nhất từ 1 đến 4 dài 5.
  - **Đáp án:** Bước 3: Nhãn 2 nhỏ nhất, và vì đi qua một đỉnh khác chỉ làm đường dài thêm, nhãn 2 không thể giảm nữa: cố định d(2) = 2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: lý lẽ 'đi qua đỉnh khác chỉ làm đường dài thêm' chỉ đúng khi mọi trọng số không âm, mà cung 3->2 có trọng số -4.
    2. Thật vậy 1->3->2 dài 4 + (-4) = 0 < 2, nên d(2) = 0 chứ không phải 2.
    3. Đường ngắn nhất đến 4 là 1->3->2->4, dài 0 + 3 = 3, không phải 5. Khi có trọng số âm phải dùng thuật toán khác, ví dụ Bellman-Ford.
- `tr_t7_dj_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (3), 1-3 (9), 2-3 (4), 2-4 (8), 3-4 (6), 3-5 (2), 4-5 (5), 4-6 (4), 5-6 (7). Chạy thuật toán Dijkstra từ đỉnh 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t6_bfs_02`, `tr_t7_dj_01`, `tr_g7_dijkstra`
  - **Phần a** (Điền số): a) Khoảng cách từ 1 đến 6 bằng bao nhiêu?
    - **Đáp án a:** 15
  - **Phần b** (Điền số): b) Trên đường đi ngắn nhất từ 1 đến 6, đỉnh đứng ngay trước 6 là đỉnh nào?
    - **Đáp án b:** 4
  - **Phần c** (Đúng/Sai): c) Đường đi ngắn nhất từ 1 đến 6 đi qua đỉnh 3.
    - **Đáp án c:** Sai
  - **Lời giải:**
    1. Cố định 1 (0); nhãn 2: 3, 3: 9. Cố định 2 (3): nhãn 3 giảm còn 7, 4: 11.
    2. Cố định 3 (7): nhãn 5: 9, nhãn 4 giữ 11 (7 + 6 = 13). Cố định 5 (9): nhãn 6: 16, nhãn 4 giữ 11 (9 + 5 = 14).
    3. Cố định 4 (11): nhãn 6 giảm còn 15, trước(6) = 4. Cố định 6 (15).
    4. a) 15. b) Lần ngược: trước(6) = 4, trước(4) = 2, trước(2) = 1, đường đi 1 - 2 - 4 - 6; đỉnh trước 6 là 4.
    5. c) Đường 1 - 2 - 4 - 6 không qua 3 (đường qua 3 ngắn nhất là 1 - 2 - 3 - 5 - 6, dài 16): sai.
- `tr_g7_dijkstra_moi` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-2 (15), 1-3 (14), 1-4 (7), 2-4 (13), 2-5 (10), 2-6 (1), 3-6 (8), 4-5 (5). Tìm khoảng cách (độ dài đường đi ngắn nhất) từ đỉnh 6 đến các đỉnh 1, 2, 3, 4, 5; nhập theo đúng thứ tự đó.
  - **Đáp án:** 16, 1, 8, 14, 11
    1. Chạy Dijkstra từ 6; trọng số đều dương nên nhãn của một đỉnh đã cố định là khoảng cách đúng.
    2. Thứ tự cố định và nhãn: 6 (0), 2 (1), 3 (8), 5 (11), 4 (14), 1 (16).
    3. Đường đi: đến 1: 6 - 2 - 1; đến 2: 6 - 2; đến 3: 6 - 3; đến 4: 6 - 2 - 4; đến 5: 6 - 2 - 5.
    4. Đáp số: 16, 1, 8, 14, 11.
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-4 (13), 1-6 (12), 2-4 (9), 2-6 (6), 3-5 (15), 3-6 (8), 4-5 (11), 4-6 (5). Tìm khoảng cách (độ dài đường đi ngắn nhất) từ đỉnh 1 đến các đỉnh 2, 3, 4, 5, 6; nhập theo đúng thứ tự đó.
  - **Đáp án:** 18, 20, 13, 24, 12
    1. Chạy Dijkstra từ 1; trọng số đều dương nên nhãn của một đỉnh đã cố định là khoảng cách đúng.
    2. Thứ tự cố định và nhãn: 1 (0), 6 (12), 4 (13), 2 (18), 3 (20), 5 (24).
    3. Đường đi: đến 2: 1 - 6 - 2; đến 3: 1 - 6 - 3; đến 4: 1 - 4; đến 5: 1 - 4 - 5; đến 6: 1 - 6.
    4. Đáp số: 18, 20, 13, 24, 12.
  - **Câu hỏi:** Đồ thị vô hướng G có các đỉnh 1, 2, ..., 6; các cạnh (trọng số trong ngoặc): 1-3 (9), 1-4 (14), 2-3 (15), 2-4 (8), 3-5 (7), 4-5 (3), 4-6 (4), 5-6 (10). Tìm khoảng cách (độ dài đường đi ngắn nhất) từ đỉnh 5 đến các đỉnh 1, 2, 3, 4, 6; nhập theo đúng thứ tự đó.
  - **Đáp án:** 16, 11, 7, 3, 7
    1. Chạy Dijkstra từ 5; trọng số đều dương nên nhãn của một đỉnh đã cố định là khoảng cách đúng.
    2. Thứ tự cố định và nhãn: 5 (0), 4 (3), 3 (7), 6 (7), 2 (11), 1 (16).
    3. Đường đi: đến 1: 5 - 3 - 1; đến 2: 5 - 4 - 2; đến 3: 5 - 3; đến 4: 5 - 4; đến 6: 5 - 4 - 6.
    4. Đáp số: 16, 11, 7, 3, 7.

### Luồng cực đại (`tr_t7_luong`)

- `tr_t7_lu_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (6), 1->3 (4), 2->3 (2), 2->4 (3), 2->5 (2), 3->4 (5), 4->5 (7). Giá trị luồng cực đại từ 1 đến 5 bằng bao nhiêu?
  - **Đáp án:** 9
    1. Tăng luồng: 1->2->5 thêm 2; 1->2->4->5 thêm 3; 1->3->4->5 thêm 4. Tổng 9.
    2. Kiểm tra cận trên: lát cắt S = {1, 2, 3, 4}, T = {5} có các cung 2->5 (2) và 4->5 (7), khả năng thông qua 9.
    3. Mọi luồng không vượt khả năng thông qua của một lát cắt, nên luồng 9 là cực đại.
- `tr_t7_lu_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong một mạng có đỉnh phát s và đỉnh thu t, giá trị của mọi luồng từ s đến t không vượt quá khả năng thông qua của mọi lát cắt (S, T) có s thuộc S và t thuộc T.
  - **Đáp án:** Đúng
    1. Giá trị luồng bằng lượng đi từ S sang T trừ lượng đi từ T về S (bảo toàn luồng ở mọi đỉnh khác s, t).
    2. Lượng đi từ S sang T không vượt tổng khả năng các cung từ S sang T, còn lượng đi về là không âm.
    3. Vậy giá trị luồng <= khả năng thông qua của lát cắt: khẳng định đúng. Định lý Ford-Fulkerson nói thêm: luồng cực đại bằng lát cắt hẹp nhất.
- `tr_g7_lat_cat` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (8), 1->3 (1), 1->4 (7), 2->4 (7), 2->5 (1), 3->4 (8), 3->5 (5), 4->5 (4). Xét lát cắt S = {1, 2, 4}, T là các đỉnh còn lại. Khẳng định: giá trị luồng cực đại từ 1 đến 5 bằng khả năng thông qua của lát cắt (S, T).
  - **Đáp án:** Đúng
    1. Khả năng thông qua của (S, T) là tổng khả năng các cung đi từ S sang T: 6.
    2. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    3. 1->2->5 thêm 1; 1->3->5 thêm 1; 1->4->5 thêm 4; tổng 6.
    4. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1, 2, 4}. Lát cắt (S, T) có khả năng thông qua 6 = 6, nên luồng đã là cực đại.
    5. Lát cắt này có khả năng thông qua bằng giá trị luồng cực đại: nó là lát cắt hẹp nhất. Khẳng định đúng.
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (1), 1->4 (3), 2->3 (7), 3->4 (7), 3->5 (9), 4->5 (6). Xét lát cắt S = {1}, T là các đỉnh còn lại. Khẳng định: giá trị luồng cực đại từ 1 đến 5 bằng khả năng thông qua của lát cắt (S, T).
  - **Đáp án:** Đúng
    1. Khả năng thông qua của (S, T) là tổng khả năng các cung đi từ S sang T: 4.
    2. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    3. 1->4->5 thêm 3; 1->2->3->5 thêm 1; tổng 4.
    4. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1}. Lát cắt (S, T) có khả năng thông qua 4 = 4, nên luồng đã là cực đại.
    5. Lát cắt này có khả năng thông qua bằng giá trị luồng cực đại: nó là lát cắt hẹp nhất. Khẳng định đúng.
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (4), 2->3 (4), 2->4 (8), 2->5 (9), 3->4 (9), 3->5 (8), 4->5 (7). Xét lát cắt S = {1}, T là các đỉnh còn lại. Khẳng định: giá trị luồng cực đại từ 1 đến 5 bằng khả năng thông qua của lát cắt (S, T).
  - **Đáp án:** Đúng
    1. Khả năng thông qua của (S, T) là tổng khả năng các cung đi từ S sang T: 4.
    2. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    3. 1->2->5 thêm 4; tổng 4.
    4. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1}. Lát cắt (S, T) có khả năng thông qua 4 = 4, nên luồng đã là cực đại.
    5. Lát cắt này có khả năng thông qua bằng giá trị luồng cực đại: nó là lát cắt hẹp nhất. Khẳng định đúng.
- `tr_t7_lu_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 6, đỉnh phát 1, đỉnh thu 6; các cung (khả năng thông qua trong ngoặc): 1->2 (5), 1->3 (6), 2->3 (2), 2->4 (4), 3->4 (3), 3->5 (4), 4->5 (2), 4->6 (6), 5->6 (5).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_02`, `tr_t7_lu_01`
  - **Phần a** (Điền số): a) Lát cắt S = {1, 2}, T = {3, 4, 5, 6} có khả năng thông qua bằng bao nhiêu?
    - **Đáp án a:** 12
  - **Phần b** (Điền số): b) Giá trị luồng cực đại từ 1 đến 6 bằng bao nhiêu?
    - **Đáp án b:** 11
  - **Phần c** (Đúng/Sai): c) Lát cắt S = {1, 2} ở câu a) là một lát cắt hẹp nhất.
    - **Đáp án c:** Sai
  - **Lời giải:**
    1. a) Các cung từ S sang T: 1->3 (6), 2->3 (2), 2->4 (4); tổng 12.
    2. b) Tăng luồng: 1->2->4->6 thêm 4; 1->3->4->6 thêm 2; 1->3->5->6 thêm 4; 1->2->3->4->5->6 thêm 1. Tổng 11.
    3. Cận trên: lát cắt S = {1} có 1->2 (5) và 1->3 (6), khả năng 11. Luồng 11 đạt cận này nên là cực đại.
    4. c) Lát cắt hẹp nhất có khả năng 11 < 12, nên S = {1, 2} không hẹp nhất: sai.
- `tr_t7_lu_04` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, 3, 4, đỉnh phát 1, đỉnh thu 4; các cung (khả năng thông qua trong ngoặc): 1->2 (3), 1->3 (2), 2->3 (3), 2->4 (2), 3->4 (3). Một đệ tử đã đẩy 3 đơn vị theo đường 1->2->3->4. Trên mạng thặng dư của luồng này, bước tăng luồng tiếp theo là gì?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_01`, `tr_g7_lat_cat`
    - **(đúng)** Đi 1->3->2->4 (dùng cung ngược 3->2), tăng thêm 2
    - Đi 1->3->4, tăng thêm 2
    - Đi 1->3->2->4, tăng thêm 3
    - Không còn đường tăng luồng, luồng 3 đã cực đại
  - **Đáp án:** Đi 1->3->2->4 (dùng cung ngược 3->2), tăng thêm 2
    1. Sau khi đẩy 3 đơn vị: 1->2 và 3->4 đã đầy (3/3), 2->3 đầy (3/3). Mạng thặng dư còn 1->3 (2), 2->4 (2), và các cung ngược 2->1, 3->2, 4->3 mỗi cung 3.
    2. Đường 1->3->4 không đi được vì 3->4 đã đầy. Đường 1->3->2->4 dùng cung ngược 3->2 (bớt luồng trên 2->3), lượng tăng là min(2, 3, 2) = 2.
    3. Luồng mới có giá trị 5, bằng khả năng thông qua của lát cắt S = {1} (3 + 2), nên đó là luồng cực đại. Không dùng cung ngược thì sẽ dừng sai ở 3.
- `tr_g7_luong_max` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (8), 1->3 (1), 1->4 (7), 2->4 (7), 2->5 (1), 3->4 (8), 3->5 (5), 4->5 (4). Giá trị luồng cực đại từ 1 đến 5 bằng bao nhiêu?
  - **Đáp án:** 6
    1. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    2. 1->2->5 thêm 1; 1->3->5 thêm 1; 1->4->5 thêm 4; tổng 6.
    3. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1, 2, 4}. Lát cắt (S, T) có khả năng thông qua 6 = 6, nên luồng đã là cực đại.
    4. Đáp số: 6.
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (1), 1->4 (3), 2->3 (7), 3->4 (7), 3->5 (9), 4->5 (6). Giá trị luồng cực đại từ 1 đến 5 bằng bao nhiêu?
  - **Đáp án:** 4
    1. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    2. 1->4->5 thêm 3; 1->2->3->5 thêm 1; tổng 4.
    3. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1}. Lát cắt (S, T) có khả năng thông qua 4 = 4, nên luồng đã là cực đại.
    4. Đáp số: 4.
  - **Câu hỏi:** Mạng G có các đỉnh 1, 2, ..., 5, đỉnh phát 1, đỉnh thu 5; các cung (khả năng thông qua trong ngoặc): 1->2 (4), 2->3 (4), 2->4 (8), 2->5 (9), 3->4 (9), 3->5 (8), 4->5 (7). Giá trị luồng cực đại từ 1 đến 5 bằng bao nhiêu?
  - **Đáp án:** 4
    1. Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:
    2. 1->2->5 thêm 4; tổng 4.
    3. Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {1}. Lát cắt (S, T) có khả năng thông qua 4 = 4, nên luồng đã là cực đại.
    4. Đáp số: 4.

## Tầng 8: Bài toán tối ưu, tập lồi và hàm lồi

35 dạng câu (25 câu viết tay, 10 bộ sinh câu); 35 chưa duyệt.

### Phát biểu bài toán tối ưu (`tr_t8_bai_toan_toi_uu`)

- `tr_t8_bt_01` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tông môn pha linh dịch từ hai loại linh thảo A và B. Mỗi gam A chứa 2 phần mộc khí, 1 phần thủy khí, giá 3 linh thạch; mỗi gam B chứa 1 phần mộc khí, 3 phần thủy khí, giá 4 linh thạch. Linh dịch cần ít nhất 8 phần mộc khí và ít nhất 9 phần thủy khí, với chi phí nhỏ nhất. Gọi x, y là số gam A, B. Mô hình nào đúng?
    - **(đúng)** min 3x + 4y với 2x + y >= 8, x + 3y >= 9, x >= 0, y >= 0
    - max 3x + 4y với 2x + y >= 8, x + 3y >= 9, x >= 0, y >= 0
    - min 3x + 4y với 2x + y <= 8, x + 3y <= 9, x >= 0, y >= 0
    - min 3x + 4y với 2x + 3y >= 8, x + y >= 9, x >= 0, y >= 0
  - **Đáp án:** min 3x + 4y với 2x + y >= 8, x + 3y >= 9, x >= 0, y >= 0
    1. Biến quyết định: x, y gam, không âm. Hàm mục tiêu: chi phí 3x + 4y, cần nhỏ nhất (min).
    2. Mộc khí: 2x + y, phải đạt ít nhất 8, nên 2x + y >= 8. Thủy khí: x + 3y >= 9.
    3. Phương án thứ tư ghép sai hệ số: mỗi ràng buộc là lượng một chất từ cả hai loại, không phải lượng hai chất từ một loại.
- `tr_t8_bt_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hàm f xác định trên tập D. Mọi điểm cực tiểu toàn cục của f trên D cũng là một điểm cực tiểu địa phương của f trên D.
  - **Đáp án:** Đúng
    1. x* là cực tiểu toàn cục khi f(x*) <= f(x) với mọi x thuộc D.
    2. Cực tiểu địa phương chỉ đòi f(x*) <= f(x) với x thuộc D gần x*, tức với ít điểm hơn.
    3. Nên cực tiểu toàn cục luôn là cực tiểu địa phương: khẳng định đúng. Chiều ngược lại thì không đúng.
- `tr_t8_bt_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi điểm với tính chất của nó (xét trên toàn bộ R).
  - **Đáp án (ghép đúng):**
    - x = 1 với f(x) = x^3 - 3x — cực tiểu địa phương nhưng không toàn cục
    - x = -1 với f(x) = x^3 - 3x — cực đại địa phương nhưng không toàn cục
    - x = 0 với f(x) = x^2 + 1 — cực tiểu toàn cục
    - x = 0 với f(x) = x^3 — điểm dừng nhưng không là cực trị
  - **Lời giải:**
    1. f(x) = x^3 - 3x có f'(x) = 3x^2 - 3 = 0 tại x = 1 và x = -1; f''(x) = 6x.
    2. f''(1) = 6 > 0: cực tiểu địa phương, f(1) = -2; nhưng f(x) -> -vô cùng khi x -> -vô cùng nên không toàn cục. f''(-1) = -6 < 0: cực đại địa phương, cũng không toàn cục vì f -> +vô cùng.
    3. x^2 + 1 >= 1 = f(0) với mọi x: cực tiểu toàn cục.
    4. x^3 có đạo hàm 0 tại 0 nhưng đổi dấu giá trị qua 0 (x^3 < 0 bên trái, > 0 bên phải): không là cực trị.
- `tr_g8_hang_rao` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một khu vườn hình chữ nhật nằm sát bờ sông; cạnh dọc bờ sông không cần rào, ba cạnh còn lại được rào. Tổng chiều dài rào là 44 mét. Gọi x là chiều dài mỗi cạnh bên (và mỗi hàng rào chia ô), y là chiều dài cạnh kia. Diện tích lớn nhất của khu vườn là bao nhiêu mét vuông?
  - **Đáp án:** 242
    1. Ràng buộc: 2x + y = 44, với x > 0, y > 0. Hàm mục tiêu: diện tích S = xy.
    2. Thế y theo x: S = x(44 - 2x), một parabol quay xuống (hàm lõm).
    3. S'(x) = 0 cho x = 11; khi đó y = 22.
    4. Diện tích lớn nhất: 11 . 22 = 242.
  - **Câu hỏi:** Một khu vườn hình chữ nhật được rào cả bốn cạnh. Tổng chiều dài rào là 20 mét. Gọi x là chiều dài mỗi cạnh bên (và mỗi hàng rào chia ô), y là chiều dài cạnh kia. Diện tích lớn nhất của khu vườn là bao nhiêu mét vuông?
  - **Đáp án:** 25
    1. Ràng buộc: 2x + 2y = 20, với x > 0, y > 0. Hàm mục tiêu: diện tích S = xy.
    2. Thế y theo x: S = x(20 - 2x)/2, một parabol quay xuống (hàm lõm).
    3. S'(x) = 0 cho x = 5; khi đó y = 5.
    4. Diện tích lớn nhất: 5 . 5 = 25.
  - **Câu hỏi:** Một khu vườn hình chữ nhật nằm sát bờ sông; cạnh dọc bờ sông không cần rào. Ngoài ba cạnh còn lại, vườn được chia thành 2 ô bằng 1 hàng rào song song với hai cạnh vuông góc bờ sông. Tổng chiều dài rào là 56 mét. Gọi x là chiều dài mỗi cạnh bên (và mỗi hàng rào chia ô), y là chiều dài cạnh kia. Diện tích lớn nhất của khu vườn là bao nhiêu mét vuông?
  - **Đáp án:** 784/3
    1. Ràng buộc: 3x + y = 56, với x > 0, y > 0. Hàm mục tiêu: diện tích S = xy.
    2. Thế y theo x: S = x(56 - 3x), một parabol quay xuống (hàm lõm).
    3. S'(x) = 0 cho x = 28/3; khi đó y = 28.
    4. Diện tích lớn nhất: 28/3 . 28 = 784/3.
- `tr_t8_bt_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đệ tử làm một chiếc hộp hình hộp chữ nhật không nắp, đáy là hình vuông cạnh x dm, chiều cao h dm, thể tích đúng 32 dm^3, sao cho tổng diện tích bìa (đáy và bốn mặt bên) nhỏ nhất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bt_01`, `tr_g8_hang_rao`
  - **Phần a** (Điền số): a) Từ ràng buộc thể tích, diện tích bìa viết được dạng S(x) = x^2 + k/x với x > 0. Tìm k.
    - **Đáp án a:** 128
  - **Phần b** (Điền số): b) Giá trị x làm S nhỏ nhất bằng bao nhiêu?
    - **Đáp án b:** 4
  - **Phần c** (Điền số): c) Diện tích bìa nhỏ nhất bằng bao nhiêu dm^2?
    - **Đáp án c:** 48
  - **Phần d** (Đúng/Sai): d) Ở phương án tối ưu, chiều cao bằng một nửa cạnh đáy.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Ràng buộc x^2 h = 32 cho h = 32/x^2. Diện tích S = x^2 + 4xh = x^2 + 128/x, nên k = 128.
    2. b) S'(x) = 2x - 128/x^2 = 0 khi x^3 = 64, x = 4. S''(x) = 2 + 256/x^3 > 0 với x > 0, nên S lồi trên (0, +vô cùng) và x = 4 là cực tiểu toàn cục.
    3. c) S(4) = 16 + 32 = 48.
    4. d) h = 32/16 = 2 = 4/2: đúng.
- `tr_t8_bt_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tìm giá trị nhỏ nhất của f(x) = x^3 - 3x + 1 trên đoạn [-3, 3].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bt_03`, `tr_t8_bt_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 3x^2 - 3.
    2. f'(x) = 0 khi x = 1 hoặc x = -1, cả hai đều thuộc [-3, 3].
    3. f(1) = -1 và f(-1) = 3.
    4. f''(1) = 6 > 0 nên x = 1 là điểm cực tiểu địa phương duy nhất; vậy giá trị nhỏ nhất của f trên [-3, 3] là -1.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: f''(1) = 6 > 0 nên x = 1 là điểm cực tiểu địa phương duy nhất; vậy giá trị nhỏ nhất của f trên [-3, 3] là -1.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng. Bước 4 sai: trên một đoạn, giá trị nhỏ nhất có thể đạt ở đầu mút, nơi f' không cần bằng 0.
    2. Phải so sánh cả f(-3) = -27 + 9 + 1 = -17 và f(3) = 27 - 9 + 1 = 19.
    3. Giá trị nhỏ nhất là -17, tại x = -3; cực tiểu địa phương x = 1 không phải cực tiểu toàn cục.
- `tr_g8_hop` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Từ một tấm bìa hình chữ nhật 15 x 24 (đơn vị dm), cắt ở bốn góc bốn hình vuông cạnh x rồi gập lên thành một cái hộp không nắp. Nhập hai số: giá trị x làm thể tích hộp lớn nhất, rồi thể tích lớn nhất đó.
  - **Đáp án:** 3, 486
    1. Thể tích V(x) = x(15 - 2x)(24 - 2x) với 0 < x < 15/2.
    2. V'(x) = 12x^2 - 156x + 360.
    3. V'(x) = 0 cho x = (39 - 21)/6 = 3 hoặc x = (39 + 21)/6 = 10; chỉ nghiệm thứ nhất nằm trong miền.
    4. V liên tục, bằng 0 ở hai đầu miền và dương bên trong, nên điểm dừng duy nhất trong miền là điểm lớn nhất.
    5. V(3) = 3 . 9 . 18 = 486.
  - **Câu hỏi:** Từ một tấm bìa hình chữ nhật 8 x 3 (đơn vị dm), cắt ở bốn góc bốn hình vuông cạnh x rồi gập lên thành một cái hộp không nắp. Nhập hai số: giá trị x làm thể tích hộp lớn nhất, rồi thể tích lớn nhất đó.
  - **Đáp án:** 2/3, 200/27
    1. Thể tích V(x) = x(8 - 2x)(3 - 2x) với 0 < x < 3/2.
    2. V'(x) = 12x^2 - 44x + 24.
    3. V'(x) = 0 cho x = (11 - 7)/6 = 2/3 hoặc x = (11 + 7)/6 = 3; chỉ nghiệm thứ nhất nằm trong miền.
    4. V liên tục, bằng 0 ở hai đầu miền và dương bên trong, nên điểm dừng duy nhất trong miền là điểm lớn nhất.
    5. V(2/3) = 2/3 . (20/3) . (5/3) = 200/27.
  - **Câu hỏi:** Từ một tấm bìa hình chữ nhật 15 x 24 (đơn vị dm), cắt ở bốn góc bốn hình vuông cạnh x rồi gập lên thành một cái hộp không nắp. Nhập hai số: giá trị x làm thể tích hộp lớn nhất, rồi thể tích lớn nhất đó.
  - **Đáp án:** 3, 486
    1. Thể tích V(x) = x(15 - 2x)(24 - 2x) với 0 < x < 15/2.
    2. V'(x) = 12x^2 - 156x + 360.
    3. V'(x) = 0 cho x = (39 - 21)/6 = 3 hoặc x = (39 + 21)/6 = 10; chỉ nghiệm thứ nhất nằm trong miền.
    4. V liên tục, bằng 0 ở hai đầu miền và dương bên trong, nên điểm dừng duy nhất trong miền là điểm lớn nhất.
    5. V(3) = 3 . 9 . 18 = 486.

### Tập lồi (`tr_t8_tap_loi`)

- `tr_t8_tl_01` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập nào dưới đây KHÔNG là tập lồi trong R^2?
    - **(đúng)** {(x, y) : xy >= 1}
    - {(x, y) : x^2 + y^2 <= 4}
    - {(x, y) : x + 2y >= 1, x >= 0}
    - {(x, y) : xy >= 1, x > 0}
    - {(x, y) : y >= x^2}
  - **Đáp án:** {(x, y) : xy >= 1}
    1. (1, 1) và (-1, -1) đều thỏa xy >= 1, nhưng trung điểm (0, 0) thì không: tập {xy >= 1} không lồi (hai nhánh hyperbol).
    2. Hình tròn, giao các nửa mặt phẳng, và tập trên đồ thị của hàm lồi y = x^2 đều lồi.
    3. {xy >= 1, x > 0} là {y >= 1/x, x > 0}: phần nằm trên đồ thị của hàm lồi 1/x trên (0, +vô cùng), nên lồi.
- `tr_t8_tl_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hợp của hai tập lồi trong R luôn là một tập lồi.
  - **Đáp án:** Sai
    1. Phản ví dụ: A = [0, 1] và B = [2, 3] đều lồi.
    2. 1 và 2 thuộc A hợp B, nhưng 3/2 nằm giữa chúng thì không.
    3. Vậy hợp không lồi: khẳng định sai. Giao của các tập lồi mới luôn lồi.
- `tr_t8_tl_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A(4, 3), B(-2, -3) và P(2, 1). Tìm t sao cho P = tA + (1 - t)B; từ đó P nằm trên đoạn AB khi t thuộc [0, 1].
  - **Đáp án:** 2/3
    1. Hoành độ: 4t - 2(1 - t) = 6t - 2 = 2, nên t = 2/3.
    2. Tung độ: 3t - 3(1 - t) = 6t - 3 = 1, cũng cho t = 2/3: P thẳng hàng với A, B.
    3. t = 2/3 thuộc [0, 1] nên P nằm trên đoạn AB; mọi tập lồi chứa A và B đều chứa P.
- `tr_g8_tap_muc` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho S = {x thuộc R : -2x^2 + 14x - 12 <= 0}. Khẳng định: S là một tập lồi.
  - **Đáp án:** Sai
    1. Trên đường thẳng, một tập là lồi khi và chỉ khi nó là một khoảng (đoạn, nửa đường thẳng, cả R, hay rỗng).
    2. Tam thức có hai nghiệm 1 và 6, hệ số của x^2 là -2 (âm).
    3. Tập S là hợp hai nửa đường thẳng (-vô cùng, 1] và [6, +vô cùng).
    4. S không lồi: 1 và 6 thuộc S nhưng trung điểm 7/2 của đoạn nối chúng không thuộc S. Khẳng định sai.
  - **Câu hỏi:** Cho S = {x thuộc R : -3x^2 + 3x + 60 <= 0}. Khẳng định: S là một tập lồi.
  - **Đáp án:** Sai
    1. Trên đường thẳng, một tập là lồi khi và chỉ khi nó là một khoảng (đoạn, nửa đường thẳng, cả R, hay rỗng).
    2. Tam thức có hai nghiệm -4 và 5, hệ số của x^2 là -3 (âm).
    3. Tập S là hợp hai nửa đường thẳng (-vô cùng, -4] và [5, +vô cùng).
    4. S không lồi: -4 và 5 thuộc S nhưng trung điểm 1/2 của đoạn nối chúng không thuộc S. Khẳng định sai.
  - **Câu hỏi:** Cho S = {x thuộc R : -2x^2 + 8x - 6 <= 0}. Khẳng định: S là một tập lồi.
  - **Đáp án:** Sai
    1. Trên đường thẳng, một tập là lồi khi và chỉ khi nó là một khoảng (đoạn, nửa đường thẳng, cả R, hay rỗng).
    2. Tam thức có hai nghiệm 1 và 3, hệ số của x^2 là -2 (âm).
    3. Tập S là hợp hai nửa đường thẳng (-vô cùng, 1] và [3, +vô cùng).
    4. S không lồi: 1 và 3 thuộc S nhưng trung điểm 2 của đoạn nối chúng không thuộc S. Khẳng định sai.
- `tr_t8_tl_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh: miền ràng buộc {x : a_i^T x <= b_i, i = 1, ..., m} của một bài toán quy hoạch tuyến tính là tập lồi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_tl_02`, `tr_t8_tl_03`
  - **Đáp án (thứ tự đúng):**
    1. Mỗi ràng buộc a_i^T x <= b_i xác định một nửa không gian H_i.
    2. Lấy x, y thuộc H_i và t thuộc [0, 1]; khi đó a_i^T(tx + (1 - t)y) = t a_i^T x + (1 - t) a_i^T y.
    3. Vì t >= 0 và 1 - t >= 0 nên vế phải không vượt t b_i + (1 - t) b_i = b_i: điểm tx + (1 - t)y thuộc H_i, nên H_i lồi.
    4. Miền ràng buộc là giao của các nửa không gian H_1, ..., H_m vừa chứng minh là lồi.
    5. Giao của các tập lồi là tập lồi, nên miền ràng buộc lồi.
  - **Lời giải:**
    1. Đầu tiên đặt tên cho các nửa không gian, rồi chứng minh mỗi nửa không gian lồi bằng định nghĩa (bước 2 và 3).
    2. Bước nhân bất đẳng thức với t và 1 - t cần chúng không âm.
    3. Cuối cùng viết miền ràng buộc thành giao và dùng tính chất giao của tập lồi.
- `tr_t8_tl_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tập S = {(x, y) : x^2 + y^2 >= 1} (phần ngoài hình tròn đơn vị) có lồi không?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_tl_02`, `tr_t8_tl_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Lấy P, Q thuộc S và M = tP + (1 - t)Q với t thuộc [0, 1].
    2. Hàm g(x, y) = x^2 + y^2 là hàm lồi trên R^2.
    3. Vì g lồi nên g(M) >= t g(P) + (1 - t) g(Q).   **<- bước sai đầu tiên**
    4. Mà g(P) >= 1 và g(Q) >= 1, nên g(M) >= 1, tức M thuộc S.
    5. Vậy S là tập lồi.
  - **Đáp án:** Bước 3: Vì g lồi nên g(M) >= t g(P) + (1 - t) g(Q).
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 đúng (g là tổng hai bình phương). Bước 3 sai chiều: hàm lồi cho g(M) <= t g(P) + (1 - t) g(Q), không phải >=.
    2. Bất đẳng thức đúng chiều chỉ cho thấy tập dưới mức {g <= 1} là lồi.
    3. Thật ra S không lồi: P(1, 0) và Q(-1, 0) thuộc S nhưng trung điểm (0, 0) thì không.
- `tr_g8_to_hop_loi` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A(-2, 5), B(-3, 0), C(-3, 3) và P(-2, 3). Tìm các số a, b, c với a + b + c = 1 và P = aA + bB + cC; nhập a, b, c.
  - **Đáp án:** 1, 2/3, -2/3
    1. Viết theo tọa độ: a + b + c = 1, -2a + (-3)b + (-3)c = -2, 5a + 0b + 3c = 3.
    2. Giải hệ ba phương trình bậc nhất (ví dụ bằng quy tắc Cramer, mỗi hệ số là tỉ số hai diện tích có dấu).
    3. a = 1, b = 2/3, c = -2/3.
    4. Có hệ số âm, nên P nằm ngoài tam giác ABC (bao lồi của A, B, C).
  - **Câu hỏi:** Cho A(-4, -3), B(-3, 1), C(-2, 6) và P(-3, 1). Tìm các số a, b, c với a + b + c = 1 và P = aA + bB + cC; nhập a, b, c.
  - **Đáp án:** 0, 1, 0
    1. Viết theo tọa độ: a + b + c = 1, -4a + (-3)b + (-2)c = -3, -3a + 1b + 6c = 1.
    2. Giải hệ ba phương trình bậc nhất (ví dụ bằng quy tắc Cramer, mỗi hệ số là tỉ số hai diện tích có dấu).
    3. a = 0, b = 1, c = 0.
    4. Cả ba hệ số đều không âm, nên P nằm trong tam giác ABC (bao lồi của A, B, C).
  - **Câu hỏi:** Cho A(-1, 5), B(4, -2), C(1, 5) và P(2, -1). Tìm các số a, b, c với a + b + c = 1 và P = aA + bB + cC; nhập a, b, c.
  - **Đáp án:** 11/14, 6/7, -9/14
    1. Viết theo tọa độ: a + b + c = 1, -1a + 4b + 1c = 2, 5a + (-2)b + 5c = -1.
    2. Giải hệ ba phương trình bậc nhất (ví dụ bằng quy tắc Cramer, mỗi hệ số là tỉ số hai diện tích có dấu).
    3. a = 11/14, b = 6/7, c = -9/14.
    4. Có hệ số âm, nên P nằm ngoài tam giác ABC (bao lồi của A, B, C).

### Hàm lồi (`tr_t8_ham_loi`)

- `tr_t8_hl_01` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm với tính lồi lõm của nó.
  - **Đáp án (ghép đúng):**
    - f(x) = e^x trên R — lồi trên R, vì f''(x) = e^x > 0
    - f(x) = ln x trên (0, +vô cùng) — lõm, vì f''(x) = -1/x^2 < 0
    - f(x) = x^3 trên R — lõm trên (-vô cùng, 0], lồi trên [0, +vô cùng)
    - f(x) = |x| trên R — lồi trên R nhưng không khả vi tại 0
  - **Lời giải:**
    1. Hàm khả vi hai lần trên một khoảng là lồi khi và chỉ khi f'' >= 0 trên khoảng đó, lõm khi f'' <= 0.
    2. x^3 có f''(x) = 6x đổi dấu tại 0.
    3. |x| không có đạo hàm tại 0, nên dùng định nghĩa: |tx + (1 - t)y| <= t|x| + (1 - t)|y| (bất đẳng thức tam giác), vậy |x| lồi.
- `tr_t8_hl_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu f và g là hai hàm lồi trên R thì tích f . g cũng là hàm lồi trên R.
  - **Đáp án:** Sai
    1. Tổng của hai hàm lồi thì lồi, nhưng tích thì không chắc.
    2. Phản ví dụ: f(x) = x (tuyến tính, nên lồi) và g(x) = x^2 (lồi). Tích là x^3, có (x^3)'' = 6x < 0 khi x < 0.
    3. x^3 không lồi trên R: khẳng định sai.
- `tr_t8_hl_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét f(x, y) = x^2 + 3xy + y^2 trên R^2. Khẳng định nào đúng?
    - **(đúng)** H = [2, 3; 3, 2], det H = -5 < 0, nên f không lồi
    - Hai hệ số của x^2 và y^2 đều dương, nên f lồi
    - H = [1, 3; 3, 1], det H = -8 < 0, nên f không lồi
    - H = [2, 3; 3, 2], det H = 13 > 0, nên f lồi
  - **Đáp án:** H = [2, 3; 3, 2], det H = -5 < 0, nên f không lồi
    1. f_xx = 2, f_yy = 2, f_xy = 3, nên ma trận Hesse H = [2, 3; 3, 2] (không phải [1, 3; 3, 1]).
    2. det H = 2 . 2 - 3 . 3 = -5 < 0: H có một trị riêng âm, nên H không nửa xác định dương và f không lồi.
    3. Cụ thể f(1, -1) = 1 - 3 + 1 = -1 < 0 = f(0, 0): theo hướng (1, -1) f là parabol quay xuống. Hai hệ số chéo dương là chưa đủ.
- `tr_g8_hesse` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = 4x^2 + 6xy + 4y^2 - 4x - y. Khẳng định: f là hàm lồi trên R^2.
  - **Đáp án:** Đúng
    1. Ma trận Hesse là hằng số: H = [8, 6; 6, 8].
    2. f lồi trên R^2 khi và chỉ khi H nửa xác định dương: hai phần tử chéo không âm và det H >= 0.
    3. Phần tử chéo 8, 8 không âm và det H = 28 >= 0, nên H nửa xác định dương và f lồi. Khẳng định đúng.
  - **Câu hỏi:** Cho f(x, y) = 4x^2 - 5xy - 2y^2 - 4x. Khẳng định: f là hàm lồi trên R^2.
  - **Đáp án:** Sai
    1. Ma trận Hesse là hằng số: H = [8, -5; -5, -4].
    2. f lồi trên R^2 khi và chỉ khi H nửa xác định dương: hai phần tử chéo không âm và det H >= 0.
    3. Có phần tử chéo âm (-4), nên theo một trục tọa độ f là parabol quay xuống: f không lồi. Khẳng định sai.
  - **Câu hỏi:** Cho f(x, y) = 2x^2 + 2xy + 4y^2 + 2x + y. Khẳng định: f là hàm lồi trên R^2.
  - **Đáp án:** Đúng
    1. Ma trận Hesse là hằng số: H = [4, 2; 2, 8].
    2. f lồi trên R^2 khi và chỉ khi H nửa xác định dương: hai phần tử chéo không âm và det H >= 0.
    3. Phần tử chéo 4, 8 không âm và det H = 28 >= 0, nên H nửa xác định dương và f lồi. Khẳng định đúng.
- `tr_g8_khoang_lom` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^4 + 10x^3 + 36x^2 - x - 6 lõm trên đúng một đoạn [p, q], và lồi trên (-vô cùng, p] cũng như trên [q, +vô cùng). Nhập p, q.
  - **Đáp án:** -3, -2
    1. f''(x) = 12x^2 + 60x + 72 = 12(x - (-3))(x - (-2)).
    2. f''(x) <= 0 đúng khi x nằm giữa hai nghiệm, tức trên [-3, -2]: ở đó f lõm.
    3. Ngoài đoạn đó f''(x) >= 0 nên f lồi. Đáp số: -3, -2.
  - **Câu hỏi:** Hàm f(x) = x^4 + 14x^3 + 72x^2 - 7x + 2 lõm trên đúng một đoạn [p, q], và lồi trên (-vô cùng, p] cũng như trên [q, +vô cùng). Nhập p, q.
  - **Đáp án:** -4, -3
    1. f''(x) = 12x^2 + 84x + 144 = 12(x - (-4))(x - (-3)).
    2. f''(x) <= 0 đúng khi x nằm giữa hai nghiệm, tức trên [-4, -3]: ở đó f lõm.
    3. Ngoài đoạn đó f''(x) >= 0 nên f lồi. Đáp số: -4, -3.
  - **Câu hỏi:** Hàm f(x) = x^4 + 6x^3 + 12x^2 + 2x + 6 lõm trên đúng một đoạn [p, q], và lồi trên (-vô cùng, p] cũng như trên [q, +vô cùng). Nhập p, q.
  - **Đáp án:** -2, -1
    1. f''(x) = 12x^2 + 36x + 24 = 12(x - (-2))(x - (-1)).
    2. f''(x) <= 0 đúng khi x nằm giữa hai nghiệm, tức trên [-2, -1]: ở đó f lõm.
    3. Ngoài đoạn đó f''(x) >= 0 nên f lồi. Đáp số: -2, -1.
- `tr_t8_hl_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^2 + kxy + 4y^2, với k là một tham số thực.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_03`, `tr_g8_hesse`
  - **Phần a** (Điền số): a) Với k = 3, định thức của ma trận Hesse của f bằng bao nhiêu?
    - **Đáp án a:** 7
  - **Phần b** (Đúng/Sai): b) Với k = 3, f là hàm lồi trên R^2.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Số nguyên dương k lớn nhất để f lồi trên R^2 là bao nhiêu?
    - **Đáp án c:** 4
  - **Lời giải:**
    1. Ma trận Hesse H = [2, k; k, 8], không phụ thuộc (x, y).
    2. a) k = 3: det H = 2 . 8 - 3^2 = 7.
    3. b) Phần tử chéo 2, 8 dương và det H = 7 > 0: H xác định dương, f lồi (chặt). Đúng.
    4. c) f lồi khi và chỉ khi H nửa xác định dương: phần tử chéo đã dương, cần 16 - k^2 >= 0, tức |k| <= 4. Với k = 4, f = (x + 2y)^2 >= 0 vẫn lồi; với k = 5, det H < 0. Đáp số 4.
- `tr_t8_hl_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: f(x, y) = x^2 + 4xy + y^2 có phải hàm lồi, và (0, 0) có phải cực tiểu toàn cục của f không?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_03`, `tr_t8_hl_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. f_xx = 2, f_yy = 2, f_xy = 4.
    2. Ma trận Hesse H = [2, 4; 4, 2], không phụ thuộc (x, y).
    3. Hai phần tử chéo của H đều dương, nên H xác định dương.   **<- bước sai đầu tiên**
    4. Vậy f lồi, và vì grad f(0, 0) = 0 nên (0, 0) là cực tiểu toàn cục.
  - **Đáp án:** Bước 3: Hai phần tử chéo của H đều dương, nên H xác định dương.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: ma trận 2 x 2 đối xứng xác định dương khi phần tử chéo dương và định thức dương; ở đây det H = 4 - 16 = -12 < 0.
    2. H có một trị riêng dương và một trị riêng âm, nên f không lồi và (0, 0) là điểm yên ngựa.
    3. Kiểm tra: f(1, -1) = 1 - 4 + 1 = -2 < 0 = f(0, 0).

### Điều kiện tối ưu không ràng buộc (`tr_t8_dieu_kien_toi_uu`)

- `tr_t8_dk_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm điểm dừng (x, y) của f(x, y) = x^2 + xy + y^2 - 2x + 4y; nhập x, y.
  - **Đáp án:** 8/3, -10/3
    1. f_x = 2x + y - 2, f_y = x + 2y + 4.
    2. Từ f_x = 0: y = 2 - 2x. Thay vào f_y = 0: x + 4 - 4x + 4 = 0, nên x = 8/3.
    3. y = 2 - 16/3 = -10/3. Kiểm tra: f_y = 8/3 - 20/3 + 4 = 0.
- `tr_t8_dk_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 có f'(0) = 0, nên x = 0 là một điểm cực trị địa phương của f.
  - **Đáp án:** Sai
    1. f'(x*) = 0 chỉ là điều kiện cần cho một cực trị của hàm khả vi, không phải điều kiện đủ.
    2. x^3 < 0 khi x < 0 và x^3 > 0 khi x > 0: trong mọi lân cận của 0 có điểm lớn hơn và điểm nhỏ hơn f(0) = 0.
    3. Vậy 0 là điểm dừng nhưng không là cực trị: khẳng định sai.
- `tr_t8_dk_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x, y) = x^3 - 3x + y^2 có hai điểm dừng (1, 0) và (-1, 0). Phân loại nào đúng?
    - **(đúng)** (1, 0) là cực tiểu địa phương, (-1, 0) là điểm yên ngựa
    - (1, 0) là cực tiểu toàn cục, (-1, 0) là cực đại địa phương
    - Cả hai đều là cực tiểu địa phương
    - (1, 0) là điểm yên ngựa, (-1, 0) là cực tiểu địa phương
  - **Đáp án:** (1, 0) là cực tiểu địa phương, (-1, 0) là điểm yên ngựa
    1. H(x, y) = [6x, 0; 0, 2].
    2. Tại (1, 0): H = [6, 0; 0, 2] xác định dương: cực tiểu địa phương. Không toàn cục vì f(x, 0) = x^3 - 3x -> -vô cùng khi x -> -vô cùng.
    3. Tại (-1, 0): H = [-6, 0; 0, 2] có trị riêng âm và dương: điểm yên ngựa (cực đại theo x, cực tiểu theo y).
- `tr_g8_diem_dung` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm điểm dừng (x, y) của f(x, y) = -x^2 + 4xy - 2y^2 - 5y; nhập x, y.
  - **Đáp án:** 5/2, 5/4
    1. f_x = -2x + 4y, f_y = 4x - 4y - 5.
    2. Điểm dừng: giải hệ f_x = 0, f_y = 0 (hệ hai phương trình bậc nhất, định thức -2 . -4 - 4^2 = -8 khác 0 nên có đúng một nghiệm).
    3. Nghiệm: x = 5/2, y = 5/4.
  - **Câu hỏi:** Tìm điểm dừng (x, y) của f(x, y) = -3x^2 - 4xy - 2y^2 + 3x - 3y; nhập x, y.
  - **Đáp án:** 3, -15/4
    1. f_x = -6x - 4y + 3, f_y = -4x - 4y - 3.
    2. Điểm dừng: giải hệ f_x = 0, f_y = 0 (hệ hai phương trình bậc nhất, định thức -6 . -4 - (-4)^2 = 8 khác 0 nên có đúng một nghiệm).
    3. Nghiệm: x = 3, y = -15/4.
  - **Câu hỏi:** Tìm điểm dừng (x, y) của f(x, y) = 2x^2 + 4xy + 4y^2 - 6x - 8y; nhập x, y.
  - **Đáp án:** 1, 1/2
    1. f_x = 4x + 4y - 6, f_y = 4x + 8y - 8.
    2. Điểm dừng: giải hệ f_x = 0, f_y = 0 (hệ hai phương trình bậc nhất, định thức 4 . 8 - 4^2 = 16 khác 0 nên có đúng một nghiệm).
    3. Nghiệm: x = 1, y = 1/2.
- `tr_t8_dk_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét bài toán min f(x, y) = 2x^2 + 2xy + y^2 - 6x - 4y trên R^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Phần a** (Điền số): a) Nhập điểm dừng x, y của f.
    - **Đáp án a:** 1, 1
  - **Phần b** (Đúng/Sai): b) Ma trận Hesse của f xác định dương, nên điểm dừng là cực tiểu toàn cục.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Giá trị nhỏ nhất của f bằng bao nhiêu?
    - **Đáp án c:** -5
  - **Lời giải:**
    1. a) f_x = 4x + 2y - 6 = 0, f_y = 2x + 2y - 4 = 0. Trừ hai phương trình: 2x - 2 = 0, x = 1, rồi y = 1.
    2. b) H = [4, 2; 2, 2]: phần tử chéo dương, det H = 8 - 4 = 4 > 0, nên H xác định dương, f lồi chặt, điểm dừng là cực tiểu toàn cục. Đúng.
    3. c) f(1, 1) = 2 + 2 + 1 - 6 - 4 = -5.
- `tr_t8_dk_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm giá trị nhỏ nhất của f(x, y) = x^2 + xy + y^2 - 3y trên R^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_dk_03`
  - **Đáp án (thứ tự đúng):**
    1. Tính các đạo hàm riêng: f_x = 2x + y, f_y = x + 2y - 3.
    2. Giải f_x = 0, f_y = 0: từ f_x = 0 có y = -2x, thay vào f_y = 0 được -3x - 3 = 0.
    3. Vậy điểm dừng duy nhất là x = -1, y = 2.
    4. H = [2, 1; 1, 2] có phần tử chéo dương và det H = 3 > 0, nên f lồi chặt và (-1, 2) là cực tiểu toàn cục.
    5. Giá trị nhỏ nhất là f(-1, 2) = 1 - 2 + 4 - 6 = -3.
  - **Lời giải:**
    1. Điều kiện cần (gradient bằng 0) cho điểm dừng; phải giải xong hệ mới có điểm (-1, 2).
    2. Điều kiện đủ (Hesse xác định dương, f lồi) biến điểm dừng thành cực tiểu toàn cục; chỉ khi đó mới gọi f(-1, 2) là giá trị nhỏ nhất.
    3. Kiểm tra: f_x(-1, 2) = -2 + 2 = 0, f_y(-1, 2) = -1 + 4 - 3 = 0.
- `tr_g8_cuc_tieu` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = 2x^2 - xy + y^2 - 5x + 7y trên R^2.
  - **Đáp án:** -88/7
    1. H = [4, -1; -1, 2] có 4 > 0 và det H = 7 > 0: xác định dương, f lồi chặt, nên điểm dừng là cực tiểu toàn cục.
    2. Giải f_x = 4x - y - 5 = 0, f_y = -x + 2y + 7 = 0: x = 3/7, y = -23/7.
    3. Giá trị nhỏ nhất f(3/7, -23/7) = -88/7.
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = 3x^2 + 4xy + 3y^2 - 2x - 7y trên R^2.
  - **Đáp án:** -103/20
    1. H = [6, 4; 4, 6] có 6 > 0 và det H = 20 > 0: xác định dương, f lồi chặt, nên điểm dừng là cực tiểu toàn cục.
    2. Giải f_x = 6x + 4y - 2 = 0, f_y = 4x + 6y - 7 = 0: x = -4/5, y = 17/10.
    3. Giá trị nhỏ nhất f(-4/5, 17/10) = -103/20.
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = 2x^2 + 2y^2 + 7x - 6y trên R^2.
  - **Đáp án:** -85/8
    1. H = [4, 0; 0, 4] có 4 > 0 và det H = 16 > 0: xác định dương, f lồi chặt, nên điểm dừng là cực tiểu toàn cục.
    2. Giải f_x = 4x + 7 = 0, f_y = 4y - 6 = 0: x = -7/4, y = 3/2.
    3. Giá trị nhỏ nhất f(-7/4, 3/2) = -85/8.

### Bài toán tối ưu lồi (`tr_t8_bai_toan_loi`)

- `tr_t8_bl_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong bài toán min f(x) với x thuộc D, nếu D là tập lồi và f là hàm lồi trên D thì mọi điểm cực tiểu địa phương cũng là điểm cực tiểu toàn cục.
  - **Đáp án:** Đúng
    1. Giả sử x* cực tiểu địa phương nhưng có y thuộc D với f(y) < f(x*).
    2. Với t nhỏ, điểm z = (1 - t)x* + ty thuộc D (D lồi) và gần x*, và f(z) <= (1 - t)f(x*) + t f(y) < f(x*) (f lồi).
    3. Điều đó mâu thuẫn với x* là cực tiểu địa phương. Khẳng định đúng: đây là tính chất quan trọng nhất của bài toán lồi.
- `tr_t8_bl_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán nào dưới đây là bài toán tối ưu lồi (cực tiểu một hàm lồi trên một tập lồi)?
    - **(đúng)** min x^2 + y^2 với x + y >= 1
    - min x^2 với x^2 >= 1
    - max x^2 + y^2 với x^2 + y^2 <= 1
    - min x^3 với -1 <= x <= 2
  - **Đáp án:** min x^2 + y^2 với x + y >= 1
    1. x^2 + y^2 lồi, và nửa mặt phẳng x + y >= 1 lồi: đây là bài toán lồi.
    2. {x^2 >= 1} = (-vô cùng, -1] hợp [1, +vô cùng) không lồi. Cực đại một hàm lồi không phải bài toán lồi (tương đương cực tiểu một hàm lõm).
    3. x^3 có f''(x) = 6x < 0 khi x < 0, nên không lồi trên [-1, 2].
- `tr_t8_bl_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giải bài toán min f(x) = (x - 1)^2 + (x - 4)^2 + (x - 7)^2 với ràng buộc x <= 2. Nhập điểm tối ưu x, rồi giá trị nhỏ nhất.
  - **Đáp án:** 2, 30
    1. f lồi (f'' = 6 > 0) và tập {x <= 2} lồi: bài toán lồi.
    2. Bỏ ràng buộc, f nhỏ nhất tại f'(x) = 2(3x - 12) = 0, x = 4; nhưng 4 > 2 vi phạm ràng buộc.
    3. Trên (-vô cùng, 2] có f'(x) = 6x - 24 < 0, nên f giảm và nhỏ nhất tại x = 2.
    4. f(2) = 1 + 4 + 25 = 30.
- `tr_g8_max_duong` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = max(-x - 2, -5, 4x + 7). Tìm giá trị nhỏ nhất của f trên R.
  - **Đáp án:** -1/5
    1. f là cực đại của các hàm tuyến tính nên là hàm lồi, tuyến tính từng khúc; nó có hệ số góc âm và dương nên đạt giá trị nhỏ nhất tại một điểm gãy.
    2. Điểm gãy nằm ở giao điểm của hai đường; tính f tại các giao điểm: x = 3: f = 19; x = -9/5: f = -1/5; x = -3: f = 1.
    3. Giá trị nhỏ nhất là -1/5 (tại x = -9/5).
  - **Câu hỏi:** Cho f(x) = max(-4x + 3, -3x - 3, x + 1). Tìm giá trị nhỏ nhất của f trên R.
  - **Đáp án:** 7/5
    1. f là cực đại của các hàm tuyến tính nên là hàm lồi, tuyến tính từng khúc; nó có hệ số góc âm và dương nên đạt giá trị nhỏ nhất tại một điểm gãy.
    2. Điểm gãy nằm ở giao điểm của hai đường; tính f tại các giao điểm: x = 6: f = 7; x = 2/5: f = 7/5; x = -1: f = 7.
    3. Giá trị nhỏ nhất là 7/5 (tại x = 2/5).
  - **Câu hỏi:** Cho f(x) = max(-3x + 3, x + 7, 2x - 6). Tìm giá trị nhỏ nhất của f trên R.
  - **Đáp án:** 6
    1. f là cực đại của các hàm tuyến tính nên là hàm lồi, tuyến tính từng khúc; nó có hệ số góc âm và dương nên đạt giá trị nhỏ nhất tại một điểm gãy.
    2. Điểm gãy nằm ở giao điểm của hai đường; tính f tại các giao điểm: x = -1: f = 6; x = 9/5: f = 44/5; x = 13: f = 20.
    3. Giá trị nhỏ nhất là 6 (tại x = -1).
- `tr_t8_bl_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tìm giá trị nhỏ nhất của f(x) = 3x^4 - 4x^3 - 12x^2 trên R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bl_01`, `tr_t8_dk_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 12x^3 - 12x^2 - 24x = 12x(x - 2)(x + 1).
    2. Các điểm dừng là x = -1, x = 0 và x = 2.
    3. f''(x) = 36x^2 - 24x - 24, và f''(-1) = 36 > 0, nên x = -1 là một điểm cực tiểu địa phương.
    4. Cực tiểu địa phương cũng là cực tiểu toàn cục, nên giá trị nhỏ nhất của f là f(-1) = -5.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Cực tiểu địa phương cũng là cực tiểu toàn cục, nên giá trị nhỏ nhất của f là f(-1) = -5.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng. Bước 4 sai: 'cực tiểu địa phương là toàn cục' chỉ đúng khi f lồi, mà f''(0) = -24 < 0 nên f không lồi.
    2. Phải so sánh mọi cực tiểu địa phương: f''(2) = 144 - 48 - 24 = 72 > 0, và f(2) = 48 - 32 - 48 = -32.
    3. f(x) -> +vô cùng khi |x| -> vô cùng, nên giá trị nhỏ nhất là min(f(-1), f(2)) = -32, tại x = 2.
- `tr_t8_bl_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét bài toán min f(x, y) = (x - 3)^2 + (y - 2)^2 với ràng buộc x + y <= 3.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bl_02`, `tr_t8_bl_03`
  - **Phần a** (Đúng/Sai): a) Đây là một bài toán tối ưu lồi.
    - **Đáp án a:** Đúng
  - **Phần b** (Điền số): b) Nhập nghiệm tối ưu x, y.
    - **Đáp án b:** 2, 1
  - **Phần c** (Điền số): c) Giá trị nhỏ nhất của f bằng bao nhiêu?
    - **Đáp án c:** 2
  - **Lời giải:**
    1. a) f là tổng bình phương nên lồi; {x + y <= 3} là nửa mặt phẳng nên lồi. Đúng.
    2. b) Bỏ ràng buộc thì f nhỏ nhất tại (3, 2), nhưng 3 + 2 = 5 > 3. Vậy nghiệm nằm trên đường x + y = 3 và là điểm gần (3, 2) nhất: chiếu (3, 2) theo hướng (1, 1), (3, 2) - ((5 - 3)/2)(1, 1) = (2, 1).
    3. Kiểm tra điều kiện tối ưu: grad f(2, 1) = (-2, -2) = -2 . (1, 1), ngược hướng với pháp tuyến (1, 1) của ràng buộc, nên không có hướng chấp nhận được nào làm f giảm.
    4. c) f(2, 1) = 1 + 1 = 2.
- `tr_g8_toan_cuc` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = 4x^2 + 2xy + 4y^2 + 4x - 2y. Khẳng định: điểm (-3/5, 2/5) là điểm cực tiểu toàn cục của f trên R^2.
  - **Đáp án:** Đúng
    1. Gradient tại (-3/5, 2/5): f_x = 0, f_y = 0.
    2. Ma trận Hesse H = [8, 2; 2, 8], det H = 60.
    3. Gradient bằng 0 và H xác định dương (phần tử chéo dương, det H > 0): f lồi, nên điểm dừng là cực tiểu toàn cục. Khẳng định đúng.
  - **Câu hỏi:** Cho f(x, y) = x^2 + y^2 - 3x + y. Khẳng định: điểm (3/2, -1/2) là điểm cực tiểu toàn cục của f trên R^2.
  - **Đáp án:** Đúng
    1. Gradient tại (3/2, -1/2): f_x = 0, f_y = 0.
    2. Ma trận Hesse H = [2, 0; 0, 2], det H = 4.
    3. Gradient bằng 0 và H xác định dương (phần tử chéo dương, det H > 0): f lồi, nên điểm dừng là cực tiểu toàn cục. Khẳng định đúng.
  - **Câu hỏi:** Cho f(x, y) = 2x^2 + 4xy + 3y^2 + 7x - 6y. Khẳng định: điểm (-33/4, 13/2) là điểm cực tiểu toàn cục của f trên R^2.
  - **Đáp án:** Đúng
    1. Gradient tại (-33/4, 13/2): f_x = 0, f_y = 0.
    2. Ma trận Hesse H = [4, 4; 4, 6], det H = 8.
    3. Gradient bằng 0 và H xác định dương (phần tử chéo dương, det H > 0): f lồi, nên điểm dừng là cực tiểu toàn cục. Khẳng định đúng.

## Tầng 9: Quy hoạch tuyến tính và quy hoạch phi tuyến

34 dạng câu (22 câu viết tay, 12 bộ sinh câu); 34 chưa duyệt.

### Mô hình quy hoạch tuyến tính (`tr_t9_mo_hinh_qhtt`)

- `tr_t9_mh_01` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một lò luyện hai loại đan A và B. Mỗi mẻ đan A cần 2 giờ lửa và 3 cân linh thảo, lãi 5 linh thạch; mỗi mẻ đan B cần 4 giờ lửa và 1 cân linh thảo, lãi 4 linh thạch. Lò có 20 giờ lửa và 15 cân linh thảo, và phải luyện ít nhất 2 mẻ đan B. Số mẻ có thể không nguyên. Gọi x, y là số mẻ A, B. Mô hình nào đúng để tiền lãi lớn nhất?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_pb_04`, `tr_t8_bt_01`
    - **(đúng)** max 5x + 4y với 2x + 4y <= 20, 3x + y <= 15, y >= 2, x >= 0
    - max 5x + 4y với 2x + 3y <= 20, 4x + y <= 15, y >= 2, x >= 0
    - max 5x + 4y với 2x + 4y <= 20, 3x + y <= 15, y <= 2, x >= 0
    - min 5x + 4y với 2x + 4y >= 20, 3x + y >= 15, y >= 2, x >= 0
    - max 5x + 4y với 2x + 4y = 20, 3x + y = 15, y >= 2, x >= 0
  - **Đáp án:** max 5x + 4y với 2x + 4y <= 20, 3x + y <= 15, y >= 2, x >= 0
    1. Giờ lửa dùng: 2x + 4y, không vượt 20. Linh thảo dùng: 3x + y, không vượt 15. Ràng buộc 'ít nhất 2 mẻ B' là y >= 2; x >= 0.
    2. Hàm mục tiêu là tiền lãi 5x + 4y, cần max. Không bắt buộc dùng hết tài nguyên, nên ràng buộc là <=, không phải =.
    3. Giải thử: các đỉnh (0, 2), (13/3, 2), (4, 3), (0, 5) cho lãi 8, 89/3, 32, 20; tối ưu 32 tại x = 4, y = 3.
- `tr_t9_mh_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đưa bài toán max z = 2x1 - x2 + 3x3 với các ràng buộc x1 + x2 + x3 <= 10, 2x1 - x2 >= 3, x1 - x3 = 2, x1 >= 0, x2 <= 0, x3 không ràng buộc dấu, về dạng chính tắc (mọi ràng buộc là đẳng thức, mọi biến không âm) bằng cách ít biến nhất theo các phép biến đổi thông thường. Nhập số biến, rồi số ràng buộc đẳng thức (không kể điều kiện không âm).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bt_02`, `tr_t8_bt_01`
  - **Đáp án:** 6, 3
    1. x1 >= 0 giữ nguyên (1 biến). x2 <= 0: đặt x2 = -x2' với x2' >= 0 (1 biến). x3 tự do: x3 = x3' - x3'' với x3', x3'' >= 0 (2 biến).
    2. Ràng buộc <= thêm một biến bù s1 >= 0; ràng buộc >= trừ một biến bù s2 >= 0; ràng buộc = giữ nguyên.
    3. Tổng số biến: 1 + 1 + 2 + 2 = 6; số ràng buộc đẳng thức: 3.
- `tr_t9_mh_03` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi thành phần của bài toán quy hoạch tuyến tính với cách đưa nó về dạng chính tắc.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_pb_04`, `tr_t8_bt_01`
  - **Đáp án (ghép đúng):**
    - Ràng buộc a^T x <= b — thêm biến bù s >= 0: a^T x + s = b
    - Ràng buộc a^T x >= b — trừ biến bù s >= 0: a^T x - s = b
    - Biến x_j <= 0 — thay x_j = -x_j' với x_j' >= 0
    - Biến x_j không ràng buộc dấu — thay x_j = x_j' - x_j'' với x_j', x_j'' >= 0
    - Bài toán max f — giải min (-f), rồi đổi dấu giá trị tối ưu
  - **Lời giải:**
    1. Dạng chính tắc chỉ có ràng buộc đẳng thức và biến không âm, nên mỗi bất đẳng thức được bù bằng một biến không âm (cộng vào vế nhỏ hơn).
    2. Biến không dương được đổi dấu; biến tự do là hiệu của hai biến không âm.
    3. max f và min (-f) có cùng nghiệm, giá trị tối ưu đối dấu nhau.
- `tr_t9_mh_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: mỗi gam linh thảo A có 2 phần mộc khí và 1 phần thủy khí, giá 3; mỗi gam B có 1 phần mộc khí và 3 phần thủy khí, giá 4. Cần ít nhất 8 phần mộc khí và 9 phần thủy khí với chi phí nhỏ nhất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_pb_05`, `tr_t8_bt_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Gọi x, y là số gam A, B; x >= 0, y >= 0.
    2. Chi phí cần nhỏ nhất: min 3x + 4y.
    3. Lượng mộc khí là 2x + y và phải đạt ít nhất 8, nên 2x + y <= 8.   **<- bước sai đầu tiên**
    4. Lượng thủy khí là x + 3y và phải đạt ít nhất 9, nên x + 3y >= 9.
    5. Giải bằng hình học được nghiệm x = 0, y = 3, chi phí 12.
  - **Đáp án:** Bước 3: Lượng mộc khí là 2x + y và phải đạt ít nhất 8, nên 2x + y <= 8.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 viết ngược chiều: 'ít nhất 8' là 2x + y >= 8.
    2. Hệ quả là nghiệm (0, 3) cho chỉ 3 phần mộc khí, thiếu.
    3. Mô hình đúng min 3x + 4y với 2x + y >= 8, x + 3y >= 9, x, y >= 0 có các đỉnh (0, 8), (3, 2), (9, 0) với chi phí 32, 17, 27: tối ưu 17 tại x = 3, y = 2.
- `tr_g9_san_xuat` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Một lò luyện đan làm hai loại đan dược A và B. Mỗi cân đan A cần 2 cân linh thảo và 1 giờ lửa; mỗi cân đan B cần 5 cân linh thảo và 3 giờ lửa. Lò có 30 cân linh thảo và 9 giờ lửa. Mỗi cân đan A lãi 8 linh thạch, mỗi cân đan B lãi 8 linh thạch; số cân có thể không nguyên. Tiền lãi lớn nhất là bao nhiêu linh thạch?
  - **Đáp án:** 72
    1. Gọi x, y là số cân đan A, B. Mô hình: max z = 8x + 8y với các ràng buộc 2x + 5y <= 30, x + 3y <= 9, x >= 0, y >= 0.
    2. Miền ràng buộc là một đa giác lồi; nghiệm tối ưu nằm ở một đỉnh. Đỉnh và giá trị z: (0, 0): 0; (0, 3): 24; (9, 0): 72.
    3. Lãi lớn nhất 72 linh thạch, tại x = 9, y = 0.
  - **Câu hỏi:** Một lò luyện đan làm hai loại đan dược A và B. Mỗi cân đan A cần 5 cân linh thảo và 1 giờ lửa; mỗi cân đan B cần 2 cân linh thảo và 5 giờ lửa. Lò có 25 cân linh thảo và 27 giờ lửa. Mỗi cân đan A lãi 3 linh thạch, mỗi cân đan B lãi 7 linh thạch; số cân có thể không nguyên. Tiền lãi lớn nhất là bao nhiêu linh thạch?
  - **Đáp án:** 983/23
    1. Gọi x, y là số cân đan A, B. Mô hình: max z = 3x + 7y với các ràng buộc 5x + 2y <= 25, x + 5y <= 27, x >= 0, y >= 0.
    2. Miền ràng buộc là một đa giác lồi; nghiệm tối ưu nằm ở một đỉnh. Đỉnh và giá trị z: (0, 0): 0; (0, 27/5): 189/5; (71/23, 110/23): 983/23; (5, 0): 15.
    3. Lãi lớn nhất 983/23 linh thạch, tại x = 71/23, y = 110/23.
  - **Câu hỏi:** Một lò luyện đan làm hai loại đan dược A và B. Mỗi cân đan A cần 2 cân linh thảo và 2 giờ lửa; mỗi cân đan B cần 5 cân linh thảo và 3 giờ lửa. Lò có 23 cân linh thảo và 25 giờ lửa. Mỗi cân đan A lãi 8 linh thạch, mỗi cân đan B lãi 2 linh thạch; số cân có thể không nguyên. Tiền lãi lớn nhất là bao nhiêu linh thạch?
  - **Đáp án:** 92
    1. Gọi x, y là số cân đan A, B. Mô hình: max z = 8x + 2y với các ràng buộc 2x + 5y <= 23, 2x + 3y <= 25, x >= 0, y >= 0.
    2. Miền ràng buộc là một đa giác lồi; nghiệm tối ưu nằm ở một đỉnh. Đỉnh và giá trị z: (0, 0): 0; (0, 23/5): 46/5; (23/2, 0): 92.
    3. Lãi lớn nhất 92 linh thạch, tại x = 23/2, y = 0.

### Phương pháp hình học hai biến (`tr_t9_hinh_hoc`)

- `tr_t9_hh_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giải bằng phương pháp hình học: max z = 2x + 3y với các ràng buộc x + y <= 6, x + 3y <= 12, 2x + y <= 10, x >= 0, y >= 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_tl_03`, `tr_t8_bl_03`, `tr_t8_bt_01`
  - **Phần a** (Điền số): a) Miền ràng buộc có bao nhiêu đỉnh?
    - **Đáp án a:** 5
  - **Phần b** (Điền số): b) Giá trị tối ưu của z bằng bao nhiêu?
    - **Đáp án b:** 15
  - **Phần c** (Điền số): c) Nhập nghiệm tối ưu x, y.
    - **Đáp án c:** 3, 3
  - **Phần d** (Đúng/Sai): d) Tại nghiệm tối ưu, ràng buộc 2x + y <= 10 không chặt (còn dư).
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Các đỉnh: (0, 0); (5, 0) trên 2x + y = 10; (4, 2) là giao của 2x + y = 10 và x + y = 6; (3, 3) là giao của x + y = 6 và x + 3y = 12; (0, 4). Có 5 đỉnh (mỗi đỉnh đều thỏa mọi ràng buộc).
    2. b) z tại các đỉnh: 0, 10, 14, 15, 12. Lớn nhất là 15.
    3. c) Đạt tại (3, 3), và chỉ tại đỉnh đó.
    4. d) 2 . 3 + 3 = 9 < 10: ràng buộc còn dư 1, không chặt. Đúng.
- `tr_t9_hh_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: max z = x + 2y với x + y <= 4, x <= 3, y <= 3, x >= 0, y >= 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. Miền ràng buộc D là ngũ giác lồi có các đỉnh (0, 0), (3, 0), (3, 1), (1, 3), (0, 3).
    2. Nghiệm tối ưu phải là một điểm trong của D, vì trên biên đã có ràng buộc bị dùng hết.   **<- bước sai đầu tiên**
    3. Tại một điểm trong, cực đại cần grad z = 0, nhưng grad z = (1, 2) khác 0 ở mọi nơi.
    4. Vậy bài toán không có nghiệm tối ưu.
  - **Đáp án:** Bước 2: Nghiệm tối ưu phải là một điểm trong của D, vì trên biên đã có ràng buộc bị dùng hết.
  - **Vì sao sai, và bước đúng:**
    1. Bước 1 đúng. Bước 2 sai: hàm mục tiêu tuyến tính khác hằng không bao giờ đạt cực trị ở điểm trong (grad z khác 0), nên nghiệm tối ưu nằm trên biên, cụ thể ở một đỉnh.
    2. D đóng và bị chặn nên chắc chắn có nghiệm tối ưu.
    3. z tại các đỉnh: 0, 3, 5, 7, 6; tối ưu z = 7 tại (1, 3).
- `tr_t9_hh_03` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước giải một bài toán quy hoạch tuyến tính hai biến bằng phương pháp hình học.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_tl_01`, `tr_t8_bt_01`
  - **Đáp án (thứ tự đúng):**
    1. Vẽ đường thẳng biên của từng ràng buộc và xác định nửa mặt phẳng thỏa mãn ràng buộc đó.
    2. Lấy giao các nửa mặt phẳng để được miền ràng buộc D, một đa giác lồi.
    3. Tìm tọa độ các đỉnh của D bằng cách giải hệ hai phương trình của hai đường biên cắt nhau tại đỉnh.
    4. Tính giá trị hàm mục tiêu tại từng đỉnh.
    5. Chọn đỉnh có giá trị tốt nhất; nếu hai đỉnh kề nhau cùng tốt nhất thì mọi điểm trên cạnh nối chúng đều tối ưu.
  - **Lời giải:**
    1. Miền ràng buộc phải có trước các đỉnh, và các đỉnh phải có trước khi so sánh giá trị.
    2. Lý do chỉ cần xét đỉnh: D lồi, hàm mục tiêu tuyến tính, nên nếu bài toán có nghiệm (chẳng hạn D bị chặn) thì có một nghiệm ở đỉnh.
- `tr_t9_hh_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét bài toán quy hoạch tuyến tính hai biến có miền ràng buộc khác rỗng và bị chặn. Khi đó bài toán luôn có nghiệm tối ưu, và ít nhất một nghiệm tối ưu là một đỉnh của miền ràng buộc.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_tl_01`, `tr_t8_bl_01`
  - **Đáp án:** Đúng
    1. Miền ràng buộc là giao hữu hạn nửa mặt phẳng đóng: một đa giác lồi đóng; bị chặn nên hàm tuyến tính liên tục đạt max và min trên nó.
    2. Mọi điểm của đa giác lồi bị chặn là tổ hợp lồi của các đỉnh, nên giá trị hàm tuyến tính tại đó không vượt giá trị lớn nhất tại các đỉnh.
    3. Vậy có một đỉnh tối ưu: khẳng định đúng. Nếu miền không bị chặn, bài toán có thể không có nghiệm tối ưu.
- `tr_g9_dinh_qhtt` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán max z = 8x + 8y với các ràng buộc 5x + y <= 14, x + 4y <= 30, x >= 0, y >= 0 có đúng một nghiệm tối ưu (x, y). Nhập x, y.
  - **Đáp án:** 26/19, 136/19
    1. Liệt kê các đỉnh của miền ràng buộc rồi tính z ở mỗi đỉnh: (0, 0): 0; (0, 15/2): 60; (26/19, 136/19): 1296/19; (14/5, 0): 112/5.
    2. z lớn nhất bằng 1296/19, chỉ đạt tại một đỉnh: x = 26/19, y = 136/19.
  - **Câu hỏi:** Bài toán max z = 5x + 5y với các ràng buộc x + y <= 17, 2x + 6y <= 27, x >= 0, y >= 0 có đúng một nghiệm tối ưu (x, y). Nhập x, y.
  - **Đáp án:** 27/2, 0
    1. Liệt kê các đỉnh của miền ràng buộc rồi tính z ở mỗi đỉnh: (0, 0): 0; (0, 9/2): 45/2; (27/2, 0): 135/2.
    2. z lớn nhất bằng 135/2, chỉ đạt tại một đỉnh: x = 27/2, y = 0.
  - **Câu hỏi:** Bài toán max z = 2x + y với các ràng buộc 5x + 5y <= 10, 3x + 5y <= 21, x >= 0, y >= 0 có đúng một nghiệm tối ưu (x, y). Nhập x, y.
  - **Đáp án:** 2, 0
    1. Liệt kê các đỉnh của miền ràng buộc rồi tính z ở mỗi đỉnh: (0, 0): 0; (0, 2): 2; (2, 0): 4.
    2. z lớn nhất bằng 4, chỉ đạt tại một đỉnh: x = 2, y = 0.
- `tr_g9_gia_tri_qhtt` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải bài toán max z = 7x + 4y với các ràng buộc 2x + 5y <= 30, x + 3y <= 9, 4x + 4y <= 21, x >= 0, y >= 0. Nhập giá trị tối ưu của z.
  - **Đáp án:** 147/4
    1. Miền ràng buộc là đa giác lồi bị chặn; hàm mục tiêu tuyến tính nên đạt max tại một đỉnh.
    2. Các đỉnh (giao của hai đường biên thỏa mọi ràng buộc) và giá trị z: (0, 0): 0; (0, 3): 12; (27/8, 15/8): 249/8; (21/4, 0): 147/4.
    3. Giá trị tối ưu z = 147/4 tại (21/4, 0).
  - **Câu hỏi:** Giải bài toán max z = 4x + y với các ràng buộc x + y <= 8, 3x + 2y <= 29, 6x + 3y <= 14, x >= 0, y >= 0. Nhập giá trị tối ưu của z.
  - **Đáp án:** 28/3
    1. Miền ràng buộc là đa giác lồi bị chặn; hàm mục tiêu tuyến tính nên đạt max tại một đỉnh.
    2. Các đỉnh (giao của hai đường biên thỏa mọi ràng buộc) và giá trị z: (0, 0): 0; (0, 14/3): 14/3; (7/3, 0): 28/3.
    3. Giá trị tối ưu z = 28/3 tại (7/3, 0).
  - **Câu hỏi:** Giải bài toán max z = 2x + y với các ràng buộc 2x + 5y <= 23, 2x + 3y <= 25, 4x + 6y <= 24, x >= 0, y >= 0. Nhập giá trị tối ưu của z.
  - **Đáp án:** 12
    1. Miền ràng buộc là đa giác lồi bị chặn; hàm mục tiêu tuyến tính nên đạt max tại một đỉnh.
    2. Các đỉnh (giao của hai đường biên thỏa mọi ràng buộc) và giá trị z: (0, 0): 0; (0, 4): 4; (6, 0): 12.
    3. Giá trị tối ưu z = 12 tại (6, 0).
- `tr_g9_rang_buoc_long` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xét bài toán max z = 7x + 4y với các ràng buộc 2x + 5y <= 30, x + 3y <= 9, 4x + 4y <= 21, x >= 0, y >= 0. Khẳng định: tại nghiệm tối ưu, ràng buộc 2x + 5y <= 30 không chặt (vế trái nhỏ hơn hẳn 30).
  - **Đáp án:** Đúng
    1. Các đỉnh và giá trị z: (0, 0): 0; (0, 3): 12; (27/8, 15/8): 249/8; (21/4, 0): 147/4; nghiệm tối ưu (21/4, 0).
    2. Thay vào: 2x + 5y = 21/2 < 30.
    3. Ràng buộc lỏng (còn dư): khẳng định đúng.
  - **Câu hỏi:** Xét bài toán max z = 4x + y với các ràng buộc x + y <= 8, 3x + 2y <= 29, 6x + 3y <= 14, x >= 0, y >= 0. Khẳng định: tại nghiệm tối ưu, ràng buộc 6x + 3y <= 14 không chặt (vế trái nhỏ hơn hẳn 14).
  - **Đáp án:** Sai
    1. Các đỉnh và giá trị z: (0, 0): 0; (0, 14/3): 14/3; (7/3, 0): 28/3; nghiệm tối ưu (7/3, 0).
    2. Thay vào: 6x + 3y = 14 = 14.
    3. Ràng buộc chặt (dùng hết): khẳng định sai.
  - **Câu hỏi:** Xét bài toán max z = 2x + y với các ràng buộc 2x + 5y <= 23, 2x + 3y <= 25, 4x + 6y <= 24, x >= 0, y >= 0. Khẳng định: tại nghiệm tối ưu, ràng buộc 2x + 3y <= 25 không chặt (vế trái nhỏ hơn hẳn 25).
  - **Đáp án:** Đúng
    1. Các đỉnh và giá trị z: (0, 0): 0; (0, 4): 4; (6, 0): 12; nghiệm tối ưu (6, 0).
    2. Thay vào: 2x + 3y = 12 < 25.
    3. Ràng buộc lỏng (còn dư): khẳng định đúng.

### Phương pháp đơn hình (`tr_t9_don_hinh`)

- `tr_t9_dh_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giải max z = 2x1 + 3x2 với x1 + 2x2 <= 8, 3x1 + 2x2 <= 12, x1 >= 0, x2 >= 0 bằng phương pháp đơn hình, xuất phát từ từ vựng s1 = 8 - x1 - 2x2, s2 = 12 - 3x1 - 2x2, z = 2x1 + 3x2. Mỗi bước, biến vào có hệ số dương lớn nhất trong z, biến ra theo tỉ số nhỏ nhất. Nhập giá trị z sau bước lặp thứ nhất, rồi sau bước lặp thứ hai.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_tl_03`, `tr_t8_bt_01`
  - **Đáp án:** 12, 13
    1. Bước 1: x2 vào (hệ số 3). Tỉ số: s1: 8/2 = 4, s2: 12/2 = 6, nên s1 ra, x2 = 4. Từ vựng mới: x2 = 4 - x1/2 - s1/2, s2 = 4 - 2x1 + s1, z = 12 + x1/2 - 3s1/2.
    2. Bước 2: x1 vào (hệ số 1/2). Tỉ số: hàng x2: 4/(1/2) = 8, hàng s2: 4/2 = 2, nên s2 ra, x1 = 2, x2 = 3.
    3. z = 12 + 1 = 13, và z = 13 - 5s1/4 - s2/4 không còn hệ số dương: tối ưu tại (2, 3). Đáp số 12, 13.
- `tr_t9_dh_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ vựng hiện tại của bài toán max: s1 = 10 - x1 - 2x2; s2 = 6 - 2x1 + x2; s3 = 9 - x1 - 3x2; z = x1 + 4x2 (mọi biến không âm). Biến vào là x2. Biến nào ra và x2 nhận giá trị bao nhiêu?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_tl_03`, `tr_t8_bt_01`
    - **(đúng)** s3 ra, x2 = 3
    - s1 ra, x2 = 5
    - s2 ra, x2 = 6
    - s3 ra, x2 = 9
  - **Đáp án:** s3 ra, x2 = 3
    1. Tăng x2, giữ x1 = 0: s1 = 10 - 2x2 >= 0 cho x2 <= 5; s3 = 9 - 3x2 >= 0 cho x2 <= 3.
    2. s2 = 6 + x2 tăng theo x2, nên hàng s2 không giới hạn x2 (không lập tỉ số với hệ số không làm biến giảm).
    3. Tỉ số nhỏ nhất là 3 ở hàng s3: s3 ra, x2 = 3, z = 12. Chọn x2 = 5 sẽ làm s3 = -6 < 0.
- `tr_t9_dh_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: một bước đơn hình cho max z = 4x1 + 3x2 từ từ vựng s1 = 20 - 5x1 - 2x2, s2 = 8 - x1 - 2x2, z = 4x1 + 3x2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_tl_02`, `tr_t8_bt_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Hệ số của x1 trong z là lớn nhất (4), nên x1 vào cơ sở.
    2. Tỉ số: hàng s1 cho 20/5 = 4, hàng s2 cho 8/1 = 8.
    3. Chọn tỉ số lớn nhất là 8 để z tăng nhiều nhất: s2 ra, x1 = 8.   **<- bước sai đầu tiên**
    4. Khi đó z = 4 . 8 = 32.
  - **Đáp án:** Bước 3: Chọn tỉ số lớn nhất là 8 để z tăng nhiều nhất: s2 ra, x1 = 8.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: phải chọn tỉ số nhỏ nhất để mọi biến vẫn không âm. Với x1 = 8 thì s1 = 20 - 40 = -20 < 0, phương án không chấp nhận được.
    2. Đúng: s1 ra, x1 = 4, s2 = 4, z = 16.
    3. Bước sau x2 vào, s2 ra, đi tới tối ưu x1 = 3, x2 = 5/2, z = 39/2.
- `tr_t9_dh_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giải max z = 2x1 + 5x2 bằng phương pháp đơn hình, từ từ vựng ban đầu s1 = 6 - x1, s2 = 10 - 2x2, s3 = 16 - 2x1 - 2x2, z = 2x1 + 5x2 (mọi biến không âm). Biến vào có hệ số dương lớn nhất trong z, biến ra theo tỉ số nhỏ nhất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bt_01`, `tr_t8_tl_03`
  - **Phần a** (Trắc nghiệm): a) Ở bước lặp thứ nhất, biến nào vào?
    - **(đúng)** x2
    - x1
    - s3
    - **Đáp án a:** x2
  - **Phần b** (Trắc nghiệm): b) Ở bước lặp thứ nhất, biến nào ra?
    - **(đúng)** s2
    - s1
    - s3
    - **Đáp án b:** s2
  - **Phần c** (Điền số): c) Sau bước lặp thứ nhất, z bằng bao nhiêu?
    - **Đáp án c:** 25
  - **Phần d** (Đúng/Sai): d) Từ vựng sau bước lặp thứ nhất đã là tối ưu.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) Hệ số trong z: 2 (x1), 5 (x2); x2 vào.
    2. b) Tỉ số: s2: 10/2 = 5; s3: 16/2 = 8; s1 không chứa x2. Nhỏ nhất ở s2, nên s2 ra, x2 = 5.
    3. c) z = 5 . 5 = 25.
    4. d) Từ vựng mới: x2 = 5 - s2/2, s3 = 6 - 2x1 + s2, z = 25 + 2x1 - 5s2/2. Hệ số của x1 còn dương nên chưa tối ưu: sai. (Bước sau x1 vào, s3 ra, x1 = 3, z = 31.)
- `tr_g9_don_hinh` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải max z = 8x1 + 6x2 với các biến không âm, bằng phương pháp đơn hình, xuất phát từ từ vựng (bảng) ban đầu: s1 = 12 - 4x1; s2 = 18 - 3x2; z = 8x1 + 6x2. Biến vào là biến có hệ số dương lớn nhất trong z, biến ra theo quy tắc tỉ số nhỏ nhất. Sau bước lặp đầu tiên, nhập giá trị của biến vào rồi giá trị của z.
  - **Đáp án:** 3, 24
    1. Hệ số trong z: 8 (x1), 6 (x2); biến vào là x1.
    2. Tỉ số r / (hệ số của biến vào) ở các hàng có hệ số dương: hàng s1: 3.
    3. Tỉ số nhỏ nhất 3 ở hàng s1: s1 ra khỏi cơ sở, x1 = 3, biến kia vẫn bằng 0.
    4. z = 8 . 3 = 24. Đáp số: 3, 24.
  - **Câu hỏi:** Giải max z = 6x1 + 5x2 với các biến không âm, bằng phương pháp đơn hình, xuất phát từ từ vựng (bảng) ban đầu: s1 = 23 - 4x1 - x2; s2 = 9 - 4x2; s3 = 16 - 3x1 - 5x2; z = 6x1 + 5x2. Biến vào là biến có hệ số dương lớn nhất trong z, biến ra theo quy tắc tỉ số nhỏ nhất. Sau bước lặp đầu tiên, nhập giá trị của biến vào rồi giá trị của z.
  - **Đáp án:** 16/3, 32
    1. Hệ số trong z: 6 (x1), 5 (x2); biến vào là x1.
    2. Tỉ số r / (hệ số của biến vào) ở các hàng có hệ số dương: hàng s3: 16/3; hàng s1: 23/4.
    3. Tỉ số nhỏ nhất 16/3 ở hàng s3: s3 ra khỏi cơ sở, x1 = 16/3, biến kia vẫn bằng 0.
    4. z = 6 . (16/3) = 32. Đáp số: 16/3, 32.
  - **Câu hỏi:** Giải max z = 2x1 + 5x2 với các biến không âm, bằng phương pháp đơn hình, xuất phát từ từ vựng (bảng) ban đầu: s1 = 8 - 4x1 - 4x2; s2 = 19 - 2x1 - 4x2; z = 2x1 + 5x2. Biến vào là biến có hệ số dương lớn nhất trong z, biến ra theo quy tắc tỉ số nhỏ nhất. Sau bước lặp đầu tiên, nhập giá trị của biến vào rồi giá trị của z.
  - **Đáp án:** 2, 10
    1. Hệ số trong z: 2 (x1), 5 (x2); biến vào là x2.
    2. Tỉ số r / (hệ số của biến vào) ở các hàng có hệ số dương: hàng s1: 2; hàng s2: 19/4.
    3. Tỉ số nhỏ nhất 2 ở hàng s1: s1 ra khỏi cơ sở, x2 = 2, biến kia vẫn bằng 0.
    4. z = 5 . 2 = 10. Đáp số: 2, 10.

### Bài toán đối ngẫu (`tr_t9_doi_ngau`)

- `tr_t9_dn_01` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán gốc: max c^T x với Ax <= b, x >= 0; bài toán đối ngẫu: min b^T y với A^T y >= c, y >= 0. Nếu x chấp nhận được cho bài gốc và y chấp nhận được cho bài đối ngẫu thì c^T x <= b^T y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_02`, `tr_t8_bt_01`
  - **Đáp án:** Đúng
    1. Vì x >= 0 và A^T y >= c: c^T x <= (A^T y)^T x = y^T A x.
    2. Vì y >= 0 và Ax <= b: y^T A x <= y^T b = b^T y.
    3. Ghép lại c^T x <= b^T y: định lý đối ngẫu yếu, khẳng định đúng. Hệ quả: nếu hai giá trị bằng nhau thì cả x và y đều tối ưu.
- `tr_t9_dn_02` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán gốc là bài max. Ghép mỗi thành phần của bài gốc với thành phần tương ứng của bài toán đối ngẫu (bài min).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_02`, `tr_t8_bt_01`
  - **Đáp án (ghép đúng):**
    - Hàm mục tiêu max c^T x — hàm mục tiêu min b^T y
    - Ràng buộc thứ i dạng <= — biến đối ngẫu y_i >= 0
    - Ràng buộc thứ i dạng = — biến đối ngẫu y_i không ràng buộc dấu
    - Biến x_j >= 0 — ràng buộc đối ngẫu thứ j dạng >=
    - Biến x_j không ràng buộc dấu — ràng buộc đối ngẫu thứ j dạng =
  - **Lời giải:**
    1. Vế phải b của bài gốc thành hệ số hàm mục tiêu đối ngẫu, hệ số c thành vế phải các ràng buộc đối ngẫu, ma trận A chuyển vị.
    2. Mỗi ràng buộc gốc ứng với một biến đối ngẫu, mỗi biến gốc ứng với một ràng buộc đối ngẫu.
    3. Dấu được chọn để đối ngẫu yếu c^T x <= b^T y luôn đúng: ràng buộc <= cần y_i >= 0, ràng buộc = cho phép y_i tùy ý; biến x_j >= 0 cho ràng buộc >=, biến tự do buộc ràng buộc đẳng thức.
- `tr_t9_dn_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán gốc: max z = 3x + 4y với x + y <= 5, x + 3y <= 9, x >= 0, y >= 0. Bài toán đối ngẫu: min w = 5u + 9v với u + v >= 3, u + 3v >= 4, u >= 0, v >= 0. Một đệ tử đoán nghiệm tối ưu của bài gốc là x = 3, y = 2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_01`, `tr_t7_lu_02`, `tr_t8_bt_01`
  - **Phần a** (Điền số): a) Giá trị z tại (3, 2) bằng bao nhiêu?
    - **Đáp án a:** 17
  - **Phần b** (Điền số): b) Dùng độ lệch bù (x > 0, y > 0 nên hai ràng buộc đối ngẫu chặt), tìm u, v.
    - **Đáp án b:** 5/2, 1/2
  - **Phần c** (Đúng/Sai): c) Từ a) và b) suy ra (3, 2) đúng là nghiệm tối ưu của bài gốc.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) (3, 2) thỏa 3 + 2 = 5 <= 5 và 3 + 6 = 9 <= 9; z = 9 + 8 = 17.
    2. b) u + v = 3, u + 3v = 4: trừ được 2v = 1, v = 1/2, u = 5/2; cả hai không âm nên (u, v) chấp nhận được.
    3. c) w = 5 . 5/2 + 9 . 1/2 = 25/2 + 9/2 = 17 = z. Theo đối ngẫu yếu, mọi z <= w = 17, nên (3, 2) tối ưu: đúng.
- `tr_t9_dn_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: bài gốc max z = 3x + 4y với x + y <= 5, x + 3y <= 9, 2x + y <= 12, x >= 0, y >= 0; bài đối ngẫu min 5u + 9v + 12w với u + v + 2w >= 3, u + 3v + w >= 4, u, v, w >= 0. Tìm nghiệm đối ngẫu từ độ lệch bù.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t7_lu_02`, `tr_t8_bt_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Nghiệm tối ưu của bài gốc là x = 3, y = 2, với z = 17.
    2. Thay vào: x + y = 5 và x + 3y = 9 (chặt), còn 2x + y = 8 < 12 (lỏng).
    3. Vì x > 0 và y > 0 nên hai ràng buộc đối ngẫu chặt: u + v + 2w = 3, u + 3v + w = 4.
    4. Ràng buộc thứ ba của bài gốc lỏng nên biến đối ngẫu w của nó phải dương; chọn w = 1.   **<- bước sai đầu tiên**
    5. Giải tiếp u + v = 1, u + 3v = 3, được v = 1, u = 0.
  - **Đáp án:** Bước 4: Ràng buộc thứ ba của bài gốc lỏng nên biến đối ngẫu w của nó phải dương; chọn w = 1.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai chiều: độ lệch bù nói ràng buộc gốc lỏng thì biến đối ngẫu tương ứng bằng 0, nên w = 0.
    2. Khi đó u + v = 3, u + 3v = 4 cho v = 1/2, u = 5/2, và 5u + 9v = 17 = z.
    3. Với lời giải sai, 5 . 0 + 9 . 1 + 12 . 1 = 21 khác 17, dấu hiệu nghiệm đối ngẫu không tối ưu.
- `tr_g9_doi_ngau_gia_tri` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán gốc: max z = 8x + 8y với các ràng buộc 2x + 5y <= 30, x + 3y <= 9, x >= 0, y >= 0. Viết bài toán đối ngẫu của nó (biến đối ngẫu u, v ứng với hai ràng buộc) và nhập giá trị tối ưu của bài toán đối ngẫu.
  - **Đáp án:** 72
    1. Bài toán đối ngẫu: min w = 30u + 9v với 2u + v >= 8, 5u + 3v >= 8, u >= 0, v >= 0.
    2. Định lý đối ngẫu mạnh: bài gốc có nghiệm tối ưu thì bài đối ngẫu cũng có, và hai giá trị tối ưu bằng nhau.
    3. Giải bài gốc bằng các đỉnh: (0, 0): 0; (0, 3): 24; (9, 0): 72; max z = 72.
    4. Vậy min w = 72.
  - **Câu hỏi:** Bài toán gốc: max z = 3x + 7y với các ràng buộc 5x + 2y <= 25, x + 5y <= 27, x >= 0, y >= 0. Viết bài toán đối ngẫu của nó (biến đối ngẫu u, v ứng với hai ràng buộc) và nhập giá trị tối ưu của bài toán đối ngẫu.
  - **Đáp án:** 983/23
    1. Bài toán đối ngẫu: min w = 25u + 27v với 5u + v >= 3, 2u + 5v >= 7, u >= 0, v >= 0.
    2. Định lý đối ngẫu mạnh: bài gốc có nghiệm tối ưu thì bài đối ngẫu cũng có, và hai giá trị tối ưu bằng nhau.
    3. Giải bài gốc bằng các đỉnh: (0, 0): 0; (0, 27/5): 189/5; (71/23, 110/23): 983/23; (5, 0): 15; max z = 983/23.
    4. Vậy min w = 983/23.
  - **Câu hỏi:** Bài toán gốc: max z = 8x + 2y với các ràng buộc 2x + 5y <= 23, 2x + 3y <= 25, x >= 0, y >= 0. Viết bài toán đối ngẫu của nó (biến đối ngẫu u, v ứng với hai ràng buộc) và nhập giá trị tối ưu của bài toán đối ngẫu.
  - **Đáp án:** 92
    1. Bài toán đối ngẫu: min w = 23u + 25v với 2u + 2v >= 8, 5u + 3v >= 2, u >= 0, v >= 0.
    2. Định lý đối ngẫu mạnh: bài gốc có nghiệm tối ưu thì bài đối ngẫu cũng có, và hai giá trị tối ưu bằng nhau.
    3. Giải bài gốc bằng các đỉnh: (0, 0): 0; (0, 23/5): 46/5; (23/2, 0): 92; max z = 92.
    4. Vậy min w = 92.
- `tr_g9_doi_ngau_nghiem` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Bài toán gốc: max z = 3x + 7y với các ràng buộc x + 4y <= 27, 5x + y <= 30, x >= 0, y >= 0. Bài toán đối ngẫu: min w = 27u + 30v với u + 5v >= 3, 4u + v >= 7, u >= 0, v >= 0. Nhập nghiệm tối ưu u, v của bài toán đối ngẫu.
  - **Đáp án:** 32/19, 5/19
    1. Đỉnh và giá trị của bài gốc: (0, 0): 0; (0, 27/4): 189/4; (93/19, 105/19): 1014/19; (6, 0): 18; nghiệm tối ưu x = 93/19, y = 105/19, cả hai dương.
    2. Độ lệch bù: x > 0 nên ràng buộc đối ngẫu thứ nhất chặt, y > 0 nên ràng buộc thứ hai chặt: u + 5v = 3, 4u + v = 7.
    3. Giải hệ: u = 32/19, v = 5/19 (đều không âm). Kiểm tra: 27 . (32/19) + 30 . (5/19) = 1014/19 = max z.
  - **Câu hỏi:** Bài toán gốc: max z = 3x + 7y với các ràng buộc 5x + 2y <= 25, x + 5y <= 27, x >= 0, y >= 0. Bài toán đối ngẫu: min w = 25u + 27v với 5u + v >= 3, 2u + 5v >= 7, u >= 0, v >= 0. Nhập nghiệm tối ưu u, v của bài toán đối ngẫu.
  - **Đáp án:** 8/23, 29/23
    1. Đỉnh và giá trị của bài gốc: (0, 0): 0; (0, 27/5): 189/5; (71/23, 110/23): 983/23; (5, 0): 15; nghiệm tối ưu x = 71/23, y = 110/23, cả hai dương.
    2. Độ lệch bù: x > 0 nên ràng buộc đối ngẫu thứ nhất chặt, y > 0 nên ràng buộc thứ hai chặt: 5u + v = 3, 2u + 5v = 7.
    3. Giải hệ: u = 8/23, v = 29/23 (đều không âm). Kiểm tra: 25 . (8/23) + 27 . (29/23) = 983/23 = max z.
  - **Câu hỏi:** Bài toán gốc: max z = 2x + 3y với các ràng buộc 5x + 4y <= 29, x + 6y <= 30, x >= 0, y >= 0. Bài toán đối ngẫu: min w = 29u + 30v với 5u + v >= 2, 4u + 6v >= 3, u >= 0, v >= 0. Nhập nghiệm tối ưu u, v của bài toán đối ngẫu.
  - **Đáp án:** 9/26, 7/26
    1. Đỉnh và giá trị của bài gốc: (0, 0): 0; (0, 5): 15; (27/13, 121/26): 471/26; (29/5, 0): 58/5; nghiệm tối ưu x = 27/13, y = 121/26, cả hai dương.
    2. Độ lệch bù: x > 0 nên ràng buộc đối ngẫu thứ nhất chặt, y > 0 nên ràng buộc thứ hai chặt: 5u + v = 2, 4u + 6v = 3.
    3. Giải hệ: u = 9/26, v = 7/26 (đều không âm). Kiểm tra: 29 . (9/26) + 30 . (7/26) = 471/26 = max z.

### Nhân tử Lagrange và điều kiện KKT (`tr_t9_lagrange_kkt`)

- `tr_t9_lg_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị lớn nhất của f(x, y) = xy với ràng buộc x + 2y = c, bằng hàm Lagrange L(x, y, lambda) = xy - lambda(x + 2y - c). Trước hết lấy c = 8.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Phần a** (Điền số): a) Với c = 8, nhân tử lambda tại điểm dừng của L bằng bao nhiêu?
    - **Đáp án a:** 2
  - **Phần b** (Điền số): b) Với c = 8, nhập x, y tại điểm đạt max.
    - **Đáp án b:** 4, 2
  - **Phần c** (Điền số): c) Với c = 8, giá trị lớn nhất của f bằng bao nhiêu?
    - **Đáp án c:** 8
  - **Phần d** (Đúng/Sai): d) Giá trị lớn nhất M(c), xem như hàm của c, có đạo hàm M'(8) bằng đúng lambda ở câu a).
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. L_x = y - lambda = 0, L_y = x - 2lambda = 0, nên y = lambda, x = 2lambda. Thay vào x + 2y = 8: 4lambda = 8.
    2. a) lambda = 2. b) x = 4, y = 2. c) f = 8; đây là max vì trên đường thẳng, xy = (8 - 2y)y là parabol quay xuống.
    3. d) Tổng quát x = c/2, y = c/4, M(c) = c^2/8, M'(c) = c/4, M'(8) = 2 = lambda: đúng. Nhân tử Lagrange đo tốc độ thay đổi của giá trị tối ưu khi nới ràng buộc.
- `tr_t9_lg_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: tìm giá trị nhỏ nhất của x^2 + y^2 với ràng buộc x + y = 2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_dk_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. Lập L(x, y, lambda) = x^2 + y^2 - lambda(x + y - 2).
    2. L_x = 2x - lambda = 0 và L_y = 2y - lambda = 0, nên x = y = lambda/2.
    3. Hàm x^2 + y^2 lồi, nên chỉ cần grad f = 0: 2x = 0 và 2y = 0, tức x = y = 0.   **<- bước sai đầu tiên**
    4. Vậy lambda = 0 và giá trị nhỏ nhất bằng 0.
  - **Đáp án:** Bước 3: Hàm x^2 + y^2 lồi, nên chỉ cần grad f = 0: 2x = 0 và 2y = 0, tức x = y = 0.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: bỏ quên ràng buộc. (0, 0) không thỏa x + y = 2; điều kiện grad f = 0 chỉ dùng cho bài toán không ràng buộc.
    2. Đúng: thêm phương trình ràng buộc L_lambda = 0, tức x + y = 2, được lambda/2 + lambda/2 = 2, lambda = 2, x = y = 1.
    3. Giá trị nhỏ nhất là 1 + 1 = 2 (f lồi, ràng buộc tuyến tính nên điểm dừng của L là cực tiểu toàn cục).
- `tr_t9_lg_03` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm cực trị của f(x, y) với một ràng buộc đẳng thức bằng phương pháp nhân tử Lagrange.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_dk_03`
  - **Đáp án (thứ tự đúng):**
    1. Viết ràng buộc dưới dạng g(x, y) = 0.
    2. Lập hàm Lagrange L(x, y, lambda) = f(x, y) - lambda . g(x, y).
    3. Giải hệ ba phương trình L_x = 0, L_y = 0, g(x, y) = 0.
    4. Tính f tại mọi nghiệm (x, y) tìm được.
    5. So sánh các giá trị đó (và xét tính lồi hoặc dáng điệu ở vô cùng) để kết luận đâu là cực tiểu, đâu là cực đại.
  - **Lời giải:**
    1. Phải có g mới lập được L; phải có L mới lập được hệ.
    2. Hệ cho các ứng viên; chỉ sau khi tính f tại chúng mới so sánh được.
    3. Điều kiện Lagrange chỉ là điều kiện cần, nên bước so sánh cuối không được bỏ.
- `tr_g9_kkt` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Xét bài toán min f(x, y) = (x + 3)^2 + (y - 4)^2 với ràng buộc x + y <= -5. Khẳng định: nghiệm tối ưu là điểm (-3, 4).
  - **Đáp án:** Sai
    1. Bỏ ràng buộc thì f nhỏ nhất (bằng 0) tại (-3, 4). Kiểm tra: x + y tại đó bằng 1, > -5.
    2. (-3, 4) vi phạm ràng buộc, nên tại nghiệm ràng buộc chặt (mu > 0): nghiệm là hình chiếu của (-3, 4) lên đường thẳng x + y = -5, tức (-6, 1), với mu = 6.
    3. Khẳng định sai.
  - **Câu hỏi:** Xét bài toán min f(x, y) = (x + 5)^2 + (y + 4)^2 với ràng buộc x + y <= -4. Khẳng định: nghiệm tối ưu là điểm (-5/2, -3/2).
  - **Đáp án:** Sai
    1. Bỏ ràng buộc thì f nhỏ nhất (bằng 0) tại (-5, -4). Kiểm tra: x + y tại đó bằng -9, <= -4.
    2. (-5, -4) thỏa ràng buộc nên là nghiệm, với nhân tử mu = 0 và ràng buộc không chặt.
    3. Khẳng định sai.
  - **Câu hỏi:** Xét bài toán min f(x, y) = (x + 2)^2 + (y - 4)^2 với ràng buộc 2x + y <= 3. Khẳng định: nghiệm tối ưu là điểm (-2, 4).
  - **Đáp án:** Đúng
    1. Bỏ ràng buộc thì f nhỏ nhất (bằng 0) tại (-2, 4). Kiểm tra: 2x + y tại đó bằng 0, <= 3.
    2. (-2, 4) thỏa ràng buộc nên là nghiệm, với nhân tử mu = 0 và ràng buộc không chặt.
    3. Khẳng định đúng.
- `tr_g9_lagrange` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = x^2 + 3y^2 với ràng buộc -3x + y = 8. Nhập x, y tại điểm đạt min, rồi giá trị nhỏ nhất.
  - **Đáp án:** -18/7, 2/7, 48/7
    1. L(x, y, lambda) = x^2 + 3y^2 - lambda(-3x + y - 8).
    2. L_x = 2x - (-3)lambda = 0, L_y = 6y - 1lambda = 0, nên x = -3/2lambda, y = 1/6lambda.
    3. Thay vào ràng buộc: lambda = 12/7, x = -18/7, y = 2/7.
    4. f là hàm lồi chặt và ràng buộc tuyến tính, nên điểm này là cực tiểu toàn cục: f = 48/7.
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = x^2 + y^2 với ràng buộc -x - 2y = 12. Nhập x, y tại điểm đạt min, rồi giá trị nhỏ nhất.
  - **Đáp án:** -12/5, -24/5, 144/5
    1. L(x, y, lambda) = x^2 + y^2 - lambda(-x - 2y - 12).
    2. L_x = 2x - (-1)lambda = 0, L_y = 2y - (-2)lambda = 0, nên x = -1/2lambda, y = -1lambda.
    3. Thay vào ràng buộc: lambda = 24/5, x = -12/5, y = -24/5.
    4. f là hàm lồi chặt và ràng buộc tuyến tính, nên điểm này là cực tiểu toàn cục: f = 144/5.
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của f(x, y) = 2x^2 + 3y^2 với ràng buộc 2x + y = 11. Nhập x, y tại điểm đạt min, rồi giá trị nhỏ nhất.
  - **Đáp án:** 33/7, 11/7, 363/7
    1. L(x, y, lambda) = 2x^2 + 3y^2 - lambda(2x + y - 11).
    2. L_x = 4x - 2lambda = 0, L_y = 6y - 1lambda = 0, nên x = 1/2lambda, y = 1/6lambda.
    3. Thay vào ràng buộc: lambda = 66/7, x = 33/7, y = 11/7.
    4. f là hàm lồi chặt và ràng buộc tuyến tính, nên điểm này là cực tiểu toàn cục: f = 363/7.

### Hạ gradient và hàm mất mát (`tr_t9_gradient_descent`)

- `tr_t9_gd_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mô hình y = wx được học từ hai điểm (1, 2) và (2, 3) bằng hàm mất mát L(w) = (w . 1 - 2)^2 + (w . 2 - 3)^2. Chạy hạ gradient từ w0 = 0 với bước học 1/20.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_bl_03`
  - **Phần a** (Điền số): a) L'(w0) bằng bao nhiêu?
    - **Đáp án a:** -16
  - **Phần b** (Điền số): b) w1 = w0 - (1/20) . L'(w0) bằng bao nhiêu?
    - **Đáp án b:** 4/5
  - **Phần c** (Đúng/Sai): c) L(w1) < L(w0).
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Điểm cực tiểu w* của L bằng bao nhiêu?
    - **Đáp án d:** 8/5
  - **Lời giải:**
    1. a) L'(w) = 2(w - 2) + 4(2w - 3) = 10w - 16, nên L'(0) = -16.
    2. b) w1 = 0 - (1/20)(-16) = 4/5.
    3. c) L(0) = 4 + 9 = 13; L(4/5) = (-6/5)^2 + (-7/5)^2 = 36/25 + 49/25 = 17/5 < 13: đúng.
    4. d) L'' = 10 > 0 nên L lồi; L'(w) = 0 cho w* = 16/10 = 8/5. Bước học nhỏ (1/20 < 2/10) nên dãy w_k tiến dần về 8/5.
- `tr_t9_gd_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau có một bước sai. Bước đầu tiên bị sai là bước nào? Đề bài: chạy hạ gradient cho f(x) = 5x^2 từ x0 = 1 với bước học 3/10.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_02`, `tr_t8_dk_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 10x.
    2. x1 = x0 - (3/10) . 10x0 = -2x0 = -2.
    3. Tương tự x2 = -2x1 = 4.
    4. Hạ gradient luôn đi theo hướng làm f giảm, nên f(x0) > f(x1) > f(x2) và dãy hội tụ về điểm cực tiểu 0.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Hạ gradient luôn đi theo hướng làm f giảm, nên f(x0) > f(x1) > f(x2) và dãy hội tụ về điểm cực tiểu 0.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng: x_(k+1) = (1 - 3)x_k = -2x_k.
    2. Bước 4 sai: hướng -f'(x) chỉ làm f giảm khi bước đủ nhỏ. Ở đây f(x0) = 5, f(x1) = 20, f(x2) = 80: f tăng.
    3. |x_k| = 2^k tăng mãi: thuật toán phân kỳ. Với f = 5x^2 cần bước học nhỏ hơn 1/5 (khi đó |1 - 10 . bước| < 1).
- `tr_t9_gd_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chạy hạ gradient x mới = x - eta . f'(x) cho f(x) = 2x^2 từ x0 = 1. Với bước học eta nào dãy x_k nhảy qua lại mãi giữa 1 và -1?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_hesse`
    - **(đúng)** eta = 1/2
    - eta = 1/4
    - eta = 1/8
    - eta = 1
  - **Đáp án:** eta = 1/2
    1. f'(x) = 4x, nên x mới = (1 - 4 eta)x.
    2. eta = 1/2: hệ số -1, x_k = 1, -1, 1, ...: nhảy qua lại mãi, f không giảm.
    3. eta = 1/8: hệ số 1/2, hội tụ đơn điệu; eta = 1/4: hệ số 0, tới 0 sau một bước; eta = 1: hệ số -3, phân kỳ.
- `tr_g9_gd_buoc` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chạy hạ gradient cho f(x, y) = 2x^2 + y^2 - 2x - 5y từ điểm (0, 3) với bước học 1/10: mỗi bước thay điểm p bằng p - 1/10 . grad f(p). Sau 2 bước, nhập tọa độ x, y của điểm.
  - **Đáp án:** 8/25, 141/50
    1. grad f(x, y) = (4x - 2, 2y - 5).
    2. Bước 1: gradient tại (0, 3) là (-2, 1); điểm mới (0 - 1/10 . (-2), 3 - 1/10 . 1) = (1/5, 29/10).
    3. Bước 2: gradient tại (1/5, 29/10) là (-6/5, 4/5); điểm mới (1/5 - 1/10 . (-6/5), 29/10 - 1/10 . (4/5)) = (8/25, 141/50).
  - **Câu hỏi:** Chạy hạ gradient cho f(x, y) = x^2 + y^2 - 5x - y từ điểm (3, -2) với bước học 1/8: mỗi bước thay điểm p bằng p - 1/8 . grad f(p). Sau 2 bước, nhập tọa độ x, y của điểm.
  - **Đáp án:** 89/32, -29/32
    1. grad f(x, y) = (2x - 5, 2y - 1).
    2. Bước 1: gradient tại (3, -2) là (1, -5); điểm mới (3 - 1/8 . 1, -2 - 1/8 . (-5)) = (23/8, -11/8).
    3. Bước 2: gradient tại (23/8, -11/8) là (3/4, -15/4); điểm mới (23/8 - 1/8 . (3/4), -11/8 - 1/8 . (-15/4)) = (89/32, -29/32).
  - **Câu hỏi:** Chạy hạ gradient cho f(x, y) = 2x^2 + 2y^2 - x + 3y từ điểm (0, 2) với bước học 1/4: mỗi bước thay điểm p bằng p - 1/4 . grad f(p). Sau 1 bước, nhập tọa độ x, y của điểm.
  - **Đáp án:** 1/4, -3/4
    1. grad f(x, y) = (4x - 1, 4y + 3).
    2. Bước 1: gradient tại (0, 2) là (-1, 11); điểm mới (0 - 1/4 . (-1), 2 - 1/4 . 11) = (1/4, -3/4).
- `tr_g9_gd_hoi_tu` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chạy hạ gradient cho f(x) = 2(x + 3)^2 với bước học 3/8 (mỗi bước x mới = x - 3/8 . f'(x)). Khẳng định: với mọi điểm xuất phát, dãy hạ gradient hội tụ về -3.
  - **Đáp án:** Đúng
    1. f'(x) = 4(x + 3), nên (x mới + 3) = (x + 3) - 3/8 . 4(x + 3) = (-1/2)(x + 3).
    2. Khoảng cách tới -3 nhân với |-1/2| sau mỗi bước, và f nhân với 1/4.
    3. |-1/2| < 1: khoảng cách và f đều giảm dần về 0. Khẳng định đúng.
  - **Câu hỏi:** Chạy hạ gradient cho f(x) = (x + 3)^2 với bước học 1/4 (mỗi bước x mới = x - 1/4 . f'(x)). Khẳng định: xuất phát từ x0 = -5, sau một bước giá trị của f giảm hẳn.
  - **Đáp án:** Đúng
    1. f'(x) = 2(x + 3), nên (x mới + 3) = (x + 3) - 1/4 . 2(x + 3) = (1/2)(x + 3).
    2. Khoảng cách tới -3 nhân với |1/2| sau mỗi bước, và f nhân với 1/4.
    3. |1/2| < 1: khoảng cách và f đều giảm dần về 0. Khẳng định đúng.
  - **Câu hỏi:** Chạy hạ gradient cho f(x) = 2(x - 4)^2 với bước học 1/4 (mỗi bước x mới = x - 1/4 . f'(x)). Khẳng định: xuất phát từ x0 = 6, sau một bước giá trị của f giảm hẳn.
  - **Đáp án:** Đúng
    1. f'(x) = 4(x - 4), nên (x mới - 4) = (x - 4) - 1/4 . 4(x - 4) = 0(x - 4).
    2. Khoảng cách tới 4 nhân với |0| sau mỗi bước, và f nhân với 0.
    3. |0| < 1: khoảng cách và f đều giảm dần về 0. Khẳng định đúng.
- `tr_g9_mat_mat` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Mô hình y = wx được học từ các điểm (-1, 2), (1, -3) bằng hàm mất mát L(w) = tổng các (wx_i - y_i)^2. Từ w0 = 1, chạy một bước hạ gradient với bước học 1/50. Nhập w1, rồi điểm cực tiểu w* của L.
  - **Đáp án:** 18/25, -5/2
    1. L'(w) = 2 tổng x_i(wx_i - y_i) = 2(w . 2 - (-5)), vì tổng x_i^2 = 2 và tổng x_i y_i = -5.
    2. L'(1) = 2(1 . 2 - (-5)) = 14.
    3. w1 = 1 - 1/50 . 14 = 18/25.
    4. L là parabol quay lên (lồi), cực tiểu khi L'(w) = 0: w* = -5/2 = -5/2.
  - **Câu hỏi:** Mô hình y = wx được học từ các điểm (1, 5), (-2, -1) bằng hàm mất mát L(w) = tổng các (wx_i - y_i)^2. Từ w0 = 3, chạy một bước hạ gradient với bước học 1/40. Nhập w1, rồi điểm cực tiểu w* của L.
  - **Đáp án:** 13/5, 7/5
    1. L'(w) = 2 tổng x_i(wx_i - y_i) = 2(w . 5 - 7), vì tổng x_i^2 = 5 và tổng x_i y_i = 7.
    2. L'(3) = 2(3 . 5 - 7) = 16.
    3. w1 = 3 - 1/40 . 16 = 13/5.
    4. L là parabol quay lên (lồi), cực tiểu khi L'(w) = 0: w* = 7/5 = 7/5.
  - **Câu hỏi:** Mô hình y = wx được học từ các điểm (-1, -2), (-2, 5) bằng hàm mất mát L(w) = tổng các (wx_i - y_i)^2. Từ w0 = 2, chạy một bước hạ gradient với bước học 1/50. Nhập w1, rồi điểm cực tiểu w* của L.
  - **Đáp án:** 32/25, -8/5
    1. L'(w) = 2 tổng x_i(wx_i - y_i) = 2(w . 5 - (-8)), vì tổng x_i^2 = 5 và tổng x_i y_i = -8.
    2. L'(2) = 2(2 . 5 - (-8)) = 36.
    3. w1 = 2 - 1/50 . 36 = 32/25.
    4. L là parabol quay lên (lồi), cực tiểu khi L'(w) = 0: w* = -8/5 = -8/5.

## Tầng 10: Mở rộng: phương pháp tính

53 dạng câu (43 câu viết tay, 10 bộ sinh câu); 53 chưa duyệt.

### Sai số và chữ số đáng tin (`tr_t10_sai_so`)

- `tr_t10_ss_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đo chiều dài một thanh gỗ được x = 12.5 m với sai số tuyệt đối Delta_x = 0.05 m. Tính sai số tương đối delta_x = Delta_x/|x|. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t4_o_04`
  - **Đáp án:** 1/250
    1. Sai số tương đối là tỉ số giữa sai số tuyệt đối và giá trị: 0.05/12.5 = 0.004 = 1/250 (tức 0.4%).
    2. Sai số tuyệt đối có đơn vị của đại lượng (m); sai số tương đối không có đơn vị và cho biết độ chính xác tương đối.
- `tr_t10_ss_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chiều dài x = 10 với sai số tuyệt đối 0.1 và chiều rộng y = 5 với sai số tuyệt đối 0.05. Dùng công thức bậc nhất Delta_A = |y| Delta_x + |x| Delta_y, tính sai số tuyệt đối của diện tích A = x y. Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_bl_03`
  - **Đáp án:** 1
    1. Delta_A = 5 . 0.1 + 10 . 0.05 = 0.5 + 0.5 = 1, trong khi A = 50.
    2. Cách kiểm tra: sai số tương đối của x là 0.1/10 = 1%, của y là 0.05/5 = 1%; sai số tương đối của tích xấp xỉ tổng của chúng 2%, và 2% của 50 là 1.
- `tr_t10_ss_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai số đo x = 100.2 và y = 99.8, mỗi số có sai số tuyệt đối 0.1. Sai số tuyệt đối của hiệu x - y là Delta_x + Delta_y. Tính sai số tương đối của hiệu x - y. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t4_o_04`
  - **Đáp án:** 1/2
    1. Delta_(x-y) = 0.1 + 0.1 = 0.2 (sai số cộng, không trừ). x - y = 100.2 - 99.8 = 0.4.
    2. Sai số tương đối = 0.2/0.4 = 1/2 = 50%: hiệu của hai số gần nhau mất gần hết độ chính xác, dù mỗi số đo chỉ sai 0.1%.
- `tr_t10_ss_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cạnh hình vuông đo được x = 5 với sai số tuyệt đối 0.01. Dùng Delta_f = |f'(x)| Delta_x, tính sai số tuyệt đối của diện tích f(x) = x^2. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án:** 1/10
    1. f'(x) = 2x nên f'(5) = 10.
    2. Delta_f = 10 . 0.01 = 0.1: sai số của diện tích lớn gấp 2x = 10 lần sai số của cạnh (còn sai số tương đối chỉ gấp đôi: 2 . 0.2% = 0.4%).
- `tr_t10_ss_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sai số tuyệt đối của hiệu hai số gần đúng x - y bằng hiệu của hai sai số tuyệt đối Delta_x - Delta_y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_01`, `tr_t4_o_03`
  - **Đáp án:** Sai
    1. Sai số tuyệt đối luôn là một số không âm cho độ lệch tối đa: x thật có thể lệch +Delta_x và y thật có thể lệch -Delta_y, nên hiệu có thể lệch tới Delta_x + Delta_y.
    2. Đúng: Delta_(x - y) <= Delta_x + Delta_y, cùng công thức với tổng. Mệnh đề sai.
- `tr_t10_ss_06` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với x, y dương, sai số tương đối của tích x y xấp xỉ bằng tổng hai sai số tương đối delta_x + delta_y (xấp xỉ bậc nhất, sai số nhỏ).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_01`, `tr_t4_o_03`
  - **Đáp án:** Đúng
    1. A = x y có Delta_A ~ y Delta_x + x Delta_y; chia cho A = x y: Delta_A/A ~ Delta_x/x + Delta_y/y = delta_x + delta_y.
    2. Với thương x/y cũng vậy. Mệnh đề đúng.
- `tr_t10_ss_07` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số gần đúng a = 3.2467 có sai số tuyệt đối Delta_a = 0.004. Một chữ số hàng 10^s là đáng tin khi Delta_a <= 0.5 . 10^s. Số chữ số đáng tin của a (kể từ chữ số đầu) là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_03`, `tr_t8_hl_01`
    - **(đúng)** 3
    - 5
    - 2
    - 4
  - **Đáp án:** 3
    1. Hàng đơn vị (s = 0): 0.5 >= 0.004; hàng phần mười (s = -1): 0.05 >= 0.004; hàng phần trăm (s = -2): 0.005 >= 0.004 đều đáng tin. Hàng phần nghìn (s = -3): 0.0005 < 0.004 không đáng tin. Vậy ba chữ số 3, 2, 4 đáng tin.
    2. 5 là đếm mọi chữ số đã viết (3, 2, 4, 6, 7): chữ số 6 và 7 nằm trong vùng bất định của sai số.
    3. 2 là dừng ở hàng phần mười vì thấy 0.004 "lớn hơn" 0.001; nhưng ngưỡng của hàng phần trăm là 0.5 . 10^(-2) = 0.005 >= 0.004, nên chữ số 4 vẫn đáng tin.
    4. 4 là coi chữ số hàng phần nghìn (6) đáng tin vì sai số 0.004 "cùng cỡ" hàng này; nhưng 0.004 > 0.0005.
- `tr_t10_ss_08` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: x = 8 với sai số tuyệt đối 0.08 và y = 4 với sai số tuyệt đối 0.04. Tìm sai số tuyệt đối của thương x/y (dùng công thức bậc nhất). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t4_o_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Sai số tương đối: delta_x = 0.08/8 = 0.01 và delta_y = 0.04/4 = 0.01.
    2. Thương x/y = 8/4 = 2.
    3. Sai số tuyệt đối của thương = Delta_x/Delta_y = 0.08/0.04 = 2.   **<- bước sai đầu tiên**
    4. Vậy x/y = 2 +- 2.
  - **Đáp án:** Bước 3: Sai số tuyệt đối của thương = Delta_x/Delta_y = 0.08/0.04 = 2.
  - **Vì sao sai, và bước đúng:**
    1. Sai số của thương không là thương của các sai số. Sai số tương đối của thương xấp xỉ delta_x + delta_y = 0.02.
    2. Sai số tuyệt đối = 0.02 . 2 = 0.04, nên x/y = 2 +- 0.04 (độ chính xác 2%, chứ không phải 100%).
- `tr_t10_ss_09` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phép tính trên các số gần đúng với quy tắc tính sai số (xấp xỉ bậc nhất).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_hl_01`, `tr_t4_o_03`
  - **Đáp án (ghép đúng):**
    - Tổng hoặc hiệu x +- y — Sai số tuyệt đối: Delta_x + Delta_y
    - Tích x y hoặc thương x/y — Sai số tương đối: delta_x + delta_y
    - Lũy thừa x^n — Sai số tương đối: n lần delta_x
    - Hàm một biến f(x) — Sai số tuyệt đối: |f'(x)| Delta_x
  - **Lời giải:**
    1. Cộng, trừ cộng sai số tuyệt đối; nhân, chia cộng sai số tương đối.
    2. x^n = x . x ... x (n thừa số) nên sai số tương đối là n lần; công thức chung cho hàm là vi phân: Delta_f ~ |f'| Delta_x.
- `tr_t10_ss_10` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** x = 20 với Delta_x = 0.2 và y = 5 với Delta_y = 0.05. Sắp xếp các bước tính sai số tuyệt đối của tích A = x y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_bl_03`, `tr_t4_o_04`
  - **Đáp án (thứ tự đúng):**
    1. Tính sai số tương đối của từng thừa số: delta_x = 0.2/20 = 0.01 và delta_y = 0.05/5 = 0.01.
    2. Sai số tương đối của tích xấp xỉ tổng của chúng: delta_A = 0.01 + 0.01 = 0.02.
    3. Nhân với giá trị của tích A = 20 . 5 = 100: Delta_A = 0.02 . 100 = 2.
    4. Kết quả: A = 100 +- 2.
    5. Kiểm tra bằng công thức trực tiếp: Delta_A = y Delta_x + x Delta_y = 5 . 0.2 + 20 . 0.05 = 1 + 1 = 2.
  - **Lời giải:**
    1. Công thức của tích chạy trên sai số tương đối, nên tính các sai số tương đối trước, cộng lại, rồi mới nhân với giá trị.
    2. Hai cách (qua sai số tương đối và công thức trực tiếp) cho cùng Delta_A = 2.
- `tr_t10_ss_11` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chiều dài x = 12.5 với sai số tuyệt đối 0.05 và chiều rộng y = 4 với sai số tuyệt đối 0.02. Diện tích A = x y = 50.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t8_bl_03`
  - **Phần a** (Điền số): a) Tính sai số tương đối delta_x của x.
    - **Đáp án a:** 1/250
  - **Phần b** (Điền số): b) Tính sai số tương đối delta_y của y.
    - **Đáp án b:** 1/200
  - **Phần c** (Điền số): c) Dùng delta_A = delta_x + delta_y, tính sai số tuyệt đối Delta_A của A.
    - **Đáp án c:** 9/20
  - **Phần d** (Đúng/Sai): d) Chữ số hàng đơn vị của A = 50 là đáng tin (Delta_A <= 0.5 . 10^0).
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) 0.05/12.5 = 0.004 = 1/250.
    2. b) 0.02/4 = 0.005 = 1/200.
    3. c) delta_A = 1/250 + 1/200 = 4/1000 + 5/1000 = 9/1000; Delta_A = 9/1000 . 50 = 9/20 = 0.45 (kiểm tra: 4 . 0.05 + 12.5 . 0.02 = 0.2 + 0.25 = 0.45).
    4. d) Delta_A = 0.45 <= 0.5 = 0.5 . 10^0 nên chữ số hàng đơn vị (số 0 của 50) đáng tin; chữ số hàng phần mười thì không.
- `tr_t10_ss_12` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Căn bậc hai f(x) = sqrt(x) tại x = 100 với sai số tuyệt đối Delta_x = 0.4 (dùng Delta_f = |f'(x)| Delta_x).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Phần a** (Điền số): a) Tính f(100).
    - **Đáp án a:** 10
  - **Phần b** (Điền số): b) Tính f'(100).
    - **Đáp án b:** 1/20
  - **Phần c** (Điền số): c) Tính Delta_f.
    - **Đáp án c:** 1/50
  - **Phần d** (Đúng/Sai): d) Sai số tương đối của f bằng một nửa sai số tương đối của x.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) sqrt(100) = 10.
    2. b) f'(x) = 1/(2 sqrt(x)) nên f'(100) = 1/20.
    3. c) Delta_f = 1/20 . 0.4 = 0.02 = 1/50.
    4. d) delta_x = 0.4/100 = 0.004 và delta_f = 0.02/10 = 0.002: bằng một nửa (đúng vì căn bậc hai là lũy thừa 1/2, sai số tương đối nhân với 1/2).
- `tr_g10_chu_so_dang_tin` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Số gần đúng a = 73.98 có sai số tuyệt đối Delta_a = 0.02. Một chữ số hàng 10^s là đáng tin khi Delta_a <= 0.5 . 10^s. Số a có bao nhiêu chữ số đáng tin (tính từ chữ số đầu bên trái)? Nhập một số nguyên.
  - **Đáp án:** 3
    1. Chữ số hàng 10^s đáng tin khi 0.5 . 10^s >= 0.02, tức s >= -1 (hàng 10^-1 cho ngưỡng 0.05).
    2. Các hàng của 73.98 từ 1 xuống -2 có 4 chữ số, trong đó các hàng từ 1 đến -1 đáng tin: 3 chữ số. Các chữ số bên phải nằm trong vùng bất định của sai số.
  - **Câu hỏi:** Số gần đúng a = 12.11 có sai số tuyệt đối Delta_a = 0.6. Một chữ số hàng 10^s là đáng tin khi Delta_a <= 0.5 . 10^s. Số a có bao nhiêu chữ số đáng tin (tính từ chữ số đầu bên trái)? Nhập một số nguyên.
  - **Đáp án:** 1
    1. Chữ số hàng 10^s đáng tin khi 0.5 . 10^s >= 0.6, tức s >= 1 (hàng 10^1 cho ngưỡng 5).
    2. Các hàng của 12.11 từ 1 xuống -2 có 4 chữ số, trong đó các hàng từ 1 đến 1 đáng tin: 1 chữ số. Các chữ số bên phải nằm trong vùng bất định của sai số.
  - **Câu hỏi:** Số gần đúng a = 76.70 có sai số tuyệt đối Delta_a = 0.03. Một chữ số hàng 10^s là đáng tin khi Delta_a <= 0.5 . 10^s. Số a có bao nhiêu chữ số đáng tin (tính từ chữ số đầu bên trái)? Nhập một số nguyên.
  - **Đáp án:** 3
    1. Chữ số hàng 10^s đáng tin khi 0.5 . 10^s >= 0.03, tức s >= -1 (hàng 10^-1 cho ngưỡng 0.05).
    2. Các hàng của 76.70 từ 1 xuống -2 có 4 chữ số, trong đó các hàng từ 1 đến -1 đáng tin: 3 chữ số. Các chữ số bên phải nằm trong vùng bất định của sai số.
- `tr_g10_sai_so_ham` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đo được x = 3 với sai số tuyệt đối Delta_x = 0.1. Dùng Delta_f = |f'(x)| Delta_x, tính sai số tuyệt đối của f(x) = x^3 tại x = 3. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 27/10
    1. f'(x) = 3x^2 nên f'(3) = 27.
    2. Delta_f = 27 . 0.1 = 27/10.
  - **Câu hỏi:** Đo được x = 3 với sai số tuyệt đối Delta_x = 0.02. Dùng Delta_f = |f'(x)| Delta_x, tính sai số tuyệt đối của f(x) = x^2 tại x = 3. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 3/25
    1. f'(x) = 2x nên f'(3) = 6.
    2. Delta_f = 6 . 0.02 = 3/25.
  - **Câu hỏi:** Đo được x = 4 với sai số tuyệt đối Delta_x = 0.1. Dùng Delta_f = |f'(x)| Delta_x, tính sai số tuyệt đối của f(x) = x^3 tại x = 4. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 24/5
    1. f'(x) = 3x^2 nên f'(4) = 48.
    2. Delta_f = 48 . 0.1 = 24/5.
- `tr_g10_sai_so_phep_tinh` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hai số đo gần đúng x = 29.9 với sai số tuyệt đối Delta_x = 0.02 và y = 39.9 với sai số tuyệt đối Delta_y = 0.05. Dùng công thức Delta = Delta_x + Delta_y (sai số cộng, cả khi trừ), tính sai số tuyệt đối của hiệu x - y. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/100
    1. Delta_D = Delta_x + Delta_y = 0.02 + 0.05 = 0.07.
  - **Câu hỏi:** Hai số đo gần đúng x = 5.4 với sai số tuyệt đối Delta_x = 0.06 và y = 5.1 với sai số tuyệt đối Delta_y = 0.03. Dùng công thức Delta = Delta_x + Delta_y (sai số cộng, cả khi trừ), tính sai số tuyệt đối của tổng x + y. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 9/100
    1. Delta_S = Delta_x + Delta_y = 0.06 + 0.03 = 0.09.
  - **Câu hỏi:** Hai số đo gần đúng x = 31.1 với sai số tuyệt đối Delta_x = 0.03 và y = 28.6 với sai số tuyệt đối Delta_y = 0.06. Dùng công thức Delta = Delta_x + Delta_y (sai số cộng, cả khi trừ), tính sai số tuyệt đối của hiệu x - y. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 9/100
    1. Delta_D = Delta_x + Delta_y = 0.03 + 0.06 = 0.09.

### Phương pháp chia đôi (`tr_t10_chia_doi`)

- `tr_t10_cd_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình f(x) = 0 có nghiệm trong [1, 2]. Sau n lần chia đôi, đoạn nghiệm dài (b - a)/2^n, và lấy trung điểm của nó làm nghiệm gần đúng thì sai số không quá (b - a)/2^(n+1). Cần ít nhất bao nhiêu lần chia đôi để sai số không quá 0.001? Nhập một số nguyên.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Đáp án:** 9
    1. Cần 1/2^(n+1) <= 0.001, tức 2^(n+1) >= 1000.
    2. 2^9 = 512 < 1000 <= 1024 = 2^10, nên n + 1 >= 10, n >= 9. Vậy n = 9 (sau 9 lần: 1/2^10 = 1/1024 < 0.001; sau 8 lần: 1/512 > 0.001).
- `tr_t10_cd_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chia đôi p(x) = x^3 - 2 trên [1, 2] (p(1) = -1 < 0 < 6 = p(2)): mỗi bước tính p ở trung điểm và giữ nửa đoạn mà p đổi dấu. Sau hai lần chia đôi, đầu trái của đoạn nghiệm là bao nhiêu? Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Đáp án:** 5/4
    1. Lần 1: c = 3/2, p(3/2) = 27/8 - 2 = 11/8 > 0 (cùng dấu p(2)), nên nghiệm ở [1, 3/2].
    2. Lần 2: c = 5/4, p(5/4) = 125/64 - 2 = -3/64 < 0 (cùng dấu p(1)), nên nghiệm ở [5/4, 3/2]. Đầu trái là 5/4 (nghiệm thật 2^(1/3) = 1.2599...).
- `tr_t10_cd_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f liên tục trên [a, b] và f(a) f(b) < 0. Khi đó phương pháp chia đôi luôn cho một dãy đoạn lồng nhau, mỗi đoạn chứa một nghiệm của f, có độ dài tiến tới 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_06`, `tr_t8_dk_02`
  - **Đáp án:** Đúng
    1. Mỗi bước giữ nửa đoạn mà f đổi dấu, nên theo định lý giá trị trung gian đoạn đó vẫn chứa nghiệm; độ dài giảm một nửa mỗi bước nên tiến tới 0.
    2. Mệnh đề đúng; điều kiện cần là f liên tục (không chỉ đổi dấu).
- `tr_t10_cd_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu f liên tục trên [a, b] và f(a) f(b) > 0 (cùng dấu) thì f chắc chắn không có nghiệm trong [a, b].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_06`, `tr_t8_dk_02`
  - **Đáp án:** Sai
    1. Phản ví dụ: f(x) = x^2 - 1 trên [-2, 2]: f(-2) = f(2) = 3 > 0 nhưng f có hai nghiệm -1 và 1.
    2. Đổi dấu ở hai đầu là điều kiện đủ để có nghiệm, không phải điều kiện cần. Mệnh đề sai.
- `tr_t10_cd_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng chia đôi trên [0, 1] (đoạn dài 1). Cần ít nhất bao nhiêu lần chia đôi để trung điểm của đoạn cuối cách nghiệm không quá 10^(-4)? (sai số sau n lần không quá 1/2^(n+1))
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
    - **(đúng)** 13
    - 14
    - 4
    - 10000
  - **Đáp án:** 13
    1. Cần 1/2^(n+1) <= 10^(-4), tức 2^(n+1) >= 10000. Vì 2^13 = 8192 < 10000 <= 16384 = 2^14, nên n + 1 >= 14, n >= 13.
    2. 14 là số lần để độ dài đoạn 1/2^n <= 10^(-4) (2^14 = 16384): dùng độ dài đoạn mà quên rằng trung điểm đã sai không quá nửa độ dài.
    3. 4 là lấy số chữ số thập phân: mỗi lần chia đôi chỉ giảm sai số một nửa, không phải một chữ số thập phân.
    4. 10000 là lấy 1/sai số: số lần chia là logarit cơ số 2 của đại lượng đó, vì sai số giảm theo cấp số nhân 1/2.
- `tr_t10_cd_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chia đôi f(x) = x^2 - 3 trên [1, 2], nghiệm là sqrt(3) = 1.732... Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_03`, `tr_t8_dk_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. f(1) = -2 < 0 và f(2) = 1 > 0 nên f đổi dấu, có nghiệm trong [1, 2].
    2. Trung điểm c = 3/2 có f(3/2) = 9/4 - 3 = -3/4 < 0.
    3. f(3/2) < 0 cùng dấu với f(1), nên nghiệm nằm trong [1, 3/2].   **<- bước sai đầu tiên**
    4. Đoạn mới [1, 3/2] ngắn bằng một nửa đoạn cũ.
  - **Đáp án:** Bước 3: f(3/2) < 0 cùng dấu với f(1), nên nghiệm nằm trong [1, 3/2].
  - **Vì sao sai, và bước đúng:**
    1. Giữ nửa đoạn mà f đổi dấu: f(3/2) < 0 cùng dấu với f(1) nên f vẫn không đổi dấu trên [1, 3/2]; f đổi dấu giữa f(3/2) < 0 và f(2) > 0.
    2. Đúng: nghiệm nằm trong [3/2, 2] (và sqrt(3) = 1.732 > 1.5).
- `tr_t10_cd_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình có nghiệm trong [0, 8]. Ghép số lần chia đôi n với độ dài đoạn nghiệm sau n lần.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Đáp án (ghép đúng):**
    - n = 3 — Độ dài 1
    - n = 4 — Độ dài 1/2
    - n = 5 — Độ dài 1/4
    - n = 6 — Độ dài 1/8
  - **Lời giải:**
    1. Độ dài sau n lần là 8/2^n: n = 3 cho 8/8 = 1; n = 4 cho 1/2; n = 5 cho 1/4; n = 6 cho 1/8.
    2. Mỗi lần chia đôi giảm độ dài đúng một nửa.
- `tr_t10_cd_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước của phương pháp chia đôi cho f liên tục trên [a, b] với một sai số cho trước e.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Đáp án (thứ tự đúng):**
    1. Kiểm tra f(a) f(b) < 0, tức f đổi dấu trên [a, b].
    2. Tính trung điểm c = (a + b)/2 và f(c).
    3. Nếu f(a) f(c) < 0 đặt b = c, ngược lại đặt a = c (nếu f(c) = 0 thì dừng).
    4. Lặp lại hai bước trên cho đến khi (b - a)/2 <= e.
    5. Lấy trung điểm của đoạn cuối làm nghiệm gần đúng.
  - **Lời giải:**
    1. Điều kiện đổi dấu phải có trước khi chia; mỗi lần chia giữ nửa đổi dấu; dừng khi sai số của trung điểm (nửa độ dài đoạn) đủ nhỏ.
    2. Bước cuối dùng đúng trung điểm vì sai số của nó không quá nửa độ dài đoạn.
- `tr_t10_cd_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chia đôi p(x) = x^3 + x - 3 trên [1, 2] (p(1) = -1 < 0, p(2) = 7 > 0): mỗi bước tính p ở trung điểm và giữ nửa đoạn mà p đổi dấu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Phần a** (Điền số): a) Tính p(3/2).
    - **Đáp án a:** 15/8
  - **Phần b** (Điền số): b) Sau lần chia đầu, đầu phải của đoạn nghiệm là bao nhiêu?
    - **Đáp án b:** 3/2
  - **Phần c** (Điền số): c) Ở lần chia thứ hai tính p(5/4). Giá trị đó là bao nhiêu?
    - **Đáp án c:** 13/64
  - **Phần d** (Điền số): d) Sau hai lần chia, đoạn nghiệm dài bao nhiêu?
    - **Đáp án d:** 1/4
  - **Lời giải:**
    1. a) p(3/2) = 27/8 + 3/2 - 3 = 27/8 + 12/8 - 24/8 = 15/8 > 0.
    2. b) p(1) < 0 < p(3/2): nghiệm ở [1, 3/2], đầu phải là 3/2.
    3. c) p(5/4) = 125/64 + 5/4 - 3 = 125/64 + 80/64 - 192/64 = 13/64 > 0, nên nghiệm ở [1, 5/4].
    4. d) Sau hai lần đoạn là [1, 5/4], dài 1/4 = 1/2^2 (độ dài ban đầu 1).
- `tr_t10_cd_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nghiệm nằm trong [0, 2]. Sau n lần chia đôi, đoạn nghiệm dài 2/2^n, và trung điểm của nó cách nghiệm không quá 2/2^(n+1).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Phần a** (Điền số): a) Đoạn nghiệm dài bao nhiêu sau 5 lần chia?
    - **Đáp án a:** 1/16
  - **Phần b** (Điền số): b) Sai số tối đa của trung điểm sau 5 lần chia là bao nhiêu?
    - **Đáp án b:** 1/32
  - **Phần c** (Điền số): c) Cần ít nhất bao nhiêu lần chia để sai số không quá 0.01?
    - **Đáp án c:** 7
  - **Phần d** (Đúng/Sai): d) Thêm một lần chia đôi nữa thì cận sai số giảm đúng một nửa.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) 2/2^5 = 2/32 = 1/16.
    2. b) 2/2^6 = 1/32.
    3. c) Cần 2/2^(n+1) <= 0.01, tức 2^n >= 100; 2^6 = 64 < 100 <= 128 = 2^7, nên n = 7 (kiểm tra: n = 7 cho 2/256 = 0.0078 <= 0.01; n = 6 cho 2/128 = 0.0156 > 0.01).
    4. d) Cận là 2/2^(n+1): tăng n thêm 1 thì chia thêm cho 2. Chia đôi là hội tụ tuyến tính với hệ số 1/2.
- `tr_g10_chia_doi_dau_doan` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chia đôi f(x) = x^2 - 6 trên [2, 3] (f đổi dấu): mỗi bước tính f ở trung điểm và giữ nửa đoạn mà f đổi dấu. Sau 2 lần chia đôi, đầu phải của đoạn nghiệm là bao nhiêu? Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 5/2
    1. f(x) = x^2 - 6 có f(2) = -2 < 0 và f(3) = 3 > 0, nên nghiệm sqrt(6) nằm trong [2, 3].
    2. Lần 1: c = 5/2, f(c) = 1/4 > 0; nghiệm nằm trong [2, 5/2].
    3. Lần 2: c = 9/4, f(c) = -15/16 < 0; nghiệm nằm trong [9/4, 5/2].
    4. Sau 2 lần: [9/4, 5/2], đầu phải là 5/2.
  - **Câu hỏi:** Chia đôi f(x) = x^2 - 29 trên [5, 6] (f đổi dấu): mỗi bước tính f ở trung điểm và giữ nửa đoạn mà f đổi dấu. Sau 2 lần chia đôi, đầu trái của đoạn nghiệm là bao nhiêu? Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 21/4
    1. f(x) = x^2 - 29 có f(5) = -4 < 0 và f(6) = 7 > 0, nên nghiệm sqrt(29) nằm trong [5, 6].
    2. Lần 1: c = 11/2, f(c) = 5/4 > 0; nghiệm nằm trong [5, 11/2].
    3. Lần 2: c = 21/4, f(c) = -23/16 < 0; nghiệm nằm trong [21/4, 11/2].
    4. Sau 2 lần: [21/4, 11/2], đầu trái là 21/4.
  - **Câu hỏi:** Chia đôi f(x) = x^2 - 20 trên [4, 5] (f đổi dấu): mỗi bước tính f ở trung điểm và giữ nửa đoạn mà f đổi dấu. Sau 2 lần chia đôi, đầu phải của đoạn nghiệm là bao nhiêu? Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 9/2
    1. f(x) = x^2 - 20 có f(4) = -4 < 0 và f(5) = 5 > 0, nên nghiệm sqrt(20) nằm trong [4, 5].
    2. Lần 1: c = 9/2, f(c) = 1/4 > 0; nghiệm nằm trong [4, 9/2].
    3. Lần 2: c = 17/4, f(c) = -31/16 < 0; nghiệm nằm trong [17/4, 9/2].
    4. Sau 2 lần: [17/4, 9/2], đầu phải là 9/2.
- `tr_g10_chia_doi_so_buoc` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình f(x) = 0 có nghiệm trong một đoạn dài 3. Sau n lần chia đôi, đoạn nghiệm dài 3/2^n, và lấy trung điểm của nó làm nghiệm gần đúng thì sai số không quá 3/2^(n+1). Cần ít nhất bao nhiêu lần chia đôi để sai số không quá 0.001? Nhập một số nguyên.
  - **Đáp án:** 11
    1. Cần 3/2^(n+1) <= 0.001, tức 2^(n+1) >= 3000.
    2. 2^11 = 2048 và 2^12 = 4096: n + 1 = 12 là số mũ nhỏ nhất đủ lớn, nên n = 11 (với n = 11: 3/4096 = 3/4096 <= 0.001; với n = 10: 3/2048 = 3/2048 > 0.001).
  - **Câu hỏi:** Phương trình f(x) = 0 có nghiệm trong một đoạn dài 1. Sau n lần chia đôi, đoạn nghiệm dài 1/2^n, và lấy trung điểm của nó làm nghiệm gần đúng thì sai số không quá 1/2^(n+1). Cần ít nhất bao nhiêu lần chia đôi để sai số không quá 0.1? Nhập một số nguyên.
  - **Đáp án:** 3
    1. Cần 1/2^(n+1) <= 0.1, tức 2^(n+1) >= 10.
    2. 2^3 = 8 và 2^4 = 16: n + 1 = 4 là số mũ nhỏ nhất đủ lớn, nên n = 3 (với n = 3: 1/16 = 1/16 <= 0.1; với n = 2: 1/8 = 1/8 > 0.1).
  - **Câu hỏi:** Phương trình f(x) = 0 có nghiệm trong một đoạn dài 4. Sau n lần chia đôi, đoạn nghiệm dài 4/2^n, và lấy trung điểm của nó làm nghiệm gần đúng thì sai số không quá 4/2^(n+1). Cần ít nhất bao nhiêu lần chia đôi để sai số không quá 0.001? Nhập một số nguyên.
  - **Đáp án:** 11
    1. Cần 4/2^(n+1) <= 0.001, tức 2^(n+1) >= 4000.
    2. 2^11 = 2048 và 2^12 = 4096: n + 1 = 12 là số mũ nhỏ nhất đủ lớn, nên n = 11 (với n = 11: 4/4096 = 1/1024 <= 0.001; với n = 10: 4/2048 = 1/512 > 0.001).

### Phương pháp lặp đơn (`tr_t10_lap_don`)

- `tr_t10_ld_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phép lặp x_(n+1) = 1 + 1/x_n bắt đầu từ x_0 = 1. Tính x_3. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án:** 5/3
    1. x_1 = 1 + 1/1 = 2.
    2. x_2 = 1 + 1/2 = 3/2, x_3 = 1 + 2/3 = 5/3. (Các số 1, 2, 3/2, 5/3, 8/5, ... là tỉ số hai số Fibonacci liên tiếp, tiến tới nghiệm dương của x^2 = x + 1.)
- `tr_t10_ld_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x = g(x) với g(x) = (x^2 + 1)/4 trên đoạn [0, 1]. Tìm hệ số co q = lớn nhất của |g'(x)| trên [0, 1]. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_khoang_lom`
  - **Đáp án:** 1/2
    1. g'(x) = 2x/4 = x/2, nên |g'(x)| = x/2 tăng trên [0, 1].
    2. Lớn nhất tại x = 1: q = 1/2 < 1. Cùng với g([0, 1]) = [1/4, 1/2] nằm trong [0, 1], phép lặp x_(n+1) = g(x_n) hội tụ về nghiệm duy nhất của [0, 1] với mọi x_0 trong [0, 1].
- `tr_t10_ld_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^3 - x - 1 = 0 có nghiệm x* ~ 1.3247. Viết thành x = g(x) theo cách nào thì phép lặp x_(n+1) = g(x_n) hội tụ gần x* (|g'(x*)| < 1)?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_khoang_lom`
    - **(đúng)** g(x) = (x + 1)^(1/3)
    - g(x) = x^3 - 1
    - g(x) = 1/(x^2 - 1)
    - g(x) = (x + 1)/x^2
  - **Đáp án:** g(x) = (x + 1)^(1/3)
    1. g'(x) = 1/(3 (x + 1)^(2/3)); tại x* = 1.3247 có |g'| ~ 0.19 < 1 nên hội tụ (mỗi bước sai số giảm khoảng 5 lần).
    2. g(x) = x^3 - 1 có g'(x) = 3x^2 ~ 5.3 tại x*, lớn hơn 1: phân kỳ (x_n bị đẩy ra xa x*).
    3. g(x) = 1/(x^2 - 1) có |g'(x*)| = 2x/(x^2 - 1)^2 ~ 4.65 > 1: phân kỳ.
    4. g(x) = (x + 1)/x^2 có |g'(x*)| = (x + 2)/x^3 ~ 1.43 > 1: phân kỳ. Cả bốn đều là cách viết đúng của cùng phương trình, nhưng chỉ cách đầu có |g'| < 1.
- `tr_t10_ld_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** x* là điểm bất động của g (x* = g(x*)) và |g'(x*)| < 1. Khi đó phép lặp x_(n+1) = g(x_n) hội tụ về x* với mọi giá trị đầu x_0 (dù x_0 xa x* đến đâu).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án:** Sai
    1. Tính hút của x* chỉ cục bộ: phép lặp hội tụ khi x_0 đủ gần x*. Ví dụ g(x) = x^2 có điểm bất động 0 với g'(0) = 0, nhưng với x_0 = 2 thì x_n = 2, 4, 16, 256, ... đi ra vô cùng.
    2. Hội tụ với mọi x_0 trong một đoạn đòi hỏi g ánh xạ đoạn đó vào chính nó và |g'| <= q < 1 trên cả đoạn. Mệnh đề sai.
- `tr_t10_ld_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi phép lặp x_(n+1) = g(x_n) hội tụ về x* với g'(x*) = 0.3, sai số |x_n - x*| giảm khoảng 0.3 lần sau mỗi bước (hội tụ tuyến tính với hệ số |g'(x*)|).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án:** Đúng
    1. Theo giá trị trung bình, x_(n+1) - x* = g(x_n) - g(x*) = g'(c)(x_n - x*) với c gần x*; khi x_n gần x*, g'(c) ~ g'(x*) = 0.3.
    2. Nên mỗi bước nhân sai số với khoảng 0.3: hội tụ tuyến tính. Mệnh đề đúng.
- `tr_t10_ld_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Phép lặp x_(n+1) = x_n^2 có hai điểm bất động; phép lặp hội tụ về điểm nào khi x_0 gần điểm đó? Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t4_o_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Điểm bất động: x = x^2 cho x = 0 hoặc x = 1.
    2. g(x) = x^2 có g'(x) = 2x, nên |g'(0)| = 0 và |g'(1)| = 2.
    3. Phép lặp hội tụ về điểm có |g'| lớn hơn, tức về 1, vì bước nhảy ở đó lớn hơn.   **<- bước sai đầu tiên**
    4. Vậy x_n tiến tới 1.
  - **Đáp án:** Bước 3: Phép lặp hội tụ về điểm có |g'| lớn hơn, tức về 1, vì bước nhảy ở đó lớn hơn.
  - **Vì sao sai, và bước đúng:**
    1. Điều kiện hội tụ là |g'(x*)| < 1, không phải lớn: |g'| > 1 làm sai số nhân lên mỗi bước nên đẩy xa x*. Với g'(1) = 2 điểm 1 là điểm đẩy.
    2. Đúng: x_n hội tụ về 0 (|g'(0)| = 0 < 1) khi |x_0| < 1; còn x_0 > 1 thì x_n tăng ra vô cùng, và chỉ x_0 = 1 đứng yên.
- `tr_t10_ld_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** x* là điểm bất động của g. Ghép mỗi giá trị g'(x*) với hành vi của phép lặp x_(n+1) = g(x_n) khi x_0 gần x*.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án (ghép đúng):**
    - g'(x*) = 0.3 — Hội tụ, sai số giảm khoảng 0.3 lần mỗi bước
    - g'(x*) = -0.5 — Hội tụ, các x_n nằm xen kẽ hai bên x*
    - g'(x*) = 1.5 — Phân kỳ: các x_n rời xa x*
    - g'(x*) = 0 — Hội tụ nhanh hơn tuyến tính (bậc cao hơn)
  - **Lời giải:**
    1. x_(n+1) - x* ~ g'(x*)(x_n - x*): hệ số dương thì sai số giữ dấu, hệ số âm thì đổi dấu mỗi bước (xen kẽ).
    2. |g'| > 1 làm sai số lớn lên; g' = 0 làm số hạng bậc nhất biến mất, chỉ còn số hạng bậc hai: hội tụ ít nhất bậc hai (cách Newton ra đời).
- `tr_t10_ld_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước dùng phép lặp đơn để giải x^3 - x - 1 = 0 trên [1, 2].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_khoang_lom`
  - **Đáp án (thứ tự đúng):**
    1. Viết phương trình dưới dạng x = g(x) với g(x) = (x + 1)^(1/3).
    2. Kiểm tra g ánh xạ [1, 2] vào chính nó: g(1) = 1.26 và g(2) = 1.44 đều thuộc [1, 2], g tăng.
    3. Kiểm tra tính co: |g'(x)| = 1/(3 (x + 1)^(2/3)) <= 1/(3 . 2^(2/3)) ~ 0.21 = q < 1 trên [1, 2].
    4. Khi cả hai điều kiện đúng, chọn x_0 trong [1, 2] và lặp x_(n+1) = g(x_n).
    5. Dừng khi cận sai số q/(1 - q) |x_n - x_(n-1)| đủ nhỏ.
  - **Lời giải:**
    1. Điều kiện (ánh xạ vào chính nó, hệ số co < 1) phải được kiểm tra trước khi lặp; công thức sai số chỉ dùng được sau đó.
    2. Cận sai số sau: |x_n - x*| <= q/(1 - q) |x_n - x_(n-1)|.
- `tr_t10_ld_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phép lặp x_(n+1) = 1 + 1/x_n bắt đầu từ x_0 = 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_khoang_lom`
  - **Phần a** (Điền số): a) Tính x_1.
    - **Đáp án a:** 2
  - **Phần b** (Điền số): b) Tính x_2.
    - **Đáp án b:** 3/2
  - **Phần c** (Điền số): c) Tính x_3.
    - **Đáp án c:** 5/3
  - **Phần d** (Đúng/Sai): d) Dãy hội tụ về nghiệm dương của x^2 - x - 1 = 0 (điểm bất động của g(x) = 1 + 1/x).
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) x_1 = 1 + 1/1 = 2.
    2. b) x_2 = 1 + 1/2 = 3/2.
    3. c) x_3 = 1 + 1/(3/2) = 1 + 2/3 = 5/3.
    4. d) Điểm bất động thoả x = 1 + 1/x, tức x^2 - x - 1 = 0, x = (1 + sqrt(5))/2 ~ 1.618. |g'(x)| = 1/x^2 ~ 0.38 < 1 tại đó, và các số 1, 2, 3/2, 5/3, 8/5 xen kẽ hai bên 1.618: hội tụ.
- `tr_t10_ld_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** g(x) = (x^2 + 1)/4 và phép lặp x_(n+1) = g(x_n) bắt đầu từ x_0 = 0 trên [0, 1], nơi |g'(x)| = x/2 <= q = 1/2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_khoang_lom`
  - **Phần a** (Điền số): a) Tính x_1 = g(0).
    - **Đáp án a:** 1/4
  - **Phần b** (Điền số): b) Hệ số co q là bao nhiêu?
    - **Đáp án b:** 1/2
  - **Phần c** (Đúng/Sai): c) g ánh xạ [0, 1] vào [0, 1].
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Dùng cận tiên nghiệm |x_n - x*| <= q^n/(1 - q) . |x_1 - x_0|, tính cận cho n = 3.
    - **Đáp án d:** 1/16
  - **Lời giải:**
    1. a) g(0) = (0 + 1)/4 = 1/4.
    2. b) |g'(x)| = x/2 lớn nhất tại x = 1: q = 1/2.
    3. c) g tăng trên [0, 1] với g(0) = 1/4 và g(1) = 1/2: g([0, 1]) = [1/4, 1/2] nằm trong [0, 1].
    4. d) q^3/(1 - q) = (1/8)/(1/2) = 1/4 và |x_1 - x_0| = 1/4: cận = 1/4 . 1/4 = 1/16.
- `tr_g10_lap_don_buoc` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phép lặp x_(n+1) = 1 + 1/x_n bắt đầu từ x_0 = 3. Tính x_2. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/4
    1. x_1 = 1 + 1/3 = 4/3.
    2. x_2 = 1 + 1/(4/3) = 7/4.
  - **Câu hỏi:** Phép lặp x_(n+1) = 1 + 1/x_n bắt đầu từ x_0 = 1. Tính x_3. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 5/3
    1. x_1 = 1 + 1/1 = 2.
    2. x_2 = 1 + 1/2 = 3/2.
    3. x_3 = 1 + 1/(3/2) = 5/3.
  - **Câu hỏi:** Phép lặp x_(n+1) = 1 + 2/x_n bắt đầu từ x_0 = 3. Tính x_4. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 43/21
    1. x_1 = 1 + 2/3 = 5/3.
    2. x_2 = 1 + 2/(5/3) = 11/5.
    3. x_3 = 1 + 2/(11/5) = 21/11.
    4. x_4 = 1 + 2/(21/11) = 43/21.
- `tr_g10_lap_don_he_so_co` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho g(x) = (x^2 + 3)/8 trên đoạn [0, 3]. Tìm hệ số co q = lớn nhất của |g'(x)| trên [0, 3]. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 3/4
    1. g'(x) = 2x/8 không âm và tăng trên [0, 3], nên |g'| lớn nhất ở đầu phải x = 3.
    2. q = g'(3) = 3/4 < 1: nếu thêm g ánh xạ [0, 3] vào chính nó thì phép lặp hội tụ.
  - **Câu hỏi:** Cho g(x) = (x^2 + 3)/3 trên đoạn [0, 1]. Tìm hệ số co q = lớn nhất của |g'(x)| trên [0, 1]. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 2/3
    1. g'(x) = 2x/3 không âm và tăng trên [0, 1], nên |g'| lớn nhất ở đầu phải x = 1.
    2. q = g'(1) = 2/3 < 1: nếu thêm g ánh xạ [0, 1] vào chính nó thì phép lặp hội tụ.
  - **Câu hỏi:** Cho g(x) = (x^2 + 2)/15 trên đoạn [0, 3]. Tìm hệ số co q = lớn nhất của |g'(x)| trên [0, 3]. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 2/5
    1. g'(x) = 2x/15 không âm và tăng trên [0, 3], nên |g'| lớn nhất ở đầu phải x = 3.
    2. q = g'(3) = 2/5 < 1: nếu thêm g ánh xạ [0, 3] vào chính nó thì phép lặp hội tụ.
- `tr_g10_lap_don_hoi_tu_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^2 - 7x + 10 = 0 có hai nghiệm 2 và 5, viết thành x = g(x) với g(x) = (x^2 + 10)/7. Phép lặp x_(n+1) = g(x_n) hội tụ về nghiệm x* = 2 khi x_0 đủ gần 2.
  - **Đáp án:** Đúng
    1. g'(x) = 2x/7 nên g'(2) = 4/7 = 4/7.
    2. |g'(2)| = 4/7 < 1: 2 là điểm hút, mệnh đề đúng.
  - **Câu hỏi:** Phương trình x^2 - 8x + 7 = 0 có hai nghiệm 1 và 7, viết thành x = g(x) với g(x) = (x^2 + 7)/8. Phép lặp x_(n+1) = g(x_n) hội tụ về nghiệm x* = 7 khi x_0 đủ gần 7.
  - **Đáp án:** Sai
    1. g'(x) = 2x/8 nên g'(7) = 14/8 = 7/4.
    2. |g'(7)| = 7/4 >= 1: 7 là điểm đẩy (nghiệm lớn hơn của hai nghiệm), phép lặp rời xa nó, mệnh đề sai. Nghiệm nhỏ hơn 1 có |g'| = 1/4 < 1 nên là điểm hút.
  - **Câu hỏi:** Phương trình x^2 - 7x + 10 = 0 có hai nghiệm 2 và 5, viết thành x = g(x) với g(x) = (x^2 + 10)/7. Phép lặp x_(n+1) = g(x_n) hội tụ về nghiệm x* = 2 khi x_0 đủ gần 2.
  - **Đáp án:** Đúng
    1. g'(x) = 2x/7 nên g'(2) = 4/7 = 4/7.
    2. |g'(2)| = 4/7 < 1: 2 là điểm hút, mệnh đề đúng.

### Phương pháp Newton (`tr_t10_newton`)

- `tr_t10_nw_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp Newton x_(n+1) = x_n - f(x_n)/f'(x_n) cho f(x) = x^2 - 2 với x_0 = 1. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án:** 3/2
    1. f'(x) = 2x, f(1) = -1 và f'(1) = 2.
    2. x_1 = 1 - (-1)/2 = 1 + 1/2 = 3/2. (Công thức này viết gọn là x_(n+1) = (x_n + 2/x_n)/2: trung bình của x_n và 2/x_n.)
- `tr_t10_nw_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp Newton cho f(x) = x^2 - 2 với x_0 = 1. Tính x_2. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án:** 17/12
    1. x_1 = 3/2 (bước trước). Với x_1: f(3/2) = 9/4 - 2 = 1/4 và f'(3/2) = 3.
    2. x_2 = 3/2 - (1/4)/3 = 3/2 - 1/12 = 17/12 ~ 1.41667, so với sqrt(2) = 1.41421 (sai số khoảng 0.0025).
- `tr_t10_nw_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp Newton cho f(x) = x^3 - 10 (để tìm căn bậc ba của 10) với x_0 = 2. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án:** 13/6
    1. f(2) = 8 - 10 = -2 và f'(x) = 3x^2 nên f'(2) = 12.
    2. x_1 = 2 - (-2)/12 = 2 + 1/6 = 13/6 ~ 2.1667 (nghiệm thật 10^(1/3) = 2.1544).
- `tr_t10_nw_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với f(x) = x^3 - 2x + 2 và x_0 = 0, dãy Newton x_(n+1) = x_n - f(x_n)/f'(x_n) hội tụ về một nghiệm của f.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án:** Sai
    1. f(0) = 2, f'(0) = -2 nên x_1 = 0 - 2/(-2) = 1. Rồi f(1) = 1, f'(1) = 1 nên x_2 = 1 - 1 = 0.
    2. Dãy là 0, 1, 0, 1, ... (chu kỳ 2), không hội tụ. Newton chỉ bảo đảm hội tụ khi x_0 đủ gần nghiệm (hoặc thoả điều kiện Fourier); chọn x_0 xấu có thể không hội tụ. Mệnh đề sai.
- `tr_t10_nw_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu f'(x_n) = 0 thì không thực hiện được bước Newton tiếp theo x_(n+1) = x_n - f(x_n)/f'(x_n) (chia cho 0), dù f(x_n) khác 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án:** Đúng
    1. Đường tiếp tuyến tại x_n nằm ngang (hệ số góc 0) và không cắt trục hoành khi f(x_n) khác 0, nên không có giao điểm để lấy làm x_(n+1).
    2. Gần điểm có f' ~ 0, bước Newton cũng rất lớn và có thể văng xa. Mệnh đề đúng.
- `tr_t10_nw_06` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi phương pháp Newton hội tụ về một nghiệm đơn, tốc độ hội tụ điển hình là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
    - **(đúng)** bậc hai: số chữ số đúng xấp xỉ gấp đôi sau mỗi bước
    - tuyến tính: thêm đúng một chữ số đúng sau mỗi bước
    - tuyến tính với hệ số 1/2: sai số giảm một nửa sau mỗi bước
    - bậc ba: số chữ số đúng gấp ba sau mỗi bước
  - **Đáp án:** bậc hai: số chữ số đúng xấp xỉ gấp đôi sau mỗi bước
    1. Gần nghiệm đơn x*, e_(n+1) ~ (f''(x*)/(2 f'(x*))) e_n^2: sai số bình phương lên mỗi bước (0.1, 0.01, 0.0001, ...), nên số chữ số đúng xấp xỉ gấp đôi. Với sqrt(2): sai số 0.41, 0.086, 0.0025, 0.0000021.
    2. Hội tụ tuyến tính (hệ số cố định) là của phép lặp đơn thông thường, không phải của Newton.
    3. Hội tụ tuyến tính với hệ số 1/2 là của phương pháp chia đôi, không phải của Newton.
    4. Bậc ba cần thêm điều kiện f'' = 0 tại nghiệm hay phương pháp khác (Halley); Newton chỉ bậc hai.
- `tr_t10_nw_07` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Dùng phương pháp Newton cho f(x) = x^2 - 3 với x_0 = 2. Tính x_2. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_t4_o_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. f(x) = x^2 - 3 và f'(x) = 2x.
    2. x_1 = 2 - (2^2 - 3)/(2 . 2) = 2 - 1/4 = 7/4.
    3. x_2 = x_1 - f(x_1)/f'(x_0) = 7/4 - (1/16)/4 = 7/4 - 1/64 = 111/64.   **<- bước sai đầu tiên**
    4. Vậy x_2 = 111/64.
  - **Đáp án:** Bước 3: x_2 = x_1 - f(x_1)/f'(x_0) = 7/4 - (1/16)/4 = 7/4 - 1/64 = 111/64.
  - **Vì sao sai, và bước đúng:**
    1. Mỗi bước Newton tính lại đạo hàm tại điểm hiện tại: x_2 = x_1 - f(x_1)/f'(x_1), không dùng f'(x_0) cũ (đó là phương pháp Newton đơn giản hoá, hội tụ chậm hơn).
    2. Đúng: f(7/4) = 49/16 - 3 = 1/16 và f'(7/4) = 7/2, nên x_2 = 7/4 - (1/16)/(7/2) = 7/4 - 1/56 = 97/56 ~ 1.73214 (sqrt(3) = 1.73205).
- `tr_t10_nw_08` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phương pháp giải f(x) = 0 với cách tạo số tiếp theo của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_02`, `tr_t8_bl_01`
  - **Đáp án (ghép đúng):**
    - Chia đôi — Lấy trung điểm c rồi giữ nửa đoạn mà f đổi dấu
    - Lặp đơn — x_(n+1) = g(x_n) với x = g(x) tương đương f(x) = 0
    - Newton — x_(n+1) = x_n - f(x_n)/f'(x_n), tiếp tuyến cắt trục hoành
    - Newton cho căn bậc hai của a (f(x) = x^2 - a) — x_(n+1) = (x_n + a/x_n)/2
  - **Lời giải:**
    1. Với f(x) = x^2 - a: x - (x^2 - a)/(2x) = (2x^2 - x^2 + a)/(2x) = (x + a/x)/2, trung bình của x và a/x.
    2. Chia đôi chỉ dùng dấu của f; lặp đơn dùng một hàm g; Newton dùng cả f và f'.
- `tr_t10_nw_09` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính căn bậc hai của 2 bằng phương pháp Newton xuất phát từ x_0 = 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Đáp án (thứ tự đúng):**
    1. Viết phương trình f(x) = x^2 - 2 = 0 và tính f'(x) = 2x.
    2. Lập công thức lặp x_(n+1) = x_n - (x_n^2 - 2)/(2 x_n) = (x_n + 2/x_n)/2.
    3. Với x_0 = 1 tính x_1 = (1 + 2)/2 = 3/2.
    4. Từ x_1 = 3/2 tính x_2 = (3/2 + 4/3)/2 = 17/12.
    5. Nhận xét x_2 = 1.41667 cách sqrt(2) = 1.41421 chừng 0.0025: sai số đã bình phương lên so với x_1 (0.086).
  - **Lời giải:**
    1. Cần có công thức lặp trước khi tính; mỗi x_(n+1) dùng x_n vừa tính. Cuối cùng so với giá trị thật để thấy tốc độ hội tụ.
    2. Sai số: 0.414, 0.086, 0.0025, 0.0000021 (x_3 = 577/408): mỗi bước gần bằng bình phương bước trước nhân một hằng số nhỏ.
- `tr_t10_nw_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp Newton cho f(x) = x^3 - 2 (nghiệm 2^(1/3) = 1.2599...) với x_0 = 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t8_dk_01`, `tr_g8_diem_dung`
  - **Phần a** (Điền số): a) Tính f'(1) với f'(x) = 3x^2.
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Tính x_1.
    - **Đáp án b:** 4/3
  - **Phần c** (Điền số): c) Tính x_2.
    - **Đáp án c:** 91/72
  - **Phần d** (Đúng/Sai): d) x_2 gần 2^(1/3) hơn x_1.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) f'(1) = 3 . 1 = 3.
    2. b) f(1) = -1 nên x_1 = 1 - (-1)/3 = 4/3.
    3. c) f(4/3) = 64/27 - 2 = 10/27 và f'(4/3) = 3 . 16/9 = 16/3; x_2 = 4/3 - (10/27)/(16/3) = 4/3 - 5/72 = 96/72 - 5/72 = 91/72 ~ 1.2639.
    4. d) |x_1 - 1.2599| ~ 0.0734 còn |x_2 - 1.2599| ~ 0.0040: x_2 gần hơn nhiều.
- `tr_t10_nw_11` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** So sánh hai phương pháp tìm sqrt(2) = 1.41421356... Newton cho f(x) = x^2 - 2 từ x_0 = 1 có x_1 = 3/2, x_2 = 17/12. Chia đôi trên [1, 2] có sai số sau n lần không quá 1/2^(n+1).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `tr_t4_o_04`, `tr_t8_bl_03`
  - **Phần a** (Điền số): a) Tính x_3 của Newton (từ x_2 = 17/12).
    - **Đáp án a:** 577/408
  - **Phần b** (Đúng/Sai): b) x_2 = 17/12 cách sqrt(2) không quá 0.01.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Chia đôi cần ít nhất bao nhiêu lần để sai số không quá 10^(-6)?
    - **Đáp án c:** 19
  - **Phần d** (Đúng/Sai): d) x_3 của Newton cách sqrt(2) không quá 10^(-5).
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) x_3 = (17/12 + 2/(17/12))/2 = (17/12 + 24/17)/2 = ((289 + 288)/204)/2 = 577/408 ~ 1.4142157.
    2. b) 17/12 = 1.41667 và sqrt(2) = 1.41421: chênh khoảng 0.0025 < 0.01.
    3. c) Cần 1/2^(n+1) <= 10^(-6), tức 2^(n+1) >= 10^6; 2^19 = 524288 < 10^6 <= 1048576 = 2^20, nên n + 1 >= 20, n = 19.
    4. d) 577/408 = 1.41421569 và sqrt(2) = 1.41421356: chênh khoảng 2.1 . 10^(-6) < 10^(-5). Newton đạt trong 3 bước điều mà chia đôi cần 19 bước.
- `tr_g10_newton_buoc` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp Newton x_(n+1) = x_n - f(x_n)/f'(x_n) cho f(x) = x^2 - 12 (để tìm sqrt(12)) với x_0 = 5. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 37/10
    1. f(x) = x^2 - 12, f'(x) = 2x, nên x_(n+1) = x_n - (x_n^2 - 12)/(2 x_n) = (x_n + 12/x_n)/2.
    2. x_1 = (5 + 12/5)/2 = 37/10.
  - **Câu hỏi:** Dùng phương pháp Newton x_(n+1) = x_n - f(x_n)/f'(x_n) cho f(x) = x^2 - 6 (để tìm sqrt(6)) với x_0 = 1. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/2
    1. f(x) = x^2 - 6, f'(x) = 2x, nên x_(n+1) = x_n - (x_n^2 - 6)/(2 x_n) = (x_n + 6/x_n)/2.
    2. x_1 = (1 + 6/1)/2 = 7/2.
  - **Câu hỏi:** Dùng phương pháp Newton x_(n+1) = x_n - f(x_n)/f'(x_n) cho f(x) = x^2 - 20 (để tìm sqrt(20)) với x_0 = 5. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 9/2
    1. f(x) = x^2 - 20, f'(x) = 2x, nên x_(n+1) = x_n - (x_n^2 - 20)/(2 x_n) = (x_n + 20/x_n)/2.
    2. x_1 = (5 + 20/5)/2 = 9/2.
- `tr_g10_newton_da_thuc` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng một bước Newton x_1 = x_0 - f(x_0)/f'(x_0) cho f(x) = x^3 - 2x^2 + 3x - 7 với x_0 = 1. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/2
    1. f'(x) = 3x^2 - 4x + 3; f(1) = -5 và f'(1) = 2.
    2. x_1 = 1 - (-5)/2 = 7/2.
  - **Câu hỏi:** Dùng một bước Newton x_1 = x_0 - f(x_0)/f'(x_0) cho f(x) = x^3 + 3x^2 - 6x - 7 với x_0 = -2. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -1/2
    1. f'(x) = 3x^2 + 6x - 6; f(-2) = 9 và f'(-2) = -6.
    2. x_1 = -2 - 9/(-6) = -1/2.
  - **Câu hỏi:** Dùng một bước Newton x_1 = x_0 - f(x_0)/f'(x_0) cho f(x) = x^3 - 2x^2 + 3x + 8 với x_0 = -1. Tính x_1. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -6/5
    1. f'(x) = 3x^2 - 4x + 3; f(-1) = 2 và f'(-1) = 10.
    2. x_1 = -1 - 2/10 = -6/5.
