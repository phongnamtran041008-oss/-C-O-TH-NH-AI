---
id: dstt_lib_t5
title_vi: Hệ phương trình tuyến tính và khử Gauss
subject: dai_so_tuyen_tinh
floor: 5
format: 2
summary_vi: Cất cả hệ vào một bảng số Ax = b, dùng ba phép an toàn trên hàng để khử dần thành bậc thang, leo ngược lên lấy nghiệm, và nhìn bậc thang mà biết hệ có 0, 1 hay vô số nghiệm.
skills: [dstt_t5_dang_ma_tran, dstt_t5_bien_doi_hang, dstt_t5_bac_thang, dstt_t5_the_nguoc, dstt_t5_so_nghiem, dstt_t5_he_thuan_nhat]
---
## Viết hệ dưới dạng Ax = b

:::hook
Hồi quy tuyến tính dẫn tới hàng nghìn phương trình. Máy cất cả hệ vào một bảng số A và một cột b, rồi giải Ax = b.
:::

:::figure grid
caption: Mỗi phương trình một hàng, mỗi ẩn một cột; ẩn vắng mặt ghi 0 (đỏ). Cột vàng là vế phải b.
table "(A | b)"
head "x" "y" "z" "b"
side "pt 1" "pt 2" "pt 3"
row 1 3 0 4
row 2 -1 1 3
row 0 -1 5 9
mark col 4 vang
mark cell 1 3 do
mark cell 3 1 do
:::

:::core
Ax = b là cả hệ gói lại: hàng i của A nhân vô hướng với vectơ ẩn x phải ra đúng b_i.
:::

Hình là hệ x + 3y = 4, 2x - y + z = 3, -y + 5z = 9. Hệ m phương trình, n ẩn cho A cỡ m x n, x có n tọa độ, b có m tọa độ. Ghép b vào làm cột cuối được ma trận bổ sung (A | b).

Ví dụ: (x, y, z) = (1, 1, 2) có là nghiệm của hệ ở hình không?

1. Hàng 1: 1 . 1 + 3 . 1 + 0 . 2 = 4. Khớp.
2. Hàng 2: 2 - 1 + 2 = 3. Khớp.
3. Hàng 3: 0 - 1 + 10 = 9. Khớp, nên đúng là nghiệm.

> Lỗi thường gặp: bỏ quên số 0 của ẩn vắng mặt, làm các cột lệch nhau. Viết mọi phương trình theo cùng thứ tự x, y, z trước khi lập bảng.

:::check
Q: Hệ có 4 phương trình, 6 ẩn. A, x và b có cỡ bao nhiêu?
A: A cỡ 4 x 6 (hàng là phương trình), x có 6 tọa độ (mỗi ẩn một), b có 4 tọa độ.
:::

### Hiệu hai nghiệm

:::figure plane
caption: u, v cùng nằm trên đường x + y = 2 (Ax = b). Hiệu u - v = (2, -2) nằm trên đường x + y = 0 qua gốc (Ax = 0).
size: 170 100
x: -2.5 3 1
y: -2.5 3 1
line 0 2 2 0 xanh
line 0 0 1 -1 do dash
point 2 0 muc "u" pos=ne
point 0 2 muc "v" pos=e
vector 0 0 2 -2 do "u - v" pos=e
:::

Hai nghiệm u, v của cùng một hệ thì hiệu của chúng giải hệ vế phải 0. Còn tổng thì cho A(u + v) = 2b, nên không còn là nghiệm khi b khác 0.

$$ A(u - v) = Au - Av = b - b = 0 $$

:::check
Q: u và v là hai nghiệm của Ax = b với b = (3, 1). Tính A(u - v) và A(u + v).
A: A(u - v) = b - b = (0, 0). A(u + v) = 2b = (6, 2).
:::

## Ba phép biến đổi sơ cấp trên hàng

:::hook
Đổi chỗ hai phương trình, nhân một phương trình với 2, cộng phương trình này vào phương trình kia: nghiệm vẫn y nguyên. Khử Gauss chỉ dùng ba thao tác ấy.
:::

:::figure grid
caption: Chỉ hàng 2 bị thay, hàng 1 giữ nguyên. Cột vế phải cũng bị trừ: 9 - 3 . 4 = -3.
style: matrix
table "trước"
head "x" "y" "b"
row 1 2 4
row 3 5 9
mark row 2 xanh
op "R2 <- R2 - 3R1"
table "sau"
head "x" "y" "b"
row 1 2 4
row 0 -1 -3
mark row 2 xanh
:::

:::core
Đổi chỗ hai hàng, nhân một hàng với số khác 0, cộng bội của hàng này vào hàng khác: cả ba đều làm ngược lại được, nên tập nghiệm không đổi.
:::

Ký hiệu: R_i <-> R_j, R_i <- kR_i, R_i <- R_i + kR_j. Không bao giờ nhân hàng với 0: mất một phương trình, không lấy lại được. Mỗi lần chỉ thay một hàng.

Ví dụ: giải hệ có hàng (0, 3 | 6) và (2, 1 | 5).

1. Hàng 1 bắt đầu bằng 0, không làm trụ được: R1 <-> R2.
2. Được (2, 1 | 5) và (0, 3 | 6): 3y = 6, y = 2. Rồi 2x + 2 = 5, x = 3/2.

> Lỗi thường gặp: quên trừ ở cột vế phải, hoặc sai dấu ở đó. Phép biến đổi làm trên cả hàng, kể cả số sau dấu |.

:::check
Q: Hàng 1 là (2, -1 | 3), hàng 3 là (1, 4 | 0). Làm R1 <- R1 - 2R3. Hàng 1 mới là gì? Hàng 3 có đổi không?
A: (2 - 2, -1 - 8 | 3 - 0) = (0, -9 | 3). Hàng 3 giữ nguyên.
:::

## Khử Gauss về dạng bậc thang

:::hook
Một hệ ba ẩn rối mắt trở nên dễ khi về dạng bậc thang: phương trình cuối chỉ còn một ẩn, giải ngay được, rồi leo dần lên.
:::

:::figure grid
caption: Trụ hàng 1 làm 0 cột x (xanh), rồi trụ hàng 2 làm 0 cột y. Trụ (vàng) lùi dần sang phải.
style: matrix
table "M"
row 1 2 1 1
row 2 5 3 2
row 1 0 3 5
mark cell 1 1 vang
op "->"
table
row 1 2 1 1
row 0 1 1 0
row 0 -2 2 4
mark cell 2 1 xanh
mark cell 3 1 xanh
mark cell 2 2 vang
op "->"
table
row 1 2 1 1
row 0 1 1 0
row 0 0 4 4
mark cell 3 2 xanh
mark cell 3 3 vang
:::

:::core
Bậc thang: trụ (số khác 0 đầu tiên) của mỗi hàng nằm bên phải trụ hàng trên; khử Gauss làm 0 từng cột dưới trụ, từ trái sang phải.
:::

Cột cuối là vế phải; hàng toàn 0 xếp xuống cuối.

Ví dụ: khử M ở hình.

1. R2 <- R2 - 2R1 và R3 <- R3 - R1: cột x dưới trụ thành 0.
2. R3 <- R3 + 2R2: (0, -2, 2 | 4) + (0, 2, 2 | 0) = (0, 0, 4 | 4).
3. Hàng cuối nói 4z = 4, nên z = 1.

### Khi trụ bằng 0

:::figure grid
caption: Ô trụ bằng 0 (đỏ): đổi chỗ hai hàng rồi mới khử tiếp, không chia cho 0.
style: matrix
table "trước"
row 0 1 2
row 3 1 0
mark cell 1 1 do
op "R1 <-> R2"
table "sau"
row 3 1 0
row 0 1 2
mark cell 1 1 vang
:::

Ô trụ bằng 0 thì đổi chỗ với một hàng dưới, không bao giờ chia cho 0. Dạng bậc thang không duy nhất (nhân một hàng với số khác 0 vẫn là bậc thang), nhưng vị trí các trụ thì luôn như nhau.

> Lỗi thường gặp: chia cho một trụ bằng 0. Gặp số 0 ở chỗ trụ thì đổi chỗ hàng trước.

:::check
Q: Ma trận có các hàng (0, 2, 1), (1, 3, 0), (0, 0, 5) đã là bậc thang chưa? Một phép nào sửa được?
A: Chưa: hàng 2 bắt đầu ở cột 1, lệch trái so với hàng 1. Đổi chỗ R1 và R2 là xong.
:::

## Thế ngược tìm nghiệm

:::hook
Bậc thang giải như leo cầu thang từ dưới lên: bậc dưới cùng chỉ có một ẩn, giải xong thì mang giá trị đó lên bậc trên.
:::

:::figure flow
caption: Hệ bậc thang (1, -1, 2 | 5), (0, 3, 1 | 11), (0, 0, 2 | 4): mỗi bậc dùng mọi ẩn đã tìm ở bậc dưới.
box "2z = 4: z = 2"
link "mang z lên"
box "3y + z = 11: y = 3" xanh
link "mang y, z lên"
box "x - y + 2z = 5: x = 4" luc
:::

:::core
Thế ngược đi từ dưới lên: giải phương trình cuối (ít ẩn nhất), rồi thay mọi giá trị vừa tìm vào phương trình ngay trên.
:::

> Lỗi thường gặp: chuyển vế quên đổi dấu. Từ x - 3 + 4 = 5 phải ra x = 5 + 3 - 4, không phải 5 - 3 + 4.

:::check
Q: Hệ bậc thang có hàng (2, 1 | 7) và (0, 3 | 3). Tìm x và y.
A: Hàng dưới: 3y = 3, y = 1. Hàng trên: 2x + 1 = 7, x = 3.
:::

### Ẩn tự do

Cột không có trụ là ẩn tự do: đặt nó bằng t, các ẩn có trụ tính theo t. Mỗi giá trị của t cho một nghiệm.

Ví dụ: bậc thang (1, 1, -2 | 1), (0, 1, 3 | 4), hàng 3 toàn 0.

1. z không có trụ: đặt z = t.
2. Hàng 2: y = 4 - 3t.
3. Hàng 1: x = 1 - y + 2t = -3 + 5t.
4. Chẳng hạn t = 1 cho (2, 1, 1); thử: 2 + 1 - 2 = 1.

$$ (x, y, z) = (-3 + 5t, \; 4 - 3t, \; t) $$

:::check
Q: Hệ chỉ còn một hàng bậc thang (1, 2 | 3) với hai ẩn x, y. Viết mọi nghiệm.
A: y không có trụ: y = t, rồi x = 3 - 2t. Nghiệm (3 - 2t, t).
:::

## Biện luận số nghiệm

:::hook
Hai đường thẳng trên mặt phẳng chỉ gặp nhau theo ba kiểu: cắt nhau, song song, trùng nhau. Hệ tuyến tính cũng vậy: 1 nghiệm, 0 nghiệm, hoặc vô số.
:::

:::figure plane
caption: Mỗi phương trình hai ẩn là một đường thẳng; nghiệm là chỗ chúng gặp nhau. Cắt nhau, song song, hay trùng nhau.
size: 380 100
axes: off
x: -0.3 12.3
y: -1 3.3
segment 0 3 3 0 xanh
segment 1 0 3.3 2.3 do
point 2 1 muc
text 1.6 -0.6 "1 nghiệm"
segment 4.5 3 7.5 0 xanh
segment 4.5 1.5 6 0 do
text 6 -0.6 "vô nghiệm"
segment 9 3 12 0 xanh
segment 9 3 12 0 do dash
text 10.5 -0.6 "vô số nghiệm"
:::

:::core
Nhìn bậc thang: có hàng (0 ... 0 | c) với c != 0 là vô nghiệm; không có thì ẩn nào cũng có trụ là nghiệm duy nhất, còn ẩn tự do là vô số nghiệm.
:::

:::check
Q: Hệ 3 ẩn có bậc thang: trụ ở cột x và y, hàng cuối là (0, 0, 0 | 0). Hệ có bao nhiêu nghiệm?
A: Vô số: hàng 0 = 0 luôn đúng, không chặn gì; z không có trụ nên là ẩn tự do.
:::

### Biện luận theo tham số

Không hệ nào có đúng 2 nghiệm: có hai nghiệm u, v thì cả đường thẳng qua chúng đều là nghiệm. Nhiều ẩn hơn phương trình chỉ loại nghiệm duy nhất; hệ vẫn có thể vô nghiệm.

$$ A(u + t(v - u)) = b + t \cdot 0 = b $$

Ví dụ: hệ x + 2y = 1, 3x + my = 4. Với m nào thì vô nghiệm?

1. R2 <- R2 - 3R1 cho hàng (0, m - 6 | 1).
2. m = 6: hàng đó nói 0 = 1, vô nghiệm.
3. m != 6: y có trụ, nghiệm duy nhất. Hệ này không bao giờ có vô số nghiệm.

> Lỗi thường gặp: thấy 3 ẩn, 2 phương trình là kết luận vô số nghiệm. Phải khử xong, xem có hàng 0 = c không.

:::check
Q: Hệ x + y = 2, 2x + 2y = k. Với k nào hệ có vô số nghiệm, với k nào vô nghiệm?
A: R2 <- R2 - 2R1 cho (0, 0 | k - 4). k = 4: hàng 0 = 0, vô số nghiệm. k != 4: 0 = k - 4 sai, vô nghiệm.
:::

## Hệ thuần nhất Ax = 0

:::hook
Tìm những tổ hợp thuộc tính triệt tiêu nhau (dữ liệu dư thừa) là giải Ax = 0. Câu hỏi không phải có nghiệm không, mà là có nghiệm khác 0 không.
:::

:::figure plane
caption: x - 2y = 0 và 3x + y = 0 chỉ gặp nhau ở gốc: chỉ có nghiệm 0.
size: 130 80
x: -2.5 2.5 5
y: -2 2 5
line 0 0 2 1 xanh
line 0 0 -1 3 do
point 0 0 muc
:::

:::figure plane
caption: x - 2y = 0 và 2x - 4y = 0 trùng nhau: mọi t(2, 1) là nghiệm.
size: 130 80
x: -2.5 2.5 5
y: -2 2 5
line 0 0 2 1 xanh
line 0 0 2 1 do dash
point 2 1 muc
point 0 0 muc
:::

:::core
Ax = 0 luôn có nghiệm x = 0; nó có thêm nghiệm khác 0 đúng khi có ẩn tự do, tức số trụ ít hơn số ẩn.
:::

Số ẩn tự do = số ẩn - số trụ. Hệ thuần nhất có nhiều ẩn hơn phương trình luôn có nghiệm khác 0. Cột vế phải toàn 0 nên có thể bỏ khi khử.

> Lỗi thường gặp: nói hệ thuần nhất "vô nghiệm". Nó luôn có ít nhất nghiệm x = 0.

:::check
Q: Hệ thuần nhất 4 phương trình, 4 ẩn; khử Gauss được 3 trụ. Có nghiệm khác 0 không?
A: Có: 4 - 3 = 1 ẩn tự do, cho nó giá trị khác 0 là được một nghiệm khác 0.
:::

### Giải hệ thuần nhất

Ví dụ: giải x + 2y - z = 0, 2x + 5y + z = 0.

1. R2 <- R2 - 2R1 cho (0, 1, 3): trụ ở x và y, z tự do.
2. Đặt z = t: y = -3t, rồi x = -2y + z = 7t.
3. Thử t = 1: 7 - 6 - 1 = 0 và 14 - 15 + 1 = 0.

$$ (x, y, z) = t(7, -3, 1) $$

:::check
Q: Giải hệ x + y = 0, y - z = 0.
A: z tự do, đặt z = t: y = t, x = -t. Nghiệm (x, y, z) = t(-1, 1, 1).
:::
