---
id: xs_lib_t8
title_vi: Khoảng tin cậy, luật số lớn và định lý giới hạn trung tâm
subject: xac_suat_thong_ke
floor: 8
summary_vi: Khoảng tin cậy đi kèm ước lượng một độ chính xác; cỡ mẫu được chọn để độ chính xác đó đủ nhỏ. Luật số lớn giải thích vì sao trung bình của nhiều lần thử tiến gần kỳ vọng, còn định lý giới hạn trung tâm cho phép coi tổng của nhiều biến độc lập là gần chuẩn.
skills: [xs_t8_tin_cay_trung_binh, xs_t8_tin_cay_ty_le, xs_t8_co_mau, xs_t8_luat_so_lon, xs_t8_gioi_han_trung_tam]
---
## Khoảng tin cậy cho trung bình

Khoảng tin cậy đối xứng cho kỳ vọng mu có dạng (x_tb - epsilon; x_tb + epsilon). Khi biết sigma (tổng thể chuẩn, hoặc mẫu lớn):

$$ \varepsilon = z\,\frac{\sigma}{\sqrt{n}}, \qquad 2\,\Phi(z) = 1 - \alpha $$

Độ tin cậy 95% dùng z = 1.96 (Phi(1.96) = 0.475), 90% dùng z = 1.645, 99% dùng z = 2.58.

Ví dụ sigma = 10, n = 25, x_tb = 48, độ tin cậy 95%:

1. sigma/sqrt(n) = 10/5 = 2.
2. epsilon = 1.96 . 2 = 3.92.
3. Khoảng tin cậy (44.08; 51.92).

Khi chưa biết sigma và tổng thể chuẩn, thay sigma bằng s và z bằng giá trị tới hạn Student với n - 1 bậc tự do; t(k; a) là số mà P(T > t(k; a)) = a:

$$ \varepsilon = t(n-1;\, \alpha/2)\,\frac{s}{\sqrt{n}} $$

Ví dụ n = 9, x_tb = 20, s = 3, độ tin cậy 95%: t(8; 0.025) = 2.306, epsilon = 2.306, khoảng (17.694; 22.306).

Ý nghĩa: nếu lấy mẫu lặp lại rất nhiều lần, khoảng 95% các khoảng lập được sẽ chứa mu.

> Lỗi thường gặp: đọc khoảng tin cậy 95% là "95% số liệu nằm trong khoảng"; dùng giá trị tới hạn một phía t(15; 0.05) cho khoảng hai phía (phải là t(15; 0.025)); hay dùng 16 bậc tự do cho mẫu cỡ 16 (phải là 15).

## Khoảng tin cậy cho tỷ lệ

m lần có tính chất trong n phép thử cho tần suất f = m/n, với E(f) = p và V(f) = p(1 - p)/n. Khi n lớn (nf và n(1 - f) đều lớn), dùng xấp xỉ chuẩn:

$$ \varepsilon = z\,\sqrt{\frac{f(1-f)}{n}} $$

Ví dụ 80 trong 400 người, độ tin cậy 95%:

1. f = 0.2.
2. sqrt(0.2 . 0.8/400) = 0.02.
3. epsilon = 1.96 . 0.02 = 0.0392; khoảng (0.1608; 0.2392).

> Lỗi thường gặp: để n ra ngoài căn. Với 36 hạt nảy mầm trong 100 hạt, sai số chuẩn là sqrt(0.36 . 0.64/100) = 0.048, không phải sqrt(0.36 . 0.64)/100 = 0.0048.

## Chọn cỡ mẫu theo độ chính xác

Muốn sai số không vượt epsilon_0 thì giải bất phương trình theo n rồi làm tròn lên:

$$ n \ge \left(\frac{z\,\sigma}{\varepsilon_0}\right)^2, \qquad n \ge \frac{z^2\, p(1-p)}{\varepsilon_0^2} $$

Ví dụ sigma = 15, epsilon_0 = 3, độ tin cậy 95%: n >= (1.96 . 5)^2 = 96.04, nên n = 97. Với tỷ lệ chưa biết gì, dùng p(1 - p) <= 1/4: sai số 0.05 cần n >= 384.16, tức n = 385.

Sai số tỉ lệ với 1/sqrt(n): muốn sai số giảm một nửa phải tăng cỡ mẫu gấp 4.

> Lỗi thường gặp: làm tròn xuống (n >= 61.4656 cho n = 62, không phải 61), hoặc lẫn độ dài khoảng với epsilon: độ dài khoảng không vượt 4 nghĩa là epsilon <= 2.

## Luật số lớn

Bất đẳng thức Chebyshev đúng cho mọi biến có phương sai hữu hạn:

$$ P\left(|Y - E(Y)| \ge \varepsilon\right) \le \frac{V(Y)}{\varepsilon^2} $$

Áp dụng cho Y = X_tb của n biến độc lập cùng phân phối (kỳ vọng mu, phương sai sigma^2):

$$ P\left(|X_{tb} - \mu| \ge \varepsilon\right) \le \frac{\sigma^2}{n\,\varepsilon^2} \to 0 $$

Đó là luật số lớn: trung bình của nhiều lần thử tiến gần kỳ vọng; riêng với tần suất, f tiến gần xác suất p. Ví dụ n = 100, sigma^2 = 4, epsilon = 0.5: cận trên là 0.04/0.25 = 4/25.

> Lỗi thường gặp: quên bình phương epsilon (với V(X) = 16, P(|X - 20| < 8) >= 1 - 16/64 = 3/4), và nghĩ luật số lớn "bù trừ": sau năm lần sấp, lần sau vẫn ra ngửa với xác suất 1/2; tần suất tiến về 1/2 nhưng hiệu số lần ngửa trừ số lần sấp thì không tiến về 0.

## Định lý giới hạn trung tâm

X_1, ..., X_n độc lập, cùng phân phối (bất kỳ), kỳ vọng mu, phương sai sigma^2. Khi n lớn, tổng S = X_1 + ... + X_n xấp xỉ chuẩn:

$$ \frac{S - n\mu}{\sigma\sqrt{n}} \approx N(0, 1) $$

Ví dụ 36 đệ tử, mỗi người nặng trung bình 60 với độ lệch chuẩn 12:

1. E(S) = 2160, độ lệch chuẩn của S = 12 . 6 = 72.
2. Chuẩn hóa mốc 2304: (2304 - 2160)/72 = 2.
3. P(S > 2304) xấp xỉ 0.5 - Phi(2) = 0.0228.

Số lần thành công của nhị thức B(n, p) là một tổng như vậy: B(400, 1/2) xấp xỉ N(200, 100).

> Lỗi thường gặp: cộng độ lệch chuẩn thay vì cộng phương sai. 64 bao, mỗi bao có độ lệch chuẩn 0.8, cho tổng có độ lệch chuẩn 0.8 . sqrt(64) = 6.4, không phải 64 . 0.8 = 51.2. Định lý cũng không đòi các X_i có phân phối chuẩn.
