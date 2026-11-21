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

Q thiếu điều này: {x thuộc Q : x^2 < 2} không có sup trong Q.

Ví dụ: tìm sup và inf của A = {2 + 1/n : n = 1, 2, ...}.

1. Các số 3, 5/2, 7/3, ... giảm dần: sup = 3 = max, thuộc A.
2. 2 + 1/n > 2, và với mọi e > 0 có n để 1/n < e.
3. inf A = 2, không thuộc A.

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

limsup không phải sup của các số hạng: (-1)^n (1 + 1/n) có số hạng 3/2 nhưng limsup = 1. Và limsup (a_n + b_n) có thể nhỏ hơn hẳn limsup a_n + limsup b_n.

Ví dụ: limsup, liminf của a_n = (-1)^n (2 - 1/n).

1. n chẵn: a_n = 2 - 1/n -> 2.
2. n lẻ: a_n = -(2 - 1/n) -> -2.
3. limsup = 2, liminf = -2: khác nhau, dãy không hội tụ.

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

Liên tục, đơn điệu, hay bị chặn với hữu hạn điểm gián đoạn: khả tích. Hàm Dirichlet (1 trên Q, 0 ngoài Q) có U = 1, L = 0 mọi P: không.

Ví dụ: U và L của x^2 trên [0, 3], P = {0, 1, 2, 3}.

1. x^2 tăng: sup ở mút phải, inf ở mút trái mỗi đoạn.
2. U = 1 + 4 + 9 = 14, L = 0 + 1 + 4 = 5 (mỗi đoạn dài 1).
3. Tích phân 9 nằm giữa 5 và 14.

> Lỗi thường gặp: tính 1 + 2 + ... + n = n^2/2. Đúng là n(n + 1)/2. Và |f| khả tích chưa chắc f khả tích.

:::check
Q: f(x) = 2x trên [0, 2], P = {0, 1, 2}. Tính U - L.
A: U = 2 . 1 + 4 . 1 = 6, L = 0 . 1 + 2 . 1 = 2, nên U - L = 4.
:::

## Hàm lồi

:::hook
Loss lồi thì gradient descent không kẹt ở đáy giả. Tính lồi cũng sinh ra cả loạt bất đẳng thức, như trung bình cộng >= trung bình nhân.
:::

:::figure plane
caption: Dây cung (đỏ) nối hai điểm của x^2 luôn nằm trên đồ thị.
size: 150 100
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

Khả vi hai lần: lồi khi f'' >= 0 (x^4 vẫn lồi); |x| cũng lồi. Lồi thì nằm trên tiếp tuyến: e^x >= 1 + x.

Ví dụ: kiểm Jensen với f = x^2, x = 0, y = 4, lambda = 1/4.

1. Điểm trộn: (1/4) . 0 + (3/4) . 4 = 3, vế trái f(3) = 9.
2. Vế phải: (1/4) . 0 + (3/4) . 16 = 12.
3. 9 <= 12, hiệu 3.

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

Không là metric: |x^2 - y^2|, (x - y)^2. Dãy Cauchy hội tụ trong R, chưa chắc trong Q.

Ví dụ: u = (1, -2, 2), v = (3, 1, -4). Tính d_1, d_2, d_inf.

1. Độ lệch từng tọa độ: |2|, |3|, |-6|.
2. d_1 = 2 + 3 + 6 = 11, d_2 = sqrt(4 + 9 + 36) = 7.
3. d_inf = 6. Luôn có d_inf <= d_2 <= d_1.

> Lỗi thường gặp: khai triển ((x - y) + (y - z))^2 mà quên số hạng giữa 2(x - y)(y - z).

:::check
Q: d(x, y) = |x - y| + 1 khi x khác y, d(x, x) = 0. Đây có phải metric trên R?
A: Có. Ba điều đầu rõ; tam giác: |x - z| + 1 <= (|x - y| + 1) + (|y - z| + 1) khi y khác x, z (y trùng một đầu thì hai vế bằng nhau).
:::
