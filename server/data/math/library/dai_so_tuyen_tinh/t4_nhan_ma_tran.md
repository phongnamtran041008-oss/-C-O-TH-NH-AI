---
id: dstt_lib_t4
title_vi: Nhân ma trận
subject: dai_so_tuyen_tinh
floor: 4
format: 2
summary_vi: Nhân ma trận là hàng nhân cột: một hàng gặp một cột ra một số, hai số giữa của cỡ phải khớp, đổi thứ tự là đổi việc làm, và lũy thừa là lặp lại cùng một bước.
skills: [dstt_t4_tich_vo_huong, dstt_t4_dieu_kien_kich_thuoc, dstt_t4_nhan_ma_tran, dstt_t4_khong_giao_hoan, dstt_t4_tinh_chat_nhan, dstt_t4_luy_thua]
---
## Tích vô hướng: một hàng nhân một cột

:::hook
Máy gợi ý phim chấm điểm "hợp gu" bằng tích vô hướng: nhân sở thích của bạn với chất của phim theo từng mục, rồi cộng lại.
:::

:::figure grid
caption: Nhân từng cột (cùng một mục), rồi cộng hàng tích: 8 - 5 - 6 = -3. Âm: phim này không hợp gu.
table
head "hành động" "lãng mạn" "hài"
side "bạn" "phim" "tích"
row 2 -1 3
row 4 5 -2
row 8 -5 -6
mark row 3 vang
:::

:::core
Tích vô hướng ghép từng cặp tọa độ cùng vị trí, nhân lại rồi cộng hết: hai vectơ vào, một con số ra.
:::

Hai vectơ phải cùng số chiều, thiếu một tọa độ là không có bạn để ghép. Tích bằng 0 nghĩa là hai vectơ vuông góc, "không liên quan" gì đến nhau.

Ví dụ: tìm m để u = (m, 1, 2) và v = (3, -4, 1) có tích vô hướng 0.

1. Ghép từng cặp: 3m + 1 . (-4) + 2 . 1 = 3m - 2.
2. Cho bằng 0: 3m = 2, m = 2/3.
3. Thử: 2 - 4 + 2 = 0.

$$ u \cdot v = u_{1}v_{1} + u_{2}v_{2} + \ldots + u_{n}v_{n} $$

> Lỗi thường gặp: sai dấu khi nhân số âm, như viết (-1) . 5 = 5. Viết dấu của từng tích ra trước rồi mới cộng.

:::check
Q: Tích vô hướng của u = (3, -2) với chính nó là bao nhiêu? u . u có khi nào âm không?
A: 9 + 4 = 13. Không bao giờ âm: u . u là tổng các bình phương.
:::

## Điều kiện kích thước để nhân

:::hook
Một lớp mạng nơ-ron nhận 784 số và nhả ra 10 số, nên ma trận trọng số của nó phải cỡ 10 x 784. Lệch một chút là chương trình báo lỗi "shape mismatch" ngay.
:::

:::figure grid
caption: Một hàng của A có 3 ô, một cột của B có 3 ô: khớp nhau mới nhân được. AB lấy 2 hàng của A, 4 cột của B.
style: matrix
table "A: 2 x 3"
row * * *
row * * *
mark row 1 do
op "x"
table "B: 3 x 4"
row * * * *
row * * * *
row * * * *
mark col 1 xanh
op "="
table "AB: 2 x 4"
row * * * *
row * * * *
mark cell 1 1 vang
:::

:::core
Đặt hai cỡ cạnh nhau (m x n)(n x p): hai số ở giữa phải bằng nhau, hai số ở ngoài là cỡ của tích.
:::

Cùng cỡ chưa chắc nhân được: hai ma trận 3 x 2 thì 2 khác 3. Ngược lại, A^T A luôn nhân được: (n x m)(m x n) cho n x n.

Ví dụ: A cỡ 3 x 2, B cỡ 2 x 5, C cỡ 5 x 1. ABC cỡ bao nhiêu?

1. AB: (3 x 2)(2 x 5), giữa khớp, ra 3 x 5.
2. (AB)C: (3 x 5)(5 x 1), giữa khớp, ra 3 x 1.

$$ (m \times n) \cdot (n \times p) = m \times p $$

> Lỗi thường gặp: so số hàng với số hàng. Chỉ có một điều kiện: số cột của ma trận trước bằng số hàng của ma trận sau.

:::check
Q: A cỡ 4 x 3. B phải cỡ bao nhiêu để cả AB lẫn BA đều nhân được?
A: AB cần B có 3 hàng, BA cần B có 4 cột: B cỡ 3 x 4.
:::

## Nhân hai ma trận

:::hook
Mỗi nơ-ron của một lớp mạng là một hàng trọng số nhân với cột dữ liệu vào. GPU làm hàng tỷ phép hàng-nhân-cột như thế mỗi giây.
:::

:::figure grid
caption: Hàng 2 của A (đỏ) nhân cột 1 của B (xanh): -2 + 0 + 4 = 2, ra ô (2, 1) của AB.
style: matrix
table "A"
row 1 2 0
row -1 3 1
mark row 2 do
op "x"
table "B"
row 2 1
row 0 -1
row 4 2
mark col 1 xanh
op "="
table "AB"
row 2 -1
row 2 -2
mark cell 2 1 vang
:::

:::core
Ô (i, j) của AB là hàng i của A nhân vô hướng với cột j của B: hàng lấy bên trái, cột lấy bên phải.
:::

Nhân ma trận với một vectơ cột x: mỗi tọa độ của Ax là một hàng của A nhân x. Hàng i của A toàn số 0 thì hàng i của AB cũng toàn số 0.

Ví dụ: tính các ô còn lại của AB ở hình.

1. Ô (1, 1): (1, 2, 0) . (2, 0, 4) = 2.
2. Ô (1, 2): (1, 2, 0) . (1, -1, 2) = 1 - 2 = -1.
3. Ô (2, 2): (-1, 3, 1) . (1, -1, 2) = -1 - 3 + 2 = -2.

$$ (AB)_{ij} = a_{i1}b_{1j} + a_{i2}b_{2j} + \ldots + a_{in}b_{nj} $$

> Lỗi thường gặp: nhân từng ô cùng vị trí như phép cộng. Nhân ma trận luôn là hàng của ma trận trước nhân cột của ma trận sau.

:::check
Q: A vuông cấp 3 có cột 2 toàn số 0. Với B vuông cấp 3, cột nào của BA chắc chắn toàn số 0?
A: Cột 2: ô (i, 2) của BA là hàng i của B nhân cột 2 của A, mà cột đó toàn 0.
:::

## Không giao hoán: AB khác BA

:::hook
Lật một tấm ảnh rồi xoay khác với xoay rồi mới lật. Mỗi phép biến hình là một ma trận, nên thứ tự nhân ma trận là thứ tự làm việc.
:::

:::figure plane
caption: v = (2, 1). Lật qua trục ngang rồi quay 90 độ được (1, 2); quay trước rồi lật được (-1, -2).
size: 150 120
x: -2.5 2.5 2
y: -2.5 2.5 2
vector 0 0 2 1 muc "v" pos=e
vector 0 0 1 2 xanh "RFv" pos=e
vector 0 0 -1 -2 do "FRv" pos=w
:::

:::matrix
R = 0 -1 ; 1 0
F = 1 0 ; 0 -1
:::

:::core
ABv nghĩa là làm B trước rồi mới A; đổi thứ tự là đổi việc làm, nên nói chung AB != BA.
:::

Có cặp giao hoán: kI với mọi ma trận, A với chính nó và các lũy thừa của nó. Lạ hơn: AB có thể bằng O khi A, B đều khác O.

Ví dụ: tính RF và FR (R quay 90 độ, F lật qua trục ngang).

1. RF: hàng (0, -1) nhân hai cột (1, 0) và (0, -1) ra (0, 1); hàng (1, 0) ra (1, 0).
2. FR: hàng (1, 0) ra (0, -1); hàng (0, -1) ra (-1, 0).
3. RF = [0, 1; 1, 0] khác FR = [0, -1; -1, 0].

$$ (A + B)^{2} = A^{2} + AB + BA + B^{2} $$

> Lỗi thường gặp: gộp AB + BA thành 2AB. Chỉ được gộp khi biết chắc AB = BA.

:::check
Q: A = [1, 2; 0, 1], B = [1, 0; 3, 1]. Tính ô (1, 1) của AB và của BA.
A: AB: (1, 2) . (1, 3) = 7. BA: (1, 0) . (1, 0) = 1. Khác nhau, nên AB != BA.
:::

## Tính chất của phép nhân ma trận

:::hook
Mạng nơ-ron ba lớp tính W3(W2(W1 x)). Nhờ tính kết hợp, có thể gộp trước W3 W2 W1 thành một ma trận, hoặc chọn thứ tự nhân rẻ nhất.
:::

:::figure grid
caption: A cỡ 2 x 3, B cỡ 3 x 4. Chỉ thứ tự đảo B^T A^T mới khớp cỡ với (AB)^T.
table
head "tích" "cỡ" "kết quả"
row "(AB)^T" "lật của 2 x 4" "4 x 2"
row "B^T A^T" "(4 x 3)(3 x 2)" "4 x 2"
row "A^T B^T" "(3 x 2)(4 x 3)" "không nhân được"
mark row 2 luc
mark row 3 do
:::

:::core
Nhân ma trận giữ mọi luật quen thuộc (kết hợp, phân phối, đưa số ra ngoài) trừ giao hoán; vì thế chuyển vị một tích phải đảo thứ tự.
:::

Phân phối phải giữ bên: A(B + C) = AB + AC, còn (B + C)A = BA + CA. Số thì đưa ra đâu cũng được: (kA)B = k(AB) = A(kB).

Ví dụ: A = [1, 3] cỡ 1 x 2, B = [2; -1] cỡ 2 x 1, C = [4, 1] cỡ 1 x 2. Tính ABC.

1. Tính AB trước: 2 - 3 = -1, chỉ là một số.
2. (AB)C = -1 . [4, 1] = [-4, -1].
3. A(BC) cũng ra [-4, -1], nhưng phải lập BC cỡ 2 x 2 trước.

$$ (AB)^{T} = B^{T} A^{T} $$

> Lỗi thường gặp: viết (A + B)(A - B) = A^2 - B^2. Nhân bung giữ thứ tự ra A^2 - AB + BA - B^2.

:::check
Q: A, B vuông cùng cấp. (A^T B)^T bằng gì?
A: Đảo thứ tự và lật từng cái: B^T (A^T)^T = B^T A.
:::

## Ma trận đơn vị và lũy thừa ma trận

:::hook
Thời tiết đổi trạng thái mỗi ngày theo một ma trận P. Dự báo 7 ngày sau là P^7: lũy thừa ma trận là lặp lại cùng một bước.
:::

:::figure grid
caption: Mỗi lần nhân thêm A, ô góc trên phải cộng thêm 3: A^n có ô đó là 3n, không phải 3^n.
style: matrix
table "A"
row 1 3
row 0 1
mark cell 1 2 vang
op "->"
table "A^2"
row 1 6
row 0 1
mark cell 1 2 vang
op "->"
table "A^3"
row 1 9
row 0 1
mark cell 1 2 vang
:::

:::core
A^n là nhân A với chính nó n lần, mỗi lần hàng nhân cột, không phải lũy thừa từng ô; I đóng vai số 1: AI = IA = A.
:::

Chỉ ma trận vuông mới có lũy thừa, và A^0 = I. Ma trận chéo thì lũy thừa từng số trên đường chéo. Nếu A^2 = I thì A^n là I khi n chẵn, là A khi n lẻ. Có A khác O mà A^2 = O.

Ví dụ: A = [2, 1; 0, 1]. Tính A^2.

1. Hàng 1 nhân hai cột: (2, 1) . (2, 0) = 4 và (2, 1) . (1, 1) = 3.
2. Hàng 2: (0, 1) . (2, 0) = 0 và (0, 1) . (1, 1) = 1.
3. A^2 = [4, 3; 0, 1]; bình phương từng ô sẽ ra [4, 1; 0, 1], sai.

$$ AI = IA = A $$

> Lỗi thường gặp: tính A^2 bằng cách bình phương từng ô. Hai cách chỉ trùng nhau với ma trận chéo.

:::check
Q: A = [0, -1; 1, 0] là phép quay 90 độ. A^4 bằng gì?
A: Quay 4 lần 90 độ là quay một vòng: A^4 = I. (Tính: A^2 = -I, nên A^4 = I.)
:::
