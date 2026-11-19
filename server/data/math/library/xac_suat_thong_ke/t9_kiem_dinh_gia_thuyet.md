---
id: xs_lib_t9
title_vi: Kiểm định giả thuyết thống kê
subject: xac_suat_thong_ke
floor: 9
summary_vi: Một kiểm định giả thuyết đặt H0 và đối thuyết H1, tính một thống kê từ mẫu, so với giá trị tới hạn của mức ý nghĩa rồi kết luận bác bỏ H0 hay chưa đủ cơ sở; cùng một cách làm dùng cho trung bình, tỷ lệ và cho việc so sánh hai tổng thể.
skills: [xs_t9_gia_thuyet, xs_t9_kiem_dinh_trung_binh, xs_t9_kiem_dinh_ty_le, xs_t9_so_sanh_trung_binh, xs_t9_so_sanh_ty_le]
---
## Giả thuyết, mức ý nghĩa và hai loại sai lầm

H0 là giả thuyết được công bố, luôn là một đẳng thức (mu = 500, p = 0.05); đối thuyết H1 là điều người kiểm định muốn tìm bằng chứng: mu != 500 (hai phía), mu < 500 hay mu > 500 (một phía).

- Sai lầm loại một: bác bỏ H0 khi H0 đúng. Xác suất của nó là mức ý nghĩa alpha.
- Sai lầm loại hai: không bác bỏ H0 khi H0 sai, xác suất beta; 1 - beta là lực của kiểm định.

Miền bác bỏ với thống kê z, trong đó z_a là số có Phi(z_a) = 0.5 - a (Phi là hàm Laplace): đối thuyết hai phía thì bác bỏ khi |z| > z_(alpha/2); một phía phải thì khi z > z_alpha (phía trái: z < -z_alpha).

$$ |z| > z_{\alpha/2}, \qquad z > z_{\alpha} $$

Ở mức 5%: hai phía 1.96, một phía 1.645; ở mức 1%: hai phía 2.58, một phía 2.33.

p-giá trị là xác suất, khi H0 đúng, được một thống kê lệch về phía H1 ít nhất như giá trị quan sát; bác bỏ H0 khi p-giá trị nhỏ hơn alpha. Ví dụ hai phía với z = -2: p = 2(0.5 - Phi(2)) = 0.0456, bác bỏ ở mức 5% nhưng không ở mức 1%.

> Lỗi thường gặp: coi "không bác bỏ H0" là đã chứng minh H0 đúng; đọc p-giá trị là xác suất để H0 đúng; dùng giá trị tới hạn một phía 1.645 cho một kiểm định hai phía.

## Kiểm định trung bình một tổng thể

Biết sigma (tổng thể chuẩn hoặc mẫu lớn), dùng z; chưa biết sigma với tổng thể chuẩn, dùng t có n - 1 bậc tự do:

$$ z = \frac{x_{tb} - \mu_0}{\sigma/\sqrt{n}}, \qquad t = \frac{x_{tb} - \mu_0}{s/\sqrt{n}} $$

Ví dụ: gói linh trà ghi 500 g, sigma = 9, cân 36 gói được x_tb = 497, nghi bị đóng thiếu, mức 5%:

1. H0: mu = 500, H1: mu < 500.
2. sigma/sqrt(n) = 9/6 = 1.5.
3. z = (497 - 500)/1.5 = -2.
4. Miền bác bỏ phía trái z < -1.645: -2 rơi vào đó, bác bỏ H0.

Kiểm định hai phía mức alpha bác bỏ H0: mu = mu_0 đúng khi mu_0 nằm ngoài khoảng tin cậy 1 - alpha.

> Lỗi thường gặp: chia cho sigma thay vì sigma/sqrt(n). Với sigma = 6, n = 36, x_tb = 22, mu_0 = 20: z = 2/1 = 2 (bác bỏ), không phải 2/6 = 1/3.

## Kiểm định tỷ lệ một tổng thể

Với n lớn, khi H0: p = p0 đúng thì tần suất f có độ lệch chuẩn sqrt(p0(1 - p0)/n):

$$ z = \frac{f - p_0}{\sqrt{p_0(1 - p_0)/n}} $$

Ví dụ xưởng công bố 20% phế phẩm, kiểm 400 món có 100 phế phẩm: f = 0.25, sqrt(0.2 . 0.8/400) = 0.02, z = 2.5 > 1.645, bác bỏ H0 với H1: p > 0.2.

Độ lệch chuẩn trong thống kê tính theo p0 của H0 (khác với khoảng tin cậy, nơi dùng f).

> Lỗi thường gặp: kết luận "đồng xu đúng là cân đối" khi 58 lần ngửa trong 100 lần cho z = 1.6 < 1.96. Kết luận đúng chỉ là: chưa có bằng chứng đồng xu lệch.

## So sánh hai trung bình

Hai mẫu độc lập: phương sai của hiệu hai trung bình mẫu là tổng hai phương sai.

$$ z = \frac{x_{tb1} - x_{tb2}}{\sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2}} $$

Với mẫu lớn thay sigma_1, sigma_2 bằng s_1, s_2. Với mẫu nhỏ từ hai tổng thể chuẩn cùng phương sai, gộp hai phương sai và dùng Student n_1 + n_2 - 2 bậc tự do:

$$ s^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}, \qquad t = \frac{x_{tb1} - x_{tb2}}{\sqrt{s^2(1/n_1 + 1/n_2)}} $$

Ví dụ n_1 = n_2 = 8, s_1^2 = 10, s_2^2 = 22, hiệu trung bình 5: s^2 = 16, sai số chuẩn sqrt(16 . 1/4) = 2, t = 2.5 > t(14; 0.025) = 2.145, bác bỏ H0.

> Lỗi thường gặp: cộng độ lệch chuẩn. Với độ lệch chuẩn của từng trung bình là 3 và 4, độ lệch chuẩn của hiệu là sqrt(9 + 16) = 5, không phải 7.

## So sánh hai tỷ lệ

Khi H0: p_1 = p_2 đúng, hai mẫu có chung một tỷ lệ, ước lượng bằng tần suất chung (gộp số đếm):

$$ f = \frac{m_1 + m_2}{n_1 + n_2}, \qquad z = \frac{f_1 - f_2}{\sqrt{f(1-f)(1/n_1 + 1/n_2)}} $$

Ví dụ 60 trong 200 và 90 trong 400:

1. f_1 = 0.3, f_2 = 0.225.
2. f = 150/600 = 0.25.
3. Sai số chuẩn sqrt(0.25 . 0.75 . (1/200 + 1/400)) = 0.0375.
4. z = 0.075/0.0375 = 2 > 1.645: bác bỏ H0 với H1: p_1 > p_2.

> Lỗi thường gặp: lấy trung bình cộng hai tần suất làm tần suất chung khi hai mẫu khác cỡ. 50/100 và 70/200 cho f = 120/300 = 0.4, không phải (0.5 + 0.35)/2 = 0.425.
