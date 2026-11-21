---
id: xs_lib_t10
title_vi: Tài năng: hàm của biến ngẫu nhiên, tương quan và hồi quy
subject: xac_suat_thong_ke
floor: 10
format: 2
summary_vi: Tầng ẩn: phân phối của Y = g(X), bảng đồng thời của hai biến, hiệp phương sai và tương quan, đường hồi quy bình phương tối thiểu, và ba tiên đề làm nền cho mọi công thức xác suất.
skills: [xs_t10_ham_bien_ngau_nhien, xs_t10_vecto_ngau_nhien, xs_t10_tuong_quan, xs_t10_hoi_quy, xs_t10_tien_de]
---
## Hàm của một biến ngẫu nhiên

:::hook
Mô hình dự đoán có sai số e; hàm mất mát là e^2. Muốn biết mất mát phân phối ra sao thì phải đi từ phân phối của chính e.
:::

:::figure map
caption: Y = X^2: -1 và 1 cùng tới Y = 1, nên P(Y = 1) phải cộng hai xác suất.
col "X" -1 0 1 2
col "Y" 0 1 4
-1 -> 1 do
0 -> 0
1 -> 1 do
2 -> 4
:::

:::core
Mỗi sự kiện về Y = g(X) là một sự kiện về X. Rời rạc: cộng xác suất các x cùng tới một y. Liên tục: lập F_Y rồi đạo hàm.
:::

$$ P(Y = y) = \sum_{x:\, g(x) = y} P(X = x) $$

Kỳ vọng thì khỏi lập bảng của Y: E(g(X)) = tổng g(x) P(X = x). Nói chung số đó khác g(E(X)).

Ví dụ: X nhận -1, 0, 1, 2 với xác suất 1/8, 3/8, 1/4, 1/4; Y = X^2.

1. P(Y = 1) = 1/8 + 1/4 = 3/8; P(Y = 0) = 3/8; P(Y = 4) = 1/4.
2. E(Y) = 0 . 3/8 + 1 . 3/8 + 4 . 1/4 = 11/8.
3. E(X) = 5/8, nên (E(X))^2 = 25/64: khác hẳn 11/8.

> Lỗi thường gặp: viết P(Y = 1) = P(X = 1), bỏ quên giá trị x = -1 cũng cho Y = 1.

:::check
Q: X nhận -2, -1, 0, 1, 2 với xác suất 1/10, 1/5, 2/5, 1/5, 1/10. Với Y = X^2, tính P(Y = 1) và E(Y).
A: P(Y = 1) = 1/5 + 1/5 = 2/5. E(Y) = 4/10 + 1/5 + 0 + 1/5 + 4/10 = 6/5.
:::

### Biến liên tục: lập F_Y rồi đạo hàm

:::figure plane
caption: X đều trên (-1, 1), Y = X^2: mật độ 1/(2 sqrt(y)) dồn về gần 0, vì X gần 0 thì X^2 còn gần 0 hơn.
size: 170 80
x: 0 1.1 0.5
y: 0 3 1
names: y f
curve "1/(2*sqrt(x))" 0.03 1 xanh
:::

Không cộng từng điểm được, nên đi qua hàm phân phối: F_Y(y) = P(g(X) < y), giải ra một sự kiện của X, tính xác suất, rồi đạo hàm theo y. Cuối cùng thử lại: tích phân của f_Y phải bằng 1.

Ví dụ: X đều trên (-1, 1), Y = X^2, với 0 < y < 1.

1. Y < y nghĩa là -sqrt(y) < X < sqrt(y): đủ cả hai phía của 0.
2. F_Y(y) = 2 sqrt(y)/2 = sqrt(y).
3. f_Y(y) = 1/(2 sqrt(y)); tích phân trên (0, 1) bằng 1.

Với Y = aX + b có sẵn công thức:

$$ f_Y(y) = \frac{1}{|a|}\, f_X\!\left(\frac{y - b}{a}\right) $$

> Lỗi thường gặp: quên nhánh âm khi giải X^2 < y, hay viết f_Y(y) = f_X(sqrt(y)) mà thiếu thừa số 1/(2 sqrt(y)).

:::check
Q: X ~ N(0, 1), Y = X^2. Tính P(Y < 4), dùng Phi(2) = 0.4772.
A: Y < 4 là -2 < X < 2: P = 2 Phi(2) = 0.9544.
:::

## Vectơ ngẫu nhiên hai chiều

:::hook
Hệ gợi ý ghi cùng lúc nhóm tuổi và thể loại phim của mỗi người xem. Bảng đồng thời cho biết từng cặp hay gặp đến đâu.
:::

:::figure grid
caption: Hàng là X, cột là Y. Cộng hàng ra biên của X, cộng cột ra biên của Y. Biết X = 0 thì chỉ nhìn hàng xanh.
table
head "Y = 0" "Y = 1" "Y = 2" "P(X)"
side "X = 0" "X = 1" "P(Y)"
row 1/6 1/4 1/12 1/2
row 1/6 1/12 1/4 1/2
row 1/3 1/3 1/3 1
mark row 1 xanh
:::

:::core
Cộng theo hàng được biên của X, theo cột được biên của Y. Điều kiện X = i thì thu về hàng i và chia cho tổng hàng đó.
:::

$$ P(X = i) = \sum_j P(X = i, Y = j), \qquad P(Y = j \mid X = i) = \frac{P(X = i, Y = j)}{P(X = i)} $$

Ô chưa biết tìm từ tổng các ô bằng 1.

Ví dụ: đọc bảng trong hình.

1. P(Y = 1 | X = 0) = (1/4)/(1/2) = 1/2.
2. P(X + Y = 2) = ô (0, 2) + ô (1, 1) = 1/12 + 1/12 = 1/6.

> Lỗi thường gặp: chia cho tổng cột khi điều kiện nằm ở hàng.

:::check
Q: Với bảng trong hình, tính P(X = 1 | Y = 2).
A: Điều kiện ở cột Y = 2, tổng cột 1/3: P = (1/4)/(1/3) = 3/4.
:::

### Độc lập: mọi ô bằng tích hai biên

X và Y độc lập khi biết X không làm đổi phân phối của Y: mọi ô phải bằng tích biên hàng nhân biên cột. Một ô lệch là đủ bác bỏ. Hai biên cũng không đủ dựng lại bảng: cùng biên có thể có nhiều bảng.

$$ P(X = i, Y = j) = P(X = i)\,P(Y = j) \quad \forall\, i, j $$

Ví dụ: kiểm tra bảng trong hình.

1. Ô (0, 0): 1/6 = 1/2 . 1/3, khớp.
2. Ô (0, 1): 1/4 khác 1/2 . 1/3 = 1/6.
3. Có ô lệch, nên X và Y không độc lập.

> Lỗi thường gặp: thấy một ô khớp đã kết luận độc lập.

:::check
Q: Bảng [1/6, 1/3; 1/6, 1/3] (hàng là X = 0, 1; cột là Y = 0, 1). X và Y có độc lập không?
A: Biên X: 1/2, 1/2; biên Y: 1/3, 2/3. Cả bốn ô bằng tích (1/6, 1/3, 1/6, 1/3): độc lập.
:::

## Hiệp phương sai và hệ số tương quan

:::hook
Số giờ luyện và điểm thi thường cùng tăng. Hiệp phương sai nói "cùng chiều", hệ số tương quan nói "chặt đến đâu", không phụ thuộc đơn vị đo.
:::

:::figure plane
caption: Mỗi điểm góp (x - x_tb)(y - y_tb). Góc phải trên và trái dưới góp dương, hai góc kia góp âm: tổng dương, Cov > 0.
size: 170 95
x: 0 6 1
y: 0 6 1
line 3 0 3 6 xam dash "x_tb" pos=n
line 0 3 6 3 xam dash "y_tb" pos=e
point 1 1.5 xanh
point 1.5 2.5 xanh
point 2.5 2 xanh
point 3.5 4 xanh
point 4.5 3.5 xanh
point 5 5 xanh
point 2 3.6 do
point 4 2.4 do
:::

:::core
Cov đo hai biến cùng lệch về một phía quanh kỳ vọng. Chia cho hai độ lệch chuẩn được rho trong [-1, 1], chỉ đo quan hệ tuyến tính.
:::

$$ \mathrm{Cov}(X, Y) = E\big[(X - E(X))(Y - E(Y))\big] = E(XY) - E(X)\,E(Y) $$

$$ \rho(X, Y) = \frac{\mathrm{Cov}(X, Y)}{\sigma(X)\,\sigma(Y)}, \qquad -1 \le \rho \le 1 $$

Ví dụ: X, Y nhận 0, 1 với bảng [2/5, 1/10; 1/10, 2/5] (hàng là X).

1. E(X) = E(Y) = 1/2; E(XY) = ô (1, 1) = 2/5.
2. Cov = 2/5 - 1/4 = 3/20; V(X) = V(Y) = 1/2 . 1/2 = 1/4.
3. rho = (3/20)/(1/4) = 3/5.

> Lỗi thường gặp: viết E(XY) = E(X)E(Y) khi chưa biết hai biến không tương quan; coi Cov = 0 là độc lập (Y = X^2 với X đều trên -1, 0, 1 có Cov = 0).

:::check
Q: V(X) = 4, V(Y) = 9, Cov(X, Y) = -3. Tính rho(X, Y).
A: rho = -3/(2 . 3) = -1/2: chia cho tích hai độ lệch chuẩn, không phải hai phương sai.
:::

### Phương sai của tổng và phép đổi biến

Khi hai biến không độc lập, phương sai của tổng có thêm số hạng chéo; hằng số cộng thêm không đổi Cov, hệ số nhân thì kéo theo.

- V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y).
- Cov(aX + b, cY + d) = ac Cov(X, Y); nhân một biến với số âm đổi dấu rho.
- rho = 1 hay -1 đúng khi Y = aX + b với a > 0 hay a < 0.

Ví dụ: V(X) = 3, V(Y) = 2, Cov(X, Y) = 1. Tính V(2X - Y) và Cov(2X + 1, 5 - Y).

1. V(2X - Y) = 4 . 3 + 2 + 2 . 2 . (-1) . 1 = 10.
2. Cov(2X + 1, 5 - Y) = 2 . (-1) . 1 = -2.

:::check
Q: V(X) = 4, V(Y) = 1, Cov(X, Y) = 1. Tính V(X - 2Y).
A: 4 + 4 . 1 + 2 . 1 . (-2) . 1 = 4.
:::

## Hồi quy tuyến tính đơn

:::hook
Dự đoán doanh thu từ chi phí quảng cáo, giá nhà từ diện tích: mô hình máy học đơn giản nhất là một đường thẳng kẻ xuyên đám điểm dữ liệu.
:::

:::figure plane
caption: Năm điểm và đường hồi quy y = 0.6 + x. Đường đi qua điểm trung bình (2, 2.6); các đoạn dọc là phần dư, cộng lại bằng 0.
size: 180 100
x: -0.5 4.5 1
y: 0 5.5 1
line 0 0.6 4 4.6 do
segment 0 1 0 0.6 xam
segment 1 1 1 1.6 xam
segment 2 3 2 2.6 xam
segment 3 3 3 3.6 xam
segment 4 5 4 4.6 xam
point 0 1 xanh
point 1 1 xanh
point 2 3 xanh
point 3 3 xanh
point 4 5 xanh
point 2 2.6 do "TB" pos=e
:::

:::core
Đường hồi quy làm tổng bình phương độ lệch dọc nhỏ nhất, và luôn đi qua điểm trung bình (x_tb, y_tb).
:::

$$ b = \frac{S_{xy}}{S_{xx}} = \frac{\sum (x_i - x_{tb})(y_i - y_{tb})}{\sum (x_i - x_{tb})^2}, \qquad a = y_{tb} - b\,x_{tb} $$

Ví dụ: các điểm trong hình (0, 1), (1, 1), (2, 3), (3, 3), (4, 5).

1. x_tb = 2, y_tb = 13/5; S_xx = 10.
2. Độ lệch y: -8/5, -8/5, 2/5, 2/5, 12/5, nên S_xy = 16/5 + 8/5 + 0 + 2/5 + 24/5 = 10.
3. b = 1, a = 13/5 - 2 = 3/5: y = 3/5 + x.

> Lỗi thường gặp: chia ngược, b = S_xx/S_xy; hay lấy S_xy/S_yy làm hệ số góc.

:::check
Q: Đường hồi quy y = 3/5 + x ở trên dự đoán bao nhiêu tại x = 2.5?
A: 3/5 + 2.5 = 3.1. Nằm trong khoảng dữ liệu nên dự đoán này đáng tin hơn một dự đoán ở x = 20.
:::

### Đọc đường hồi quy: r và r^2

Hệ số góc còn viết được qua hệ số tương quan mẫu r: b = r s_y/s_x. r^2 là phần biến thiên của y mà đường thẳng giải thích; phần còn lại là phần dư. Hồi quy x theo y là đường khác (hệ số góc S_xy/S_yy), trừ khi các điểm thẳng hàng. Và tương quan không phải nhân quả.

Ví dụ: x_tb = 10, y_tb = 20, s_x = 2, s_y = 6, r = 1/2.

1. b = (1/2) . 6/2 = 3/2.
2. a = 20 - 3/2 . 10 = 5.
3. r^2 = 1/4: đường thẳng giải thích 25% biến thiên của y.

:::check
Q: x_tb = 4, y_tb = 10, s_x = 2, s_y = 5, r = 0.8. Tìm b, a và dự đoán y tại x = 6.
A: b = 0.8 . 5/2 = 2; a = 10 - 2 . 4 = 2; y(6) = 2 + 12 = 14.
:::

## Tiên đề xác suất

:::hook
Mọi công thức từ tầng 1 tới giờ đều suy ra từ ba luật chơi. Mô hình nào xuất "xác suất" âm, hay tổng khác 1, là đã phạm luật.
:::

:::figure flow
caption: Từ ba tiên đề, từng hệ quả được suy ra; không cái nào cần thêm luật mới.
box "3 tiên đề" vang
link "Omega và rỗng"
box "P(rỗng) = 0"
link "A và Ā"
box "P(Ā) = 1 - P(A)"
link "P(Ā) >= 0"
box "P(A) <= 1" luc
:::

:::core
Ba luật: xác suất không âm, cả Omega có xác suất 1, sự kiện xung khắc thì cộng. Mọi công thức khác là hệ quả.
:::

$$ P(A) \ge 0, \qquad P(\Omega) = 1, \qquad A \cap B = \varnothing \Rightarrow P(A \cup B) = P(A) + P(B) $$

- A nằm trong B thì P(A) <= P(B): P(B) = P(A) + P(B \ A) và P(B \ A) >= 0.
- Công thức cộng P(A + B) = P(A) + P(B) - P(AB): tách A + B = A + (B \ A) và B = AB + (B \ A).

Ví dụ: Omega = {1, 2, 3}, đặt P({k}) = c . k.

1. Chuẩn hóa: c(1 + 2 + 3) = 1, nên c = 1/6; các giá trị đều không âm.
2. Cộng tính: P({1, 3}) = 1/6 + 3/6 = 2/3, và P({2}) = 1/3 bù lại đủ 1.

> Lỗi thường gặp: coi "P(A) <= 1" hay "P(Ā) = 1 - P(A)" là tiên đề; chúng là hệ quả.

:::check
Q: P(A) = 2/3, P(B) = 1/2, P(A + B) = 5/6. Tính P(AB). Bộ 1/2, 1/2, 1/4 trên Omega = {a, b, c} có phải xác suất không?
A: P(AB) = 2/3 + 1/2 - 5/6 = 1/3. Không: tổng 5/4 khác 1, phạm tiên đề P(Omega) = 1.
:::
