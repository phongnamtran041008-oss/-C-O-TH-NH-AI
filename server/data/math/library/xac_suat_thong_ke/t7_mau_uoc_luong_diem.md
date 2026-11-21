---
id: xs_lib_t7
title_vi: Tổng thể, mẫu và ước lượng điểm
subject: xac_suat_thong_ke
floor: 7
format: 2
summary_vi: Không đo được cả tổng thể thì đo một mẫu ngẫu nhiên: trung bình mẫu và s^2 ước lượng tham số chưa biết, trung bình mẫu tản ít hơn từng số liệu, và hợp lý cực đại chọn tham số làm dữ liệu đã thấy dễ xảy ra nhất.
skills: [xs_t7_tong_the_mau, xs_t7_dac_trung_mau, xs_t7_phan_phoi_mau, xs_t7_uoc_luong_diem, xs_t7_hop_ly_cuc_dai]
---
## Tổng thể và mẫu ngẫu nhiên

:::hook
Muốn biết bao nhiêu phần trăm người dùng thích tính năng mới, không ai hỏi cả triệu người: ta hỏi 500 người chọn ngẫu nhiên rồi suy ra cho cả triệu.
:::

:::figure flow
caption: Tham số cố định nhưng bị giấu; thống kê đổi theo từng mẫu.
box "tổng thể: mu ẩn" tim
link "chọn ngẫu nhiên n"
box "mẫu x_1..x_n" xanh
link "tính"
box "thống kê x_tb" luc
link "ước lượng"
box "mu?" tim
:::

:::core
Tham số là số cố định của tổng thể. Thống kê tính từ mẫu, mỗi mẫu một giá trị: trước khi lấy mẫu, nó là biến ngẫu nhiên.
:::

- Mẫu ngẫu nhiên đơn giản: bốc thăm theo danh sách, mọi nhóm cùng cỡ cùng khả năng. Người tự nguyện, người đứng gần nhất: mẫu lệch.
- X_tb = (X_1 + ... + X_n)/n. Các X_i độc lập khi lấy có hoàn lại hoặc tổng thể rất lớn; không hoàn lại từ tổng thể nhỏ thì không.

Ví dụ: tổng thể là ba số 1, 4, 7. Lấy có hoàn lại 2 lần. P(X_tb >= 5.5)?

1. 3 . 3 = 9 mẫu có thứ tự, mỗi mẫu xác suất 1/9.
2. X_tb >= 5.5 khi tổng >= 11: (4, 7), (7, 4), (7, 7).
3. P = 3/9 = 1/3 (còn mu = 4 thì cố định).

> Lỗi thường gặp: 200 viên đan có 14 viên hỏng, f = 0.07, rồi nói tỷ lệ hỏng của cả lô đúng bằng 0.07. Nó chỉ được ước lượng bằng 0.07.

:::check
Q: Trưởng lão hỏi 50 đệ tử đứng gần Đan phòng nhất để ước lượng tỷ lệ người biết luyện đan. Đó có phải mẫu ngẫu nhiên không?
A: Không: người gần Đan phòng dễ biết luyện đan hơn, mẫu lệch. Phải bốc thăm theo danh sách cả tông môn.
:::

## Trung bình mẫu và phương sai mẫu

:::hook
Đo thời gian phản hồi của máy chủ 5 lần. Trung bình nói "thường mất bao lâu", độ lệch chuẩn nói "ổn định đến đâu".
:::

:::figure bars
caption: Mẫu 3, 5, 6, 8, 8, x_tb = 6. Cột là độ lệch x_i - x_tb: tổng 0, tổng bình phương 18.
size: 180 80
bar "3" -3 do
bar "5" -1 do
bar "6" 0
bar "8" 2
bar "8" 2
:::

:::core
x_tb là tâm của số liệu. s^2 là trung bình bình phương độ lệch, nhưng chia cho n - 1, vì các độ lệch đã đo từ chính x_tb của mẫu.
:::

$$ x_{tb} = \frac{1}{n}\sum_{i=1}^{n} x_i, \qquad s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - x_{tb})^2 $$

Ở hình: s^2 = 18/4 = 9/2. Tính nhanh: tổng (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2 (khai triển bình phương). Bảng tần số: nhân mỗi số hạng với n_i, n = tổng n_i. Cộng 3 vào mọi số liệu: x_tb tăng 3, s^2 giữ nguyên. Tổng = n . x_tb, nên tìm được giá trị thiếu.

Ví dụ: giá trị 2 xuất hiện 3 lần, 4 xuất hiện 2 lần, 6 xuất hiện 1 lần.

1. n = 6, x_tb = (6 + 8 + 6)/6 = 10/3.
2. Tổng n_i x_i^2 = 12 + 32 + 36 = 80; 80 - 6 . (10/3)^2 = 40/3.
3. s^2 = (40/3)/5 = 8/3.

> Lỗi thường gặp: chia cho n thay vì n - 1. Mẫu 3, 5, 7 có s^2 = 8/2 = 4, không phải 8/3.

:::check
Q: Mẫu cỡ 4 có x_tb = 5; ba giá trị là 3, 4, 7. Tìm giá trị thứ tư và s^2.
A: Tổng 20, nên giá trị thứ tư là 6. Độ lệch -2, -1, 2, 1: tổng bình phương 10, s^2 = 10/3.
:::

## Phân phối của trung bình mẫu

:::hook
Một lần đo thời gian tải trang dao động mạnh; trung bình của 100 lần đo thì gần như đứng yên. Đó là lý do người ta luôn lấy trung bình.
:::

:::figure plane
caption: Xanh: một số liệu. Đỏ: trung bình của 4 số liệu, độ lệch chuẩn sigma/2, cùng tâm.
size: 190 80
x: -3.5 3.5 1
y: 0 0.85
names: x f
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
curve "2*exp(-2*x^2)/sqrt(2*pi)" -3.5 3.5 do
:::

:::core
Trung bình mẫu có cùng tâm mu nhưng tản ít hơn: độ lệch chuẩn chỉ còn sigma/sqrt(n). Muốn giảm độ tản một nửa phải lấy mẫu gấp 4.
:::

$$ E(X_{tb}) = \mu, \qquad V(X_{tb}) = \frac{\sigma^2}{n}, \qquad \sigma(X_{tb}) = \frac{\sigma}{\sqrt{n}} $$

Tổng thể chuẩn thì X_tb chuẩn; n lớn thì X_tb xấp xỉ chuẩn. Tổng S = n X_tb có E(S) = n mu, V(S) = n sigma^2.

Ví dụ: tổng thể N(80, 100), n = 25. Tính P(X_tb < 77), dùng Phi(1.5) = 0.4332.

1. Độ lệch chuẩn của X_tb: 10/sqrt(25) = 2.
2. Chuẩn hóa: (77 - 80)/2 = -1.5.
3. P = 0.5 - Phi(1.5) = 0.0668.

> Lỗi thường gặp: chuẩn hóa X_tb bằng sigma thay vì sigma/sqrt(n).

:::check
Q: Tổng thể có sigma = 6. Cần cỡ mẫu n bao nhiêu để độ lệch chuẩn của X_tb bằng 1.5? Khi đó V(X_tb) bằng mấy?
A: sqrt(n) = 6/1.5 = 4, nên n = 16. V(X_tb) = 36/16 = 9/4.
:::

## Ước lượng điểm không chệch

:::hook
Cái cân lệch 2 gam: cân bao nhiêu lần, trung bình vẫn lệch 2 gam. Ước lượng không chệch là cái cân không lệch.
:::

:::figure plane
caption: Xanh: tâm đúng ở mu, không chệch. Đỏ: tâm lệch, lặp mãi vẫn sai về một phía.
size: 190 75
x: -3 5 1
y: 0 0.45
axes: off
line 0 0 0 0.45 xam dash "mu" pos=n
curve "exp(-x^2/2)/sqrt(2*pi)" -3 3 xanh
curve "exp(-(x-2)^2/2)/sqrt(2*pi)" -1 5 do
:::

:::core
T không chệch khi E(T) = tham số: trung bình qua mọi mẫu trúng đúng đích. Giữa hai ước lượng không chệch, cái có phương sai nhỏ hơn thì tốt hơn.
:::

$$ E(X_{tb}) = \mu, \qquad E(s^2) = \sigma^2, \qquad E(f) = p $$

T = c_1 X_1 + ... + c_n X_n có E(T) = (tổng c_i) mu, nên không chệch khi tổng hệ số bằng 1; V(T) = (tổng c_i^2) sigma^2. Chia cho n thay vì n - 1 cho kỳ vọng (n - 1) sigma^2/n: bị chệch, vì E(tổng (X_i - X_tb)^2) = (n - 1) sigma^2.

Ví dụ: T = X_1/2 + X_2/3 + c X_3, sigma^2 = 36.

1. Không chệch: 1/2 + 1/3 + c = 1, nên c = 1/6.
2. V(T) = (1/4 + 1/9 + 1/36) . 36 = 14.
3. X_tb có V = 36/3 = 12 < 14: X_tb tốt hơn.

> Lỗi thường gặp: coi phương sai chia cho n là không chệch. Với sigma^2 = 20 và n = 4, kỳ vọng của nó chỉ là 15.

:::check
Q: T = (X_1 + X_2 + X_3 + X_4)/5 có phải ước lượng không chệch của mu không?
A: Không: tổng hệ số là 4/5, nên E(T) = 4mu/5 khác mu (khi mu khác 0).
:::

## Ước lượng hợp lý cực đại

:::hook
Mô hình ngôn ngữ được huấn luyện bằng cách chỉnh tham số sao cho văn bản đã thấy có xác suất cao nhất. Đó chính là hợp lý cực đại.
:::

:::figure plane
caption: 3 thành công trong 5 lần: L(p) = p^3 (1 - p)^2 cao nhất tại p = 3/5.
size: 180 75
x: 0 1 0.2
y: 0 0.04
names: p L
curve "x^3*(1-x)^2" 0 1 xanh
point 0.6 0.03456 do "p* = 3/5" pos=n
drop 0.6 0.03456
:::

:::core
Chọn tham số làm cho chính dữ liệu đã thấy dễ xảy ra nhất. Lấy ln để tích thành tổng, rồi cho đạo hàm bằng 0.
:::

$$ L(\theta) = \prod_{i=1}^{n} f(x_i; \theta), \qquad \frac{d}{d\theta}\ln L(\theta) = 0 $$

Hay gặp: Bernoulli p* = k/n; Poisson lambda* = x_tb; mũ lambda* = 1/x_tb; số lần thử tới lần thành công đầu p* = 1/x_tb; chuẩn mu* = x_tb. L = C theta^a (1 - theta)^b cho theta* = a/(a + b).

Ví dụ: Poisson, quan sát 1, 4, 2, 5.

1. ln L = -4 lambda + 12 ln lambda + hằng số (n = 4, tổng 12).
2. Đạo hàm: -4 + 12/lambda = 0.
3. lambda* = 3 = x_tb; đạo hàm cấp hai -12/lambda^2 < 0 nên là cực đại.

> Lỗi thường gặp: đạo hàm ln lambda thành lambda. Đạo hàm của ln lambda là 1/lambda.

:::check
Q: Thời gian chờ có mật độ lambda e^(-lambda x). Mẫu 3, 5, 4. Tìm lambda*.
A: ln L = 3 ln lambda - 12 lambda; đạo hàm 3/lambda - 12 = 0 cho lambda* = 1/4 = 1/x_tb.
:::
