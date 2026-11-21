---
id: gt_lib_t4
title_vi: Đạo hàm và vi phân
subject: giai_tich
floor: 4
format: 2
summary_vi: Đạo hàm là tốc độ thay đổi tại một điểm, là hệ số góc của tiếp tuyến: định nghĩa, quy tắc tính, dây chuyền, hàm ngược, vi phân và đạo hàm cấp cao.
skills: [gt_t4_dinh_nghia_dao_ham, gt_t4_quy_tac_tinh, gt_t4_day_chuyen, gt_t4_ham_nguoc_tham_so, gt_t4_vi_phan_cap_cao]
---
## Đạo hàm theo định nghĩa

:::hook
Đồng hồ tốc độ xe máy chỉ vận tốc ngay lúc này, không phải vận tốc trung bình cả chuyến. Đạo hàm chính là con số đó: tốc độ thay đổi tại đúng một điểm.
:::

:::figure plane
caption: Dây cung AB có hệ số góc (f(1 + h) - f(1))/h. Cho h -> 0, B trượt về A, dây cung quay thành tiếp tuyến.
size: 200 120
x: -0.5 3 1
y: -1 6 1
curve "x^2" xanh "y = x^2" pos=w
segment 1 1 2 4 xam dash "dây cung"
tangent "x^2" 1 do "tiếp tuyến" pos=sw
point 1 1 muc "A" pos=se
point 2 4 muc "B" pos=e
:::

:::core
Đạo hàm f'(a) là hệ số góc của tiếp tuyến tại a: x nhích thêm một chút thì f đổi gấp f'(a) lần chừng đó.
:::

$$ f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h} $$

Ví dụ: f(x) = x^2 - x, tính f'(3) bằng định nghĩa.

1. f(3 + h) - f(3) = (3 + h)^2 - (3 + h) - 6 = 5h + h^2.
2. Chia cho h (h khác 0): được 5 + h.
3. Cho h -> 0: f'(3) = 5.

Biết hệ số góc thì viết được tiếp tuyến tại điểm (a, f(a)):

$$ y = f'(a)(x - a) + f(a) $$

f có đạo hàm tại a khi giới hạn trên tồn tại hữu hạn. Có đạo hàm thì liên tục, nhưng ngược lại thì không: |x| liên tục tại 0 mà đồ thị gãy góc, tỉ số |h|/h bằng 1 bên phải và -1 bên trái.

> Lỗi thường gặp: thay h = 0 khi h còn ở mẫu, ra 0/0. Rút gọn cho hết h ở mẫu trước, rồi mới cho h -> 0.

:::check
Q: Nhìn hình: tiếp tuyến của y = x^2 tại A(1, 1) có hệ số góc bao nhiêu?
A: 2. Tỉ số số gia là 2 + h, cho h -> 0 được 2; tiếp tuyến là y = 2x - 1.
:::

## Quy tắc tính đạo hàm

:::hook
Doanh thu bằng giá nhân số lượng. Khi cả giá lẫn số lượng cùng đổi, doanh thu đổi nhanh cỡ nào? Quy tắc tích trả lời ngay, không phải quay về định nghĩa.
:::

:::figure plane
caption: u và v cùng lớn thêm: diện tích u.v được thêm hai dải v.du và u.dv. Góc du.dv quá nhỏ, bỏ được.
size: 200 110
axes: off
x: -0.7 4.2
y: -0.6 3.2
poly 0 0 3 0 3 2 0 2 xanh "u.v"
poly 3 0 4 0 4 2 3 2 vang "v.du"
poly 0 2 3 2 3 3 0 3 luc "u.dv"
poly 3 2 4 2 4 3 3 3 do "du.dv"
text 1.5 -0.3 "u"
text 3.5 -0.3 "du"
text -0.35 1 "v"
text -0.35 2.5 "dv"
:::

:::core
Đạo hàm của tích không phải tích các đạo hàm: mỗi thừa số lần lượt đổi trong khi thừa số kia đứng yên, rồi cộng hai phần lại.
:::

:::figure grid
caption: Bảng đạo hàm cơ bản, trên tập xác định của từng hàm.
table
head "f(x)" "f'(x)"
row "x^n" "n x^(n-1)"
row "e^x" "e^x"
row "ln x" "1/x"
row "sin x" "cos x"
row "cos x" "-sin x"
:::

Tổng, hiệu và tích với hằng số thì lấy đạo hàm từng phần. Thương có quy tắc riêng; trong tử số, u'v đứng trước, đảo lại thì sai dấu.

Ví dụ: tính đạo hàm của f(x) = x . e^x.

1. Đặt u = x, v = e^x; khi đó u' = 1, v' = e^x.
2. (uv)' = u'v + uv' = 1 . e^x + x . e^x.
3. Gom lại: f'(x) = (x + 1) e^x.

$$ (uv)' = u'v + uv', \qquad \left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2} $$

> Lỗi thường gặp: viết (uv)' = u'v'. Thử với u = v = x: (x . x)' = (x^2)' = 2x, còn u'v' chỉ bằng 1.

:::check
Q: Tính đạo hàm của x^3 . sin x.
A: 3x^2 sin x + x^3 cos x.
:::

## Quy tắc dây chuyền

:::hook
Mạng nơ-ron là một chuỗi hàm nối nhau. Muốn học, máy phải biết đầu ra đổi bao nhiêu khi một trọng số ở đầu chuỗi nhích đi: đó là quy tắc dây chuyền, gọi là lan truyền ngược.
:::

:::figure flow
caption: x nhích dx thì u nhích 3 dx, rồi y nhích cos u . 3 dx. Tốc độ dọc chuỗi nhân với nhau: (sin 3x)' = cos 3x . 3.
box "x"
link "u' = 3"
box "u = 3x" xanh
link "dy/du = cos u"
box "y = sin u" luc
:::

:::core
Đạo hàm của hàm hợp là tích các tốc độ dọc chuỗi: đạo hàm hàm ngoài, lấy tại hàm trong, nhân đạo hàm hàm trong.
:::

$$ \big(f(g(x))\big)' = f'(g(x)) \cdot g'(x) $$

Ví dụ: tính đạo hàm của f(x) = (3x + 1)^4.

1. Hàm trong u = 3x + 1, hàm ngoài là u^4.
2. Đạo hàm ngoài theo u: 4u^3. Đạo hàm trong: u' = 3.
3. Nhân lại: f'(x) = 4(3x + 1)^3 . 3 = 12(3x + 1)^3.

Nhiều lớp thì nhân hết, từ ngoài vào trong: sin^2(3x) = (sin 3x)^2 có đạo hàm 2 sin 3x . cos 3x . 3.

> Lỗi thường gặp: quên nhân đạo hàm hàm trong, như viết (e^(x^2))' = e^(x^2). Lấy xong đạo hàm ngoài, luôn hỏi: hàm trong là gì, đã nhân đạo hàm của nó chưa?

:::check
Q: Tính đạo hàm của cos(x^2).
A: -sin(x^2) . 2x = -2x sin(x^2).
:::

## Đạo hàm của hàm ngược và hàm cho bởi tham số

:::hook
Đổi độ C ra độ F là nhân 1.8 rồi cộng 32. Chiều đi nhanh gấp 1.8 thì chiều về phải chậm đúng 1.8 lần: đạo hàm của hàm ngược là nghịch đảo.
:::

:::figure plane
caption: y = x^2 và hàm ngược y = sqrt(x) đối xứng qua y = x. Tiếp tuyến tại hai điểm đối xứng có hệ số góc 3 và 1/3.
size: 140 120
aspect: equal
x: 0 3 1
y: 0 3 1
line 0 0 1 1 xam dash "y = x" pos=sw
curve "x^2" xanh "f"
curve "sqrt(x)" luc "f^-1" pos=se
tangent "x^2" 1.5 do len=22
tangent "sqrt(x)" 2.25 do len=22
point 1.5 2.25 do "k = 3" pos=w
point 2.25 1.5 do "k = 1/3" pos=se
:::

:::core
Lật đồ thị qua đường y = x thì hệ số góc thành nghịch đảo: đạo hàm của hàm ngược tại y0 = f(x0) bằng 1/f'(x0).
:::

$$ (f^{-1})'(y_0) = \frac{1}{f'(x_0)} $$

Ví dụ: f(x) = x^5 + x tăng ngặt. Tính (f^(-1))'(2).

1. Tìm x0 với f(x0) = 2: thử x0 = 1, có f(1) = 1 + 1 = 2.
2. f'(x) = 5x^4 + 1, nên f'(1) = 6.
3. (f^(-1))'(2) = 1/f'(1) = 1/6, không cần công thức của f^(-1).

Đường cong cho bởi tham số x = x(t), y = y(t) cũng làm theo tỉ số tốc độ: dy/dx = y'(t)/x'(t), khi x'(t) khác 0. Ví dụ x = t^2, y = t^3 tại t = 1: dy/dx = 3/2.

$$ \frac{dy}{dx} = \frac{y'(t)}{x'(t)} \quad (x'(t) \ne 0) $$

> Lỗi thường gặp: lấy f' tại y0 thay vì tại x0, và lật tỉ số thành x'(t)/y'(t).

:::check
Q: Đường cong x = t^2 + t, y = t^3. Tính dy/dx tại t = 1.
A: y'(1) = 3, x'(1) = 2 + 1 = 3, nên dy/dx = 3/3 = 1.
:::

## Vi phân và đạo hàm cấp cao

:::hook
Tính sqrt(25.2) không cần máy: đi dọc tiếp tuyến thay vì dọc đường cong. Mỗi bước gradient descent trong máy học cũng tin vào đúng phép xấp xỉ này.
:::

:::figure plane
caption: Từ x = 1 đi thêm dx = 1. Theo tiếp tuyến, y tăng dy = 2; theo đường cong, tăng 3. Đoạn tím dx^2 = 1 teo rất nhanh khi dx nhỏ lại.
size: 210 120
x: 0 3 1
y: 0 5 1
curve "x^2" xanh "y = x^2" pos=w
tangent "x^2" 1 do "tiếp tuyến" pos=sw
segment 1 1 2 1 xam dash
segment 2 1 2 3 luc "dy = 2" pos=e
segment 2 3 2 4 tim
text 1.5 1 "dx = 1" pos=s
point 1 1 muc
:::

:::core
Vi phân dy = f'(x) dx là phần thay đổi đi theo tiếp tuyến. Khi dx nhỏ, nó gần bằng phần thay đổi thật của f.
:::

$$ f(x_0 + dx) \approx f(x_0) + f'(x_0)\, dx $$

Ví dụ: tính gần đúng sqrt(25.2).

1. Chọn x0 = 25 (vì sqrt(25) = 5) và dx = 0.2.
2. f(x) = sqrt(x) có f'(x) = 1/(2 sqrt(x)), nên f'(25) = 1/10.
3. sqrt(25.2) xấp xỉ 5 + (1/10) . 0.2 = 5.02.

Đạo hàm cấp hai f'' là đạo hàm của f': tốc độ của tốc độ, như gia tốc. Lặp n lần được f^(n); chẳng hạn x^n lấy đạo hàm n lần ra n!, thêm một lần nữa ra 0.

$$ (e^{ax})^{(n)} = a^n e^{ax}, \qquad \left(\frac{1}{x}\right)^{(n)} = \frac{(-1)^n n!}{x^{n+1}} $$

> Lỗi thường gặp: quên nhân dx, ra sqrt(25.2) xấp xỉ 5.1. Bình phương lại để thử: 5.1^2 = 26.01, quá xa 25.2.

:::check
Q: f(x) = x^3. Tính f''(2) và vi phân df tại x = 2.
A: f''(x) = 6x nên f''(2) = 12; df = 3x^2 dx = 12 dx.
:::
