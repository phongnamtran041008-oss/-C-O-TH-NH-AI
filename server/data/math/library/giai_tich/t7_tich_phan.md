---
id: gt_lib_t7
title_vi: Tích phân bất định và tích phân xác định
subject: giai_tich
floor: 7
format: 2
summary_vi: Nguyên hàm là đi ngược đạo hàm; đổi biến, từng phần và tách phân thức đưa tích phân lạ về bảng; tích phân xác định là tổng vô số dải mỏng, tính bằng một phép trừ F(b) - F(a).
skills: [gt_t7_nguyen_ham, gt_t7_doi_bien, gt_t7_tung_phan, gt_t7_ham_huu_ty, gt_t7_newton_leibniz, gt_t7_can_bien_thien]
---
## Nguyên hàm và bảng nguyên hàm

:::hook
Biết vận tốc của con thuyền ở từng lúc, muốn biết nó đã trôi tới đâu: phải đi ngược từ đạo hàm về hàm. Đó là lấy nguyên hàm.
:::

:::figure plane
caption: Nguyên hàm x^2 + C của 2x trượt lên xuống; F(1) = 2 chọn đúng một đường.
size: 150 100
x: -2 2 1
y: -1.5 5 1
curve "x^2 - 1" xam
curve "x^2" xam
curve "x^2 + 2" xam
curve "x^2 + 1" do "C = 1" pos=w
point 1 2 do
:::

:::core
Lấy nguyên hàm là đi ngược đạo hàm: tìm F có F' = f. Các nguyên hàm chỉ khác nhau một hằng số, nên luôn kèm + C.
:::

Đọc ngược bảng đạo hàm: x^a cho x^(a+1)/(a+1), 1/x cho ln|x|, sin x cho -cos x. Biến đổi rồi mới tra: sin^2 x = (1 - cos 2x)/2; e^(3x) cho e^(3x)/3.

Ví dụ: F là nguyên hàm của 4x - 1/x^2 trên (0, +vô cùng), F(1) = 5. Tính F(2).

1. Tra bảng từng số hạng: F(x) = 2x^2 + 1/x + C.
2. F(1) = 3 + C = 5, nên C = 2.
3. F(2) = 8 + 1/2 + 2 = 21/2.

> Lỗi thường gặp: cho rằng hai nguyên hàm phải bằng nhau. sin^2 x và -cos^2 x cùng là nguyên hàm của sin 2x, hơn kém nhau đúng 1.

:::check
Q: f''(x) = 6x, f'(0) = 1, f(0) = 2. Tính f(1).
A: f'(x) = 3x^2 + 1 (dùng f'(0) = 1), rồi f(x) = x^3 + x + 2 (dùng f(0) = 2). f(1) = 4. Hai lần lấy nguyên hàm, hai hằng số.
:::

## Phương pháp đổi biến

:::hook
Đổi đơn vị đo cho dễ tính: thay vì đo bằng x, đo bằng u = x^2 + 1. Một tích phân rối co lại thành một dòng tra bảng.
:::

:::figure flow
caption: Dưới dấu tích phân: du = 2x dx nuốt trọn phần 2x dx, chỉ còn u^3 du.
box "2x(x^2 + 1)^3 dx"
link "u = x^2 + 1"
box "u^3 du" xanh
link "tra bảng"
box "u^4/4 + C" luc
link "trả lại x"
box "(x^2 + 1)^4/4 + C" vang
:::

:::core
Thấy một hàm đứng cạnh đạo hàm của nó thì đặt hàm đó là u: du nuốt phần đạo hàm, tích phân co về dạng trong bảng.
:::

Ví dụ: tính tích phân từ 0 đến 1 của x e^(x^2) dx.

1. u = x^2, du = 2x dx, nên x dx = du/2.
2. Đổi cận cùng lúc: x = 0 cho u = 0, x = 1 cho u = 1.
3. (1/2) . tích phân từ 0 đến 1 của e^u du = (e - 1)/2.

Khử căn thì đặt ngược: t = sqrt(x), dx = 2t dt. Hàm lẻ trên [-a, a]: tích phân 0.

> Lỗi thường gặp: đổi biến mà giữ cận cũ. Với u = x^2, cận x = 3 thành u = 9, không phải 3.

:::check
Q: Tính tích phân từ 0 đến 2 của x/(x^2 + 1) dx.
A: u = x^2 + 1 chạy từ 1 đến 5, x dx = du/2: (1/2) . tích phân của du/u = (1/2) ln 5.
:::

## Tích phân từng phần

:::hook
x . e^x là tích của hai thứ khác loại, đổi biến không gỡ được. Từng phần chuyển phép đạo hàm sang thừa số x để nó biến mất.
:::

:::figure grid
caption: x đạo hàm xong chỉ còn 1. Ưu tiên chọn u: ln, arctan, rồi đa thức, rồi lượng giác và mũ.
table
head "bước" "u: đạo hàm" "dv: nguyên hàm"
row "trước" "u = x" "dv = e^x dx"
row "sau" "du = dx" "v = e^x"
mark col 2 xanh
:::

:::core
Từng phần đổi tích phân khó lấy tích phân dễ: u là thừa số đạo hàm xong đơn giản đi (x, ln x), dv là thừa số dễ lấy nguyên hàm (e^x, sin x).
:::

$$ \int u\,dv = uv - \int v\,du, \qquad \int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du $$

Ví dụ: tính tích phân từ 0 đến 1 của x e^x dx.

1. u = x, dv = e^x dx, nên du = dx, v = e^x.
2. [x e^x] từ 0 đến 1 trừ tích phân của e^x: e - (e - 1).
3. Kết quả: 1.

> Lỗi thường gặp: sai dấu ở bước cuối. Nguyên hàm của x cos x là x sin x + cos x: trừ đi -cos x thành cộng.

:::check
Q: Tìm nguyên hàm của ln x. Chọn u và dv thế nào?
A: u = ln x, dv = dx: du = dx/x, v = x. Được x ln x - tích phân của 1 dx = x ln x - x + C.
:::

### Khi tích phân cũ quay lại

:::figure flow
caption: J đứng ở hai vế như một ẩn của phương trình: chuyển vế là giải ra J.
box "J"
link "từng phần hai lần"
box "e^x sin x - e^x cos x - J" xanh
link "chuyển vế"
box "2J = e^x (sin x - cos x)" luc
:::

Có khi tích phân cũ quay lại, và đó là tin tốt. Gọi J là nguyên hàm của e^x sin x. Làm từng phần hai lần (cả hai lần dv = e^x dx) được J = e^x sin x - e^x cos x - J. Chuyển vế, 2J = e^x (sin x - cos x), nên J = e^x (sin x - cos x)/2 + C.

:::check
Q: Gọi K là nguyên hàm của e^x cos x. Làm cùng cách (hai lần dv = e^x dx), K bằng gì?
A: K = e^x cos x + e^x sin x - K, nên K = e^x (sin x + cos x)/2 + C.
:::

## Tích phân hàm hữu tỉ và hàm lượng giác

:::hook
Một phân thức rối thường là vài phân thức đơn giản bị trộn vào nhau. Tách được ra thì mỗi mảnh là một ln hoặc một arctan.
:::

:::figure flow
caption: Mẫu x^2 - 1 = (x - 1)(x + 1) có hai nhân tử: hai mảnh, mỗi mảnh nguyên hàm ra một ln.
box "(3x + 1)/(x^2 - 1)"
link "tách"
box "2/(x - 1) + 1/(x + 1)" xanh
:::

:::core
Mỗi nhân tử (x - r) của mẫu góp một mảnh A/(x - r): nhân với mẫu, thay x = r là ra A.
:::

Ví dụ: tách (3x + 1)/(x^2 - 1) = A/(x - 1) + B/(x + 1).

1. Nhân với mẫu: 3x + 1 = A(x + 1) + B(x - 1).
2. Thay x = 1: 4 = 2A, nên A = 2.
3. Thay x = -1: -2 = -2B, nên B = 1.

$$ \int \frac{dx}{x^2 + a^2} = \frac{1}{a}\arctan\frac{x}{a} + C $$

Mẫu bậc hai vô nghiệm thì đưa về (x + p)^2 + a^2 rồi dùng arctan: 1/(x^2 + 2x + 5) = 1/((x + 1)^2 + 4) có nguyên hàm (1/2) arctan((x + 1)/2).

> Lỗi thường gặp: quên hệ số 1/a. Nguyên hàm của 1/(x^2 + 9) là (1/3) arctan(x/3).

:::check
Q: Dùng phép tách ở ví dụ, tìm nguyên hàm của (3x + 1)/(x^2 - 1).
A: 2/(x - 1) + 1/(x + 1) có nguyên hàm 2 ln|x - 1| + ln|x + 1| + C.
:::

### Hàm lượng giác

:::figure grid
caption: Ba đường cho hàm lượng giác; đường cuối luôn đi được.
table
head "gặp" "làm"
row "mũ lẻ của sin" "tách sin x dx, đặt u = cos x"
row "ví dụ" "sin^3 x = (1 - cos^2 x) sin x"
row "mũ chẵn" "hạ bậc: sin^2 x = (1 - cos 2x)/2"
row "bí" "t = tan(x/2), dx = 2 dt/(1 + t^2)"
row "khi đó" "sin x = 2t/(1 + t^2)"
row "và" "cos x = (1 - t^2)/(1 + t^2)"
:::

Với t = tan(x/2), mọi phân thức của sin, cos thành phân thức của t, và ta quay về cách tách ở trang trước.

:::check
Q: Tính tích phân từ 0 đến pi của sin^2 x dx.
A: Hạ bậc: sin^2 x = (1 - cos 2x)/2. Phần cos 2x tích phân ra 0 trên [0, pi], còn lại pi/2.
:::

:::check
Q: Đặt t = tan(x/2), tìm nguyên hàm của 1/(1 + cos x).
A: 1 + cos x = 2/(1 + t^2), còn dx = 2 dt/(1 + t^2): thương chỉ còn dt. Nguyên hàm t + C = tan(x/2) + C.
:::

## Tích phân xác định và công thức Newton-Leibniz

:::hook
Quãng đường là tổng của vô số đoạn ngắn vận tốc . thời gian. Newton-Leibniz cộng xong tổng vô hạn ấy chỉ bằng một phép trừ.
:::

:::figure plane
caption: 4 dải mỏng: tổng 2.625, đã sát diện tích thật 8/3.
size: 170 105
x: -0.3 2.3 1
y: -0.4 4.2 1
poly 0 0 0.5 0 0.5 0.0625 0 0.0625 vang
poly 0.5 0 1 0 1 0.5625 0.5 0.5625 vang
poly 1 0 1.5 0 1.5 1.5625 1 1.5625 vang
poly 1.5 0 2 0 2 3.0625 1.5 3.0625 vang
curve "x^2" xanh 0 2.05 "y = x^2" pos=w
:::

:::core
Tích phân là tổng vô số dải mỏng f(x) dx; có nguyên hàm F thì tổng ấy bằng F(b) - F(a).
:::

$$ \int_a^b f(x)\,dx = F(b) - F(a) $$

Trung bình trên [a, b] là tích phân chia (b - a). Tổng (1/n)(f(1/n) + ... + f(n/n)) dần tới tích phân từ 0 đến 1 của f.

Ví dụ: tính tích phân từ 0 đến 3 của |x - 1| dx.

1. x - 1 đổi dấu tại 1: tách đoạn tại đó.
2. Từ 0 đến 1 của (1 - x) dx = 1/2.
3. Từ 1 đến 3 của (x - 1) dx = 2. Tổng: 5/2.

> Lỗi thường gặp: dùng công thức khi f không liên tục trên đoạn. 1/x^2 trên [-1, 1] ra -2 là vô lý: hàm dương mà tích phân âm.

:::check
Q: Giá trị trung bình của x^2 trên [0, 3] là bao nhiêu?
A: Tích phân từ 0 đến 3 của x^2 dx = 9, chia độ dài đoạn 3: được 3.
:::

## Tích phân với cận biến thiên

:::hook
Vòi chảy f(t) lít mỗi phút. Lượng nước tới phút x là tích phân từ 0 đến x của f. Nó đang tăng nhanh cỡ nào? Đúng bằng tốc độ vòi lúc ấy, f(x).
:::

:::figure plane
caption: Kéo cận x thêm dx, diện tích thêm một dải cao f(x).
size: 170 100
x: -0.3 3.2 1
y: -0.3 3.2 1
area "1 + x^2/4" 0 2 xanh "F(x)"
poly 2 0 2.3 0 2.3 2.3225 2 2 do
curve "1 + x^2/4" muc 0 2.9
text 2.15 2.7 "f(x)" do
:::

:::core
F(x) = tích phân từ a đến x của f(t) dt có F'(x) = f(x): diện tích tăng theo cận trên với tốc độ bằng chiều cao đường cong tại đó.
:::

$$ \frac{d}{dx}\int_{u(x)}^{v(x)} f(t)\,dt = f\big(v(x)\big)\,v'(x) - f\big(u(x)\big)\,u'(x) $$

F' = f: biết F tăng, giảm ở đâu mà khỏi tính F; tử là tích phân, dạng 0/0 thì L'Hospital.

Ví dụ: F(x) = tích phân từ x đến 2x của t^2 dt. Tính F'(1).

1. Cận trên 2x có đạo hàm 2, cận dưới x có đạo hàm 1.
2. F'(x) = (2x)^2 . 2 - x^2 . 1 = 7x^2.
3. F'(1) = 7.

> Lỗi thường gặp: quên nhân đạo hàm của cận. Tích phân từ 0 đến x^2 của cos t dt có đạo hàm 2x cos(x^2).

:::check
Q: G(x) = tích phân từ 0 đến x của (t - 2) e^t dt đạt cực tiểu tại đâu?
A: G'(x) = (x - 2) e^x, đổi - sang + tại x = 2: cực tiểu tại x = 2.
:::
