---
id: tr_lib_t4
title_vi: Bài toán tối ưu tổ hợp và độ phức tạp thuật toán
subject: toi_uu_roi_rac
floor: 4
format: 2
summary_vi: Không chỉ đếm mà phải chọn ra cấu hình tốt nhất: viết rõ phương án và hàm mục tiêu, duyệt toàn bộ, cắt nhánh bằng cận, thử tham lam và biết lúc nó sai, rồi đo tốc độ thuật toán bằng ký hiệu O.
skills: [tr_t4_phat_bieu, tr_t4_duyet_toan_bo, tr_t4_nhanh_can, tr_t4_tham_lam, tr_t4_ky_hieu_o]
---
## Phát biểu bài toán tối ưu tổ hợp

:::hook
Chọn những mô hình nào chạy trên một GPU 7 GB để tổng điểm cao nhất: đó là bài toán cái túi, bài toán tối ưu tổ hợp kinh điển.
:::

:::figure grid
caption: Túi chứa 7, đồ vật nặng 2, 3, 4, 5, giá trị 3, 5, 6, 8. Dòng đỏ giá trị cao nhất nhưng quá nặng: không phải phương án.
table
head "x" "nặng" "giá trị"
row "1100" 5 8
row "0110" 7 11
row "1001" 7 11
row "0011" 9 14
mark row 4 do
:::

:::core
Bài toán tối ưu tổ hợp có hai phần: tập phương án hữu hạn (các cấu hình thỏa ràng buộc) và hàm mục tiêu; cần tìm phương án làm hàm mục tiêu tốt nhất.
:::

Cái túi viết đầy đủ: x_i = 1 khi lấy đồ vật i; tối đa tổng giá trị, giữ tổng khối lượng trong sức chứa b.

$$ \sum_{i=1}^{n} c_i x_i \to \text{max} $$

$$ \sum_{i=1}^{n} a_i x_i \le b, \quad x_i \in \{0, 1\} $$

:::check
Q: Nhìn bảng: phương án tốt nhất trong bốn dòng là gì? Vì sao không phải 0011?
A: 0110 hoặc 1001, cùng giá trị 11. 0011 nặng 9 > 7, vi phạm ràng buộc nên không được xét.
:::

### Ba bài toán mẫu

Thứ tự bỏ đồ vào túi không quan trọng, nên phương án cái túi là một xâu nhị phân. Hai bài kia thì phương án là hoán vị:

- Người du lịch: đi qua n thành phố, mỗi nơi một lần, rồi về thành phố 1. Phương án là thứ tự (1, j_2, ..., j_n). Hàm mục tiêu là tổng độ dài, kể cả đoạn trở về d(j_n, 1).
- Phân việc: n người, n việc, người i làm việc j_i, chi phí c(i, j_i). Hai người không nhận chung một việc, nên phương án là hoán vị (j_1, ..., j_n).

> Lỗi thường gặp: đếm n^n cách phân việc. Đó là khi hai người được nhận chung một việc; đúng phải là n!.

:::check
Q: Phân 3 việc cho 3 đệ tử, mỗi người một việc khác nhau. Có bao nhiêu phương án? Vì sao không phải 27?
A: 3! = 6. 3^3 = 27 đếm cả những cách hai người nhận chung một việc.
:::

## Duyệt toàn bộ

:::hook
Thử mọi mật khẩu thì chắc chắn mở được khóa, nhưng là cách chậm nhất.
:::

:::figure graph
caption: Bốn thành phố. Đường xanh 1-2-3-4-1 dài 2 + 3 + 1 + 4 = 10.
size: 140 85
layout: free
node 1 0 1 "1"
node 2 2 0 "2"
node 3 4 1 "3"
node 4 2 4 "4"
edge 1 2 2 xanh
edge 2 3 3 xanh
edge 3 4 1 xanh
edge 4 1 4 xanh
edge 1 3 5
edge 2 4 6
:::

:::figure grid
caption: Mỗi hành trình đi ngược chiều dài bằng nó: chỉ cần xét 3.
table
head "hành trình" "độ dài"
row "1-2-3-4-1" 10
row "1-2-4-3-1" 14
row "1-3-2-4-1" 18
mark row 1 vang
:::

:::core
Duyệt toàn bộ xét từng phương án và giữ cái tốt nhất làm kỷ lục: luôn đúng, nhưng số phương án bùng nổ rất nhanh.
:::

1. Đặt kỷ lục ban đầu (rất lớn nếu tìm giá trị nhỏ nhất).
2. Với mỗi phương án, tính hàm mục tiêu; tốt hơn kỷ lục thì cập nhật.
3. Hết phương án: kỷ lục là giá trị tối ưu.

Số phương án với n đồ vật, n thành phố (cố định thành phố 1), n người phân việc:

$$ 2^n, \quad (n-1)!, \quad n! $$

> Lỗi thường gặp: 40 đồ vật cho 2^40 phương án, không phải 40^2.

:::check
Q: Máy xét 10^6 phương án mỗi giây. Duyệt cái túi 30 đồ vật mất khoảng bao lâu?
A: 2^30 khoảng 1,07 . 10^9 phương án, tức khoảng 1074 giây, gần 18 phút. Thêm 10 đồ vật là gấp 1024 lần.
:::

## Thuật toán nhánh cận

:::hook
Kỷ lục đang là 19 điểm, mà nhánh này cao lắm được 18: khỏi đi vào.
:::

:::figure graph
caption: Cái túi, tìm giá trị lớn nhất. Nút vàng cho kỷ lục 19. Nút có cận trên <= 19 bị cắt (đỏ); cận lớn hơn thì xét tiếp.
size: 300 85
layout: tree
node R "gốc"
node A "x1=1: 25"
node B "x1=0: 21"
node AA "x2=1: 19" vang
node AB "x2=0: 20"
node ABa "x3=1: 19" do
node ABb "x3=0: 15" do
node Ba "x2=1: 17" do
node Bb "x2=0: 14" do
edge R A
edge R B
edge A AA vang
edge A AB
edge AB ABa do dash
edge AB ABb do dash
edge B Ba do dash
edge B Bb do dash
:::

:::core
Nhánh cận là quay lui biết ước lượng: cận cho biết nhánh tốt nhất được tới đâu; nếu không thể hơn kỷ lục thì cắt cả nhánh.
:::

- Tìm giá trị nhỏ nhất: cận dưới >= kỷ lục thì cắt.
- Tìm giá trị lớn nhất: cận trên <= kỷ lục thì cắt.

Kỷ lục là giá trị tốt nhất tìm được tới lúc đó; khi dừng, nó là giá trị tối ưu.

> Lỗi thường gặp: tìm lớn nhất mà cắt nhánh có cận trên 23 > kỷ lục 20.

:::check
Q: Tìm giá trị nhỏ nhất, kỷ lục 30, một nhánh có cận dưới 27: cắt được không?
A: Không. Trong nhánh có thể có phương án giá trị từ 27 đến 29, tốt hơn kỷ lục.
:::

### Cận trên của cái túi

Xếp đồ vật theo tỉ số giá trị/khối lượng giảm dần. Đã quyết định k đồ vật đầu, được giá trị v, còn sức chứa b_k: phần còn lại không thể quý hơn tỉ số của đồ vật kế tiếp.

$$ g = v + b_k \cdot \frac{c_{k+1}}{a_{k+1}} $$

Ví dụ: hình trên có túi chứa 7, đồ vật (nặng, giá trị) = (2, 10), (3, 9), (4, 8), (5, 5). Tính cận nút x1 = 1, x2 = 0.

1. Đã lấy đồ vật 1: v = 10, còn sức chứa 7 - 2 = 5.
2. Đồ vật kế tiếp là đồ vật 3, tỉ số 8/4 = 2.
3. g = 10 + 5 . 2 = 20 > 19: chưa cắt được, phải xét tiếp.

:::check
Q: Cũng bài đó, nút x1 = 0 có cận bao nhiêu?
A: v = 0, còn sức chứa 7, đồ vật kế tiếp là đồ vật 2 với tỉ số 9/3 = 3: g = 0 + 7 . 3 = 21.
:::

## Thuật toán tham lam

:::hook
Thu ngân trả tiền thừa bằng cách đưa tờ lớn nhất còn vừa trước. Với tiền Việt thì ổn; với một hệ mệnh giá lạ thì có thể không.
:::

:::figure grid
caption: Đồng 1, 5, 6; trả 10. Tham lam lấy 6 trước rồi kẹt: 5 đồng. Hai đồng 5 là đủ.
table "tham lam"
row 6 1 1 1 1
op "khác"
table "tốt nhất"
row 5 5
:::

:::core
Tham lam mỗi bước chọn cái tốt nhất trước mắt và không bao giờ sửa lại: rất nhanh, nhưng chỉ tin được khi đã chứng minh nó tối ưu.
:::

Một phản ví dụ nhỏ là đủ bác bỏ tham lam. Muốn tin nó, phải chứng minh, hoặc so với duyệt toàn bộ trên các bài nhỏ.

Ví dụ: túi chứa 6, đồ vật (nặng, giá trị) = (4, 8), (3, 5), (3, 5). Tham lam theo tỉ số giá trị/khối lượng.

1. Tỉ số 2, 5/3, 5/3: lấy đồ vật 1 trước, còn sức chứa 2.
2. Hai đồ vật kia nặng 3, không vừa: tham lam được 8.
3. Lấy hai đồ vật nặng 3 được 10: tham lam không tối ưu.

> Lỗi thường gặp: chạy đúng thuật toán tham lam rồi tin ngay kết quả là tối ưu.

:::check
Q: Đồng 1, 7, 10. Trả 14 thì tham lam dùng mấy đồng? Ít nhất là mấy?
A: Tham lam: 10 + 1 + 1 + 1 + 1, 5 đồng. Ít nhất: 7 + 7, 2 đồng.
:::

### Khi tham lam đúng: xếp lịch

:::figure grid
caption: Mỗi lần chọn buổi kết thúc sớm nhất còn xếp được: A, C, D (xanh). Không cách nào xếp được 4 buổi.
table
head 1 2 3 4 5 6 7 8
side "A [0,2]" "B [1,5]" "C [2,4]" "D [4,7]" "E [5,8]" "F [6,8]"
row "#" "#" . . . . . .
row . "#" "#" "#" "#" . . .
row . . "#" "#" . . . .
row . . . . "#" "#" "#" .
row . . . . . "#" "#" "#"
row . . . . . . "#" "#"
mark row 1 luc
mark row 3 luc
mark row 4 luc
:::

Một phòng luyện công, nhiều buổi xin dùng. Chọn buổi kết thúc sớm nhất trong các buổi còn xếp được: nó để lại nhiều thời gian nhất cho phần sau, nên tham lam này luôn tối ưu.

:::check
Q: Các buổi [0, 4], [1, 2], [2, 3], [3, 5], [4, 6]. Xếp được nhiều nhất mấy buổi?
A: Kết thúc sớm nhất: [1, 2], rồi [2, 3], rồi [3, 5]; [4, 6] bắt đầu trước 5. Được 3 buổi.
:::

## Ký hiệu O lớn

:::hook
Dữ liệu tăng 1000 lần, thuật toán chậm đi 1000 lần hay 1 triệu lần?
:::

:::figure plane
caption: Khi n lớn, 2^n bỏ xa n^2, n^2 bỏ xa n, n bỏ xa log n.
size: 220 120
x: 1 6 1
y: 0 40 10
names: n T
curve "2^x" do "2^n" pos=w
curve "x^2" vang "n^2" pos=se
curve "x" xanh "n" pos=se
curve "ln(x)/ln(2)" luc "log n" pos=n
:::

:::core
O đo tốc độ tăng: f(n) = O(g(n)) nghĩa là f(n) <= C . g(n) khi n đủ lớn, nên bỏ hằng số nhân và các số hạng tăng chậm hơn.
:::

$$ f(n) = O(g(n)) \Leftrightarrow f(n) \le C \cdot g(n) \text{ khi } n \ge n_0 $$

Ví dụ: 4n^2 + 7n + 20 <= 4n^2 + 7n^2 + 20n^2 = 31n^2 khi n >= 1, nên nó là O(n^2). O(n^3) cũng đúng nhưng lỏng; O(n^2) là chặt nhất.

$$ \log n < n < n \log n < n^2 < 2^n < n! $$

> Lỗi thường gặp: nói O(4n) chậm gấp đôi O(2n): cả hai là O(n). Hằng số ở số mũ thì không bỏ được: 4^n không là O(2^n).

:::check
Q: T(n) = 2n^3 + 100n^2. Đánh giá O chặt nhất là gì? T(n) có là O(n^2) không?
A: O(n^3), vì T(n) <= 102n^3 khi n >= 1. Không là O(n^2): T(n)/n^2 >= 2n tăng mãi, không hằng số C nào chặn được.
:::

### Đếm vòng lặp

- Hai vòng for lồng nhau, mỗi vòng n lần: n^2 lượt.
- for i = 1 to n: for j = i + 1 to n: (n - 1) + ... + 1 + 0 = n(n - 1)/2 lượt. Nếu j chạy từ i thì n(n + 1)/2. Vẫn là O(n^2).
- j = 1; while j <= n: j = 2j: j đi qua 1, 2, 4, ...: khoảng log_2 n lượt.

Ví dụ: đếm số lượt của hai đoạn với n = 10 và n = 50.

1. for i = 1 to 10: for j = i + 1 to 10: 10 . 9/2 = 45 lượt.
2. j = 1; while j <= 50: j = 2j: j là 1, 2, 4, 8, 16, 32 rồi 64 > 50: 6 lượt.

:::check
Q: for i = 1 to 20: for j = i to 20: x = x + 1. Lệnh x = x + 1 chạy bao nhiêu lần?
A: 20 + 19 + ... + 1 = 20 . 21/2 = 210 lần.
:::
