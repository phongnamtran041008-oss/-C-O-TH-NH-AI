---
id: dstt_lib_t3
title_vi: Vectơ trong R^n và ma trận
subject: dai_so_tuyen_tinh
floor: 3
format: 2
summary_vi: Vectơ là dãy số có thứ tự, ma trận là bảng số: đọc đúng ô, cộng từng ô, lật bảng, cộng đường chéo và nhận mặt vài dạng đặc biệt.
skills: [dstt_t3_vecto_rn, dstt_t3_kich_thuoc_phan_tu, dstt_t3_cong_nhan_vo_huong, dstt_t3_chuyen_vi, dstt_t3_vet, dstt_t3_ma_tran_dac_biet]
---
## Vectơ trong R^n

:::hook
Một tấm ảnh 28 x 28 điểm ảnh là 784 con số xếp theo thứ tự. Máy học coi nó là một vectơ trong R^784, rồi cộng và co giãn ảnh như cộng và co giãn mũi tên.
:::

:::figure bars
caption: (3, -1, 2, 0, 4) trong R^5: không vẽ được mũi tên 5 chiều, nhưng vẽ được 5 cột.
bar "u_1" 3
bar "u_2" -1 do
bar "u_3" 2
bar "u_4" 0
bar "u_5" 4
:::

:::core
Vectơ trong R^n là một dãy n số có thứ tự. Cộng hai vectơ và nhân vectơ với một số đều làm riêng từng tọa độ.
:::

$$ u = (u_{1}, u_{2}, \ldots, u_{n}) \in \mathbb{R}^{n} $$

> Lỗi thường gặp: cộng (1, 2) với (1, 2, 0) vì "thêm số 0 không đổi gì". Hai vectơ khác số chiều nằm ở hai không gian khác nhau, không cộng được.

:::check
Q: Vectơ (0, 5, -2, 1) nằm trong R^n với n bằng mấy? Tọa độ thứ ba của nó là gì?
A: n = 4, vì nó có 4 số. Tọa độ thứ ba là -2.
:::

### Cộng và co giãn vectơ

:::figure plane
caption: Với n = 2, vectơ là mũi tên. Nối đuôi v vào ngọn u: (2, 1) + (1, 2) = (3, 3).
size: 200 105
x: -0.5 3.5 1
y: -0.5 3.5 1
vector 0 0 2 1 do "u"
vector 2 1 3 3 xanh "v"
vector 0 0 3 3 luc "u + v" pos=nw
:::

Ví dụ: u = (1, -2, 0) và v = (3, 1, 4). Tính 2u - v.

1. Nhân mọi tọa độ của u với 2: 2u = (2, -4, 0).
2. Trừ từng cặp cùng vị trí: (2 - 3, -4 - 1, 0 - 4).
3. Kết quả: 2u - v = (-1, -5, -4).

:::check
Q: Cho u = (2, 0, -1) và v = (1, 3, 1). Tính 2u + v.
A: (4 + 1, 0 + 3, -2 + 1) = (5, 3, -1).
:::

## Kích thước ma trận và phần tử a_ij

:::hook
Bảng dữ liệu 100 khách hàng, mỗi người 5 thông tin, là ma trận 100 x 5: mỗi hàng một người, mỗi cột một loại thông tin.
:::

:::figure grid
caption: A cỡ 3 x 4. Ô a_23 nằm ở chỗ hàng 2 (xanh) cắt cột 3 (đỏ): a_23 = -4.
style: matrix
table
head "cột 1" "cột 2" "cột 3" "cột 4"
side "hàng 1" "hàng 2" "hàng 3"
row 5 -1 0 2
row 3 7 -4 1
row 6 0 9 -2
mark row 2 xanh
mark col 3 do
mark cell 2 3 vang
:::

:::core
Cỡ m x n nghĩa là m hàng và n cột. a_ij là ô ở hàng i, cột j: chỉ số đầu luôn là hàng.
:::

Ma trận vuông có số hàng bằng số cột; các ô a_11, a_22, ... nằm trên đường chéo chính. Ma trận cũng có thể cho bằng công thức: thay số hàng, số cột vào là ra từng ô.

Ví dụ: lập ma trận B cỡ 2 x 3 với b_ij = 2i - j.

1. Hàng 1 (i = 1): b_11 = 1, b_12 = 0, b_13 = -1.
2. Hàng 2 (i = 2): b_21 = 3, b_22 = 2, b_23 = 1. Xếp hai hàng lại:

:::matrix
B = 1 0 -1 ; 3 2 1
:::

> Lỗi thường gặp: đọc a_32 là hàng 2, cột 3. Đọc ngược là lấy nhầm ô, có khi ô đó không tồn tại.

:::check
Q: Trong ma trận A ở hình trên, a_31 bằng bao nhiêu?
A: 6: hàng 3 là (6, 0, 9, -2), lấy ô ở cột 1.
:::

## Cộng ma trận và nhân với một số

:::hook
Ảnh xám là một ma trận độ sáng. Làm ảnh sáng gấp đôi là nhân mọi ô với 2; chồng hai ảnh cùng cỡ là cộng hai ma trận, ô với ô.
:::

:::figure grid
caption: Ô cùng vị trí cộng với nhau: ô hàng 1, cột 2 cho 2 + 5 = 7.
style: matrix
table "A"
row 1 2
row 3 -4
mark cell 1 2 vang
op "+"
table "B"
row 0 5
row -1 2
mark cell 1 2 vang
op "="
table "A + B"
row 1 7
row 2 -2
mark cell 1 2 vang
:::

:::core
Cộng hai ma trận cùng cỡ và nhân ma trận với một số đều làm từng ô một, đúng như với vectơ.
:::

Điều kiện duy nhất của phép cộng là cùng cỡ: cỡ 2 x 3 và 3 x 2 cùng có 6 ô mà vẫn không cộng được. Vì mọi việc diễn ra trong từng ô, các luật của số vẫn đúng: A + B = B + A, k(A + B) = kA + kB, và ma trận không O đóng vai số 0.

Ví dụ: với A, B ở hình trên, tính 2A - B.

1. Nhân mọi ô của A với 2: 2A = [2, 4; 6, -8].
2. Trừ từng ô cùng vị trí: [2 - 0, 4 - 5; 6 + 1, -8 - 2].
3. Kết quả: 2A - B = [2, -1; 7, -10].

$$ (kA)_{ij} = k \cdot a_{ij} $$

> Lỗi thường gặp: tưởng kA chỉ nhân k vào một hàng hay một ô. Nhân với một số là nhân vào mọi ô.

:::check
Q: Tính 3 . [1, -2; 0, 4] + [2, 2; 1, -5].
A: [3 + 2, -6 + 2; 0 + 1, 12 - 5] = [5, -4; 1, 7].
:::

## Ma trận chuyển vị A^T

:::hook
Có thư viện xếp mỗi khách hàng một hàng, có thư viện lại muốn mỗi khách hàng một cột. Chuyển vị đổi giữa hai cách xếp đó mà không mất con số nào.
:::

:::figure grid
caption: Hàng 1 của A (đỏ) thành cột 1 của A^T, hàng 2 (xanh) thành cột 2. Cỡ 2 x 3 thành 3 x 2.
style: matrix
table "A"
row 1 2 3
row 4 5 6
mark row 1 do
mark row 2 xanh
op "->"
table "A^T"
row 1 4
row 2 5
row 3 6
mark col 1 do
mark col 2 xanh
:::

:::core
Chuyển vị là lật bảng qua đường chéo chính: hàng i thành cột i, nên cỡ m x n thành n x m.
:::

$$ (A^{T})_{ij} = a_{ji} $$

Lật hai lần thì mọi ô về chỗ cũ: (A^T)^T = A. Chuyển vị đi qua phép cộng và nhân với số: (A + B)^T = A^T + B^T và (kA)^T = kA^T.

Ví dụ: với A ở hình trên, tìm ô (A^T)_31.

1. Theo công thức, (A^T)_31 = a_13.
2. a_13 là ô hàng 1, cột 3 của A, bằng 3.
3. Trên hình: hàng 3 của A^T là (3, 6), ô đầu đúng là 3.

> Lỗi thường gặp: cộng A với A^T khi A không vuông. A cỡ 2 x 3 thì A^T cỡ 3 x 2, khác cỡ nên không cộng được.

:::check
Q: A có cỡ 4 x 7. A^T có cỡ bao nhiêu, và có tính được A + A^T không?
A: A^T cỡ 7 x 4. Không tính được A + A^T, vì 4 x 7 khác 7 x 4.
:::

## Vết của ma trận vuông

:::hook
Tổng phương sai của mọi thuộc tính đo độ phân tán của dữ liệu. Các phương sai ấy nằm trên đường chéo một ma trận, nên tổng đó là một vết.
:::

:::figure grid
caption: tr(A) = 2 + (-3) + 6 = 5. Chỉ các ô vàng được cộng, các ô khác không ảnh hưởng.
style: matrix
table "A"
row 2 7 -1
row 0 -3 4
row 5 1 6
mark diag vang
:::

:::core
Vết của ma trận vuông là tổng các ô a_ii trên đường chéo chính.
:::

Vết là tuyến tính: vết của một tổ hợp tính được từ vết của từng ma trận. Lật bảng không đụng tới đường chéo, nên tr(A^T) = tr(A).

$$ \text{tr}(kA + B) = k \cdot \text{tr}(A) + \text{tr}(B) $$

Ví dụ: A, B vuông cấp 4, tr(A) = 3, tr(B) = -1. Tính tr(2A - B + I).

1. Tách từng hạng tử: 2 tr(A) - tr(B) + tr(I).
2. I cấp 4 có bốn số 1 trên đường chéo, nên tr(I) = 4.
3. 2 . 3 - (-1) + 4 = 11.

> Lỗi thường gặp: cộng hết mọi ô của ma trận. Vết chỉ lấy các ô trên đường chéo chính.

:::check
Q: Ma trận [4, 9; -2, 1] có vết bằng bao nhiêu?
A: 4 + 1 = 5. Hai ô 9 và -2 nằm ngoài đường chéo nên không tính.
:::

## Các ma trận đặc biệt

:::hook
Bảng khoảng cách giữa các thành phố luôn đối xứng: từ A tới B xa bằng từ B tới A. Nhận ra những dạng như vậy giúp tính nhanh và bắt lỗi sớm.
:::

:::figure sets
caption: Tam giác trên giao đối xứng đúng bằng các ma trận chéo (vùng vàng), trong đó có I và O.
size: 220 100
set T "tam giác trên" xanh
set D "đối xứng" do
shade T&D vang
in T-D "U"
in D-T "S"
in T&D "chéo"
:::

:::matrix
U = 1 2 ; 0 3
S = 2 7 ; 7 0
I = 1 0 ; 0 1
:::

:::core
Mỗi dạng đặc biệt là một luật về đường chéo chính: số 0 nằm ở đâu, và hai ô đối nhau qua nó có bằng nhau không.
:::

- Tam giác trên: mọi ô dưới đường chéo chính bằng 0.
- Đối xứng: a_ij = a_ji với mọi i, j.
- Chéo: mọi ô ngoài đường chéo bằng 0. Đơn vị I: chéo, các ô trên đường chéo bằng 1. Không O: mọi ô bằng 0.

:::check
Q: Ma trận đơn vị cấp 3 có bao nhiêu ô bằng 0, và nó nằm ở vùng nào của hình?
A: 6 ô bằng 0. I là ma trận chéo, nên nằm ở vùng vàng: vừa tam giác trên, vừa đối xứng.
:::

### Nhận ra ma trận đối xứng

:::figure grid
caption: Hai ô đối nhau qua đường chéo cùng màu và bằng nhau, nên S^T = S.
style: matrix
table "S"
row 2 7 -1
row 7 0 4
row -1 4 5
mark cell 1 2 do
mark cell 2 1 do
mark cell 1 3 xanh
mark cell 3 1 xanh
mark cell 2 3 luc
mark cell 3 2 luc
:::

Ví dụ: S = [2, 7, -1; 7, 0, 4; -1, 4, 5] có đối xứng không?

1. So a_12 = 7 với a_21 = 7: bằng nhau.
2. So a_13 với a_31 (cùng là -1), a_23 với a_32 (cùng là 4): bằng nhau.
3. Mọi cặp đối nhau đều bằng nhau nên S đối xứng. S không chéo, vì có ô 7 khác 0.

$$ A^{T} = A $$

> Lỗi thường gặp: tưởng đối xứng nghĩa là các ô ngoài đường chéo bằng 0. Đối xứng chỉ đòi hai ô đối nhau bằng nhau, chúng được phép khác 0.

:::check
Q: Ma trận [1, 3; -3, 2] có đối xứng không?
A: Không: a_12 = 3 nhưng a_21 = -3.
:::
