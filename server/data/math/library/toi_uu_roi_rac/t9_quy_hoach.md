---
id: tr_lib_t9
title_vi: Quy hoạch tuyến tính và quy hoạch phi tuyến
subject: toi_uu_roi_rac
floor: 9
format: 2
summary_vi: Quy hoạch tuyến tính là cắt mặt phẳng bằng các ràng buộc rồi đẩy đường mục tiêu tới một đỉnh; đơn hình đi từ đỉnh sang đỉnh, đối ngẫu định giá từng tài nguyên. Phần phi tuyến: nhân tử Lagrange, điều kiện KKT, và hạ gradient trên hàm mất mát.
skills: [tr_t9_mo_hinh_qhtt, tr_t9_hinh_hoc, tr_t9_don_hinh, tr_t9_doi_ngau, tr_t9_lagrange_kkt, tr_t9_gradient_descent]
---
## Mô hình quy hoạch tuyến tính

:::hook
Lò luyện đan có hạn giờ lửa và linh thảo; mỗi loại đan tốn một ít và lãi một ít. Luyện bao nhiêu mẻ mỗi loại để lãi nhất? Mọi thứ đều tỉ lệ thuận: đó là quy hoạch tuyến tính.
:::

:::figure grid
caption: Mỗi hàng tài nguyên thành một ràng buộc: hệ số lấy từ cả hai loại đan, vế phải là cột "có".
table
head "đan A" "đan B" "có"
side "giờ lửa" "linh thảo" "lò B" "lãi"
row 1 1 4
row 2 1 6
row 0 1 3
row 3 2 -
mark row 4 vang
:::

:::core
Quy hoạch tuyến tính: mục tiêu và mọi ràng buộc đều là tổng có hệ số của các biến. Mỗi tài nguyên có hạn là một ràng buộc.
:::

Ví dụ: đọc bảng, gọi x, y là số mẻ đan A, B.

1. Biến: x, y >= 0. Mục tiêu: max 3x + 2y.
2. Giờ lửa: x + y <= 4. Linh thảo: 2x + y <= 6. Lò B chỉ luyện tối đa 3 mẻ: y <= 3.

$$ \max c^T x, \quad A x \le b, \; x \ge 0 $$

> Lỗi thường gặp: viết "=" khi đề nói "không vượt quá" (không bắt buộc dùng hết), viết ngược chiều "ít nhất" (là >=), hay lấy một hàng hệ số từ một loại đan.

:::check
Q: Thêm yêu cầu "phải luyện ít nhất 1 mẻ đan A". Ràng buộc mới viết thế nào?
A: x >= 1. "Ít nhất" là >=, và chỉ liên quan tới biến x.
:::

### Dạng chính tắc

:::figure grid
caption: Dạng chính tắc: chỉ có đẳng thức và biến không âm.
table
head "có" "đổi thành"
row "a^T x <= b" "a^T x + s = b, s >= 0"
row "a^T x >= b" "a^T x - s = b, s >= 0"
row "x_j <= 0" "x_j = -x_j', x_j' >= 0"
row "x_j tự do" "x_j = x_j' - x_j''"
row "max f" "min (-f), đổi dấu kết quả"
:::

Mỗi bất đẳng thức thêm một biến bù; biến tự do tách thành hiệu hai biến không âm. Ràng buộc đẳng thức giữ nguyên.

Ví dụ: max x1 + 2x2 - x3 với x1 - x2 <= 4, x2 + x3 >= 1; x1 tự do, x2 >= 0, x3 <= 0.

1. x1 = x1' - x1'' (2 biến), x2 giữ nguyên, x3 = -x3' (1 biến).
2. Hai bất đẳng thức thêm s1, s2: tổng 6 biến, 2 ràng buộc đẳng thức.

:::check
Q: Bài có 3 biến đều không âm và 2 ràng buộc <=, 1 ràng buộc =. Dạng chính tắc có bao nhiêu biến, bao nhiêu đẳng thức?
A: Thêm 2 biến bù cho 2 bất đẳng thức: 3 + 2 = 5 biến, 3 ràng buộc đẳng thức.
:::

## Phương pháp hình học hai biến

:::hook
Đường "lãi = hằng số" là một đường thẳng. Kéo nó song song ra xa cho lãi tăng dần: lần cuối nó còn chạm miền chấp nhận được là ở một góc.
:::

:::figure plane
caption: Miền lục là các phương án. Đường lãi 3x + 2y trượt song song từ 6 (xám) ra 10 (đỏ), rời miền tại đỉnh (2, 2).
size: 180 110
x: -0.5 4 1
y: -0.5 5.2 1
poly 0 0 3 0 2 2 1 3 0 3 luc
segment 0 3 2 0 xam dash
segment 0 5 3.333 0 do dash
point 2 2 do "(2, 2)" pos=ne
:::

:::core
Miền ràng buộc là một đa giác lồi; mục tiêu tuyến tính không có đáy hay đỉnh bên trong, nên tốt nhất luôn đạt ở một đỉnh.
:::

Nếu miền khác rỗng và bị chặn thì bài toán có nghiệm tối ưu, và có một nghiệm là đỉnh. Hai đỉnh kề cùng tốt nhất thì cả cạnh nối chúng tối ưu.

> Lỗi thường gặp: cho đạo hàm bằng 0 để tìm điểm trong miền. Hàm tuyến tính có gradient khác 0 ở mọi nơi.

:::check
Q: Đổi mục tiêu thành max x + y trên cùng miền. Đỉnh nào tốt nhất?
A: Giá trị ở năm đỉnh 0, 3, 4, 4, 3: hai đỉnh kề (2, 2) và (1, 3) cùng đạt 4, nên cả cạnh nối chúng đều tối ưu.
:::

### Tìm đỉnh, ràng buộc chặt và lỏng

:::figure grid
caption: Lãi z = 3x + 2y ở năm đỉnh của miền; lớn nhất ở (2, 2).
table
side "đỉnh" "z"
row "(0, 0)" "(3, 0)" "(2, 2)" "(1, 3)" "(0, 3)"
row 0 9 10 9 6
mark col 3 vang
:::

1. Vẽ đường biên mỗi ràng buộc, chọn nửa mặt phẳng thỏa nó.
2. Giao các nửa mặt phẳng: miền D, một đa giác lồi.
3. Tìm các đỉnh: giao của hai đường biên mà thỏa mọi ràng buộc còn lại.
4. Tính mục tiêu ở từng đỉnh, chọn đỉnh tốt nhất.

Tại (2, 2): x + y = 4 và 2x + y = 6 chặt (dùng hết tài nguyên); y = 2 < 3 nên y <= 3 lỏng (còn dư 1).

> Lỗi thường gặp: lấy giao điểm của hai đường biên mà quên kiểm tra nó có thỏa các ràng buộc khác. Giao của x + y = 4 và y = 3 là (1, 3), hợp lệ; giao của 2x + y = 6 và y = 3 là (1.5, 3), vi phạm x + y <= 4.

:::check
Q: Thêm ràng buộc x <= 1.5. Đỉnh (2, 2) còn hợp lệ không? Nghiệm mới là gì?
A: Không, 2 > 1.5. Đỉnh mới (1.5, 2.5) cho z = 4.5 + 5 = 9.5, lớn hơn (1, 3) với 9: nghiệm mới (1.5, 2.5).
:::

## Phương pháp đơn hình

:::hook
Hàng nghìn biến thì không vẽ được. Đơn hình làm việc của hình học bằng đại số: từ một đỉnh nhảy sang đỉnh kề tốt hơn.
:::

:::figure plane
caption: Từ (0, 0) lên (3, 0) rồi (2, 2): z = 0, 9, 10.
size: 110 80
x: -0.5 4 1
y: -0.5 3.5 1
poly 0 0 3 0 2 2 1 3 0 3 luc
vector 0 0 3 0 do
vector 3 0 2 2 do
point 2 2 do "z = 10" pos=ne
:::

:::core
Mỗi bước: chọn một biến còn làm z tăng (biến vào), tăng nó đến khi một biến cơ sở chạm 0 (biến ra, tỉ số nhỏ nhất).
:::

Từ vựng viết mỗi biến cơ sở (ban đầu là các biến bù s) theo các biến ngoài cơ sở; cho biến ngoài cơ sở bằng 0 là được một đỉnh. Hết hệ số dương trong z thì đã tối ưu.

:::check
Q: Ở đỉnh (3, 0), từ vựng cho z = 9 + y/2 - 3s2/2. Vì sao chưa tối ưu, và biến nào sẽ vào?
A: Hệ số của y còn dương: tăng y vẫn làm z tăng. y vào cơ sở.
:::

### Một vòng trên từ vựng

Từ vựng ban đầu, biến ngoài cơ sở x = y = 0: s1 = 4 - x - y, s2 = 6 - 2x - y, s3 = 3 - y, z = 3x + 2y.

1. x vào (hệ số 3 lớn nhất). Tỉ số s1: 4, s2: 6/2 = 3; s3 không chứa x. s2 ra: x = 3, z = 9.
2. Rút x = 3 - y/2 - s2/2, thế vào: z = 9 + y/2 - 3s2/2, s1 = 1 - y/2 + s2/2.
3. y vào (hệ số 1/2). Tỉ số: hàng x: 6, s1: 2, s3: 3. s1 ra, y = 2, x = 2.
4. z = 10 - s1 - s2: không còn hệ số dương, tối ưu.

> Lỗi thường gặp: chọn tỉ số lớn nhất, hay lập tỉ số ở hàng mà biến cơ sở tăng khi biến vào tăng. Một biến sẽ thành âm.

:::check
Q: s1 = 6 - 2x1 - x2, s2 = 4 - x2, s3 = 2 - x1 + x2, z = x1 + 3x2. Biến nào vào, biến nào ra, z mới?
A: x2 vào (hệ số 3). Tỉ số s1: 6, s2: 4; s3 tăng khi x2 tăng nên bỏ qua. s2 ra, x2 = 4, z = 12.
:::

## Bài toán đối ngẫu

:::hook
Một thương nhân muốn mua lại hết giờ lửa và linh thảo của lò. Trả mỗi đơn vị bao nhiêu để lò không thiệt so với tự luyện đan, mà tổng tiền ít nhất? Đó là bài đối ngẫu.
:::

:::figure grid
caption: Lật bảng: hàng của bài gốc thành cột của bài đối ngẫu. b thành hệ số mục tiêu, c thành vế phải.
table "gốc"
head x y b
row 1 1 4
row 2 1 6
row 0 1 3
row 3 2 -
mark row 4 vang
op "->"
table "đối ngẫu"
head u v w c
row 1 2 0 3
row 1 1 1 2
row 4 6 3 -
mark row 3 vang
:::

:::core
Đối ngẫu định giá từng tài nguyên. Giá trị bài max không bao giờ vượt bài min; ở tối ưu hai giá trị bằng nhau.
:::

$$ \min b^T y, \quad A^T y \ge c, \; y \ge 0 $$

Ví dụ: đối ngẫu của bài lò đan là min 4u + 6v + 3w với u + 2v >= 3 (giá trị tài nguyên một mẻ A ít nhất bằng lãi 3), u + v + w >= 2, u, v, w >= 0.

- Đối ngẫu yếu: mọi x, y chấp nhận được có c^T x <= b^T y.
- Đối ngẫu mạnh: một bài có nghiệm tối ưu thì bài kia cũng có, và hai giá trị tối ưu bằng nhau.

:::check
Q: Thử u = 2, v = 1, w = 0 có chấp nhận được không? Nó nói gì về lãi của lò?
A: 2 + 2 = 4 >= 3, 2 + 1 = 3 >= 2: được. 4u + 6v + 3w = 14, nên lãi mọi phương án không vượt 14 (thật ra tối ưu là 10).
:::

### Quy tắc lập và độ lệch bù

:::figure map
caption: Bài gốc là bài max: mỗi ràng buộc ứng với một biến đối ngẫu, mỗi biến ứng với một ràng buộc.
col "gốc (max)" "ràng buộc <=" "ràng buộc =" "biến >= 0" "biến tự do"
col "đối ngẫu (min)" "biến >= 0" "biến tự do" "ràng buộc >=" "ràng buộc ="
"ràng buộc <=" -> "biến >= 0"
"ràng buộc =" -> "biến tự do"
"biến >= 0" -> "ràng buộc >="
"biến tự do" -> "ràng buộc ="
:::

Độ lệch bù tại cặp nghiệm tối ưu: ràng buộc gốc lỏng thì biến đối ngẫu của nó bằng 0 (tài nguyên còn dư thì không có giá); biến gốc dương thì ràng buộc đối ngẫu của nó chặt.

Ví dụ: nghiệm gốc (2, 2), y <= 3 lỏng.

1. Lỏng nên w = 0. x, y > 0 nên u + 2v = 3 và u + v + w = 2.
2. Giải: v = 1, u = 1. Kiểm: 4 . 1 + 6 . 1 = 10 = lãi tối ưu.

> Lỗi thường gặp: đảo chiều, cho biến đối ngẫu của ràng buộc lỏng là số dương.

:::check
Q: Lò có thêm nửa giờ lửa (vế phải 4 thành 4.5). Lãi tối ưu tăng bao nhiêu?
A: u . 0.5 = 0.5: biến đối ngẫu u = 1 là giá một giờ lửa. Thật vậy, đỉnh mới (1.5, 3) cho lãi 10.5.
:::

## Nhân tử Lagrange và điều kiện KKT

:::hook
Tối ưu với ngân sách cố định, hay với điều kiện "tổng trọng số bằng 1": chỉ được đi trên đường ràng buộc.
:::

:::figure plane
caption: Đường mức x^2 + y^2 = 5 vừa chạm x + 2y = 5 tại (1, 2); gradient (đỏ) vuông góc với cả hai.
size: 130 85
x: -3 4 1
y: -3 3.5 1
param "sqrt(5)*cos(t)" "sqrt(5)*sin(t)" 0 2*pi xanh
line -1 3 5 0 luc
vector 1 2 1.6 3.2 do
point 1 2 muc "(1, 2)" pos=sw
:::

:::core
Ở nghiệm có ràng buộc, đường mức của f tiếp xúc với ràng buộc: grad f song song grad g, hệ số tỉ lệ là lambda.
:::

$$ L = f - \lambda g, \quad L_x = 0, \; L_y = 0, \; g = 0 $$

Ví dụ: min x^2 + y^2 với x + 2y = 5, tức g = x + 2y - 5.

1. L_x = 2x - lambda = 0, L_y = 2y - 2lambda = 0: x = lambda/2, y = lambda.
2. Thay vào g = 0: lambda/2 + 2lambda = 5, lambda = 2; x = 1, y = 2, f = 5.
3. Nới vế phải thành c: tối ưu là c^2/5, đạo hàm tại c = 5 là 2 = lambda.

> Lỗi thường gặp: quên phương trình g = 0. Chỉ giải grad f = 0 cho (0, 0), không nằm trên đường ràng buộc.

:::check
Q: max xy với x + y = 10 bằng Lagrange: lambda, x, y và giá trị lớn nhất?
A: L_x = y - lambda = 0, L_y = x - lambda = 0, nên x = y = lambda; 2lambda = 10: lambda = 5, x = y = 5, giá trị 25.
:::

### Ràng buộc bất đẳng thức: KKT

:::figure plane
caption: Đáy tự do (2, 1) nằm ngoài miền x + y <= 2: nghiệm là điểm chạm biên (1.5, 0.5), ràng buộc chặt, mu = 1 > 0.
size: 130 100
x: -0.5 3 1
y: -0.5 2.5 1
poly 0 0 2 0 0 2 xanh
segment 2 1 1.5 0.5 do dash
point 2 1 tim "(2, 1)" pos=e
point 1.5 0.5 do "(1.5, 0.5)" pos=sw
:::

Với bài min f, ràng buộc g <= 0, điều kiện KKT tại nghiệm: grad f + mu grad g = 0, mu >= 0, g <= 0 và mu . g = 0. Nghĩa là một trong hai:

- ràng buộc lỏng (g < 0) và mu = 0: nghiệm chính là đáy tự do;
- ràng buộc chặt (g = 0) và mu >= 0: nghiệm nằm trên biên.

Với bài lồi, KKT là điều kiện đủ.

Ví dụ: min (x - 2)^2 + (y - 1)^2 với x + y <= 2, như hình.

1. Đáy tự do (2, 1) có 2 + 1 = 3 > 2: ràng buộc phải chặt.
2. Chiếu (2, 1) lên x + y = 2 được (1.5, 0.5).
3. Từ 2(x - 2) + mu = 0 có mu = 1 >= 0: thỏa KKT.

:::check
Q: min (x + 1)^2 + (y - 2)^2 với x + y <= 0. Nghiệm và mu? Còn nếu ràng buộc là x + y <= 4?
A: (-1, 2) có tổng 1 > 0: chiếu được (-1.5, 1.5), mu = 1. Với x + y <= 4 thì (-1, 2) thỏa: nghiệm chính nó, mu = 0.
:::

## Hạ gradient và hàm mất mát

:::hook
Mọi mạng nơ-ron đều học bằng một vòng lặp: đo độ dốc của hàm mất mát, rồi bước một bước nhỏ xuống dốc. Lặp hàng triệu lần.
:::

:::figure plane
caption: f(x) = x^2, bước học 0.3: mỗi bước x mới = 0.4 x, đi từ 2 xuống 0.8, 0.32, 0.128 về đáy.
size: 170 95
x: -0.5 2.3 0.5
y: -0.3 4.3 1
curve "x^2" xanh
point 2 4 do "x_0" pos=e
point 0.8 0.64 do "x_1" pos=n
point 0.32 0.1024 do "x_2" pos=n
segment 2 4 0.8 0.64 do dash
segment 0.8 0.64 0.32 0.1024 do dash
:::

:::core
Gradient chỉ hướng dốc lên nhanh nhất; đi một bước nhỏ ngược hướng đó thì hàm giảm. Bước học eta quyết định bước dài hay ngắn.
:::

$$ x_{k+1} = x_k - \eta \nabla f(x_k) $$

Ví dụ: f(x, y) = x^2 + 2y^2 - 2x, từ (0, 1), eta = 1/4.

1. grad f = (2x - 2, 4y). Tại (0, 1): (-2, 4).
2. Điểm mới (0 + 1/2, 1 - 1) = (1/2, 0).
3. Tại (1/2, 0): grad (-1, 0), điểm mới (3/4, 0). Đáy thật ở (1, 0).

> Lỗi thường gặp: đi cùng hướng gradient (dấu cộng): đó là leo dốc, f tăng.

:::check
Q: f(x) = (x - 3)^2, từ x0 = 1 với eta = 1/4. Tính x1 và x2.
A: f'(x) = 2(x - 3). x1 = 1 - (1/4)(-4) = 2; x2 = 2 - (1/4)(-2) = 2.5: mỗi bước khoảng cách tới 3 giảm một nửa.
:::

### Bước học quá lớn

:::figure plane
caption: Cùng f = x^2 nhưng eta = 1.1: x mới = -1.2 x, nhảy qua đáy và văng ra xa dần.
size: 170 85
x: -2.2 2.2 1
y: -0.3 4.5 1
curve "x^2" xanh
segment 1 1 -1.2 1.44 do dash
segment -1.2 1.44 1.44 2.0736 do dash
segment 1.44 2.0736 -1.728 2.985984 do dash
point 1 1 do "x_0" pos=e
point -1.728 2.985984 do "x_3" pos=w
:::

Với f(x) = a x^2 (a > 0): x mới = x - eta . 2a x = (1 - 2a eta) x. Dãy về 0 khi |1 - 2a eta| < 1, tức 0 < eta < 1/a.

- eta = 1/(2a): tới đáy ngay một bước.
- eta = 1/a: hệ số -1, nhảy qua lại mãi giữa x0 và -x0.
- eta > 1/a: |hệ số| > 1, phân kỳ, f tăng.

> Lỗi thường gặp: tin rằng mỗi bước hạ gradient đều làm f giảm. Chỉ đúng khi bước đủ nhỏ.

:::check
Q: f(x) = 4x^2. Với eta nào dãy nhảy qua lại giữa 1 và -1? eta = 0.2 thì sao?
A: a = 4, eta = 1/4 cho hệ số -1. eta = 0.2: hệ số 1 - 1.6 = -0.6, vẫn hội tụ (đổi dấu nhưng nhỏ dần).
:::

### Hàm mất mát của mô hình y = wx

:::figure plane
caption: Hai điểm dữ liệu (1, 1), (2, 3) và đường khớp nhất y = 1.4x (đỏ); nét đứt là sai số mà mất mát bình phương cộng lại.
size: 130 95
x: -0.3 2.6 1
y: -0.3 3.6 1
line 0 0 1 1.4 do
point 1 1 xanh
point 2 3 xanh
segment 1 1 1 1.4 muc dash
segment 2 3 2 2.8 muc dash
:::

$$ L(w) = \sum (w x_i - y_i)^2, \quad L'(w) = 2 \sum x_i (w x_i - y_i) $$

L là parabol quay lên (lồi): cực tiểu tại w* = (tổng x_i y_i)/(tổng x_i^2).

Ví dụ: điểm (1, 1), (2, 3), từ w0 = 0, eta = 1/20.

1. L(w) = (w - 1)^2 + (2w - 3)^2, L'(w) = 10w - 14.
2. w1 = 0 - (1/20)(-14) = 7/10. L giảm từ 10 xuống 53/20.
3. w* = 14/10 = 7/5.

:::check
Q: Hai điểm (1, 2), (3, 5). Tính L'(w) và w*.
A: L'(w) = 2(w - 2) + 6(3w - 5) = 20w - 34, nên w* = 17/10 (= tổng x_i y_i / tổng x_i^2 = 17/10).
:::
