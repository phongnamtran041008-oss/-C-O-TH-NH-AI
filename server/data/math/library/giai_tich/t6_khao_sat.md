---
id: gt_lib_t6
title_vi: Đơn điệu, cực trị và khảo sát hàm số
subject: giai_tich
floor: 6
summary_vi: Dấu của đạo hàm cấp một kể chuyện hàm tăng giảm và đạt cực trị ở đâu, dấu của đạo hàm cấp hai kể chuyện đồ thị cong lên hay cong xuống; ghép thêm tiệm cận là vẽ được cả đồ thị.
skills: [gt_t6_don_dieu, gt_t6_cuc_tri, gt_t6_gtln_gtnn, gt_t6_loi_lom, gt_t6_tiem_can, gt_t6_khao_sat]
---
## Tính đơn điệu

Trên một khoảng I mà f khả vi:

$$ f'(x) > 0 \ \forall x \in I \;\Rightarrow\; f(x_1) < f(x_2) \ \forall x_1 < x_2 \in I $$

tức f tăng ngặt trên I; f'(x) < 0 trên I thì f giảm ngặt trên I. Điều này suy ra từ định lý Lagrange: f(x2) - f(x1) = f'(c)(x2 - x1) cùng dấu với f'.

Cách tìm khoảng tăng, giảm:

1. Tính f'(x) và phân tích thành nhân tử.
2. Tìm các điểm f' bằng 0 hoặc không xác định.
3. Lập bảng dấu của f' giữa các điểm đó.

Ví dụ f(x) = x^3 - 12x + 1: f'(x) = 3(x - 2)(x + 2), âm trên (-2, 2), dương ngoài đoạn đó. f giảm trên [-2, 2], tăng trên hai khoảng còn lại.

Chiều ngược lại chỉ đúng một nửa: f tăng ngặt thì f' >= 0, có thể bằng 0 tại vài điểm (x^3 tăng ngặt mà f'(0) = 0). Vì vậy "f đồng biến trên R" với đa thức bậc ba ứng với f'(x) >= 0 với mọi x, tức tam thức f' có biệt thức không dương.

Tính đơn điệu chứng minh được bất đẳng thức: muốn ln(1 + x) < x với x > 0, xét g(x) = x - ln(1 + x) có g(0) = 0 và g'(x) = x/(1 + x) > 0.

> Lỗi thường gặp: gộp hai khoảng rời nhau. 1/x giảm trên (-vô cùng, 0) và trên (0, +vô cùng), nhưng không giảm trên R \ {0}: f(-1) = -1 < 1 = f(1).

## Cực trị

f đạt cực đại tại x0 khi f(x0) >= f(x) với mọi x gần x0; cực tiểu thì ngược lại. Nếu f khả vi tại một điểm cực trị thì f'(x0) = 0 (định lý Fermat). Các điểm f' = 0 hoặc f' không tồn tại gọi là điểm tới hạn: chỉ ở đó mới có thể có cực trị.

Điều kiện f'(x0) = 0 là cần, chưa đủ: x^3 có f'(0) = 0 mà không có cực trị. Hai dấu hiệu đủ:

- Cấp một: f' đổi dấu từ + sang - qua x0 thì cực đại, từ - sang + thì cực tiểu, không đổi dấu thì không có cực trị.
- Cấp hai: f'(x0) = 0 và f''(x0) < 0 thì cực đại, f''(x0) > 0 thì cực tiểu. Lý do nằm ở khai triển Taylor quanh x0: số hạng bậc một mất đi, dấu của f''(x0) quyết định f(x) lớn hay nhỏ hơn f(x0).

$$ f'(x_0) = 0 \;\Rightarrow\; f(x) - f(x_0) \approx \frac{f''(x_0)}{2}(x - x_0)^2 $$

Khi f''(x0) = 0, dấu hiệu cấp hai không nói gì: x^4, -x^4 và x^3 đều có f'(0) = f''(0) = 0 với ba kết luận khác nhau. Quay về xét dấu f'.

Nghiệm bội của f' cũng cần để ý: f(x) = x^4 - 4x^3 có f'(x) = 4x^2(x - 3). Qua nghiệm kép 0, f' không đổi dấu; chỉ x = 3 là cực trị (cực tiểu, f(3) = -27).

> Lỗi thường gặp: kết luận "f'(a) = 0 nên a là điểm cực trị", hoặc "f''(a) = 0 nên a không phải điểm cực trị". Cả hai đều cần xét dấu f'.

## Giá trị lớn nhất và nhỏ nhất trên đoạn

Hàm liên tục trên đoạn đóng [a, b] luôn có giá trị lớn nhất (GTLN) và nhỏ nhất (GTNN). Chúng đạt ở điểm tới hạn bên trong đoạn hoặc ở hai đầu mút. Cách tìm:

1. Tìm các điểm tới hạn thuộc (a, b).
2. Tính f tại các điểm đó và tại a, b.
3. Số lớn nhất là GTLN, số nhỏ nhất là GTNN.

$$ \max_{[a, b]} f = \max\{ f(a),\ f(b),\ f(c_1), \dots, f(c_k) \} $$

Ví dụ f(x) = x^3 - 3x trên [0, 3]: điểm tới hạn trong đoạn là x = 1, f(1) = -2; hai đầu f(0) = 0, f(3) = 18. GTLN = 18 ở đầu mút, GTNN = -2.

Không cần biết điểm nào là cực đại hay cực tiểu: chỉ so các giá trị. GTLN có thể lớn hơn mọi giá trị cực đại, vì nó nằm ở đầu mút.

Trên khoảng mở hoặc vô hạn, hàm có thể không có GTLN, GTNN (x trên (0, 1) không đạt 1). Khi đó dùng bảng biến thiên: x + 4/x trên (0, +vô cùng) giảm rồi tăng, nên GTNN là f(2) = 4 và không có GTLN.

Bài toán thực tế: viết đại lượng cần tối ưu thành hàm một biến, tìm miền của biến, rồi làm như trên. Hộp không nắp gấp từ tấm vuông cạnh 12 có V(x) = x(12 - 2x)^2 với 0 < x < 6, lớn nhất tại x = 2, V = 128.

> Lỗi thường gặp: quên hai đầu mút. Chỉ xét điểm tới hạn sẽ bỏ sót GTLN 18 của x^3 - 3x trên [0, 3].

## Lồi, lõm và điểm uốn

Trong bí cảnh này, đồ thị gọi là lồi trên khoảng khi nó cong lên, tức f'' > 0; lõm khi nó cong xuống, tức f'' < 0. (Sách khác có thể gọi ngược lại; câu hỏi sẽ luôn ghi rõ dấu của f''.)

$$ f'' > 0 \;\Rightarrow\; f(x) > f(x_0) + f'(x_0)(x - x_0) \quad (x \ne x_0) $$

Công thức trên (với f'' > 0 trên cả khoảng) nói: đồ thị lồi nằm phía trên mọi tiếp tuyến của nó. Điểm uốn là điểm của đồ thị nơi chiều cong đổi, tức f'' đổi dấu.

Cách tìm:

1. Tính f'' và tìm các điểm f'' = 0 hoặc không xác định.
2. Xét dấu f'' ở hai bên mỗi điểm.
3. Nơi nào f'' đổi dấu thì có điểm uốn; tung độ tính bằng f, không phải f''.

Ví dụ y = x^3 - 6x^2 + 5: y'' = 6x - 12 đổi dấu tại 2, điểm uốn (2, -11). Ví dụ y = x^4 - 4x^3: y'' = 12x(x - 2), hai điểm uốn (0, 0) và (2, -16).

Đồ thị bậc ba luôn có đúng một điểm uốn, và nó là tâm đối xứng của đồ thị.

> Lỗi thường gặp: f''(x0) = 0 chưa đủ để có điểm uốn. x^4 có f''(0) = 0 nhưng f'' >= 0 ở hai bên, đồ thị cong lên suốt.

## Tiệm cận

Ba loại tiệm cận của đồ thị y = f(x):

- Tiệm cận đứng x = a: f(x) -> vô cùng khi x -> a (ít nhất một phía).
- Tiệm cận ngang y = b: f(x) -> b khi x -> +vô cùng hoặc -vô cùng.
- Tiệm cận xiên y = px + q (p khác 0): f(x) - (px + q) -> 0 khi x -> vô cùng.

Hệ số của tiệm cận xiên:

$$ p = \lim_{x \to \infty} \frac{f(x)}{x}, \qquad q = \lim_{x \to \infty} \big(f(x) - px\big) $$

Với phân thức, chia đa thức là nhanh nhất: x^2/(x - 1) = x + 1 + 1/(x - 1), nên tiệm cận xiên y = x + 1 và tiệm cận đứng x = 1. Với (ax + b)/(cx + d) (ad - bc khác 0): tiệm cận đứng x = -d/c, tiệm cận ngang y = a/c.

Phía +vô cùng và -vô cùng có thể khác nhau: sqrt(x^2 + 2x) có tiệm cận y = x + 1 bên phải nhưng y = -x - 1 bên trái.

Không phải nơi nào mẫu bằng 0 cũng có tiệm cận đứng: (x^2 - 4)/(x - 2) -> 4 khi x -> 2, chỉ là điểm gián đoạn khử được. Và f(x)/x -> p chưa đủ: x + sin x có f(x)/x -> 1 nhưng f(x) - x = sin x không dần tới 0, nên không có tiệm cận xiên.

> Lỗi thường gặp: tính sai q, chẳng hạn cho x/(x + 1) -> 0 khi x -> vô cùng (đúng là -> 1). Kiểm tra lại bằng phép chia đa thức.

## Lược đồ khảo sát hàm số

Khảo sát và vẽ đồ thị của y = f(x) đi theo các bước:

1. Tập xác định; tính chẵn, lẻ, tuần hoàn nếu có (để thu gọn việc vẽ).
2. Đạo hàm f', bảng biến thiên, cực trị.
3. Đạo hàm f'', khoảng lồi lõm, điểm uốn.
4. Các tiệm cận và giới hạn ở hai đầu tập xác định.
5. Vài điểm đặc biệt (giao với các trục), rồi vẽ.

Ví dụ y = x^3 - 3x: lẻ nên đối xứng qua O; y' = 3(x - 1)(x + 1) cho cực đại y(-1) = 2, cực tiểu y(1) = -2; y'' = 6x cho điểm uốn O; không có tiệm cận.

Bảng biến thiên trả lời ngay bài đếm nghiệm: số nghiệm của f(x) = m là số giao điểm của đồ thị với đường ngang y = m. Với hàm bậc ba có giá trị cực đại f_CD và giá trị cực tiểu f_CT, phương trình có ba nghiệm phân biệt đúng khi

$$ f_{CT} < m < f_{CD} $$

hai nghiệm khi m bằng một trong hai giá trị đó, một nghiệm khi m nằm ngoài. Với x^3 - 3x^2 (cực đại 0, cực tiểu -4): ba nghiệm khi -4 < m < 0.

Một đồ thị có thể có giá trị cực đại nhỏ hơn giá trị cực tiểu khi hai điểm đó ở hai nhánh khác nhau, ngăn bởi tiệm cận đứng: (x^2 + 3)/(x - 1) có cực đại -2 và cực tiểu 6.

> Lỗi thường gặp: làm từng bước đúng rồi chép sai một kết quả ở bước cuối, như ghi tiệm cận xiên của x^2/(x - 1) là y = x. Đối chiếu bảng biến thiên với tiệm cận: nhánh phải đi lên sát y = x + 1.
