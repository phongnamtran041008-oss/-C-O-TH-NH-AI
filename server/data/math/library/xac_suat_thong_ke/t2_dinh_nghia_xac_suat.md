---
id: xs_lib_t2
title_vi: Định nghĩa xác suất: cổ điển và thống kê
subject: xac_suat_thong_ke
floor: 2
format: 2
summary_vi: Xác suất là một con số từ 0 đến 1: đếm phần thuận lợi khi các kết quả đồng khả năng, hoặc đo tần suất khi đã thử rất nhiều lần.
skills: [xs_t2_co_dien, xs_t2_co_dien_to_hop, xs_t2_hoan_lai, xs_t2_tinh_chat, xs_t2_thong_ke]
---
## Xác suất cổ điển

:::hook
Trò Đổ Linh Thạch trả thưởng theo tổng hai xúc xắc. Nhà cái không đoán: họ đếm xem mỗi tổng chiếm bao nhiêu trong 36 cặp, rồi mới đặt giá.
:::

:::figure bars
caption: Số cặp cho mỗi tổng t của hai xúc xắc: 6 - |t - 7|. Tổng 7 có 6 trong 36 cặp.
size: 210 100
bar "2" 1
bar "3" 2
bar "4" 3
bar "5" 4
bar "6" 5
bar "7" 6 do
bar "8" 5
bar "9" 4 vang
bar "10" 3 vang
bar "11" 2 vang
bar "12" 1 vang
:::

:::core
Khi n kết quả đồng khả năng, xác suất của A là phần A chiếm: m kết quả thuận lợi chia cho n.
:::

$$ P(A) = \frac{m}{n} $$

Ví dụ: gieo hai xúc xắc, tính P(tổng >= 9).

1. n = 36 cặp đồng khả năng.
2. Cột vàng: 4 + 3 + 2 + 1 = 10 cặp.
3. P = 10/36 = 5/18.

> Lỗi thường gặp: túi có 2 bi đỏ, 6 xanh, 2 vàng mà nói P(không xanh) = 2/3 vì "2 trong 3 màu". Mười viên bi mới đồng khả năng: P = 4/10 = 2/5.

:::check
Q: Nhìn hình: tổng 4 và tổng 10, tổng nào dễ ra hơn?
A: Bằng nhau: mỗi tổng có 3 cặp, cùng xác suất 3/36 = 1/12.
:::

## Xác suất cổ điển dùng tổ hợp

:::hook
Lô 10 mẫu dữ liệu có 4 mẫu gán nhãn sai. Lấy ngẫu nhiên 3 mẫu để soát: khả năng gặp đúng 1 mẫu sai là bao nhiêu?
:::

:::figure flow
caption: Đếm từng loại rồi nhân: 60 trong C(10, 3) = 120 nhóm.
box "1 trong 4 sai: 4" do
link "x"
box "2 trong 6 đúng: 15" luc
link "="
box "60 nhóm" vang
:::

:::core
Lấy đồng thời thì kết quả là một nhóm: tử và mẫu đều đếm nhóm, bằng tổ hợp.
:::

$$ P = \frac{C_a^r \cdot C_b^{k-r}}{C_{a+b}^k} $$

Xếp người thành hàng thì một kết quả là một hoán vị: mẫu số là n!.

Ví dụ: tính xác suất ở trên.

1. Mẫu: mọi nhóm 3 trong 10 mẫu, C(10, 3) = 120.
2. Tử: C(4, 1) . C(6, 2) = 4 . 15 = 60.
3. P = 60/120 = 1/2.

> Lỗi thường gặp: mẫu đếm có thứ tự, A(10, 3) = 720, mà tử đếm nhóm. Tử và mẫu phải đếm cùng một kiểu.

:::check
Q: Rút đồng thời 2 lá từ bộ 52 lá. Xác suất cả hai là át?
A: C(4, 2)/C(52, 2) = 6/1326 = 1/221.
:::

## Lấy có hoàn lại và không hoàn lại

:::hook
Bootstrap trong máy học lấy mẫu CÓ hoàn lại: một dòng dữ liệu có thể bị chọn hai lần. Chia tập huấn luyện và tập kiểm tra thì KHÔNG hoàn lại.
:::

:::figure grid
caption: Có hoàn lại: 16 ô. Không hoàn lại: bỏ 4 ô đỏ, còn 12. Đồng thời: 12 và 21 là một nhóm, còn 6.
table "lần 1 \ lần 2"
head "1" "2" "3" "4"
side "1" "2" "3" "4"
row 11 12 13 14
row 21 22 23 24
row 31 32 33 34
row 41 42 43 44
mark diag do
:::

:::core
Có hoàn lại: lần nào cũng đủ n cách. Không hoàn lại: lần sau ít đi một. Lấy đồng thời: chỉ còn nhóm, không thứ tự.
:::

$$ n^2, \qquad n(n-1), \qquad C_n^2 = \frac{n(n-1)}{2} $$

Ví dụ: hộp 3 bi trắng, 2 bi đen, lấy lần lượt 2 bi. Tính P(khác màu).

1. Không hoàn lại: mẫu 5 . 4 = 20.
2. Trắng rồi đen 3 . 2, đen rồi trắng 2 . 3: 12 cặp, P = 12/20 = 3/5.
3. Có hoàn lại: mẫu 5 . 5 = 25, vẫn 12 cặp khác màu, P = 12/25.

> Lỗi thường gặp: lấy không hoàn lại mà vẫn viết mẫu n . n. Lần thứ hai hộp đã vơi một bi.

:::check
Q: Hộp 4 bi trắng, 4 bi đen, lấy lần lượt 2 bi. P(cả hai trắng) khi có hoàn lại? Khi không hoàn lại?
A: Có hoàn lại: 16/64 = 1/4. Không hoàn lại: 4 . 3/(8 . 7) = 12/56 = 3/14.
:::

## Tính chất của xác suất và sự kiện đối

:::hook
"Trong 5 đệ tử có ít nhất hai người trùng ngày sinh?" Đếm thẳng rất rối. Đếm điều ngược lại, mọi người khác ngày, thì gọn hơn nhiều.
:::

:::figure grid
caption: Ít nhất một mặt 1: 11 ô đỏ, khó đếm. Phần còn lại 5 x 5 = 25 ô, đếm ngay.
table
head "1" "2" "3" "4" "5" "6"
side "1" "2" "3" "4" "5" "6"
row . . . . . .
row . . . . . .
row . . . . . .
row . . . . . .
row . . . . . .
row . . . . . .
mark row 1 do
mark col 1 do
:::

:::core
Mọi xác suất nằm giữa 0 và 1, và A với Ā chia nhau trọn 1. Gặp "ít nhất một", hãy đếm "không có cái nào".
:::

$$ P(\bar{A}) = 1 - P(A) $$

A, B xung khắc thì P(A + B) = P(A) + P(B). Sự kiện chắc chắn có xác suất 1, sự kiện không thể có 0.

Ví dụ: gieo 3 xúc xắc. P(có ít nhất một mặt 1)?

1. Mẫu: 6^3 = 216.
2. Đối: không xúc xắc nào ra 1, 5^3 = 125.
3. P = 1 - 125/216 = 91/216.

> Lỗi thường gặp: đối của "ít nhất một ngửa" là "ít nhất một sấp". Sai: SN thuộc cả hai. Đối đúng là "không có mặt ngửa nào".

:::check
Q: P(A) = 3/7. Tính P(Ā). Nếu B xung khắc với A và P(B) = 2/7, tính P(A + B).
A: P(Ā) = 1 - 3/7 = 4/7. P(A + B) = 3/7 + 2/7 = 5/7.
:::

## Định nghĩa thống kê: tần suất

:::hook
Không ai tính trước được xác suất một người bấm quảng cáo. Hệ thống đo: sau hàng vạn lượt xem, tỉ lệ bấm đứng yên quanh một con số.
:::

:::figure plane
caption: Tần suất ngửa sau 10, 50, 100, 500, 1000 lần tung (số cạnh chấm): dần sát vạch 1/2.
size: 200 90
axes: off
x: 0.5 6
y: 0.38 0.76
line 0 0.5 6 0.5 xam dash "1/2" pos=se
segment 1 0.7 2 0.44 xanh
segment 2 0.44 3 0.54 xanh
segment 3 0.54 4 0.482 xanh
segment 4 0.482 5 0.507 xanh
point 1 0.7 do "10" pos=e
point 2 0.44 xanh "50" pos=s
point 3 0.54 xanh "100" pos=n
point 4 0.482 xanh "500" pos=s
point 5 0.507 do "1000" pos=n
:::

:::core
Không đếm được thì đo: A xảy ra m lần trong n lần thử, tần suất là m/n. Thử càng nhiều, nó càng sát xác suất.
:::

$$ f_n(A) = \frac{m}{n} $$

Ví dụ: ba ngày quảng cáo: 200 lượt xem có 6 lượt bấm, 300 có 9, 500 có 13.

1. Gộp hết: 28 lượt bấm trong 1000 lượt xem.
2. Tần suất: 28/1000 = 7/250.
3. Dùng ngược: 5000 lượt xem cho khoảng 5000 . 7/250 = 140 lượt bấm.

Cá: đánh dấu 100, bắt lại 50 có 5 con dấu: hồ có cỡ 100 . 50/5 = 1000 con.

> Lỗi thường gặp: tưởng ít lần thử thì tần suất đã bằng xác suất.

:::check
Q: Gieo xúc xắc 30 lần, mặt 6 ra 8 lần. Tần suất? Đã đủ nói xúc xắc lệch chưa?
A: 8/30 = 4/15. Chưa: 30 lần quá ít, tần suất còn dao động quanh 1/6.
:::
