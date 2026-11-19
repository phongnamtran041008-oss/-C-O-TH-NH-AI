---
id: dstt_lib_t4
title_vi: Nhân ma trận
subject: dai_so_tuyen_tinh
floor: 4
summary_vi: Phép nhân ma trận là hàng nhân cột: khi nào nhân được, cách tính từng ô, vì sao đổi thứ tự thì đổi kết quả, và các luật còn giữ được.
skills: [dstt_t4_tich_vo_huong, dstt_t4_dieu_kien_kich_thuoc, dstt_t4_nhan_ma_tran, dstt_t4_khong_giao_hoan, dstt_t4_tinh_chat_nhan, dstt_t4_luy_thua]
---
## Tích vô hướng: một hàng nhân một cột

Mọi phép nhân ma trận đều dựng từ một viên gạch nhỏ: tích vô hướng của hai vectơ cùng số chiều. Nhân từng cặp tọa độ cùng vị trí rồi cộng tất cả lại.

$$ u \cdot v = u_{1}v_{1} + u_{2}v_{2} + \ldots + u_{n}v_{n} $$

Kết quả là một số, không phải một vectơ.

Ví dụ với u = (1, -2, 3) và v = (4, 0, -1):

1. Nhân từng cặp: 1 . 4 = 4, (-2) . 0 = 0, 3 . (-1) = -3.
2. Cộng lại: 4 + 0 - 3 = 1.

Hai vectơ có tích vô hướng bằng 0 gọi là vuông góc với nhau; tầng 9 sẽ dùng lại điều này.

> Lỗi thường gặp: quên dấu khi nhân số âm, như viết (-3) . 4 = 12. Hãy viết rõ dấu của từng tích trước khi cộng.

## Điều kiện kích thước để nhân

Tích AB chỉ xác định khi số cột của A bằng số hàng của B. Khi đó AB lấy số hàng của A và số cột của B:

$$ (m \times n) \cdot (n \times p) = m \times p $$

Cách nhớ: viết hai cỡ cạnh nhau, hai số ở giữa phải bằng nhau và "triệt tiêu", hai số ở ngoài là cỡ của tích.

- A cỡ 2 x 3, B cỡ 3 x 4: nhân được, AB cỡ 2 x 4.
- Cũng hai ma trận đó, BA là (3 x 4)(2 x 3): 4 khác 2, không nhân được.
- Với mọi A cỡ m x n, cả A^T A (cỡ n x n) lẫn A A^T (cỡ m x m) đều xác định.

Hai ma trận cùng cỡ chưa chắc nhân được: hai ma trận cùng cỡ 3 x 2 thì không nhân được với nhau.

> Lỗi thường gặp: so số hàng với số hàng, hoặc đòi hai ma trận cùng cỡ. Điều kiện duy nhất là số cột của ma trận trước bằng số hàng của ma trận sau.

## Nhân hai ma trận

Phần tử ở hàng i, cột j của AB là tích vô hướng của hàng i của A với cột j của B.

$$ (AB)_{ij} = a_{i1}b_{1j} + a_{i2}b_{2j} + \ldots + a_{in}b_{nj} $$

Ví dụ với hai ma trận cỡ 2 x 2:

:::matrix
A = 1 2 ; 3 4
B = 2 0 ; 1 -1
:::

Ô hàng 1, cột 1 là (1, 2) . (2, 1) = 4; ô hàng 1, cột 2 là (1, 2) . (0, -1) = -2. Làm tương tự với hàng 2 được tích:

:::matrix
C = 4 -2 ; 10 -4
:::

Hai hệ quả nên nhớ: nếu hàng i của A toàn số 0 thì hàng i của AB cũng toàn số 0; và một ma trận nhân với một vectơ cột cho một vectơ cột, mỗi tọa độ là một hàng nhân vectơ đó.

> Lỗi thường gặp: nhân từng ô cùng vị trí như phép cộng. Nhân ma trận luôn là hàng của ma trận trước nhân cột của ma trận sau.

## AB != BA

Phép nhân ma trận không giao hoán. Ngay cả khi cả AB và BA đều xác định và cùng cỡ, hai kết quả thường khác nhau.

:::matrix
A = 1 1 ; 0 1
B = 1 0 ; 1 1
:::

Với hai ma trận này, AB có hàng (2, 1) và (1, 1), còn BA có hàng (1, 1) và (1, 2).

Có những cặp giao hoán: mọi ma trận giao hoán với chính nó, với I và với các bội kI; A giao hoán với mọi đa thức của A như 2A + 3I.

Một điều lạ khác: AB có thể là ma trận không trong khi A và B đều khác không.

:::matrix
A = 0 1 ; 0 0
B = 1 0 ; 0 0
:::

Ở đây AB = 0 nhưng BA có hàng (0, 1) và (0, 0).

Vì không giao hoán, các hằng đẳng thức quen thuộc phải viết lại:

$$ (A + B)^{2} = A^{2} + AB + BA + B^{2} $$

> Lỗi thường gặp: gộp AB + BA thành 2AB, hoặc viết (A + B)(A - B) = A^2 - B^2. Hai bước này chỉ đúng khi AB = BA.

## Tính chất của phép nhân ma trận

Mất tính giao hoán nhưng phép nhân ma trận giữ được các luật còn lại, miễn là các cỡ phù hợp:

$$ A(BC) = (AB)C $$

$$ A(B + C) = AB + AC, \quad (B + C)A = BA + CA $$

$$ (kA)B = k(AB) = A(kB) $$

Tính kết hợp cho phép chọn thứ tự tính cho gọn: với A cỡ 1 x 2, B cỡ 2 x 1, C cỡ 1 x 2, tính AB trước chỉ là một số.

Chuyển vị một tích thì đảo thứ tự:

$$ (AB)^{T} = B^{T} A^{T} $$

Lý do: ô (i, j) của (AB)^T là hàng j của A nhân cột i của B, cũng chính là hàng i của B^T nhân cột j của A^T.

> Lỗi thường gặp: viết (AB)^T = A^T B^T. Khi A, B không vuông thì A^T B^T thường không nhân được; khi vuông thì nó thường cho một ma trận khác.

## Ma trận đơn vị và lũy thừa ma trận

Ma trận đơn vị I đóng vai số 1 trong phép nhân:

$$ AI = IA = A $$

Với A vuông, lũy thừa là nhân A với chính nó nhiều lần: A^2 = A . A, A^3 = A^2 . A, và quy ước A^0 = I. Chỉ ma trận vuông mới có lũy thừa.

Một vài dạng tính nhanh:

- Ma trận chéo: lũy thừa từng phần tử trên đường chéo, ví dụ đường chéo 2, -1, 3 cho A^4 có đường chéo 16, 1, 81.
- Ma trận có hàng (1, a) và (0, 1): A^n có hàng (1, na) và (0, 1).
- Nếu A^2 = I thì A^n bằng I khi n chẵn, bằng A khi n lẻ.

:::matrix
A = 0 1 ; 1 0
:::

Ma trận trên có A^2 = I, nên A^2025 = A.

> Lỗi thường gặp: tính A^2 bằng cách bình phương từng ô. A^2 là tích A . A, chỉ với ma trận chéo thì hai cách mới trùng nhau.
