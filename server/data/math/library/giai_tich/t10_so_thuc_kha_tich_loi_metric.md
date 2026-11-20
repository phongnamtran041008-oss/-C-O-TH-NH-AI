---
id: gt_lib_t10
title_vi: Tài năng: số thực, khả tích, hàm lồi và không gian metric
subject: giai_tich
floor: 10
summary_vi: Tầng ẩn dựng lại nền của giải tích - tiên đề cận trên đúng của số thực, giới hạn trên và giới hạn dưới của một dãy, điều kiện khả tích Riemann qua tổng Darboux, hàm lồi cùng bất đẳng thức Jensen, rồi khái quát hoá khoảng cách thành không gian metric và không gian định chuẩn. Trọng tâm là chứng minh bằng định nghĩa và tìm phản ví dụ.
skills: [gt_t10_tien_de_so_thuc, gt_t10_gioi_han_tren_duoi, gt_t10_kha_tich_riemann, gt_t10_ham_loi, gt_t10_khong_gian_metric]
---
## Tiên đề của tập số thực

Tiên đề cận trên đúng: mọi tập con khác rỗng của R mà bị chặn trên đều có một cận trên bé nhất, gọi là cận trên đúng sup A; cận dưới đúng inf A định nghĩa tương tự. Đây là điều làm R khác Q: tập {x thuộc Q : x^2 < 2} có cận trên hữu tỉ nhưng không có cận trên bé nhất hữu tỉ (nó chỉ bằng sqrt(2) trong R).

Cách kiểm tra s = sup A chia làm hai nửa:

$$ s = \mathrm{sup}\,A \iff \big(\forall a \in A:\ a \le s\big) \land \big(\forall \varepsilon > 0\ \exists a \in A:\ a > s - \varepsilon\big) $$

Nửa đầu nói s là cận trên, nửa sau nói không có cận trên nào nhỏ hơn s. Ví dụ A = {1 - 1/n : n = 1, 2, ...}:

1. Mọi phần tử 1 - 1/n < 1 nên 1 là cận trên.
2. Cho e > 0; theo tính Archimedes có n với 1/n < e, khi đó 1 - 1/n > 1 - e.
3. Vậy 1 - e không là cận trên, nên sup A = 1; 1 không thuộc A (mọi phần tử đều < 1), nên A không có phần tử lớn nhất.

> Lỗi thường gặp: nhầm sup với max (sup có thể không thuộc tập, như (0, 1) có sup 1); suy từ "sup A = 1" ra "1 thuộc A"; nghĩ rằng mọi tập bị chặn trên của Q đều có cận trên đúng hữu tỉ.

## Giới hạn trên và giới hạn dưới

Với dãy bị chặn (a_n), đặt các số sup{a_k : k >= n} giảm dần theo n. Giới hạn của chúng là giới hạn trên, và đó cũng là giới hạn lớn nhất của các dãy con hội tụ; giới hạn dưới là giới hạn nhỏ nhất.

$$ \mathrm{limsup}_{n \to \infty}\, a_n = \lim_{n \to \infty} \mathrm{sup}\,\{a_k : k \ge n\} $$

Tính chất cần nhớ: liminf <= limsup; dãy bị chặn hội tụ khi và chỉ khi liminf = limsup (và khi đó bằng giới hạn); limsup (a_n + b_n) <= limsup a_n + limsup b_n, và dấu bằng không phải lúc nào cũng xảy ra.

Ví dụ a_n = (-1)^n (1 + 1/n):

1. Dãy con chẵn a_(2k) = 1 + 1/(2k) tiến tới 1; dãy con lẻ a_(2k+1) = -(1 + 1/(2k+1)) tiến tới -1.
2. Mọi số hạng thuộc một trong hai dãy con này, nên chỉ có hai giới hạn dãy con: 1 và -1.
3. limsup a_n = 1 và liminf a_n = -1; hai số khác nhau nên dãy không hội tụ.

> Lỗi thường gặp: lấy sup của tập các số hạng (ví dụ 3/2 ở n = 2) thay vì giới hạn lớn nhất của dãy con; cho rằng dãy có hai giới hạn dãy con khác nhau thì "không có limsup"; coi limsup của tổng bằng tổng các limsup (a_n = (-1)^n và b_n = -(-1)^n cho 0 khác 2).

## Điều kiện khả tích Riemann

Với hàm bị chặn f trên [a, b] và phân hoạch P chia nó thành các đoạn con, gọi M_k, m_k là sup và inf của f trên đoạn con thứ k và h_k là độ dài của nó. Tổng Darboux trên và dưới là:

$$ U(f, P) = \sum_k M_k\, h_k, \qquad L(f, P) = \sum_k m_k\, h_k $$

f khả tích Riemann khi và chỉ khi với mọi e > 0 có phân hoạch P để U(f, P) - L(f, P) < e; khi đó tích phân nằm giữa L(f, P) và U(f, P) với mọi P.

Ví dụ f(x) = x^2 trên [0, 2] và P = {0, 1, 2}: f tăng nên sup ở mút phải, inf ở mút trái.

1. Trên [0, 1]: M = 1, m = 0. Trên [1, 2]: M = 4, m = 1.
2. U(f, P) = 1 . 1 + 4 . 1 = 5 và L(f, P) = 0 . 1 + 1 . 1 = 1; tích phân 8/3 nằm giữa.
3. Với hàm tăng chia đều thành n đoạn dài h: U - L = h (f(b) - f(a)), nhỏ tuỳ ý khi n lớn.

Hàm liên tục, hàm bị chặn với hữu hạn điểm gián đoạn, hàm đơn điệu đều khả tích; hàm không bị chặn thì không. Hàm Dirichlet (1 trên số hữu tỉ, 0 trên số vô tỉ) trên [0, 1] có U = 1 và L = 0 với mọi P nên không khả tích Riemann.

> Lỗi thường gặp: tính tổng 1 + 2 + ... + n thành n^2/2 (đúng là n(n + 1)/2); coi "bị chặn" là đủ để khả tích; coi "liên tục" là cần để khả tích (hàm bậc thang khả tích); nghĩ |f| khả tích thì f khả tích (hàm 1 trên hữu tỉ, -1 trên vô tỉ là phản ví dụ).

## Hàm lồi

Hàm f trên một khoảng là lồi khi mọi đoạn nối hai điểm của đồ thị nằm trên đồ thị:

$$ f(\lambda x + (1 - \lambda) y) \le \lambda f(x) + (1 - \lambda) f(y), \qquad 0 \le \lambda \le 1 $$

Hàm khả vi hai lần có tiêu chuẩn f'' >= 0 (không cần f'' > 0: x^4 lồi dù f''(0) = 0); đồ thị hàm lồi khả vi nằm trên mọi tiếp tuyến. Bất đẳng thức Jensen mở rộng định nghĩa cho nhiều điểm với trọng số l_i không âm có tổng bằng 1:

$$ f\Big(\sum_i \lambda_i x_i\Big) \le \sum_i \lambda_i f(x_i) $$

Ví dụ e^x >= 1 + x với mọi x:

1. f(x) = e^x có f''(x) = e^x > 0 nên f lồi.
2. Tiếp tuyến tại 0 là y = 1 + x và đồ thị lồi nằm trên nó.
3. Dùng Jensen với e^x và x = ln a, y = ln b, z = ln c cho (abc)^(1/3) <= (a + b + c)/3 (trung bình nhân không vượt trung bình cộng).

> Lỗi thường gặp: kết luận lồi trên R từ f'' = 6x >= 0 (chỉ đúng với x >= 0); đảo chiều bất đẳng thức Jensen (chiều <= dành cho hàm lồi, hàm lõm như ln thì ngược lại); nghĩ tích của hai hàm lồi là lồi (x và -x đều lồi nhưng tích -x^2 lõm); đòi f'' > 0 ngặt.

## Không gian metric và không gian định chuẩn

Khoảng cách (metric) d trên tập X gán cho mỗi cặp điểm một số d(x, y) thoả bốn điều: không âm, bằng 0 khi và chỉ khi x = y, đối xứng, và bất đẳng thức tam giác. Chuẩn của vectơ có ba tính chất tương ứng (dương trừ vectơ 0, nhân với số thì nhân với |số|, bất đẳng thức tam giác) và sinh ra khoảng cách d(x, y) = chuẩn của (x - y).

$$ d(x, z) \le d(x, y) + d(y, z) $$

$$ \|x\|_1 = \sum_i |x_i|, \qquad \|x\|_2 = \sqrt{\sum_i x_i^2}, \qquad \|x\|_{\infty} = \max_i |x_i| $$

Với mọi x trong R^n: chuẩn max <= chuẩn Euclid <= chuẩn tổng. Dãy (x_n) là dãy Cauchy nếu với mọi e > 0 có N sao cho d(x_m, x_n) < e khi m, n >= N. Dãy hội tụ thì là dãy Cauchy; không gian mà mọi dãy Cauchy hội tụ gọi là đầy đủ (R đầy đủ, Q không: các số thập phân gần đúng của sqrt(2) là dãy Cauchy trong Q không hội tụ trong Q).

Ví dụ d(x, y) = (x - y)^2 trên R không là metric:

1. Không âm, bằng 0 đúng khi x = y, và đối xứng: ba điều đầu đúng.
2. Bất đẳng thức tam giác với x = 0, y = 1, z = 2: d(0, 2) = 4 còn d(0, 1) + d(1, 2) = 2, nên bị vi phạm.
3. Lỗi nằm ở số hạng giữa của ((x - y) + (y - z))^2 = (x - y)^2 + 2(x - y)(y - z) + (y - z)^2.

> Lỗi thường gặp: quên số hạng giữa khi khai triển bình phương; coi |x^2 - y^2| là metric trên R (d(1, -1) = 0 dù 1 khác -1); chỉ kiểm tra một vài bộ ba rồi kết luận bất đẳng thức tam giác đúng; nghĩ mọi dãy Cauchy đều hội tụ trong không gian bất kỳ.
