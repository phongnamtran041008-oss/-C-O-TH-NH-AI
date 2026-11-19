---
id: gt_lib_t7
title_vi: Tích phân bất định và tích phân xác định
subject: giai_tich
floor: 7
summary_vi: Lấy nguyên hàm là đi ngược phép lấy đạo hàm; đổi biến và từng phần là hai cách đưa một tích phân lạ về bảng; công thức Newton-Leibniz biến nguyên hàm thành con số, và tích phân có cận trên là x cho lại chính hàm dưới dấu tích phân khi lấy đạo hàm.
skills: [gt_t7_nguyen_ham, gt_t7_doi_bien, gt_t7_tung_phan, gt_t7_ham_huu_ty, gt_t7_newton_leibniz, gt_t7_can_bien_thien]
---
## Nguyên hàm và bảng nguyên hàm

F là một nguyên hàm của f trên khoảng I khi F'(x) = f(x) với mọi x thuộc I. Trên một khoảng, hai nguyên hàm của cùng một hàm chỉ sai khác nhau một hằng số, nên mọi nguyên hàm được viết chung là F(x) + C.

$$ \int f(x)\,dx = F(x) + C \iff F'(x) = f(x) $$

Bảng cần thuộc (C là hằng số tùy ý):

- Nguyên hàm của x^a (a khác -1) là x^(a + 1)/(a + 1); của 1/x là ln|x|.
- Nguyên hàm của e^x là e^x; của sin x là -cos x; của cos x là sin x.
- Nguyên hàm của 1/cos^2 x là tan x; của 1/(1 + x^2) là arctan x; của 1/sqrt(1 - x^2) là arcsin x.
- Nếu đổi x thành ax + b thì chia thêm cho a: nguyên hàm của e^(3x) là e^(3x)/3.

Nhiều hàm phải biến đổi trước khi tra bảng: tan^2 x = 1/cos^2 x - 1, sin^2 x = (1 - cos(2x))/2.

Một điều kiện như F(1) = 2 chọn ra đúng một nguyên hàm: tìm nguyên hàm tổng quát rồi giải ra C. Với f'' cho trước thì lấy nguyên hàm hai lần, mỗi lần một hằng số, cần hai điều kiện.

Trên tập gồm nhiều khoảng rời nhau, như R \ {0}, mỗi khoảng được một hằng số riêng: ln|x| + 1 bên phải và ln|x| - 3 bên trái vẫn là một nguyên hàm của 1/x.

> Lỗi thường gặp: kết luận hai nguyên hàm bằng nhau. sin^2 x và -cos^2 x đều là nguyên hàm của sin(2x), chúng sai khác nhau hằng số 1. Luôn kiểm tra nguyên hàm bằng cách lấy đạo hàm lại.

## Phương pháp đổi biến

Nếu hàm dưới dấu tích phân có dạng f(u(x)) . u'(x), đặt u = u(x), du = u'(x) dx:

$$ \int f\big(u(x)\big)\,u'(x)\,dx = \int f(u)\,du $$

Dấu hiệu nhận ra: thấy một hàm và (gần đúng) đạo hàm của nó cùng lúc, như x và x^2 + 1, 1/x và ln x, cos x và sin x. Thiếu hằng số thì bù vào: x dx = du/2 khi u = x^2 + 1.

Với tích phân xác định, đổi cận cùng lúc với đổi biến, không cần quay lại biến x:

$$ \int_a^b f\big(u(x)\big)\,u'(x)\,dx = \int_{u(a)}^{u(b)} f(u)\,du $$

Ví dụ tích phân từ 0 đến 1 của x(x^2 + 1)^3 dx: u = x^2 + 1 chạy từ 1 đến 2, được (1/2) . (16 - 1)/4 = 15/8.

Có khi phải đặt ngược x = phi(t) để khử căn: với 1/(1 + sqrt(x)) đặt t = sqrt(x), x = t^2, dx = 2t dt.

Đổi biến x = -t cho kết quả quan trọng: tích phân của hàm lẻ trên đoạn [-a, a] bằng 0, của hàm chẵn bằng hai lần tích phân trên [0, a].

> Lỗi thường gặp: đổi biến mà giữ nguyên cận cũ. Với u = x^2, cận x = 2 thành u = 4, không phải u = 2.

## Tích phân từng phần

Từ quy tắc đạo hàm của tích (uv)' = u'v + uv':

$$ \int u\,dv = uv - \int v\,du, \qquad \int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du $$

Chọn u là phần có đạo hàm đơn giản hơn, dv là phần dễ lấy nguyên hàm. Thứ tự ưu tiên chọn u thường dùng: ln, arctan (hàm ngược), rồi đa thức, rồi lượng giác và mũ.

- Đa thức nhân e^x hoặc sin, cos: u là đa thức; mỗi lần dùng công thức bậc giảm một.
- x^n ln x hoặc ln x đứng một mình: u = ln x (với ln x đứng một mình, dv = dx).
- e^x sin x: dùng hai lần thì tích phân ban đầu xuất hiện lại; chuyển vế để giải ra.

Ví dụ tích phân từ 1 đến e của x ln x dx: u = ln x, v = x^2/2, được e^2/2 - (e^2 - 1)/4 = (e^2 + 1)/4.

Với họ tích phân I_n, từng phần cho công thức truy hồi; chẳng hạn tích phân từ 0 đến 1 của x^n e^x dx thỏa I_n = e - n I_(n-1).

> Lỗi thường gặp: sai dấu ở bước cuối. Nguyên hàm của x cos x là x sin x + cos x, vì trừ đi nguyên hàm của sin x (là -cos x) thành cộng.

## Tích phân hàm hữu tỉ và hàm lượng giác

Hàm hữu tỉ P/Q: nếu bậc của P không nhỏ hơn bậc của Q thì chia đa thức trước. Sau đó tách thành phân thức đơn giản theo các nhân tử của Q:

$$ \frac{px + q}{(x - r)(x - s)} = \frac{A}{x - r} + \frac{B}{x - s}, \qquad A = \frac{pr + q}{r - s},\; B = \frac{ps + q}{s - r} $$

Cách nhanh tìm A: nhân hai vế với mẫu rồi thay x = r. Nhân tử bậc hai vô nghiệm x^2 + bx + c cho phân thức (Bx + C)/(x^2 + bx + c), dẫn tới ln và arctan sau khi đưa mẫu về (x + b/2)^2 + k^2.

$$ \int \frac{dx}{x^2 + a^2} = \frac{1}{a}\arctan\frac{x}{a} + C $$

Hàm lượng giác:

- Lũy thừa lẻ của sin (hoặc cos): tách ra một thừa số sin x dx và đặt u = cos x.
- Lũy thừa chẵn: hạ bậc bằng sin^2 x = (1 - cos(2x))/2, cos^2 x = (1 + cos(2x))/2.
- Phép đặt tổng quát t = tan(x/2): sin x = 2t/(1 + t^2), cos x = (1 - t^2)/(1 + t^2), dx = 2dt/(1 + t^2), đưa về hàm hữu tỉ của t.

> Lỗi thường gặp: quên hệ số 1/a trước arctan. Nguyên hàm của 1/(t^2 + 4) là (1/2) arctan(t/2), không phải arctan(t/2).

## Tích phân xác định và công thức Newton-Leibniz

Tích phân xác định là giới hạn của tổng Riemann: chia [a, b] thành n đoạn bằng nhau, cộng f(điểm) . độ dài đoạn. Nếu f liên tục trên [a, b] và F là một nguyên hàm của f thì

$$ \int_a^b f(x)\,dx = F(b) - F(a) $$

Các tính chất dùng nhiều: tuyến tính; cộng theo đoạn (tích phân từ a đến c bằng từ a đến b cộng từ b đến c); đổi chỗ hai cận thì đổi dấu; f >= 0 thì tích phân không âm.

Hàm có trị tuyệt đối hoặc nhiều công thức: tách đoạn tại nơi biểu thức đổi dấu hoặc đổi công thức. Tích phân từ 0 đến 3 của |x^2 - 2x| dx = 4/3 + 4/3 = 8/3.

Giá trị trung bình của f trên [a, b] là (1/(b - a)) . tích phân; f liên tục thì có c trong [a, b] với f(c) bằng đúng giá trị đó.

Ngược lại, một giới hạn của tổng có thể là một tích phân: tổng (1/n) . (f(1/n) + f(2/n) + ... + f(n/n)) dần tới tích phân từ 0 đến 1 của f(x) dx.

> Lỗi thường gặp: dùng Newton-Leibniz cho hàm không liên tục trên đoạn. Tích phân từ -1 đến 1 của 1/x^2 không bằng -2: hàm không bị chặn quanh 0, tích phân đó phân kỳ.

## Tích phân với cận biến thiên

Nếu f liên tục thì hàm F(x) = tích phân từ a đến x của f(t) dt khả vi và F' = f (định lý cơ bản của giải tích). Kết hợp với quy tắc dây chuyền:

$$ \frac{d}{dx}\int_{u(x)}^{v(x)} f(t)\,dt = f\big(v(x)\big)\,v'(x) - f\big(u(x)\big)\,u'(x) $$

Ví dụ F(x) = tích phân từ x đến x^3 của 1/(1 + t^2) dt: F'(x) = 3x^2/(1 + x^6) - 1/(1 + x^2), F'(1) = 1.

Ứng dụng:

- Khảo sát hàm cho bởi tích phân: F' = f cho biết F tăng, giảm, cực trị ở đâu mà không cần tính F.
- Giới hạn dạng 0/0 có tích phân ở tử: dùng L'Hospital, đạo hàm của tử là hàm dưới dấu tích phân.
- Phương trình chứa tích phân của hàm chưa biết: lấy đạo hàm hai vế để được phương trình vi phân, rồi thay x bằng cận dưới để có điều kiện ban đầu.

> Lỗi thường gặp: quên nhân với đạo hàm của cận. Đạo hàm của tích phân từ 0 đến x^2 của cos t dt là 2x cos(x^2), không phải cos(x^2).
