---
id: gt_lib_t8
title_vi: Ứng dụng của tích phân và tích phân suy rộng
subject: giai_tich
floor: 8
summary_vi: Diện tích, thể tích và độ dài đều là tổng của vô số mảnh nhỏ, nên đều là tích phân; khi cận ra vô cùng hoặc hàm vọt lên vô cùng, tích phân trở thành một giới hạn có thể hội tụ hay phân kỳ, và phép so sánh với 1/x^p cho biết điều đó mà không cần tính.
skills: [gt_t8_dien_tich, gt_t8_the_tich, gt_t8_do_dai_cung, gt_t8_suy_rong_loai_1, gt_t8_suy_rong_loai_2, gt_t8_tieu_chuan_hoi_tu]
---
## Diện tích hình phẳng

Miền giữa hai đồ thị y = f(x) và y = g(x) với a <= x <= b có diện tích

$$ S = \int_a^b \big|f(x) - g(x)\big|\,dx $$

Cách làm:

1. Giải f(x) = g(x) để tìm các giao điểm; chúng chia đoạn thành nhiều khúc.
2. Trên mỗi khúc, xem hàm nào nằm trên (thử một điểm ở giữa).
3. Tích phân (hàm trên - hàm dưới) trên từng khúc rồi cộng lại.

Ví dụ y = x^2 và y = 2x + 3 cắt nhau tại -1 và 3, đường thẳng ở trên: S = tích phân từ -1 đến 3 của (2x + 3 - x^2) dx = 32/3.

Khi miền được mô tả gọn hơn theo y (một đường cong cho x theo y), lấy tích phân theo y: S = tích phân của (x_phải - x_trái) dy. Miền giữa y^2 = 2x và y = x - 4 tính theo y chỉ cần một tích phân, ra 18.

Diện tích dưới parabol a(x - r)(x - s) giữa hai nghiệm luôn bằng |a|(s - r)^3/6.

> Lỗi thường gặp: bỏ trị tuyệt đối khi hiệu f - g đổi dấu. Với y = x^3 và y = x, tích phân có dấu trên [-1, 1] bằng 0, còn diện tích thật là 1/2.

## Thể tích vật thể tròn xoay

Quay miền dưới y = f(x) >= 0 (a <= x <= b) quanh trục Ox: mỗi lát cắt vuông góc với trục là một hình tròn bán kính f(x).

$$ V_{Ox} = \pi\int_a^b f(x)^2\,dx $$

Miền giữa hai đường f >= g >= 0 cho lát cắt hình vành khăn, diện tích pi(f^2 - g^2). Quay quanh trục Oy một miền dưới y = f(x) với 0 <= a <= x <= b, dùng phương pháp vỏ trụ: dải đứng tại x quay thành vỏ trụ bán kính x, chiều cao f(x).

$$ V_{Oy} = 2\pi\int_a^b x\,f(x)\,dx $$

Ví dụ: quay y = sqrt(x), 0 <= x <= 4 quanh Ox được 8pi; quay vòm y = sin x (0 <= x <= pi) quanh Oy được 2pi . pi = 2pi^2.

Công thức thể tích hình nón pi r^2 h/3 và hình cầu (4/3)pi r^3 đều ra từ đây, khi quay đoạn thẳng y = (r/h)x hoặc nửa đường tròn.

> Lỗi thường gặp: viết diện tích vành khăn thành pi(f - g)^2. Đúng là pi(f^2 - g^2): lấy hình tròn lớn trừ hình tròn nhỏ.

## Độ dài đường cong

Một mảnh nhỏ của đường cong có độ dài xấp xỉ sqrt(dx^2 + dy^2). Với đồ thị y = f(x), a <= x <= b, và với đường cong tham số x = x(t), y = y(t), t từ alpha đến beta:

$$ L = \int_a^b \sqrt{1 + f'(x)^2}\,dx, \qquad L = \int_{\alpha}^{\beta} \sqrt{x'(t)^2 + y'(t)^2}\,dt $$

Hầu hết các tích phân này không tính được bằng nguyên hàm sơ cấp; bài tập chọn đường cong để biểu thức dưới căn là một bình phương:

- y = (2/3)x^(3/2): 1 + (y')^2 = 1 + x.
- y = x^2/2 - (ln x)/4: 1 + (y')^2 = (x + 1/(4x))^2.
- Cycloid x = t - sin t, y = 1 - cos t: x'^2 + y'^2 = 4 sin^2(t/2), một nhịp dài 8.

Khi lấy căn bậc hai của một bình phương, nhớ giá trị tuyệt đối. Astroid x = cos^3 t, y = sin^3 t có căn bằng 3|sin t cos t|; dùng tính đối xứng, tổng độ dài bằng 4 lần phần trong góc phần tư thứ nhất, tức 6.

> Lỗi thường gặp: dùng y thay cho y' dưới dấu căn, hoặc quên số 1. Công thức là sqrt(1 + (y')^2).

## Tích phân suy rộng cận vô hạn

Khi một cận là vô cùng, tích phân được định nghĩa bằng giới hạn:

$$ \int_a^{+\infty} f(x)\,dx = \lim_{R \to +\infty} \int_a^R f(x)\,dx $$

Nếu giới hạn tồn tại hữu hạn thì tích phân hội tụ, ngược lại phân kỳ (kể cả khi không có giới hạn, như tích phân của sin x). Tích phân trên cả trục thì tách tại một điểm c: hội tụ khi cả hai phần hội tụ, với hai giới hạn độc lập.

Họ quan trọng nhất (a > 0):

$$ \int_a^{+\infty} \frac{dx}{x^p} < +\infty \iff p > 1 $$

Ví dụ tích phân từ 1 đến +vô cùng của ln x / x^2 dx: từng phần cho 1 - (ln R + 1)/R, dần tới 1. Tích phân từ 0 đến +vô cùng của e^(-x) sin x dx bằng 1/2.

Với hàm hữu tỉ, gộp các logarit lại trước khi cho R ra vô cùng: (1/2) ln((R - 1)/(R + 1)) -> 0, dù từng phần ln(R - 1), ln(R + 1) đều ra vô cùng.

> Lỗi thường gặp: lấy giới hạn đối xứng của tích phân từ -R đến R. Tích phân của x trên cả trục phân kỳ, dù tích phân từ -R đến R luôn bằng 0.

## Tích phân suy rộng của hàm không bị chặn

Khi f không bị chặn gần đầu mút a (ví dụ 1/sqrt(x) gần 0), lấy giới hạn từ bên trong:

$$ \int_a^b f(x)\,dx = \lim_{c \to a^+} \int_c^b f(x)\,dx $$

Nếu điểm bất thường nằm bên trong đoạn, tách đoạn tại đó; tích phân hội tụ khi mọi phần đều hội tụ. Họ so sánh ở đây ngược chiều với cận vô hạn:

$$ \int_0^1 \frac{dx}{x^p} < +\infty \iff p < 1 $$

Ví dụ tích phân từ 0 đến 1 của ln x dx: x ln x - x từ c đến 1 là -1 - c ln c + c, và c ln c -> 0, nên bằng -1. Tích phân từ 0 đến 9 của 1/(x - 1)^(2/3) dx có điểm bất thường x = 1 bên trong; hai phần cho 3 và 6, tổng 9.

Các dạng 0 . vô cùng sinh ra ở đầu mút (như sqrt(c) ln c) phải tính bằng L'Hospital, đừng đoán.

> Lỗi thường gặp: không nhìn thấy điểm bất thường ở giữa đoạn và dùng thẳng Newton-Leibniz, hoặc kết luận phân kỳ chỉ vì hàm không xác định tại một đầu mút.

## Tiêu chuẩn hội tụ

Khi không tính được nguyên hàm, so sánh với hàm đã biết. Với f, g không âm trên [a, +vô cùng):

- So sánh: 0 <= f <= g. Tích phân của g hội tụ thì của f hội tụ; tích phân của f phân kỳ thì của g phân kỳ.
- So sánh giới hạn: nếu f(x)/g(x) -> L với 0 < L < +vô cùng thì hai tích phân cùng hội tụ hoặc cùng phân kỳ.

$$ f(x) \sim \frac{C}{x^p} \;(x \to +\infty) \;\Rightarrow\; \left( \int_a^{+\infty} f(x)\,dx < +\infty \iff p > 1 \right) $$

Cách tìm p: giữ lũy thừa cao nhất ở tử và ở mẫu. sqrt(x)/(x^2 + 1) giống 1/x^(3/2), hội tụ; x/(x^2 + 1) giống 1/x, phân kỳ. Với tích phân từ 0 đến +vô cùng, xét riêng hai đầu: 1/(x^p(1 + x)) hội tụ khi 0 < p < 1.

Hàm dần tới 0 chưa đủ để hội tụ: 1/x dần tới 0 mà tích phân phân kỳ. Hàm có dao động bị chặn bởi một hàm khả tích, như sin^2 x/x^2 <= 1/x^2, thì hội tụ.

> Lỗi thường gặp: so sánh sai chiều. Từ 1/(x + sqrt(x)) <= 1/x và tích phân của 1/x phân kỳ, không kết luận được gì; phải chặn dưới, chẳng hạn 1/(x + sqrt(x)) >= 1/(2x).
