---
id: gt_lib_t2
title_vi: Dãy số, giới hạn, vô cùng bé và vô cùng lớn
subject: giai_tich
floor: 2
summary_vi: Giới hạn là con số mà một đại lượng tiến sát tới; học cách tìm nó cho dãy số và cho hàm số, khử các dạng vô định, và dùng vô cùng bé tương đương để tính nhanh.
skills: [gt_t2_gioi_han_day, gt_t2_gioi_han_ham, gt_t2_gioi_han_vo_cuc, gt_t2_gioi_han_dac_biet, gt_t2_vo_cung_be]
---
## Giới hạn của dãy số

Dãy u_n có giới hạn L khi các số hạng tiến sát L tùy ý, miễn là n đủ lớn: với mọi số dương epsilon, từ một lúc nào đó trở đi |u_n - L| < epsilon.

$$ \lim_{n \to \infty} u_n = L $$

Hai giới hạn nền tảng, mọi bài khác đều quy về chúng:

$$ \lim_{n \to \infty} \frac{1}{n^{k}} = 0 \;(k > 0), \qquad \lim_{n \to \infty} q^{n} = 0 \;(|q| < 1) $$

Với phân thức của n, chia cả tử và mẫu cho lũy thừa cao nhất của mẫu. Ví dụ (3n + 1)/(n - 2):

1. Chia cho n: (3 + 1/n) / (1 - 2/n).
2. 1/n và 2/n dần tới 0.
3. Giới hạn bằng 3/1 = 3.

Với lũy thừa mũ như 4^n và 2^n, chia cho lũy thừa có cơ số lớn nhất; phần còn lại có dạng (2/4)^n, dần tới 0.

Khi có hiệu hai căn kiểu sqrt(n^2 + 4n) - n, nhân và chia cho biểu thức liên hợp để biến hiệu thành thương: sqrt(n^2 + 4n) - n = 4n / (sqrt(n^2 + 4n) + n), dần tới 2.

Một dãy có |u_n| dần tới 0 thì chính nó dần tới 0, nên (-1)^n / n dần tới 0. Còn (-1)^n thì nhảy giữa -1 và 1, không có giới hạn.

> Lỗi thường gặp: chia tử và mẫu cho lũy thừa không phải cao nhất của mẫu, rồi quên rằng phần còn lại ở mẫu vẫn dần ra vô cùng.

## Giới hạn hàm số tại một điểm

Giới hạn của f khi x -> a nói về các giá trị f(x) khi x gần a mà khác a. Giá trị f(a), nếu có, không tham gia.

Bước đầu tiên luôn là thử thay x = a. Nếu hàm là đa thức, phân thức có mẫu khác 0 tại a, hay một hàm sơ cấp xác định tại a, thì giới hạn chính là giá trị đó.

Nếu thay số ra dạng 0/0, đó là dạng vô định: phải biến đổi rồi mới thay. Hai cách hay dùng:

- Phân tích tử và mẫu thành nhân tử, rút gọn thừa số chung (x - a).
- Có căn thì nhân với biểu thức liên hợp.

$$ \lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = \lim_{x \to 3} (x + 3) = 6 $$

Ví dụ có căn, giới hạn của (sqrt(x + 4) - 2)/x khi x -> 0:

1. Nhân tử và mẫu với sqrt(x + 4) + 2.
2. Tử thành (x + 4) - 4 = x, biểu thức còn 1 / (sqrt(x + 4) + 2).
3. Thay x = 0 được 1/4.

> Lỗi thường gặp: phân tích sai nhân tử. Luôn nhân ngược lại để kiểm tra: (x - 2)(x - 1) = x^2 - 3x + 2.

## Giới hạn ở vô cùng và giới hạn vô cùng

Khi x -> +vô cùng hay x -> -vô cùng, với phân thức P(x)/Q(x) chỉ cần so bậc:

- Bậc của P nhỏ hơn bậc của Q: giới hạn bằng 0.
- Bậc bằng nhau: giới hạn bằng tỉ số hai hệ số cao nhất.
- Bậc của P lớn hơn: giới hạn là vô cùng (dấu tùy hệ số và hướng của x).

Lý do vẫn là chia tử và mẫu cho lũy thừa cao nhất của mẫu. Ví dụ (5 - 3x)/(2x + 1) dần tới -3/2.

Giới hạn bằng vô cùng xảy ra khi mẫu dần tới 0 còn tử dần tới một số khác 0. Lúc đó phải xem dấu ở từng phía:

$$ \lim_{x \to 0} \frac{1}{x^{2}} = +\infty $$

Nhưng với 1/(x - 1) khi x -> 1, bên phải ra +vô cùng, bên trái ra -vô cùng: không có giới hạn. Muốn nói "giới hạn bằng +vô cùng" thì cả hai phía phải cùng ra +vô cùng.

Dạng vô cùng trừ vô cùng, như sqrt(x^2 + 2x) - x khi x -> +vô cùng, lại dùng liên hợp: biểu thức bằng 2x / (sqrt(x^2 + 2x) + x), chia cho x được 2 / (sqrt(1 + 2/x) + 1), dần tới 1.

> Lỗi thường gặp: thấy mẫu dần tới 0 liền kết luận +vô cùng mà không xét dấu hai phía.

## Hai giới hạn đáng nhớ

Giới hạn đáng nhớ thứ nhất, với x đo bằng radian:

$$ \lim_{x \to 0} \frac{\sin x}{x} = 1 $$

Muốn dùng nó, tạo ra đúng dạng sin u / u với u -> 0. Ví dụ sin(5x)/x = 5 . sin(5x)/(5x), dần tới 5. Từ nó suy ra tan x / x -> 1 và (1 - cos x)/x^2 -> 1/2, vì 1 - cos x = 2 sin^2(x/2).

Giới hạn đáng nhớ thứ hai định nghĩa số e (khoảng 2.718):

$$ \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^{n} = e $$

Nó vẫn đúng khi n chạy qua số thực ra +vô cùng hoặc -vô cùng, và viết được dưới dạng (1 + t)^(1/t) -> e khi t -> 0. Đây là dạng 1 mũ vô cùng: cơ số dần tới 1 nhưng số mũ lớn dần, nên kết quả không phải 1.

Cách dùng: đổi biến để thấy đúng dạng đó. Ví dụ (1 + 2/n)^n với m = n/2 thành [(1 + 1/m)^m]^2, dần tới e^2.

> Lỗi thường gặp: dùng sin x / x -> 1 khi x không dần tới 0. Khi x -> +vô cùng, sin x / x dần tới 0; còn x . sin(1/x) khi x -> 0 cũng dần tới 0 vì |x . sin(1/x)| <= |x|.

## Vô cùng bé, vô cùng lớn và tương đương

Một vô cùng bé (khi x -> a) là đại lượng dần tới 0; một vô cùng lớn là đại lượng có trị tuyệt đối dần ra +vô cùng. So sánh hai vô cùng bé a(x), b(x) bằng giới hạn của thương:

- a/b -> 0: a là vô cùng bé bậc cao hơn b.
- a/b -> 1: a và b tương đương, viết a ~ b.
- a/b -> một số khác 0: a và b cùng bậc.

Khi x -> 0, các tương đương cần thuộc:

$$ \sin x \sim x, \quad \tan x \sim x, \quad \arcsin x \sim x $$

$$ \ln(1 + x) \sim x, \quad e^{x} - 1 \sim x, \quad 1 - \cos x \sim \frac{x^{2}}{2} $$

Thay x bằng một vô cùng bé khác vẫn đúng: sin(3x) ~ 3x, ln(1 + x^2) ~ x^2.

Quy tắc vàng: trong một tích hoặc một thương, được thay mỗi thừa số bằng một vô cùng bé tương đương. Ví dụ [ln(1 + 3x) . sin(2x)] / x^2 ~ (3x . 2x) / x^2 = 6.

Bậc của vô cùng bé so với x là số k để a(x)/x^k dần tới một số khác 0. Với tổng các lũy thừa, số hạng có số mũ nhỏ nhất quyết định.

> Lỗi thường gặp: thay tương đương trong một hiệu. Với (tan x - sin x)/x^3, thay tan x ~ x và sin x ~ x cho 0, sai; viết thành tích tan x . (1 - cos x) ~ x^3/2 mới được giới hạn đúng là 1/2.
