---
id: gt_lib_t6
title_vi: Đơn điệu, cực trị và khảo sát hàm số
subject: giai_tich
floor: 6
format: 2
summary_vi: Dấu của f' cho biết đồ thị đi lên hay đi xuống và dừng ở đâu, dấu của f'' cho biết nó cong lên hay cong xuống; thêm tiệm cận là phác được cả đồ thị và đếm được nghiệm.
skills: [gt_t6_don_dieu, gt_t6_cuc_tri, gt_t6_gtln_gtnn, gt_t6_loi_lom, gt_t6_tiem_can, gt_t6_khao_sat]
---
## Tính đơn điệu

:::hook
Đường loss khi huấn luyện: chỉ cần biết độ dốc âm hay dương ở từng đoạn là biết loss đang giảm hay tăng, không phải tính từng điểm.
:::

:::figure plane
caption: f' = 3(x - 1)(x + 1): dương thì đồ thị đi lên, âm thì đi xuống.
size: 170 100
x: -2.4 2.4 1
y: -3 3 1
curve "x^3 - 3*x" luc -2.2 -1
curve "x^3 - 3*x" do -1 1
curve "x^3 - 3*x" luc 1 2.2
text -1.9 2.3 "f' > 0" luc
text 0.6 1.3 "f' < 0" do
text 1.75 -1.9 "f' > 0" luc
:::

:::core
Dấu của f' là chiều đi của f: f' > 0 trên cả một khoảng thì f tăng trên khoảng đó, f' < 0 thì f giảm.
:::

Bậc ba đồng biến trên cả R khi f' >= 0 với mọi x, tức tam thức f' có biệt thức <= 0. f' > 0 khắp nơi thì f(x) = 0 có nhiều nhất một nghiệm.

Ví dụ: tìm các khoảng tăng, giảm của f(x) = 2x^3 - 3x^2 - 12x.

1. f'(x) = 6x^2 - 6x - 12 = 6(x + 1)(x - 2), bằng 0 tại -1 và 2.
2. Thử một số ở giữa: f'(0) = -12 < 0; hai bên ngoài thì f' > 0.
3. f tăng trên (-vô cùng, -1] và [2, +vô cùng), giảm trên [-1, 2].

> Lỗi thường gặp: gộp hai khoảng rời nhau. 1/x giảm trên từng khoảng (-vô cùng, 0) và (0, +vô cùng), nhưng f(-1) < f(1).

:::check
Q: x^3 tăng ngặt trên R, vậy mà f'(0) = 0. Điều đó có mâu thuẫn gì không?
A: Không. f' > 0 thì f tăng, nhưng tăng ngặt chỉ cho f' >= 0: f' được phép chạm 0 tại vài điểm rời nhau.
:::

## Cực trị

:::hook
Huấn luyện mô hình là đi tìm đáy của hàm loss. Ở đáy, mặt đất phẳng: độ dốc bằng 0. Nhưng chỗ phẳng chưa chắc đã là đáy.
:::

:::figure plane
caption: Lên rồi xuống (f' đổi + sang -) là đỉnh; xuống rồi lên là đáy.
size: 170 100
x: -2.4 2.4 1
y: -3.4 3.4 1
curve "x^3 - 3*x" xanh -2.2 2.2
point -1 2 do "cực đại" pos=n
point 1 -2 luc "cực tiểu" pos=s
:::

:::core
Cực trị nằm nơi f' đổi dấu: + sang - là đỉnh, - sang + là đáy; f' = 0 mà không đổi dấu thì không phải cực trị.
:::

Cách khác: f'(x0) = 0 mà f''(x0) < 0 thì đỉnh, > 0 thì đáy, = 0 thì chưa biết. |x| có đáy tại 0 dù f'(0) không tồn tại.

Ví dụ: tìm cực trị của f(x) = x^3 - 6x^2 + 9x + 1.

1. f'(x) = 3x^2 - 12x + 9 = 3(x - 1)(x - 3).
2. f' đổi + sang - tại 1, đổi - sang + tại 3.
3. Cực đại f(1) = 5, cực tiểu f(3) = 1.

> Lỗi thường gặp: thấy f'(a) = 0 là kết luận có cực trị. x^3 có f'(0) = 0 mà vẫn đi lên qua 0: không có cực trị.

:::check
Q: f'(x) = (x - 1)^2 (x + 2). f có bao nhiêu điểm cực trị, là loại gì?
A: Một: cực tiểu tại x = -2 (f' đổi - sang +). Qua nghiệm kép 1, f' không đổi dấu.
:::

## Giá trị lớn nhất và nhỏ nhất trên đoạn

:::hook
Chỉnh learning rate trong khoảng cho phép [0.001, 0.1]: giá trị tốt nhất có thể nằm ở một đáy bên trong, cũng có thể nằm ngay mép khoảng.
:::

:::figure plane
caption: Trên [0, 2]: thấp nhất ở đáy x = 1, cao nhất ở đầu mút x = 2.
size: 170 100
x: -0.4 2.4 1
y: -2.5 2.5 1
curve "x^3 - 3*x" xanh 0 2
drop 2 2
point 0 0 muc
point 2 2 do "GTLN" pos=w
point 1 -2 luc "GTNN" pos=e
:::

:::core
Trên một đoạn, GTLN và GTNN nằm ở điểm tới hạn bên trong hoặc ở hai đầu mút: tính hết rồi so.
:::

Khoảng mở thì có thể không đạt: x trên (0, 1) không chạm 1. x + 9/x trên (0, +vô cùng) nhỏ nhất là f(3) = 6, không có lớn nhất.

Ví dụ: GTLN, GTNN của f(x) = x^3 - 3x^2 trên [1, 4].

1. f'(x) = 3x(x - 2): chỉ x = 2 nằm trong (1, 4); bỏ x = 0.
2. Tính: f(1) = -2, f(2) = -4, f(4) = 16.
3. GTLN = 16 tại đầu mút 4, GTNN = -4 tại x = 2.

> Lỗi thường gặp: quên hai đầu mút. Chỉ so điểm tới hạn thì ở ví dụ trên mất GTLN 16.

:::check
Q: Tấm vuông cạnh 6, cắt bốn góc cạnh x, gấp thành hộp không nắp. x nào cho hộp to nhất?
A: V = x(6 - 2x)^2, 0 < x < 3. V' = (6 - 2x)(6 - 6x) = 0 tại x = 1, V' đổi + sang -: x = 1, V = 16.
:::

## Lồi, lõm và điểm uốn

:::hook
Hàm loss lồi như cái bát chỉ có một đáy, gradient descent đi đâu cũng về đó. Vì vậy dân máy học rất quý hàm lồi, và kiểm tra lồi bằng f''.
:::

:::figure plane
caption: Đỏ: f'' < 0, cong xuống. Xanh: f'' > 0, cong lên, nằm trên tiếp tuyến.
size: 170 100
x: -1.2 3.2 1
y: -2.5 2.5 1
curve "x^3 - 3*x^2 + 2" do -1 1
curve "x^3 - 3*x^2 + 2" xanh 1 3
tangent "x^3 - 3*x^2 + 2" 2.3 xam len=34
point 1 0 muc "uốn" pos=ne
text 0.8 1.9 "lõm" do
text 2.8 -1.6 "lồi" xanh
:::

:::core
f'' đo độ cong: f'' > 0 thì đồ thị cong lên (lồi, như cái bát), f'' < 0 thì cong xuống (lõm); điểm uốn là nơi f'' đổi dấu.
:::

Hàm bậc bốn có y'' là tam thức: hai nghiệm phân biệt thì có hai điểm uốn, biệt thức <= 0 thì y'' không đổi dấu, không có điểm uốn.

Ví dụ: tìm điểm uốn của y = x^3 + 3x^2 - 1.

1. y' = 3x^2 + 6x, y'' = 6x + 6.
2. y'' = 0 tại x = -1 và đổi dấu qua đó.
3. Tung độ lấy từ y: y(-1) = 1. Điểm uốn (-1, 1).

> Lỗi thường gặp: thấy f''(a) = 0 là kết luận có điểm uốn. x^4 có f''(0) = 0 nhưng f'' >= 0 hai bên: cong lên suốt.

:::check
Q: Đồ thị y = x^4 - 24x^2 cong xuống (lõm) trên khoảng nào?
A: y'' = 12x^2 - 48 = 12(x - 2)(x + 2) < 0 khi -2 < x < 2: lõm trên (-2, 2).
:::

## Tiệm cận

:::hook
Độ chính xác của mô hình tăng dần khi thêm dữ liệu nhưng không vượt nổi một trần. Cái trần ấy là một tiệm cận: đồ thị bám sát mãi mà không chạm.
:::

:::figure plane
caption: x + 1/(x - 1): phần 1/(x - 1) vọt lên gần x = 1, tắt dần ở xa, còn lại y = x.
size: 170 105
x: -3 5 1
y: -3 6 1
curve "x + 1/(x - 1)" xanh
line 1 0 1 1 xam dash
line 0 0 1 1 do dash
text 1.8 -2.3 "x = 1" xam
text -1.6 0.6 "y = x" do
:::

:::core
Tiệm cận là đường thẳng đồ thị bám sát mãi: đứng ở nơi f phóng ra vô cùng, ngang hoặc xiên khi f(x) - (px + q) -> 0 lúc x -> vô cùng.
:::

Với (ax + b)/(cx + d): đứng x = -d/c, ngang y = a/c. Không chia đa thức được thì tính p = lim f(x)/x, rồi q = lim (f(x) - px).

Ví dụ: tiệm cận của y = (2x^2 + x)/(x - 1).

1. Mẫu bằng 0 tại 1, tử bằng 3 khác 0: tiệm cận đứng x = 1.
2. Chia đa thức: 2x^2 + x = (x - 1)(2x + 3) + 3.
3. y = 2x + 3 + 3/(x - 1), phần dư -> 0: tiệm cận xiên y = 2x + 3.

> Lỗi thường gặp: chỉ kiểm f(x)/x -> p. x + sin x có f(x)/x -> 1 nhưng f(x) - x = sin x dao động mãi: không có tiệm cận xiên.

:::check
Q: y = (x^2 + 2x)/(x + 2) có tiệm cận đứng x = -2 không?
A: Không. Với x khác -2, y = x, nên y -> -2, hữu hạn: chỉ là một lỗ trên đường thẳng.
:::

## Lược đồ khảo sát hàm số

:::hook
Đếm nghiệm của -x^3 + 3x^2 = m mà không cần giải: phác dáng đồ thị rồi kéo một đường ngang. Khảo sát là phác được dáng ấy từ vài con số.
:::

:::figure plane
caption: Đường ngang cắt 3 lần giữa hai giá trị cực trị, 2 lần khi chạm đỉnh, 1 lần ở ngoài.
size: 170 105
x: -1.5 3.5 1
y: -1 6 1
curve "-x^3 + 3*x^2" xanh
line 0 2 1 2 luc dash
line 0 4 1 4 do dash
line 0 5 1 5 xam dash
point 2 4 do
point 0 0 do
:::

:::core
Biết đồ thị lên, xuống ở đâu và dừng ở độ cao nào là đếm được số giao điểm với mọi đường ngang y = m.
:::

Lược đồ: tập xác định; f' và bảng biến thiên; f'' và điểm uốn; tiệm cận; vài điểm. Hàm lẻ: đối xứng qua O.

Ví dụ: với m nào thì -x^3 + 3x^2 = m có ba nghiệm phân biệt?

1. f'(x) = -3x(x - 2): f giảm, tăng trên [0, 2], rồi giảm.
2. Cực tiểu f(0) = 0, cực đại f(2) = 4.
3. Ba nghiệm khi 0 < m < 4; m = 0 hay 4: hai nghiệm; còn lại: một.

> Lỗi thường gặp: coi m bằng đúng giá trị cực trị là có ba nghiệm. Đường ngang chỉ chạm đỉnh: hai nghiệm.

:::check
Q: x + 1/x có cực đại f(-1) = -2, cực tiểu f(1) = 2. Sao đỉnh lại thấp hơn đáy?
A: Hai điểm nằm trên hai nhánh, ngăn bởi tiệm cận đứng x = 0. Cực trị chỉ so với các điểm ở gần nó.
:::
