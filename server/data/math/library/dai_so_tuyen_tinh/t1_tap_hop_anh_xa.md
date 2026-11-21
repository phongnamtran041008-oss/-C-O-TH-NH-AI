---
id: dstt_lib_t1
title_vi: Tập hợp và ánh xạ
subject: dai_so_tuyen_tinh
floor: 1
format: 2
summary_vi: Tập hợp là cái túi, ánh xạ là bó mũi tên: chọn tập con, giao hợp hiệu, ghép cặp, rồi xem mũi tên đi đâu, có chung đích không, có đi ngược được không.
skills: [dstt_t1_tap_hop, dstt_t1_phep_toan_tap_hop, dstt_t1_tich_descartes, dstt_t1_anh_xa, dstt_t1_don_toan_song_anh, dstt_t1_hop_va_nguoc]
---
## Tập hợp và phần tử

:::hook
Một bộ dữ liệu huấn luyện là một tập ảnh; mỗi lô (batch) đưa vào máy là một tập con của nó. Hỏi "ảnh này có trong lô không" chỉ có hai câu trả lời: có hoặc không.
:::

:::figure graph
caption: Lập tập con của {a, b, c}: mỗi phần tử một lần chọn lấy (xanh) hay bỏ (xám). Ba lần chọn đôi cho 2 . 2 . 2 = 8 tập con.
layout: ltr
node R "chọn a?"
node A1 "{a}"
node A0 "{ }"
node B11 "{a,b}"
node B10 "{a}"
node B01 "{b}"
node B00 "{ }"
node C111 "{a,b,c}"
node C110 "{a,b}"
node C101 "{a,c}"
node C100 "{a}"
node C011 "{b,c}"
node C010 "{b}"
node C001 "{c}"
node C000 "{ }"
edge R A1 xanh
edge R A0 xam
edge A1 B11 xanh
edge A1 B10 xam
edge A0 B01 xanh
edge A0 B00 xam
edge B11 C111 xanh
edge B11 C110 xam
edge B10 C101 xanh
edge B10 C100 xam
edge B01 C011 xanh
edge B01 C010 xam
edge B00 C001 xanh
edge B00 C000 xam
:::

:::core
Tập hợp là một cái túi: mỗi vật chỉ ở trong hoặc ở ngoài, và mỗi tập con là một cách chọn lấy hay bỏ từng vật.
:::

Vật nằm trong túi là phần tử. Tập con là cả một túi nhỏ mà mọi thứ trong nó đều nằm trong túi lớn. Tập rỗng là tập con của mọi tập: nó không có gì nằm ngoài cả.

Ví dụ: A = {3, 5, 8, 9} có bao nhiêu tập con?

1. Đếm phần tử: A có 4 phần tử.
2. Mỗi phần tử có 2 cách: lấy hoặc bỏ.
3. Số tập con: 2^4 = 16, kể cả tập rỗng và chính A.

> Lỗi thường gặp: coi {1, {2, 3}} có ba phần tử. Nó chỉ có hai: số 1 và cái túi {2, 3}. Số 2 nằm trong túi con, không phải phần tử của tập lớn.

:::check
Q: Cho A = {1, {1, 2}} và B = {1, 2}. B là phần tử của A hay tập con của A?
A: Là phần tử: B được liệt kê trong A. Không là tập con: 2 không phải phần tử của A.
:::

## Phép toán trên tập hợp

:::hook
Gõ "mèo" VÀ "chó" vào máy tìm kiếm là lấy giao hai tập kết quả; "mèo" HOẶC "chó" là hợp; "mèo" mà KHÔNG "chó" là hiệu.
:::

:::figure sets
caption: Phần vàng là giao {5, 6}. A \ B chỉ là phần của A nằm ngoài B: {1, 3}. Hợp là cả hai hình tròn.
size: 230 100
set A "A" xanh
set B "B" do
shade A&B vang
in A-B "1, 3"
in A&B "5, 6"
in B-A "8"
:::

:::core
Giao là phần chung, hợp là gom tất cả (mỗi phần tử viết một lần), còn A \ B là A bỏ đi phần dính vào B.
:::

Phần bù của A trong tập nền U là U \ A: mọi thứ của U nằm ngoài A. Có ngoặc thì làm trong ngoặc trước.

Ví dụ: với A = {1, 3, 5, 6} và B = {5, 6, 8} như hình, A hợp B có bao nhiêu phần tử?

1. Cộng thẳng: 4 + 3 = 7, nhưng 5 và 6 bị đếm hai lần.
2. Bớt phần chung một lần: 7 - 2 = 5.
3. Đúng vậy: A hợp B = {1, 3, 5, 6, 8}.

$$ |A \cup B| = |A| + |B| - |A \cap B| $$

> Lỗi thường gặp: tưởng A \ B = B \ A. Ở hình, A \ B = {1, 3} còn B \ A = {8}: hai mảnh trăng khác nhau.

:::check
Q: Tập nền U = {1, 2, ..., 8}. Phần bù của A = {1, 3, 5, 6} trong U là gì, có mấy phần tử?
A: {2, 4, 7, 8}, gồm 4 phần tử: mọi số của U không nằm trong A.
:::

## Tích Descartes

:::hook
Mỗi ô bàn cờ vua có tên là một cặp (cột, hàng) như (e, 4). 8 cột nhân 8 hàng ra 64 ô: bàn cờ chính là một tích Descartes.
:::

:::figure grid
caption: Hàng lấy từ A, cột lấy từ B: mỗi ô là một cặp, 2 hàng x 3 cột = 6 cặp.
table "A x B"
head "p" "q" "r"
side "1" "2"
row "(1, p)" "(1, q)" "(1, r)"
row "(2, p)" "(2, q)" "(2, r)"
mark cell 2 3 vang
:::

:::core
A x B là bảng mọi cặp (a, b) có thứ tự, a lấy từ A, b lấy từ B, nên số cặp là |A| . |B|.
:::

Có thứ tự nghĩa là (1, p) khác (p, 1). Vì thế A x B khác B x A, dù hai tập có cùng số phần tử. Ở tầng 3, vị trí các ô của một ma trận cũng là cặp (hàng, cột).

Ví dụ: A x B có 15 phần tử và A có 5 phần tử. B có bao nhiêu phần tử?

1. Số cặp là tích: 5 . |B| = 15.
2. Chia: |B| = 3.

$$ |A \times B| = |A| \cdot |B| $$

> Lỗi thường gặp: cộng thay vì nhân, ra 2 + 3 = 5 cặp. Mỗi hàng của bảng có đủ 3 ô, nên phải nhân.

:::check
Q: Cho A = {u, v}. A x A có bao nhiêu phần tử? (u, v) và (v, u) có phải là một không?
A: 4 phần tử: (u, u), (u, v), (v, u), (v, v). Hai cặp kia khác nhau, vì thứ tự khác nhau.
:::

## Ánh xạ, ảnh và tạo ảnh

:::hook
Mô hình phân loại ảnh là một ánh xạ: mỗi ảnh vào nhận đúng một nhãn. Hai ảnh khác nhau được cùng nhãn "mèo", nhưng một ảnh không được vừa "mèo" vừa "chó".
:::

:::figure map
caption: f(x) = x^2. Mỗi x có đúng một mũi tên. Ảnh f(X) = {1, 4, 9}; số 0 không được trúng. Tạo ảnh của {4} là {-2, 2} (đỏ).
col "X" -2 -1 1 2 3
col "Y" 0 1 4 9
gap 1 "f"
-2 -> 4 do
-1 -> 1
1 -> 1
2 -> 4 do
3 -> 9
:::

:::core
Ánh xạ gửi mỗi phần tử của X tới đúng một phần tử của Y; ảnh là nơi các mũi tên cắm tới, tạo ảnh là nơi chúng xuất phát.
:::

"Đúng một" là luật duy nhất: quy tắc cho x hai kết quả, hoặc bỏ sót x nào, đều không phải ánh xạ. Tạo ảnh của một tập có thể rỗng.

Ví dụ: f(x) = x^2 - 1, A = {-3, -1, 0, 1}. Tìm f(A).

1. Tính từng ảnh: 8, 0, -1, 0.
2. Gom lại, mỗi giá trị viết một lần: f(A) = {-1, 0, 8}.

$$ f(A) = \{f(x) : x \in A\} $$

> Lỗi thường gặp: cho f(A) có 4 phần tử vì A có 4 phần tử. Hai mũi tên được phép cắm vào cùng một đích.

:::check
Q: Với f(x) = x^2 - 1 từ R vào R, tạo ảnh của tập {-5} là gì?
A: Tập rỗng: x^2 - 1 = -5 nghĩa là x^2 = -4, không có số thực nào.
:::

## Đơn ánh, toàn ánh, song ánh

:::hook
Phát số báo danh: hai thí sinh không được trùng số. Xếp phòng thi: không ghế nào bỏ trống. Đủ cả hai thì mỗi ghế có đúng một người.
:::

:::figure map
caption: Không đơn ánh: 1 và 2 chung ảnh.
col "X" 1 2 3
col "Y" a b c
1 -> a do
2 -> a do
3 -> b
:::

:::figure map
caption: Không toàn ánh: c bị bỏ trống.
col "X" 1 2
col "Y" a b c do
1 -> a
2 -> b
:::

:::figure map
caption: Song ánh: mỗi đích một mũi tên.
col "X" 1 2 3
col "Y" a b c
1 -> b luc
2 -> c luc
3 -> a luc
:::

:::core
Đơn ánh: không ai dùng chung ảnh; toàn ánh: không phần tử nào của Y bị bỏ trống; song ánh: cả hai, mỗi phần tử của Y nhận đúng một mũi tên.
:::

Bác bỏ đơn ánh chỉ cần một cặp như f(1) = f(-1). Chứng minh đơn ánh thì đi từ f(u) = f(v) tới u = v; với -4x - 1, từ -4u - 1 = -4v - 1 ra ngay u = v. Toàn ánh: giải f(x) = y với mọi y của Y. Còn e^x từ R vào R đơn ánh mà không toàn ánh: nó không bao giờ ra số <= 0.

$$ f(u) = f(v) \Rightarrow u = v $$

Ví dụ: có bao nhiêu đơn ánh từ {1, 2, 3} vào {a, b, c, d}?

1. Ảnh của 1: 4 cách.
2. Ảnh của 2 phải khác: còn 3 cách. Ảnh của 3: còn 2 cách.
3. Tổng: 4 . 3 . 2 = 24. Khi hai tập cùng 3 phần tử thì có 3 . 2 . 1 = 6 song ánh.

> Lỗi thường gặp: nói "f không toàn ánh" mà quên hỏi Y là tập nào. Đổi Y là đổi câu trả lời.

:::check
Q: Xem f(x) = e^x là ánh xạ từ R vào tập các số dương. Nó thuộc loại nào?
A: Song ánh: e^x tăng nên đơn ánh, và mọi y > 0 có x = ln y nên toàn ánh.
:::

## Ánh xạ hợp và ánh xạ ngược

:::hook
Chuẩn hóa ảnh rồi cắt ảnh không cho cùng kết quả với cắt rồi mới chuẩn hóa. Mã hóa rồi giải mã thì phải trả lại đúng tin nhắn cũ: đó là ánh xạ ngược.
:::

:::figure flow
caption: g(f(3)): làm f trước (bình phương), được 10.
box "3"
link "f: x^2"
box "9" xanh
link "g: +1"
box "10" luc
:::

:::figure flow
caption: f(g(3)): làm g trước (cộng 1), được 16. Đổi thứ tự, đổi kết quả.
box "3"
link "g: +1"
box "4" xanh
link "f: x^2"
box "16" luc
:::

:::core
g o f là làm f trước rồi mới g (chữ gần x nhất làm trước); ánh xạ ngược quay ngược mọi mũi tên, nên chỉ song ánh mới có.
:::

Không đơn ánh thì một đích có hai mũi tên, quay ngược không biết về đâu; không toàn ánh thì có đích không có đường về.

Ví dụ: tìm ánh xạ ngược của f(x) = 5x - 4.

1. Đặt y = 5x - 4 rồi giải theo x: x = (y + 4)/5.
2. Vậy f^-1(x) = (x + 4)/5.
3. Thử: f(2) = 6 và f^-1(6) = 10/5 = 2.

$$ (g \circ f)(x) = g(f(x)) $$

> Lỗi thường gặp: viết f^-1(x) = 1/f(x). Ánh xạ ngược là đi ngược mũi tên, không phải lấy nghịch đảo của số.

:::check
Q: f(x) = 2x và g(x) = x - 3. Tính g(f(5)) và f(g(5)).
A: g(f(5)) = g(10) = 7; f(g(5)) = f(2) = 4.
:::
