---
id: dstt_lib_t8
title_vi: Ánh xạ tuyến tính và ma trận của nó
subject: dai_so_tuyen_tinh
floor: 8
summary_vi: Ánh xạ giữ phép cộng và phép nhân với số, nhân và ảnh, định lý số chiều, ma trận của ánh xạ trong một cặp cơ sở, hợp ánh xạ ứng với tích ma trận, và đổi cơ sở B = P^(-1) A P.
skills: [dstt_t8_anh_xa_tuyen_tinh, dstt_t8_nhan_va_anh, dstt_t8_dinh_ly_so_chieu, dstt_t8_ma_tran_anh_xa, dstt_t8_hop_anh_xa, dstt_t8_doi_co_so]
---
## Ánh xạ tuyến tính

Ánh xạ f: V -> W giữa hai không gian vectơ là tuyến tính khi với mọi u, v và mọi số k:

$$ f(u + v) = f(u) + f(v), \qquad f(ku) = k f(u) $$

Hệ quả: f(0) = 0, và f giữ mọi tổ hợp tuyến tính. Vì vậy chỉ cần biết ảnh của các vectơ của MỘT cơ sở là biết f ở mọi nơi.

Từ R^n vào R^m, f tuyến tính khi và chỉ khi mỗi tọa độ của f(x) là một tổ hợp tuyến tính của các tọa độ của x, không có hằng số, không có tích, bình phương hay trị tuyệt đối. f(x, y) = (2x - y, x + 3y) tuyến tính; (x + y, x - 1) thì không vì f(0, 0) khác 0.

Ví dụ f(1, 2) = (3, 1), f(2, 3) = (1, 0). Để tính f(1, 0): viết (1, 0) = -3(1, 2) + 2(2, 3), rồi f(1, 0) = -3(3, 1) + 2(1, 0) = (-7, -3).

> Lỗi thường gặp: lấy luôn cặp hệ số (-3, 2) làm f(1, 0). Hệ số là tọa độ của (1, 0); ảnh phải tính qua f(1, 2) và f(2, 3).

## Nhân Ker f và ảnh Im f

$$ \text{Ker} f = \{v : f(v) = 0\}, \qquad \text{Im} f = \{f(v) : v \in V\} $$

Ker f là không gian con của V, Im f là không gian con của W. Nếu f(x) = Ax:

- Ker f là không gian nghiệm của Ax = 0: giải hệ thuần nhất, mỗi ẩn tự do cho một vectơ cơ sở.
- Im f được sinh bởi các cột của A: khử Gauss, các cột có trụ của CHÍNH A là một cơ sở.

:::matrix
A = 1 2 0 1 ; 0 0 1 1 ; 1 2 1 2
:::

Hàng 3 bằng hàng 1 cộng hàng 2, rank A = 2. Ker f có cơ sở (-2, 1, 0, 0), (-1, 0, -1, 1); Im f có cơ sở là cột 1 và cột 3 của A: (1, 0, 1), (0, 1, 1).

f đơn ánh khi và chỉ khi Ker f = {0}.

> Lỗi thường gặp: lấy các hàng khác 0 của dạng bậc thang làm cơ sở của Im f. Biến đổi hàng làm thay đổi không gian cột; phải lấy cột của ma trận ban đầu.

## Định lý số chiều

Với f: V -> W tuyến tính và V có số chiều hữu hạn:

$$ \text{dim} \, \text{Ker} f + \text{dim} \, \text{Im} f = \text{dim} \, V $$

Với f(x) = Ax, đó là n = (n - rank A) + rank A.

Hệ quả, với dim V = n và dim W = m:

- f đơn ánh khi dim Ker f = 0; khi đó n <= m.
- f toàn ánh khi dim Im f = m; khi đó n >= m.
- Khi n = m: đơn ánh, toàn ánh và song ánh là một.

Ví dụ f: R^5 -> R^3 toàn ánh thì dim Ker f = 5 - 3 = 2. Không có ánh xạ tuyến tính nào từ R^3 lên toàn bộ R^4.

> Lỗi thường gặp: nghĩ rằng ánh xạ từ R^3 vào chính nó có thể toàn ánh mà không đơn ánh. Khi số chiều hai phía bằng nhau, mất đơn ánh là mất luôn toàn ánh.

## Ma trận của ánh xạ tuyến tính

Cho cơ sở B = {b1, ..., bn} của V và C của W. Ma trận của f trong cặp cơ sở đó có cột thứ j là tọa độ của f(bj) trong C:

$$ A = \left( [f(b_{1})]_{C} \; \ldots \; [f(b_{n})]_{C} \right) $$

Với cơ sở chính tắc ở cả hai phía, cột j chính là f(ej). Ví dụ f(x, y) = (2x - y, x + 3y, y) có cột f(1, 0) = (2, 1, 0) và f(0, 1) = (-1, 3, 1):

:::matrix
A = 2 -1 ; 1 3 ; 0 1
:::

Ví dụ trên đa thức: f(p) = p' với cơ sở 1, x, x^2. f(1) = 0, f(x) = 1, f(x^2) = 2x cho ba cột (0, 0, 0), (1, 0, 0), (0, 2, 0).

$$ [f(v)]_{C} = A \, [v]_{B} $$

> Lỗi thường gặp: đặt ảnh f(bj) làm HÀNG, hoặc đặt chính f(bj) làm cột khi cơ sở đích không phải chính tắc. Cột là TỌA ĐỘ của ảnh trong cơ sở đích.

## Hợp ánh xạ và tích ma trận

Nếu f có ma trận A_f và g có ma trận A_g (cơ sở chính tắc) thì ánh xạ hợp g o f, làm f trước, có ma trận

$$ A_{g \circ f} = A_{g} A_{f} $$

Ánh xạ làm sau đứng bên trái, giống như trong g(f(x)). Vì AB nói chung khác BA, g o f và f o g nói chung khác nhau.

Ví dụ f(x, y) = (x + 2y, y), g(x, y) = (x, 3x + y): g(f(x, y)) = (x + 2y, 3x + 7y), còn f(g(x, y)) = (7x + 2y, 3x + y).

f là đẳng cấu (song ánh tuyến tính) khi ma trận vuông của nó khả nghịch; khi đó

$$ A_{f^{-1}} = (A_{f})^{-1}, \qquad (g \circ f)^{-1} = f^{-1} \circ g^{-1} $$

> Lỗi thường gặp: viết ma trận của g o f là A_f A_g, hoặc lấy ma trận chuyển vị thay cho ma trận nghịch đảo khi tìm ánh xạ ngược.

## Đổi cơ sở và ma trận đồng dạng

Nếu f: R^n -> R^n có ma trận chính tắc A và P có các cột là các vectơ của cơ sở mới B, thì ma trận của f trong B là

$$ B = P^{-1} A P $$

Đọc từ phải sang trái: đổi tọa độ trong B sang chính tắc (P), tác động f (A), đổi về B (P^(-1)).

:::matrix
A = 4 -2 ; 1 1
P = 1 2 ; 1 1
:::

A(1, 1) = (2, 2) = 2(1, 1) và A(2, 1) = (6, 3) = 3(2, 1), nên trong cơ sở (1, 1), (2, 1) ma trận của f là ma trận chéo với đường chéo 2, 3.

Hai ma trận A và B = P^(-1) A P gọi là đồng dạng. Chúng có cùng định thức, cùng vết, cùng hạng và cùng đa thức đặc trưng.

$$ \text{det} \, B = \text{det} \, A, \qquad \text{tr} \, B = \text{tr} \, A $$

> Lỗi thường gặp: tính (AP)P^(-1) thay cho P^(-1)(AP). Thứ tự đó cho lại chính A.
