---
id: xs_lib_t1
title_vi: Phép thử, sự kiện và giải tích kết hợp
subject: xac_suat_thong_ke
floor: 1
summary_vi: Trước khi nói đến xác suất phải biết phép thử cho ra những kết quả nào, gọi tên các sự kiện, và đếm cho đúng: lúc nào cộng, lúc nào nhân, lúc nào thứ tự có ý nghĩa.
skills: [xs_t1_khong_gian_mau, xs_t1_quan_he_su_kien, xs_t1_quy_tac_dem, xs_t1_hoan_vi_chinh_hop, xs_t1_to_hop]
---
## Phép thử và không gian mẫu

Phép thử là một việc làm mà ta biết trước mọi kết quả có thể xảy ra nhưng không biết trước kết quả nào sẽ xảy ra: tung đồng xu, gieo xúc xắc, rút một lá bài. Tập mọi kết quả có thể của phép thử gọi là không gian mẫu, thường ký hiệu là Omega.

$$ \Omega = \{1, 2, 3, 4, 5, 6\} $$

Đó là không gian mẫu của phép gieo một con xúc xắc. Việc đầu tiên của mọi bài xác suất là nói rõ một kết quả trông như thế nào.

- Tung hai đồng xu và ghi mặt từng đồng xu: một kết quả là một cặp như SN, nên có 4 kết quả SS, SN, NS, NN.
- Lấy lần lượt hai viên bi và ghi số theo thứ tự lấy: một kết quả là cặp có thứ tự (lần 1, lần 2).
- Khi phép thử gồm nhiều phần nối tiếp, số kết quả bằng tích số khả năng của từng phần.

Ví dụ tung 2 đồng xu và gieo 1 xúc xắc:

1. Một kết quả ghi mặt của đồng xu 1, mặt của đồng xu 2 và số chấm của xúc xắc.
2. Hai đồng xu cho 2 . 2 = 4 khả năng, xúc xắc cho 6 khả năng.
3. Không gian mẫu có 4 . 6 = 24 phần tử.

Chú ý: chỉ ghi tổng số chấm của hai xúc xắc thì vẫn được một không gian mẫu {2, 3, ..., 12}, nhưng 11 kết quả đó không đồng khả năng. Ở tầng sau, muốn dùng định nghĩa cổ điển thì phải chọn không gian mẫu gồm các kết quả đồng khả năng: các cặp (xúc xắc 1, xúc xắc 2).

> Lỗi thường gặp: coi SN và NS là một kết quả. Hai đồng xu là hai vật khác nhau, kể cả khi trông giống hệt nhau, nên "đồng xu 1 sấp, đồng xu 2 ngửa" và "đồng xu 1 ngửa, đồng xu 2 sấp" là hai kết quả.

## Quan hệ giữa các sự kiện

Một sự kiện (còn gọi là biến cố) là một tập con của không gian mẫu: nó xảy ra khi kết quả của phép thử thuộc tập đó. Gieo xúc xắc, sự kiện "ra mặt chẵn" là A = {2, 4, 6}.

Từ hai sự kiện A và B lập ra các sự kiện mới:

- Tổng A + B xảy ra khi ít nhất một trong hai sự kiện xảy ra: đó là hợp của hai tập.
- Tích AB xảy ra khi cả hai cùng xảy ra: đó là giao của hai tập.
- Sự kiện đối Ā xảy ra đúng khi A không xảy ra: đó là phần còn lại của Omega.

$$ A + B = A \cup B, \quad AB = A \cap B $$

Ba quan hệ hay gặp:

- A và B xung khắc khi chúng không thể cùng xảy ra, tức AB là sự kiện không thể (không có kết quả chung).
- A kéo theo B khi hễ A xảy ra thì B xảy ra, tức mọi kết quả của A đều thuộc B.
- A và Ā là hai sự kiện đối nhau: xung khắc và tổng của chúng là sự kiện chắc chắn.

Ví dụ gieo xúc xắc với A = {2, 4, 6} (mặt chẵn) và B = {4, 5, 6} (mặt lớn hơn 3):

1. A + B = {2, 4, 5, 6}.
2. AB = {4, 6}.
3. Ā = {1, 3, 5}.
4. A xảy ra mà B không xảy ra là {2}.

Sự kiện đối của một tổng là tích các sự kiện đối: "không có A hoặc B" nghĩa là "không A và không B". Nhờ vậy, sự kiện đối của "có ít nhất một đồng xu ngửa" là "mọi đồng xu đều sấp".

> Lỗi thường gặp: viết sự kiện đối của A + B thành tổng của hai sự kiện đối. Phải là tích. Kiểm tra bằng ví dụ trên: đối của A + B là {1, 3}, đúng bằng giao của Ā = {1, 3, 5} với đối của B là {1, 2, 3}.

## Quy tắc cộng và quy tắc nhân

Hai quy tắc này là nền của mọi phép đếm.

- Quy tắc cộng: một việc được làm theo một trong hai phương án loại trừ nhau, phương án một có m cách, phương án hai có n cách, thì có m + n cách.
- Quy tắc nhân: một việc phải làm qua hai bước nối tiếp, bước một có m cách, ứng với mỗi cách đó bước hai có n cách, thì có m . n cách.

$$ m + n \quad \text{(chon mot phuong an)}, \qquad m \cdot n \quad \text{(lam ca hai buoc)} $$

Câu hỏi để chọn quy tắc: làm xong một phần đã đủ chưa? Đi tàu hoặc đi máy bay thì chọn một là đủ, nên cộng. Chọn áo rồi chọn quần thì phải làm cả hai, nên nhân.

Khi được lặp lại, mỗi vị trí có đủ mọi lựa chọn: mã gồm k ký tự lấy trong n ký tự, được lặp, có n^k mã.

Ví dụ: có bao nhiêu số có 3 chữ số khác nhau lập từ 0, 1, 2, 3, 4?

1. Hàng trăm không được là 0: có 4 cách.
2. Hàng chục khác hàng trăm, được là 0: còn 4 cách.
3. Hàng đơn vị khác hai chữ số trước: còn 3 cách.
4. Nhân lại: 4 . 4 . 3 = 48 số.

Gặp ràng buộc thì xử lý vị trí bị ràng buộc trước (ở đây là hàng trăm), rồi mới đến các vị trí tự do.

> Lỗi thường gặp: quên rằng chữ số đầu của một số không được là 0, và cho hàng trăm đủ mọi chữ số. Từ 0, 1, 2, 3, 4, 5 lập số có 3 chữ số khác nhau thì hàng trăm chỉ có 5 cách, đáp số là 5 . 5 . 4 = 100, không phải 120.

## Hoán vị và chỉnh hợp

Xếp n vật khác nhau thành một hàng: chỗ đầu có n cách, chỗ thứ hai còn n - 1 cách, cứ thế đến chỗ cuối còn 1 cách. Mỗi cách xếp là một hoán vị.

$$ P_n = n! = n (n-1) \cdots 2 \cdot 1 $$

Chọn k vật trong n vật rồi xếp chúng theo thứ tự (k chỗ khác nhau, k chức vụ khác nhau) là một chỉnh hợp chập k của n. Trong các câu hỏi của game, số đó viết là A(n, k).

$$ A_n^k = n (n-1) \cdots (n-k+1) = \frac{n!}{(n-k)!} $$

Dấu hiệu nhận ra thứ tự có ý nghĩa: đổi chỗ hai người được chọn thì ra một cách khác. Lớp trưởng An, lớp phó Bình khác với lớp trưởng Bình, lớp phó An.

Hai mẹo hay dùng:

- Hai người phải đứng cạnh nhau: buộc họ thành một khối, xếp khối như một người, rồi nhân với 2 vì trong khối đổi chỗ được.
- Hai người không được đứng cạnh nhau: đếm mọi cách rồi trừ đi các cách họ đứng cạnh nhau.

Ví dụ xếp 6 người sao cho X và Y không đứng cạnh nhau:

1. Mọi cách xếp: 6! = 720.
2. X, Y cạnh nhau: khối XY cùng 4 người xếp được 5! = 120 cách, nhân 2 vì đổi chỗ trong khối: 240.
3. Không cạnh nhau: 720 - 240 = 480.

> Lỗi thường gặp: trao huy chương vàng, bạc, đồng cho 3 trong 7 người mà lại chia cho 3!. Các huy chương khác nhau nên thứ tự có ý nghĩa: đáp số là A(7, 3) = 210, không phải 35.

## Tổ hợp

Chọn k vật trong n vật mà không kể thứ tự (chỉ quan tâm nhóm gồm những ai) là một tổ hợp chập k của n, trong game viết là C(n, k). Mỗi nhóm k vật xếp được k! thứ tự, nên số tổ hợp bằng số chỉnh hợp chia cho k!.

$$ C_n^k = \frac{A_n^k}{k!} = \frac{n!}{k!\,(n-k)!} $$

Chọn k vật để lấy cũng là chọn n - k vật để bỏ lại, nên:

$$ C_n^k = C_n^{n-k} $$

Ví dụ: một nhóm 5 nam và 4 nữ, chọn 3 người sao cho có ít nhất 1 nữ.

1. Mọi cách chọn 3 người trong 9 người: C(9, 3) = 84.
2. Các cách không có nữ nào, tức chọn 3 trong 5 nam: C(5, 3) = 10.
3. Có ít nhất 1 nữ: 84 - 10 = 74.

Khi phải chọn từ hai nhóm (ví dụ 2 bi đỏ và 1 bi xanh), chọn trong từng nhóm là các bước nối tiếp nên nhân: C(6, 2) . C(4, 1) = 15 . 4 = 60.

Bảng so sánh nhanh khi chọn 2 trong 6:

- Không kể thứ tự, không lặp: C(6, 2) = 15.
- Có thứ tự, không lặp: A(6, 2) = 30.
- Có thứ tự, được lặp: 6^2 = 36.

> Lỗi thường gặp: cộng số cách chọn của hai nhóm thay vì nhân. Lấy 2 bi đỏ trong 6 và 1 bi xanh trong 4 là phải làm cả hai việc, nên có 15 . 4 = 60 cách chứ không phải 15 + 4 = 19.
