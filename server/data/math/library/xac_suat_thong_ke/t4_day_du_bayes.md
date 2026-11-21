---
id: xs_lib_t4
title_vi: Công thức xác suất đầy đủ và công thức Bayes
subject: xac_suat_thong_ke
floor: 4
format: 2
summary_vi: Cắt phép thử theo các trường hợp của bước đầu: đi xuôi cây và cộng các nhánh để có xác suất của kết quả (đầy đủ), đi ngược cây để biết kết quả đó nhiều khả năng đến từ đâu (Bayes).
skills: [xs_t4_he_day_du, xs_t4_so_do_cay, xs_t4_day_du, xs_t4_bayes, xs_t4_bayes_ung_dung]
---
## Hệ đầy đủ các sự kiện

:::hook
Mỗi yêu cầu gửi tới hệ thống được đúng một trong ba mô hình xử lý. Chữ "đúng một" cho phép cộng các trường hợp mà không đếm sót, không đếm trùng.
:::

:::figure grid
caption: Gieo xúc xắc, chia mặt thành H_1 = {1}, H_2 = {2, 3}, H_3 = {4, 5, 6}: mỗi mặt thuộc đúng một mảnh.
table "mặt"
head "1" "2" "3" "4" "5" "6"
row "H_1" "H_2" "H_2" "H_3" "H_3" "H_3"
mark cell 1 1 do
mark cell 1 2 xanh
mark cell 1 3 xanh
mark cell 1 4 luc
mark cell 1 5 luc
mark cell 1 6 luc
:::

:::core
Hệ đầy đủ là cách cắt Omega thành các mảnh: không mảnh nào chồng nhau, không kết quả nào bị sót.
:::

$$ P(H_1) + P(H_2) + \cdots + P(H_n) = 1 $$

- {1, 2}, {2, 3, 4}, {5, 6}: chồng nhau ở mặt 2, không được.
- {1, 2}, {3, 4}: sót mặt 5, 6, không được.
- A và Ā: hệ đầy đủ đơn giản nhất.

Ví dụ: H_1, H_2, H_3 là hệ đầy đủ, P(H_1) = 3 P(H_3), P(H_2) = 2 P(H_3).

1. Đặt P(H_3) = t, thì P(H_2) = 2t, P(H_1) = 3t; cộng lại: 6t = 1.
2. t = 1/6, nên P(H_1) = 3/6 = 1/2.

> Lỗi thường gặp: chỉ xét "phủ hết". Nhóm học Anh và nhóm học Pháp chồng nhau ở người học cả hai.

:::check
Q: Rút một lá bài. {lá đỏ, lá bích, lá nhép} có phải hệ đầy đủ không?
A: Có: lá đỏ là cơ hoặc rô, nên mỗi lá thuộc đúng một trong ba nhóm.
:::

## Sơ đồ cây cho phép thử nhiều giai đoạn

:::hook
Đệ tử chọn lối vào hang, rồi mới gặp hay không gặp yêu thú. Cây xác suất vẽ đúng thứ tự đó.
:::

:::figure graph
caption: Mỗi lá ghi tích dọc đường đi tới nó; bốn lá cộng lại bằng 1.
size: 210 85
layout: ltr
node S "hang"
node L "trái"
node R "phải"
node LG "gặp: 1/6"
node LK "không: 1/12"
node RG "gặp: 3/20"
node RK "không: 3/5"
edge S L "1/4" do
edge S R "3/4"
edge L LG "2/3" do
edge L LK "1/3"
edge R RG "1/5"
edge R RK "4/5"
:::

:::core
Mỗi nhánh sau là một xác suất có điều kiện; một đường đi có xác suất bằng tích các nhánh dọc đường.
:::

$$ P(H_i A) = P(H_i)\,P(A \mid H_i) $$

Ví dụ: hộp 3 đỏ, 2 xanh, lấy không hoàn lại đến khi được đỏ. P(lấy đúng 3 lần)?

1. Đường đi: xanh, xanh, đỏ.
2. Các nhánh: 2/5, rồi 1/4 (còn 4 bi, 1 xanh), rồi 3/3 = 1.
3. Nhân dọc: 2/5 . 1/4 . 1 = 1/10.

> Lỗi thường gặp: ghi trên nhánh tầng sau xác suất lúc chưa lấy gì. Sau một bi xanh, hộp chỉ còn 4 bi.

:::check
Q: Lá "phải, không gặp" có xác suất bao nhiêu? Bốn lá cộng lại bằng mấy?
A: 3/4 . 4/5 = 3/5. Bốn lá: 1/6 + 1/12 + 3/20 + 3/5 = 1, vì chúng phủ mọi khả năng.
:::

## Công thức xác suất đầy đủ

:::hook
Ba mô hình xử lý 1/2, 3/10, 1/5 số yêu cầu, mỗi mô hình trả lời sai một tỉ lệ khác nhau. Tỉ lệ sai của cả hệ thống không phải trung bình cộng.
:::

:::figure graph
caption: Theo 1000 yêu cầu: các nhánh góp 50 + 15 + 8 = 73 câu sai. P(sai) = 73/1000.
size: 210 85
layout: ltr
node S "1000"
node A "A: 500"
node B "B: 300"
node C "C: 200"
node AS "sai 50"
node BS "sai 15"
node CS "sai 8"
edge S A "1/2"
edge S B "3/10"
edge S C "1/5"
edge A AS "1/10" do
edge B BS "1/20" do
edge C CS "1/25" do
:::

:::core
A xảy ra qua đúng một nhánh của hệ đầy đủ: tính từng đường đi "H_i rồi A", rồi cộng tất cả.
:::

$$ P(A) = \sum_{i=1}^{n} P(H_i)\,P(A \mid H_i) $$

Ví dụ: hộp I: 2 trắng, 1 đen; hộp II: 1 trắng, 2 đen. Chuyển 1 bi từ I sang II, rồi lấy 1 bi từ II. P(trắng)?

1. Hệ đầy đủ là màu bi được chuyển: trắng 2/3, đen 1/3.
2. Hộp II còn 4 bi: có 2 trắng nếu chuyển trắng, 1 trắng nếu chuyển đen.
3. P = 2/3 . 2/4 + 1/3 . 1/4 = 4/12 + 1/12 = 5/12.

Dùng ngược: hai xưởng chia đôi sản lượng, xưởng I hỏng 1/10, cả nhà máy 3/40. Tỉ lệ x của xưởng II: 1/2 . 1/10 + 1/2 . x = 3/40, x = 1/20.

> Lỗi thường gặp: lấy trung bình cộng ba tỉ lệ sai, ra 19/300. Mô hình làm nhiều phải nặng ký hơn.

:::check
Q: Chọn hộp I với xác suất 1/4 (bi đỏ chiếm 1/2), hộp II với xác suất 3/4 (bi đỏ chiếm 1/3). P(lấy được bi đỏ)?
A: 1/4 . 1/2 + 3/4 . 1/3 = 1/8 + 1/4 = 3/8.
:::

## Công thức Bayes

:::hook
Kho có một viên đan hỏng. Lò nào đã luyện ra nó? Bayes đi ngược cây: từ kết quả đã thấy, quay về nguyên nhân.
:::

:::figure graph
caption: Chỉ còn 65 viên hỏng, lò II góp 30: P(lò II | hỏng) = 6/13.
size: 210 85
layout: ltr
node S "1000 viên"
node A "lò I: 700"
node B "lò II: 300"
node AH "hỏng 35"
node AT "tốt 665"
node BH "hỏng 30"
node BT "tốt 270"
edge S A "7/10"
edge S B "3/10"
edge A AH "1/20" do
edge A AT "19/20"
edge B BH "1/10" do
edge B BT "9/10"
:::

:::core
Biết A đã xảy ra, mỗi giả thuyết H_k nhận phần của nhánh nó trong tổng P(A).
:::

$$ P(H_k \mid A) = \frac{P(H_k)\,P(A \mid H_k)}{P(A)} $$

P(H_k): tiên nghiệm, trước khi thấy A. P(H_k | A): hậu nghiệm, sau khi thấy A.

Ví dụ: tính lại số trong hình bằng phân số.

1. P(hỏng) = 7/10 . 1/20 + 3/10 . 1/10 = 7/200 + 6/200 = 13/200.
2. P(lò II | hỏng) = (6/200)/(13/200) = 6/13.
3. Thử lại: P(lò I | hỏng) = 7/13, cộng lại đủ 1.

> Lỗi thường gặp: lẫn P(lò II | hỏng) với P(hỏng | lò II).

:::check
Q: Hộp I: 2 đỏ, 2 xanh; hộp II: 1 đỏ, 3 xanh. Chọn bừa hộp, lấy được đỏ. P(hộp I | đỏ)?
A: P(đỏ) = 1/2 . 1/2 + 1/2 . 1/4 = 3/8. P(hộp I | đỏ) = (1/4)/(3/8) = 2/3.
:::

## Bayes trong xét nghiệm và phân loại

:::hook
Xét nghiệm bắt được 90% người bệnh vừa báo bạn dương tính. Khả năng bạn mắc bệnh thật? Thấp bất ngờ, khi bệnh hiếm.
:::

:::figure graph
caption: Theo 1000 người: 67 người dương tính, chỉ 18 người bệnh thật. P(bệnh | dương) = 18/67.
size: 210 85
layout: ltr
node S "1000"
node B "bệnh 20"
node K "khỏe 980"
node BD "dương 18"
node BA "âm 2"
node KD "dương 49"
node KA "âm 931"
edge S B "1/50"
edge S K "49/50"
edge B BD "9/10" do
edge B BA "1/10"
edge K KD "1/20" do
edge K KA "19/20"
:::

:::core
Dương tính gồm cả người bệnh lẫn người khỏe bị báo nhầm. Bệnh càng hiếm, phần báo nhầm càng lấn át.
:::

$$ P(B \mid D) = \frac{p\,s}{p\,s + (1-p)\,f} $$

p: tỉ lệ bệnh, s = P(dương | bệnh), f = P(dương | khỏe). Hai lần xét nghiệm độc lập cùng dương: thay s bằng s^2, f bằng f^2 (số trong hình ra 324/373).

Ví dụ: 1/3 số thư là rác; chữ "miễn phí" có trong 3/5 thư rác, 1/10 thư thường. P(rác | có chữ)?

1. Rác và có chữ: 1/3 . 3/5 = 1/5. Thường và có chữ: 2/3 . 1/10 = 1/15.
2. P(rác | có chữ) = (1/5)/(1/5 + 1/15) = (1/5)/(4/15) = 3/4.

> Lỗi thường gặp: quên tỉ lệ nền, tưởng dương tính là 90% bệnh.

:::check
Q: Cùng xét nghiệm (s = 9/10, f = 1/20), ở vùng có tỉ lệ bệnh 1/5. P(bệnh | dương)?
A: ps = 9/50, (1 - p)f = 4/5 . 1/20 = 2/50. P = 9/(9 + 2) = 9/11: tỉ lệ nền cao hơn, kết quả đáng tin hơn.
:::
