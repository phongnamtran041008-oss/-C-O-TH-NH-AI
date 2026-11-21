---
id: dstt_lib_t10
title_vi: Tài năng: cấu trúc đại số và dạng song tuyến tính
subject: dai_so_tuyen_tinh
floor: 10
format: 2
summary_vi: Tầng ẩn nhìn ra bộ xương phía sau ma trận: quan hệ tương đương cắt tập thành lớp, phép toán có trung hòa và phần tử ngược, nhóm đếm bước quay về, trường là nơi chia được, và dạng song tuyến tính x^T A y. Trọng tâm là kiểm từng điều kiện và biết tìm phản ví dụ.
skills: [dstt_t10_quan_he, dstt_t10_phep_toan_hai_ngoi, dstt_t10_nhom, dstt_t10_vanh_truong, dstt_t10_dang_song_tuyen_tinh]
---
## Quan hệ hai ngôi

:::hook
Bộ lọc thư gom các thư "cùng loại" thành từng nhóm. Muốn gom được gọn, rời nhau, thì "cùng loại" phải là một quan hệ tương đương.
:::

:::figure graph
caption: a ~ b khi a - b chia hết cho 3, trên {1, ..., 6}: ba lớp {1, 4}, {2, 5}, {3, 6}, rời nhau và phủ kín.
layout: circle
node 1 "1" do
node 4 "4" do
node 2 "2" xanh
node 5 "5" xanh
node 3 "3" luc
node 6 "6" luc
edge 1 4 do
edge 2 5 xanh
edge 3 6 luc
:::

:::figure grid
caption: Quan hệ trên {1, 2, 3} viết thành bảng 0/1. Phản xạ: đường chéo toàn 1. Đối xứng: bảng bằng chuyển vị của nó.
table "R"
head 1 2 3
side 1 2 3
row 1 0 1
row 0 1 0
row 1 0 1
mark diag
:::

:::core
Quan hệ tương đương (phản xạ, đối xứng, bắc cầu) là "giống nhau theo một tiêu chí": nó cắt tập thành các lớp rời nhau phủ kín.
:::

Phản xạ: a R a. Đối xứng: a R b thì b R a. Bắc cầu: a R b và b R c thì a R c. Thay đối xứng bằng phản đối xứng (a R b và b R a thì a = b) là quan hệ thứ tự, như <= hay "chia hết"; toàn phần nếu mọi cặp so sánh được.

Ví dụ: a ~ b khi a - b chia hết cho 4, trên {1, ..., 15}.

1. Cùng lớp nghĩa là cùng số dư khi chia cho 4: có 4 lớp.
2. Lớp của 2: 2, 6, 10, 14, có 4 phần tử.
3. Bắc cầu: a - b = 4k, b - c = 4m thì a - c = 4(k + m).

$$ a \sim b \iff n \mid (a - b) $$

> Lỗi thường gặp: "cộng" hai bất đẳng thức để có bắc cầu. |x - y| < 1 và |y - z| < 1 chỉ cho |x - z| < 2: x = 0, y = 0.6, z = 1.2 phá bắc cầu.

:::check
Q: Trên Z, a R b khi |a| = |b|. Đây có là quan hệ tương đương không? Lớp của 3 là gì?
A: Có: phản xạ, đối xứng, bắc cầu đều đúng vì chỉ so hai số |a|, |b|. Lớp của 3 là {3, -3}.
:::

## Phép toán hai ngôi

:::hook
Mật mã và hàm băm dựng trên những phép toán lạ. Trước khi tin một phép toán, phải biết nó có giao hoán, kết hợp, có trung hòa, có phần tử ngược hay không.
:::

:::figure grid
caption: a * b = max(a, b) trên {0, 1, 2}. Bảng đối xứng qua đường chéo: giao hoán. Hàng của 0 chép y tiêu đề (vàng): 0 là trung hòa. Số 0 chỉ ở ô (0, 0): chỉ 0 có phần tử ngược.
table "*"
head 0 1 2
side 0 1 2
row 0 1 2
row 1 1 2
row 2 2 2
mark row 1 vang
:::

:::core
Trung hòa e là phần tử "không làm gì": a * e = a với mọi a; phần tử ngược của a là thứ đưa a về đúng e, không phải về 0 hay 1.
:::

Giao hoán: a * b = b * a. Kết hợp: (a * b) * c = a * (b * c). Chứng minh thì khai triển hai vế với mọi a, b, c; bác bỏ thì một phản ví dụ là đủ. Trung hòa, nếu có, là duy nhất và không phụ thuộc a.

Ví dụ: a * b = a + b - 4 trên R. Tìm trung hòa và phần tử ngược của 1.

1. a * e = a + e - 4 = a với mọi a, nên e = 4.
2. Ngược của 1: 1 * b = 1 + b - 4 phải bằng e = 4.
3. b = 7. Thử: 1 + 7 - 4 = 4.

$$ (a * b) * c = a * (b * c), \qquad a * e = e * a = a, \qquad a * a' = a' * a = e $$

> Lỗi thường gặp: tìm phần tử ngược trước khi biết e, rồi cho a * b bằng 0 hay 1 theo thói quen. Phải tìm e trước.

:::check
Q: a * b = ab + 1 trên R có kết hợp không? Thử a = b = 0, c = 1.
A: (0 * 0) * 1 = 1 * 1 = 2, còn 0 * (0 * 1) = 0 * 1 = 1. Khác nhau: không kết hợp.
:::

## Nhóm và nhóm con

:::hook
Xoay khối Rubik, mã hóa RSA, mã sửa lỗi đều là nhóm. Cấp của một phần tử là số bước để lặp lại nó thì quay về chỗ cũ.
:::

:::figure graph
caption: Trong Z_10, cứ cộng 4: 0, 4, 8, 2, 6 rồi về 0. Năm bước, nên 4 có cấp 5 = 10/gcd(4, 10).
layout: circle
directed: yes
node 0 "0" vang
node 1 "1"
node 2 "2"
node 3 "3"
node 4 "4"
node 5 "5"
node 6 "6"
node 7 "7"
node 8 "8"
node 9 "9"
edge 0 4 do
edge 4 8 do
edge 8 2 do
edge 2 6 do
edge 6 0 do
:::

:::core
Cấp của a là số bước ít nhất để lặp a quay về trung hòa; theo Lagrange, nó và mọi nhóm con đều có số phần tử chia hết cấp của nhóm.
:::

Nhóm: phép toán đóng, kết hợp, có trung hòa, ai cũng có ngược. Nhóm con: tập con khác rỗng, đóng với phép toán và lấy ngược. Trong Z_n cộng, a sinh cả nhóm khi gcd(a, n) = 1: có phi(n) phần tử sinh. Các số khả nghịch của Z_n lập nhóm nhân phi(n) phần tử.

Ví dụ: cấp của 2 trong nhóm nhân các số khác 0 của Z_7.

1. 2^1 = 2, 2^2 = 4, 2^3 = 8 = 1 (modulo 7).
2. Cấp là 3, chia hết 6 phần tử của nhóm.
3. 2 không sinh cả nhóm, vì 3 nhỏ hơn 6.

$$ \mathrm{ord}(a) = \frac{n}{\mathrm{gcd}(a, n)} \quad (a \in \mathbb{Z}_n), \qquad \mathrm{ord}(a) \mid |G| $$

> Lỗi thường gặp: lấy 1/a làm phần tử ngược trong nhóm cộng. Phép toán là cộng thì ngược của a là -a. Hợp hai nhóm con cũng không phải nhóm con: 2 và 3 trong 2Z hợp 3Z, nhưng 5 thì không.

:::check
Q: Nhóm có 15 phần tử có thể có nhóm con 6 phần tử không? Z_15 có bao nhiêu phần tử sinh?
A: Không: 6 không chia hết 15. Phần tử sinh là a có gcd(a, 15) = 1: phi(15) = 8.
:::

## Vành và trường

:::hook
Mã QR và mã sửa lỗi trên đĩa tính toán trong một trường hữu hạn. Chọn Z_n với n hợp số thì phép chia hỏng và mã không giải lại được.
:::

:::figure grid
caption: Bảng nhân Z_6. Đỏ: hai số khác 0 nhân ra 0 (ước của 0). Xanh: tích bằng 1, chỉ 1 và 5 khả nghịch. Z_6 không là trường.
table
head x 0 1 2 3 4 5
row 0 0 0 0 0 0 0
row 1 0 1 2 3 4 5
row 2 0 2 4 0 2 4
row 3 0 3 0 3 0 3
row 4 0 4 2 0 4 2
row 5 0 5 4 3 2 1
mark cell 3 5 do
mark cell 4 4 do
mark cell 4 6 do
mark cell 5 5 do
mark cell 2 3 luc
mark cell 6 7 luc
:::

:::core
Trường là nơi chia được cho mọi số khác 0; Z_n là trường đúng khi n nguyên tố, còn n hợp số thì có ước của 0 phá phép chia.
:::

Vành: cộng là nhóm giao hoán, nhân kết hợp, nhân phân phối với cộng. Trong Z_n, a khả nghịch khi gcd(a, n) = 1; mỗi số khác 0 hoặc khả nghịch, hoặc là ước của 0. Z không có ước của 0 nhưng vẫn không là trường: 2 không có nghịch đảo.

Ví dụ: xét Z_9.

1. Khả nghịch: gcd(a, 9) = 1, tức 1, 2, 4, 5, 7, 8 (phi(9) = 6).
2. Còn lại 3 và 6 là ước của 0: 3 . 3 = 9 = 0.
3. Nghịch đảo của 2 là 5, vì 2 . 5 = 10 = 1. Z_9 không là trường.

$$ \exists\, b : \; ab \equiv 1 \ (\mathrm{mod}\ n) \iff \mathrm{gcd}(a, n) = 1 $$

> Lỗi thường gặp: thử vài số thấy khả nghịch rồi kết luận là trường. Phải xét mọi số khác 0; Z_8 có 3, 5, 7 khả nghịch nhưng 2 . 4 = 0.

:::check
Q: Trong Z_7, nghịch đảo của 2 là gì? Z_15 có bao nhiêu ước của 0?
A: 2 . 4 = 8 = 1, nên là 4. Z_15: 14 số khác 0, phi(15) = 8 khả nghịch, còn 6 ước của 0 (3, 5, 6, 9, 10, 12).
:::

## Dạng tuyến tính và song tuyến tính

:::hook
Điểm chú ý trong mô hình attention có dạng x^T A y. A không đối xứng nên "x chú ý tới y" có thể khác "y chú ý tới x".
:::

:::figure grid
caption: f = x1 y1 + 4 x1 y2 + 2 x2 y1 - 3 x2 y2: ô (i, j) của A là hệ số của x_i y_j. q(x) = f(x, x) gộp 4 + 2 = 6 rồi chia đôi vào B.
table "A của f"
head y1 y2
side x1 x2
row 1 4
row 2 -3
mark cell 1 2 vang
mark cell 2 1 vang
op "->"
table "B của q"
head x1 x2
side x1 x2
row 1 3
row 3 -3
mark cell 1 2 luc
mark cell 2 1 luc
:::

:::core
Dạng song tuyến tính là f(x, y) = x^T A y với a_ij là hệ số của x_i y_j; dạng toàn phương q(x) = f(x, x) chỉ thấy phần đối xứng của A.
:::

f đối xứng đúng khi A^T = A. Hai dạng khác nhau có thể cho cùng q. Với B đối xứng cấp 2: q xác định dương khi b11 > 0 và det B > 0. Mẹo thử: q(1, 1) bằng tổng các ô của B.

Ví dụ: A như hình, u = (1, 1), v = (2, -1).

1. Av = (2 - 4, 4 + 3) = (-2, 7); f(u, v) = -2 + 7 = 5.
2. Au = (5, -1); f(v, u) = 10 + 1 = 11.
3. Khác nhau, vì A không đối xứng.

$$ f(x, y) = x^{T} A y, \qquad B = \frac{A + A^{T}}{2} $$

> Lỗi thường gặp: đặt nguyên hệ số của x1 x2 vào cả hai ô của B. x^T B x có 2 b12 x1 x2, nên b12 là một nửa hệ số.

:::check
Q: q = 2 x1^2 - 4 x1 x2 + 3 x2^2. Viết B. q có xác định dương không?
A: B = [2, -2; -2, 3]. b11 = 2 > 0, det B = 6 - 4 = 2 > 0: xác định dương.
:::
