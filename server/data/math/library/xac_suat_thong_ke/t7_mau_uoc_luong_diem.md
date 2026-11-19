---
id: xs_lib_t7
title_vi: Tổng thể, mẫu và ước lượng điểm
subject: xac_suat_thong_ke
floor: 7
summary_vi: Không đo được cả tổng thể thì ta đo một mẫu ngẫu nhiên; trung bình mẫu và phương sai mẫu hiệu chỉnh là những con số tính từ mẫu để ước lượng các tham số chưa biết, và ước lượng hợp lý cực đại chọn tham số làm cho mẫu đã thấy dễ xảy ra nhất.
skills: [xs_t7_tong_the_mau, xs_t7_dac_trung_mau, xs_t7_phan_phoi_mau, xs_t7_uoc_luong_diem, xs_t7_hop_ly_cuc_dai]
---
## Tổng thể và mẫu ngẫu nhiên

Tổng thể là toàn bộ các đối tượng cần nghiên cứu (mọi đệ tử của tông môn, mọi viên đan của một lô). Mẫu là phần được chọn ra để đo; số phần tử của mẫu là cỡ mẫu n.

- Tham số: một con số của tổng thể, như trung bình mu, phương sai sigma^2, tỷ lệ p. Nó cố định nhưng thường chưa biết.
- Thống kê: một con số tính từ mẫu, như trung bình mẫu x_tb, tần suất f. Chọn mẫu khác thì được số khác.

Mẫu ngẫu nhiên cỡ n là n biến X_1, ..., X_n độc lập, mỗi biến có cùng phân phối với tổng thể. Lấy có hoàn lại (hoặc từ một tổng thể rất lớn) cho đúng điều đó; bốc thăm theo danh sách, mỗi nhóm cùng khả năng, cho mẫu không thiên lệch.

$$ X_{tb} = \frac{X_1 + X_2 + \cdots + X_n}{n} $$

Trước khi lấy mẫu, X_tb là một biến ngẫu nhiên; sau khi lấy mẫu, nó cho một con số x_tb.

> Lỗi thường gặp: coi một thống kê là chính tham số. 200 viên đan có 14 viên hỏng cho f = 0.07, nhưng tỷ lệ hỏng của cả lô chỉ được ước lượng bằng 0.07, không bằng đúng 0.07. Một lỗi khác: rút không hoàn lại từ một tổng thể nhỏ rồi coi các lần rút là độc lập.

## Trung bình mẫu và phương sai mẫu

Với số liệu x_1, ..., x_n, trung bình mẫu và phương sai mẫu hiệu chỉnh là

$$ x_{tb} = \frac{1}{n}\sum_{i=1}^{n} x_i, \qquad s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - x_{tb})^2 $$

Độ lệch chuẩn mẫu là s = sqrt(s^2). Công thức tính nhanh, có được bằng cách khai triển bình phương:

$$ s^2 = \frac{\sum x_i^2 - n\,x_{tb}^2}{n-1} $$

Ví dụ mẫu 2, 4, 4, 5, 7, 8 (n = 6):

1. x_tb = 30/6 = 5.
2. Các độ lệch -3, -1, -1, 0, 2, 3; tổng bình phương 24.
3. s^2 = 24/5 (cách khác: tổng x_i^2 = 174, 174 - 6 . 25 = 24).

Với bảng tần số (giá trị x_i xuất hiện n_i lần) thì nhân mỗi số hạng với n_i và n = tổng các n_i. Cộng cùng một số vào mọi số liệu làm x_tb tăng theo nhưng không đổi s^2.

> Lỗi thường gặp: chia cho n thay vì n - 1. Mẫu 3, 5, 7 có s^2 = 8/2 = 4; số 8/3 là phương sai chưa hiệu chỉnh.

## Phân phối của trung bình mẫu

Nếu tổng thể có kỳ vọng mu và phương sai sigma^2, mẫu ngẫu nhiên cỡ n cho

$$ E(X_{tb}) = \mu, \qquad V(X_{tb}) = \frac{\sigma^2}{n}, \qquad \sigma(X_{tb}) = \frac{\sigma}{\sqrt{n}} $$

Trung bình mẫu phân tán ít hơn một số liệu đơn lẻ: tăng n gấp 4 thì độ lệch chuẩn của X_tb giảm một nửa. Nếu tổng thể có phân phối chuẩn thì X_tb có phân phối chuẩn đúng; nếu không, với n lớn X_tb vẫn xấp xỉ chuẩn (tầng 8).

Ví dụ tổng thể N(100, 36), n = 9: X_tb có độ lệch chuẩn 6/3 = 2, nên P(X_tb > 104) = 0.5 - Phi(2) = 0.0228 (Phi là hàm Laplace, tích phân của mật độ N(0, 1) từ 0 đến x).

> Lỗi thường gặp: chuẩn hóa X_tb bằng sigma thay cho sigma/sqrt(n). Với gói linh trà N(500, 16^2) và n = 16, mốc 492 chuẩn hóa thành (492 - 500)/4 = -2, không phải (492 - 500)/16 = -0.5.

## Ước lượng điểm không chệch

Một thống kê T dùng để ước lượng tham số theta là không chệch khi E(T) = theta với mọi giá trị của theta.

$$ E(X_{tb}) = \mu, \qquad E(s^2) = \sigma^2, \qquad E(f) = p $$

Với T = c_1 X_1 + ... + c_n X_n thì E(T) = (c_1 + ... + c_n) mu: T không chệch cho mu đúng khi tổng các hệ số bằng 1. Trong các ước lượng không chệch, ước lượng có phương sai nhỏ hơn là hiệu quả hơn: với n = 3 và sigma^2 = 8, X_tb có phương sai 8/3, còn (X_1 + 2X_2 + X_3)/4 có phương sai 3, nên X_tb tốt hơn.

Vì sao chia cho n - 1: E(tổng của (X_i - X_tb)^2) = n(sigma^2 + mu^2) - n(sigma^2/n + mu^2) = (n - 1) sigma^2.

> Lỗi thường gặp: nghĩ phương sai chia cho n là không chệch. Kỳ vọng của nó là (n - 1) sigma^2/n: với sigma^2 = 10 và n = 5 chỉ được 8.

## Ước lượng hợp lý cực đại

Hàm hợp lý L(theta) là xác suất (hay mật độ) của chính mẫu đã thấy, coi như hàm của tham số; ước lượng hợp lý cực đại theta* là giá trị làm L lớn nhất. Lấy logarit để tích thành tổng rồi giải phương trình đạo hàm bằng 0:

$$ L(\theta) = \prod_{i=1}^{n} f(x_i; \theta), \qquad \frac{d}{d\theta}\ln L(\theta) = 0 $$

Ví dụ phân phối mũ, mật độ lambda e^(-lambda x), mẫu 2, 3, 5, 6:

1. ln L(lambda) = 4 ln lambda - 16 lambda (n = 4, tổng x_i = 16).
2. Đạo hàm 4/lambda - 16 = 0 cho lambda = 1/4.
3. Đạo hàm cấp hai -4/lambda^2 < 0, nên lambda* = 1/4 = 1/x_tb.

Các kết quả hay gặp: Bernoulli p* = k/n (k lần thành công trong n lần); Poisson lambda* = x_tb; mũ lambda* = 1/x_tb; số lần thử đến lần thành công đầu tiên p* = 1/x_tb; trung bình của phân phối chuẩn mu* = x_tb.

> Lỗi thường gặp: đạo hàm sai logarit. Với Poisson, (ln L)' = -n + (tổng x_i)/lambda, không phải -n + (tổng x_i) lambda; đạo hàm đúng cho lambda* = x_tb, khớp với E(X) = lambda.
