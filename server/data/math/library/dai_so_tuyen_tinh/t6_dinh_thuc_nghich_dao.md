---
id: dstt_lib_t6
title_vi: Định thức, hạng và ma trận nghịch đảo
subject: dai_so_tuyen_tinh
floor: 6
summary_vi: Một con số nói ma trận vuông có khả nghịch hay không, cách tính nó bằng công thức, bằng khai triển và bằng khử Gauss; hạng; nghịch đảo và hai cách giải hệ vuông.
skills: [dstt_t6_dinh_thuc_cap_2_3, dstt_t6_khai_trien, dstt_t6_tinh_chat_dinh_thuc, dstt_t6_hang, dstt_t6_nghich_dao, dstt_t6_giai_he_nghich_dao]
---
## Định thức cấp 2 và cấp 3

Định thức chỉ có ở ma trận vuông. Với cấp 2:

$$ \text{det} \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc $$

Với cấp 3, quy tắc Sarrus: cộng ba tích theo đường chéo xuống, trừ ba tích theo đường chéo lên.

$$ D_{\text{xuong}} = a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32} $$

$$ D_{\text{len}} = a_{13}a_{22}a_{31} + a_{11}a_{23}a_{32} + a_{12}a_{21}a_{33} $$

$$ \text{det} A = D_{\text{xuong}} - D_{\text{len}} $$

Ví dụ:

:::matrix
A = 1 2 3 ; 0 1 4 ; 5 6 0
:::

Ba tích xuống là 0, 40, 0; ba tích lên là 15, 24, 0. Vậy det A = 40 - 39 = 1.

Khi một phần tử là ẩn x, định thức là một biểu thức của x; đặt nó bằng giá trị đề cho rồi giải. Ví dụ ma trận có hàng (x, 2) và (3, x + 1) có định thức x^2 + x - 6, bằng 0 khi x = 2 hoặc x = -3.

Quy tắc Sarrus chỉ dùng cho cấp 3; cấp 4 trở lên phải khai triển hoặc khử Gauss.

> Lỗi thường gặp: cộng cả sáu tích. Ba tích theo đường chéo lên mang dấu trừ.

## Khai triển theo hàng hoặc cột

Bỏ hàng i và cột j của A được định thức con M_ij. Phần bù đại số gắn thêm dấu theo vị trí:

$$ C_{ij} = (-1)^{i + j} M_{ij} $$

Dấu theo vị trí xếp như bàn cờ, bắt đầu bằng dấu cộng ở góc trên bên trái. Định thức bằng tổng các phần tử của một hàng (hoặc một cột) nhân với phần bù đại số của chúng:

$$ \text{det} A = a_{i1}C_{i1} + a_{i2}C_{i2} + \ldots + a_{in}C_{in} $$

Mỗi số 0 trên hàng được chọn xóa đi một số hạng, nên hãy chọn hàng hoặc cột có nhiều số 0 nhất.

:::matrix
A = 2 0 1 ; 3 0 -1 ; 1 4 5
:::

Cột 2 chỉ còn a_32 = 4. M_32 có hàng (2, 1) và (3, -1), bằng -5; dấu ở (3, 2) là -1 nên C_32 = 5. Vậy det A = 4 . 5 = 20.

> Lỗi thường gặp: quên dấu (-1)^(i + j), coi C_ij = M_ij. Ở vị trí (1, 2), (2, 1), (2, 3), (3, 2) dấu là trừ.

## Tính chất của định thức

Ba phép biến đổi hàng làm định thức đổi một cách biết trước:

- Đổi chỗ hai hàng: định thức đổi dấu.
- Nhân một hàng với k: định thức nhân với k.
- Cộng bội của một hàng vào hàng khác: định thức không đổi.

Vì vậy cách tính nhanh nhất cho ma trận lớn là khử Gauss về dạng tam giác, nhớ các lần đổi chỗ hàng, rồi nhân các phần tử trên đường chéo. Ma trận tam giác có định thức bằng tích đường chéo chính.

Các quy tắc với phép toán ma trận, cho A, B vuông cấp n:

$$ \text{det}(AB) = \text{det} A \cdot \text{det} B, \qquad \text{det}(A^{T}) = \text{det} A $$

$$ \text{det}(kA) = k^{n} \, \text{det} A $$

Hệ quả: det(AB) = det(BA) dù AB có thể khác BA, và det(A^2) = (det A)^2.

Không có quy tắc cộng: nói chung det(A + B) khác det A + det B. Với A = B = I cấp 2, vế trái là 4 còn vế phải là 2.

> Lỗi thường gặp: viết det(kA) = k det A. Nhân cả ma trận với k là nhân n hàng với k, nên định thức nhân với k mũ n.

## Hạng của ma trận

Hạng của A là số hàng khác không của một dạng bậc thang của A, viết rank A. Dạng bậc thang không duy nhất nhưng số hàng khác không thì luôn như nhau.

$$ \text{rank} A \le \text{min}(m, n) \quad \text{voi } A \text{ co } m \times n $$

Ví dụ:

:::matrix
A = 1 2 1 ; 2 4 2 ; 1 0 3
:::

Hàng 2 gấp đôi hàng 1 nên R2 - 2R1 là hàng 0; R3 - R1 = (0, -2, 2). Dạng bậc thang có hai hàng khác không: rank A = 2.

Với ma trận vuông cấp n: rank A = n khi và chỉ khi det A khác 0. Hạng còn cho số ẩn tự do của hệ Ax = 0: bằng số ẩn trừ rank A.

> Lỗi thường gặp: đếm số hàng khác không của chính A mà chưa khử Gauss. Một hàng khác không vẫn có thể bị khử thành 0.

## Ma trận nghịch đảo

Ma trận vuông A khả nghịch khi có B với AB = BA = I; khi đó B là duy nhất, viết A^(-1).

$$ A \text{ kha nghich} \Leftrightarrow \text{det} A \neq 0 $$

Cách tìm nghịch đảo bằng khử Gauss-Jordan: lập (A | I), biến đổi hàng cho đến khi bên trái thành I, khi đó bên phải là A^(-1).

:::matrix
A = 1 2 ; 3 7
:::

(1, 2 | 1, 0) và (3, 7 | 0, 1); R2 - 3R1 cho (0, 1 | -3, 1); R1 - 2R2 cho (1, 0 | 7, -2). Vậy A^(-1) có hàng (7, -2) và (-3, 1).

Với cấp 2 có công thức: đổi chỗ hai phần tử trên đường chéo chính, đổi dấu hai phần tử kia, rồi chia cho định thức.

$$ \begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} $$

Các quy tắc: nghịch đảo của tích đảo thứ tự, và đi qua phép chuyển vị.

$$ (AB)^{-1} = B^{-1} A^{-1}, \qquad (A^{T})^{-1} = (A^{-1})^{T} $$

$$ \text{det}(A^{-1}) = \frac{1}{\text{det} A} $$

> Lỗi thường gặp: viết (AB)^(-1) = A^(-1) B^(-1). Thử lại bằng phép nhân sẽ thấy ngay: (AB)(B^(-1) A^(-1)) = I, còn thứ tự kia thì không.

## Giải hệ bằng nghịch đảo và quy tắc Cramer

Khi A vuông và khả nghịch, hệ Ax = b có đúng một nghiệm:

$$ x = A^{-1} b $$

Nhân A^(-1) ở bên trái, vì b A^(-1) không nhân được.

Quy tắc Cramer cho từng ẩn một: thay cột thứ k của A bằng vế phải b được ma trận A_k, rồi

$$ x_{k} = \frac{\text{det} A_{k}}{\text{det} A} $$

Ví dụ hệ x + 2y = 5, 3x + 4y = 6: det A = -2. Thay cột 1 bằng (5, 6) được hàng (5, 2) và (6, 4), định thức 8, nên x = -4; thay cột 2 được hàng (1, 5) và (3, 6), định thức -9, nên y = 9/2.

Cả hai cách chỉ dùng được khi det A khác 0. Khi det A = 0, hệ vô nghiệm hoặc vô số nghiệm, và phải khử Gauss để biết là trường hợp nào.

> Lỗi thường gặp: thay một HÀNG của A bằng b. Quy tắc Cramer thay CỘT của ẩn cần tìm.
