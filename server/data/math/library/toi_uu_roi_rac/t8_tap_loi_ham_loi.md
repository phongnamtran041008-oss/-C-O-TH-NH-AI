---
id: tr_lib_t8
title_vi: Bài toán tối ưu, tập lồi và hàm lồi
subject: toi_uu_roi_rac
floor: 8
format: 2
summary_vi: Viết bài toán thành biến, mục tiêu và ràng buộc; nhận ra tập lồi (đoạn nối hai điểm không ra ngoài) và hàm lồi (dây cung nằm trên đồ thị); dùng gradient bằng 0 và ma trận Hesse; và hiểu vì sao với bài toán lồi, đáy thung lũng nào tìm được cũng là đáy thấp nhất.
skills: [tr_t8_bai_toan_toi_uu, tr_t8_tap_loi, tr_t8_ham_loi, tr_t8_dieu_kien_toi_uu, tr_t8_bai_toan_loi]
---
## Phát biểu bài toán tối ưu

:::hook
Huấn luyện mô hình học máy là tối ưu: biến là các trọng số, mục tiêu là hàm mất mát cần nhỏ nhất.
:::

:::figure flow
caption: Mô hình của ví dụ dưới: ba phần của mọi bài toán tối ưu.
box "biến: x, y gam" xanh
link "chọn sao cho"
box "min 5x + 4y" vang
link "thỏa"
box "3x + y >= 6, x + 2y >= 4, x, y >= 0" luc
:::

:::core
Tối ưu là chọn biến sao cho hàm mục tiêu nhỏ nhất (bài max f là bài min -f), mà vẫn nằm trong miền ràng buộc.
:::

Ví dụ: linh thảo P có 3 phần mộc khí, 1 phần thủy khí, giá 5 linh thạch mỗi gam; Q có 1 mộc, 2 thủy, giá 4. Cần ít nhất 6 mộc, 4 thủy, tốn ít nhất.

1. Biến: x gam P, y gam Q, với x, y >= 0.
2. Mục tiêu: chi phí 5x + 4y, cần min.
3. Mộc khí lấy từ cả hai loại: 3x + y >= 6. Thủy khí: x + 2y >= 4.

> Lỗi thường gặp: viết ngược chiều ràng buộc ("ít nhất 6" là >= 6), hay ghép một ràng buộc từ hai chất của cùng một loại thảo.

:::check
Q: Ở ví dụ, phương án x = 2, y = 1 có chấp nhận được không? Tốn bao nhiêu?
A: 3 . 2 + 1 = 7 >= 6 và 2 + 2 = 4 >= 4: chấp nhận được. Chi phí 5 . 2 + 4 . 1 = 14 linh thạch.
:::

### Cực tiểu địa phương và toàn cục

:::figure plane
caption: Trên [-2.5, 2], x = 1 là đáy một thung lũng (cực tiểu địa phương), nhưng điểm thấp nhất nằm ở đầu mút x = -2.5.
size: 200 100
x: -2.7 2.3 1
y: -9 3 3
curve "x^3 - 3*x" -2.5 2 xanh
point 1 -2 luc "địa phương" pos=s
point -2.5 -8.125 do "toàn cục" pos=e
point -1 2 muc "cực đại" pos=n
:::

x* là cực tiểu toàn cục khi f(x*) <= f(x) với mọi x trong miền; cực tiểu địa phương chỉ cần điều đó với các x ở gần x*. Toàn cục luôn là địa phương; chiều ngược lại thì không.

Ví dụ: f(x) = x^3 - 3x trên [-2.5, 2].

1. f'(x) = 3x^2 - 3 = 0 tại x = 1 (f = -2) và x = -1 (f = 2).
2. Đầu mút: f(-2.5) = -8.125, f(2) = 2.
3. Nhỏ nhất là -8.125 tại x = -2.5; x = 1 chỉ là cực tiểu địa phương.

> Lỗi thường gặp: trên một đoạn chỉ xét điểm f' = 0 mà quên hai đầu mút.

:::check
Q: Cũng f(x) = x^3 - 3x nhưng trên cả R: x = 1 có còn là cực tiểu địa phương không? Có cực tiểu toàn cục không?
A: x = 1 vẫn là cực tiểu địa phương (f = -2). Nhưng f -> -vô cùng khi x -> -vô cùng, nên không có cực tiểu toàn cục.
:::

## Tập lồi

:::hook
Robot đi thẳng giữa hai điểm bất kỳ trong kho mà không đụng tường: kho đó là tập lồi, không có góc khuất nào để mắc kẹt.
:::

:::figure plane
caption: Lục: lồi, mọi đoạn nối nằm trong. Tím: không lồi, có đoạn nối A, B đi ra ngoài.
size: 360 58
axes: off
x: -3 13
y: 0 4
poly 0.5 0.5 3.5 0.3 4.2 2.4 2.4 3.7 0.6 2.8 luc
segment 1 1 3.4 3 muc
poly 5.5 0.5 9.5 0.5 9.5 3.5 8.3 3.5 8.3 1.6 5.5 1.6 tim
segment 6 1 8.8 3.2 do
point 6 1 do "A" pos=s
point 8.8 3.2 do "B" pos=n
:::

:::core
Tập lồi là tập mà đoạn thẳng nối hai điểm bất kỳ của nó nằm trọn bên trong.
:::

$$ x, y \in D, \; t \in [0, 1] \Rightarrow t x + (1 - t) y \in D $$

- Lồi: cả không gian, nửa mặt phẳng a^T x <= b, hình tròn, phần trên đồ thị một hàm lồi (y >= x^2). Trên đường thẳng, tập lồi chính là một khoảng.
- Giao các tập lồi là lồi: miền ràng buộc của quy hoạch tuyến tính lồi.
- Hợp thường không lồi: [0, 1] hợp [2, 3] thiếu 3/2.

> Lỗi thường gặp: coi {xy >= 1} là lồi. (1, 1) và (-1, -1) thuộc tập, trung điểm (0, 0) thì không. Thêm x > 0 thì mới lồi.

:::check
Q: S = {x thuộc R : x^2 - 5x + 4 >= 0} có lồi không?
A: Nghiệm 1 và 4, nên S = (-vô cùng, 1] hợp [4, +vô cùng). 1 và 4 thuộc S, trung điểm 5/2 thì không: S không lồi.
:::

### Tổ hợp lồi và bao lồi

:::figure plane
caption: P = (1/4)A + (1/4)B + (1/2)C: ba hệ số không âm, tổng 1, nên P nằm trong tam giác. Q cần một hệ số âm.
size: 130 100
x: -0.5 4.5 1
y: -0.5 4.5 1
poly 0 0 4 0 0 4 xanh
point 0 0 muc "A" pos=sw
point 4 0 muc "B" pos=s
point 0 4 muc "C" pos=w
point 1 2 do "P" pos=e
point 3 3 tim "Q" pos=e
:::

Tổ hợp lồi của A, B, C là aA + bB + cC với a, b, c >= 0, a + b + c = 1. Tập mọi tổ hợp lồi (bao lồi) chính là tam giác ABC. Với hai điểm: tA + (1 - t)B, t thuộc [0, 1], là đoạn AB.

Ví dụ: A(0, 0), B(4, 0), C(0, 4), P(1, 2).

1. Hoành độ: 4b = 1, nên b = 1/4. Tung độ: 4c = 2, nên c = 1/2.
2. a = 1 - b - c = 1/4. Cả ba không âm: P trong tam giác.
3. Q(3, 3): b = c = 3/4, a = -1/2 < 0: Q ở ngoài.

Nửa không gian lồi vì a^T(tx + (1 - t)y) = t a^T x + (1 - t) a^T y <= b khi t, 1 - t >= 0; lấy giao thì vẫn lồi.

:::check
Q: A(1, 2), B(7, 5), P(5, 4). Tìm t để P = tA + (1 - t)B. P có nằm trên đoạn AB không?
A: Hoành độ 7 - 6t = 5 và tung độ 5 - 3t = 4 cùng cho t = 1/3, thuộc [0, 1]: P nằm trên đoạn AB.
:::

## Hàm lồi

:::hook
Mất mát bình phương của hồi quy tuyến tính là một cái bát: thả bi ở đâu cũng lăn về cùng một đáy.
:::

:::figure plane
caption: Dây cung đỏ nối hai điểm trên đồ thị y = x^2 luôn nằm trên đồ thị.
size: 150 90
x: -2.5 2.5 1
y: -0.5 5
curve "x^2" xanh
segment -2 4 1 1 do
point -2 4 do
point 1 1 do
:::

:::core
Hàm lồi là hàm có đồ thị cong lên như cái bát: mọi dây cung nằm trên đồ thị.
:::

$$ f(t x + (1 - t) y) \le t f(x) + (1 - t) f(y) $$

- Một biến, khả vi hai lần: f lồi trên khoảng khi f'' >= 0, lõm khi f'' <= 0.
- e^x lồi; ln x lõm; x^3 lõm khi x <= 0, lồi khi x >= 0; |x| lồi dù không có đạo hàm tại 0.

Ví dụ: f(x) = x^4 - 6x^3 + 12x^2 lõm ở đâu?

1. f''(x) = 12(x - 1)(x - 2) <= 0 giữa hai nghiệm: f lõm trên [1, 2], lồi ngoài đoạn đó.

> Lỗi thường gặp: nhớ ngược chiều. Lồi: f(trung bình) <= trung bình các f.

:::check
Q: f(x) = x^4 - 6x^3 + 12x^2. Lấy x = 1 và x = 2: so f(1.5) với trung bình của f(1) và f(2). Điều đó nói gì?
A: f(1) = 7, f(2) = 16, trung bình 11.5; f(1.5) = 11.8125 > 11.5. Đồ thị nằm trên dây cung: f không lồi trên [1, 2], đúng như f'' <= 0 ở đó.
:::

### Nhiều biến: ma trận Hesse

:::matrix
H = 6 4 ; 4 2
:::

Với f(x, y), ma trận Hesse H gồm các đạo hàm riêng cấp hai. f lồi khi H nửa xác định dương tại mọi điểm. Với ma trận 2 x 2 đối xứng:

- nửa xác định dương: hai phần tử chéo >= 0 và det H >= 0;
- xác định dương (lồi chặt): phần tử chéo > 0 và det H > 0.

Tổng, bội dương, cực đại của các hàm lồi là lồi; tích thì không chắc: x và x^2 lồi mà x^3 không.

Ví dụ: f(x, y) = 3x^2 + 4xy + y^2 (ma trận trên).

1. f_xx = 6, f_xy = 4, f_yy = 2.
2. det H = 12 - 16 = -4 < 0: f không lồi.
3. Thử: f(1, -2) = 3 - 8 + 4 = -1 < 0 = f(0, 0). Theo hướng (1, -2), f là parabol quay xuống.

> Lỗi thường gặp: chỉ nhìn đường chéo. Ở đây 6 và 2 đều dương mà f vẫn không lồi.

:::check
Q: f(x, y) = x^2 + kxy + 9y^2. Với những k nào f lồi?
A: H = [2, k; k, 18]. Phần tử chéo dương; cần det H = 36 - k^2 >= 0, tức -6 <= k <= 6.
:::

## Điều kiện tối ưu không ràng buộc

:::hook
Gradient descent dừng khi gradient bằng 0: mặt đất phẳng dưới chân. Nhưng chỗ phẳng có thể là đáy, đỉnh, hay một yên ngựa.
:::

:::figure plane
caption: f(x) = x^3 - 3x: tiếp tuyến nằm ngang tại cả hai điểm dừng, nhưng 1 là đáy còn -1 là đỉnh.
size: 160 90
x: -2.3 2.3 1
y: -3 3 1
curve "x^3 - 3*x" xanh
tangent "x^3 - 3*x" 1 luc len=30
tangent "x^3 - 3*x" -1 do len=30
point 1 -2 luc "x = 1" pos=s
point -1 2 do "x = -1" pos=n
:::

:::core
Gradient bằng 0 chỉ là điều kiện cần; ma trận Hesse cho biết điểm dừng là đáy, đỉnh hay yên ngựa.
:::

1. Điều kiện cần: cực tiểu địa phương (khả vi) thì grad f = 0.
2. Đủ: grad f = 0 và H xác định dương thì là cực tiểu địa phương. H có trị riêng âm và dương (2 x 2: det H < 0) thì là yên ngựa.
3. f lồi: mọi điểm dừng là cực tiểu toàn cục.

Một biến: x^3 có f'(0) = 0 mà 0 không là cực trị (x^3 đổi dấu qua 0).

> Lỗi thường gặp: thấy điểm dừng là gọi "cực tiểu". f(x, y) = x^2 - y^2 có điểm dừng (0, 0), H = [2, 0; 0, -2]: yên ngựa.

:::check
Q: f(x, y) = x^3 - 12x + y^2 có điểm dừng nào, và mỗi điểm là gì?
A: f_x = 3x^2 - 12 = 0 cho x = 2 hoặc -2; f_y = 2y = 0. H = [6x, 0; 0, 2]: tại (2, 0) xác định dương, cực tiểu địa phương; tại (-2, 0) có -12 < 0, yên ngựa.
:::

### Giải hệ gradient bằng 0

Với hàm bậc hai f = ax^2 + bxy + cy^2 + dx + ey, grad f = 0 là hai phương trình bậc nhất: 2ax + by + d = 0 và bx + 2cy + e = 0.

$$ \nabla f(x^*) = 0 $$

Ví dụ: tìm giá trị nhỏ nhất của f(x, y) = x^2 + 2xy + 3y^2 - 4x - 8y.

1. f_x = 2x + 2y - 4 = 0, f_y = 2x + 6y - 8 = 0.
2. Trừ hai phương trình: 4y = 4, nên y = 1, x = 1.
3. H = [2, 2; 2, 6], det H = 8 > 0, chéo dương: f lồi chặt, (1, 1) là cực tiểu toàn cục.
4. Giá trị nhỏ nhất f(1, 1) = 1 + 2 + 3 - 4 - 8 = -6.

> Lỗi thường gặp: kết luận "giá trị nhỏ nhất" khi chưa kiểm tra H. Điểm dừng của hàm không lồi có thể là yên ngựa.

:::check
Q: Tìm điểm dừng và giá trị nhỏ nhất của f(x, y) = x^2 - xy + y^2 - 3x.
A: 2x - y - 3 = 0 và -x + 2y = 0 cho x = 2, y = 1. H = [2, -1; -1, 2], det 3 > 0: nhỏ nhất f(2, 1) = 4 - 2 + 1 - 6 = -3.
:::

## Bài toán tối ưu lồi

:::hook
Mạng nơ-ron có hàm mất mát nhiều thung lũng: gradient descent có thể dừng ở đáy cao. Hồi quy tuyến tính thì lồi: đáy nào tìm được cũng là đáy thấp nhất.
:::

:::figure plane
caption: Lồi (xanh): chỉ một đáy. Không lồi (tím): đáy phải chỉ là cực tiểu địa phương, đáy trái mới thấp nhất.
size: 200 90
x: -2.3 2.3 1
y: -6 5 2
curve "(x - 0.5)^2 - 1" xanh
curve "x^4 - 4*x^2 + x" tim
point -1.47 -5.44 do "toàn cục" pos=e
point 1.35 -2.62 tim "địa phương" pos=se
:::

:::core
Bài toán lồi (min hàm lồi trên tập lồi): cực tiểu địa phương nào cũng là toàn cục.
:::

Lý do: nếu có y trong D với f(y) < f(x*), đi thẳng từ x* về y (vẫn trong D vì D lồi) thì f giảm ngay từ bước đầu (vì f lồi): x* không thể là đáy.

- Lồi: min hàm lồi trên tập lồi; max một hàm lõm.
- Không lồi: max một hàm lồi; miền {x^2 >= 1} (hai nửa đường thẳng); min x^3 trên [-1, 2].

> Lỗi thường gặp: áp "địa phương là toàn cục" cho hàm không lồi, như đường tím trong hình.

:::check
Q: min (x - 1)^2 + y^2 với x^2 + y^2 <= 4 có phải bài toán lồi không? Còn min -x^2 với -1 <= x <= 1?
A: Bài đầu lồi: tổng bình phương lồi, hình tròn lồi. Bài sau không: -x^2 lõm (đó là bài max x^2), cực tiểu ở hai đầu mút.
:::

### Ràng buộc đẩy nghiệm ra biên

:::figure plane
caption: Đáy tự do (3, 3) nằm ngoài miền x + y <= 4 (xanh). Điểm tốt nhất trong miền là hình chiếu (2, 2) lên biên.
size: 130 100
x: -0.5 4.5 1
y: -0.5 4.5 1
poly 0 0 4 0 0 4 xanh
segment 3 3 2 2 do dash
point 3 3 tim "(3, 3)" pos=n
point 2 2 do "(2, 2)" pos=sw
:::

Bài lồi có ràng buộc: nếu cực tiểu tự do vi phạm ràng buộc, nghiệm nằm trên biên. Với hàm khoảng cách bình phương, đó là hình chiếu của điểm tự do lên biên. Ở hình: min (x - 3)^2 + (y - 3)^2 với x + y <= 4 cho (2, 2), giá trị 2.

Ví dụ: min (x - 1)^2 + (x - 5)^2 với x <= 2.

1. Bỏ ràng buộc: f' = 4x - 12 = 0 tại x = 3, nhưng 3 > 2.
2. Trên (-vô cùng, 2], f' < 0 nên f giảm: nghiệm x = 2, f(2) = 1 + 9 = 10.

> Lỗi thường gặp: lấy cực tiểu tự do làm đáp án mà không kiểm tra nó có thỏa ràng buộc.

:::check
Q: min (x - 4)^2 + (y - 1)^2 với x + y <= 3. Nghiệm và giá trị nhỏ nhất?
A: (4, 1) vi phạm vì 5 > 3. Chiếu lên x + y = 3: (4, 1) - 1 . (1, 1) = (3, 0), giá trị 1 + 1 = 2.
:::

### Cực đại của các đường thẳng

:::figure plane
caption: f(x) = max(-2x - 1, x - 1, 3x - 7) là đường gấp khúc lồi (đỏ); đáy tại x = 0, f = -1.
size: 170 85
x: -2 4 1
y: -3 6 1
curve "-2*x - 1" xam
curve "x - 1" xam
curve "3*x - 7" xam
curve "-2*x - 1" -2 0 do
curve "x - 1" 0 3 do
curve "3*x - 7" 3 4 do
point 0 -1 do "đáy" pos=se
:::

Cực đại của các hàm lồi là lồi, nên f = max của vài đường thẳng là một đường gấp khúc lồi. Nó nhỏ nhất tại một điểm gãy: tính f (lấy max cả ba) tại từng giao điểm của hai đường, chọn số nhỏ nhất.

Ví dụ: ở hình, ba giao điểm.

1. -2x - 1 = x - 1 tại x = 0: f = max(-1, -1, -7) = -1.
2. -2x - 1 = 3x - 7 tại x = 6/5: f = 1/5. x - 1 = 3x - 7 tại x = 3: f = 2.
3. Nhỏ nhất: -1, tại x = 0.

:::check
Q: Tìm giá trị nhỏ nhất của f(x) = max(-x + 2, 2x - 7, x/2 - 1).
A: Giao điểm: x = 3 cho f = 1/2; x = 2 cho f = max(0, -3, 0) = 0; x = 4 cho f = 1. Nhỏ nhất 0, tại x = 2.
:::
