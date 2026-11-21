---
id: gt_lib_t2
title_vi: Dãy số, giới hạn, vô cùng bé và vô cùng lớn
subject: giai_tich
floor: 2
format: 2
summary_vi: Giới hạn là con số mà một đại lượng tiến sát tới: đọc nó cho dãy và cho hàm, gỡ các dạng 0/0 và vô cùng, nhớ sin x / x và số e, rồi bỏ phần nhỏ bằng vô cùng bé tương đương.
skills: [gt_t2_gioi_han_day, gt_t2_gioi_han_ham, gt_t2_gioi_han_vo_cuc, gt_t2_gioi_han_dac_biet, gt_t2_vo_cung_be]
---
## Giới hạn của dãy số

:::hook
Mỗi vòng huấn luyện, sai số của mô hình nhỏ đi một chút. Hỏi "cuối cùng sai số về đâu" chính là hỏi giới hạn của một dãy số.
:::

:::figure numberline
caption: u_n = (2n + 1)/n đi 3; 2.5; 2.33; 2.25; ... Từ n = 5 trở đi, mọi số hạng nằm trong dải 2 +- 0.25.
range: 1.5 3.2 0.5
nbhd 2 0.25 luc "dải 2 +- 0.25"
seq "(2*n + 1)/n" 1 9 xanh "u_n"
:::

:::core
u_n -> L nghĩa là: dải quanh L hẹp tới đâu cũng được, từ một lúc nào đó mọi số hạng đều nằm trong dải.
:::

$$ \lim_{n \to \infty} \frac{1}{n^{k}} = 0 \;(k > 0), \qquad \lim_{n \to \infty} q^{n} = 0 \;(|q| < 1) $$

Ví dụ: tính giới hạn của u_n = (4n^2 - n)/(2n^2 + 3).

1. Lũy thừa cao nhất của mẫu là n^2: chia cả tử và mẫu cho n^2.
2. Được (4 - 1/n)/(2 + 3/n^2).
3. 1/n và 3/n^2 -> 0, còn lại 4/2 = 2.

Có lũy thừa mũ như 5^n và 2^n: chia cho số có cơ số lớn nhất, phần còn lại (2/5)^n -> 0. Hiệu hai căn như sqrt(n^2 + 4n) - n: nhân liên hợp để thành thương. (-1)^n/n -> 0 vì trị tuyệt đối 1/n -> 0; còn (-1)^n nhảy -1, 1 mãi, không có giới hạn.

> Lỗi thường gặp: chia cho lũy thừa nhỏ hơn bậc của mẫu. Khi đó mẫu vẫn còn chạy ra vô cùng, đừng vội coi nó là một hằng số.

:::check
Q: Tính giới hạn của (3 . 5^n - 2^n)/(5^n + 4 . 2^n).
A: Chia cho 5^n: (3 - (2/5)^n)/(1 + 4 . (2/5)^n). (2/5)^n -> 0, nên giới hạn bằng 3.
:::

## Giới hạn hàm số tại một điểm

:::hook
Vận tốc là quãng đường chia thời gian; cho thời gian về 0 thì thành 0/0. Giới hạn cho ta đọc ra con số mà biểu thức đang tiến tới, dù ngay tại điểm đó không thay số được.
:::

:::figure plane
caption: y = (x^2 - 9)/(x - 3) là đường y = x + 3 bị khoét lỗ tại x = 3. Từ hai phía, độ cao đều tiến về 6.
size: 150 105
x: 0 5 1
y: 0 9 3
curve "(x^2 - 9)/(x - 3)" xanh
drop 3 6
point 3 6 do "lỗ (3, 6)" open pos=nw
:::

:::core
Giới hạn tại a là độ cao mà f(x) tiến tới khi x sát a. Chính f(a) có hay không, bằng bao nhiêu, không quan trọng.
:::

$$ \lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = \lim_{x \to 3} (x + 3) = 6 $$

Ví dụ: tính giới hạn của (x^2 + x - 6)/(x^2 - 4) khi x -> 2.

1. Thay x = 2: tử 0, mẫu 0. Dạng 0/0, chưa có đáp số.
2. Tử và mẫu cùng có nghiệm 2 nên cùng chứa (x - 2): (x - 2)(x + 3) và (x - 2)(x + 2).
3. Rút gọn (x - 2), còn (x + 3)/(x + 2).
4. Thay x = 2: 5/4.

Luôn thay số trước. Ra một số bình thường (mẫu khác 0) thì đó là đáp số. Ra 0/0 là có thừa số chung đang trốn, phải lôi ra. Có căn thì nhân liên hợp: (sqrt(x + 9) - 3)/x = 1/(sqrt(x + 9) + 3) -> 1/6.

> Lỗi thường gặp: phân tích sai nhân tử. Nhân ngược lại để thử: (x - 2)(x + 3) = x^2 + x - 6.

:::check
Q: f(x) = x + 1 khi x khác 2, và f(2) = 10. Giới hạn của f khi x -> 2 bằng bao nhiêu?
A: 3. Giới hạn chỉ nhìn các x gần 2, không nhìn f(2) = 10.
:::

## Giới hạn ở vô cùng và giới hạn vô cùng

:::hook
Chi phí trung bình mỗi sản phẩm là (5000 + 2x)/x. Làm càng nhiều, nó càng sát 2. Giới hạn ở vô cùng cho biết một đại lượng về lâu dài ổn định ở đâu.
:::

:::figure plane
caption: y = (2x + 1)/(x - 1). Đi xa, đồ thị sát y = 2 (tỉ số hệ số 2/1). Gần x = 1, mẫu -> 0: bên phải vọt lên, bên trái lao xuống.
size: 190 115
x: -4 6 2
y: -5 8 2
line -4 2 6 2 xam dash "y = 2" pos=se
line 1 -5 1 8 xam dash
curve "(2*x + 1)/(x - 1)" xanh
:::

:::core
Ở rất xa, chỉ số hạng bậc cao nhất có tiếng nói. Gần chỗ mẫu bằng 0, phải xem dấu từng phía.
:::

Phân thức P/Q khi x -> vô cùng:

- bậc P nhỏ hơn bậc Q: giới hạn 0;
- bằng nhau: tỉ số hai hệ số cao nhất;
- bậc P lớn hơn: ra vô cùng, dấu theo hệ số và hướng của x.

Mẫu -> 0 còn tử -> một số khác 0 thì ra vô cùng: 1/x^2 -> +vô cùng cả hai phía, nhưng 1/(x - 1) lệch dấu hai phía nên không có giới hạn.

Ví dụ: tính giới hạn của sqrt(x^2 + 6x) - x khi x -> +vô cùng.

1. Dạng vô cùng - vô cùng: nhân và chia cho liên hợp sqrt(x^2 + 6x) + x.
2. Tử thành (x^2 + 6x) - x^2 = 6x.
3. Chia tử và mẫu cho x: 6/(sqrt(1 + 6/x) + 1).
4. Mẫu -> 1 + 1 = 2, nên giới hạn bằng 3.

> Lỗi thường gặp: thấy mẫu -> 0 liền viết +vô cùng mà không xét dấu hai phía.

:::check
Q: Tính giới hạn của (6x^2 - x)/(1 - 3x^2) khi x -> +vô cùng.
A: Cùng bậc 2: chỉ còn tỉ số hai hệ số cao nhất, 6/(-3) = -2.
:::

## Hai giới hạn đáng nhớ

:::hook
Máy tính dùng sin x xấp xỉ x cho góc nhỏ; lãi kép chia càng nhiều kỳ càng tiến về số e. Hai giới hạn này là hai viên gạch nền của mọi khai triển về sau.
:::

:::figure plane
caption: Gần 0, đường sin x dính sát y = x, nên sin x / x -> 1 (x đo bằng radian).
size: 140 100
x: -3 3 1
y: -1.6 1.6 1
curve "x" xam
text -2.2 -1.3 "y = x"
curve "sin(x)" xanh "sin x" pos=se
:::

:::core
sin u / u -> 1 khi u -> 0, và (1 + 1/m)^m -> e khi m -> vô cùng. Mọi bài là đổi biến cho lộ ra đúng hai dạng đó.
:::

$$ \lim_{x \to 0} \frac{\sin x}{x} = 1 $$

:::figure numberline
caption: (1 + 1/n)^n với n = 1, 2, 3, ...: tăng dần nhưng không vượt qua e, khoảng 2.718.
range: 1.9 2.9 0.2
seq "(1 + 1/n)^n" 1 12 xanh
point e do "e"
:::

$$ \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^{n} = e $$

Ví dụ: tính giới hạn của (1 + 2/n)^(3n).

1. Đặt m = n/2: 2/n = 1/m và 3n = 6m.
2. Biểu thức thành [(1 + 1/m)^m]^6.
3. Trong ngoặc -> e, nên giới hạn là e^6.

Với sin: sin(5x)/x = 5 . sin(5x)/(5x) -> 5. Từ đó tan x / x -> 1 và (1 - cos x)/x^2 -> 1/2. Nhưng khi x -> vô cùng thì sin x / x -> 0; còn x . sin(1/x) -> 0 khi x -> 0, vì bị kẹp giữa -|x| và |x|.

> Lỗi thường gặp: thay riêng cơ số, coi (1 + 1/n)^(2n) là 1^vô cùng = 1. Số mũ cũng đang chạy: đây là dạng vô định, đáp số là e^2.

:::check
Q: Tính giới hạn của (1 - 2/n)^n khi n -> +vô cùng.
A: Đặt m = -n/2: -2/n = 1/m và n = -2m. Biểu thức là [(1 + 1/m)^m]^(-2) -> e^(-2).
:::

## Vô cùng bé, vô cùng lớn và tương đương

:::hook
Kỹ sư ước lượng chỉ giữ phần lớn nhất, bỏ phần nhỏ hơn hẳn. Vô cùng bé tương đương là phép bỏ phần nhỏ có giấy phép: thay sin(3x) bằng 3x mà giới hạn không đổi.
:::

:::figure grid
caption: Khi x -> 0: sin x / x -> 1 (tương đương), còn x^2 / x -> 0 (x^2 bậc cao hơn x).
table
head "x" "sin x / x" "x^2 / x"
row 0.1 0.9983 0.1
row 0.01 0.99998 0.01
row 0.001 0.9999998 0.001
:::

:::figure grid
caption: Bảng tương đương khi u -> 0; u có thể là 3x, x^2, ...
table
head "vô cùng bé" "tương đương"
row "sin u, tan u, arcsin u" "u"
row "ln(1 + u), e^u - 1" "u"
row "1 - cos u" "u^2/2"
:::

:::core
Hai vô cùng bé tương đương khi tỉ số -> 1. Trong tích và thương, thay mỗi thừa số bằng bản tương đương; trong hiệu thì không.
:::

Ví dụ: tính giới hạn của sin(3x) . (e^(2x) - 1) / (x . ln(1 + 4x)) khi x -> 0.

1. sin(3x) ~ 3x, e^(2x) - 1 ~ 2x, ln(1 + 4x) ~ 4x.
2. Cả biểu thức là tích và thương, nên thay được từng thừa số.
3. Giới hạn = (3x . 2x)/(x . 4x) = 6/4 = 3/2.

So hai vô cùng bé a, b bằng a/b: -> 0 thì a bậc cao hơn; -> 1 thì tương đương; -> số khác 0 thì cùng bậc. Bậc của a là số k để a/x^k -> một số khác 0; với tổng các lũy thừa, mũ nhỏ nhất thắng: x^4 - 3x^6 bậc 4. Còn 1/x khi x -> 0 là vô cùng lớn: |1/x| -> +vô cùng.

> Lỗi thường gặp: thay tương đương trong một hiệu. (e^x - 1 - x)/x^2: thay e^x - 1 ~ x cho 0, sai; đúng là e^x - 1 - x ~ x^2/2, giới hạn 1/2.

:::check
Q: Khi x -> 0, x^3 + 2x^2 - sin(x^5) là vô cùng bé bậc mấy? Và sin(6x)/(e^(3x) - 1) -> ?
A: Bậc 2: 2x^2 thắng (sin(x^5) ~ x^5). Giới hạn thứ hai: 6x/(3x) = 2.
:::
