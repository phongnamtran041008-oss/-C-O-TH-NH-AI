---
id: xs_lib_t3
title_vi: Công thức cộng, nhân, xác suất có điều kiện và Bernoulli
subject: xac_suat_thong_ke
floor: 3
format: 2
summary_vi: Tính xác suất mà không liệt kê cả không gian mẫu: "hoặc" thì cộng rồi trừ phần chung, "biết rằng" thì thu nhỏ thế giới, "và" thì nhân dọc nhánh cây, lặp lại thì dùng Bernoulli.
skills: [xs_t3_cong_thuc_cong, xs_t3_dieu_kien, xs_t3_cong_thuc_nhan, xs_t3_doc_lap, xs_t3_bernoulli]
---
## Công thức cộng xác suất

:::hook
Tông môn có 30 đệ tử: 18 người luyện kiếm, 12 người luyện đan, 5 người luyện cả hai. Có bao nhiêu người luyện ít nhất một môn? Không phải 18 + 12.
:::

:::figure sets
caption: 18 + 12 đếm 5 người vàng hai lần. Trừ một lần: 25 người.
size: 190 95
universe: "30"
set A "kiếm 18" xanh
set B "đan 12" do
shade A&B vang
in A-B "13"
in A&B "5"
in B-A "7"
in ~(A|B) "5"
:::

:::core
Hợp: cộng hai phần, trừ phần chung một lần vì nó bị đếm hai lần. Xung khắc thì không có gì để trừ.
:::

$$ P(A + B) = P(A) + P(B) - P(AB) $$

Biết ba trong P(A), P(B), P(AB), P(A + B) là ra số thứ tư. Ba sự kiện: cộng ba, trừ ba phần chung từng cặp, cộng lại phần chung cả ba.

Ví dụ: chọn ngẫu nhiên một số từ 1 đến 20. P(chia hết cho 2 hoặc 3)?

1. Chia hết cho 2: 10 số; cho 3: 6 số; cho cả hai, tức cho 6: 3 số.
2. P = (10 + 6 - 3)/20 = 13/20.

> Lỗi thường gặp: cộng thẳng P(A) + P(B) khi A, B có phần chung.

:::check
Q: P(A) = 2/3, P(B) = 1/2. A, B xung khắc được không? P(AB) ít nhất là bao nhiêu?
A: Không: xung khắc thì P(A + B) = 7/6 > 1, vô lý. P(AB) = 7/6 - P(A + B) >= 7/6 - 1 = 1/6.
:::

## Xác suất có điều kiện

:::hook
Trong 100 người có 20 người đeo kính. Biết người được chọn đeo kính, câu hỏi "người này là nữ?" chỉ còn xét trong 20 người đó, không phải cả 100.
:::

:::figure sets
caption: Biết B (đeo kính), thế giới thu về hình tròn B: 20 người. Phần đỏ, A trong B, có 12 người: P(A|B) = 12/20.
size: 190 95
universe: "100 người"
set A "A: nữ" xanh
set B "B: kính" do
shade B-A vang
shade A&B do
in A-B "48"
in A&B "12"
in B-A "8"
in ~(A|B) "32"
:::

:::core
Biết B đã xảy ra thì thế giới thu lại chỉ còn B. P(A|B) là phần của A nằm trong B.
:::

$$ P(A \mid B) = \frac{P(AB)}{P(B)}, \quad P(B) > 0 $$

Ví dụ: lớp có nam 10 đạt, 15 trượt; nữ 12 đạt, 3 trượt.

1. P(nữ | đạt): thu về 22 bạn đạt, có 12 nữ: 12/22 = 6/11.
2. P(đạt | nữ): thu về 15 bạn nữ, có 12 đạt: 12/15 = 4/5.
3. Cùng tử số 12, khác mẫu số: hai câu hỏi khác nhau.

> Lỗi thường gặp: lẫn P(A|B) với P(B|A). Sự kiện đứng sau dấu | là điều đã biết, và nó nằm ở mẫu số.

:::check
Q: Gieo hai xúc xắc, biết tổng bằng 6. Xác suất có một mặt 1 là bao nhiêu?
A: Thế giới còn 5 cặp: (1, 5), (2, 4), (3, 3), (4, 2), (5, 1). Có mặt 1: 2 cặp. P = 2/5.
:::

## Công thức nhân xác suất

:::hook
Soát lô 10 linh đan có 3 viên hỏng, lấy lần lượt không trả lại: sau mỗi lần lấy, lô đã khác đi.
:::

:::figure graph
caption: Nhánh sau ghi xác suất khi đã biết nhánh trước. Đường đỏ: 7/10 . 6/9 = 7/15.
size: 200 95
layout: ltr
node S "lô 10"
node T "tốt"
node H "hỏng"
node TT "tốt"
node TH "hỏng"
node HT "tốt"
node HH "hỏng"
edge S T "7/10" do
edge S H "3/10"
edge T TT "6/9" do
edge T TH "3/9"
edge H HT "7/9"
edge H HH "2/9"
:::

:::core
P(A và B) bằng P(A) nhân P(B khi đã biết A): đi dọc một nhánh cây và nhân các số trên đường.
:::

$$ P(AB) = P(A)\,P(B \mid A) $$

Ví dụ: hộp 5 đỏ, 3 xanh, lấy lần lượt 3 bi không hoàn lại. P(đỏ, xanh, đỏ)?

1. Lần 1 đỏ: 5/8.
2. Còn 7 bi, 3 xanh: 3/7. Còn 6 bi, 4 đỏ: 4/6.
3. Nhân: 5/8 . 3/7 . 4/6 = 60/336 = 5/28.

> Lỗi thường gặp: không hoàn lại mà vẫn nhân 5/8 . 3/8 . 5/8. Mỗi bước hộp đã vơi một bi.

:::check
Q: 5 chìa, 1 chìa đúng, thử lần lượt, bỏ chìa sai ra. P(mở được ở lần thứ hai)?
A: Lần 1 sai 4/5, rồi còn 4 chìa: đúng 1/4. P = 4/5 . 1/4 = 1/5.
:::

## Sự kiện độc lập

:::hook
Hai camera an ninh chạy riêng rẽ: camera này hỏng không làm camera kia dễ hỏng hơn. Vì vậy xác suất cả hai cùng hỏng chỉ là tích.
:::

:::figure grid
caption: A, B độc lập: mỗi ô là tích của số ở đầu hàng và đầu cột, ví dụ 1/2 . 2/5 = 1/5.
table
head "B: 2/5" "không B: 3/5"
side "A: 1/2" "không A: 1/2"
row "1/5" "3/10"
row "1/5" "3/10"
mark cell 1 1 vang
:::

:::core
Độc lập là biết A không làm đổi khả năng của B, nên P(AB) = P(A) P(B). Xung khắc thì ngược hẳn: biết A là biết chắc B không xảy ra.
:::

$$ P(AB) = P(A)\,P(B) $$

A, B độc lập thì A với đối của B, Ā với B, Ā với đối của B cũng độc lập.

Ví dụ: hai linh kiện độc lập, tốt với xác suất 4/5 và 3/4.

1. Nối tiếp, cần cả hai tốt: 4/5 . 3/4 = 3/5.
2. Song song, cần ít nhất một tốt: đối là cả hai hỏng, 1/5 . 1/4 = 1/20.
3. P(song song thông) = 1 - 1/20 = 19/20.

> Lỗi thường gặp: tưởng không có kết quả chung là độc lập. Đó là xung khắc; hai sự kiện xung khắc có xác suất dương thì không bao giờ độc lập.

:::check
Q: Gieo xúc xắc. A: số chấm nhỏ hơn 3, B: số chấm chẵn. A và B có độc lập không?
A: Có. P(A) = 1/3, P(B) = 1/2, AB = {2} nên P(AB) = 1/6 = 1/3 . 1/2. Phải tính, không đoán.
:::

## Công thức Bernoulli

:::hook
Mỗi thư mời gửi đi được mở với xác suất 1/10, các thư độc lập. Gửi 5 thư, khả năng có đúng 2 thư được mở là bao nhiêu?
:::

:::figure bars
caption: n = 4, p = 1/4. P(đúng k lần), k = 0..4, là 81, 108, 54, 12, 1 phần 256: cộng lại đủ 1.
size: 200 95
values: off
bar "0" 81
bar "1" 108 do
bar "2" 54
bar "3" 12
bar "4" 1
:::

:::core
Mỗi dãy có k lần thành công có xác suất p^k (1 - p)^(n - k), và có C(n, k) dãy như thế.
:::

$$ P_n(k) = C_n^k \, p^k (1-p)^{n-k} $$

Điều kiện: các lần độc lập, cùng một p (p tùy ý). Ít nhất 1 lần: 1 - (1 - p)^n.

Ví dụ: 5 thư, p = 1/10, tính P(đúng 2 thư được mở).

1. Một dãy cụ thể, như "mở, mở, không, không, không": (1/10)^2 (9/10)^3.
2. Số cách chọn 2 vị trí trong 5: C(5, 2) = 10.
3. P = 10 . 729/100000 = 729/10000.

> Lỗi thường gặp: quên C(n, k), chỉ tính một dãy cụ thể.

:::check
Q: Nhìn hình (n = 4, p = 1/4): k nào có xác suất lớn nhất? Tính P(ít nhất 1 lần thành công).
A: k = 1, với 108/256 = 27/64. P(ít nhất 1) = 1 - (3/4)^4 = 1 - 81/256 = 175/256.
:::
