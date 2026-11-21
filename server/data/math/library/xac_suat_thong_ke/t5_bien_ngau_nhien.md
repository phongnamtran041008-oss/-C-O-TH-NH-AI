---
id: xs_lib_t5
title_vi: Biến ngẫu nhiên, bảng phân phối và hàm phân phối
subject: xac_suat_thong_ke
floor: 5
format: 2
summary_vi: Gắn mỗi kết quả với một con số để tính toán: bảng phân phối cho biến rời rạc, đường mật độ và diện tích cho biến liên tục, và F(x) = P(X < x) gom xác suất cho cả hai.
skills: [xs_t5_bien_ngau_nhien, xs_t5_bang_phan_phoi, xs_t5_ham_phan_phoi, xs_t5_mat_do, xs_t5_xac_suat_khoang]
---
## Biến ngẫu nhiên rời rạc và liên tục

:::hook
Máy không tính toán được với chữ "sấp" hay "ngửa". Nó cần con số: số lượt bấm, số lỗi, thời gian chờ. Biến ngẫu nhiên biến mỗi kết quả thành một số.
:::

:::figure map
caption: Tung 2 đồng xu, X là số mặt ngửa. SN và NS cùng tới X = 1, nên X = 1 dễ ra gấp đôi X = 0.
col "Omega" SS SN NS NN
col "X" 0 1 2
SS -> 0
SN -> 1 do
NS -> 1 do
NN -> 2
:::

:::core
Biến ngẫu nhiên gắn mỗi kết quả của phép thử với một số. Rời rạc: các giá trị đếm được từng cái; liên tục: lấp kín cả một khoảng.
:::

- Rời rạc: số chấm, số phế phẩm, số lần gieo tới khi ra mặt 6 (vô hạn mà vẫn đếm được).
- Liên tục: thời gian chờ, chiều cao. Xác suất nhận đúng một giá trị bằng 0.

Ví dụ: gieo hai xúc xắc, X = |hiệu hai số chấm|. Tính P(X = 2).

1. Hiệu 2: (1, 3), (2, 4), (3, 5), (4, 6).
2. Đảo thứ tự cho thêm 4 cặp: 8 trong 36 cặp.
3. P(X = 2) = 8/36 = 2/9.

> Lỗi thường gặp: X có 3 giá trị thì cho mỗi giá trị xác suất 1/3. Phải đếm trên các kết quả đồng khả năng, như hình.

:::check
Q: Tung 4 đồng xu, X = số mặt ngửa trừ số mặt sấp. X nhận những giá trị nào?
A: k ngửa thì X = k - (4 - k) = 2k - 4, với k = 0..4: X nhận -4, -2, 0, 2, 4.
:::

## Bảng phân phối xác suất

:::hook
Hệ gợi ý ghi lại mỗi người xem bao nhiêu video trong một phiên. Một bảng nhỏ nói đủ: mỗi giá trị kèm xác suất của nó.
:::

:::figure bars
caption: Lấy cùng lúc 2 bi từ hộp 3 đỏ, 3 xanh; X là số bi đỏ. Đếm trên C(6, 2) = 15 nhóm: 3, 9, 3.
size: 150 90
bar "X = 0" 1/5
bar "X = 1" 3/5 do
bar "X = 2" 1/5
:::

:::core
Bảng phân phối ghi mỗi giá trị của X cùng xác suất của nó. Các xác suất không âm và cộng lại đúng bằng 1.
:::

$$ p_i \ge 0, \qquad \sum_i p_i = 1 $$

Tổng bằng 1 dùng để tìm hằng số, tìm ô còn thiếu, và bắt lỗi.

Ví dụ: P(X = k) = c . k với k = 1, 2, 3. Tìm c và P(X >= 2).

1. Tổng bằng 1: c(1 + 2 + 3) = 6c = 1, nên c = 1/6.
2. P(X >= 2) = 2/6 + 3/6 = 5/6.

> Lỗi thường gặp: lập bảng xong không cộng thử. Tổng khác 1 là chắc chắn có chỗ đếm sai.

:::check
Q: Hai xạ thủ bắn độc lập, trúng với xác suất 1/2 và 1/3. X = số phát trúng. Lập bảng của X.
A: P(X = 0) = 1/2 . 2/3 = 1/3; P(X = 1) = 1/2 . 2/3 + 1/2 . 1/3 = 1/2; P(X = 2) = 1/6. Tổng bằng 1.
:::

## Hàm phân phối F(x)

:::hook
"Xác suất chờ dưới 5 phút" là một câu hỏi tích lũy. F(x) gom sẵn mọi xác suất nằm bên trái x.
:::

:::figure plane
caption: X nhận 1, 2, 4 với xác suất 3/10, 1/2, 1/5. Chấm đặc là giá trị của F tại đó, lúc chưa nhảy.
size: 210 100
names: x F
x: 0 5 1
y: 0 1.1 0.5
segment 0 0 1 0 xanh
segment 1 0.3 2 0.3 xanh
segment 2 0.8 4 0.8 xanh
segment 4 1 5 1 xanh
point 1 0 xanh
point 1 0.3 xanh open
point 2 0.3 xanh
point 2 0.8 xanh open
point 4 0.8 xanh
point 4 1 xanh open
text 1 0.15 "+3/10" pos=w
text 2 0.55 "+1/2" pos=w
text 4 0.9 "+1/5" pos=w
:::

:::core
F(x) = P(X < x) cộng xác suất mọi giá trị nhỏ hơn hẳn x. Bước nhảy tại x_i đúng bằng P(X = x_i).
:::

$$ F(x) = P(X < x) $$

F không giảm, từ 0 lên 1. Biến liên tục có F liền nét: F(x) = kx^2 trên (0, 3] nối với 1 tại 3 nên k = 1/9.

Ví dụ: đọc hình.

1. F(2) = P(X < 2) = 3/10: giá trị 2 chưa được tính.
2. F(3) = 3/10 + 1/2 = 4/5.
3. Ngược lại, bước nhảy tại 2 là 4/5 - 3/10 = 1/2 = P(X = 2).

> Lỗi thường gặp: tính F(x) như P(X <= x). Ở đây F(2) là 3/10, không phải 4/5.

:::check
Q: Với X ở hình, F(4) bằng bao nhiêu? F(5) bằng bao nhiêu?
A: F(4) = P(X < 4) = 3/10 + 1/2 = 4/5 (chưa tính giá trị 4). F(5) = 1.
:::

## Hàm mật độ xác suất

:::hook
Thời gian chờ có thể là 3.27 phút: không liệt kê nổi từng giá trị. Thay cho bảng là một đường cong; xác suất là diện tích bên dưới nó.
:::

:::figure plane
caption: f(x) = 3x^2/2 trên [-1, 1]: cả vùng tô có diện tích 1, dù f(1) = 3/2 vượt quá 1.
size: 190 100
x: -1.5 1.5 0.5
y: 0 1.6 0.5
names: x f
area "3*x^2/2" -1 1 vang
curve "3*x^2/2" -1 1 xanh
point 1 1.5 do "f(1) = 3/2" pos=e
:::

:::core
Xác suất là diện tích dưới mật độ f, và cả diện tích bằng 1. Bản thân f(x) không phải xác suất: nó được lớn hơn 1.
:::

$$ F(x) = \int_{-\infty}^{x} f(t)\,dt, \qquad f(x) = F'(x) $$

Ví dụ: tìm k để f(x) = kx trên [0, 3] (bằng 0 nơi khác) là hàm mật độ.

1. Cần f >= 0, nên k > 0.
2. Diện tích: tích phân của kx từ 0 đến 3 là 9k/2.
3. 9k/2 = 1, nên k = 2/9.

> Lỗi thường gặp: tưởng f(x) = P(X = x), hay tưởng f không được vượt 1. Chỉ cần f không âm và tổng diện tích bằng 1.

:::check
Q: Biến liên tục có F(x) = x^3 trên (0, 1]. Tính f(1/2).
A: f(x) = F'(x) = 3x^2, nên f(1/2) = 3/4.
:::

## Xác suất rơi vào một khoảng

:::hook
"Xác suất chờ từ 2 đến 4 phút" là hỏi về một khoảng. Có F trong tay thì chỉ cần một phép trừ.
:::

:::figure plane
caption: f(x) = x/8 trên [0, 4], nên F(x) = x^2/16. Vùng tô: P(2 <= X <= 4) = F(4) - F(2) = 1 - 1/4 = 3/4.
size: 190 100
x: 0 4.5 1
y: 0 0.6 0.25
names: x f
area "x/8" 2 4 vang
curve "x/8" 0 4 xanh "f" pos=n
:::

:::core
P(a <= X < b) = F(b) - F(a): tích lũy tới b, bỏ phần tới a. Biến liên tục thì đó là diện tích dưới f, dấu < hay <= không đổi gì.
:::

$$ P(a \le X < b) = F(b) - F(a) $$

Ví dụ: X rời rạc nhận 0, 1, 2, 3 với xác suất 1/5, 3/10, 2/5, 1/10.

1. P(1 <= X < 2) = F(2) - F(1) = 1/2 - 1/5 = 3/10: chỉ có giá trị 1.
2. P(1 <= X <= 2) phải lấy tới F(3): 9/10 - 1/5 = 7/10.
3. Thử lại: 3/10 + 2/5 = 7/10.

> Lỗi thường gặp: dùng F(b) - F(a) cho P(a <= X <= b) với biến rời rạc. F(b) chưa chứa P(X = b), nên thiếu một bước nhảy.

:::check
Q: Với f(x) = x/8 trên [0, 4] ở hình, tính P(X < 1) và P(1 <= X <= 3).
A: P(X < 1) = F(1) = 1/16. P(1 <= X <= 3) = F(3) - F(1) = 9/16 - 1/16 = 1/2.
:::
