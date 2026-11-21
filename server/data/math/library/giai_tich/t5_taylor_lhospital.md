---
id: gt_lib_t5
title_vi: Định lý về hàm khả vi, khai triển Taylor và quy tắc L'Hospital
subject: giai_tich
floor: 5
format: 2
summary_vi: Tốc độ trung bình luôn bằng tốc độ tức thời ở một điểm nào đó; một hàm trơn được thay bằng đa thức ôm sát nó; và so tốc độ (đạo hàm) gỡ được mọi dạng giới hạn vô định.
skills: [gt_t5_rolle_lagrange, gt_t5_taylor, gt_t5_maclaurin, gt_t5_lhospital, gt_t5_dang_vo_dinh]
---
## Định lý Rolle, Lagrange và Cauchy

:::hook
Đi 120 km trong 2 giờ thì chắc chắn có một lúc đồng hồ tốc độ chỉ đúng 60 km/h. Định lý Lagrange nói điều đó cho mọi hàm trơn, và nhờ nó ta chặn được sai số.
:::

:::figure plane
caption: Dây cung nối hai đầu của y = x^2 trên [0, 2] có hệ số góc 2. Tại c = 1, tiếp tuyến song song với nó.
size: 150 110
x: -0.3 2.4 1
y: -1 4.5 1
curve "x^2" xanh "y = x^2" pos=w
segment 0 0 2 4 xam dash "dây cung" pos=nw
tangent "x^2" 1 do len=30
point 0 0 muc
point 2 4 muc
point 1 1 do "c = 1" pos=se
:::

:::core
Hàm liền và trơn trên một đoạn thì ở một điểm c bên trong, tốc độ tức thời f'(c) bằng đúng tốc độ trung bình cả đoạn.
:::

$$ f'(c) = \frac{f(b) - f(a)}{b - a} $$

Ví dụ: tìm c của định lý Lagrange cho f(x) = 1/x trên [1, 4].

1. 1/x liên tục, khả vi trên [1, 4] vì 0 không nằm trong đoạn.
2. Hệ số góc dây cung: (1/4 - 1)/(4 - 1) = -1/4.
3. f'(c) = -1/c^2 = -1/4 nên c^2 = 4; lấy c = 2, nằm trong (1, 4).

Rolle là trường hợp f(a) = f(b): có c với f'(c) = 0. Cauchy là Lagrange cho hai hàm chạy cùng lúc: (f(b) - f(a))/(g(b) - g(a)) = f'(c)/g'(c). Hai cách dùng:

- chặn: |f'| <= M thì |f(b) - f(a)| <= M |b - a|;
- đếm nghiệm: giữa hai nghiệm của f có một nghiệm của f'; f' không bao giờ bằng 0 thì f có nhiều nhất một nghiệm.

> Lỗi thường gặp: quên kiểm giả thiết. |x| trên [-1, 1] không khả vi tại 0 nên không dùng được Rolle; và c phải nằm trong khoảng mở, không lấy đầu mút.

:::check
Q: f khả vi, f(0) = 1 và 2 <= f'(x) <= 3 với mọi x. f(4) chắc chắn nằm trong đoạn nào?
A: f(4) - 1 = 4f'(c) với c trong (0, 4), nên 8 <= f(4) - 1 <= 12, tức f(4) thuộc [9, 13].
:::

## Khai triển Taylor

:::hook
Máy tính chỉ biết cộng và nhân. Muốn tính sqrt(10) hay ln 1.1, nó thay hàm bằng một đa thức ôm sát hàm quanh một điểm: đa thức Taylor.
:::

:::figure plane
caption: Quanh x = 1, đường thẳng (bậc 1) chỉ chạm ln x; parabol bậc 2 ôm sát hơn. Bậc càng cao, ôm càng xa.
size: 170 115
x: 0 3 1
y: -2 1.5 1
curve "ln(x)" xanh "ln x" pos=se
curve "x - 1" xam "bậc 1" 0.2 2.4 pos=e
curve "(x - 1) - (x - 1)^2/2" do "bậc 2" 0.2 2.6 pos=e
point 1 0 muc
:::

:::core
Đa thức Taylor bậc n quanh a bắt chước f tại a: cùng giá trị, cùng độ dốc, cùng độ cong... tới đạo hàm cấp n.
:::

$$ f(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x - a)^k + R_n(x) $$

Ví dụ: đa thức Taylor bậc 2 của sqrt(x) quanh 9, rồi ước lượng sqrt(10).

1. f(9) = 3.
2. f'(x) = 1/(2 sqrt(x)), nên f'(9) = 1/6.
3. f''(x) = -1/(4x sqrt(x)), nên f''(9) = -1/108; chia 2! được -1/216.
4. sqrt(x) xấp xỉ 3 + (x - 9)/6 - (x - 9)^2/216. Tại 10: 3.16204, số thật là 3.16228.

Hệ số của (x - a)^k là f^(k)(a)/k!: đạo hàm lấy tại số a, rồi chia k!. Một đa thức bậc n chính là đa thức Taylor bậc n của nó quanh mọi điểm. Phần dư dạng Lagrange f^(n+1)(c)/(n+1)! . (x - a)^(n+1), với c giữa a và x, dùng để chặn sai số: thay e^x bằng 1 + x + x^2/2 trên [0, 1], sai không quá e/6 < 1/2.

> Lỗi thường gặp: quên chia k!. Số hạng bậc 2 của e^x quanh 1 là (e/2)(x - 1)^2, không phải e(x - 1)^2.

:::check
Q: p(x) = x^3 + 2x. Hệ số của (x - 1)^2 trong khai triển Taylor quanh 1 là bao nhiêu?
A: p''(x) = 6x nên p''(1) = 6; chia 2! được 3.
:::

## Khai triển Maclaurin của các hàm cơ bản

:::hook
Thư viện toán trong máy tính tính sin, e^x bằng vài số hạng của các dãy dưới đây. Thuộc năm khai triển này là có trong tay bảng tra cho cả chương giới hạn.
:::

:::figure plane
caption: Quanh 0: y = x ôm sin x một quãng ngắn; thêm -x^3/6 thì ôm xa hơn hẳn.
size: 150 105
x: -3.2 3.2 1
y: -2 2 1
curve "sin(x)" xanh "sin x" pos=se
curve "x" xam -2 2
text -1.3 -1.75 "y = x"
curve "x - x^3/6" do "x - x^3/6" -3 3 pos=nw
:::

:::figure grid
caption: Năm khai triển quanh 0 cần thuộc (a là số mũ bất kỳ).
table
head "hàm" "khai triển"
row "e^x" "1 + x + x^2/2! + x^3/3! + ..."
row "sin x" "x - x^3/3! + x^5/5! - ..."
row "cos x" "1 - x^2/2! + x^4/4! - ..."
row "ln(1 + x)" "x - x^2/2 + x^3/3 - ..."
row "(1 + x)^a" "1 + ax + a(a - 1)/2! x^2 + ..."
:::

:::core
Hệ số của x^k là f^(k)(0)/k!. Thuộc năm khai triển gốc rồi thay biến, nhân, cộng là ra khai triển của hàm mới.
:::

Ví dụ: tìm hệ số của x^3 trong e^x . sin x.

1. e^x = 1 + x + x^2/2 + ..., sin x = x - x^3/6 + ...
2. Các cặp nhân ra x^3: 1 . (-x^3/6) và (x^2/2) . x.
3. Cộng hệ số: -1/6 + 1/2 = 1/3.

Thay biến thì lũy thừa cả hệ số: sin(3x) = 3x - (3x)^3/6 + ... = 3x - (9/2)x^3 + ... Đọc ngược: hệ số của x^k nhân k! ra f^(k)(0). sin lẻ nên chỉ có mũ lẻ; cos chẵn nên chỉ có mũ chẵn.

> Lỗi thường gặp: thay u = 3x vào ln(1 + u) mà quên lũy thừa số 3: u^2/2 là 9x^2/2, không phải 3x^2/2.

:::check
Q: Dùng khai triển, tính đạo hàm cấp bốn tại 0 của f(x) = x . e^x.
A: x . e^x = x + x^2 + x^3/2 + x^4/6 + ..., hệ số x^4 là 1/6, nên f^(4)(0) = 4! . 1/6 = 4.
:::

## Quy tắc L'Hospital

:::hook
Hai đại lượng cùng teo về 0, ai teo nhanh hơn? L'Hospital trả lời bằng cách so tốc độ của chúng: so đạo hàm thay vì so giá trị.
:::

:::figure plane
caption: Phóng to quanh x = 1: x^2 - 1 và ln x cùng qua 0, trông như hai đường thẳng dốc 2 và dốc 1. Tỉ số của chúng tiến về 2/1 = 2.
size: 160 110
x: 0.7 1.3 0.1
y: -0.6 0.7 0.2
curve "x^2 - 1" do "x^2 - 1" pos=w
curve "ln(x)" xanh "ln x" pos=se
point 1 0 muc
:::

:::core
Dạng 0/0 hay vô cùng/vô cùng: giới hạn của f/g bằng giới hạn của f'/g' (đạo hàm riêng tử, riêng mẫu), nếu cái sau tồn tại.
:::

$$ \lim \frac{f(x)}{g(x)} = \lim \frac{f'(x)}{g'(x)} $$

Ví dụ: tính giới hạn của (e^(3x) - 1 - 3x)/x^2 khi x -> 0.

1. Thay x = 0: tử 1 - 1 - 0 = 0, mẫu 0. Dạng 0/0.
2. Lần 1: (3e^(3x) - 3)/(2x), vẫn 0/0.
3. Lần 2: 9e^(3x)/2.
4. Hết vô định: giới hạn bằng 9/2.

Mỗi lần dùng xong, thay số kiểm lại dạng; ra số chia số khác 0 thì dừng. Ở vô cùng: ln x / x -> 0, x^2/e^x -> 0 (dùng hai lần). e^x thắng mọi lũy thừa, lũy thừa thắng ln. Quy tắc chỉ đi một chiều: f'/g' không có giới hạn thì chưa kết luận gì; (x + sin x)/x vẫn -> 1.

> Lỗi thường gặp: dùng khi không vô định. (x^2 + 1)/(x + 2) khi x -> 1 bằng 2/3; lấy đạo hàm lại ra 2, sai. Cũng đừng lấy đạo hàm cả phân thức.

:::check
Q: Tính giới hạn của (x^4 - 1)/(x^3 - 1) khi x -> 1.
A: Dạng 0/0: chuyển thành 4x^3/(3x^2), thay x = 1 được 4/3.
:::

## Các dạng vô định khác

:::hook
Lãi 100% một năm, chia làm n kỳ: (1 + 1/n)^n. Cơ số về 1 mà số mũ phình to, hai lực kéo ngược nhau và ra e. Mọi dạng vô định đều là một cuộc kéo co như thế.
:::

:::figure flow
caption: Dạng mũ (1^vô cùng, 0^0, vô cùng^0): lấy ln ra một tích, đổi thành thương (vc là vô cùng), tính ra L, rồi trả lại e mũ.
box "u^v"
link "lấy ln"
box "v . ln u" xanh
link "đổi thành thương"
box "0/0 hay vc/vc" vang
link "ra giới hạn L"
box "e^L" luc
:::

:::core
Mọi dạng vô định đều đổi về một thương 0/0 hoặc vô cùng/vô cùng. Dạng mũ thì lấy ln, tính giới hạn số mũ, rồi trả lại e mũ.
:::

$$ \lim u(x)^{v(x)} = e^{\lim v(x)\ln u(x)} $$

Ví dụ: tính giới hạn của (1 - 2/x)^(3x) khi x -> +vô cùng.

1. Cơ số -> 1, số mũ -> vô cùng: dạng 1^vô cùng.
2. Lấy ln: 3x . ln(1 - 2/x).
3. ln(1 - 2/x) ~ -2/x, nên số mũ -> 3x . (-2/x) = -6.
4. Trả lại e mũ: giới hạn là e^(-6).

Hai dạng còn lại:

- 0 . vô cùng: chuyển một thừa số xuống mẫu. x ln x = ln x / (1/x) -> 0 khi x -> 0+.
- vô cùng - vô cùng: quy đồng thành một phân số. 1/sin^2 x - 1/x^2 = (x^2 - sin^2 x)/(x^2 sin^2 x) -> 1/3.

Khai triển Maclaurin thường nhanh hơn dùng L'Hospital nhiều lần: (e^x - 1 - x)/x^2 = (x^2/2 + ...)/x^2 -> 1/2.

> Lỗi thường gặp: tính xong số mũ rồi quên lấy e mũ, như kết luận (cos x)^(1/x^2) -> -1/2 thay vì e^(-1/2). Và coi 1^vô cùng là 1.

:::check
Q: Tính giới hạn của x . (ln(x + 5) - ln x) khi x -> +vô cùng.
A: Dạng vô cùng . 0: bằng ln(1 + 5/x)/(1/x). ln(1 + 5/x) ~ 5/x, nên giới hạn bằng 5.
:::
