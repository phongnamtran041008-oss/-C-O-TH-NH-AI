---
id: gt_lib_t1
title_vi: Hàm số, hàm hợp, hàm ngược và hàm sơ cấp
subject: giai_tich
floor: 1
summary_vi: Một hàm số là một quy tắc gán; biết nó gán cho những số nào, ghép hai quy tắc lại, đi ngược một quy tắc, và làm quen với các hàm quen mặt nhất.
skills: [gt_t1_ham_so, gt_t1_tinh_chat_ham, gt_t1_ham_hop, gt_t1_ham_nguoc, gt_t1_ham_so_cap]
---
## Hàm số và tập xác định

Một hàm số f từ tập X vào R là một quy tắc gán cho mỗi số x thuộc X đúng một số thực f(x). Hai chữ quan trọng là "mỗi" và "đúng một": số nào trong X cũng có ảnh, và không số nào có hai ảnh.

$$ f : X \to \mathbb{R}, \quad x \mapsto f(x) $$

Tính giá trị của hàm tại một điểm thì thay số đó vào mọi chỗ có x. Ví dụ f(x) = x^2 - 3x thì f(-1) = 1 + 3 = 4. Nhớ đặt số âm trong ngoặc trước khi bình phương.

Khi hàm chỉ cho bằng công thức, tập xác định là tập mọi x làm công thức có nghĩa. Có ba điều kiện hay gặp:

- Mẫu số phải khác 0.
- Biểu thức dưới căn bậc hai phải không âm.
- Biểu thức trong ln (hay log) phải dương.

Ví dụ với f(x) = sqrt(x - 1) / (x - 3):

1. Căn có nghĩa khi x - 1 >= 0, tức x >= 1.
2. Mẫu khác 0 khi x khác 3.
3. Lấy giao: tập xác định là [1, 3) hợp (3, +vô cùng).

Hai hàm số chỉ bằng nhau khi chúng có cùng tập xác định và cùng giá trị tại mọi điểm. Vì vậy (x^2 - 1)/(x - 1) và x + 1 là hai hàm khác nhau: hàm thứ nhất không xác định tại 1.

> Lỗi thường gặp: quên dấu bằng. Căn bậc hai của 0 vẫn có nghĩa, nên điều kiện dưới căn là >= 0, không phải > 0. Ngược lại, ln 0 không có nghĩa.

## Hàm chẵn, hàm lẻ, hàm tuần hoàn

Cho f xác định trên một tập đối xứng qua 0 (có x thì có -x). So f(-x) với f(x):

$$ f(-x) = f(x) \;\Rightarrow\; f \text{ chan}, \qquad f(-x) = -f(x) \;\Rightarrow\; f \text{ le} $$

Đồ thị hàm chẵn đối xứng qua trục tung, đồ thị hàm lẻ đối xứng qua gốc tọa độ. Với đa thức, nhìn số mũ là biết: chỉ có số mũ chẵn (kể cả hằng số) thì chẵn, chỉ có số mũ lẻ thì lẻ, lẫn lộn thì không chẵn không lẻ.

- cos x, x^2, |x| là hàm chẵn; sin x, tan x, x^3 là hàm lẻ.
- Tích hai hàm lẻ là hàm chẵn; tích một hàm chẵn và một hàm lẻ là hàm lẻ.
- Một hàm lẻ xác định tại 0 thì f(0) = 0, vì f(0) = -f(0).

Muốn chứng tỏ một hàm không chẵn không lẻ, chỉ cần một ví dụ số: với f(x) = x^3 - x + 1 có f(2) = 7 và f(-2) = -5, khác cả 7 lẫn -7.

Hàm f tuần hoàn nếu có số T > 0 với f(x + T) = f(x) cho mọi x. Số T dương nhỏ nhất như vậy là chu kỳ cơ sở. sin và cos có chu kỳ 2pi, tan có chu kỳ pi. Nhân biến với a thì chu kỳ chia cho |a|:

$$ \sin(ax + b) \text{ co chu ky } \frac{2\pi}{|a|} $$

> Lỗi thường gặp: bỏ ngoặc sai dấu khi tính -f(x). Viết hẳn -(x^3 - x + 1) = -x^3 + x - 1 rồi mới so sánh.

## Hàm hợp

Hàm hợp của f và g, viết f o g, là làm g trước rồi làm f với kết quả đó:

$$ (f \circ g)(x) = f(g(x)) $$

Tính giá trị thì đi từ trong ra ngoài. Ví dụ f(x) = 3x - 2, g(x) = x^2, h(x) = x + 1, tính f(g(h(1))):

1. h(1) = 2.
2. g(2) = 4.
3. f(4) = 10.

Lập công thức thì thay cả biểu thức của hàm trong vào chỗ x của hàm ngoài, giữ nguyên dấu ngoặc. Với f(x) = x^2 + 1 và g(x) = 2x - 3: g(f(x)) = 2(x^2 + 1) - 3 = 2x^2 - 1.

Thứ tự rất quan trọng: nói chung f(g(x)) khác g(f(x)). Với f(x) = x + 1 và g(x) = 2x thì f(g(x)) = 2x + 1 còn g(f(x)) = 2x + 2.

Ngược lại, nhận ra một hàm là hàm hợp giúp tính toán về sau (nhất là khi lấy đạo hàm). sin(x^2) là f(g(x)) với hàm trong g(x) = x^2 và hàm ngoài f(x) = sin x.

Hàm hợp chỉ xác định tại những x mà g(x) xác định và g(x) lại thuộc tập xác định của f. Ví dụ sqrt(x - 4) cần x >= 4.

> Lỗi thường gặp: nhân phân phối sót số hạng, như viết 2(x^2 + 1) thành 2x^2 + 1.

## Hàm ngược

Nếu f là song ánh từ X lên Y (mỗi y thuộc Y là ảnh của đúng một x), thì có hàm ngược f^(-1) đi từ Y về X:

$$ f^{-1}(y) = x \;\Leftrightarrow\; f(x) = y $$

Một hàm tăng ngặt hoặc giảm ngặt trên một khoảng thì là đơn ánh trên khoảng đó. Hàm x^2 trên R không có hàm ngược (f(2) = f(-2)), nhưng thu hẹp về [0, +vô cùng) thì có, và hàm ngược là sqrt(x).

Cách tìm công thức của hàm ngược:

1. Viết y = f(x).
2. Giải phương trình theo x.
3. Đổi tên y thành x.

Ví dụ f(x) = (x + 1)/(x - 2): nhân chéo y(x - 2) = x + 1, gom x(y - 1) = 2y + 1, nên f^(-1)(x) = (2x + 1)/(x - 1). Kiểm tra lại bằng một số: f(3) = 4 và f^(-1)(4) = 3.

Đồ thị của f và của f^(-1) đối xứng nhau qua đường thẳng y = x, vì điểm (a, b) đổi thành (b, a).

> Lỗi thường gặp: nhầm f^(-1)(x) với 1/f(x). Dấu -1 ở đây là "hàm ngược", không phải nghịch đảo của một số.

## Các hàm sơ cấp cơ bản

Các hàm sơ cấp cơ bản là lũy thừa, mũ, lôgarit, lượng giác và lượng giác ngược; ghép chúng bằng cộng, trừ, nhân, chia và lấy hàm hợp ta được các hàm sơ cấp.

Hàm mũ a^x (a > 0, a khác 1) xác định trên R và luôn dương. Lôgarit là hàm ngược của nó, chỉ xác định khi biến dương:

$$ y = \log_a x \;\Leftrightarrow\; a^{y} = x, \quad x > 0 $$

Các quy tắc lôgarit hay dùng, với x, y > 0:

$$ \log_a(xy) = \log_a x + \log_a y, \qquad \log_a \frac{x}{y} = \log_a x - \log_a y $$

Ví dụ log_2(12) - log_2(3) = log_2(4) = 2. ln là lôgarit cơ số e, nên ln(e^t) = t.

Các hàm lượng giác ngược trả về một góc trong một khoảng cố định:

- arcsin x xác định trên [-1, 1], cho góc trong [-pi/2, pi/2].
- arccos x xác định trên [-1, 1], cho góc trong [0, pi].
- arctan x xác định trên R, cho góc trong (-pi/2, pi/2).

Ví dụ arcsin(1/2) = pi/6, arccos(-1) = pi, arctan(1) = pi/4. Vì khoảng giá trị bị giới hạn, arcsin(sin x) = x chỉ đúng khi x thuộc [-pi/2, pi/2].

> Lỗi thường gặp: giải phương trình lôgarit xong quên đối chiếu điều kiện. Với ln x + ln(x - 1) = ln 2, nghiệm x = -1 của phương trình bậc hai phải bị loại.
