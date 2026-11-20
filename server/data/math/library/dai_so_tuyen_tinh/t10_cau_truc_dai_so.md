---
id: dstt_lib_t10
title_vi: Tài năng: cấu trúc đại số và dạng song tuyến tính
subject: dai_so_tuyen_tinh
floor: 10
summary_vi: Tầng ẩn đi từ ma trận sang cấu trúc đứng sau nó - quan hệ hai ngôi, phép toán hai ngôi và các tính chất của chúng, nhóm, vành, trường - rồi quay lại với dạng song tuyến tính và dạng toàn phương viết bằng ma trận. Trọng tâm là kiểm tra từng tiên đề một cách chính xác và biết tìm phản ví dụ.
skills: [dstt_t10_quan_he, dstt_t10_phep_toan_hai_ngoi, dstt_t10_nhom, dstt_t10_vanh_truong, dstt_t10_dang_song_tuyen_tinh]
---
## Quan hệ hai ngôi

Một quan hệ R trên tập A là một tập con của A x A; viết a R b khi cặp (a, b) thuộc R. Ba tính chất cần kiểm tra:

- Phản xạ: a R a với mọi a.
- Đối xứng: a R b thì b R a.
- Bắc cầu: a R b và b R c thì a R c.

Quan hệ vừa phản xạ, đối xứng, bắc cầu là quan hệ tương đương; nó chia A thành các lớp tương đương đôi một rời nhau (lớp của a gồm mọi b có b R a). Quan hệ phản xạ, phản đối xứng (a R b và b R a thì a = b) và bắc cầu là quan hệ thứ tự; thứ tự toàn phần nếu hai phần tử bất kỳ đều so sánh được.

$$ a \sim b \iff n \mid (a - b) $$

(hai số cùng lớp khi cùng số dư trong phép chia cho n.)

Ví dụ: trên Z, a ~ b khi a - b chia hết cho 3. Bắc cầu:

1. Giả sử a - b = 3k và b - c = 3m với k, m nguyên.
2. Cộng lại: a - c = 3(k + m), mà k + m nguyên.
3. Vậy a - c chia hết cho 3, tức a ~ c. Có ba lớp, ứng với số dư 0, 1, 2.

Trong ma trận: quan hệ trên {1, ..., n} là một ma trận 0/1 cỡ n x n; phản xạ nghĩa là đường chéo toàn 1, đối xứng nghĩa là ma trận bằng chuyển vị của nó.

> Lỗi thường gặp: kết luận bắc cầu bằng cách "cộng" hai bất đẳng thức, ví dụ |x - y| < 1 và |y - z| < 1 không cho |x - z| < 1 (chỉ cho < 2), nên quan hệ |x - y| < 1 trên R không là quan hệ tương đương; nhầm quan hệ <= (thứ tự) với quan hệ tương đương vì thiếu đối xứng; chỉ kiểm tra một cặp rồi kết luận cho mọi cặp.

## Phép toán hai ngôi

Phép toán hai ngôi trên tập A gán cho mỗi cặp (a, b) một phần tử a * b của A. Các tính chất hay hỏi:

- Giao hoán: a * b = b * a với mọi a, b.
- Kết hợp: (a * b) * c = a * (b * c) với mọi a, b, c.
- Phần tử trung hoà e: a * e = e * a = a với mọi a (nếu có thì duy nhất).
- Phần tử ngược của a: số a' có a * a' = a' * a = e.

$$ (a * b) * c = a * (b * c), \qquad a * e = e * a = a, \qquad a * a' = a' * a = e $$

Muốn chứng minh một tính chất, khai triển cả hai vế cho mọi a, b, c; muốn bác bỏ, chỉ cần một phản ví dụ. Ví dụ phép toán a * b = a + b + ab trên R:

1. Trung hoà: a * e = a + e + ae = a cho e (1 + a) = 0 với mọi a, nên e = 0.
2. Phần tử ngược của a: a + b + ab = 0 cho b = -a/(1 + a), tồn tại khi a khác -1.
3. Số -1 không có phần tử ngược; số 2 có phần tử ngược -2/3.

> Lỗi thường gặp: tìm phần tử ngược mà không biết phần tử trung hoà (phần tử ngược phải đưa về chính phần tử trung hoà, không phải về 1 hay 0 tuỳ ý); coi phép trừ hay trung bình cộng là kết hợp; để phần tử trung hoà phụ thuộc a (nó là một phần tử cố định chung cho mọi a).

## Nhóm và nhóm con

Nhóm (G, *) là tập G với một phép toán kết hợp, có phần tử trung hoà và mọi phần tử đều có phần tử ngược (phép toán phải đóng, tức a * b vẫn thuộc G). Nhóm giao hoán nếu thêm tính giao hoán. Nhóm con H của G là tập con khác rỗng, đóng với phép toán và với phép lấy ngược.

Với một nhóm hữu hạn:

- Cấp của phần tử a là số k nhỏ nhất > 0 có a^k = e (viết cộng: ka = 0).
- Định lý Lagrange: số phần tử của một nhóm con chia hết số phần tử của nhóm; cấp của mỗi phần tử cũng chia hết cấp của nhóm.
- Nhóm cộng Z_n gồm các số dư modulo n; cấp của a là n/gcd(a, n), và a sinh ra cả nhóm khi gcd(a, n) = 1 (có phi(n) phần tử sinh).
- Các phần tử khả nghịch của Z_n (gcd(a, n) = 1) lập thành nhóm nhân có phi(n) phần tử.

$$ \mathrm{ord}(a) = \frac{n}{\mathrm{gcd}(a, n)} \quad (a \in \mathbb{Z}_n), \qquad \mathrm{ord}(a) \mid |G| $$

Ví dụ: nhóm các phần tử khả nghịch của Z_7 (cấp 6) và phần tử 3.

1. 3^1 = 3, 3^2 = 9 = 2, 3^3 = 6 (mọi phép tính modulo 7).
2. 3^6 = (3^3)^2 = 36 = 1.
3. Cấp của 3 chia hết 6 và không phải 1, 2, 3 (các lũy thừa đó khác 1), nên cấp là 6: 3 sinh ra cả nhóm.

> Lỗi thường gặp: dùng nghịch đảo nhân 1/a khi phép toán của nhóm là phép cộng (phần tử ngược là -a); kiểm tra nhóm con mà quên điều kiện đóng hay quên khác rỗng; cho rằng hợp của hai nhóm con là nhóm con (2Z hợp 3Z chứa 2 và 3 nhưng không chứa 2 + 3 = 5); nghĩ rằng một tập con của nhóm có số phần tử bất kỳ đều có thể là nhóm con.

## Vành và trường

Vành là tập có hai phép toán, cộng và nhân: với phép cộng là một nhóm giao hoán, phép nhân kết hợp, và nhân phân phối đối với cộng. Vành giao hoán có đơn vị 1 là vành mà phép nhân giao hoán và có phần tử trung hoà 1. Trường là vành giao hoán có đơn vị 1 khác 0 mà mọi phần tử khác 0 đều khả nghịch.

- Ước của 0: a khác 0 có a b = 0 với một b khác 0; trường không có ước của 0.
- Z là vành giao hoán không có ước của 0 nhưng không là trường (2 không có nghịch đảo); Q, R, C là trường.
- Z_n là trường khi và chỉ khi n nguyên tố; nếu n hợp số thì Z_n có ước của 0 và các phần tử không khả nghịch.
- Ma trận vuông cấp 2 là vành không giao hoán, có ước của 0.

$$ \exists\, b : \; ab \equiv 1 \ (\mathrm{mod}\ n) \iff \mathrm{gcd}(a, n) = 1 $$

Ví dụ Z_8: 2 . 4 = 8 = 0 với 2, 4 khác 0 nên 2 và 4 là ước của 0, không khả nghịch; chỉ 1, 3, 5, 7 khả nghịch (mỗi số tự nghịch đảo của nó, vì 3 . 3 = 9 = 1). Vậy Z_8 là vành giao hoán nhưng không là trường.

> Lỗi thường gặp: thử vài phần tử khả nghịch rồi kết luận mọi phần tử khác 0 đều khả nghịch; nói "vành giao hoán không có ước của 0 là trường" (đúng khi vành hữu hạn, sai với Z); đếm ước của 0 mà quên rằng phần tử khả nghịch không bao giờ là ước của 0.

## Dạng tuyến tính và song tuyến tính

Dạng song tuyến tính f trên R^n gán cho mỗi cặp vectơ (x, y) một số, tuyến tính theo từng biến khi biến kia cố định. Mọi dạng như vậy có ma trận A với phần tử a_ij = f(e_i, e_j) và viết được f(x, y) = x^T A y; thứ tự x, y quan trọng. f đối xứng khi và chỉ khi A^T = A.

Dạng toàn phương của f là q(x) = f(x, x). Nó chỉ phụ thuộc phần đối xứng của A, nên có thể thay A bằng ma trận đối xứng B = (A + A^T)/2, với các phần tử ngoài đường chéo bằng một nửa hệ số của x_i x_j.

$$ f(x, y) = x^{T} A y, \qquad q(x) = x^{T} A x = \sum_{i, j} a_{ij} x_i x_j, \qquad B = \frac{A + A^{T}}{2} $$

Ví dụ về thứ tự: với A như dưới đây, u = (1, 1) và v = (2, -1).

:::matrix
A = 2 1 ; -1 3
:::

1. A v = (2 . 2 + 1 . (-1), -1 . 2 + 3 . (-1)) = (3, -5), nên f(u, v) = u^T (A v) = 3 - 5 = -2.
2. A u = (3, 2), nên f(v, u) = v^T (A u) = 2 . 3 + (-1) . 2 = 4: đổi chỗ hai vectơ cho kết quả khác vì A không đối xứng.

Ví dụ q(x) = 3 x1^2 - 8 x1 x2 + 5 x2^2:

1. Đường chéo của B lấy từ hệ số của x1^2 và x2^2: 3 và 5.
2. Hệ số -8 của x1 x2 chia đều cho hai ô đối xứng: b12 = b21 = -4.
3. Kiểm tra: q(2, 1) = 12 - 16 + 5 = 1 và x^T B x = 3 . 4 + 2 . (-4) . 2 + 5 = 1.

Muốn biết q xác định dương, xét ma trận đối xứng B: với cấp 2, b11 > 0 và det B > 0 (ở ví dụ trên det B = 15 - 16 = -1 nên q nhận cả hai dấu).

> Lỗi thường gặp: chia hệ số x1 x2 không chia đôi (hệ số 2 b12, nên b12 = hệ số/2); đảo thứ tự x, y và đọc A chuyển vị; cho rằng mọi dạng song tuyến tính đều đối xứng; coi hai dạng song tuyến tính có cùng q là một (chúng chỉ cùng phần đối xứng).
