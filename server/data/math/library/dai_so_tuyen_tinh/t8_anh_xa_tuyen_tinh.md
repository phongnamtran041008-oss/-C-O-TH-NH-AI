---
id: dstt_lib_t8
title_vi: Ánh xạ tuyến tính và ma trận của nó
subject: dai_so_tuyen_tinh
floor: 8
format: 2
summary_vi: Ánh xạ tuyến tính biến lưới thẳng thành lưới thẳng và giữ gốc đứng yên: biết nó làm gì với các vectơ cơ sở là biết hết, ghi lại thành ma trận, làm liền hai phép là nhân hai ma trận, và đổi cơ sở là nhìn cùng một phép qua cặp kính khác.
skills: [dstt_t8_anh_xa_tuyen_tinh, dstt_t8_nhan_va_anh, dstt_t8_dinh_ly_so_chieu, dstt_t8_ma_tran_anh_xa, dstt_t8_hop_anh_xa, dstt_t8_doi_co_so]
---
## Ánh xạ tuyến tính

:::hook
Trong game, xoay, lật hay phóng to nhân vật là biến đổi mọi điểm cùng một lúc mà lưới vẫn thẳng, gốc đứng yên. Đó chính là ánh xạ tuyến tính.
:::

:::figure plane
caption: f(x, y) = (2x - y, x + y) đưa ô vuông đơn vị (xanh) thành hình bình hành (vàng) dựng trên f(e1) = (2, 1) và f(e2) = (-1, 1).
size: 150 110
x: -1.5 2.5 1
y: -0.5 2.5 1
poly 0 0 2 1 1 2 -1 1 vang
poly 0 0 1 0 1 1 0 1 xanh
vector 0 0 2 1 do
vector 0 0 -1 1 do
:::

:::core
Ánh xạ tuyến tính giữ phép cộng và phép nhân với số; vì thế biết ảnh của các vectơ cơ sở là biết ảnh của mọi vectơ.
:::

Hệ quả: f(0) = 0. Từ R^n vào R^m, f tuyến tính khi mỗi tọa độ của f(x) là tổ hợp của x, y, ... không hằng số, không tích, bình phương hay trị tuyệt đối. Vài mẫu: chiếu lên Ox là (x, 0), lật qua Ox là (x, -y), quay 90 độ là (-y, x).

Ví dụ: f(1, 1) = (2, 0), f(1, -1) = (0, 4). Tính f(3, 1).

1. Viết (3, 1) = a(1, 1) + b(1, -1): a + b = 3, a - b = 1, nên a = 2, b = 1.
2. f giữ tổ hợp: f(3, 1) = 2 f(1, 1) + 1 f(1, -1).
3. = (4, 0) + (0, 4) = (4, 4).

$$ f(u + v) = f(u) + f(v), \qquad f(ku) = k f(u) $$

> Lỗi thường gặp: lấy luôn hệ số (2, 1) làm f(3, 1). Đó là tọa độ của (3, 1); ảnh phải tính qua f(1, 1) và f(1, -1).

:::check
Q: f tuyến tính và f(2, 4) = (6, -2). Tính f(1, 2) và f(0, 0).
A: (1, 2) = (1/2)(2, 4), nên f(1, 2) = (3, -1). Còn f(0, 0) = (0, 0) với mọi ánh xạ tuyến tính.
:::

## Nhân Ker f và ảnh Im f

:::hook
Một mô hình nén ảnh là một ánh xạ. Những gì nó đè về 0 là thông tin mất vĩnh viễn (nhân); những gì nó tạo ra được là mọi bản nén có thể có (ảnh).
:::

:::figure map
caption: f(x, y, z) = (x - y, y - z): mọi bội của (1, 1, 1) rơi vào 0 (đỏ), đó là Ker f. Các điểm được trúng tạo thành Im f.
col "R^3" "(1, 1, 1)" "(2, 2, 2)" "(1, 0, 0)" "(0, 1, 0)"
col "R^2" "(0, 0)" "(1, 0)" "(-1, 1)"
gap 1 "f"
"(1, 1, 1)" -> "(0, 0)" do
"(2, 2, 2)" -> "(0, 0)" do
"(1, 0, 0)" -> "(1, 0)"
"(0, 1, 0)" -> "(-1, 1)"
:::

:::core
Ker f là mọi thứ bị f đè về 0, Im f là mọi thứ f tạo ra được; với f(x) = Ax, Ker là nghiệm của Ax = 0, Im là span các cột của A.
:::

Cả hai là không gian con. f đơn ánh đúng khi Ker f = {0}. Cơ sở của Im lấy các cột có trụ của CHÍNH A.

Ví dụ: A có hàng (1, 2, 1), (0, 1, 1), (1, 3, 2), f(x) = Ax.

1. Hàng 3 = hàng 1 + hàng 2: khử còn x + 2y + z = 0, y + z = 0.
2. z = t cho y = -t, x = t: Ker f = span{(1, -1, 1)}.
3. Trụ ở cột 1, 2: Im f = span{(1, 0, 1), (2, 1, 3)}, mặt phẳng z = x + y.

$$ \text{Ker} f = \{v : f(v) = 0\}, \qquad \text{Im} f = \{f(v) : v \in V\} $$

> Lỗi thường gặp: lấy hàng của dạng bậc thang làm cơ sở của Im f. Biến đổi hàng làm đổi không gian cột; phải lấy cột của A ban đầu.

:::check
Q: f(x, y) = (x + 2y, 2x + 4y). Im f là gì? (3, 6) có thuộc Im f không?
A: f(x, y) = (x + 2y)(1, 2), nên Im f = span{(1, 2)}. (3, 6) = 3(1, 2) = f(3, 0): thuộc.
:::

## Định lý số chiều

:::hook
Nén ảnh 1000 chiều xuống 50 chiều thì ít nhất 950 chiều thông tin phải bị đè về 0. Định lý số chiều là luật bảo toàn đó.
:::

:::figure plane
caption: Chiếu (x, y) -> (x, 0): trục y bị đè về 0 (Ker, 1 chiều), trục x sống sót (Im, 1 chiều). 1 + 1 = 2.
size: 150 100
x: -2.5 2.5 5
y: -2 2 5
line 0 0 0 1 do "Ker" pos=e
line 0 0 1 0 xanh
text -1.8 -0.4 "Im"
vector 0 0 1.5 1.5 muc "v" pos=e
segment 1.5 1.5 1.5 0 muc dash
point 1.5 0 xanh
:::

:::core
Mỗi chiều của không gian nguồn hoặc bị đè về 0, hoặc sống sót thành một chiều của ảnh: dim Ker + dim Im = dim nguồn.
:::

Với f(x) = Ax: dim Im f = rank A. f: R^n -> R^m đơn ánh cần n <= m, toàn ánh cần n >= m. Khi n = m, đơn ánh, toàn ánh, song ánh là một.

Ví dụ: f(x, y, z, t) = (x - y, z + t, x - y + z + t), từ R^4 vào R^3.

1. Hàng 3 = hàng 1 + hàng 2, nên rank A = 2 = dim Im f.
2. dim Ker f = 4 - 2 = 2.
3. dim Im f = 2 < 3: f không toàn ánh.

$$ \text{dim} \, \text{Ker} f + \text{dim} \, \text{Im} f = \text{dim} \, V $$

> Lỗi thường gặp: dùng số chiều của không gian ĐÍCH trong định lý. Vế phải là số chiều của không gian nguồn (số cột của A).

:::check
Q: Có ánh xạ tuyến tính từ R^3 lên toàn R^4 không? Có ánh xạ đơn ánh từ R^4 vào R^3 không?
A: Không cả hai: dim Im <= 3 < 4; và dim Ker = 4 - dim Im >= 1, nên không đơn ánh.
:::

## Ma trận của ánh xạ tuyến tính

:::hook
GPU không hiểu "xoay 30 độ", nó chỉ nhân ma trận. Muốn đưa một phép biến hình vào máy, phải ghi nó thành một bảng số.
:::

:::figure grid
caption: f(x, y) = (x + 2y, 3x, x - y). Cột 1 là f(1, 0), cột 2 là f(0, 1).
style: matrix
table "A"
head "f(e1)" "f(e2)"
row 1 2
row 3 0
row 1 -1
mark col 1 xanh
mark col 2 vang
:::

:::core
Cột j của ma trận là ảnh của vectơ cơ sở thứ j, viết bằng tọa độ trong cơ sở đích: ma trận là sổ ghi f làm gì với từng vectơ cơ sở.
:::

Ánh xạ R^n -> R^m cho ma trận cỡ m x n. Cơ sở đích chính tắc thì cột chính là f(b_j); cơ sở đích khác thì phải đổi f(b_j) ra tọa độ.

Ví dụ: f(p) = x p' trên đa thức bậc <= 2, cơ sở 1, x, x^2.

1. f(1) = 0, f(x) = x, f(x^2) = 2x^2.
2. Tọa độ: (0, 0, 0), (0, 1, 0), (0, 0, 2).
3. Đặt làm cột: ma trận chéo với đường chéo 0, 1, 2.

$$ [f(v)]_{C} = A \, [v]_{B} $$

> Lỗi thường gặp: đặt ảnh f(b_j) làm HÀNG. Hàng là chuyển vị, sai; mỗi vectơ cơ sở cho một CỘT.

:::check
Q: f(x, y) = (y, x). Ma trận của f trong cơ sở b1 = (1, 1), b2 = (1, -1) (dùng cho cả hai phía) là gì?
A: f(b1) = (1, 1) = b1, tọa độ (1, 0); f(b2) = (-1, 1) = -b2, tọa độ (0, -1). Ma trận [1, 0; 0, -1].
:::

## Hợp ánh xạ và tích ma trận

:::hook
Một ảnh đi qua nhiều lớp biến đổi liên tiếp. Gộp các lớp tuyến tính lại thành một phép chỉ là nhân các ma trận, nhưng phải đúng thứ tự.
:::

:::figure flow
caption: Làm f trước nên A_f đứng sát x; ma trận của g o f là A_g A_f, đọc từ phải sang trái.
box "x"
link "A_f"
box "f(x)" xanh
link "A_g"
box "g(f(x))" luc
:::

:::core
Làm f rồi làm g ứng với tích A_g A_f, ma trận của phép làm sau đứng bên trái; phép làm ngược f^(-1) ứng với A_f^(-1).
:::

f là đẳng cấu (song ánh tuyến tính) khi ma trận vuông của nó có det khác 0. det = 0 thì f đè bẹp gì đó, không làm ngược được.

Ví dụ: f(x, y) = (y, x), g(x, y) = (x, x + y). Tìm ma trận của g o f.

1. A_f = [0, 1; 1, 0], A_g = [1, 0; 1, 1].
2. A_g A_f = [0, 1; 1, 1].
3. Thử: g(f(x, y)) = g(y, x) = (y, y + x). Khớp. Còn f o g có ma trận A_f A_g = [1, 1; 1, 0], khác.

$$ A_{g \circ f} = A_{g} A_{f} $$

$$ A_{f^{-1}} = (A_{f})^{-1}, \qquad (g \circ f)^{-1} = f^{-1} \circ g^{-1} $$

> Lỗi thường gặp: lấy chuyển vị A^T thay cho nghịch đảo A^(-1) khi tìm ánh xạ ngược. Hai cái chỉ trùng nhau với phép quay, phép lật.

:::check
Q: f(x, y) = (x + y, y). Tìm f^(-1).
A: A = [1, 1; 0, 1], det 1, A^(-1) = [1, -1; 0, 1], nên f^(-1)(x, y) = (x - y, y). Thử: f(x - y, y) = (x, y).
:::

## Đổi cơ sở và ma trận đồng dạng

:::hook
PCA chọn hệ trục mới theo hướng dữ liệu trải dài. Trong hệ trục khéo chọn, một phép biến hình rối rắm chỉ còn là kéo giãn dọc từng trục.
:::

:::figure flow
caption: P^(-1) A P đọc từ phải sang trái: đổi tọa độ B sang tọa độ thường (P), làm f (A), đổi về B (P^(-1)).
box "[v]_B"
link "P"
box "v"
link "A"
box "f(v)" xanh
link "P^(-1)"
box "[f(v)]_B" luc
:::

:::core
Đổi cơ sở không đổi phép biến hình, chỉ đổi cách ghi: B = P^(-1) A P, với các cột của P là vectơ cơ sở mới.
:::

A và B = P^(-1) A P gọi là đồng dạng: cùng định thức, cùng vết, cùng hạng. Chọn cơ sở là các vectơ mà A chỉ kéo giãn thì B là ma trận chéo.

Ví dụ: A = [3, 1; 0, 2], cơ sở mới b1 = (1, 0), b2 = (1, -1).

1. P = [1, 1; 0, -1], AP = [3, 2; 0, -2].
2. det P = -1, P^(-1) = [1, 1; 0, -1].
3. B = P^(-1)(AP) = [3, 0; 0, 2]: A chỉ giãn b1 gấp 3, b2 gấp 2.

$$ B = P^{-1} A P $$

> Lỗi thường gặp: tính (AP)P^(-1). Thứ tự đó trả lại đúng A; P^(-1) phải đứng bên trái.

:::check
Q: A có det A = 6, tr A = 5. B = P^(-1) A P có định thức và vết bao nhiêu?
A: Vẫn 6 và 5: hai ma trận ghi cùng một phép biến hình, chỉ khác cơ sở.
:::
