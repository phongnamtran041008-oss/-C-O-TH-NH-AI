---
id: gt_lib_t4
title_vi: Đạo hàm và vi phân
subject: giai_tich
floor: 4
summary_vi: Đạo hàm đo xem hàm thay đổi nhanh tới đâu tại một điểm; học định nghĩa của nó, các quy tắc tính, quy tắc dây chuyền cho hàm hợp, đạo hàm của hàm ngược và hàm tham số, rồi vi phân và đạo hàm cấp cao.
skills: [gt_t4_dinh_nghia_dao_ham, gt_t4_quy_tac_tinh, gt_t4_day_chuyen, gt_t4_ham_nguoc_tham_so, gt_t4_vi_phan_cap_cao]
---
## Đạo hàm theo định nghĩa

Khi x đi từ a tới a + h, hàm đi từ f(a) tới f(a + h). Tỉ số số gia (f(a + h) - f(a)) / h là hệ số góc của dây cung nối hai điểm trên đồ thị. Cho h -> 0, dây cung quay dần thành tiếp tuyến, và hệ số góc của nó là đạo hàm:

$$ f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h} $$

f có đạo hàm tại a khi giới hạn này tồn tại hữu hạn. Tiếp tuyến của đồ thị tại điểm (a, f(a)) là

$$ y = f'(a)(x - a) + f(a) $$

Ví dụ: f(x) = x^2 + 3x tại a = 2. f(2 + h) - f(2) = 7h + h^2, chia cho h được 7 + h, cho h -> 0 được f'(2) = 7.

Có đạo hàm thì liên tục, nhưng liên tục chưa chắc có đạo hàm: |x| liên tục tại 0, còn tỉ số |h|/h bằng 1 bên phải và -1 bên trái, nên không có đạo hàm ở đó. Đồ thị có một góc nhọn tại 0.

Khi công thức có giá trị tuyệt đối hoặc nhiều mảnh, quay về định nghĩa: với f(x) = x|x|, tỉ số (f(h) - f(0))/h = |h| dần tới 0, nên f'(0) = 0.

> Lỗi thường gặp: rút gọn tỉ số số gia rồi thay h = 0 nhầm ở mẫu, chẳng hạn từ -1/(2(2 + h)) ra -1/2 thay vì -1/4. Thay h = 0 vào cả biểu thức, mọi chỗ có h.

## Quy tắc tính đạo hàm

Bảng đạo hàm cơ bản (trên tập xác định của từng hàm):

$$ (x^n)' = n x^{n-1}, \quad (e^x)' = e^x, \quad (\ln x)' = \frac{1}{x} $$

$$ (\sin x)' = \cos x, \quad (\cos x)' = -\sin x, \quad (\tan x)' = \frac{1}{\cos^2 x} $$

Tổng, hiệu, tích với hằng số lấy đạo hàm từng phần. Tích và thương thì có quy tắc riêng:

$$ (uv)' = u'v + uv', \qquad \left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2} $$

Ví dụ: (x^2 . e^x)' = 2x e^x + x^2 e^x = (x^2 + 2x) e^x. Với f(x) = (x^2 + 1)/(x - 1): f'(x) = (2x(x - 1) - (x^2 + 1))/(x - 1)^2 = (x^2 - 2x - 1)/(x - 1)^2.

Trong quy tắc thương, thứ tự ở tử quan trọng: u'v đứng trước. Đảo lại thì kết quả đổi dấu.

> Lỗi thường gặp: viết (uv)' = u'v' hoặc (u/v)' = u'/v'. Thử với u = v = x: (x . x)' = 2x chứ không phải 1.

## Quy tắc dây chuyền

Hàm hợp f(g(x)) có đạo hàm bằng đạo hàm của hàm ngoài, lấy tại hàm trong, nhân với đạo hàm của hàm trong:

$$ \big(f(g(x))\big)' = f'(g(x)) \cdot g'(x) $$

Cách làm: gọi tên hàm trong u = g(x), lấy đạo hàm hàm ngoài theo u, rồi nhân u'.

- (sin 3x)' = cos 3x . 3.
- (2x - 1)^5 có đạo hàm 5(2x - 1)^4 . 2.
- e^(x^2 + 3x) có đạo hàm (2x + 3) e^(x^2 + 3x).
- ln(x^2 + 1) có đạo hàm 2x/(x^2 + 1).

Có nhiều lớp thì nhân hết các đạo hàm, từ ngoài vào trong: sin^2(3x) = (sin 3x)^2 có đạo hàm 2 sin 3x . cos 3x . 3.

Khi đề cho số: nếu g(1) = 2, g'(1) = 3 và f'(2) = 5 thì đạo hàm của f(g(x)) tại 1 bằng f'(2) . 3 = 15. Đạo hàm ngoài lấy tại g(1), không phải tại 1.

> Lỗi thường gặp: quên nhân đạo hàm của hàm trong, như viết (e^(x^2 + 3x))' = e^(x^2 + 3x). Sau khi lấy đạo hàm hàm ngoài, luôn hỏi: hàm trong là gì, đã nhân đạo hàm của nó chưa?

## Đạo hàm của hàm ngược và hàm cho bởi tham số

Nếu f liên tục, đơn điệu ngặt và f'(x0) khác 0 thì hàm ngược có đạo hàm tại y0 = f(x0):

$$ (f^{-1})'(y_0) = \frac{1}{f'(x_0)} $$

Không cần công thức của f^(-1): chỉ cần tìm x0 mà f(x0) = y0. Ví dụ f(x) = x^3 + x, tính (f^(-1))'(2): f(1) = 2 nên x0 = 1, f'(1) = 4, kết quả 1/4.

Từ đó có đạo hàm của các hàm lượng giác ngược:

$$ (\arcsin x)' = \frac{1}{\sqrt{1 - x^2}}, \qquad (\arctan x)' = \frac{1}{1 + x^2} $$

Đường cong cho bởi tham số x = x(t), y = y(t) có hệ số góc

$$ \frac{dy}{dx} = \frac{y'(t)}{x'(t)} \quad (x'(t) \ne 0) $$

Ví dụ x = t^2 - 2t, y = t^3 - 3t tại t = 2: x' = 2, y' = 9, dy/dx = 9/2.

Đạo hàm cấp hai theo x phải lấy đạo hàm của dy/dx (một hàm của t) rồi lại chia cho x'(t), không phải y''(t)/x''(t).

> Lỗi thường gặp: lấy f' tại y0 thay vì tại x0 = f^(-1)(y0), và đảo ngược tỉ số thành x'(t)/y'(t).

## Vi phân và đạo hàm cấp cao

Vi phân của y = f(x) là dy = f'(x) dx. Khi dx nhỏ, số gia của hàm gần bằng vi phân, cho công thức tính gần đúng:

$$ f(x_0 + dx) \approx f(x_0) + f'(x_0)\, dx $$

Ví dụ sqrt(4.1): x0 = 4, dx = 0.1, f'(4) = 1/4, nên sqrt(4.1) xấp xỉ 2 + 0.025 = 2.025.

Đạo hàm cấp hai là đạo hàm của f', cấp n là đạo hàm n lần, viết f^(n). Một số công thức cấp n đáng nhớ:

$$ (e^{ax})^{(n)} = a^n e^{ax}, \qquad \left(\frac{1}{x}\right)^{(n)} = \frac{(-1)^n n!}{x^{n+1}} $$

Đạo hàm cấp n của x^n là n!, và mọi đạo hàm cấp cao hơn của nó bằng 0.

Với tích, đạo hàm cấp hai có thêm số hạng giữa: (uv)'' = u''v + 2u'v' + uv''.

> Lỗi thường gặp: quên nhân dx khi tính gần đúng, ra sqrt(4.1) xấp xỉ 2.25. Thử bình phương lại đáp số để thấy ngay nó quá xa.
