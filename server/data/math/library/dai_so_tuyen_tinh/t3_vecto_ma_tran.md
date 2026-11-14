---
id: dstt_lib_t3
title_vi: Vectơ trong R^n và ma trận
subject: dai_so_tuyen_tinh
floor: 3
summary_vi: Bảng số và dãy số có thứ tự: cách gọi tên từng ô, cách cộng, cách lật bảng và vài dạng bảng đặc biệt cần nhớ mặt.
skills: [dstt_t3_vecto_rn, dstt_t3_kich_thuoc_phan_tu, dstt_t3_cong_nhan_vo_huong, dstt_t3_chuyen_vi, dstt_t3_vet, dstt_t3_ma_tran_dac_biet]
---
## Vectơ trong R^n

Một vectơ trong R^n chỉ là một dãy n số thực có thứ tự. Số n gọi là số chiều.

$$ u = (u_{1}, u_{2}, \ldots, u_{n}) \in \mathbb{R}^{n} $$

Có đúng hai phép toán, cả hai đều làm theo từng tọa độ một:

- Cộng hai vectơ cùng số chiều: cộng tọa độ thứ nhất với tọa độ thứ nhất, và cứ thế.
- Nhân một vectơ với một số: nhân mọi tọa độ với số đó.

Hai vectơ khác số chiều thì không cộng được, vì không biết ghép tọa độ nào với tọa độ nào.

Ví dụ với u = (1, -2, 0) và v = (3, 1, 4), tính 2u - v:

1. Nhân: 2u = (2, -4, 0).
2. Trừ theo từng tọa độ: (2 - 3, -4 - 1, 0 - 4).
3. Kết quả: (-1, -5, -4).

Mọi tính chất quen thuộc vẫn đúng, vì chúng chỉ là tính chất của số thực lặp lại trên từng tọa độ:

$$ a(u + v) = au + av $$

> Lỗi thường gặp: cộng (1, 2) với (1, 2, 0) rồi coi như bằng nhau vì "thêm số 0 không đổi gì". Chúng thuộc hai không gian khác nhau.

## Kích thước ma trận và phần tử a_ij

Ma trận là một bảng số hình chữ nhật. Cỡ của nó luôn viết theo thứ tự số hàng x số cột.

:::matrix
A = -7 1 3 ; -2 2 -8 ; -3 -4 5
:::

Ma trận trên có 3 hàng và 3 cột, nên cỡ 3 x 3. Phần tử ở hàng i, cột j viết là a_ij: chỉ số thứ nhất là hàng, chỉ số thứ hai là cột. Thứ tự này không bao giờ đổi.

$$ A = (a_{ij}), \quad 1 \le i \le m, \quad 1 \le j \le n $$

Ma trận vuông là ma trận có số hàng bằng số cột. Khi đó các phần tử a_11, a_22, ... nằm trên đường chéo chính, đi từ góc trên bên trái xuống góc dưới bên phải.

Đôi khi ma trận được cho bằng công thức thay vì bằng bảng, ví dụ a_ij = 2i - j. Khi đó cứ thay số hàng và số cột vào là ra từng ô.

> Lỗi thường gặp: đọc a_32 là hàng 2, cột 3. Hàng luôn đứng trước.

## Cộng ma trận và nhân với một số

Hai phép toán này cũng làm theo từng ô, giống hệt vectơ.

$$ (A + B)_{ij} = a_{ij} + b_{ij} $$

$$ (kA)_{ij} = k \cdot a_{ij} $$

Điều kiện duy nhất của phép cộng là hai ma trận phải cùng cỡ. Cùng số phần tử thì chưa đủ: cỡ 2 x 3 và cỡ 3 x 2 đều có 6 ô nhưng không cộng được.

Ví dụ cộng hai ma trận cỡ 2 x 2:

:::matrix
A = 1 2 ; 3 -4
B = 0 5 ; -1 2
:::

Cộng từng ô cùng vị trí được kết quả:

:::matrix
C = 1 7 ; 2 -2
:::

Vì mọi việc diễn ra theo từng ô, phép cộng ma trận giao hoán và kết hợp, còn phép nhân với một số thì phân phối. Ma trận không, tức là ma trận có mọi ô bằng 0, đóng vai trò số 0.

> Lỗi thường gặp: nghĩ rằng kA là nhân k với một hàng hay một ô nào đó. Nhân với một số là nhân vào mọi ô.

## Ma trận chuyển vị A^T

Chuyển vị là lật bảng qua đường chéo chính: hàng thành cột, cột thành hàng.

$$ (A^{T})_{ij} = a_{ji} $$

Nếu A cỡ m x n thì A^T cỡ n x m. Lật hai lần thì mọi ô về chỗ cũ.

$$ (A^{T})^{T} = A $$

Chuyển vị đi qua phép cộng một cách êm thấm, nên trong mọi biểu thức chỉ có cộng và nhân với số, cứ chuyển vị từng hạng tử:

$$ (A + B)^{T} = A^{T} + B^{T} $$

Ví dụ với ma trận cỡ 2 x 3:

:::matrix
A = 1 2 3 ; 4 5 6
:::

Chuyển vị của nó có 3 hàng và 2 cột:

:::matrix
B = 1 4 ; 2 5 ; 3 6
:::

> Lỗi thường gặp: cộng A với A^T khi A không vuông. Hai ma trận đó khác cỡ, chỉ ma trận vuông mới cộng được với chuyển vị của chính nó.

## Vết của ma trận vuông

Vết chỉ được định nghĩa cho ma trận vuông: nó là tổng các phần tử trên đường chéo chính.

$$ \text{tr}(A) = a_{11} + a_{22} + \ldots + a_{nn} $$

Vết biến cả một bảng số thành một số duy nhất, và nó làm việc đó một cách tuyến tính:

$$ \text{tr}(kA + B) = k \cdot \text{tr}(A) + \text{tr}(B) $$

Nhờ vậy, muốn tính vết của một tổ hợp thì không cần lập ma trận tổ hợp đó: chỉ cần vết của từng ma trận. Ví dụ biết tr(A) = 4 với A vuông cấp 3, thì tr(2A + I) = 2 . 4 + 3 = 11, vì vết của ma trận đơn vị cấp 3 bằng 3.

Lật bảng không đụng tới đường chéo chính, nên:

$$ \text{tr}(A^{T}) = \text{tr}(A) $$

> Lỗi thường gặp: cộng hết mọi phần tử của ma trận. Vết chỉ cộng các ô có chỉ số hàng bằng chỉ số cột.

## Các ma trận đặc biệt

Vài dạng ma trận xuất hiện nhiều đến mức cần nhớ mặt.

- Ma trận không: mọi ô bằng 0.
- Ma trận chéo: mọi ô ngoài đường chéo chính bằng 0.
- Ma trận đơn vị I: ma trận chéo với mọi ô trên đường chéo chính bằng 1.
- Ma trận tam giác trên: mọi ô nằm dưới đường chéo chính bằng 0.
- Ma trận đối xứng: a_ij = a_ji với mọi i, j.

Ma trận đơn vị cấp 3 trông như sau:

:::matrix
I = 1 0 0 ; 0 1 0 ; 0 0 1
:::

Còn đây là một ma trận đối xứng: cứ lật qua đường chéo chính là nó trùng với chính nó.

:::matrix
S = 2 7 -1 ; 7 0 4 ; -1 4 5
:::

Cách gọn nhất để nói một ma trận vuông là đối xứng:

$$ A^{T} = A $$

Quan hệ giữa các dạng: ma trận chéo nào cũng vừa là tam giác trên, vừa đối xứng. Ngược lại thì không đúng, như ma trận S ở trên: đối xứng nhưng không phải ma trận chéo.

> Lỗi thường gặp: tưởng đối xứng là mọi ô ngoài đường chéo chính bằng 0. Đối xứng chỉ đòi hỏi hai ô đối nhau qua đường chéo bằng nhau, chúng có quyền khác 0.
