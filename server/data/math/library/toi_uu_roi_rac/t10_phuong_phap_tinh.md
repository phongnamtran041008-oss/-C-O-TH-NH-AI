---
id: tr_lib_t10
title_vi: Mở rộng: phương pháp tính
subject: toi_uu_roi_rac
floor: 10
summary_vi: Máy tính chỉ làm việc với số gần đúng, nên phải biết sai số lan truyền thế nào qua các phép tính, và biết giải phương trình f(x) = 0 bằng các phương pháp lặp: chia đôi (chắc chắn nhưng chậm), lặp đơn (cần điều kiện co) và Newton (nhanh, hội tụ bậc hai, nhưng phụ thuộc điểm xuất phát).
skills: [tr_t10_sai_so, tr_t10_chia_doi, tr_t10_lap_don, tr_t10_newton]
---
## Sai số và chữ số đáng tin

Một số đo gần đúng a có sai số tuyệt đối Delta_a (độ lệch tối đa so với giá trị thật) và sai số tương đối delta_a = Delta_a/|a| (không có đơn vị, thường viết dưới dạng phần trăm). Ví dụ x = 12.5 m với Delta_x = 0.05 m có delta_x = 0.05/12.5 = 0.4%.

Sai số lan truyền qua phép tính theo quy tắc bậc nhất (khi sai số nhỏ):

- Tổng và hiệu: sai số tuyệt đối cộng lại, Delta = Delta_x + Delta_y, kể cả khi trừ.
- Tích và thương: sai số tương đối cộng lại, delta = delta_x + delta_y.
- Lũy thừa x^n: delta = n delta_x.
- Hàm một biến f(x): Delta_f = |f'(x)| Delta_x.

$$ \Delta_{xy} \approx |y|\,\Delta_x + |x|\,\Delta_y, \qquad \Delta_{f(x)} \approx |f'(x)|\,\Delta_x $$

Chữ số hàng 10^s của một số gần đúng là đáng tin khi sai số tuyệt đối không vượt quá nửa đơn vị của hàng đó:

$$ \Delta_a \le 0.5 \cdot 10^{s} $$

Ví dụ: A = x y với x = 10 +- 0.1 và y = 5 +- 0.05.

1. delta_x = 0.1/10 = 1% và delta_y = 0.05/5 = 1%.
2. delta_A = 1% + 1% = 2%, A = 50.
3. Delta_A = 2% . 50 = 1, tức A = 50 +- 1; chữ số hàng đơn vị của 50 không đáng tin (1 > 0.5).

> Lỗi thường gặp: trừ hai sai số khi tính sai số của hiệu (luôn cộng); chia sai số của hai số để được sai số của thương (phải cộng sai số tương đối); coi hiệu của hai số gần nhau còn chính xác (100.2 - 99.8 = 0.4 có sai số 0.2, tức 50%); đếm mọi chữ số đã viết là đáng tin.

## Phương pháp chia đôi

Nếu f liên tục trên [a, b] và f(a) f(b) < 0 thì f có nghiệm trong [a, b] (định lý giá trị trung gian). Chia đôi: tính f ở trung điểm c = (a + b)/2 và giữ nửa đoạn mà f đổi dấu, rồi lặp.

Sau n lần chia, đoạn nghiệm dài (b - a)/2^n; lấy trung điểm của nó làm nghiệm gần đúng thì sai số không quá một nửa độ dài:

$$ |x_n - x^*| \le \frac{b - a}{2^{n+1}} $$

Muốn sai số không quá e, cần n thoả 2^(n+1) >= (b - a)/e. Ví dụ [1, 2] và e = 0.001: 2^(n+1) >= 1000 nên n + 1 >= 10, n = 9.

Ví dụ giữ nửa đoạn với p(x) = x^3 - 2 trên [1, 2] (p(1) = -1 < 0, p(2) = 6 > 0):

1. c = 3/2, p(3/2) = 11/8 > 0, cùng dấu với p(2), nên nghiệm ở [1, 3/2].
2. c = 5/4, p(5/4) = -3/64 < 0, cùng dấu với p(1), nên nghiệm ở [5/4, 3/2].

Chia đôi luôn hội tụ (với hàm liên tục đổi dấu) nhưng chậm: mỗi bước chỉ giảm sai số một nửa, hội tụ tuyến tính. Nó tìm một nghiệm trong đoạn, không phải mọi nghiệm.

> Lỗi thường gặp: giữ nhầm nửa đoạn (phải giữ nửa mà f đổi dấu, tức hai đầu trái dấu nhau); nghĩ f(a) f(b) > 0 nghĩa là không có nghiệm; đếm số lần chia theo độ dài đoạn (b - a)/2^n thay vì sai số của trung điểm (b - a)/2^(n+1), hoặc nhầm số chữ số thập phân với số lần chia.

## Phương pháp lặp đơn

Viết f(x) = 0 thành x = g(x) rồi lặp x_(n+1) = g(x_n). Nếu g ánh xạ đoạn [a, b] vào chính nó và |g'(x)| <= q < 1 trên [a, b] (g là phép co) thì có đúng một điểm bất động x* trong [a, b] và phép lặp hội tụ về nó với mọi x_0 trong [a, b].

$$ |x_n - x^*| \le \frac{q^n}{1 - q}\,|x_1 - x_0|, \qquad |x_n - x^*| \le \frac{q}{1 - q}\,|x_n - x_{n-1}| $$

Gần điểm bất động, x_(n+1) - x* xấp xỉ g'(x*) (x_n - x*): |g'(x*)| < 1 thì hội tụ tuyến tính với hệ số đó (g' âm thì các x_n xen kẽ hai bên x*), |g'(x*)| > 1 thì phân kỳ. Cùng một phương trình có nhiều cách viết x = g(x), có cách hội tụ và có cách phân kỳ.

Ví dụ g(x) = (x^2 + 1)/4 trên [0, 1], x_0 = 0:

1. g'(x) = x/2 nên q = 1/2 < 1 trên [0, 1]; g(0) = 1/4 và g(1) = 1/2 nằm trong [0, 1].
2. x_1 = g(0) = 1/4, và cận tiên nghiệm cho n = 3 là (1/2)^3/(1 - 1/2) . 1/4 = 1/16.

> Lỗi thường gặp: kiểm tra |g'| < 1 mà quên điều kiện ánh xạ đoạn vào chính nó; chọn điểm có |g'| lớn hơn làm điểm hút (điểm có |g'| > 1 là điểm đẩy); tin rằng |g'(x*)| < 1 đủ để hội tụ từ mọi x_0 (chỉ cục bộ, như g(x) = x^2 chỉ hút về 0 khi |x_0| < 1).

## Phương pháp Newton

Thay đường cong bằng tiếp tuyến tại x_n và lấy giao điểm của tiếp tuyến với trục hoành làm x_(n+1):

$$ x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} $$

Với f(x) = x^2 - a công thức thành x_(n+1) = (x_n + a/x_n)/2. Khi f'(x*) khác 0 và x_0 đủ gần nghiệm, Newton hội tụ bậc hai: sai số bình phương lên sau mỗi bước, số chữ số đúng xấp xỉ gấp đôi.

Ví dụ tìm sqrt(2) với f(x) = x^2 - 2 và x_0 = 1:

1. f'(x) = 2x, nên x_1 = 1 - (-1)/2 = 3/2.
2. x_2 = 3/2 - (1/4)/3 = 17/12 = 1.41667, x_3 = 577/408 = 1.4142157; so với sqrt(2) = 1.4142136 các sai số là 0.41, 0.086, 0.0025, 0.0000021.

Newton có thể hỏng: f'(x_n) = 0 thì không tính được bước tiếp theo; chọn x_0 xấu có thể làm dãy lặp vòng (f(x) = x^3 - 2x + 2 từ x_0 = 0 cho 0, 1, 0, 1, ...) hoặc nhảy xa nghiệm cần tìm.

> Lỗi thường gặp: dùng lại đạo hàm cũ f'(x_0) ở mọi bước (đó là một phương pháp khác, chậm hơn); nhầm tốc độ của Newton (bậc hai) với của chia đôi (tuyến tính, mỗi bước một nửa); tin Newton hội tụ với mọi điểm xuất phát; tính f(x_n)/f'(x_n) rồi cộng thay vì trừ.
