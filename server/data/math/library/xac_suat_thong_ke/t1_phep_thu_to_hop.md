---
id: xs_lib_t1
title_vi: Phép thử, sự kiện và giải tích kết hợp
subject: xac_suat_thong_ke
floor: 1
format: 2
summary_vi: Trước khi tính xác suất phải thấy hết các kết quả và đếm cho đúng: một kết quả trông ra sao, sự kiện là tập nào, lúc nào cộng, lúc nào nhân, lúc nào thứ tự có nghĩa.
skills: [xs_t1_khong_gian_mau, xs_t1_quan_he_su_kien, xs_t1_quy_tac_dem, xs_t1_hoan_vi_chinh_hop, xs_t1_to_hop]
---
## Phép thử và không gian mẫu

:::hook
Trò Đổ Linh Thạch gieo hai xúc xắc, tổng 7 thì thắng. Muốn biết tổng 7 có dễ ra hơn tổng 2 không, trước hết phải thấy hết mọi kết quả có thể.
:::

:::figure grid
caption: 36 cặp (xúc xắc 1, xúc xắc 2), ô ghi tổng. Tổng 7: 6 ô vàng; tổng 2: 1 ô đỏ.
table "tổng"
head "1" "2" "3" "4" "5" "6"
side "1" "2" "3" "4" "5" "6"
row 2 3 4 5 6 7
row 3 4 5 6 7 8
row 4 5 6 7 8 9
row 5 6 7 8 9 10
row 6 7 8 9 10 11
row 7 8 9 10 11 12
mark cell 1 1 do
mark cell 1 6 vang
mark cell 2 5 vang
mark cell 3 4 vang
mark cell 4 3 vang
mark cell 5 2 vang
mark cell 6 1 vang
:::

:::core
Không gian mẫu Omega là mọi kết quả có thể. Nhiều vật thì một kết quả ghi từng vật, nên số kết quả là tích.
:::

Hai xúc xắc là hai vật khác nhau, kể cả khi trông giống hệt: ô (1, 2) khác ô (2, 1). Ghi riêng tổng thì chỉ còn 11 kết quả, nhưng chúng không đồng khả năng.

Ví dụ: tung 1 đồng xu rồi gieo 2 xúc xắc. Không gian mẫu có mấy phần tử?

1. Một kết quả ghi mặt đồng xu, rồi số chấm xúc xắc 1, rồi xúc xắc 2.
2. Đồng xu có 2 khả năng, mỗi xúc xắc có 6.
3. Nhân lại: 2 . 6 . 6 = 72 phần tử.

> Lỗi thường gặp: tung hai đồng xu mà gộp SN với NS. Đánh số hai đồng xu là thấy: có 4 kết quả, không phải 3.

:::check
Q: Nhìn hình: tổng 8 có bao nhiêu ô? Tổng 8 dễ ra gấp mấy lần tổng 2?
A: 5 ô: (2, 6), (3, 5), (4, 4), (5, 3), (6, 2). Gấp 5 lần, vì tổng 2 chỉ có ô (1, 1).
:::

## Quan hệ giữa các sự kiện

:::hook
Bộ lọc thư chặn một thư nếu có đường link lạ HOẶC người gửi lạ; gắn cờ đỏ nếu có CẢ HAI. "Hoặc" là gom lại, "và" là lấy phần chung.
:::

:::figure sets
caption: Gieo xúc xắc. Vàng là AB = {4, 6}; cả hai hình tròn là A + B; 1, 3 nằm ngoài.
size: 190 95
universe: "Omega"
set A "A: chẵn" xanh
set B "B: > 3" do
shade A&B vang
in A-B "2"
in A&B "4, 6"
in B-A "5"
in ~(A|B) "1, 3"
:::

:::core
Sự kiện là tập con của Omega: A + B là hợp (ít nhất một xảy ra), AB là giao (cả hai), Ā là phần ngoài A.
:::

- Xung khắc: AB rỗng, hai hình không chạm nhau.
- A kéo theo B: hình A nằm trọn trong B.
- Đối nhau: xung khắc và gộp lại đủ Omega.

Ví dụ: với A, B ở hình, tìm đối của A + B.

1. A + B = {2, 4, 5, 6}, phần còn lại là {1, 3}.
2. Ā = {1, 3, 5}, đối của B là {1, 2, 3}: giao của chúng cũng là {1, 3}.

> Lỗi thường gặp: lấy đối của A + B bằng tổng hai sự kiện đối. "Không (A hoặc B)" là "không A VÀ không B": phải lấy giao.

:::check
Q: Gieo xúc xắc. A = {1, 2}, B = {5, 6}. A và B có xung khắc không? Có đối nhau không?
A: Xung khắc, vì không có mặt chung. Không đối nhau: gộp lại thiếu mặt 3 và 4.
:::

## Quy tắc cộng và quy tắc nhân

:::hook
Thử mô hình với 3 tốc độ học và 2 cỡ lô dữ liệu: mỗi cấu hình phải chọn đủ cả hai. Lưới thử có bao nhiêu cấu hình?
:::

:::figure graph
caption: Mỗi tốc độ học mở ra 2 nhánh cỡ lô: 3 . 2 = 6 lá, mỗi lá là một cấu hình.
layout: ltr
node R "chọn"
node L1 "0.1"
node L2 "0.01"
node L3 "0.001"
node A1 "lô 32"
node A2 "lô 64"
node B1 "lô 32"
node B2 "lô 64"
node C1 "lô 32"
node C2 "lô 64"
edge R L1 xanh
edge R L2 xanh
edge R L3 xanh
edge L1 A1
edge L1 A2
edge L2 B1
edge L2 B2
edge L3 C1
edge L3 C2
:::

:::core
Chỉ chọn MỘT trong các phương án thì cộng; phải làm XONG mọi bước nối tiếp thì nhân.
:::

Đi tàu (3 chuyến) hoặc máy bay (2 chuyến): chọn một là xong, 3 + 2 = 5 cách. Mã k ký tự lấy trong n ký tự, được lặp: n^k mã.

Ví dụ: lập số có 3 chữ số khác nhau từ 0, 1, 2, 3.

1. Hàng trăm khác 0 (vị trí bị ràng buộc làm trước): 3 cách.
2. Hàng chục khác hàng trăm, được là 0: còn 3 cách.
3. Hàng đơn vị: còn 2 cách. Nhân lại: 3 . 3 . 2 = 18 số.

> Lỗi thường gặp: cho hàng trăm cả chữ số 0. Số 012 chỉ có hai chữ số.

:::check
Q: Mã PIN 3 chữ số (0 đến 9, được lặp), chữ số đầu phải chẵn. Có bao nhiêu mã?
A: Chữ số đầu 5 cách (0, 2, 4, 6, 8), hai chữ số sau mỗi chữ 10 cách: 5 . 10 . 10 = 500.
:::

## Hoán vị và chỉnh hợp

:::hook
Trang chủ gợi ý đặt 3 trong 10 bộ phim vào ô số 1, 2, 3. Đổi chỗ hai phim là ra một trang chủ khác: thứ tự có nghĩa.
:::

:::figure flow
caption: Phim đã đặt không dùng lại: A(10, 3) = 10 . 9 . 8.
box "ô 1: 10 cách" xanh
link "x"
box "ô 2: 9 cách" xanh
link "x"
box "ô 3: 8 cách" xanh
link "="
box "720" luc
:::

:::core
Khi đổi vai là ra cách mới, thứ tự có nghĩa: mỗi chỗ sau ít đi một lựa chọn. Xếp hết n vật là n!, lấp k chỗ là A(n, k).
:::

$$ A_n^k = n (n-1) \cdots (n-k+1) = \frac{n!}{(n-k)!} $$

Ví dụ: xếp 4 người thành hàng, An và Bình đứng cạnh nhau.

1. Buộc An, Bình thành khối; khối và 2 người kia: 3! = 6 cách.
2. Trong khối đổi chỗ được: 6 . 2 = 12 cách.
3. Không cạnh nhau thì lấy phần còn lại: 4! - 12 = 12.

> Lỗi thường gặp: trao vàng, bạc, đồng mà chia cho 3!. Huy chương khác nhau: đó là chỉnh hợp.

:::check
Q: Chọn 1 chưởng môn, 1 trưởng lão trong 6 đệ tử: mấy cách? Sao không là 15?
A: A(6, 2) = 6 . 5 = 30. 15 là số nhóm hai người, nhưng An làm chưởng môn khác Bình làm chưởng môn.
:::

## Tổ hợp

:::hook
Chọn 3 trong 10 đặc trưng để huấn luyện mô hình: chỉ cần biết bộ nào được chọn, chọn trước hay sau không quan trọng.
:::

:::figure grid
caption: 6 thứ tự chỉ là 3 nhóm: mỗi nhóm bị đếm 2! lần.
table
head "nhóm" "thứ tự"
row "{a, b}" "ab, ba"
row "{a, c}" "ac, ca"
row "{b, c}" "bc, cb"
:::

:::core
Tổ hợp đếm nhóm, không kể thứ tự: số cách xếp có thứ tự chia cho k!, vì mỗi nhóm k vật bị đếm k! lần.
:::

$$ C_n^k = \frac{A_n^k}{k!} = \frac{n!}{k!\,(n-k)!} $$

Lấy 2 trong 5: thành nhóm C(5, 2) = 10, có thứ tự A(5, 2) = 20, có thứ tự và được lặp 5^2 = 25. Chọn k để lấy cũng là chọn n - k để bỏ: C(n, k) = C(n, n - k).

Ví dụ: 4 nam, 3 nữ. Chọn 3 người, có ít nhất 1 nữ.

1. Mọi nhóm 3 trong 7 người: C(7, 3) = 35.
2. Nhóm không có nữ (3 trong 4 nam): C(4, 3) = 4.
3. Có ít nhất 1 nữ: 35 - 4 = 31.

> Lỗi thường gặp: chọn 2 nam VÀ 1 nữ mà cộng C(4, 2) + C(3, 1). Làm cả hai việc thì nhân: 6 . 3 = 18.

:::check
Q: 8 điểm, không 3 điểm nào thẳng hàng: vẽ được bao nhiêu tam giác?
A: Tam giác ABC cũng là tam giác BCA: không kể thứ tự. C(8, 3) = 56.
:::
