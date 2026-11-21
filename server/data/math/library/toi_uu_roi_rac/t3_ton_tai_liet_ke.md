---
id: tr_lib_t3
title_vi: Bài toán tồn tại và bài toán liệt kê
subject: toi_uu_roi_rac
floor: 3
format: 2
summary_vi: Chứng minh một điều chắc chắn xảy ra mà không cần đếm hết (Dirichlet, bất biến), rồi đi qua mọi cấu hình theo thứ tự từ điển không sót cái nào: so sánh, sinh cấu hình liền sau, tính thứ hạng, và quay lui có cắt nhánh.
skills: [tr_t3_dirichlet, tr_t3_bat_bien, tr_t3_tu_dien, tr_t3_sinh_ke_tiep, tr_t3_thu_hang, tr_t3_quay_lui]
---
## Nguyên lý Dirichlet

:::hook
Bảng băm có 1000 ô mà phải cất 1001 khóa: chắc chắn có hai khóa chung một ô, dù hàm băm tốt đến đâu.
:::

:::figure grid
caption: 6 vật vẫn chia đều mỗi hộp 2. Vật thứ 7 rơi vào đâu cũng làm một hộp có 3: cần k(m - 1) + 1 = 7.
table "6 vật"
head "hộp 1" "hộp 2" "hộp 3"
row "o o" "o o" "o o"
op "+1"
table "7 vật"
head "hộp 1" "hộp 2" "hộp 3"
row "o o o" "o o" "o o"
mark cell 1 1 do
:::

:::core
Nhiều vật hơn hộp thì có hộp chứa chung: N vật vào k hộp thì chắc chắn có một hộp chứa ít nhất trần(N/k) vật.
:::

Trần(N/k) là số nguyên nhỏ nhất không nhỏ hơn N/k: trần(17/5) = 4. Muốn chắc chắn có m vật cùng hộp, cần một vật nhiều hơn cách chia đều mỗi hộp m - 1 vật:

$$ k(m-1) + 1 $$

Ví dụ: túi linh thạch 3 màu. Lấy bao nhiêu viên để chắc có 3 viên cùng màu?

1. Màu là hộp: k = 3, cần m = 3.
2. 6 viên vẫn có thể là 2, 2, 2. Viên thứ 7 bắt buộc tạo bộ ba: 3 . 2 + 1 = 7.

:::check
Q: Cất 17 cuộn bí kíp vào 5 rương. Chắc chắn có một rương chứa ít nhất mấy cuộn? Sao không nói được 5?
A: trần(17/5) = 4. Chia 4, 4, 3, 3, 3 thì không rương nào có 5 cuộn.
:::

### Chọn hộp cho khéo

Phần khó là chọn hộp. Hộp hay gặp: số dư khi chia cho d, cặp số có tổng hoặc hiệu cố định, các giá trị có thể của một đại lượng.

Ví dụ: chọn ít nhất bao nhiêu số khác nhau trong {1, ..., 10} để chắc có hai số có tổng 11?

1. Hộp là các cặp tổng 11: {1, 10}, {2, 9}, {3, 8}, {4, 7}, {5, 6}. Có 5 hộp.
2. Chọn 6 số thì hai số rơi cùng một cặp. Chọn 5 số 1, 2, 3, 4, 5 thì chưa có.
3. Vậy cần 6 số.

> Lỗi thường gặp: kết luận về một hộp cụ thể. Nguyên lý chỉ nói có MỘT hộp đầy, không nói hộp nào.

:::check
Q: Trong 5 số nguyên bất kỳ, luôn có hai số có hiệu chia hết cho 4. Hộp là gì?
A: Số dư khi chia cho 4: chỉ có 4 hộp 0, 1, 2, 3. 5 số nên hai số cùng số dư, hiệu của chúng chia hết cho 4.
:::

## Chẵn lẻ và bất biến

:::hook
Một trò xếp hình chơi mãi không ra đích. Thay vì thử tiếp, hãy tìm một con số mà mọi nước đi đều giữ nguyên.
:::

:::figure grid
caption: Lật đúng 2 cốc: số cốc úp d đổi -2, +2 hoặc 0. Tính chẵn lẻ của d không bao giờ đổi.
table
head "lật" "d đổi"
row "úp, úp" "-2"
row "ngửa, ngửa" "+2"
row "úp, ngửa" "0"
mark col 2 vang
:::

:::core
Bất biến là đại lượng mà mọi nước đi đều giữ nguyên; lúc đầu và đích khác giá trị bất biến thì đích không bao giờ tới được.
:::

1. Chọn đại lượng: tổng, tính chẵn lẻ, số ô mỗi màu, hiệu hai tổng xen kẽ.
2. Kiểm MỌI kiểu nước đi đều giữ nó.
3. So giá trị lúc đầu với giá trị mà đích phải có.

Ví dụ: bảng có 1, 2, 3, 4, 5. Mỗi lượt xóa a, b và viết |a - b|. Số cuối chẵn hay lẻ?

1. Tổng mới = tổng cũ - 2 . min(a, b): tính chẵn lẻ của tổng không đổi.
2. Tổng đầu là 15, lẻ. Số cuối là tổng cuối, nên luôn lẻ.

> Lỗi thường gặp: chỉ kiểm vài kiểu nước đi. Quên kiểu "úp, ngửa" là tưởng d giảm 1.

:::check
Q: Bàn 3 x 3 bỏ một ô ở giữa cạnh. Lát kín bằng 4 quân domino được không?
A: Tô xen kẽ: 4 góc và ô tâm cùng màu (5 ô), 4 ô giữa cạnh màu kia. Bỏ một ô giữa cạnh còn 5 và 3, mà mỗi domino phủ 1 ô mỗi màu: không được.
:::

## Thứ tự từ điển

:::hook
Từ điển, danh bạ, tên tệp: so chữ đầu, bằng nhau mới so chữ kế tiếp.
:::

:::figure grid
caption: Vị trí 1 bằng nhau. Ở vị trí 2, 1 < 2 nên dãy trên đứng trước.
table
head "1" "2" "3" "4"
row 3 1 4 2
row 3 2 1 4
mark col 1 xanh
mark col 2 do
:::

:::core
So từ trái sang phải và dừng ở vị trí khác nhau đầu tiên: dãy có phần tử nhỏ hơn ở đó đứng trước.
:::

- Xâu nhị phân dài n xếp đúng như các số 0, 1, ..., 2^n - 1.
- Hoán vị của {1, ..., n}: đầu là (1, 2, ..., n), cuối là (n, ..., 2, 1).
- Tập k phần tử viết tăng dần: đầu {1, ..., k}, cuối {n - k + 1, ..., n}.

Ví dụ: xếp 2101, 2011, 1220, 2100.

1. Chữ đầu: 1220 đứng trước ba xâu bắt đầu bằng 2.
2. Chữ thứ hai: 2011 trước 2101 và 2100. Chữ thứ tư: 2100 trước 2101.
3. Thứ tự: 1220, 2011, 2100, 2101.

> Lỗi thường gặp: so theo tổng hay theo số lớn nhất. 1012 và 1021 cùng chữ số, nhưng 1012 đứng trước.

:::check
Q: Các tập 3 phần tử của {1, ..., 7}, viết tăng dần, xếp theo từ điển. Tập đầu và tập cuối là gì?
A: Đầu {1, 2, 3}, cuối {5, 6, 7}: mỗi vị trí đạt giá trị lớn nhất được phép.
:::

## Phương pháp sinh

:::hook
Muốn thử mọi cấu hình mà không lưu cả danh sách, chỉ cần biết từ cấu hình này đi tới cấu hình liền sau như thế nào.
:::

:::figure grid
caption: Như cộng 1: chữ 0 cuối cùng thành 1, mọi chữ 1 bên phải nó về 0.
table "trước"
row 1 0 0 1 1
mark cell 1 3 do
op "->"
table "sau"
row 1 0 1 0 0
mark cell 1 3 do
:::

:::core
Sinh đi từ cấu hình đầu tới cấu hình cuối; mỗi bước tăng vị trí phải nhất còn tăng được, rồi đưa mọi vị trí sau nó về nhỏ nhất.
:::

Xâu nhị phân: từ phải sang trái tìm chữ 0 đầu tiên. Xâu toàn số 1 là cấu hình cuối. Tập k phần tử của {1, ..., n}: vị trí i lớn nhất là n - k + i. Tìm từ phải phần tử chưa đạt giá trị lớn nhất, tăng nó 1, các phần tử sau lấy số liền tiếp.

Ví dụ: tập 3 phần tử của {1, ..., 6}. Tập liền sau {2, 5, 6}?

1. Giá trị lớn nhất của ba vị trí: 4, 5, 6. Số 6 và 5 đã đạt.
2. Tăng 2 lên 3, hai vị trí sau lấy 4, 5: được {3, 4, 5}.

:::check
Q: Tập 2 phần tử của {1, ..., 6}. Tập liền sau {3, 6} là gì?
A: 6 đã lớn nhất ở vị trí 2. Tăng 3 lên 4, vị trí sau lấy 5: {4, 5}.
:::

### Hoán vị liền sau

:::figure flow
caption: Đuôi (5, 4, 3, 1) đã giảm dần, tức lớn nhất. Tăng số đứng trước nó ít nhất có thể, rồi đưa đuôi về nhỏ nhất.
box "2 5 4 3 1"
link "đổi 2 với 3"
box "3 5 4 2 1" xanh
link "đảo đuôi"
box "3 1 2 4 5" luc
:::

1. Từ phải sang trái tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: số 2.
2. Trong đuôi bên phải, số nhỏ nhất còn lớn hơn 2 là 3: đổi chỗ.
3. Đuôi (5, 4, 2, 1) vẫn giảm dần: đảo ngược thành tăng dần.

> Lỗi thường gặp: quên đảo đuôi. Giữ (3, 5, 4, 2, 1) là nhảy qua mọi hoán vị bắt đầu bằng 3 ở giữa.

:::check
Q: Hoán vị liền sau (1, 4, 3, 2) là gì?
A: Số 1 nhỏ hơn số sau nó. Đổi 1 với 2 được (2, 4, 3, 1), đảo đuôi được (2, 1, 3, 4).
:::

## Thứ hạng của cấu hình

:::hook
Đánh số mọi cấu hình rồi lưu một con số thay cho cả cấu hình: muốn vậy phải tính được nó đứng thứ mấy mà không liệt kê hết.
:::

:::figure grid
caption: (2, 4, 1, 3): có 6 + 4 = 10 hoán vị đứng trước, nên nó đứng thứ 11.
table
head "1" "2" "3" "4"
side "số" "nhỏ hơn, chưa dùng" "nhân" "góp"
row 2 4 1 3
row 1 2 0 0
row 3! 2! 1! 0!
row 6 4 0 0
mark row 4 vang
:::

:::core
Thứ hạng là 1 cộng số cấu hình đứng trước; đếm chúng theo từng vị trí, không cần liệt kê.
:::

Ở vị trí i, đặt một số nhỏ hơn chưa dùng thì mọi cách xếp (n - i)! phần còn lại đều đứng trước. Xâu nhị phân thì dễ hơn: xâu là số m thì đứng thứ m + 1, như 0110 = 6 đứng thứ 7.

$$ \text{hang} = 1 + \sum_{i=1}^{n} c_i \, (n-i)! $$

> Lỗi thường gặp: lệch một. Có m cấu hình đứng trước thì nó đứng thứ m + 1, không phải thứ m.

:::check
Q: Trong các hoán vị của {1, 2, 3, 4}, (4, 1, 2, 3) đứng thứ mấy?
A: Vị trí 1 có 3 số nhỏ hơn 4: 3 . 3! = 18; các vị trí sau góp 0. Đứng thứ 19.
:::

### Thứ hạng của tập con

Với tập viết tăng dần, cũng đếm các tập đứng trước: giữ nguyên các phần tử đầu, đặt một số nhỏ hơn ở một vị trí, rồi đếm cách chọn các phần tử sau lớn hơn nó.

Ví dụ: tập 2 phần tử của {1, ..., 5}. {2, 4} đứng thứ mấy?

1. Bắt đầu bằng 1: {1, 2}, {1, 3}, {1, 4}, {1, 5}, là 4 tập.
2. Bắt đầu bằng 2 mà phần tử sau nhỏ hơn 4: chỉ {2, 3}.
3. 5 tập đứng trước: {2, 4} đứng thứ 6.

:::check
Q: Cùng danh sách đó, tập đứng thứ 8 là tập nào?
A: Bắt đầu bằng 1: thứ 1 đến 4; bằng 2: {2, 3}, {2, 4}, {2, 5} là thứ 5 đến 7. Thứ 8 là {3, 4}.
:::

## Thuật toán quay lui

:::hook
Giải sudoku bằng máy: điền thử một ô, đi tiếp; gặp ngõ cụt thì xóa ô vừa điền và thử số khác.
:::

:::figure graph
caption: Tìm tập con của {1, 2, 3, 4} có tổng 5, chọn số tăng dần. Nút đỏ có tổng vượt 5 nên bị cắt; hai nút xanh {1, 4}, {2, 3} là lời giải.
size: 300 120
layout: tree
node R "bắt đầu"
node A "1"
node B "2"
node C "3"
node D "4"
node AB "1,2"
node AC "1,3"
node AD "1,4" luc
node BC "2,3" luc
node BD "2,4" do
node CD "3,4" do
node ABC "1,2,3" do
node ACD "1,3,4" do
edge R A
edge R B
edge R C
edge R D
edge A AB
edge A AC
edge A AD luc
edge B BC luc
edge B BD do dash
edge C CD do dash
edge AB ABC do dash
edge AC ACD do dash
:::

:::core
Quay lui dựng lời giải từng bước, thử mọi lựa chọn còn hợp lệ, hết lựa chọn thì lùi về bước trước; nhánh đã hỏng thì cắt bỏ cả nhánh.
:::

:::check
Q: Nhìn hình: vì sao nút "1,2" vẫn đi tiếp còn "2,4" bị cắt ngay?
A: Tổng 1 + 2 = 3 còn nhỏ hơn 5, có thể thêm số. 2 + 4 = 6 đã vượt 5, thêm số nào cũng chỉ lớn hơn.
:::

### Thủ tục Try(i) và đếm lời giải

1. Try(i): với mỗi giá trị v còn hợp lệ, gán x_i = v.
2. Nếu đã đủ cấu hình thì in ra, chưa đủ thì gọi Try(i + 1).
3. Thử hết giá trị thì Try(i) trả về: đó là bước quay lui.

Không ràng buộc thì không cắt gì: xâu nhị phân dài n cho đủ 2^n lá. Liệt kê hoán vị thì chỉ thử những số chưa dùng. Muốn biết quay lui in ra bao nhiêu cấu hình, chia theo lựa chọn ở bước đầu rồi cộng lại.

Ví dụ: bộ (x_1, x_2, x_3), mỗi x_i từ 0 đến 2, tổng bằng 4. Có bao nhiêu bộ?

1. x_1 = 0: x_2 + x_3 = 4, chỉ (2, 2): 1 bộ.
2. x_1 = 1: tổng 3, có (1, 2), (2, 1): 2 bộ. x_1 = 2: tổng 2, có (0, 2), (1, 1), (2, 0): 3 bộ.
3. Cộng lại: 1 + 2 + 3 = 6 bộ.

> Lỗi thường gặp: dùng lại một giá trị bài không cho phép, như ghép {3, 3} thành tập có tổng 6.

:::check
Q: Quay lui liệt kê các tập con của {1, ..., 5} có tổng 7. Nó in ra mấy tập?
A: 3 tập: {1, 2, 4}, {2, 5}, {3, 4}.
:::
