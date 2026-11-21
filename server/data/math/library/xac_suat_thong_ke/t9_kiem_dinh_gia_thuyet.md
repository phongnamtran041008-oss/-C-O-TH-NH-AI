---
id: xs_lib_t9
title_vi: Kiểm định giả thuyết thống kê
subject: xac_suat_thong_ke
floor: 9
format: 2
summary_vi: Đặt H0 là lời công bố, đo xem dữ liệu cách nó bao nhiêu sai số chuẩn, rồi bác bỏ khi kết quả rơi vào đuôi hiếm; cùng một cách làm cho trung bình, tỷ lệ và so sánh hai tổng thể.
skills: [xs_t9_gia_thuyet, xs_t9_kiem_dinh_trung_binh, xs_t9_kiem_dinh_ty_le, xs_t9_so_sanh_trung_binh, xs_t9_so_sanh_ty_le]
---
## Giả thuyết, mức ý nghĩa và hai loại sai lầm

:::hook
Bộ lọc coi mọi thư là thư thường (H0), chỉ đưa vào thư rác khi đủ bằng chứng. Lọc nhầm thư thật và bỏ lọt thư rác là hai cái sai khác nhau.
:::

:::figure plane
caption: Xanh: thống kê khi H0 đúng; tím: khi H1 đúng. Qua vạch thì bác bỏ H0. Đỏ là alpha (bác bỏ nhầm), vàng là beta (bỏ sót).
size: 200 80
axes: off
x: -3.5 6.5
y: 0 0.45
area "exp(-(x-3)^2/2)/sqrt(2*pi)" -0.5 1.645 vang
area "exp(-x^2/2)/sqrt(2*pi)" 1.645 4 do
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
curve "exp(-(x-3)^2/2)/sqrt(2*pi)" -0.5 6.5 tim
line 1.645 0 1.645 0.43 xam dash "vạch" pos=n
:::

:::core
Chỉ bác bỏ lời công bố H0 khi dữ liệu quá hiếm nếu H0 đúng. Bác bỏ nhầm: sai loại một (alpha); bỏ sót: sai loại hai (beta).
:::

- H0 luôn là đẳng thức (mu = 500). H1: mu khác 500 (hai phía), mu < 500 hay mu > 500 (một phía).
- alpha = P(bác bỏ | H0 đúng), beta = P(giữ H0 | H1 đúng), lực = 1 - beta.

Ví dụ: sigma = 6, n = 36, H0: mu = 20, H1: mu = 22.5; bác bỏ khi x_tb > 22. Dùng Phi(2) = 0.4772, Phi(0.5) = 0.1915.

1. Độ lệch chuẩn của x_tb: 6/6 = 1.
2. alpha = P(x_tb > 22 | mu = 20) = 0.5 - Phi(2) = 0.0228.
3. beta = P(x_tb <= 22 | mu = 22.5) = 0.5 - Phi(0.5) = 0.3085.

> Lỗi thường gặp: coi "không bác bỏ H0" là đã chứng minh H0 đúng. Có thể chỉ là beta lớn: dữ liệu chưa đủ.

:::check
Q: Bộ lọc thư: H0 "thư thường", bác bỏ thì chuyển vào thư rác. Sai lầm loại một và loại hai là gì?
A: Loại một: thư thường bị đưa vào thư rác (bác bỏ H0 khi H0 đúng). Loại hai: thư rác lọt vào hộp thư (không bác bỏ khi H0 sai).
:::

### Vạch bác bỏ và p-giá trị

Vạch đặt sao cho đuôi vượt vạch, tính khi H0 đúng, đúng bằng alpha. Hai phía thì chia alpha cho hai đuôi.

$$ |z| > z_{\alpha/2}, \qquad z > z_{\alpha} $$

- Mức 5%: 1.96 hai phía, 1.645 một phía. Mức 1%: 2.58 hai phía, 2.33 một phía.
- p-giá trị: xác suất, khi H0 đúng, được kết quả lệch ít nhất như đã thấy. Bác bỏ khi p < alpha.

Ví dụ: kiểm định hai phía cho z = -2, dùng Phi(2) = 0.4772.

1. p = 2(0.5 - Phi(2)) = 0.0456.
2. p < 0.05: bác bỏ ở mức 5%. p > 0.01: chưa bác bỏ ở mức 1%.

> Lỗi thường gặp: đọc p-giá trị là xác suất để H0 đúng, hay dùng 1.645 cho kiểm định hai phía.

:::check
Q: Thống kê z = 1.7, mức 5%. Bác bỏ H0 không, nếu H1 là hai phía? Nếu H1 là một phía phải?
A: Hai phía: 1.7 < 1.96, chưa bác bỏ. Một phía phải: 1.7 > 1.645, bác bỏ.
:::

## Kiểm định trung bình một tổng thể

:::hook
Gói linh trà ghi 500 g. Cân 36 gói được trung bình 497 g. Thiếu 3 g là do may rủi khi lấy mẫu, hay nhà sản xuất đóng thiếu thật?
:::

:::figure plane
caption: H1: mu < mu_0, mức 5%: vùng bác bỏ là đuôi trái z < -1.645. z = -2 rơi vào đó.
size: 190 85
x: -3.5 3.5 1
y: 0 0.45
names: z f
area "exp(-x^2/2)/sqrt(2*pi)" -3.5 -1.645 do
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
point -2 0 do "z = -2" pos=n
:::

:::core
Thống kê đếm xem x_tb cách mu_0 bao nhiêu sai số chuẩn. Rơi vào vùng đuôi hiếm thì bác bỏ H0.
:::

$$ z = \frac{x_{tb} - \mu_0}{\sigma/\sqrt{n}}, \qquad t = \frac{x_{tb} - \mu_0}{s/\sqrt{n}} $$

Biết sigma dùng z. Chưa biết sigma, tổng thể chuẩn: dùng t với n - 1 bậc tự do. Kiểm định hai phía mức alpha bác bỏ đúng khi mu_0 nằm ngoài khoảng tin cậy 1 - alpha.

Ví dụ: sigma = 8, n = 64, x_tb = 52. H0: mu = 50, H1: mu khác 50, mức 5%.

1. Sai số chuẩn: 8/sqrt(64) = 1.
2. z = (52 - 50)/1 = 2.
3. |z| = 2 > 1.96: bác bỏ H0.

> Lỗi thường gặp: chia cho sigma thay vì sigma/sqrt(n). Ở ví dụ sẽ ra z = 2/8 = 0.25 và bỏ sót hẳn chênh lệch.

:::check
Q: n = 16, x_tb = 52, s = 8, phân phối chuẩn. Kiểm định H0: mu = 48 hai phía mức 5%, t(15; 0.025) = 2.131.
A: t = (52 - 48)/(8/4) = 2 < 2.131: chưa đủ cơ sở bác bỏ H0.
:::

## Kiểm định tỷ lệ một tổng thể

:::hook
Năm trước 10% người dùng bỏ ứng dụng. Năm nay trong 400 người có 52 người bỏ. Tỷ lệ bỏ đã tăng thật, hay chỉ do may rủi?
:::

:::figure plane
caption: p-giá trị là diện tích đuôi từ z quan sát trở ra, tính khi H0 đúng. z = 2: đuôi phải là 0.0228.
size: 190 85
x: -3.5 3.5 1
y: 0 0.45
names: z f
area "exp(-x^2/2)/sqrt(2*pi)" 2 3.5 do
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
point 2 0 do "z = 2" pos=n
:::

:::core
Sai số chuẩn tính theo p0 của H0, không theo f: câu hỏi là "nếu lời công bố đúng, tần suất này hiếm đến đâu?".
:::

$$ z = \frac{f - p_0}{\sqrt{p_0(1 - p_0)/n}} $$

Ví dụ: H0: p = 0.1, H1: p > 0.1, n = 400, có 52 người bỏ, mức 5%.

1. f = 52/400 = 0.13.
2. Theo H0: sqrt(0.1 . 0.9/400) = 0.3/20 = 0.015.
3. z = 0.03/0.015 = 2 > 1.645: bác bỏ H0. p-giá trị = 0.5 - Phi(2) = 0.0228.

> Lỗi thường gặp: z nhỏ hơn vạch thì kết luận "đúng là 10%". Chỉ được nói: chưa có bằng chứng tỷ lệ đã đổi.

:::check
Q: Tung đồng xu 400 lần được 220 ngửa. Kiểm định đồng xu cân đối, hai phía: bác bỏ ở mức 5% không? Ở mức 1%?
A: f = 0.55, sai số chuẩn 0.5/20 = 0.025, z = 2. Mức 5%: 2 > 1.96, bác bỏ. Mức 1%: 2 < 2.58, chưa bác bỏ.
:::

## So sánh hai trung bình

:::hook
Kiểm thử A/B: phiên bản mới có thời gian dùng trung bình cao hơn bản cũ 11 giây. Chênh lệch đó là thật, hay chỉ là dao động của hai mẫu?
:::

:::figure plane
caption: Sai số chuẩn của hiệu cộng như hai cạnh góc vuông: sqrt(3^2 + 4^2) = 5, không phải 3 + 4.
size: 130 90
axes: off
x: -0.5 4.8
y: -0.7 3.5
poly 0 0 4 0 4 3 xanh
text 2 -0.4 "4"
text 4.4 1.5 "3"
text 1.6 1.9 "5"
:::

:::core
Hai mẫu độc lập: phương sai của hiệu là tổng hai phương sai. Rồi đo hiệu hai trung bình bằng sai số chuẩn đó.
:::

$$ z = \frac{x_{tb1} - x_{tb2}}{\sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2}} $$

Mẫu lớn thì thay sigma bằng s.

Ví dụ: sigma_1 = 12, n_1 = 16; sigma_2 = 8, n_2 = 4; hiệu trung bình 11; hai phía, mức 5%.

1. Phương sai của hiệu: 144/16 + 64/4 = 25, sai số chuẩn 5.
2. z = 11/5 = 2.2 > 1.96: bác bỏ H0.

> Lỗi thường gặp: cộng độ lệch chuẩn 3 + 4 = 7 thay vì cộng phương sai rồi lấy căn.

:::check
Q: Hai mẫu lớn có trung bình chênh 3, sai số chuẩn của hiệu là 2. Kiểm định H1: mu_1 > mu_2 mức 5% có bác bỏ H0 không?
A: z = 3/2 = 1.5 < 1.645: chưa đủ cơ sở. Hai trung bình mẫu khác nhau chưa đủ để kết luận.
:::

### Mẫu nhỏ: gộp phương sai

Hai tổng thể chuẩn, cùng phương sai chưa biết, mẫu nhỏ: gộp hai phương sai mẫu thành một s^2, có trọng số là bậc tự do n_i - 1, rồi dùng Student n_1 + n_2 - 2 bậc tự do.

$$ s^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}, \qquad t = \frac{x_{tb1} - x_{tb2}}{\sqrt{s^2(1/n_1 + 1/n_2)}} $$

Ví dụ: n_1 = n_2 = 9, s_1^2 = 20, s_2^2 = 16, hiệu trung bình 5, hai phía mức 5%, t(16; 0.025) = 2.120.

1. s^2 = (8 . 20 + 8 . 16)/16 = 18.
2. Sai số chuẩn: sqrt(18 . 2/9) = 2.
3. t = 5/2 = 2.5 > 2.120: bác bỏ H0.

> Lỗi thường gặp: lấy trung bình cộng hai phương sai khi hai mẫu khác cỡ, hay dùng n_1 + n_2 bậc tự do.

:::check
Q: n_1 = 4, s_1^2 = 12; n_2 = 6, s_2^2 = 6. Tính s^2 gộp và số bậc tự do.
A: s^2 = (3 . 12 + 5 . 6)/8 = 66/8 = 33/4; 4 + 6 - 2 = 8 bậc tự do.
:::

## So sánh hai tỷ lệ

:::hook
Thử hai dòng tiêu đề email: dòng A được mở 34 lần trên 100, dòng B 66 lần trên 300. Dòng A có thật sự tốt hơn không?
:::

:::figure grid
caption: Khi H0 đúng hai mẫu chung một tỷ lệ: gộp số đếm, 100/400 = 0.25, không lấy trung bình 0.28 của hai tần suất.
table
head "có" "n" "f"
side "mẫu 1" "mẫu 2" "gộp"
row 34 100 0.34
row 66 300 0.22
row 100 400 0.25
mark row 3 vang
:::

:::core
Dưới H0, hai tổng thể chung một tỷ lệ: ước lượng nó bằng cách gộp số đếm cả hai mẫu, rồi đo f_1 - f_2 bằng sai số chuẩn tính từ đó.
:::

$$ f = \frac{m_1 + m_2}{n_1 + n_2}, \qquad z = \frac{f_1 - f_2}{\sqrt{f(1-f)(1/n_1 + 1/n_2)}} $$

Ví dụ: số liệu trong bảng, hai phía, mức 5%.

1. Tần suất chung f = 0.25.
2. Sai số chuẩn: sqrt(0.25 . 0.75 . (1/100 + 1/300)) = sqrt(0.0025) = 0.05.
3. z = (0.34 - 0.22)/0.05 = 2.4 > 1.96: bác bỏ H0.

> Lỗi thường gặp: lấy trung bình cộng hai tần suất khi hai mẫu khác cỡ.

:::check
Q: Mẫu 1: 110 trên 200; mẫu 2: 90 trên 200. Tính tần suất chung và z. Bác bỏ H0: p_1 = p_2 ở mức 5% hai phía không?
A: f = 200/400 = 0.5; sai số chuẩn sqrt(0.25 . 0.01) = 0.05; z = 0.1/0.05 = 2 > 1.96: bác bỏ.
:::
