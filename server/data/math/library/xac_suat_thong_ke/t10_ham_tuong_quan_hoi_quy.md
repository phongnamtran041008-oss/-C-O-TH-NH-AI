---
id: xs_lib_t10
title_vi: Tài năng: hàm của biến ngẫu nhiên, tương quan và hồi quy
subject: xac_suat_thong_ke
floor: 10
summary_vi: Tầng ẩn mở rộng ba hướng đi sâu của xác suất thống kê - tìm phân phối của Y = g(X), đọc và dùng bảng phân phối đồng thời của hai biến (biên, điều kiện, độc lập, hiệp phương sai, hệ số tương quan), tìm đường thẳng hồi quy bằng bình phương tối thiểu - và quay về ba tiên đề làm nền cho mọi công thức xác suất.
skills: [xs_t10_ham_bien_ngau_nhien, xs_t10_vecto_ngau_nhien, xs_t10_tuong_quan, xs_t10_hoi_quy, xs_t10_tien_de]
---
## Hàm của một biến ngẫu nhiên

Cho X có phân phối đã biết và Y = g(X). Phân phối của Y không cần học thêm gì mới: mỗi sự kiện về Y đều là một sự kiện về X.

Biến rời rạc: lập bảng giá trị g(x) cho từng giá trị x, rồi cộng xác suất của mọi x cho cùng một giá trị y.

$$ P(Y = y) = \sum_{x:\, g(x) = y} P(X = x) $$

Muốn tính kỳ vọng của Y thì không cần lập bảng của Y: lấy g(x) nhân với xác suất của chính x.

$$ E(g(X)) = \sum_x g(x)\,P(X = x), \qquad E(g(X)) 
e g(E(X)) $$

(dấu khác ở cuối đúng nói chung, chỉ bằng nhau trong vài trường hợp đặc biệt như g tuyến tính.)

Ví dụ: X nhận -1, 0, 1, 2 với xác suất 1/8, 3/8, 1/4, 1/4 và Y = X^2.

1. X = -1 và X = 1 cho cùng Y = 1; X = 0 cho Y = 0; X = 2 cho Y = 4.
2. P(Y = 1) = 1/8 + 1/4 = 3/8; P(Y = 0) = 3/8; P(Y = 4) = 1/4.
3. E(Y) = 0 . 3/8 + 1 . 3/8 + 4 . 1/4 = 11/8, cũng bằng 1 . 1/8 + 0 + 1 . 1/4 + 4 . 1/4.

Biến liên tục: dùng hàm phân phối rồi đạo hàm.

1. Viết F_Y(y) = P(Y < y) = P(g(X) < y).
2. Đưa về sự kiện của X: giải g(X) < y theo X (nếu g không đơn điệu thì có thể có hai khoảng).
3. Tính xác suất đó từ mật độ của X, được F_Y(y).
4. Đạo hàm theo y: f_Y(y) = F_Y'(y). Cuối cùng kiểm tra tích phân của f_Y bằng 1.

Với phép đổi tuyến tính Y = aX + b (a khác 0) có sẵn công thức:

$$ f_Y(y) = \frac{1}{|a|}\, f_X\!\left(\frac{y - b}{a}\right) $$

Ví dụ X đều trên (-1, 1), Y = X^2: F_Y(y) = P(-sqrt(y) < X < sqrt(y)) = sqrt(y) với 0 < y < 1, nên f_Y(y) = 1/(2 sqrt(y)); tích phân trên (0, 1) bằng 1.

> Lỗi thường gặp: coi E(X^2) = (E(X))^2 (hiệu của chúng chính là V(X)); quên nhánh âm khi giải X^2 < y; viết f_Y(y) = f_X(sqrt(y)) mà thiếu thừa số 1/(2 sqrt(y)) của phép đổi biến. Mật độ sai thường lộ ra khi tích phân của nó không bằng 1.

## Vectơ ngẫu nhiên hai chiều

Hai biến rời rạc X, Y được mô tả cùng nhau bởi bảng phân phối đồng thời P(X = i, Y = j), các ô cộng lại bằng 1. Quy ước ở đây: hàng ứng với giá trị của X, cột ứng với giá trị của Y.

:::matrix
P = 1/6 1/4 1/12 ; 1/6 1/12 1/4
:::

- Phân phối biên của X: cộng các ô trên mỗi hàng; của Y: cộng các ô trên mỗi cột.
- Xác suất có điều kiện: ô chia cho tổng của hàng (hay cột) chứa điều kiện.
- X và Y độc lập khi và chỉ khi mọi ô bằng tích hai xác suất biên của nó.

$$ P(X = i) = \sum_j P(X = i, Y = j), \qquad P(Y = j \mid X = i) = \frac{P(X = i, Y = j)}{P(X = i)} $$

$$ P(X = i, Y = j) = P(X = i)\,P(Y = j) \quad \forall\, i, j $$

Ví dụ với bảng trên (hai hàng X = 0, 1, ba cột Y = 0, 1, 2):

1. Cộng hàng: P(X = 0) = 1/6 + 1/4 + 1/12 = 1/2 và P(X = 1) = 1/2.
2. Cộng cột: P(Y = 0) = P(Y = 1) = P(Y = 2) = 1/3.
3. P(Y = 1 | X = 0) = (1/4)/(1/2) = 1/2.
4. Ô đầu tiên: P(X = 0, Y = 0) = 1/6 = 1/2 . 1/3, khớp; nhưng ô thứ hai 1/4 khác 1/2 . 1/3 = 1/6, nên X và Y không độc lập.

> Lỗi thường gặp: kiểm tra một ô thấy khớp rồi kết luận độc lập (một ô lệch là đủ để bác bỏ, nhưng phải đủ mọi ô để khẳng định); chia điều kiện cho tổng cột thay vì tổng hàng; nghĩ rằng hai phân phối biên đủ để dựng lại bảng đồng thời (cùng biên có thể có nhiều bảng khác nhau, chỉ khi độc lập thì bảng là tích hai biên).

## Hiệp phương sai và hệ số tương quan

Hiệp phương sai đo hai biến cùng tăng hay ngược chiều nhau quanh kỳ vọng của chúng.

$$ \mathrm{Cov}(X, Y) = E\big[(X - E(X))(Y - E(Y))\big] = E(XY) - E(X)\,E(Y) $$

Hệ số tương quan là hiệp phương sai đã chia cho độ lệch chuẩn của hai biến, nên không có đơn vị và nằm giữa -1 và 1.

$$ \rho(X, Y) = \frac{\mathrm{Cov}(X, Y)}{\sigma(X)\,\sigma(Y)}, \qquad -1 \le \rho \le 1 $$

Các tính chất dùng nhiều nhất:

- V(X + Y) = V(X) + V(Y) + 2 Cov(X, Y); tổng quát V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y).
- Cov(aX + b, cY + d) = ac Cov(X, Y); nhân một biến với số âm đổi dấu hệ số tương quan.
- rho = 1 hay rho = -1 đúng khi Y = aX + b với a > 0 hay a < 0 (hầu chắc chắn).
- X, Y độc lập thì Cov = 0; chiều ngược lại không đúng.

Ví dụ: X nhận 0 hay 1, Y nhận 0 hay 1, bảng phân phối đồng thời như sau (hàng ứng với X, cột ứng với Y).

:::matrix
P = 1/2 1/8 ; 1/8 1/4
:::

1. P(X = 1) = P(Y = 1) = 3/8 nên E(X) = E(Y) = 3/8.
2. Chỉ ô (1, 1) cho tích xy khác 0: E(XY) = 1/4.
3. Cov = 1/4 - (3/8)^2 = 7/64; V(X) = V(Y) = 3/8 . 5/8 = 15/64.
4. rho = (7/64)/(15/64) = 7/15.

> Lỗi thường gặp: viết E(XY) = E(X)E(Y) khi chưa biết hai biến không tương quan (khi đó Cov luôn ra 0); coi Cov = 0 nghĩa là độc lập - ví dụ X đều trên -1, 0, 1 và Y = X^2 có Cov = 0 mà Y hoàn toàn do X quyết định; quên rằng V(-Y) = V(Y), không âm.

## Hồi quy tuyến tính đơn

Từ mẫu hai chiều (x_1, y_1), ..., (x_n, y_n), đường hồi quy y = a + bx là đường làm tổng bình phương độ lệch dọc nhỏ nhất.

$$ \min_{a, b} \sum_{i=1}^{n} \big(y_i - a - b x_i\big)^2 $$

Đặt đạo hàm theo a và b bằng 0 cho nghiệm, viết qua S_xx và S_xy là hai tổng của độ lệch quanh trung bình.

$$ b = \frac{S_{xy}}{S_{xx}} = \frac{\sum (x_i - x_{tb})(y_i - y_{tb})}{\sum (x_i - x_{tb})^2}, \qquad a = y_{tb} - b\,x_{tb} $$

Ví dụ: năm điểm (0, 0), (1, 2), (2, 2), (3, 3), (4, 3).

1. x_tb = 2 và y_tb = 2; độ lệch của x: -2, -1, 0, 1, 2; của y: -2, 0, 0, 1, 1.
2. S_xx = 4 + 1 + 0 + 1 + 4 = 10; S_xy = 4 + 0 + 0 + 1 + 2 = 7.
3. b = 7/10 và a = 2 - 7/10 . 2 = 3/5, đường hồi quy y = 3/5 + 7x/10.

Ba điều cần nhớ về đường này:

- Nó luôn đi qua điểm trung bình (x_tb, y_tb), và tổng các phần dư y_i - (a + b x_i) bằng 0.
- Hệ số góc có thể viết b = r s_y/s_x với r là hệ số tương quan mẫu; r^2 là phần biến thiên của y mà đường thẳng giải thích được.
- Hồi quy x theo y là một đường khác (hệ số góc S_xy/S_yy, không phải nghịch đảo của b), trừ khi các điểm nằm đúng trên một đường thẳng.

> Lỗi thường gặp: chia ngược, viết b = S_xx/S_xy; nhầm S_xy/S_yy (đường của x theo y) với hệ số góc; dùng đường hồi quy để dự đoán xa ngoài khoảng dữ liệu; đọc r lớn thành "x gây ra y" - tương quan không phải nhân quả.

## Tiên đề xác suất

Mọi công thức xác suất đều đi ra từ ba tiên đề trên một họ các sự kiện của không gian mẫu Omega.

$$ P(A) \ge 0, \qquad P(\Omega) = 1, \qquad A \cap B = \varnothing \Rightarrow P(A \cup B) = P(A) + P(B) $$

(Với vô hạn đếm được các sự kiện đôi một xung khắc, tiên đề cộng viết cho cả dãy; ở không gian mẫu hữu hạn hai sự kiện là đủ.)

Một số hệ quả, mỗi cái chứng minh được chỉ bằng ba tiên đề:

- P(rỗng) = 0, vì Omega và rỗng xung khắc và hợp của chúng vẫn là Omega.
- P(A') = 1 - P(A), vì A và A' xung khắc với hợp là Omega.
- A nằm trong B thì P(A) <= P(B), vì P(B) = P(A) + P(B \ A) và P(B \ A) >= 0; do đó P(A) <= 1.
- P(A + B) = P(A) + P(B) - P(AB) cho mọi A, B: tách A + B = A + (B \ A) và B = AB + (B \ A).

Ví dụ kiểm tra một cách đặt xác suất: trên Omega = {1, 2, 3, 4} cho P({k}) = c k.

1. Chuẩn hoá: c (1 + 2 + 3 + 4) = 1 cho c = 1/10; các giá trị 1/10, 2/10, 3/10, 4/10 đều không âm.
2. Tính cộng: P({1, 2}) = 3/10 và P({3, 4}) = 7/10, cộng lại bằng P(Omega) = 1.

> Lỗi thường gặp: coi "P(A) <= 1" hay "P(A') = 1 - P(A)" là tiên đề (chúng là hệ quả); cho một bộ xác suất có tổng khác 1 hay có số âm mà vẫn gọi là phân phối; dùng tính cộng cho hai sự kiện không xung khắc.
