---
id: xs_lib_t6
title_vi: Các số đặc trưng và các phân phối thông dụng
subject: xac_suat_thong_ke
floor: 6
summary_vi: Kỳ vọng cho biết giá trị trung bình của một biến ngẫu nhiên, phương sai cho biết nó phân tán quanh trung bình bao xa; năm phân phối hay gặp (nhị thức, Poisson, đều, mũ, chuẩn) có sẵn công thức cho cả hai con số này.
skills: [xs_t6_ky_vong, xs_t6_phuong_sai, xs_t6_nhi_thuc_poisson, xs_t6_deu_mu, xs_t6_chuan]
---
## Kỳ vọng

Kỳ vọng E(X) là trung bình có trọng số của các giá trị, trọng số là xác suất (với biến liên tục, trọng số là mật độ):

$$ E(X) = \sum_i x_i\,p_i, \qquad E(X) = \int_{-\infty}^{+\infty} x f(x)\,dx $$

Ví dụ X nhận -1, 0, 2 với xác suất 1/5, 1/2, 3/10: E(X) = -1/5 + 0 + 6/10 = 2/5. Với mật độ f(x) = 2x trên [0, 1]: E(X) = tích phân của 2x^2 từ 0 đến 1 = 2/3.

Hai tính chất dùng nhiều nhất:

$$ E(aX + b) = a\,E(X) + b, \qquad E(X + Y) = E(X) + E(Y) $$

Tính chất thứ hai không cần X, Y độc lập: tổng số chấm của 10 xúc xắc có kỳ vọng 10 . 7/2 = 35.

Một trò chơi trả 2 linh thạch, ra mặt 6 nhận 9, ra mặt 5 nhận 3: số nhận có kỳ vọng 12/6 = 2, nên tiền lãi có kỳ vọng 0, trò chơi công bằng.

Với hàm g bất kỳ, tính theo bảng: E(g(X)) = tổng của g(x_i) p_i.

> Lỗi thường gặp: cho kỳ vọng đi qua mọi hàm. X nhận 1 và 2 cùng xác suất 1/2 thì E(1/X) = 1/2 + 1/4 = 3/4, không phải 1/E(X) = 2/3. Chỉ hàm bậc nhất aX + b mới làm vậy được.

## Phương sai và độ lệch chuẩn

Phương sai đo độ phân tán quanh kỳ vọng; công thức tính nhanh:

$$ V(X) = E(X^2) - \left(E(X)\right)^2, \qquad \sigma(X) = \sqrt{V(X)} $$

Ví dụ X nhận 0, 1, 2 với xác suất 1/4, 1/2, 1/4:

1. E(X) = 1/2 + 2/4 = 1.
2. E(X^2) = 1/2 + 4/4 = 3/2.
3. V(X) = 3/2 - 1 = 1/2.

Khi đổi biến bậc nhất, hằng số cộng thêm không làm đổi độ phân tán, hệ số nhân được bình phương:

$$ V(aX + b) = a^2\,V(X) $$

Nếu V(X) = 9 thì V(-2X + 5) = 36 và độ lệch chuẩn là 6 (độ lệch chuẩn không bao giờ âm). Với X, Y độc lập: V(2X - Y + 4) = 4V(X) + V(Y).

> Lỗi thường gặp: viết E(X^2) = (E(X))^2, hay V(aX + b) = aV(X) + b, hay cộng phương sai của hai biến phụ thuộc. X nhận -1, 1 thì E(X) = 0 nhưng E(X^2) = 1; với Y = X thì V(X + Y) = V(2X) = 4V(X), không phải 2V(X).

## Phân phối nhị thức và Poisson

Nhị thức B(n, p): số lần thành công trong n phép thử Bernoulli độc lập, xác suất thành công p.

$$ P(X = k) = C_n^k p^k (1-p)^{n-k}, \quad E(X) = np, \quad V(X) = np(1-p) $$

Ví dụ X ~ B(10, 1/5): E(X) = 2, V(X) = 10 . 1/5 . 4/5 = 8/5.

Poisson tham số lambda > 0: số lần một sự kiện hiếm xảy ra trong một khoảng thời gian hay không gian, khi trung bình là lambda (số cuộc gọi trong một phút, số lỗi in trên một trang).

$$ P(X = k) = e^{-\lambda} \frac{\lambda^k}{k!}, \quad E(X) = V(X) = \lambda $$

Ví dụ lambda = 2 và e^(-2) = 0.1353: P(X = 2) = 2 e^(-2) = 0.2706. Tỉ số hai xác suất liền nhau gọn: P(X = k)/P(X = k - 1) = lambda/k.

Khi n lớn và p nhỏ, B(n, p) xấp xỉ Poisson với lambda = np: 1000 sản phẩm, mỗi sản phẩm hỏng với xác suất 1/500, số hỏng xấp xỉ Poisson với lambda = 2.

> Lỗi thường gặp: lẫn tham số. Phương sai bằng kỳ vọng là của Poisson; nhị thức B(20, 1/4) có E = 5 nhưng V = 15/4. Tham số Poisson xấp xỉ là np, không phải n hay 1/p.

## Phân phối đều và phân phối mũ

Đều trên [a, b]: mật độ bằng 1/(b - a) trên đoạn, xác suất tỉ lệ với độ dài khoảng.

$$ E(X) = \frac{a+b}{2}, \qquad V(X) = \frac{(b-a)^2}{12} $$

Ví dụ X đều trên [2, 10]: P(3 < X < 7) = 4/8 = 1/2. X đều trên [1, 4]: E(X^2) = (64 - 1)/9 = 7.

Mũ tham số lambda > 0: mật độ lambda e^(-lambda x) khi x > 0, dùng cho thời gian chờ.

$$ P(X > x) = e^{-\lambda x}, \quad E(X) = \frac{1}{\lambda}, \quad V(X) = \frac{1}{\lambda^2} $$

Ví dụ thời gian chờ trung bình 5 phút thì lambda = 1/5, và P(X > 10) = e^(-2). Phân phối mũ không nhớ: đã chờ s phút thì xác suất phải chờ thêm hơn t phút vẫn là e^(-lambda t).

> Lỗi thường gặp: quên bình phương trong phương sai của phân phối đều. X đều trên [2, 8] có V(X) = 36/12 = 3, không phải 6/12 = 1/2.

## Phân phối chuẩn

X ~ N(mu, sigma^2) có kỳ vọng mu và phương sai sigma^2 (độ lệch chuẩn sigma). Chuẩn hóa đưa mọi phân phối chuẩn về N(0, 1):

$$ Z = \frac{X - \mu}{\sigma} \sim N(0, 1) $$

Xác suất tính bằng hàm Laplace Phi(x), tích phân của mật độ N(0, 1) từ 0 đến x, tra bảng. Phi là hàm lẻ: Phi(-x) = -Phi(x), và nửa trục có xác suất 0.5.

$$ P(a < X < b) = \Phi\left(\frac{b - \mu}{\sigma}\right) - \Phi\left(\frac{a - \mu}{\sigma}\right) $$

Ví dụ X ~ N(10, 4), với Phi(1) = 0.3413:

1. sigma = 2; chuẩn hóa 8 và 12 thành -1 và 1.
2. P(8 < X < 12) = Phi(1) - Phi(-1) = 2 . 0.3413 = 0.6826.

Một phía: P(X > a) = 0.5 - Phi((a - mu)/sigma). Với X ~ N(5, 4) và Phi(2) = 0.4772: P(X > 9) = 0.0228.

Vài giá trị hay dùng: Phi(1) = 0.3413, Phi(1.5) = 0.4332, Phi(1.96) = 0.475, Phi(2) = 0.4772.

> Lỗi thường gặp: chia cho phương sai thay vì độ lệch chuẩn. Với N(20, 9), chuẩn hóa là (X - 20)/3, không phải (X - 20)/9.
