---
id: tr_lib_t10
title_vi: Mở rộng: phương pháp tính
subject: toi_uu_roi_rac
floor: 10
format: 2
summary_vi: Máy tính chỉ có số gần đúng: biết sai số lớn đến đâu và lan qua phép tính thế nào. Rồi ba cách giải f(x) = 0 bằng lặp: chia đôi (chắc mà chậm), lặp đơn (cần phép co), Newton (đi theo tiếp tuyến, nhanh gấp bội nhưng kén điểm xuất phát).
skills: [tr_t10_sai_so, tr_t10_chia_doi, tr_t10_lap_don, tr_t10_newton]
---
## Sai số và chữ số đáng tin

:::hook
Cảm biến báo lò 812.4 độ nhưng chỉ chính xác trong khoảng 0.5 độ: chữ số 4 cuối có còn nghĩa lý gì không?
:::

:::figure numberline
caption: a = 2.718, sai số 0.003: giá trị thật nằm đâu đó trong đoạn xanh [2.715, 2.721].
size: 200 40
range: 2.71 2.73 0.01
interval 2.715 2.721 [ ] xanh
point 2.718 do "a"
:::

:::core
Sai số tuyệt đối là bán kính của vùng mà giá trị thật có thể nằm; sai số tương đối là bán kính đó so với độ lớn của số.
:::

- Sai số tuyệt đối Delta_a: độ lệch tối đa so với giá trị thật.
- Sai số tương đối delta_a = Delta_a/|a|, thường viết phần trăm.
- Chữ số hàng 10^s đáng tin khi Delta_a <= 0.5 . 10^s.

Ví dụ: a = 2.718, Delta_a = 0.003.

1. Tương đối: 0.003/2.718, khoảng 0.11%.
2. Hàng 10^-2: 0.003 <= 0.005, đáng tin; hàng 10^-3: 0.003 > 0.0005, không. Vậy 3 chữ số 2, 7, 1.

> Lỗi thường gặp: đếm mọi chữ số đã viết ra là đáng tin.

:::check
Q: a = 45.62 với Delta_a = 0.3. Có mấy chữ số đáng tin? Sai số tương đối khoảng bao nhiêu?
A: Hàng đơn vị: 0.3 <= 0.5, đáng tin; hàng 10^-1: 0.3 > 0.05, không. Hai chữ số 4, 5. Tương đối 0.3/45.62, khoảng 0.66%.
:::

### Sai số lan qua phép tính

:::figure grid
caption: Quy tắc bậc nhất khi sai số nhỏ: cộng trừ thì cộng sai số tuyệt đối, nhân chia thì cộng sai số tương đối.
table
head "phép tính" "sai số"
row "x + y, x - y" "Delta = Delta_x + Delta_y"
row "x . y, x/y" "delta = delta_x + delta_y"
row "x^n" "delta = n . delta_x"
row "f(x)" "Delta = |f'(x)| . Delta_x"
:::

Trừ hai số gần nhau là nguy hiểm: 50.3 - 49.9 = 0.4, mỗi số sai 0.1, nên hiệu sai tới 0.2, tức 50%.

$$ \Delta_{xy} \approx |y|\,\Delta_x + |x|\,\Delta_y, \qquad \Delta_{f(x)} \approx |f'(x)|\,\Delta_x $$

Ví dụ: A = x . y, x = 4 với sai số 0.02, y = 6 với sai số 0.06.

1. delta_x = 0.5%, delta_y = 1%, nên delta_A = 1.5%.
2. A = 24, Delta_A = 1.5% . 24 = 0.36. Công thức trên cũng cho 6 . 0.02 + 4 . 0.06 = 0.36.

> Lỗi thường gặp: trừ hai sai số khi tính hiệu, hay chia hai sai số khi tính thương. Sai số luôn cộng dồn.

:::check
Q: Cạnh lập phương đo được x = 2 với sai số 0.01. Sai số tuyệt đối của thể tích x^3?
A: |f'(x)| . Delta_x = 3 . 2^2 . 0.01 = 0.12. (Cũng là delta = 3 . 0.5% = 1.5% của 8.)
:::

## Phương pháp chia đôi

:::hook
Đoán số trong khoảng 1 đến 100 bằng câu hỏi "lớn hơn hay nhỏ hơn?": mỗi lần hỏi loại một nửa. Chia đôi tìm nghiệm của f(x) = 0 y như vậy.
:::

:::figure plane
caption: f(x) = x^2 - 5 trên [2, 3]: mỗi bậc đỏ là đoạn còn giữ sau một lần chia, luôn bao lấy nghiệm sqrt(5), khoảng 2.236.
size: 180 100
x: 1.9 3.1 0.25
y: -3.2 4.2 1
curve "x^2 - 5" xanh
segment 2 -1.4 3 -1.4 do
segment 2 -1.9 2.5 -1.9 do
segment 2 -2.4 2.25 -2.4 do
segment 2.125 -2.9 2.25 -2.9 do
point 2.236 0 luc
:::

:::core
f liên tục đổi dấu trên đoạn thì có nghiệm bên trong; giữ nửa đoạn còn đổi dấu, mỗi lần sai số giảm một nửa.
:::

Mỗi vòng: tính f ở trung điểm c = (a + b)/2, giữ nửa đoạn mà hai đầu trái dấu, lặp đến khi đoạn đủ ngắn.

Ví dụ: hình trên. f(2) = -1 < 0, f(3) = 4 > 0.

1. c = 2.5: f = 1.25 > 0, cùng dấu f(3): giữ [2, 2.5].
2. c = 2.25: f = 0.0625 > 0: giữ [2, 2.25].
3. c = 2.125: f < 0, cùng dấu f(2): giữ [2.125, 2.25].

> Lỗi thường gặp: nghĩ f(a) f(b) > 0 là không có nghiệm. x^2 - 1 trên [-2, 2] cùng dấu ở hai đầu mà có hai nghiệm.

:::check
Q: Chia đôi f(x) = x^2 - 7 trên [2, 3]. Sau hai lần chia, đoạn còn lại là gì?
A: c = 2.5: f = -0.75 < 0, giữ [2.5, 3]. c = 2.75: f = 0.5625 > 0, giữ [2.5, 2.75].
:::

### Cần bao nhiêu lần chia

:::figure bars
caption: Đoạn dài 1: sau n lần chia còn 1/2^n; trung điểm cách nghiệm không quá nửa số đó.
bar 0 1
bar 1 1/2
bar 2 1/4
bar 3 1/8
bar 4 1/16
:::

$$ |x_n - x^*| \le \frac{b - a}{2^{n+1}} $$

Muốn sai số không quá e, chọn n nhỏ nhất với 2^(n+1) >= (b - a)/e.

Ví dụ: đoạn dài 1, sai số 0.01.

1. Cần 2^(n+1) >= 100.
2. 2^6 = 64 chưa đủ, 2^7 = 128 đủ: n + 1 = 7, n = 6.

Chia đôi luôn hội tụ nhưng chậm: mỗi bước chỉ thêm khoảng một chữ số nhị phân (hội tụ tuyến tính). Nó tìm một nghiệm trong đoạn, không phải mọi nghiệm.

> Lỗi thường gặp: dùng độ dài đoạn (b - a)/2^n làm sai số của trung điểm; sai số thật chỉ bằng nửa số đó.

:::check
Q: Đoạn dài 4, cần sai số không quá 0.001. Ít nhất mấy lần chia?
A: 2^(n+1) >= 4000. 2^11 = 2048 chưa đủ, 2^12 = 4096 đủ: n + 1 = 12, n = 11.
:::

## Phương pháp lặp đơn

:::hook
Bấm phím cos liên tục trên máy tính bỏ túi: màn hình dừng ở 0.739..., chỗ cos x = x. Lặp đơn giải phương trình đúng như thế.
:::

:::figure plane
caption: Hình mạng nhện của g(x) = (x^2 + 2)/4: đi dọc lên đồ thị g, ngang sang đường y = x, lặp lại; các bước dồn về giao điểm x* = 2 - sqrt(2), khoảng 0.586.
size: 150 110
x: -0.05 1 0.25
y: -0.05 1 0.25
curve "x" xam
curve "(x^2 + 2)/4" xanh
segment 0 0 0 0.5 do
segment 0 0.5 0.5 0.5 do
segment 0.5 0.5 0.5 0.5625 do
segment 0.5 0.5625 0.5625 0.5625 do
segment 0.5625 0.5625 0.5625 0.5791 do
point 0.586 0.586 luc "x*" pos=nw
:::

:::core
Viết f(x) = 0 thành x = g(x) rồi lặp x_(n+1) = g(x_n). Nếu g là phép co (|g'| <= q < 1) thì mỗi bước kéo sai số lại gần nhau theo hệ số q.
:::

Điều kiện đủ trên [a, b]: g biến [a, b] vào chính nó, và |g'(x)| <= q < 1 trên [a, b]. Khi đó có đúng một điểm bất động, lặp từ mọi x_0 trong đoạn đều hội tụ.

> Lỗi thường gặp: chỉ kiểm tra |g'| < 1 mà quên điều kiện g biến đoạn vào chính nó.

:::check
Q: x_(n+1) = 2 + 3/x_n, x_0 = 1. Tính x_1, x_2, x_3. Dãy tiến về số nào?
A: x_1 = 5, x_2 = 13/5, x_3 = 2 + 15/13 = 41/13. Điểm bất động thỏa x = 2 + 3/x, tức x^2 - 2x - 3 = 0: x = 3.
:::

### Hệ số co và cận sai số

q là độ dốc lớn nhất của g trên đoạn: mỗi bước, khoảng cách tới x* co lại ít nhất q lần. Biết q và hai số lặp đầu là chặn được sai số trước khi chạy.

$$ |x_n - x^*| \le \frac{q^n}{1 - q}\,|x_1 - x_0|, \qquad |x_n - x^*| \le \frac{q}{1 - q}\,|x_n - x_{n-1}| $$

Ví dụ: g(x) = (x^2 + 2)/4 trên [0, 1], x_0 = 0.

1. g'(x) = x/2, nên q = max |g'| = 1/2. g(0) = 1/2, g(1) = 3/4: g biến [0, 1] vào chính nó.
2. x_1 = 1/2, x_2 = 9/16, x_3 = 593/1024.
3. Cận cho n = 3: (1/2)^3/(1/2) . 1/2 = 1/8.

:::check
Q: g(x) = (x^2 + 1)/6 trên [0, 2]. Tìm q, và kiểm tra g biến [0, 2] vào chính nó.
A: g'(x) = x/3, lớn nhất tại x = 2: q = 2/3 < 1. g(0) = 1/6, g(2) = 5/6, cả đoạn ảnh nằm trong [0, 2].
:::

### Điểm hút, điểm đẩy

:::figure grid
caption: Gần điểm bất động, sai số mới xấp xỉ g'(x*) nhân sai số cũ.
table
head "g'(x*)" "khi x_0 gần x*"
row "0" "hội tụ rất nhanh"
row "0 < g' < 1" "hội tụ, một phía"
row "-1 < g' < 0" "hội tụ, nhảy hai bên x*"
row "|g'| > 1" "bị đẩy ra xa"
:::

$$ x_{n+1} - x^* \approx g'(x^*)\,(x_n - x^*) $$

Cùng một phương trình có nhiều cách viết x = g(x): cách có |g'(x*)| < 1 thì hội tụ, cách kia thì không. Và |g'(x*)| < 1 chỉ bảo đảm hội tụ khi x_0 đủ gần x*.

Ví dụ: x_(n+1) = x_n^2 có hai điểm bất động 0 và 1.

1. g'(x) = 2x: g'(0) = 0, điểm hút; g'(1) = 2, điểm đẩy.
2. Từ x_0 = 0.9 dãy về 0; từ x_0 = 1.1 dãy chạy ra vô cùng.

:::check
Q: x^2 - 9x + 14 = 0 viết thành x = (x^2 + 14)/9. Lặp gần nghiệm 2 và gần nghiệm 7 thì sao?
A: g'(x) = 2x/9. g'(2) = 4/9 < 1: 2 là điểm hút. g'(7) = 14/9 > 1: 7 là điểm đẩy, dãy rời xa 7.
:::

## Phương pháp Newton

:::hook
Máy tính tính sqrt(5) chỉ bằng cộng, nhân, chia: mỗi bước Newton gần gấp đôi số chữ số đúng.
:::

:::figure plane
caption: Tiếp tuyến tại x_0 = 3 cắt trục ở x_1 = 7/3, tiếp tuyến tại x_1 cho x_2 = 47/21.
size: 170 95
x: 1 3.2 0.5
y: -4.5 4.5 2
curve "x^2 - 5" xanh
segment 3 4 2.3333 0 do
segment 2.3333 0 2.3333 0.4444 xam dash
segment 2.3333 0.4444 2.2381 0 do
point 3 4 do "x_0" pos=e
point 2.3333 0 do "x_1" pos=s
point 2.2381 0 do "x_2" pos=sw
:::

:::core
Newton thay đường cong bằng tiếp tuyến tại điểm hiện tại, rồi nhảy tới chỗ tiếp tuyến cắt trục hoành.
:::

$$ x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} $$

Ví dụ: f(x) = x^2 - 5, x_0 = 3.

1. f'(x) = 2x, nên x_(n+1) = (x_n + 5/x_n)/2. x_1 = 3 - 4/6 = 7/3.
2. x_2 = 7/3 - (4/9)/(14/3) = 7/3 - 2/21 = 47/21.
3. Sai số 0.76, 0.097, 0.002: gần như bình phương mỗi bước (bậc hai).

> Lỗi thường gặp: cộng f/f' thay vì trừ, hay giữ f'(x_0) cho mọi bước.

:::check
Q: Một bước Newton cho f(x) = x^3 - 4 từ x_0 = 2: x_1 bằng bao nhiêu?
A: f(2) = 4, f'(x) = 3x^2 nên f'(2) = 12. x_1 = 2 - 4/12 = 5/3.
:::

### Khi Newton hỏng, và so ba cách

:::figure grid
caption: Ba cách tạo số tiếp theo, và cái giá của mỗi cách.
table
head "cách" "số tiếp theo" "tốc độ"
row "chia đôi" "trung điểm đoạn đổi dấu" "chậm, chắc chắn"
row "lặp đơn" "x_(n+1) = g(x_n)" "theo hệ số |g'|"
row "Newton" "giao tiếp tuyến với trục" "bậc hai, kén x_0"
:::

Newton có thể hỏng:

- f'(x_n) = 0: tiếp tuyến nằm ngang, không cắt trục, không tính được bước sau.
- x_0 xấu: f(x) = x^3 - 2x + 2 từ x_0 = 0 cho 0, 1, 0, 1, ... lặp vòng mãi, không tới nghiệm.

Newton hội tụ bậc hai khi f'(x*) khác 0 và x_0 đủ gần nghiệm; chia đôi chỉ tuyến tính, mỗi bước giảm một nửa.

> Lỗi thường gặp: tin Newton hội tụ từ mọi điểm xuất phát.

:::check
Q: Kiểm tra vòng lặp: với f(x) = x^3 - 2x + 2, tính một bước Newton từ x = 1.
A: f(1) = 1, f'(x) = 3x^2 - 2 nên f'(1) = 1. x mới = 1 - 1/1 = 0: quay về điểm đầu.
:::
