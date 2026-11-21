---
id: dstt_lib_t6
title_vi: Định thức, hạng và ma trận nghịch đảo
subject: dai_so_tuyen_tinh
floor: 6
format: 2
summary_vi: Định thức là hệ số phóng diện tích của một ma trận vuông: khác 0 thì ma trận làm ngược lại được (có nghịch đảo, hệ có đúng một nghiệm), bằng 0 thì mặt phẳng bị ép bẹp; hạng đếm số hướng còn sống.
skills: [dstt_t6_dinh_thuc_cap_2_3, dstt_t6_khai_trien, dstt_t6_tinh_chat_dinh_thuc, dstt_t6_hang, dstt_t6_nghich_dao, dstt_t6_giai_he_nghich_dao]
---
## Định thức cấp 2 và cấp 3

:::hook
Một lớp mạng nơ-ron biến hình vuông nhỏ quanh mỗi điểm dữ liệu thành hình bình hành. Định thức cho biết diện tích bị nhân lên bao nhiêu lần, và có bị ép bẹp hay không.
:::

:::figure plane
caption: Hai cột (3, 1) và (1, 2) của [3, 1; 1, 2] dựng một hình bình hành diện tích 3 . 2 - 1 . 1 = 5.
size: 130 110
x: -0.5 4.5 1
y: -0.5 3.5 1
poly 0 0 3 1 4 3 1 2 vang "5"
vector 0 0 3 1 do "cột 1" pos=e
vector 0 0 1 2 xanh "cột 2" pos=w
:::

:::figure grid
caption: Cấp 3 (Sarrus): chép hai cột đầu sang phải. Mỗi đường chéo xuống (xanh) là một tích mang dấu +, mỗi đường chéo lên (đỏ) mang dấu -.
style: matrix
table "A, chép thêm 2 cột"
row 1 2 0 1 2
row 0 3 1 0 3
row 2 1 1 2 1
mark cell 1 2 xanh
mark cell 2 3 xanh
mark cell 3 4 xanh
mark cell 3 3 do
mark cell 2 4 do
mark cell 1 5 do
:::

:::core
Định thức là hệ số phóng diện tích (cấp 3: thể tích) của ma trận vuông; bằng 0 nghĩa là các cột cùng phương, mặt phẳng bị ép bẹp.
:::

Chỉ ma trận vuông mới có định thức. Có ẩn x trong ma trận thì định thức là một biểu thức của x: đặt nó bằng số đề cho rồi giải.

Ví dụ: tính det A, với A ở hình Sarrus.

1. Ba tích xuống: 1 . 3 . 1 = 3, 2 . 1 . 2 = 4, 0 . 0 . 1 = 0. Cộng được 7.
2. Ba tích lên: 2 . 3 . 0 = 0, 1 . 1 . 1 = 1, 1 . 0 . 2 = 0. Cộng được 1.
3. det A = 7 - 1 = 6.

$$ \text{det} \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc $$

> Lỗi thường gặp: cộng cả sáu tích. Ba tích theo đường chéo lên phải trừ đi. Sarrus cũng chỉ dùng cho cấp 3.

:::check
Q: [2, 6; 1, 3] có định thức bao nhiêu? Hình bình hành của hai cột trông ra sao?
A: 2 . 3 - 6 . 1 = 0. Cột (6, 3) gấp 3 lần cột (2, 1): hai mũi tên cùng phương, hình bị ép thành một đoạn thẳng, diện tích 0.
:::

## Khai triển theo hàng hoặc cột

:::hook
Ma trận cấp 4 đã có 24 tích, cấp 10 có hơn ba triệu. Khai triển đổi một định thức lớn thành vài định thức nhỏ, và mỗi số 0 xóa hẳn một nhánh.
:::

:::figure grid
caption: Dấu theo vị trí xếp như bàn cờ, góc trên trái là +. Xóa hàng 3, cột 2 của A (đỏ) còn lại định thức con M_32.
table "dấu"
row + - +
row - + -
row + - +
mark cell 3 2 do
table "A"
row 1 0 2
row 3 0 1
row 2 5 4
mark row 3 do
mark col 2 do
:::

:::core
Chọn một hàng hoặc cột; mỗi phần tử nhân với định thức nhỏ còn lại khi xóa hàng và cột của nó, kèm dấu bàn cờ, rồi cộng hết.
:::

Phần bù đại số C_ij là định thức con M_ij gắn dấu của ô (i, j). Chọn hàng hoặc cột nhiều số 0 nhất: số 0 nhân gì cũng bằng 0.

Ví dụ: tính det A ở hình.

1. Cột 2 là (0, 0, 5): chỉ còn số hạng của a_32 = 5.
2. Xóa hàng 3, cột 2: M_32 = det [1, 2; 3, 1] = 1 - 6 = -5.
3. Ô (3, 2) mang dấu -: C_32 = 5.
4. det A = 5 . 5 = 25.

$$ C_{ij} = (-1)^{i + j} M_{ij} $$

> Lỗi thường gặp: quên dấu, coi C_ij = M_ij. Các ô (1, 2), (2, 1), (2, 3), (3, 2) mang dấu trừ.

:::check
Q: Hàng 2 của ma trận cấp 4 là (0, 0, 0, 3). det A bằng gì nhân với M_24? Dấu nào?
A: Chỉ còn a_24 = 3, dấu (-1)^(2 + 4) = +1, nên det A = 3 M_24.
:::

## Tính chất của định thức

:::hook
Máy tính không bao giờ khai triển ma trận lớn: nó khử Gauss về tam giác rồi nhân đường chéo. Muốn vậy phải biết mỗi phép biến đổi hàng làm định thức đổi ra sao.
:::

:::figure plane
caption: Cộng bội của hàng này vào hàng kia là trượt hình: cùng đáy, cùng chiều cao, diện tích vẫn 1.
size: 170 70
axes: off
x: -0.3 4.3
y: -0.5 1.3
poly 0 0 1 0 1 1 0 1 xanh "1"
text 1.5 0.5 "->"
poly 2 0 3 0 4 1 3 1 vang "1"
segment 2 -0.25 3 -0.25 muc "đáy 1" pos=s
:::

:::figure grid
caption: Luật của định thức, A vuông cấp n.
table
head "làm gì" "det thành"
row "đổi chỗ 2 hàng" "-det A"
row "nhân 1 hàng với k" "k det A"
row "cộng bội hàng" "không đổi"
row "kA" "k^n det A"
row "AB" "det A . det B"
row "A^T" "det A"
mark row 4 do
:::

:::core
Định thức nhân tính, det(AB) = det A . det B, nhưng không cộng tính; ma trận tam giác có định thức bằng tích đường chéo.
:::

Ví dụ: tính det A, A có hàng (0, 2, 1), (1, 1, 0), (2, 4, 5).

1. Trụ bằng 0: R1 <-> R2, định thức đổi dấu.
2. R3 <- R3 - 2R1 cho (0, 2, 5); R3 <- R3 - R2 cho (0, 0, 4). Không đổi định thức.
3. Tam giác: 1 . 2 . 4 = 8. Nhớ lần đổi chỗ: det A = -8.

$$ \text{det}(kA) = k^{n} \, \text{det} A $$

> Lỗi thường gặp: viết det(kA) = k det A. kA nhân cả n hàng với k, nên định thức nhân với k đúng n lần.

:::check
Q: A cấp 3, det A = 2. Tính det(-A) và det(A^2). Có phải det(A + A) = det A + det A không?
A: det(-A) = (-1)^3 . 2 = -2; det(A^2) = 2 . 2 = 4. Không: det(2A) = 8 . 2 = 16, khác 4.
:::

## Hạng của ma trận

:::hook
Bảng dữ liệu có cột "giá (nghìn đồng)" và cột "giá (triệu đồng)": hai cột nhưng chỉ một thông tin. Hạng đếm số thông tin thật sự độc lập.
:::

:::figure grid
caption: Hàng 2 gấp đôi hàng 1 nên bị khử thành 0 (đỏ). Còn 2 hàng sống: rank A = 2.
style: matrix
table "A"
row 1 -1 2
row 2 -2 4
row 0 1 1
op "->"
table "bậc thang"
row 1 -1 2
row 0 1 1
row 0 0 0
mark row 3 do
:::

:::core
Hạng là số hàng khác 0 còn lại sau khi khử Gauss: số hướng thật sự độc lập mà ma trận chứa.
:::

Hạng không vượt số hàng, cũng không vượt số cột. Ma trận vuông cấp n có rank A = n đúng khi det A khác 0. Hệ Ax = 0 có số ẩn tự do bằng số ẩn trừ rank A.

Ví dụ: tìm m để A có hàng (1, 1, 2), (2, 3, m), (1, 2, 4) có hạng 2.

1. R2 - 2R1 = (0, 1, m - 4); R3 - R1 = (0, 1, 2).
2. Trừ hai hàng đó: (0, 0, 6 - m).
3. Hạng 2 khi hàng cuối toàn 0: m = 6.

> Lỗi thường gặp: đếm hàng khác 0 của chính A khi chưa khử. Hàng khác 0 vẫn có thể là tổ hợp của các hàng khác.

:::check
Q: A vuông cấp 3 có det A = 0. rank A có thể bằng 3 không? Ma trận cỡ 4 x 2 có hạng lớn nhất là bao nhiêu?
A: Không: rank 3 cần det khác 0. Cỡ 4 x 2 chỉ có 2 cột, nên hạng nhiều nhất là 2.
:::

## Ma trận nghịch đảo

:::hook
Mã hóa tin nhắn bằng ma trận A thì người nhận cần A^(-1) để giải mã. Nếu det A = 0, hai tin khác nhau thành cùng một mã: không ai giải lại được.
:::

:::figure grid
caption: Biến đổi hàng trên cả (A | I) đến khi bên trái thành I; bên phải (vàng) là A^(-1).
style: matrix
table "(A | I)"
row 1 2 1 0
row 2 5 0 1
op "R2 - 2R1"
table
row 1 2 1 0
row 0 1 -2 1
op "R1 - 2R2"
table "(I | A^-1)"
row 1 0 5 -2
row 0 1 -2 1
mark col 3 vang
mark col 4 vang
:::

:::core
A^(-1) là phép làm ngược của A: AA^(-1) = A^(-1)A = I; nó tồn tại đúng khi det A khác 0, tức A không ép bẹp gì cả.
:::

Cấp 2 có lối tắt: đổi chỗ hai số trên đường chéo chính, đổi dấu hai số kia, chia cho det A. Ngoài ra det(A^(-1)) = 1/det A và (A^T)^(-1) = (A^(-1))^T.

Ví dụ: kiểm tra A^(-1) ở hình bằng lối tắt, A = [1, 2; 2, 5].

1. det A = 5 - 4 = 1.
2. Đổi chỗ 1 và 5, đổi dấu hai số 2: [5, -2; -2, 1], chia cho 1.
3. Thử: hàng (1, 2) nhân hai cột cho 5 - 4 = 1 và -2 + 2 = 0. Đúng.

$$ \begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} $$

$$ (AB)^{-1} = B^{-1} A^{-1} $$

> Lỗi thường gặp: viết (AB)^(-1) = A^(-1) B^(-1). Muốn gỡ áo khoác sau khi đã mặc áo sơ mi thì phải gỡ áo khoác trước: làm ngược thì đảo thứ tự.

:::check
Q: A = [3, 1; 5, 2]. Tìm A^(-1) và det(A^(-1)).
A: det A = 6 - 5 = 1, nên A^(-1) = [2, -1; -5, 3] và det(A^(-1)) = 1/1 = 1.
:::

## Giải hệ bằng nghịch đảo và quy tắc Cramer

:::hook
Một bộ lọc ảnh phải giải cùng một hệ Ax = b cho hàng nghìn vế phải b khác nhau. Tính A^(-1) một lần, rồi mỗi b chỉ còn là một phép nhân.
:::

:::figure grid
caption: Hệ 2x + y = 5, x + 3y = 5. A_1 thay cột x bằng b, A_2 thay cột y bằng b (vàng).
style: matrix
table "A"
row 2 1
row 1 3
table "b"
row 5
row 5
mark col 1 vang
table "A_1"
row 5 1
row 5 3
mark col 1 vang
table "A_2"
row 2 5
row 1 5
mark col 2 vang
:::

:::core
Khi det A khác 0, hệ Ax = b có đúng một nghiệm x = A^(-1) b; Cramer tìm từng ẩn bằng cách thay cột của ẩn đó bằng b.
:::

A^(-1) phải đứng bên trái b: b A^(-1) không nhân được. Khi det A = 0 thì cả hai cách đều không dùng được: hệ vô nghiệm hoặc vô số nghiệm, phải khử Gauss.

Ví dụ: giải hệ ở hình bằng Cramer.

1. det A = 6 - 1 = 5.
2. det A_1 = 15 - 5 = 10, nên x = 10/5 = 2.
3. det A_2 = 10 - 5 = 5, nên y = 5/5 = 1.
4. Thử: 4 + 1 = 5 và 2 + 3 = 5.

$$ x_{k} = \frac{\text{det} A_{k}}{\text{det} A} $$

> Lỗi thường gặp: thay một HÀNG của A bằng b. Cramer thay CỘT của ẩn cần tìm, vì mỗi cột ứng với một ẩn.

:::check
Q: Hệ x + 2y = 3, 2x + 4y = 6 có det A bằng bao nhiêu? Dùng Cramer được không, và hệ có mấy nghiệm?
A: det A = 4 - 4 = 0: không dùng Cramer được. Phương trình 2 gấp đôi phương trình 1, nên hệ có vô số nghiệm.
:::
