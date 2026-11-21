---
id: gt_lib_t10
title_vi: Tài năng: số thực, khả tích, hàm lồi và không gian metric
subject: giai_tich
floor: 10
format: 2
summary_vi: Tầng ẩn dựng lại nền móng: trần thấp nhất của một tập, hai mức mà một dãy dao động bám vào, diện tích kẹp giữa hai bậc thang, dây cung nằm trên hàm lồi, và mọi cách đo khoảng cách.
skills: [gt_t10_tien_de_so_thuc, gt_t10_gioi_han_tren_duoi, gt_t10_kha_tich_riemann, gt_t10_ham_loi, gt_t10_khong_gian_metric]
---
## Tiên đề của tập số thực

:::hook
Độ chính xác qua các vòng: 0.5, 0.67, 0.75, ... sát dần 1 mà không chạm. Mức 1 là trần thấp nhất của cả tập, dù không thuộc tập.
:::

:::figure numberline
caption: Các số 1 - 1/n dồn về 1: sup = 1 nhưng 1 không thuộc tập.
size: 200 45
range: 0 1.2 0.2
seq "1 - 1/n" 1 12 xanh
point 1 do "sup = 1" open
:::

:::core
sup A là trần thấp nhất của A: không phần tử nào vượt nó, nhưng hạ nó xuống chút nào là có phần tử vượt.
:::

$$ s = \mathrm{sup}\,A \iff \big(\forall a \in A:\ a \le s\big) \land \big(\forall \varepsilon > 0\ \exists a \in A:\ a > s - \varepsilon\big) $$

Đây là chỗ R hơn Q. Tập các số hữu tỉ có x^2 < 2 bị chặn trên (bởi 2 chẳng hạn), nhưng cận trên nhỏ nhất của nó là sqrt(2), không hữu tỉ: trong Q, dưới mỗi cận trên hữu tỉ luôn còn một cận trên hữu tỉ nhỏ hơn.

Ví dụ: tìm sup và inf của A = {2 + 1/n : n = 1, 2, ...}.

1. Các số 3, 5/2, 7/3, ... giảm dần: sup = 3 = max, thuộc A.
2. 2 + 1/n > 2, và với mọi e > 0 có n để 1/n < e: inf A = 2, không thuộc A.

> Lỗi thường gặp: nhầm sup với max. (0, 1) có sup = 1, nhưng 1 không thuộc (0, 1): tập không có phần tử lớn nhất.

:::check
Q: A = {(-1)^n/n : n = 1, 2, ...}. Tìm sup A và inf A.
A: Các số -1, 1/2, -1/3, 1/4, ... sup = 1/2 (n = 2), inf = -1 (n = 1); cả hai thuộc A.
:::

## Giới hạn trên và giới hạn dưới

:::hook
Loss khi huấn luyện có lúc dao động mãi giữa hai mức. limsup và liminf là hai mức mà dao động ấy bám vào về lâu dài.
:::

:::figure plane
caption: a_n = (-1)^n (2 - 1/n): số hạng chẵn bám lên 2, số hạng lẻ bám xuống -2.
size: 170 100
x: 0 11 2
y: -2.6 2.6 1
names: n a
line 0 2 1 2 do dash "limsup" pos=nw
line 0 -2 1 -2 xanh dash "liminf" pos=sw
point 1 -1 muc
point 2 1.5 muc
point 3 -1.667 muc
point 4 1.75 muc
point 5 -1.8 muc
point 6 1.833 muc
point 7 -1.857 muc
point 8 1.875 muc
point 9 -1.889 muc
point 10 1.9 muc
:::

:::core
limsup, liminf là giới hạn lớn nhất, nhỏ nhất của các dãy con; dãy bị chặn hội tụ đúng khi chúng bằng nhau.
:::

limsup không phải sup của các số hạng: (-1)^n (1 + 1/n) có số hạng 3/2 nhưng limsup = 1. Và limsup (a_n + b_n) có thể nhỏ hơn limsup a_n + limsup b_n: với a_n = (-1)^n, b_n = -(-1)^n, tổng luôn bằng 0, còn 1 + 1 = 2.

Ví dụ: limsup, liminf của a_n = (-1)^n (2 - 1/n).

1. n chẵn: a_n = 2 - 1/n -> 2. n lẻ: a_n = -(2 - 1/n) -> -2.
2. limsup = 2, liminf = -2: khác nhau, dãy không hội tụ.

> Lỗi thường gặp: thấy hai dãy con có hai giới hạn khác nhau là nói "không có limsup". Dãy bị chặn luôn có limsup và liminf.

:::check
Q: a_n = 1 + 3(-1)^n. Tìm limsup và liminf.
A: Các số -2, 4, -2, 4, ... limsup = 4, liminf = -2.
:::

## Điều kiện khả tích Riemann

:::hook
Kẹp diện tích giữa bậc thang thừa và bậc thang thiếu; khe hở co về 0 là xong.
:::

:::figure plane
caption: U = 14, L = 5 (xanh): diện tích 9 kẹp giữa.
size: 160 100
aspect: free
x: -0.3 3.3 1
y: -0.5 9.5 2
poly 0 0 1 0 1 1 0 1 vang
poly 1 0 2 0 2 4 1 4 vang
poly 2 0 3 0 3 9 2 9 vang
poly 1 0 2 0 2 1 1 1 xanh
poly 2 0 3 0 3 4 2 4 xanh
curve "x^2" do 0 3
:::

:::core
f khả tích khi chia đủ mịn thì bậc thang trên U và dưới L kẹp sát nhau tùy ý: U - L < e.
:::

$$ U(f, P) = \sum_k M_k\, h_k, \qquad L(f, P) = \sum_k m_k\, h_k $$

Ví dụ: U và L của x^2 trên [0, 3], P = {0, 1, 2, 3}.

1. x^2 tăng: sup ở mút phải, inf ở mút trái mỗi đoạn.
2. U = 1 + 4 + 9 = 14, L = 0 + 1 + 4 = 5 (mỗi đoạn dài 1).
3. Tích phân 9 nằm giữa 5 và 14.

:::check
Q: f(x) = 2x trên [0, 2], P = {0, 1, 2}. Tính U - L.
A: U = 2 . 1 + 4 . 1 = 6, L = 0 . 1 + 2 . 1 = 2, nên U - L = 4.
:::

### Hàm nào khả tích

:::figure plane
caption: Hàm nhảy một lần: chỉ dải đỏ chứa chỗ nhảy làm U khác L; chia mịn thì dải hẹp lại.
size: 150 70
x: -0.2 2.3 1
y: -0.3 2.6 1
segment 0 1 1 1 xanh
segment 1 2 2 2 xanh
poly 0.8 1 1.2 1 1.2 2 0.8 2 do
point 1 1 xanh open
point 1 2 xanh
:::

Hàm liên tục, đơn điệu, hay bị chặn và chỉ nhảy ở hữu hạn điểm đều khả tích: chỗ nhảy chỉ nằm trong vài dải, chia mịn thì dải hẹp lại. Hàm Dirichlet (1 trên số hữu tỉ, 0 trên số vô tỉ) thì không: đoạn con nào cũng chứa cả hai loại số, nên U = 1, L = 0 với mọi phân hoạch, khe hở không bao giờ co.

> Lỗi thường gặp: nghĩ |f| khả tích thì f khả tích. Trên [0, 1], lấy f = 1 tại số hữu tỉ, -1 tại số vô tỉ: |f| = 1 khả tích, còn f có U = 1, L = -1 với mọi phân hoạch.

:::check
Q: f(x) = x trên [0, 1], chia n đoạn đều. Tính U_n và U_n - L_n.
A: U_n = (1/n)(1/n + 2/n + ... + n/n) = (1 + ... + n)/n^2 = (n + 1)/(2n), vì 1 + ... + n = n(n + 1)/2 (không phải n^2/2). U_n - L_n = 1/n -> 0.
:::

## Hàm lồi

:::hook
Loss lồi thì gradient descent không kẹt ở đáy giả. Tính lồi cũng sinh ra cả loạt bất đẳng thức, như trung bình cộng >= trung bình nhân.
:::

:::figure plane
caption: Dây cung (đỏ) nối hai điểm của x^2 luôn nằm trên đồ thị.
size: 120 90
x: -1.6 2.6 1
y: -0.5 4.5 1
curve "x^2" xanh -1.5 2.1
segment -1 1 2 4 do
point -1 1 muc
point 2 4 muc
:::

:::core
f lồi khi mọi dây cung nằm trên đồ thị: f tại một điểm trung bình không vượt trung bình các giá trị f.
:::

$$ f(\lambda x + (1 - \lambda) y) \le \lambda f(x) + (1 - \lambda) f(y), \qquad 0 \le \lambda \le 1 $$

Hàm khả vi hai lần lồi đúng khi f'' >= 0 khắp khoảng; f'' chạm 0 vài điểm vẫn được, như x^4. |x| không khả vi mà vẫn lồi. Đồ thị lồi nằm trên mọi tiếp tuyến: tiếp tuyến của e^x tại 0 là 1 + x, nên e^x >= 1 + x.

Ví dụ: kiểm Jensen với f = x^2, x = 0, y = 4, lambda = 1/4.

1. Điểm trộn: (1/4) . 0 + (3/4) . 4 = 3, vế trái f(3) = 9.
2. Vế phải: (1/4) . 0 + (3/4) . 16 = 12, và 9 <= 12 (hiệu 3).

> Lỗi thường gặp: x^3 có f'' = 6x >= 0 chỉ khi x >= 0, nên chỉ lồi trên [0, +vô cùng). Tích hai hàm lồi cũng chưa chắc lồi.

:::check
Q: f(x) = x^3 - 6x^2 + x lồi trên [a, +vô cùng). Số a nhỏ nhất là bao nhiêu?
A: f''(x) = 6x - 12 >= 0 khi x >= 2: a = 2.
:::

## Không gian metric và không gian định chuẩn

:::hook
k-NN cần đo xa gần. Taxi theo ô phố, chim bay thẳng: hai cách đo, hai khoảng cách.
:::

:::figure plane
caption: Tới P(3, 4): taxi 7, bay 5, d_inf = 4.
size: 150 105
aspect: equal
x: -0.5 4.5 1
y: -0.5 4.5 1
segment 0 0 3 0 xanh
segment 3 0 3 4 xanh "d_1 = 7" pos=e
segment 0 0 3 4 do "d_2 = 5" pos=nw
point 0 0 muc
point 3 4 muc "P" pos=ne
:::

:::core
Khoảng cách: không âm, bằng 0 chỉ khi trùng nhau, đối xứng, và đi vòng không ngắn hơn đi thẳng.
:::

$$ \|x\|_1 = \sum_i |x_i|, \qquad \|x\|_2 = \sqrt{\sum_i x_i^2}, \qquad \|x\|_{\infty} = \max_i |x_i| $$

Ví dụ: u = (1, -2, 2), v = (3, 1, -4). Tính d_1, d_2, d_inf.

1. Độ lệch từng tọa độ: |2|, |3|, |-6|.
2. d_1 = 2 + 3 + 6 = 11, d_2 = sqrt(4 + 9 + 36) = 7.
3. d_inf = 6. Luôn có d_inf <= d_2 <= d_1.

:::check
Q: u = (0, 0, 0), v = (1, -2, 2). Tính d_1, d_2, d_inf.
A: Độ lệch 1, 2, 2: d_1 = 5, d_2 = sqrt(1 + 4 + 4) = 3, d_inf = 2.
:::

### Bác một công thức khoảng cách

:::figure grid
caption: Bác một công thức chỉ cần một phản ví dụ cho một điều kiện.
table
head "d(x, y)" "hỏng điều" "phản ví dụ"
row "|x^2 - y^2|" "= 0 chỉ khi x = y" "d(1, -1) = 0"
row "(x - y)^2" "tam giác" "d(0, 2) = 4 > 1 + 1"
row "x - y" "không âm" "d(0, 1) = -1"
row "|x - y|/(1 + |x - y|)" "không hỏng" "là metric"
:::

Muốn bác thì chỉ cần một bộ số làm hỏng một trong bốn điều kiện; muốn khẳng định thì phải chứng minh cả bốn.

> Lỗi thường gặp: khai triển ((x - y) + (y - z))^2 mà quên số hạng giữa 2(x - y)(y - z).

:::check
Q: d(x, y) = |x - y| + 1 khi x khác y, d(x, x) = 0. Đây có phải metric trên R?
A: Có. Ba điều đầu rõ; tam giác: |x - z| + 1 <= (|x - y| + 1) + (|y - z| + 1) khi y khác x, z (y trùng một đầu thì hai vế bằng nhau).
:::

### Dãy Cauchy và không gian đầy đủ

:::figure numberline
caption: Phóng to: 1.4; 1.41; 1.414; ... sát nhau dần trong Q, nhưng đích sqrt(2) không thuộc Q.
size: 200 45
range: 1.39 1.42 0.01
point 1.4 xanh
point 1.41 xanh
point 1.414 xanh
point sqrt(2) do "sqrt(2)" open
:::

Dãy Cauchy là dãy mà về sau các số hạng sát nhau tùy ý, dù chưa biết nó tiến về đâu. Dãy hội tụ thì luôn Cauchy. Không gian đầy đủ là nơi chiều ngược lại cũng đúng: R đầy đủ, còn Q thì không, vì 1, 1.4, 1.41, 1.414, ... là dãy Cauchy trong Q nhưng đích sqrt(2) nằm ngoài Q.

:::check
Q: Trong không gian (0, 1] với d(x, y) = |x - y|, dãy 1/n có là dãy Cauchy không? Có hội tụ trong (0, 1] không?
A: Có Cauchy: trong R nó hội tụ về 0. Nhưng 0 không thuộc (0, 1], nên nó không hội tụ trong (0, 1]: không gian này không đầy đủ.
:::
