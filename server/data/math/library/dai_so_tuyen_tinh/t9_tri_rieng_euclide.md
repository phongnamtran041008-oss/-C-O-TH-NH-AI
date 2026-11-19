---
id: dstt_lib_t9
title_vi: Giá trị riêng, không gian Euclide và dạng toàn phương
subject: dai_so_tuyen_tinh
floor: 9
summary_vi: Giá trị riêng và vectơ riêng, chéo hóa, độ dài, góc và trực giao hóa Gram-Schmidt, dạng toàn phương và cách xét dấu, phép chiếu trực giao, và làm quen với PCA, SVD.
skills: [dstt_t9_tri_rieng, dstt_t9_cheo_hoa, dstt_t9_khong_gian_euclide, dstt_t9_dang_toan_phuong, dstt_t9_phep_chieu, dstt_t9_pca_svd]
---
## Giá trị riêng và vectơ riêng

Số t là giá trị riêng của ma trận vuông A nếu có vectơ v khác 0 với Av = tv; v là một vectơ riêng ứng với t. Trong các câu hỏi của Tàng Thư Các, giá trị riêng được viết là t.

$$ Av = tv, \; v \neq 0 \iff \text{det}(A - tI) = 0 $$

Các bước:

1. Lập đa thức đặc trưng p(t) = det(A - tI).
2. Giải p(t) = 0 để có các giá trị riêng.
3. Với mỗi giá trị riêng t0, giải hệ thuần nhất (A - t0 I)x = 0; các nghiệm khác 0 là vectơ riêng.

:::matrix
A = 4 1 ; 2 3
:::

p(t) = (4 - t)(3 - t) - 2 = t^2 - 7t + 10 = (t - 2)(t - 5). Với t = 5: A - 5I có hàng (-1, 1), (2, -2), vectơ riêng (1, 1).

Với ma trận cấp 2: p(t) = t^2 - (tr A) t + det A. Tổng các giá trị riêng bằng vết, tích bằng định thức. Ma trận tam giác có giá trị riêng là các phần tử trên đường chéo.

Nếu Av = tv thì A^k v = t^k v, và với A khả nghịch, A^(-1) v = (1/t) v.

> Lỗi thường gặp: lấy các phần tử đường chéo làm giá trị riêng của một ma trận không tam giác, hoặc chọn vectơ riêng mà không thử lại vào (A - tI)v = 0.

## Chéo hóa ma trận

A cấp n chéo hóa được khi có P khả nghịch và D chéo với

$$ A = P D P^{-1} $$

Điều đó xảy ra khi và chỉ khi A có n vectơ riêng độc lập tuyến tính; khi đó các cột của P là các vectơ riêng và đường chéo của D là các giá trị riêng tương ứng, cùng thứ tự.

- n giá trị riêng thực khác nhau: luôn chéo hóa được.
- Có giá trị riêng bội k: cần không gian riêng của nó có số chiều đúng k, tức rank(A - tI) = n - k.
- Đa thức đặc trưng có nghiệm phức không thực: không chéo hóa được trên R.

:::matrix
J = 2 1 ; 0 2
:::

J có giá trị riêng 2 bội 2, nhưng J - 2I có hạng 1 nên không gian riêng chỉ một chiều: J không chéo hóa được.

Ứng dụng: lũy thừa của ma trận.

$$ A^{k} = P D^{k} P^{-1} $$

> Lỗi thường gặp: đếm số giá trị riêng (tính cả bội) thay vì cộng số chiều các không gian riêng.

## Không gian Euclide và trực giao hóa

Trong R^n với tích vô hướng u . v = u1 v1 + ... + un vn:

$$ \|u\| = \sqrt{u \cdot u}, \qquad \cos \theta = \frac{u \cdot v}{\|u\| \, \|v\|} $$

u và v trực giao (vuông góc) khi u . v = 0. Với u, v trực giao: ||u + v||^2 = ||u||^2 + ||v||^2 (Pythagore). Luôn có bất đẳng thức Cauchy-Schwarz |u . v| <= ||u|| ||v||.

Trực giao hóa Gram-Schmidt biến một họ độc lập u1, u2, u3 thành họ trực giao v1, v2, v3 sinh ra cùng không gian:

$$ v_{1} = u_{1}, \qquad v_{2} = u_{2} - \frac{u_{2} \cdot v_{1}}{v_{1} \cdot v_{1}} v_{1} $$

$$ v_{3} = u_{3} - \frac{u_{3} \cdot v_{1}}{v_{1} \cdot v_{1}} v_{1} - \frac{u_{3} \cdot v_{2}}{v_{2} \cdot v_{2}} v_{2} $$

Muốn họ trực chuẩn thì chia mỗi vi cho độ dài của nó.

Ví dụ u1 = (1, 1, 0), u2 = (1, 0, 1), u3 = (0, 1, 1) cho v2 = (1/2, -1/2, 1) và v3 = (-2/3, 2/3, 2/3).

> Lỗi thường gặp: chia cho ||v1|| thay vì cho v1 . v1 = ||v1||^2 trong hệ số chiếu.

## Dạng toàn phương

Dạng toàn phương trên R^n là q(x) = x^T A x với A đối xứng. Hệ số của x_i^2 nằm trên đường chéo; hệ số của tích x_i x_j được CHIA ĐÔI và đặt vào hai ô (i, j), (j, i).

Ví dụ q(x, y) = 2x^2 + 2xy + 2y^2:

:::matrix
A = 2 1 ; 1 2
:::

A đối xứng nên chéo hóa được bởi một ma trận trực giao. Đổi biến theo cơ sở trực chuẩn gồm vectơ riêng, q có dạng chính tắc

$$ q = t_{1} X^{2} + t_{2} Y^{2} + \ldots $$

với t1, t2, ... là các giá trị riêng. Ở ví dụ trên: q = X^2 + 3Y^2.

Xét dấu:

- Mọi giá trị riêng dương: xác định dương. Mọi giá trị riêng âm: xác định âm.
- Có cả dương lẫn âm: không xác định dấu.

Tiêu chuẩn Sylvester: q xác định dương khi và chỉ khi mọi định thức con chính góc trên bên trái đều dương.

$$ D_{1} > 0, \; D_{2} > 0, \; \ldots, \; D_{n} > 0 $$

> Lỗi thường gặp: quên chia đôi hệ số của tích chéo khi lập ma trận, ví dụ 4yz phải cho hai ô bằng 2.

## Phép chiếu trực giao

Hình chiếu của b lên đường thẳng span{a}:

$$ p = \frac{a \cdot b}{a \cdot a} a, \qquad r = b - p $$

Phần dư r luôn vuông góc với a. Ma trận của phép chiếu đó là a a^T / (a^T a).

Chiếu lên mặt phẳng W qua gốc trong R^3 có vectơ pháp tuyến n: bỏ đi phần dọc theo n.

$$ p = b - \frac{b \cdot n}{n \cdot n} n $$

Ví dụ W = {x + y + z = 0}, b = (1, 2, 6): b . n = 9, n . n = 3, p = (1, 2, 6) - (3, 3, 3) = (-2, -1, 3).

Chiếu lên không gian con W sinh bởi các cột của A (độc lập): giải hệ chuẩn A^T A c = A^T b, rồi p = Ac. Nếu W có cơ sở TRỰC GIAO thì p bằng tổng các hình chiếu lên từng vectơ cơ sở.

Hình chiếu là điểm của W gần b nhất, và ||p|| <= ||b||. Đây là cốt lõi của phương pháp bình phương tối thiểu trong hồi quy.

> Lỗi thường gặp: cộng hình chiếu lên từng vectơ của một cơ sở KHÔNG trực giao. Phải trực giao hóa trước, hoặc giải hệ chuẩn.

## Làm quen PCA và SVD

Phần này là phần mở rộng hướng AI, không có trong đề cương.

PCA (phân tích thành phần chính): cho dữ liệu X, mỗi hàng một điểm, đã trừ trung bình từng cột. Ma trận hiệp phương sai C = X^T X / n đối xứng, nửa xác định dương. Vectơ riêng của C ứng với giá trị riêng lớn nhất là hướng dữ liệu trải rộng nhất; giá trị riêng đó là phương sai theo hướng ấy.

Giữ k hướng đầu tiên thì giữ được một phần của tổng phương sai bằng

$$ \frac{t_{1} + \ldots + t_{k}}{t_{1} + \ldots + t_{n}} $$

Ví dụ bốn điểm (2, 1), (-2, -1), (1, 2), (-1, -2): X^T X có hàng (10, 8), (8, 10), giá trị riêng 18 và 2. Hướng chính là (1, 1), giữ 18/20 = 9/10 phương sai.

SVD (phân tích giá trị kỳ dị): mọi ma trận thực A cỡ m x n viết được

$$ A = U \Sigma V^{T} $$

với U, V trực giao và Sigma "chéo" có các giá trị kỳ dị s1 >= s2 >= ... >= 0. Các s_i là căn bậc hai của các giá trị riêng của A^T A, nên luôn thực và không âm.

:::matrix
A = 1 4 ; 2 -4 ; 2 2
:::

A^T A có hàng (9, 0), (0, 36), nên A có giá trị kỳ dị 6 và 3.

PCA chính là SVD của ma trận dữ liệu: các cột của V là các hướng chính.

> Lỗi thường gặp: quên trừ trung bình trước khi lập ma trận hiệp phương sai, hoặc lấy căn của giá trị riêng của A thay cho của A^T A.
