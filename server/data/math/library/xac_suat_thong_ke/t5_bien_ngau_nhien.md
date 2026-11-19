---
id: xs_lib_t5
title_vi: Biến ngẫu nhiên, bảng phân phối và hàm phân phối
subject: xac_suat_thong_ke
floor: 5
summary_vi: Gắn một con số với mỗi kết quả của phép thử để tính toán trên các con số đó: bảng phân phối cho biến rời rạc, hàm mật độ cho biến liên tục, và hàm phân phối F(x) = P(X < x) dùng được cho cả hai.
skills: [xs_t5_bien_ngau_nhien, xs_t5_bang_phan_phoi, xs_t5_ham_phan_phoi, xs_t5_mat_do, xs_t5_xac_suat_khoang]
---
## Biến ngẫu nhiên rời rạc và liên tục

Một biến ngẫu nhiên X gắn với mỗi kết quả của phép thử một số thực. Tung 3 đồng xu, X = số lần ngửa trừ số lần sấp: kết quả NNS cho X = 1, kết quả SSS cho X = -3. X nhận các giá trị -3, -1, 1, 3.

Có hai loại chính:

- Rời rạc: các giá trị tách rời, liệt kê được (hữu hạn hoặc vô hạn đếm được). Số chấm xúc xắc, số phế phẩm, số lần gieo đến khi ra mặt 6, số cuộc gọi trong một giờ.
- Liên tục: nhận mọi giá trị trong một khoảng. Thời gian chờ, chiều cao, khối lượng.

Với biến liên tục, xác suất nhận đúng một giá trị bằng 0:

$$ P(X = c) = 0 $$

Các giá trị của một biến không nhất thiết đồng khả năng. Gieo hai xúc xắc, X = số chấm lớn hơn: P(X = 4) = (16 - 9)/36 = 7/36, vì có 16 cặp mà cả hai số chấm <= 4 và 9 cặp mà cả hai <= 3.

> Lỗi thường gặp: chia đều xác suất cho các giá trị. Lấy 2 bi từ hộp 2 đỏ, 3 xanh, số bi đỏ X nhận 0, 1, 2 nhưng P(X = 2) = 1/10, không phải 1/3: phải đếm trên 10 cách lấy đồng khả năng.

## Bảng phân phối xác suất

Biến rời rạc được mô tả bằng bảng: các giá trị x_1, x_2, ... và xác suất p_i = P(X = x_i). Một bảng đúng phải có:

$$ p_i \ge 0, \qquad \sum_i p_i = 1 $$

Ví dụ lấy cùng lúc 2 bi từ hộp 3 đỏ, 2 xanh, X = số bi đỏ:

1. Có C(5, 2) = 10 cách lấy đồng khả năng.
2. X = 0: 1 cách; X = 1: 3 . 2 = 6 cách; X = 2: 3 cách.
3. Bảng: P(X = 0) = 1/10, P(X = 1) = 3/5, P(X = 2) = 3/10; tổng bằng 1.

Điều kiện tổng bằng 1 giúp tìm hằng số: P(X = k) = ck với k = 1, ..., 4 cho 10c = 1, c = 1/10. Nó cũng là cách tính giá trị cuối: xạ thủ 3 viên đạn, trúng 2/3, bắn đến khi trúng; P(X = 1) = 2/3, P(X = 2) = 2/9, nên P(X = 3) = 1 - 2/3 - 2/9 = 1/9.

> Lỗi thường gặp: lập bảng mà không thử lại tổng. Tung 3 đồng xu, ghi P(X = 1) = 1/8 là quên rằng có ba dãy NSS, SNS, SSN; bảng 1/8, 1/8, 1/8, 1/8 có tổng 1/2, báo ngay là sai.

## Hàm phân phối F(x)

Trong tông môn này, hàm phân phối được định nghĩa với dấu nhỏ hơn hẳn:

$$ F(x) = P(X < x) $$

Với biến rời rạc, F(x) cộng xác suất của các giá trị nhỏ hơn hẳn x. Đồ thị là bậc thang: không đổi giữa hai giá trị liền nhau, và nhảy lên đúng p_i ngay sau giá trị x_i.

Ví dụ X nhận 0 và 1 với xác suất 1/3, 2/3:

- F(x) = 0 khi x <= 0.
- F(x) = 1/3 khi 0 < x <= 1.
- F(x) = 1 khi x > 1.

Đọc ngược: độ cao bước nhảy tại x_i là P(X = x_i). F bằng 0 khi x <= 1, 1/5 trên (1, 2], 7/10 trên (2, 4], 1 khi x > 4 cho P(X = 1) = 1/5, P(X = 2) = 1/2, P(X = 4) = 3/10.

F luôn không giảm, đi từ 0 đến 1. Hàm phân phối của biến liên tục là hàm liên tục: F(x) = kx^3 trên (0, 2] nối với 1 tại x = 2 cho k = 1/8.

> Lỗi thường gặp: tính F(x) bằng P(X <= x). Với X nhận 1, 2, 3 có xác suất 1/4, 1/2, 1/4 thì F(2) = P(X < 2) = 1/4, không phải 3/4; giá trị bằng x không được tính.

## Hàm mật độ xác suất

Biến liên tục được mô tả bằng hàm mật độ f: xác suất là diện tích dưới đồ thị f. Một hàm là hàm mật độ khi:

$$ f(x) \ge 0, \qquad \int_{-\infty}^{+\infty} f(x)\,dx = 1 $$

Mật độ và hàm phân phối liên hệ với nhau qua tích phân và đạo hàm:

$$ F(x) = \int_{-\infty}^{x} f(t)\,dt, \qquad f(x) = F'(x) $$

Ví dụ tìm k để f(x) = k(1 - x^2) trên [-1, 1] (bằng 0 nơi khác) là hàm mật độ:

1. Tích phân của 1 - x^2 từ -1 đến 1 bằng 2 - 2/3 = 4/3.
2. k . 4/3 = 1, nên k = 3/4, và f >= 0 trên [-1, 1].

Đi ngược: F(x) = 3x^2 - 2x^3 trên (0, 1] cho f(x) = 6x - 6x^2, f(1/2) = 3/2.

f(x) không phải là xác suất: nó có thể lớn hơn 1. f(x) = 24x^2 trên [0, 1/2] là hàm mật độ hợp lệ dù f(1/2) = 6.

> Lỗi thường gặp: nghĩ hàm mật độ không vượt quá 1, hoặc f(x) = P(X = x). Với biến liên tục P(X = x) = 0; điều kiện duy nhất là f không âm và tổng diện tích bằng 1.

## Xác suất rơi vào một khoảng

Với quy ước F(x) = P(X < x), công thức sau đúng cho mọi biến:

$$ P(a \le X < b) = F(b) - F(a) $$

Với biến liên tục, các dấu < và <= ở hai đầu không làm đổi gì, và xác suất là diện tích dưới f trên đoạn đó:

$$ P(a \le X \le b) = \int_a^b f(x)\,dx $$

Ví dụ f(x) = kx^2 trên [0, 3]:

1. 9k = 1 nên k = 1/9, và F(x) = x^3/27 trên [0, 3].
2. P(1 <= X < 2) = F(2) - F(1) = 8/27 - 1/27 = 7/27.

Với biến rời rạc, phải giữ đúng dấu ở đầu phải. X nhận 1, 2, 3, 4 với xác suất 1/10, 1/5, 3/10, 2/5:

- P(2 <= X < 3) = F(3) - F(2) = 1/5: chỉ có giá trị 2.
- P(2 <= X <= 3) = F(4) - F(2) = 1/2: có cả giá trị 3.

> Lỗi thường gặp: dùng F(b) - F(a) cho P(a <= X <= b) với biến rời rạc. F(b) không chứa P(X = b), nên đáp số thiếu đúng một bước nhảy.
