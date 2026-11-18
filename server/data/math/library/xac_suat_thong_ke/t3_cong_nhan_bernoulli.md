---
id: xs_lib_t3
title_vi: Công thức cộng, nhân, xác suất có điều kiện và Bernoulli
subject: xac_suat_thong_ke
floor: 3
summary_vi: Bốn công cụ để tính xác suất mà không phải liệt kê cả không gian mẫu: cộng cho chữ "hoặc", nhân cho chữ "và", điều kiện khi đã biết thêm thông tin, và Bernoulli cho các lần thử lặp lại.
skills: [xs_t3_cong_thuc_cong, xs_t3_dieu_kien, xs_t3_cong_thuc_nhan, xs_t3_doc_lap, xs_t3_bernoulli]
---
## Công thức cộng xác suất

Với hai sự kiện bất kỳ A và B:

$$ P(A + B) = P(A) + P(B) - P(AB) $$

Số hạng cuối có mặt vì những kết quả thuộc cả A và B đã được tính hai lần, một lần trong P(A) và một lần trong P(B). Khi A, B xung khắc thì P(AB) = 0 và công thức chỉ còn P(A) + P(B).

Ví dụ rút một lá từ bộ 52 lá, tính xác suất được lá cơ hoặc lá K:

1. P(cơ) = 13/52, P(K) = 4/52.
2. Lá K cơ thuộc cả hai, nên P(AB) = 1/52.
3. P = 13/52 + 4/52 - 1/52 = 16/52 = 4/13.

Với ba sự kiện, cộng ba xác suất, trừ ba xác suất của từng cặp, rồi cộng lại xác suất của cả ba. Chọn ngẫu nhiên một số từ 1 đến 30, xác suất chia hết cho 2, 3 hoặc 5 là (15 + 10 + 6 - 5 - 3 - 2 + 1)/30 = 22/30 = 11/15.

Công thức cộng còn dùng ngược: biết ba trong bốn đại lượng P(A), P(B), P(AB), P(A + B) thì tìm được cái còn lại. Nếu P(A) + P(B) > 1 thì A và B chắc chắn không xung khắc.

> Lỗi thường gặp: cộng thẳng P(A) + P(B) khi A, B có kết quả chung. Lá cơ hoặc lá K có xác suất 16/52, không phải 17/52.

## Xác suất có điều kiện

Xác suất của A khi biết B đã xảy ra, viết P(A|B), được tính bằng cách thu hẹp không gian mẫu về B:

$$ P(A \mid B) = \frac{P(AB)}{P(B)}, \quad P(B) > 0 $$

Với các kết quả đồng khả năng, đó chính là số kết quả thuộc cả A và B chia cho số kết quả thuộc B.

Ví dụ gieo hai xúc xắc, biết tổng bằng 8, tính xác suất có một mặt 6:

1. Biết tổng bằng 8, chỉ còn (2, 6), (3, 5), (4, 4), (5, 3), (6, 2): 5 cặp.
2. Có mặt 6: (2, 6) và (6, 2).
3. P = 2/5.

Với một bảng số liệu, điều kiện cho biết lấy hàng nào hoặc cột nào làm mẫu số. Một trường có khoa Toán 30 nam, 20 nữ và khoa Lý 10 nam, 40 nữ:

- P(nữ | khoa Toán) = 20/50 = 2/5: mẫu số là 50 sinh viên khoa Toán.
- P(khoa Toán | nữ) = 20/60 = 1/3: mẫu số là 60 sinh viên nữ.

Hai con số khác nhau dù cùng tử số 20.

> Lỗi thường gặp: lẫn P(A|B) với P(B|A). Sự kiện đứng sau dấu | là điều đã biết, và xác suất của nó nằm ở mẫu số. Chia nhầm cho P(A) là đã tính một câu hỏi khác.

## Công thức nhân xác suất

Nhân hai vế của định nghĩa xác suất có điều kiện với P(A):

$$ P(AB) = P(A)\,P(B \mid A) $$

Cách dùng điển hình là các lần lấy nối tiếp không hoàn lại: xác suất của lần sau tính trên những gì còn lại sau lần trước. Với nhiều lần, cứ nhân tiếp.

$$ P(A_1 A_2 A_3) = P(A_1)\,P(A_2 \mid A_1)\,P(A_3 \mid A_1 A_2) $$

Ví dụ lô 8 sản phẩm có 2 phế phẩm, lấy lần lượt 3 sản phẩm không hoàn lại, tính xác suất cả 3 đều tốt:

1. Lần 1 tốt: 6/8.
2. Biết lần 1 tốt, còn 7 sản phẩm với 5 tốt: 5/7.
3. Biết hai lần đầu tốt, còn 6 sản phẩm với 4 tốt: 4/6.
4. Nhân lại: 6/8 . 5/7 . 4/6 = 5/14.

Thử chìa khóa cũng vậy: 5 chìa, 1 chìa đúng, thử lần lượt và bỏ chìa sai ra. Mở được ở lần thứ ba có xác suất 4/5 . 3/4 . 1/3 = 1/5.

> Lỗi thường gặp: không hoàn lại mà vẫn nhân các xác suất như lúc đầu. Rút 2 lá không hoàn lại, cả hai là át có xác suất 4/52 . 3/51 = 1/221, không phải 4/52 . 4/52.

## Sự kiện độc lập

A và B độc lập khi việc biết A xảy ra hay không không làm đổi xác suất của B. Định nghĩa dùng để kiểm tra là:

$$ P(AB) = P(A)\,P(B) $$

Nếu A, B độc lập thì các cặp A và đối của B, Ā và B, Ā và đối của B cũng độc lập. Các phép thử tách biệt về vật lý (hai xạ thủ bắn riêng, xúc xắc và đồng xu) thường được coi là độc lập.

Ví dụ hai xạ thủ bắn độc lập, trúng với xác suất 4/5 và 7/10, tính xác suất có ít nhất một người trúng:

1. Sự kiện đối: cả hai cùng trượt, 1/5 . 3/10 = 3/50.
2. P = 1 - 3/50 = 47/50.

Có lúc độc lập xuất hiện ở chỗ không ngờ: gieo hai xúc xắc, "xúc xắc 1 chẵn" và "tổng bằng 7" độc lập, vì P(AB) = 3/36 = 1/12 đúng bằng 1/2 . 1/6. Vì vậy phải tính, không đoán.

Mạch song song thông khi ít nhất một linh kiện tốt; mạch nối tiếp thông khi mọi linh kiện đều tốt. Với các linh kiện độc lập, mạch nối tiếp nhân xác suất tốt, mạch song song lấy 1 trừ tích các xác suất hỏng.

> Lỗi thường gặp: nghĩ rằng hai sự kiện không có kết quả chung thì độc lập. Đó là xung khắc, và hai sự kiện xung khắc có xác suất dương thì không bao giờ độc lập: biết A xảy ra là biết chắc B không xảy ra.

## Công thức Bernoulli

Dãy n phép thử Bernoulli là n phép thử độc lập, mỗi lần chỉ xét sự kiện A (thành công) xảy ra hay không, và P(A) = p như nhau ở mọi lần. Xác suất có đúng k lần thành công là:

$$ P_n(k) = C_n^k \, p^k (1-p)^{n-k} $$

Ý nghĩa từng phần: p^k (1 - p)^(n - k) là xác suất của một dãy cụ thể có k lần thành công ở những vị trí đã chọn, còn C(n, k) đếm số cách chọn k vị trí đó trong n lần.

Ví dụ thi trắc nghiệm 5 câu, mỗi câu 4 phương án, chọn ngẫu nhiên, tính xác suất đúng ít nhất 4 câu:

1. Đây là 5 phép thử Bernoulli với p = 1/4.
2. Đúng 4 câu: C(5, 4) (1/4)^4 (3/4) = 15/1024.
3. Đúng 5 câu: (1/4)^5 = 1/1024.
4. Cộng lại: 16/1024 = 1/64.

Câu hỏi "ít nhất 1 lần" nên tính qua sự kiện đối: 1 - (1 - p)^n. Ba sản phẩm, mỗi cái hỏng với xác suất 1/10, có ít nhất 1 cái hỏng với xác suất 1 - (9/10)^3 = 271/1000.

p không cần bằng 1/2; điều bắt buộc là các lần độc lập và p không đổi. Rút bài không hoàn lại không phải dãy Bernoulli, vì p đổi sau mỗi lần rút.

> Lỗi thường gặp: quên hệ số C(n, k). Gieo xúc xắc 4 lần, đúng 1 lần ra mặt 6 có xác suất 4 . (1/6)(5/6)^3 = 125/324, vì lần ra mặt 6 có thể là lần 1, 2, 3 hoặc 4.
