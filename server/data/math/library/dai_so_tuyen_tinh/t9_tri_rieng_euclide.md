---
id: dstt_lib_t9
title_vi: Giá trị riêng, không gian Euclide và dạng toàn phương
subject: dai_so_tuyen_tinh
floor: 9
format: 2
summary_vi: Vectơ riêng là hướng ma trận chỉ kéo giãn chứ không xoay; nhìn ma trận theo các hướng đó là chéo hóa. Rồi độ dài, góc và cách làm vuông góc, dạng toàn phương dương hay không, chiếu xuống điểm gần nhất, và PCA chọn hướng dữ liệu trải dài nhất.
skills: [dstt_t9_tri_rieng, dstt_t9_cheo_hoa, dstt_t9_khong_gian_euclide, dstt_t9_dang_toan_phuong, dstt_t9_phep_chieu, dstt_t9_pca_svd]
---
## Giá trị riêng và vectơ riêng

:::hook
Google từng xếp hạng trang web bằng một vectơ riêng của ma trận liên kết: vectơ mà nhân với ma trận xong vẫn giữ nguyên hướng.
:::

:::figure plane
caption: A = [2, 1; 1, 2]. v = (1, 1) giữ hướng, chỉ dài ra 3 lần: vectơ riêng, t = 3. Còn w = (1, 0) bị xoay thành Aw = (2, 1).
size: 150 120
x: -0.5 3.5 1
y: -0.5 3.5 1
vector 0 0 3 3 luc "Av = 3v" pos=nw
vector 0 0 1 1 do "v" pos=se
vector 0 0 2 1 xam "Aw" pos=e
vector 0 0 1 0 xanh "w" pos=s
:::

:::core
Vectơ riêng là hướng mà A chỉ kéo giãn chứ không xoay: Av = tv với v khác 0; giá trị riêng t là hệ số kéo giãn.
:::

Ở đây giá trị riêng viết là t. Cấp 2: p(t) = t^2 - (tr A)t + det A, nên tổng các giá trị riêng là vết, tích là định thức. Ma trận tam giác có giá trị riêng là đường chéo. Nếu Av = tv thì A^k v = t^k v, A^(-1) v = (1/t) v. Cấp 3 có nghiệm nguyên thì thử các ước của det A.

Ví dụ: tìm giá trị riêng, vectơ riêng của A ở hình.

1. p(t) = (2 - t)^2 - 1 = t^2 - 4t + 3 = (t - 1)(t - 3).
2. t = 3: A - 3I = [-1, 1; 1, -1], nên y = x: vectơ (1, 1).
3. t = 1: A - I = [1, 1; 1, 1], nên y = -x: vectơ (1, -1).

$$ Av = tv, \; v \neq 0 \iff \text{det}(A - tI) = 0 $$

> Lỗi thường gặp: lấy đường chéo làm giá trị riêng khi A không tam giác. Ở đây đường chéo là 2, 2 nhưng giá trị riêng là 1 và 3.

:::check
Q: A cấp 2 có giá trị riêng 2 và -1. Tính det A, tr A, và giá trị riêng của A^2 + A.
A: det A = -2, tr A = 1. Av = tv cho (A^2 + A)v = (t^2 + t)v: được 6 và 0.
:::

## Chéo hóa ma trận

:::hook
Dân số sau 100 năm, chuỗi Markov sau 1000 bước: cần A^1000. Chéo hóa biến việc đó thành lũy thừa vài con số.
:::

:::figure flow
caption: A^k = P D^k P^(-1): sang tọa độ vectơ riêng, giãn mỗi trục t^k lần, rồi đổi về.
box "x"
link "P^(-1)"
box "tọa độ riêng"
link "D^k"
box "mỗi trục giãn t^k" xanh
link "P"
box "A^k x" luc
:::

:::core
Chéo hóa là nhìn A trong một cơ sở toàn vectơ riêng; ở đó A chỉ giãn từng trục: A = P D P^(-1), cột của P là vectơ riêng, D là giá trị riêng.
:::

Cần n vectơ riêng độc lập. n giá trị riêng khác nhau: luôn được. Giá trị riêng bội k: không gian riêng phải đủ k chiều. Đa thức đặc trưng vô nghiệm thực: không chéo hóa được trên R.

Ví dụ: A = [1, 2; 0, 3]. Tính A^4.

1. Tam giác: giá trị riêng 1 và 3; vectơ riêng (1, 0) và (1, 1).
2. P = [1, 1; 0, 1], D = [1, 0; 0, 3], P^(-1) = [1, -1; 0, 1].
3. A^4 = P D^4 P^(-1) = [1, 80; 0, 81].

$$ A^{k} = P D^{k} P^{-1} $$

> Lỗi thường gặp: đếm giá trị riêng tính cả bội rồi kết luận chéo hóa được. Phải cộng số chiều các không gian riêng.

:::check
Q: [3, 0; 1, 3] có chéo hóa được không?
A: Không: giá trị riêng 3 bội 2, nhưng A - 3I = [0, 0; 1, 0] có hạng 1, không gian riêng chỉ 1 chiều.
:::

## Không gian Euclide và trực giao hóa

:::hook
Mạng nơ-ron sâu thường khởi tạo trọng số trực giao để tín hiệu không co lại hay nổ tung qua nhiều lớp. Gram-Schmidt là cách bẻ một bộ vectơ cho vuông góc.
:::

:::figure plane
caption: Gọt khỏi u2 phần bóng của nó trên v1 (đứt nét): còn lại v2 = (0, 2), vuông góc với v1.
size: 150 100
x: -0.5 2.5 1
y: -0.5 2.5 1
vector 0 0 2 0 do "v1 = u1" pos=s
vector 0 0 1 2 xam "u2" pos=e
segment 0 0 1 0 muc dash
segment 1 0 1 2 muc dash
vector 0 0 0 2 luc "v2" pos=w
:::

:::core
Gram-Schmidt lần lượt gọt khỏi mỗi vectơ phần bóng của nó trên các vectơ đã có; phần còn lại vuông góc với tất cả.
:::

Độ dài ||u|| = sqrt(u . u); u, v trực giao khi u . v = 0. Khi đó ||u + v||^2 = ||u||^2 + ||v||^2 (Pythagore, bình phương chứ không phải độ dài). Luôn có |u . v| <= ||u|| ||v|| (Cauchy-Schwarz). Muốn trực chuẩn, chia mỗi v_i cho độ dài của nó.

Ví dụ: trực giao hóa u1 = (1, 1), u2 = (2, 0).

1. v1 = u1 = (1, 1).
2. Hệ số bóng: u2 . v1 / v1 . v1 = 2/2 = 1.
3. v2 = (2, 0) - (1, 1) = (1, -1). Thử: v2 . v1 = 1 - 1 = 0.

$$ v_{1} = u_{1}, \qquad v_{2} = u_{2} - \frac{u_{2} \cdot v_{1}}{v_{1} \cdot v_{1}} v_{1} $$

> Lỗi thường gặp: chia cho ||v1|| thay vì cho v1 . v1 = ||v1||^2. Bóng sẽ dài sai và v2 không còn vuông góc.

:::check
Q: u = (3, 0), v = (0, 4) vuông góc. ||u + v|| bằng bao nhiêu? Có bằng ||u|| + ||v|| không?
A: ||u + v||^2 = 9 + 16 = 25, nên ||u + v|| = 5, khác 3 + 4 = 7.
:::

## Dạng toàn phương

:::hook
Gần điểm tối ưu, hàm mất mát trông như một dạng toàn phương. Nó là đáy bát hay yên ngựa quyết định thuật toán đã tới cực tiểu thật hay chưa.
:::

:::figure grid
caption: q = x^2 + 2y^2 + 3z^2 + 2xy - 4yz. Bình phương lên đường chéo; hệ số tích chéo CHIA ĐÔI vào hai ô đối xứng: 2xy cho hai ô 1, -4yz cho hai ô -2.
table "A"
head x y z
side x y z
row 1 1 0
row 1 2 -2
row 0 -2 3
mark cell 1 2 vang
mark cell 2 1 vang
mark cell 2 3 do
mark cell 3 2 do
:::

:::core
q xác định dương khi q(x) > 0 theo mọi hướng x khác 0 (đáy bát), tức mọi giá trị riêng của ma trận đối xứng của q đều dương.
:::

Có giá trị riêng dương lẫn âm: không xác định dấu (yên ngựa). Tiêu chuẩn Sylvester: xác định dương khi các định thức con góc trên trái D_1, D_2, ... đều dương. Ở hình: D_1 = 1, D_2 = 1, D_3 = -1, nên không xác định dương.

Ví dụ: tìm m để q = x^2 + 6xy + my^2 xác định dương.

1. Chia đôi 6: A = [1, 3; 3, m].
2. D_1 = 1 > 0, D_2 = m - 9.
3. Cần m - 9 > 0: m > 9.

$$ D_{1} > 0, \; D_{2} > 0, \; \ldots, \; D_{n} > 0 $$

> Lỗi thường gặp: đặt nguyên hệ số tích chéo vào cả hai ô. Ô (1, 2) và (2, 1) cộng lại mới ra hệ số của xy.

:::check
Q: q = x^2 - 2xy + y^2 có xác định dương không?
A: Không: q = (x - y)^2 bằng 0 tại (1, 1) khác 0. Ma trận [1, -1; -1, 1] có D_2 = 0, không dương.
:::

## Phép chiếu trực giao

:::hook
Hồi quy tuyến tính chính là phép chiếu: dữ liệu b không nằm trên mặt phẳng các dự đoán, nên lấy điểm của mặt phẳng gần b nhất.
:::

:::figure plane
caption: Chiếu b = (1, 3) lên đường của a = (2, 1): p = (5/5)a = (2, 1). Phần dư r = (-1, 2) vuông góc với a.
size: 150 110
x: -1 3.5 1
y: -0.5 3.5 1
line 0 0 2 1 xam
vector 0 0 1 3 xanh "b" pos=w
vector 0 0 2 1 do "p" pos=se
segment 2 1 1 3 luc dash "r" pos=e
:::

:::core
Hình chiếu của b là điểm gần b nhất trên đường hay mặt phẳng; phần dư b - p luôn vuông góc với chỗ được chiếu lên.
:::

Chiếu lên mặt phẳng qua gốc có pháp tuyến n: bỏ đi phần của b dọc theo n. Ma trận chiếu lên span{a} là a a^T / (a^T a). Cộng hình chiếu lên từng vectơ chỉ đúng khi cơ sở trực giao.

Ví dụ: chiếu b = (3, 1, 1) lên mặt phẳng x + z = 0.

1. n = (1, 0, 1): b . n = 4, n . n = 2.
2. Phần dọc n: 2n = (2, 0, 2).
3. p = (3, 1, 1) - (2, 0, 2) = (1, 1, -1). Thử: 1 + (-1) = 0.

$$ p = \frac{a \cdot b}{a \cdot a} a, \qquad r = b - p $$

$$ p = b - \frac{b \cdot n}{n \cdot n} n $$

> Lỗi thường gặp: cộng hình chiếu lên hai vectơ không vuông góc của mặt phẳng. Phải trực giao hóa trước, hoặc chiếu qua pháp tuyến.

:::check
Q: p là hình chiếu của b lên một không gian con. ||p|| có thể lớn hơn ||b|| không?
A: Không: b = p + r với r vuông góc p, nên ||b||^2 = ||p||^2 + ||r||^2 >= ||p||^2.
:::

## Làm quen PCA và SVD

:::hook
Ảnh khuôn mặt có hàng nghìn chiều. PCA tìm vài hướng dữ liệu trải rộng nhất, giữ chúng và vứt phần còn lại mà vẫn giữ được gần hết thông tin.
:::

:::figure plane
caption: Bốn điểm (3, 1), (1, 3), (-3, -1), (-1, -3) trải dài theo hướng (1, 1) (xanh), hẹp theo hướng (1, -1) (đỏ).
size: 150 120
x: -3.5 3.5 1
y: -3.5 3.5 1
line 0 0 1 1 xanh
line 0 0 1 -1 do dash
point 3 1 muc
point 1 3 muc
point -3 -1 muc
point -1 -3 muc
:::

:::core
PCA tìm hướng dữ liệu trải dài nhất: đó là vectơ riêng của ma trận hiệp phương sai, và giá trị riêng là độ trải theo hướng ấy.
:::

Trước hết trừ trung bình mỗi cột. SVD: mọi ma trận A = U Sigma V^T; các giá trị kỳ dị là căn bậc hai giá trị riêng của A^T A, luôn thực và không âm. Phần phương sai giữ lại là tổng giá trị riêng giữ chia tổng tất cả.

Ví dụ: PCA với bốn điểm ở hình (trung bình đã bằng 0), S = X^T X.

1. Tổng x^2 = 20, tổng y^2 = 20, tổng xy = 12: S = [20, 12; 12, 20].
2. p(t) = (20 - t)^2 - 144: giá trị riêng 32 và 8.
3. t = 32 cho hướng (1, 1); giữ 1 hướng được 32/40 = 4/5 phương sai.

$$ \frac{t_{1} + \ldots + t_{k}}{t_{1} + \ldots + t_{n}} $$

> Lỗi thường gặp: quên trừ trung bình trước khi lập ma trận hiệp phương sai; hoặc lấy căn giá trị riêng của A thay cho của A^T A.

:::check
Q: A cỡ 3 x 2 có hai cột (1, 2, 2) và (6, 3, -6). Tìm các giá trị kỳ dị của A.
A: Hai cột vuông góc (6 + 6 - 12 = 0), dài 3 và 9: A^T A = [9, 0; 0, 81]. Giá trị kỳ dị 9 và 3.
:::
