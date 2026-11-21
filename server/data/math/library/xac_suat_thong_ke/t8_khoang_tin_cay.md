---
id: xs_lib_t8
title_vi: Khoảng tin cậy, luật số lớn và định lý giới hạn trung tâm
subject: xac_suat_thong_ke
floor: 8
format: 2
summary_vi: Một ước lượng đi kèm sai số: khoảng tin cậy bắt được tham số trong 95 trên 100 lần lấy mẫu, cỡ mẫu chọn để sai số đủ nhỏ; luật số lớn giữ trung bình sát kỳ vọng, và tổng của nhiều biến độc lập ra hình chuông.
skills: [xs_t8_tin_cay_trung_binh, xs_t8_tin_cay_ty_le, xs_t8_co_mau, xs_t8_luat_so_lon, xs_t8_gioi_han_trung_tam]
---
## Khoảng tin cậy cho trung bình

:::hook
"Mô hình chạy trung bình 50 mili giây" chưa đủ: phải nói thêm "cộng trừ bao nhiêu" thì mới biết con số đó chắc đến đâu.
:::

:::figure plane
caption: Mỗi mẫu cho một khoảng. Lặp rất nhiều lần, 95% số khoảng bắt được mu; khoảng đỏ trượt.
size: 190 85
axes: off
x: 44 56
y: 0 8
line 50 0 50 8 xam dash "mu" pos=n
segment 47 1 51 1 xanh
segment 49 2 53 2 xanh
segment 48.5 3 52.5 3 xanh
segment 51.5 4 55.5 4 do
segment 46.5 5 50.5 5 xanh
segment 48 6 52 6 xanh
segment 49.5 7 53.5 7 xanh
:::

:::core
Khoảng tin cậy là x_tb cộng trừ một sai số epsilon. "95%" là của cách lập khoảng: lấy mẫu 100 lần thì khoảng 95 khoảng chứa mu.
:::

$$ \varepsilon = z\,\frac{\sigma}{\sqrt{n}}, \qquad 2\,\Phi(z) = 1 - \alpha $$

Biết sigma: z = 1.645 (90%), 1.96 (95%), 2.58 (99%). Biết khoảng thì x_tb là điểm giữa, epsilon là nửa độ dài.

Ví dụ: sigma = 12, n = 36, x_tb = 50, độ tin cậy 95%.

1. sigma/sqrt(n) = 12/6 = 2.
2. epsilon = 1.96 . 2 = 3.92.
3. Khoảng (46.08; 53.92).

> Lỗi thường gặp: đọc là "95% số liệu nằm trong khoảng". Khoảng nói về mu, không nói về từng số liệu.

:::check
Q: sigma = 10, độ tin cậy 95%, khoảng tin cậy là (38.04; 41.96). Tìm x_tb và cỡ mẫu n.
A: x_tb = 40 (điểm giữa), epsilon = 1.96. 1.96 . 10/sqrt(n) = 1.96 cho sqrt(n) = 10, n = 100.
:::

### Chưa biết sigma: dùng Student

Tổng thể chuẩn mà không biết sigma: thay sigma bằng độ lệch chuẩn mẫu s. Vì s cũng dao động, z được thay bằng giá trị tới hạn Student t(k; a) lớn hơn một chút, với k = n - 1 bậc tự do và a = alpha/2 mỗi phía (P(T > t(k; a)) = a).

$$ \varepsilon = t(n-1;\, \alpha/2)\,\frac{s}{\sqrt{n}} $$

Ví dụ: n = 25, x_tb = 30, s = 10, độ tin cậy 95%, t(24; 0.025) = 2.064.

1. s/sqrt(n) = 10/5 = 2.
2. epsilon = 2.064 . 2 = 4.128.
3. Khoảng (25.872; 34.128).

> Lỗi thường gặp: dùng n thay vì n - 1 bậc tự do, hay lấy t(n - 1; 0.05) (một phía) cho khoảng 95% hai phía.

:::check
Q: Mẫu n = 16 từ tổng thể chuẩn, chưa biết sigma, cần khoảng 90% hai phía. Tra giá trị tới hạn nào?
A: t(15; 0.05): 15 bậc tự do, mỗi phía (1 - 0.9)/2 = 0.05.
:::

## Khoảng tin cậy cho tỷ lệ

:::hook
Thử nghiệm A/B: 144 trong 400 người bấm nút mới. Tỷ lệ thật trên mọi người dùng nằm trong khoảng nào?
:::

:::figure numberline
caption: f = 0.36, epsilon = 0.047: khoảng 95% là (0.313; 0.407).
size: 200 45
range: 0.25 0.45 0.05
interval 0.31296 0.40704 ( ) xanh
point 0.36 do "f = 0.36"
:::

:::core
Với tỷ lệ, tâm là tần suất f = m/n và sai số chuẩn là sqrt(f(1 - f)/n): n nằm trong căn.
:::

$$ \varepsilon = z\,\sqrt{\frac{f(1-f)}{n}} $$

f có E(f) = p, V(f) = p(1 - p)/n. Xấp xỉ chuẩn dùng được khi nf và n(1 - f) đều lớn.

Ví dụ: 144 trong 400, độ tin cậy 95%.

1. f = 144/400 = 0.36.
2. Sai số chuẩn: sqrt(0.36 . 0.64/400) = 0.48/20 = 0.024.
3. epsilon = 1.96 . 0.024 = 0.04704; khoảng (0.31296; 0.40704).

> Lỗi thường gặp: để n ra ngoài căn: sqrt(0.36 . 0.64)/400 nhỏ đi 20 lần, khoảng hẹp giả tạo.

:::check
Q: 50 trong 100 viên đan đạt chuẩn. Sai số epsilon của khoảng tin cậy 95% cho tỷ lệ đạt chuẩn là bao nhiêu?
A: f = 0.5, sai số chuẩn sqrt(0.25/100) = 0.05, epsilon = 1.96 . 0.05 = 0.098.
:::

### Đọc ngược một khoảng tin cậy

Khoảng tin cậy đối xứng quanh f, nên khi chỉ biết khoảng: f là điểm giữa, epsilon là nửa độ dài, và số trường hợp trong mẫu là f . n.

Ví dụ: mẫu 500 người, khoảng 95% cho tỷ lệ là (0.56; 0.64).

1. f = (0.56 + 0.64)/2 = 0.6, epsilon = 0.04.
2. Số người có tính chất đó: 0.6 . 500 = 300.

:::check
Q: Mẫu 200 người, khoảng tin cậy 95% cho tỷ lệ là (0.3; 0.5). Có bao nhiêu người trong mẫu có tính chất đó?
A: f là điểm giữa: 0.4. Số người: 0.4 . 200 = 80.
:::

## Chọn cỡ mẫu theo độ chính xác

:::hook
Khảo sát tốn tiền theo từng người hỏi. Hỏi bao nhiêu người là vừa đủ để sai số dưới mức mình cần?
:::

:::figure plane
caption: Sai số 1.96 . 10/sqrt(n) giảm chậm. Muốn nó <= 2 cần n >= 96.04: chọn n = 97.
size: 190 80
x: 0 200 50
y: 0 6 2
names: n e
curve "19.6/sqrt(x)" 10 200 xanh
line 0 2 200 2 do dash "e = 2" pos=ne
point 96.04 2 do "n = 97" pos=n
:::

:::core
Sai số tỉ lệ với 1/sqrt(n): đặt sai số không vượt mức cho phép, giải ra n, rồi luôn làm tròn lên. Muốn sai số giảm một nửa phải tăng n gấp 4.
:::

$$ n \ge \left(\frac{z\,\sigma}{\varepsilon_0}\right)^2 $$

Ví dụ: sigma = 9, độ tin cậy 95%, sai số không quá 2.

1. n >= (1.96 . 9/2)^2 = 8.82^2 = 77.7924.
2. Làm tròn lên: n = 78.

> Lỗi thường gặp: làm tròn xuống (77.79 thành 77 là thiếu), hoặc lấy độ dài khoảng làm epsilon: dài 4 nghĩa là epsilon = 2.

:::check
Q: sigma = 5, độ tin cậy 95%, muốn khoảng tin cậy dài không quá 2. Cần n nhỏ nhất bao nhiêu?
A: Dài 2 nghĩa là epsilon <= 1: n >= (1.96 . 5)^2 = 96.04, nên n = 97.
:::

### Cỡ mẫu cho một tỷ lệ

Với tỷ lệ, sai số là z sqrt(p(1 - p)/n). Có mẫu thử thì thay p bằng f của mẫu thử. Chưa biết gì thì dùng trường hợp xấu nhất: p(1 - p) lớn nhất bằng 1/4, khi p = 1/2.

$$ n \ge \frac{z^2\, p(1-p)}{\varepsilon_0^2} $$

Ví dụ: chưa biết gì về p, độ tin cậy 90% (z = 1.645), sai số không quá 0.03.

1. Dùng p(1 - p) = 1/4.
2. n >= 1.645^2/(4 . 0.03^2) = 751.67.
3. Làm tròn lên: n = 752.

:::check
Q: Mẫu thử cho f = 0.2. Độ tin cậy 95%, sai số không quá 0.04. Cần n nhỏ nhất bao nhiêu?
A: n >= 1.96^2 . 0.16/0.04^2 = 384.16, nên n = 385.
:::

## Luật số lớn

:::hook
Vì sao sòng bạc luôn thắng về lâu dài, dù từng ván ai thắng cũng được? Vì trung bình của rất nhiều ván bị kéo sát về kỳ vọng.
:::

:::figure plane
caption: Với mọi phân phối, hai đuôi đỏ ngoài mu cộng trừ e cộng lại không quá V/e^2.
size: 180 80
x: -3.5 3.5 1
y: 0 0.45
axes: off
area "exp(-x^2/2)/sqrt(2*pi)" -3.5 -1.5 do
area "exp(-x^2/2)/sqrt(2*pi)" 1.5 3.5 do
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
line -1.5 0 -1.5 0.42 xam dash "mu - e" pos=n
line 1.5 0 1.5 0.42 xam dash "mu + e" pos=n
:::

:::core
Trung bình của nhiều lần thử dính sát kỳ vọng: xác suất lệch quá epsilon không vượt sigma^2/(n epsilon^2), về 0 khi n lớn.
:::

$$ P\left(|Y - E(Y)| \ge \varepsilon\right) \le \frac{V(Y)}{\varepsilon^2} $$

Bất đẳng thức Chebyshev đúng cho mọi biến có phương sai. Đảo lại: P(|X - mu| < epsilon) >= 1 - V/epsilon^2.

> Lỗi thường gặp: quên bình phương epsilon. Với V = 16 và epsilon = 8 phải chia cho 64, không chia cho 8.

:::check
Q: E(X) = 10, V(X) = 4. Dùng Chebyshev, tìm một cận dưới của P(5 < X < 15).
A: epsilon = 5: P(|X - 10| < 5) >= 1 - 4/25 = 21/25.
:::

### Từ Chebyshev tới luật số lớn

Áp Chebyshev cho trung bình X_tb của n lần đo độc lập: V(X_tb) = sigma^2/n, nên cận trên co lại như 1/n. Tần suất f cũng vậy, với V(f) = p(1 - p)/n.

$$ P\left(|X_{tb} - \mu| \ge \varepsilon\right) \le \frac{\sigma^2}{n\,\varepsilon^2} \to 0 $$

Ví dụ: sigma^2 = 9, n = 100, epsilon = 0.5.

1. V(X_tb) = 9/100.
2. Cận trên: (9/100)/0.25 = 9/25.
3. Muốn cận <= 0.05 với sigma^2 = 25, epsilon = 1: 25/n <= 0.05, n >= 500.

> Lỗi thường gặp: nghĩ luật số lớn "bù trừ". Sau 5 lần sấp, lần sau vẫn ngửa với xác suất 1/2; hiệu số ngửa trừ sấp cũng không về 0, chỉ tần suất về 1/2.

:::check
Q: sigma^2 = 9, epsilon = 1. Cần n nhỏ nhất bao nhiêu để Chebyshev bảo đảm P(|X_tb - mu| >= 1) <= 0.1?
A: 9/(n . 1) <= 0.1 cho n >= 90.
:::

## Định lý giới hạn trung tâm

:::hook
Mỗi khách chi tiền theo một kiểu lộn xộn, chẳng có hình chuông nào. Vậy mà tổng doanh thu của cả trăm khách lại theo đúng hình chuông.
:::

:::figure bars
caption: Số mặt ngửa trong 10 lần tung: mỗi lần chỉ là 0 hoặc 1, mà tổng đã có hình chuông.
size: 200 85
values: off
bar "0" 1
bar "1" 10
bar "2" 45
bar "3" 120
bar "4" 210
bar "5" 252 do
bar "6" 210
bar "7" 120
bar "8" 45
bar "9" 10
bar "10" 1
:::

:::core
Tổng của nhiều biến độc lập cùng phân phối, phân phối gì cũng được, xấp xỉ chuẩn N(n mu, n sigma^2). Cộng phương sai, không cộng độ lệch chuẩn.
:::

$$ \frac{S - n\mu}{\sigma\sqrt{n}} \approx N(0, 1) $$

Ví dụ: 100 khách, mỗi người chi kỳ vọng 5, độ lệch chuẩn 3. Tính P(S > 545), Phi(1.5) = 0.4332.

1. E(S) = 500, độ lệch chuẩn 3 . sqrt(100) = 30.
2. Chuẩn hóa: (545 - 500)/30 = 1.5.
3. P xấp xỉ 0.5 - 0.4332 = 0.0668.

> Lỗi thường gặp: cộng độ lệch chuẩn, ra 100 . 3 = 300 thay vì 30. Định lý cũng không đòi từng X_i có phân phối chuẩn.

:::check
Q: Tung đồng xu cân đối 100 lần, X là số ngửa. Dùng Phi(1) = 0.3413, tính xấp xỉ P(45 < X < 55).
A: X là tổng 100 biến 0-1: xấp xỉ N(50, 25), độ lệch chuẩn 5. Chuẩn hóa ra -1 và 1: P xấp xỉ 2 . 0.3413 = 0.6826.
:::

### Tìm ngưỡng từ xác suất

Bài ngược: cho trước xác suất, tìm mốc t. Vì S xấp xỉ chuẩn, P(S > t) = 0.025 nghĩa là t cách n mu đúng 1.96 độ lệch chuẩn của S (Phi(1.96) = 0.475); với 0.05 thì là 1.645.

Ví dụ: 100 khách như trên. Mốc t nào chỉ bị vượt với xác suất 0.025?

1. E(S) = 500, độ lệch chuẩn 30.
2. t = 500 + 1.96 . 30 = 558.8.

:::check
Q: Tổng S của 64 biến độc lập, mỗi biến kỳ vọng 10, độ lệch chuẩn 2. Tìm t với P(S > t) = 0.05.
A: E(S) = 640, độ lệch chuẩn 2 . 8 = 16. t = 640 + 1.645 . 16 = 666.32.
:::
