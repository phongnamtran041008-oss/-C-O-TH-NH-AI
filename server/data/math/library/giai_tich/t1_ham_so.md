---
id: gt_lib_t1
title_vi: Hàm số, hàm hợp, hàm ngược và hàm sơ cấp
subject: giai_tich
floor: 1
format: 2
summary_vi: Hàm số là cỗ máy nhận một số, trả đúng một số: máy nhận được những số nào, soi gương hay lặp lại, nối hai máy, chạy ngược một máy, và các máy quen mặt nhất.
skills: [gt_t1_ham_so, gt_t1_tinh_chat_ham, gt_t1_ham_hop, gt_t1_ham_nguoc, gt_t1_ham_so_cap]
---
## Hàm số và tập xác định

:::hook
Bấm nút A3 trên máy bán nước thì ra đúng một chai. Nếu cùng một nút lúc ra trà, lúc ra cà phê, máy đã hỏng. Hàm số là cỗ máy không bao giờ hỏng kiểu ấy.
:::

:::figure map
caption: Mỗi x ra đúng một mũi tên: f(x) = x^2 là hàm số. Hai x chung một đích (-1 và 1) vẫn được.
col "x" -1 0 1 2
col "f(x)" 0 1 4
gap 1 "f"
-1 -> 1
0 -> 0
1 -> 1
2 -> 4
:::

:::core
Hàm số là cỗ máy: mỗi x được nhận vào cho ra đúng một số f(x). Tập xác định là mọi x mà máy chạy được.
:::

Thay số âm thì đặt trong ngoặc: f(x) = x^2 - 3x cho f(-1) = (-1)^2 - 3 . (-1) = 4.

:::check
Q: f(x + 2) = 3x - 1 với mọi x. Tính f(5).
A: Cần x + 2 = 5, tức x = 3. Khi đó f(5) = 3 . 3 - 1 = 8.
:::

### Tập xác định

Máy kẹt ở ba chỗ: mẫu số bằng 0, số âm dưới căn bậc hai, ln (hay log) của một số <= 0.

:::figure numberline
caption: Tập xác định của sqrt(x + 2)/(x - 1): từ -2 trở đi (lấy cả -2), khoét bỏ điểm 1.
range: -3 3 1
interval -2 inf [ xanh
point 1 do "x = 1" open
:::

Ví dụ: tìm tập xác định của f(x) = sqrt(x + 2)/(x - 1).

1. Căn cần x + 2 >= 0, tức x >= -2. Lấy cả -2 vì sqrt(0) = 0.
2. Mẫu cần x - 1 khác 0, tức x khác 1.
3. Giữ phần chung: [-2, 1) hợp (1, +vô cùng), đúng như trục số.

Hai hàm chỉ bằng nhau khi cùng tập xác định và cùng giá trị: (x^2 - 1)/(x - 1) không xác định tại 1, nên khác x + 1.

> Lỗi thường gặp: viết điều kiện dưới căn là > 0 rồi đánh rơi đầu mút. Căn của 0 vẫn có nghĩa; chỉ ln 0 mới không.

:::check
Q: Tìm tập xác định của g(x) = ln(3 - x).
A: ln cần 3 - x > 0, tức x < 3: tập xác định là (-vô cùng, 3). Điểm 3 bị loại vì ln 0 không có nghĩa.
:::

## Hàm chẵn, hàm lẻ, hàm tuần hoàn

:::hook
Lật ngang ảnh một con mèo, nó vẫn là con mèo: máy học dùng phép soi gương này để có thêm dữ liệu. Hàm chẵn là hàm soi gương.
:::

:::figure plane
caption: Chẵn: f(-1.5) = f(1.5).
size: 120 66
x: -2 2 1
y: -0.5 4 1
curve "x^2" xanh
segment -1.5 2.25 1.5 2.25 xam dash
point -1.5 2.25 do
point 1.5 2.25 do
:::

:::figure plane
caption: Lẻ: f(-1) = -f(1).
size: 120 66
x: -1.6 1.6 1
y: -3 3 1
curve "x^3" luc
segment -1 -1 1 1 xam dash
point -1 -1 do
point 1 1 do
:::

:::core
Thay -x vào rồi so: f(-x) = f(x) là chẵn (soi gương qua trục tung), f(-x) = -f(x) là lẻ (đối xứng qua gốc).
:::

Ví dụ: xét tính chẵn lẻ của f(x) = x^3 + x + 2.

1. f(-x) = -x^3 - x + 2.
2. So với f(x) = x^3 + x + 2: khác. So với -f(x) = -x^3 - x - 2: khác ở hằng số.
3. Thử số cho chắc: f(1) = 4, f(-1) = 0, khác cả 4 lẫn -4. Không chẵn, không lẻ.

> Lỗi thường gặp: bỏ ngoặc khi tính -f(x). Viết hẳn -(x^3 + x + 2) = -x^3 - x - 2 rồi mới so.

:::check
Q: f(x) = x^2 . sin x + x^4 chẵn, lẻ hay không?
A: f(1) = 1 + sin 1, f(-1) = 1 - sin 1: không bằng nhau, cũng không đối nhau, nên không chẵn cũng không lẻ.
:::

### Mẹo nhanh và hàm tuần hoàn

Đa thức chỉ có mũ chẵn (kể cả hằng số) thì chẵn, chỉ có mũ lẻ thì lẻ. Nhân như dấu: lẻ . lẻ = chẵn, chẵn . lẻ = lẻ; vì thế x^2 . sin x là lẻ. Hàm lẻ xác định tại 0 thì f(0) = 0.

:::figure plane
caption: sin 2x lặp lại sau mỗi đoạn dài pi, đúng bằng 2pi/2.
size: 200 70
x: 0 6.6 1
y: -1.4 1.6 1
curve "sin(2*x)" xanh
segment 0 1.3 pi 1.3 do "T = pi" pos=n
segment pi 1.3 6.283 1.3 tim "T = pi" pos=n
:::

Hàm tuần hoàn lặp lại như bốn mùa: chu kỳ T thỏa f(x + T) = f(x) với mọi x, cứ đi thêm T thì đồ thị lặp lại y hệt. sin và cos lặp sau 2pi, tan lặp sau pi. Nhân x với a thì chu kỳ chia cho |a|, còn cộng thêm b chỉ dịch đồ thị sang ngang.

$$ T_{\sin(ax+b)} = T_{\cos(ax+b)} = \frac{2\pi}{|a|}, \qquad T_{\tan(ax+b)} = \frac{\pi}{|a|} $$

:::check
Q: Chu kỳ của cos(3x - 1) là bao nhiêu? Còn của tan(x/2)?
A: cos(3x - 1): 2pi/3. tan(x/2): a = 1/2, nên chu kỳ là pi/(1/2) = 2pi.
:::

## Hàm hợp

:::hook
Ảnh đi vào lớp thứ nhất của mạng nơ-ron, kết quả lại đi vào lớp thứ hai. Cả mạng là một hàm hợp: đầu ra của khâu trước là đầu vào của khâu sau.
:::

:::figure flow
caption: f(g(1)): g làm trước. Với g(x) = x^2 + 2, f(x) = 3x - 1 được 8.
box "x = 1"
link "g"
box "g(1) = 3" xanh
link "f"
box "f(3) = 8" luc
:::

:::figure flow
caption: Đổi thứ tự, g(f(1)) ra 6: dây chuyền khác, kết quả khác.
box "x = 1"
link "f"
box "f(1) = 2" luc
link "g"
box "g(2) = 6" xanh
:::

:::core
f(g(x)) là dây chuyền: làm g trước, đưa kết quả cho f. Đổi thứ tự là đổi dây chuyền, và thường ra kết quả khác.
:::

$$ (f \circ g)(x) = f(g(x)) $$

Ví dụ: f(x) = 3x - 1, g(x) = x^2 + 2. Tìm công thức f(g(x)).

1. f nhân 3 rồi trừ 1, nên f(g(x)) = 3 . (g(x)) - 1, giữ nguyên ngoặc.
2. Thay g(x): 3(x^2 + 2) - 1.
3. Nhân vào cả hai số hạng: 3x^2 + 6 - 1 = 3x^2 + 5.

> Lỗi thường gặp: nhân phân phối sót số hạng, viết 3(x^2 + 2) thành 3x^2 + 2.

:::check
Q: f(x) = 2x + 1 và f(g(x)) = 4x - 3 với mọi x. Tìm g(x).
A: f(g(x)) = 2g(x) + 1 = 4x - 3, nên g(x) = 2x - 2.
:::

### Nhìn ra hàm trong, hàm ngoài

:::figure flow
caption: sin(x^2): bình phương là hàm trong, làm trước; sin là hàm ngoài, làm sau.
box "x"
link "bình phương"
box "x^2" xanh
link "sin"
box "sin(x^2)" luc
:::

Nhìn ra hàm hợp cũng là một kỹ năng: hỏi xem với một x cụ thể, bước nào phải làm trước. sin(x^2) có hàm trong x^2 và hàm ngoài sin. Tập xác định của hàm hợp: x phải vào được g, rồi g(x) phải vào được f. Chẳng hạn sqrt(x - 4) có hàm trong x - 4 và hàm ngoài là căn, nên cần x - 4 >= 0, tức x >= 4.

:::check
Q: Trong ln(x^2 + 1), hàm trong và hàm ngoài là gì? Hàm xác định ở đâu?
A: Hàm trong x^2 + 1, hàm ngoài ln. Vì x^2 + 1 >= 1 > 0 với mọi x, hàm xác định trên cả R.
:::

## Hàm ngược

:::hook
Mã hóa một tin nhắn thì phải giải mã được; đổi độ C ra độ F thì phải đổi về được. Hàm ngược là nút hoàn tác: từ kết quả, lần về đúng đầu vào.
:::

:::figure flow
caption: f(x) = 2x + 1 nhân 2 rồi cộng 1; f^(-1) làm ngược từng bước theo thứ tự ngược: trừ 1 rồi chia 2.
box "1"
link "nhân 2, cộng 1"
box "3" xanh
link "trừ 1, chia 2"
box "1" luc
:::

:::core
f^(-1) chạy ngược f: f(a) = b thì f^(-1)(b) = a. Nó chỉ có khi mỗi đầu ra đến từ đúng một đầu vào.
:::

$$ f^{-1}(y) = x \;\Leftrightarrow\; f(x) = y $$

Ví dụ: f(x) = (x + 2)/(x - 1) có hàm ngược. Tính f^(-1)(3).

1. f^(-1)(3) là số x mà f(x) = 3.
2. Nhân chéo: x + 2 = 3(x - 1) = 3x - 3.
3. Gom x: 2x = 5, nên x = 5/2. Thử: f(5/2) = 4.5/1.5 = 3.

> Lỗi thường gặp: hiểu f^(-1)(x) là 1/f(x). Dấu -1 ở đây là "chạy ngược", không phải nghịch đảo một số.

:::check
Q: f có hàm ngược và f(5) = -1. Tính f^(-1)(-1) và 1/f(5).
A: f^(-1)(-1) = 5 (chạy ngược), còn 1/f(5) = -1. Hai thứ khác hẳn nhau.
:::

### Tìm công thức hàm ngược

:::figure plane
caption: Điểm (1, 3) của f đổi thành (3, 1) của f^(-1): hai đồ thị soi gương qua y = x.
size: 110 100
aspect: equal
x: -1 4 1
y: -1 4 1
line 0 0 1 1 xam dash "y = x" pos=se
curve "2*x + 1" xanh "f" pos=w
curve "(x - 1)/2" luc "f^-1" pos=se
point 1 3 do "(1, 3)" pos=e
point 3 1 do "(3, 1)" pos=s
:::

Muốn cả công thức: viết y = f(x), giải ra x, đổi tên y thành x. Đổi tên x với y chính là soi gương qua y = x như trong hình. f(x) = 4x - 2 cho x = (y + 2)/4, nên f^(-1)(x) = (x + 2)/4. Hàm x^2 trên R không có hàm ngược vì f(2) = f(-2); chỉ lấy x >= 0 thì có, và đó là sqrt(x).

:::check
Q: Tìm công thức hàm ngược của f(x) = 3x + 6.
A: y = 3x + 6 cho x = (y - 6)/3. Đổi tên: f^(-1)(x) = (x - 6)/3. Thử: f(1) = 9 và f^(-1)(9) = 1.
:::

## Các hàm sơ cấp cơ bản

:::hook
Decibel đo tiếng ồn, độ pH, độ Richter đều dùng log: log biến "gấp 10 lần" thành "cộng thêm 1". Hàm mất mát cross-entropy của máy học cũng là một log.
:::

:::figure plane
caption: e^x và ln x là cặp hàm ngược, soi gương qua y = x. e^x luôn dương; ln x chỉ sống khi x > 0.
size: 150 108
aspect: equal
x: -2.5 3.5 1
y: -2.5 3.5 1
line 0 0 1 1 xam dash
curve "exp(x)" xanh "e^x" pos=w
curve "ln(x)" luc "ln x" pos=se
point 0 1 do "(0, 1)" pos=nw
point 1 0 do "(1, 0)" pos=se
:::

:::core
log_a(N) là số mũ phải đặt lên a để được N. Nó là hàm ngược của a^x, nên chỉ nhận N > 0.
:::

Ví dụ: giải log_3(x - 1) = 2.

1. Điều kiện: x - 1 > 0.
2. log_3(A) = 2 nghĩa là A = 3^2 = 9.
3. x - 1 = 9, nên x = 10; thỏa điều kiện.

ln là log cơ số e, nên ln(e^t) = t. Phương trình mũ thì đưa về cùng cơ số rồi so số mũ: 3^(x - 1) = 27 cho x - 1 = 3.

:::check
Q: Giải 2^(x + 1) = 16.
A: 16 = 2^4, nên x + 1 = 4 và x = 3.
:::

### Quy tắc log

Log biến nhân thành cộng, chia thành trừ: đó là lý do người ta cộng log thay cho nhân những xác suất rất nhỏ.

$$ \log_a(xy) = \log_a x + \log_a y, \qquad \log_a \frac{x}{y} = \log_a x - \log_a y $$

Ví dụ: giải log_2 x + log_2(x - 2) = 3.

1. Điều kiện: x > 0 và x - 2 > 0, tức x > 2.
2. Gộp: log_2(x(x - 2)) = 3, nên x(x - 2) = 2^3 = 8.
3. x^2 - 2x - 8 = 0 cho x = 4 hoặc x = -2. Loại -2 vì x > 2, còn x = 4.

> Lỗi thường gặp: giải xong quên đối chiếu điều kiện. ln x + ln(x - 1) = ln 2 cho x = 2 hoặc x = -1, nhưng -1 làm ln vô nghĩa, phải loại.

:::check
Q: Tính log_2(40) - log_2(5).
A: log_2(40/5) = log_2(8) = 3.
:::

### Lượng giác ngược

:::figure grid
caption: Lượng giác ngược nhận số nào, trả góc trong khoảng nào.
table
head "hàm" "nhận x trong" "trả góc trong"
row "arcsin" "[-1, 1]" "[-pi/2, pi/2]"
row "arccos" "[-1, 1]" "[0, pi]"
row "arctan" "R" "(-pi/2, pi/2)"
:::

arcsin, arccos, arctan chạy ngược sin, cos, tan. Vì sin lặp lại nên nhiều góc cho cùng một sin; để có hàm ngược, góc trả về bị khóa trong một khoảng như bảng trên. Vì thế arcsin(sin x) = x chỉ đúng khi x thuộc [-pi/2, pi/2].

:::check
Q: Tính arccos(1/2) và arcsin(sin pi).
A: arccos(1/2) = pi/3, vì cos(pi/3) = 1/2 và pi/3 thuộc [0, pi]. sin pi = 0 nên arcsin(sin pi) = arcsin 0 = 0, không phải pi.
:::
