---
id: tr_lib_t2
title_vi: Bài toán đếm
subject: toi_uu_roi_rac
floor: 2
summary_vi: Những công thức đếm dùng hằng ngày: chỉnh hợp, hoán vị, tổ hợp, tổ hợp lặp, nguyên lý bù trừ và hệ thức truy hồi, kèm cách nhận ra bài nào cần công thức nào.
skills: [tr_t2_chinh_hop, tr_t2_hoan_vi, tr_t2_to_hop, tr_t2_to_hop_lap, tr_t2_bu_tru, tr_t2_truy_hoi]
---
## Chỉnh hợp lặp và không lặp

Một chỉnh hợp chập k của n phần tử là một dãy có thứ tự gồm k phần tử lấy từ n phần tử.

Nếu được lặp lại (chỉnh hợp lặp), mỗi vị trí có n cách độc lập với nhau:

$$ \bar{A}_n^k = n^k $$

Nếu không được lặp (chỉnh hợp không lặp), vị trí đầu có n cách, vị trí sau ít hơn một cách:

$$ A_n^k = n(n-1)\cdots(n-k+1) = \frac{n!}{(n-k)!} $$

Ví dụ: 8 tông môn tranh ba giải nhất, nhì, ba.

1. Giải khác nhau nên thứ tự có ý nghĩa; một tông môn không nhận hai giải nên không lặp.
2. Đây là chỉnh hợp không lặp chập 3 của 8.
3. A_8^3 = 8 . 7 . 6 = 336.

Còn mật lệnh 3 ký tự lấy từ 5 phù văn, được lặp, là chỉnh hợp lặp: 5^3 = 125.

> Lỗi thường gặp: viết A_n^k = n!/k!. Mẫu số là (n - k)!, phần đuôi của n! không được dùng tới. Kiểm tra nhanh: A_6^4 phải là tích 4 số 6 . 5 . 4 . 3 = 360.

## Hoán vị và hoán vị lặp

Hoán vị của n phần tử là một cách xếp cả n phần tử thành hàng, tức là chỉnh hợp không lặp chập n:

$$ P_n = n! = n(n-1)\cdots 2 \cdot 1, \quad 0! = 1 $$

Khi có vật giống nhau, đổi chỗ chúng không tạo cách xếp mới. Có n_1 vật loại 1, n_2 vật loại 2, ..., n_m vật loại m (tổng là n) thì số cách xếp thành hàng là:

$$ \frac{n!}{n_1! \, n_2! \cdots n_m!} $$

Hai kỹ thuật hay dùng:

- Muốn hai người đứng cạnh nhau: buộc họ thành một khối, xếp khối cùng những người còn lại, rồi nhân với số cách xếp trong khối.
- Muốn hai người không đứng cạnh nhau: lấy tổng số cách trừ đi số cách đứng cạnh nhau.

Xếp n người quanh một bàn tròn, xoay bàn coi như không đổi: có (n - 1)! cách, vì mỗi cách ngồi ứng với n cách xếp hàng.

Ví dụ: 3 viên đỏ giống nhau và 2 viên xanh giống nhau xếp thành hàng có 5!/(3! . 2!) = 10 cách.

> Lỗi thường gặp: buộc hai người thành một khối nhưng quên nhân 2 cho hai thứ tự bên trong khối. Với 6 người, số cách An và Bình đứng cạnh nhau là 2 . 5! = 240, không phải 120.

## Tổ hợp

Tổ hợp chập k của n phần tử là một tập con k phần tử: chọn mà không kể thứ tự. Mỗi tổ hợp xếp được thành k! chỉnh hợp, nên:

$$ C_n^k = \frac{A_n^k}{k!} = \frac{n!}{k! \, (n-k)!} $$

Các tính chất nên thuộc:

$$ C_n^k = C_n^{n-k} $$

$$ C_n^k = C_{n-1}^{k-1} + C_{n-1}^{k} $$

$$ (a+b)^n = \sum_{k=0}^{n} C_n^k a^{k} b^{n-k} $$

Công thức thứ hai (tam giác Pascal) chia các tập con theo việc có chứa một phần tử cố định hay không. Công thức cuối là nhị thức Newton; thay a = b = 1 được tổng mọi C_n^k bằng 2^n.

Khi đề bài có chữ "ít nhất một", thường đếm phần bù sẽ gọn hơn. Ví dụ tổ 6 nam 4 nữ, chọn 3 người có ít nhất 1 nữ:

1. Mọi cách chọn 3 người: C_10^3 = 120.
2. Cách chọn toàn nam: C_6^3 = 20.
3. Có ít nhất 1 nữ: 120 - 20 = 100.

> Lỗi thường gặp: dùng A_n^k khi thứ tự không quan trọng. Số đoạn nối hai trong 8 đỉnh là C_8^2 = 28, không phải 8 . 7 = 56, vì đoạn AB và đoạn BA là một.

## Tổ hợp lặp và nghiệm nguyên

Chọn k vật từ n loại, mỗi loại có nhiều vật giống nhau, được chọn cùng loại nhiều lần, không kể thứ tự: đó là tổ hợp lặp. Gọi x_i là số vật lấy ở loại i, ta cần đếm nghiệm nguyên không âm của x_1 + x_2 + ... + x_n = k.

Mẹo chia vách: xếp k viên đá và n - 1 vách ngăn thành một hàng; số đá giữa các vách là x_1, x_2, ..., x_n. Hàng có n + k - 1 vị trí, chọn vị trí cho vách:

$$ C_{n+k-1}^{n-1} = C_{n+k-1}^{k} $$

Ví dụ: x_1 + x_2 + x_3 = 5 có C_7^2 = 21 nghiệm nguyên không âm.

Khi có cận dưới, đổi biến cho về không âm. Ví dụ đếm nghiệm của x_1 + x_2 + x_3 + x_4 = 10 với mọi x_i >= 2:

1. Đặt y_i = x_i - 2 thì y_i >= 0.
2. Phương trình thành y_1 + y_2 + y_3 + y_4 = 10 - 8 = 2.
3. Số nghiệm: C_5^3 = 10.

Nghiệm nguyên dương là trường hợp cận dưới bằng 1.

> Lỗi thường gặp: quên trừ phần cận dưới khỏi vế phải, hoặc đếm sai số vị trí trong hàng. Với tổng n và k ẩn, hàng luôn có n + k - 1 vị trí, không phải n + k.

## Nguyên lý bù trừ

Khi các trường hợp có phần chung, quy tắc cộng đếm phần chung nhiều lần. Nguyên lý bù trừ sửa lại:

$$ |A \cup B| = |A| + |B| - |A \cap B| $$

$$ |A \cup B \cup C| = \sum |A| - \sum |A \cap B| + |A \cap B \cap C| $$

Ở công thức thứ hai, tổng thứ nhất chạy qua ba tập, tổng thứ hai qua ba cặp. Một phần tử thuộc cả ba tập được cộng 3 lần, trừ 3 lần, rồi cộng lại 1 lần: cuối cùng được tính đúng một lần.

Bài "không chia hết cho số nào trong 2, 3, 5" là bài đếm phần bù: đếm các số chia hết cho ít nhất một số rồi trừ khỏi tổng.

1. Từ 1 đến 100: chia hết cho 2, 3, 5 lần lượt có 50, 33, 20 số.
2. Chia hết cho 6, 10, 15 có 16, 10, 6 số; cho 30 có 3 số.
3. Chia hết cho ít nhất một số: 50 + 33 + 20 - 16 - 10 - 6 + 3 = 74.
4. Không chia hết cho số nào: 100 - 74 = 26.

Số các bội của d từ 1 đến N là phần nguyên của N/d.

> Lỗi thường gặp: trừ phần chung của cả ba tập thay vì cộng lại. Dấu đổi luân phiên: cộng các tập, trừ các cặp, cộng bộ ba.

## Hệ thức truy hồi

Hệ thức truy hồi tính số hạng thứ n từ các số hạng đứng trước. Muốn lập hệ thức cho một bài đếm, hãy chia các cấu hình cỡ n theo phần cuối của chúng, mỗi phần quy về cấu hình nhỏ hơn cùng loại.

Ví dụ s_n là số xâu nhị phân độ dài n không có hai chữ số 1 liền nhau. Xâu kết thúc bằng 0 thì bỏ chữ số cuối; kết thúc bằng 1 thì chữ số trước phải là 0, bỏ hai chữ số cuối. Được s_n = s_(n - 1) + s_(n - 2), với s_1 = 2, s_2 = 3.

Tháp Hà Nội: dời n - 1 đĩa sang cọc phụ, chuyển đĩa lớn, rồi dời n - 1 đĩa về: h_n = 2h_(n - 1) + 1.

Hệ thức tuyến tính hệ số hằng cấp hai giải bằng phương trình đặc trưng:

$$ a_n = c_1 a_{n-1} + c_2 a_{n-2} \quad \to \quad r^2 = c_1 r + c_2 $$

Nếu phương trình đặc trưng có hai nghiệm phân biệt r_1, r_2 thì:

$$ a_n = A \, r_1^{n} + B \, r_2^{n} $$

rồi tìm A, B từ hai số hạng đầu. Ví dụ a_n = a_(n - 1) + 2a_(n - 2), a_0 = 2, a_1 = 1:

1. r^2 - r - 2 = 0 có nghiệm 2 và -1.
2. a_n = A . 2^n + B . (-1)^n.
3. n = 0: A + B = 2. n = 1: 2A - B = 1. Giải ra A = B = 1.
4. a_n = 2^n + (-1)^n. Thử lại a_2 = 5 = 1 + 2 . 2.

> Lỗi thường gặp: thay n = 1 mà quên rằng (-1)^1 = -1, nên viết 2A + B thay vì 2A - B. Luôn thử lại công thức với một số hạng tính trực tiếp từ hệ thức.
