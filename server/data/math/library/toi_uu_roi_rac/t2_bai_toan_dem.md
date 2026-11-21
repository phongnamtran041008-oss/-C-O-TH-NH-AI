---
id: tr_lib_t2
title_vi: Bài toán đếm
subject: toi_uu_roi_rac
floor: 2
format: 2
summary_vi: Sáu công cụ đếm và cách nhận ra chúng: chỉnh hợp và hoán vị khi thứ tự có nghĩa, tổ hợp khi chỉ cần nhóm, chia vách khi vật giống nhau, bù trừ khi các tập chồng nhau, truy hồi khi bài lớn tựa vào bài nhỏ.
skills: [tr_t2_chinh_hop, tr_t2_hoan_vi, tr_t2_to_hop, tr_t2_to_hop_lap, tr_t2_bu_tru, tr_t2_truy_hoi]
---
## Chỉnh hợp lặp và không lặp

:::hook
Mã PIN được lặp chữ số, nên có 10^4 mã. Bảng xếp hạng 3 mô hình tốt nhất thì không: một mô hình không đứng hai hạng.
:::

:::figure grid
caption: Lấp 3 ô bằng 6 ký tự. Không lặp thì mỗi ô sau mất một lựa chọn.
table
head "ô 1" "ô 2" "ô 3" "số mã"
side "được lặp" "không lặp"
row 6 6 6 216
row 6 5 4 120
mark row 2 vang
:::

:::core
Chỉnh hợp là dãy có thứ tự lấp k chỗ bằng n vật: được lặp thì mỗi chỗ n cách, không lặp thì mỗi chỗ sau ít đi một cách.
:::

Được lặp: n^k. Không lặp: A_n^k là tích k số giảm dần bắt đầu từ n.

$$ A_n^k = n (n-1) \cdots (n-k+1) = \frac{n!}{(n-k)!} $$

Ví dụ: 9 mô hình thi đấu, xếp hạng nhất, nhì, ba. Có bao nhiêu bảng xếp hạng?

1. Hạng khác nhau nên thứ tự có nghĩa; một mô hình không giữ hai hạng nên không lặp.
2. A_9^3 = 9 . 8 . 7 = 504, đúng bằng 9!/6!.

> Lỗi thường gặp: viết n!/k!. Mẫu số là (n - k)!: A_7^3 = 7!/4! = 210, không phải 7!/3! = 840.

:::check
Q: Mật khẩu 2 ký tự lấy từ 6 ký tự. Được lặp có mấy mật khẩu, không lặp có mấy? Vì sao chênh 6?
A: 6^2 = 36 và A_6^2 = 6 . 5 = 30. Chênh đúng 6 mật khẩu hai ký tự giống nhau, như "aa".
:::

## Hoán vị và hoán vị lặp

:::hook
Trộn dữ liệu là chọn một hoán vị; đổi hai vật giống hệt thì hàng vẫn thế.
:::

:::figure grid
caption: Đánh số hai chữ A thì có 3! = 6 cách xếp. Xóa số đi, mỗi hàng 2! cách gộp làm một: còn 3!/2! = 3.
table
head "hàng" "khi đánh số"
row "AAB" "A1 A2 B, A2 A1 B"
row "ABA" "A1 B A2, A2 B A1"
row "BAA" "B A1 A2, B A2 A1"
:::

:::core
Xếp hết n vật khác nhau thành hàng có n! cách; vật giống nhau thì chia cho giai thừa số vật mỗi loại, vì đổi chỗ chúng không ra hàng mới.
:::

- Đứng cạnh nhau: buộc thành một khối, xếp, rồi nhân 2 cho thứ tự trong khối.
- Không cạnh nhau: lấy tổng số cách trừ số cách cạnh nhau.
- Bàn tròn: n!/n = (n - 1)! cách, vì xoay bàn không đổi chỗ ngồi.
- 0! = 1: xếp 0 vật có đúng một cách, là không làm gì.

Ví dụ: xếp 2 viên đỏ, 2 viên xanh, 1 viên vàng thành hàng.

1. Nếu 5 viên khác nhau: 5! = 120 cách.
2. Chia cho 2! (đỏ), 2! (xanh), 1! (vàng): 120/4 = 30 hàng.

> Lỗi thường gặp: buộc An, Bình thành khối mà quên nhân 2.

:::check
Q: 5 người ngồi quanh bàn tròn (xoay coi như nhau), An và Bình ngồi cạnh nhau. Có bao nhiêu cách?
A: Khối An Bình cùng 3 người là 4 phần tử quanh bàn: 3! = 6. Nhân 2 cho trong khối: 12.
:::

## Tổ hợp

:::hook
Chọn 3 đặc trưng trong 10 cho mô hình: chỉ cần biết bộ nào, không kể thứ tự.
:::

:::figure bars
caption: C_5^k là số nhóm k trong 5 vật, cũng là hệ số của x^k trong (1 + x)^5. Cột đối xứng; cộng lại 32 = 2^5.
size: 200 80
bar "k=0" 1
bar "k=1" 5
bar "k=2" 10 xanh
bar "k=3" 10 xanh
bar "k=4" 5
bar "k=5" 1
:::

:::core
Tổ hợp đếm nhóm không kể thứ tự: mỗi nhóm k vật xuất hiện k! lần trong các dãy có thứ tự, nên lấy A_n^k chia k!.
:::

$$ C_n^k = \frac{A_n^k}{k!} = \frac{n!}{k!\,(n-k)!} $$

Chọn k để lấy là chọn n - k để bỏ: C_n^k = C_n^(n-k). Hệ số của x^k trong (1 + x)^n là C_n^k: chọn x ở k trong n thừa số. Gặp "ít nhất một" thì đếm phần bù.

Ví dụ: 5 kiếm tu, 4 pháp tu. Chọn 4 người có ít nhất 1 pháp tu.

1. Mọi nhóm 4 trong 9 người: C_9^4 = 126.
2. Nhóm toàn kiếm tu: C_5^4 = 5.
3. Có ít nhất 1 pháp tu: 126 - 5 = 121.

> Lỗi thường gặp: đoạn nối 2 trong 7 điểm là C_7^2 = 21, không phải A_7^2 = 42.

:::check
Q: Nhìn hình: hệ số của x^3 trong (1 + x)^5 là bao nhiêu? Sao nó bằng hệ số của x^2?
A: C_5^3 = 10. Chọn 3 thừa số cho x cũng là chọn 2 thừa số cho 1: C_5^3 = C_5^2.
:::

## Tổ hợp lặp và nghiệm nguyên

:::hook
Chia 4 viên linh thạch giống nhau cho 3 đệ tử, có người không được viên nào. Viên nào đi đâu không quan trọng, chỉ quan trọng mỗi người được mấy viên.
:::

:::figure grid
caption: 4 viên đá (o) và 2 vách (|) cho nghiệm (2, 0, 2). Mỗi cách đặt 2 vách vào 6 chỗ là một nghiệm: C_6^2 = 15.
table
head "1" "2" "3" "4" "5" "6"
row o o | | o o
mark cell 1 3 do
mark cell 1 4 do
:::

:::core
Chia k vật giống nhau vào n hộp là xếp k viên đá với n - 1 vách thành hàng: chỉ cần chọn chỗ cho các vách.
:::

$$ C_{n+k-1}^{n-1} = C_{n+k-1}^{k} $$

Mua k viên đan từ n loại, được trùng loại, cũng là bài này: x_i là số viên loại i. Có cận dưới x_i >= a thì đặt y_i = x_i - a và trừ phần đó khỏi vế phải. Nghiệm nguyên dương là cận dưới 1.

Ví dụ: x_1 + x_2 + x_3 = 7, mọi x_i >= 1. Có bao nhiêu nghiệm?

1. Đặt y_i = x_i - 1 >= 0: y_1 + y_2 + y_3 = 7 - 3 = 4.
2. Đúng như hình: 4 đá, 2 vách, C_6^2 = 15 nghiệm.

> Lỗi thường gặp: cho hàng n + k chỗ. Hàng có k đá và n - 1 vách: n + k - 1 chỗ.

:::check
Q: Mua 3 viên đan từ 3 loại, được mua trùng loại. Có bao nhiêu cách?
A: 3 đá, 2 vách: hàng 5 chỗ, C_5^2 = 10 cách.
:::


## Nguyên lý bù trừ

:::hook
Khảo sát 100 người: 60 dùng ứng dụng A, 50 dùng B. Không thể có 110 người dùng ít nhất một ứng dụng: ai dùng cả hai bị đếm hai lần.
:::

:::figure sets
caption: Cộng ba tập, trừ ba giao đôi, cộng giao ba. Mỗi vùng ghi số lần nó được đếm: vùng nào cũng còn đúng 1.
size: 230 125
set A "A" xanh
set B "B" do
set C "C" luc
shade A&B&C vang
in A-B-C "1"
in B-A-C "1"
in C-A-B "1"
in (A&B)-C "2-1"
in (A&C)-B "2-1"
in (B&C)-A "2-1"
in A&B&C "3-3+1"
:::

:::core
Cộng thẳng thì phần chung bị đếm nhiều lần; bù trừ trừ các giao đôi rồi cộng lại giao ba, để mỗi phần tử được đếm đúng một lần.
:::

Với hai tập chỉ cần bớt phần chung một lần: |A hợp B| = |A| + |B| - |A giao B|. Hai tập rời nhau thì mới cộng thẳng được.

$$ |A \cup B \cup C| = \sum |A| - \sum |A \cap B| + |A \cap B \cap C| $$

> Lỗi thường gặp: trừ luôn giao ba. Phần tử ở cả ba tập đã bị cộng 3 lần, trừ 3 lần: phải cộng lại 1 lần.

:::check
Q: Lớp 30 đệ tử: 18 học kiếm, 15 học đan, 3 người không học môn nào. Bao nhiêu người học cả hai?
A: 27 người học ít nhất một môn. 27 = 18 + 15 - x, nên x = 6.
:::

### Đếm số không chia hết

Từ 1 đến N có phần nguyên của N/d số chia hết cho d. Chia hết cho cả a và b là chia hết cho BCNN(a, b). Bài "không chia hết cho số nào" thì đếm phần bù: đếm các số chia hết cho ít nhất một số, rồi lấy N trừ đi.

Ví dụ: từ 1 đến 60, bao nhiêu số không chia hết cho 2, 3, 5?

1. Chia hết cho 2, 3, 5: 30, 20, 12. Cho 6, 10, 15: 10, 6, 4. Cho 30: 2.
2. Chia hết cho ít nhất một số: 62 - 20 + 2 = 44.
3. Không chia hết cho số nào: 60 - 44 = 16.

> Lỗi thường gặp: coi "chia hết cho 4 và 6" là chia hết cho 24. Phải là BCNN(4, 6) = 12.

:::check
Q: Từ 1 đến 50, có bao nhiêu số chia hết cho 4 hoặc cho 6?
A: 12 bội của 4, 8 bội của 6, trong đó 4 bội của 12 bị đếm hai lần: 12 + 8 - 4 = 16.
:::

## Hệ thức truy hồi

:::hook
Một hàm đệ quy gọi lại chính nó với đầu vào nhỏ hơn. Hệ thức truy hồi đếm cũng vậy: bài cỡ n dựa vào bài cỡ n - 1, n - 2.
:::

:::figure graph
caption: Xâu không có 11, cắt theo đuôi.
size: 150 70
layout: tree
node R "dài n"
node A "đuôi 0"
node B "đuôi 01"
node A2 "s_(n-1)"
node B2 "s_(n-2)"
edge R A xanh
edge R B do
edge A A2 xanh
edge B B2 do
:::

:::figure grid
caption: s_1 = 2, s_2 = 3, rồi cộng hai số trước.
table
head "n" "1" "2" "3" "4" "5"
row s_n 2 3 5 8 13
mark cell 1 6 vang
:::

:::core
Truy hồi tính số hạng mới từ vài số hạng trước; lập nó bằng cách cắt cấu hình cỡ n theo phần đuôi thành những bài nhỏ hơn cùng loại.
:::

Bỏ đuôi 0 còn một xâu tốt dài n - 1; bỏ đuôi 01 còn một xâu tốt dài n - 2. Vậy s_n = s_(n-1) + s_(n-2). Có hệ thức và số hạng đầu thì cứ tính lần lượt từng số hạng.

Ví dụ: tháp Hà Nội, h_n là số lần chuyển ít nhất với n đĩa.

1. Dời n - 1 đĩa trên sang cọc phụ: h_(n-1) lần. Chuyển đĩa lớn: 1 lần.
2. Dời n - 1 đĩa về trên đĩa lớn: thêm h_(n-1). Vậy h_n = 2h_(n-1) + 1.
3. h_1 = 1, h_2 = 3, h_3 = 7, h_4 = 15.

:::check
Q: Xâu nhị phân không chứa 111 có thể kết thúc bằng những đuôi nào? Viết hệ thức cho số xâu t_n.
A: Đuôi 0, 01 hoặc 011; bỏ đuôi vẫn là xâu tốt. Nên t_n = t_(n-1) + t_(n-2) + t_(n-3).
:::

### Giải bằng phương trình đặc trưng

Hệ thức tuyến tính cấp hai có công thức đóng. Thử a_n = r^n rồi chia cho r^(n-2), ta được phương trình đặc trưng. Hai nghiệm r_1 khác r_2 cho a_n = A r_1^n + B r_2^n, rồi tìm A, B từ hai số hạng đầu.

$$ a_n = c_1 a_{n-1} + c_2 a_{n-2} \quad \to \quad r^2 = c_1 r + c_2 $$

Ví dụ: a_n = 4a_(n-1) - 3a_(n-2), a_0 = 2, a_1 = 4.

1. r^2 - 4r + 3 = 0 có nghiệm 1 và 3: a_n = A + B . 3^n.
2. n = 0: A + B = 2. n = 1: A + 3B = 4. Ra A = B = 1.
3. a_n = 1 + 3^n. Thử lại: a_2 = 16 - 6 = 10 = 1 + 9.

> Lỗi thường gặp: thay số ẩu, như quên (-1)^1 = -1. Luôn thử lại với một số hạng tính thẳng từ hệ thức.

:::check
Q: Phương trình đặc trưng của a_n = a_(n-1) + 6a_(n-2) có những nghiệm nào?
A: r^2 = r + 6, tức (r - 3)(r + 2) = 0: nghiệm 3 và -2. Vậy a_n = A . 3^n + B (-2)^n.
:::
