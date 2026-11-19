---
id: tr_lib_t8
title_vi: Bài toán tối ưu, tập lồi và hàm lồi
subject: toi_uu_roi_rac
floor: 8
summary_vi: Cách viết một bài toán tối ưu, hai khái niệm làm cho bài toán dễ giải là tập lồi và hàm lồi, điều kiện gradient bằng 0, và lý do mọi cực tiểu địa phương của bài toán lồi đều là toàn cục.
skills: [tr_t8_bai_toan_toi_uu, tr_t8_tap_loi, tr_t8_ham_loi, tr_t8_dieu_kien_toi_uu, tr_t8_bai_toan_loi]
---
## Phát biểu bài toán tối ưu

Một bài toán tối ưu gồm ba phần:

- Biến quyết định x = (x_1, ..., x_n): những gì ta được chọn.
- Hàm mục tiêu f(x): cần làm nhỏ nhất (min) hoặc lớn nhất (max).
- Ràng buộc: tập D các phương án chấp nhận được, thường cho bởi các bất đẳng thức g_i(x) <= 0 và đẳng thức h_j(x) = 0.

$$ \min f(x) \quad \text{voi} \quad x \in D $$

x* là cực tiểu toàn cục nếu f(x*) <= f(x) với mọi x thuộc D; là cực tiểu địa phương nếu bất đẳng thức đó chỉ cần đúng với các x thuộc D gần x*. Cực tiểu toàn cục luôn là cực tiểu địa phương, chiều ngược lại thì không. Bài max f tương đương bài min (-f).

Ví dụ: làm hộp không nắp đáy vuông cạnh x, cao h, thể tích 32, tốn ít bìa nhất. Ràng buộc x^2 h = 32 cho h = 32/x^2, hàm mục tiêu S = x^2 + 4xh = x^2 + 128/x với x > 0. S'(x) = 2x - 128/x^2 = 0 cho x = 4, h = 2, S = 48.

> Lỗi thường gặp: chỉ tìm điểm đạo hàm bằng 0 khi miền là một đoạn. Trên [-3, 3], f(x) = x^3 - 3x + 1 có cực tiểu địa phương tại x = 1 với f(1) = -1, nhưng giá trị nhỏ nhất là f(-3) = -17 ở đầu mút. Cũng hay viết ngược chiều ràng buộc: "cần ít nhất 8" là >= 8.

## Tập lồi

Tập D là lồi nếu đoạn thẳng nối hai điểm bất kỳ của D nằm trọn trong D:

$$ x, y \in D, \; t \in [0, 1] \Rightarrow t x + (1 - t) y \in D $$

Các tập lồi thường gặp: cả không gian, nửa không gian a^T x <= b, siêu phẳng a^T x = b, hình tròn, hình cầu, tập phía trên đồ thị của một hàm lồi. Trên đường thẳng, tập lồi chính là các khoảng.

- Giao của các tập lồi là tập lồi; do đó miền ràng buộc của một bài toán quy hoạch tuyến tính (giao các nửa không gian) là tập lồi.
- Hợp của hai tập lồi thường không lồi: [0, 1] hợp [2, 3] không chứa 3/2.
- Bao lồi của các điểm A, B, C là các điểm aA + bB + cC với a, b, c >= 0, a + b + c = 1 (tổ hợp lồi), tức tam giác ABC.

Ví dụ: A(4, 3), B(-2, -3), P(2, 1). Từ P = tA + (1 - t)B có 6t - 2 = 2 và 6t - 3 = 1, cùng cho t = 2/3 thuộc [0, 1]: P nằm trên đoạn AB, nên mọi tập lồi chứa A và B đều chứa P.

> Lỗi thường gặp: chứng minh một tập lồi chỉ bằng vài điểm, hoặc lấy một tập "cong" làm ví dụ lồi. {xy >= 1} không lồi: (1, 1) và (-1, -1) thuộc tập nhưng trung điểm (0, 0) thì không. Còn {x^2 + y^2 >= 1} (phần ngoài hình tròn) cũng không lồi.

## Hàm lồi

Hàm f xác định trên tập lồi D là lồi nếu đồ thị nằm dưới mọi dây cung:

$$ f(t x + (1 - t) y) \le t f(x) + (1 - t) f(y) $$

Cách nhận ra hàm lồi:

- Một biến, khả vi hai lần trên một khoảng: f lồi khi và chỉ khi f''(x) >= 0 trên khoảng đó (lõm khi f'' <= 0).
- Nhiều biến: f lồi khi và chỉ khi ma trận Hesse H(x) nửa xác định dương tại mọi x. Với ma trận 2 x 2 đối xứng: nửa xác định dương khi hai phần tử chéo không âm và det H >= 0; xác định dương khi phần tử chéo dương và det H > 0.
- Tổng các hàm lồi, hàm lồi nhân với số dương, cực đại của các hàm lồi đều lồi. Tích của hai hàm lồi thì không chắc.

Ví dụ: f(x, y) = x^2 + 3xy + y^2 có ma trận Hesse

:::matrix
H = 2 3 ; 3 2
:::

det H = 4 - 9 = -5 < 0, nên f không lồi: f(1, -1) = -1 < 0 = f(0, 0). Còn x^2 + kxy + 4y^2 có H = [2, k; k, 8], lồi khi và chỉ khi 16 - k^2 >= 0, tức |k| <= 4.

> Lỗi thường gặp: chỉ nhìn đường chéo của ma trận Hesse. Với f = x^2 + 4xy + y^2 hai phần tử chéo đều bằng 2 > 0, nhưng det H = 4 - 16 < 0 nên f không lồi. Cũng hay nhớ ngược bất đẳng thức: hàm lồi cho f(trung bình) <= trung bình của f, không phải >=.

## Điều kiện tối ưu không ràng buộc

Với f khả vi trên R^n:

1. Điều kiện cần: nếu x* là cực tiểu địa phương thì grad f(x*) = 0 (x* là điểm dừng).
2. Điều kiện đủ bậc hai: nếu grad f(x*) = 0 và H(x*) xác định dương thì x* là cực tiểu địa phương; H(x*) có trị riêng âm và dương thì x* là điểm yên ngựa.
3. Nếu f lồi thì mọi điểm dừng là cực tiểu toàn cục.

$$ \nabla f(x^*) = 0, \quad H(x^*) \text{ xac dinh duong} $$

Với hàm bậc hai f = ax^2 + bxy + cy^2 + dx + ey, hệ grad f = 0 là hai phương trình bậc nhất 2ax + by + d = 0, bx + 2cy + e = 0.

Ví dụ: f(x, y) = 2x^2 + 2xy + y^2 - 6x - 4y. Hệ 4x + 2y = 6, 2x + 2y = 4 cho điểm dừng (1, 1). H = [4, 2; 2, 2] có det 4 > 0, phần tử chéo dương: f lồi chặt, nên giá trị nhỏ nhất là f(1, 1) = -5.

> Lỗi thường gặp: coi điểm dừng là cực trị. x^3 có đạo hàm 0 tại 0 nhưng 0 không là cực trị; f(x, y) = x^3 - 3x + y^2 có điểm dừng (-1, 0) là điểm yên ngựa, và (1, 0) là cực tiểu địa phương nhưng không toàn cục.

## Bài toán tối ưu lồi

Bài toán min f(x) với x thuộc D là bài toán lồi khi D là tập lồi và f là hàm lồi trên D (bài max g là lồi khi g lõm). Tính chất quan trọng nhất:

$$ \text{bai toan loi: cuc tieu dia phuong} \Rightarrow \text{cuc tieu toan cuc} $$

Lý do: nếu x* là cực tiểu địa phương mà có y thuộc D với f(y) < f(x*), thì các điểm (1 - t)x* + ty (thuộc D vì D lồi) gần x* có f nhỏ hơn f(x*) (vì f lồi), mâu thuẫn.

Khi có ràng buộc, nghiệm của bài toán lồi có thể nằm trên biên. Ví dụ min (x - 3)^2 + (y - 2)^2 với x + y <= 3: điểm (3, 2) không thỏa ràng buộc, nên nghiệm là hình chiếu của (3, 2) lên đường x + y = 3, tức (2, 1), giá trị nhỏ nhất 2.

Ví dụ một biến: min (x - 1)^2 + (x - 4)^2 + (x - 7)^2 với x <= 2. Không ràng buộc thì cực tiểu tại x = 4, nhưng 4 > 2; trên (-vô cùng, 2] hàm giảm nên nghiệm là x = 2, giá trị 30.

> Lỗi thường gặp: dùng "cực tiểu địa phương là toàn cục" cho hàm không lồi. f(x) = 3x^4 - 4x^3 - 12x^2 có cực tiểu địa phương tại x = -1 với f(-1) = -5, nhưng f''(0) = -24 < 0 nên f không lồi, và giá trị nhỏ nhất thật là f(2) = -32.
