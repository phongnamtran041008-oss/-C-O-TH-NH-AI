---
id: xs_lib_t6
title_vi: Các số đặc trưng và các phân phối thông dụng
subject: xac_suat_thong_ke
floor: 6
format: 2
summary_vi: Kỳ vọng là điểm cân bằng, phương sai là độ tản ra; năm phân phối hay gặp (nhị thức, Poisson, đều, mũ, chuẩn) có sẵn hai con số đó, và mọi hình chuông quy về N(0, 1).
skills: [xs_t6_ky_vong, xs_t6_phuong_sai, xs_t6_nhi_thuc_poisson, xs_t6_deu_mu, xs_t6_chuan]
---
## Kỳ vọng

:::hook
Trò chơi linh thạch có đáng chơi? Chơi thật nhiều lần, trung bình mỗi lần được bao nhiêu: đó là kỳ vọng. Máy học cũng tối thiểu hóa kỳ vọng sai số.
:::

:::figure bars
caption: Xác suất 2/5, 1/5, 1/5, 1/5 tại 0, 1, 2, 3: thanh thăng bằng tại E(X) = 6/5.
size: 190 80
bar "0" 2/5
bar "1" 1/5
bar "2" 1/5
bar "3" 1/5
mark 1.2 do "E(X)"
:::

:::core
Kỳ vọng là trung bình sau rất nhiều lần thử: mỗi giá trị nhân xác suất của nó rồi cộng lại, là điểm cân bằng của phân phối.
:::

$$ E(X) = \sum_i x_i\,p_i, \qquad E(X) = \int_{-\infty}^{+\infty} x f(x)\,dx $$

E(aX + b) = aE(X) + b, và E(X + Y) = E(X) + E(Y) kể cả khi không độc lập: 4 xúc xắc có tổng trung bình 4 . 7/2 = 14. Hàm khác thì tính theo bảng: E(g(X)) = tổng g(x_i) p_i. Mật độ 3x^2 trên [0, 1]: E(X) = tích phân của 3x^3 = 3/4.

Ví dụ: trả 2 linh thạch, gieo xúc xắc; mặt 6 nhận 6, mặt 1 nhận 3, mặt khác không có gì.

1. E(nhận) = 6 . 1/6 + 3 . 1/6 = 3/2.
2. E(lãi) = 3/2 - 2 = -1/2: chơi lâu, mỗi lần mất trung bình nửa viên.

> Lỗi thường gặp: cho kỳ vọng đi qua mọi hàm. X là 1 hoặc 2 (mỗi số 1/2) thì E(1/X) = 3/4, không phải 1/E(X) = 2/3.

:::check
Q: E(X) = 3. Tính E(2X - 5). X nhận 1, 2, 4 với xác suất 1/2, 1/4, 1/4: tính E(X^2).
A: E(2X - 5) = 2 . 3 - 5 = 1. E(X^2) = 1/2 + 4/4 + 16/4 = 11/2.
:::

## Phương sai và độ lệch chuẩn

:::hook
Hai cung thủ cùng trung bình 8 điểm: một người luôn bắn 7 đến 9, người kia lúc 4 lúc 12. Kỳ vọng không phân biệt được hai người; phương sai thì có.
:::

:::figure plane
caption: Cùng tâm 8. A tản trong [7, 9]: V = 1/2. B tản trong [4, 12]: V = 8.
size: 200 70
axes: off
x: 2.5 13.5
y: -0.6 1.6
line 8 -0.6 8 1.6 do dash "E = 8" pos=n
segment 7 1 9 1 xanh
segment 4 0 12 0 tim
point 7 1 xanh
point 8 1 xanh
point 9 1 xanh
point 4 0 tim "4" pos=s
point 8 0 tim
point 12 0 tim "12" pos=s
text 3 1 "A"
text 3 0 "B"
:::

:::core
Phương sai là trung bình bình phương khoảng cách tới kỳ vọng: độ tản ra. Độ lệch chuẩn là căn của nó, cùng đơn vị với X.
:::

$$ V(X) = E(X^2) - \left(E(X)\right)^2, \qquad \sigma(X) = \sqrt{V(X)} $$

V(aX + b) = a^2 V(X): cộng hằng số không đổi độ tản, hệ số nhân thì bình phương. X, Y độc lập thì V(aX + bY) = a^2 V(X) + b^2 V(Y), dấu trừ vẫn thành cộng; Y = X thì không được cộng.

Ví dụ: X nhận 0, 1, 3 với xác suất 1/2, 1/4, 1/4. Tính V(X).

1. E(X) = 1/4 + 3/4 = 1.
2. E(X^2) = 1/4 + 9/4 = 5/2.
3. V(X) = 5/2 - 1^2 = 3/2.

> Lỗi thường gặp: viết E(X^2) = (E(X))^2, hay V(3X + 1) = 3V(X) + 1. Đúng là 9V(X).

:::check
Q: V(X) = 5. Tính V(-3X + 2) và độ lệch chuẩn của -3X + 2. Biết E(X) = 2, tính E(X^2).
A: V = 9 . 5 = 45, độ lệch chuẩn sqrt(45) = 3 sqrt(5) (không âm). E(X^2) = V(X) + (E(X))^2 = 5 + 4 = 9.
:::

## Phân phối nhị thức và Poisson

:::hook
Trang đăng ký nhận trung bình 2 lượt mỗi phút. Phút tới có bao nhiêu lượt? Không đoán được con số, nhưng biết cả phân phối của nó: Poisson.
:::

:::figure bars
caption: Poisson lambda = 2, giá trị 0 đến 5: đỉnh ở 1 và 2; E = V = 2.
size: 190 80
bar "0" 0.135
bar "1" 0.271
bar "2" 0.271
bar "3" 0.180
bar "4" 0.090
bar "5" 0.036
mark 2 do "E = 2"
:::

:::core
Nhị thức đếm số lần thành công trong n lần thử độc lập. Poisson đếm sự kiện hiếm trong một khoảng, khi biết số trung bình lambda.
:::

$$ P(X = k) = C_n^k p^k (1-p)^{n-k}, \quad E(X) = np, \quad V(X) = np(1-p) $$

$$ P(X = k) = e^{-\lambda} \frac{\lambda^k}{k!}, \quad E(X) = V(X) = \lambda $$

Tỉ số hai cột liền nhau của Poisson gọn: P(X = k)/P(X = k - 1) = lambda/k. Khi n lớn, p nhỏ: B(n, p) xấp xỉ Poisson với lambda = np.

Ví dụ: 2000 sản phẩm, mỗi cái hỏng với xác suất 1/1000. Dùng e^(-2) = 0.1353.

1. X ~ B(2000, 1/1000) xấp xỉ Poisson với lambda = np = 2.
2. P(X = 0) = e^(-2) = 0.1353, P(X = 1) = 0.1353 . 2/1 = 0.2706.

> Lỗi thường gặp: cho nhị thức phương sai bằng kỳ vọng. B(12, 1/4) có E = 3 nhưng V = 9/4; "V = E" là của Poisson.

:::check
Q: X ~ B(12, 1/4): tính E(X), V(X). Y ~ Poisson với lambda = 4: tính P(Y = 5)/P(Y = 4).
A: E = 3, V = 12 . 1/4 . 3/4 = 9/4. Tỉ số = lambda/5 = 4/5.
:::

## Phân phối đều và phân phối mũ

:::hook
Một điểm rơi ngẫu nhiên trên đoạn: phân phối đều. Thời gian chờ đến yêu cầu kế tiếp của máy chủ: phân phối mũ.
:::

:::figure plane
caption: Thời gian chờ có phân phối mũ, lambda = 1/2: đuôi tô vàng là P(X > 4) = e^(-2).
size: 170 80
x: 0 8 2
y: 0 0.55 0.25
names: x f
area "exp(-x/2)/2" 4 8 vang
curve "exp(-x/2)/2" 0 8 xanh
:::

:::core
Đều: mật độ phẳng, xác suất tỉ lệ với độ dài khoảng. Mũ: thời gian chờ với P(X > x) = e^(-lambda x), và nó không nhớ đã chờ bao lâu.
:::

Đều trên [a, b]: E = (a + b)/2, V = (b - a)^2/12. Mũ tham số lambda:

$$ P(X > x) = e^{-\lambda x}, \quad E(X) = \frac{1}{\lambda}, \quad V(X) = \frac{1}{\lambda^2} $$

Không nhớ: P(X > s + t | X > s) = P(X > t).

Ví dụ: X đều trên [2, 6].

1. Mật độ 1/4: P(3 < X < 5) = 2/4. E(X) = 4, V(X) = 4^2/12 = 4/3.
2. E(X^2) = V(X) + (E(X))^2 = 4/3 + 16 = 52/3.

> Lỗi thường gặp: quên bình phương: đều trên [2, 6] có V = 16/12, không phải 4/12.

:::check
Q: Thời gian chờ có phân phối mũ, trung bình 4 phút. lambda bằng mấy? P(X > 8)? Đã chờ 5 phút, xác suất phải chờ thêm hơn 8 phút?
A: lambda = 1/4. P(X > 8) = e^(-2). Chờ thêm vẫn là e^(-2), vì mũ không nhớ.
:::

## Phân phối chuẩn

:::hook
Chiều cao, sai số đo, nhiễu trong dữ liệu: nhiều yếu tố nhỏ cộng lại cho ra hình chuông. Mọi hình chuông quy về một chuông chuẩn N(0, 1) để tra bảng.
:::

:::figure plane
caption: N(0, 1): giữa -1 và 1 là 2 Phi(1) = 0.6826; mỗi đuôi là 0.5 - Phi(1) = 0.1587.
size: 200 80
x: -3.5 3.5 1
y: 0 0.45
names: z f
area "exp(-x^2/2)/sqrt(2*pi)" -1 1 vang
curve "exp(-x^2/2)/sqrt(2*pi)" -3.5 3.5 xanh
:::

:::core
Mọi chuông N(mu, sigma^2) quy về N(0, 1) bằng Z = (X - mu)/sigma: đếm xem X cách trung bình bao nhiêu độ lệch chuẩn.
:::

$$ Z = \frac{X - \mu}{\sigma} \sim N(0, 1) $$

$$ P(a < X < b) = \Phi\left(\frac{b - \mu}{\sigma}\right) - \Phi\left(\frac{a - \mu}{\sigma}\right) $$

Phi(x): diện tích dưới chuông từ 0 đến x; Phi(-x) = -Phi(x), nửa trục là 0.5, nên P(X > a) = 0.5 - Phi((a - mu)/sigma). Phi(0.5) = 0.1915, Phi(1) = 0.3413, Phi(1.5) = 0.4332, Phi(2) = 0.4772.

Ví dụ: X ~ N(50, 16). Tính P(48 < X < 56).

1. sigma = sqrt(16) = 4.
2. Chuẩn hóa: (48 - 50)/4 = -0.5 và (56 - 50)/4 = 1.5.
3. P = Phi(1.5) - Phi(-0.5) = 0.4332 + 0.1915 = 0.6247.

> Lỗi thường gặp: chia cho phương sai. Với N(50, 16) phải chia cho 4, không chia cho 16.

:::check
Q: X ~ N(30, 25). Tính P(X < 35), dùng Phi(1) = 0.3413.
A: sigma = 5, z = (35 - 30)/5 = 1. P(X < 35) = 0.5 + Phi(1) = 0.8413.
:::
