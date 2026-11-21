---
id: tr_lib_t5
title_vi: Đồ thị: khái niệm cơ bản và biểu diễn trên máy tính
subject: toi_uu_roi_rac
floor: 5
format: 2
summary_vi: Đồ thị là đỉnh và cạnh: các loại đồ thị, bậc và định lý bắt tay, đường đi và thành phần liên thông, rồi hai cách cất đồ thị trong máy, ma trận kề và danh sách kề, cùng việc mỗi cách giỏi ở đâu.
skills: [tr_t5_khai_niem, tr_t5_bac, tr_t5_duong_di_lien_thong, tr_t5_ma_tran_ke, tr_t5_danh_sach_ke]
---
## Đỉnh, cạnh và các loại đồ thị

:::hook
Mạng xã hội là đồ thị: người là đỉnh, kết bạn là cạnh. Theo dõi một chiều là cung có hướng.
:::

:::figure graph
caption: K_4: mọi cặp đỉnh kề nhau, C_4^2 = 6 cạnh.
size: 100 65
layout: circle
node 1
node 2
node 3
node 4
edge 1 2
edge 1 3
edge 1 4
edge 2 3
edge 2 4
edge 3 4
:::

:::figure graph
caption: Có hướng: 1 -> 2 và 2 -> 1 là hai cung khác nhau.
size: 100 65
layout: circle
directed: yes
node 1
node 2
node 3
edge 1 2
edge 2 1
edge 2 3
edge 3 1
:::

:::core
Đồ thị là một tập đỉnh cùng các cạnh nối từng cặp đỉnh; loại đồ thị cho biết cạnh có chiều không, có cạnh lặp hay khuyên không.
:::

- Đơn vô hướng: không chiều, không khuyên, mỗi cặp đỉnh nhiều nhất một cạnh. Đa đồ thị cho phép cạnh bội.
- Đầy đủ K_n: mọi cặp kề nhau, C_n^2 cạnh. Có hướng không khuyên: nhiều nhất A_n^2 = n(n - 1) cung.
- Đồ thị bù của G: cùng đỉnh, nối đúng những cặp G không nối. G có m cạnh thì bù có C_n^2 - m cạnh.

:::check
Q: Đồ thị đơn 8 đỉnh có 20 cạnh. Đồ thị bù của nó có bao nhiêu cạnh?
A: Mỗi cặp đỉnh thuộc đúng một trong hai đồ thị: C_8^2 - 20 = 28 - 20 = 8 cạnh.
:::

### Đồ thị hai phía

:::figure graph
caption: Chu trình 6 đỉnh tô được hai màu xen kẽ: hai phía.
size: 110 85
layout: circle
node 1 xanh
node 2 do
node 3 xanh
node 4 do
node 5 xanh
node 6 do
edge 1 2
edge 2 3
edge 3 4
edge 4 5
edge 5 6
edge 6 1
:::

:::figure graph
caption: Chu trình 5 đỉnh: cạnh 5-1 nối hai đỉnh cùng màu.
size: 110 85
layout: circle
node 1 xanh
node 2 do
node 3 xanh
node 4 do
node 5 xanh
edge 1 2
edge 2 3
edge 3 4
edge 4 5
edge 5 1 do
:::

Hai phía: chia được đỉnh thành hai phần, mọi cạnh nối hai phần khác nhau. Kiểm tra bằng tô màu: đỉnh kề một đỉnh màu A thì tô màu B. Gặp một cạnh hai đầu cùng màu là có chu trình lẻ, nên không hai phía. K_n với n >= 3 có tam giác nên không hai phía.

$$ |E(K_n)| = \frac{n(n-1)}{2}, \quad |E(K_{m,n})| = m \cdot n $$

> Lỗi thường gặp: tô màu xong quên kiểm cạnh cuối, như cạnh 5-1 ở hình phải.

:::check
Q: Đồ thị có các cạnh 1-2, 2-3, 3-4, 4-1, 1-3. Nó có hai phía không?
A: Không: 1, 2, 3 đôi một kề nhau tạo tam giác, một chu trình lẻ.
:::

## Bậc của đỉnh và định lý bắt tay

:::hook
Trong một buổi gặp mặt, đếm tổng số lần mỗi người bắt tay rồi chia đôi là ra số cái bắt tay: mỗi cái được hai người cùng đếm.
:::

:::figure graph
caption: Mỗi cạnh góp 1 vào bậc của cả hai đầu: tổng bậc 2 + 3 + 2 + 2 + 1 = 10 = 2 . 5 cạnh.
size: 170 85
layout: free
node A 0 1 "A:2"
node B 2 2 "B:3" vang
node C 2 0 "C:2"
node D 4 2 "D:2"
node E 6 2 "E:1"
edge A B
edge A C
edge B D
edge B C
edge D E
:::

:::core
Mỗi cạnh được đếm hai lần, một lần ở mỗi đầu: tổng các bậc bằng hai lần số cạnh, nên số đỉnh bậc lẻ luôn chẵn.
:::

$$ \sum_{v \in V} \deg(v) = 2|E| $$

Ví dụ: 8 đỉnh, đỉnh nào cũng bậc 3. Có mấy cạnh? Còn 7 đỉnh bậc 3 thì sao?

1. Tổng bậc 8 . 3 = 24, nên có 24/2 = 12 cạnh.
2. 7 . 3 = 21 lẻ, không chia đôi được: không có đồ thị nào như vậy.

> Lỗi thường gặp: quên chia đôi, lấy tổng bậc làm số cạnh.

:::check
Q: Đồ thị có 6 cạnh, bậc của bốn đỉnh là 3, 3, 2, 2, còn đỉnh thứ năm có bậc x. Tìm x.
A: Tổng bậc 2 . 6 = 12, nên x = 12 - 10 = 2.
:::

### Dãy bậc nào dựng được?

Trong đồ thị đơn n đỉnh, bậc nằm từ 0 đến n - 1, và không thể vừa có đỉnh bậc 0 vừa có đỉnh bậc n - 1. Vì thế luôn có hai đỉnh cùng bậc (Dirichlet). Kiểm tra một dãy bằng Havel-Hakimi: bỏ bậc lớn nhất d, trừ 1 ở d bậc lớn nhất còn lại, xếp lại, lặp. Về toàn 0 là dựng được; gặp số âm là không.

Ví dụ: dãy 3, 3, 2, 1, 1 có dựng được không?

1. Tổng 10 chẵn. Bỏ 3, trừ 1 ở 3, 2, 1: còn 2, 1, 0, 1, xếp lại 2, 1, 1, 0.
2. Bỏ 2, trừ 1 ở 1, 1: còn 0, 0, 0. Dựng được.

:::check
Q: Dãy 4, 4, 2, 1, 1 (5 đỉnh) có dựng được không?
A: Không. Hai đỉnh bậc 4 kề mọi đỉnh khác, nên đỉnh nào cũng có bậc ít nhất 2, mâu thuẫn với bậc 1.
:::

## Đường đi, chu trình và liên thông

:::hook
Mạng bị đứt cáp: máy nào còn gửi tin được cho máy nào?
:::

:::figure graph
caption: Ba thành phần liên thông, đỉnh 7 đứng một mình cũng là một. Nối 3 mảnh cần ít nhất 2 cạnh.
size: 200 80
layout: free
node 1 0 0 "1" xanh
node 2 1 1 "2" xanh
node 3 2 0 "3" xanh
node 4 3 1 "4" do
node 5 4 0 "5" do
node 6 5 1 "6" do
node 7 6 0 "7" vang
edge 1 2 xanh
edge 2 3 xanh
edge 4 5 do
edge 5 6 do
edge 4 6 do
:::

:::core
Liên thông là đi được giữa mọi cặp đỉnh; một đồ thị vỡ thành các thành phần liên thông, và đỉnh cô lập cũng là một thành phần.
:::

- Đường đi: dãy đỉnh, hai đỉnh liền nhau kề nhau; độ dài là số cạnh. Đường đi đơn không lặp đỉnh.
- Chu trình: quay về đỉnh đầu, không dùng một cạnh hai lần.
- Có hành trình từ u tới v thì có đường đi đơn: cắt bỏ các vòng lặp.

Đếm thành phần: từ một đỉnh chưa thăm, gom mọi đỉnh tới được; lặp lại. k thành phần cần ít nhất k - 1 cạnh để nối thành một.

> Lỗi thường gặp: quên đỉnh cô lập khi đếm thành phần.

:::check
Q: Cạnh 1-2, 2-3, 3-1, 3-4. Dãy 1, 2, 3, 1 có là chu trình không? Còn 3, 4, 3?
A: 1, 2, 3, 1 là chu trình: ba cạnh khác nhau, về đỉnh đầu. 3, 4, 3 không: dùng cạnh 3-4 hai lần.
:::

### Bao nhiêu cạnh thì chắc chắn liên thông?

Đồ thị không liên thông thì chia đỉnh được thành hai nhóm a và n - a đỉnh, không cạnh nào nối hai nhóm. Nên nó có nhiều nhất C_a^2 + C_(n-a)^2 cạnh, lớn nhất khi một nhóm chỉ có 1 đỉnh.

Ví dụ: tìm số cạnh ít nhất để mọi đồ thị đơn 5 đỉnh đều liên thông.

1. K_4 cộng một đỉnh cô lập: C_4^2 = 6 cạnh mà không liên thông.
2. Chia 2 + 3 đỉnh thì nhiều nhất 1 + 3 = 4 cạnh. Vậy đồ thị không liên thông có nhiều nhất 6 cạnh.
3. Có 7 cạnh là chắc chắn liên thông.

:::check
Q: Đồ thị đơn 9 đỉnh gồm đúng 3 thành phần, thành phần nào cũng là K_3. Cần thêm ít nhất mấy cạnh để liên thông?
A: 3 thành phần thì cần 3 - 1 = 2 cạnh, mỗi cạnh nối hai mảnh.
:::

## Ma trận kề

:::hook
Muốn biết "i và j có nối nhau không", ma trận kề chỉ cần đọc đúng một ô.
:::

:::figure graph
caption: Cạnh 1-2, 1-3, 2-3, 3-4.
size: 90 70
layout: circle
node 1
node 2
node 3 vang
node 4
edge 1 2
edge 1 3
edge 2 3
edge 3 4
:::

:::figure grid
caption: Hàng 3 có ba số 1: đỉnh 3 bậc 3. Bảng đối xứng qua đường chéo.
style: matrix
table "A"
head 1 2 3 4
side 1 2 3 4
row 0 1 1 0
row 1 0 1 0
row 1 1 0 1
row 0 0 1 0
mark row 3 vang
:::

:::core
Ma trận kề là bảng có hay không của mọi cặp đỉnh: ô (i, j) là số cạnh nối i với j, và hàng i cộng lại là bậc của i.
:::

- Vô hướng: ma trận đối xứng. Tổng mọi ô là 2 lần số cạnh.
- Có hướng: ô (i, j) là số cung từ i tới j. Tổng hàng i là số cung đi ra khỏi i, tổng cột j là số cung đi vào j.

> Lỗi thường gặp: với đồ thị có hướng, đọc cung đi vào từ hàng. Hàng là đi ra, cột là đi vào.

:::check
Q: Đồ thị đơn vô hướng có ma trận kề với tổng mọi ô bằng 14. Nó có bao nhiêu cạnh?
A: Mỗi cạnh cho hai số 1, ở (i, j) và (j, i): 14/2 = 7 cạnh.
:::

### Lũy thừa của A đếm hành trình

Ô (i, j) của A^2 cộng a_ik . a_kj qua mọi k: mỗi số hạng bằng 1 khi k kề cả i lẫn j. Vậy nó đếm hành trình độ dài 2 từ i tới j. A^k đếm hành trình độ dài k. Mỗi tam giác cho 6 hành trình khép kín độ dài 3.

$$ (A^2)_{ij} = \sum_{k=1}^{n} a_{ik} a_{kj} $$

Ví dụ: với đồ thị ở trang trước, đếm hành trình độ dài 3 từ 1 tới 4.

1. Dãy 1, a, b, 4: a kề 1, nên a là 2 hoặc 3; b phải kề cả a lẫn 4.
2. Chỉ đỉnh 3 kề 4. a = 2: b = 3 được. a = 3: b = 3 không, vì 3 không kề chính nó.
3. Có 1 hành trình: 1, 2, 3, 4. Đó là ô (1, 4) của A^3.

:::check
Q: Cũng đồ thị đó, ô (1, 2) của A^2 bằng bao nhiêu?
A: Đỉnh kề cả 1 lẫn 2: chỉ có 3. Ô (1, 2) của A^2 bằng 1.
:::

## Danh sách kề và danh sách cạnh

:::hook
Mạng xã hội có tỉ người, mỗi người vài trăm bạn. Ma trận kề cần 10^18 ô, gần như toàn số 0; danh sách kề chỉ ghi những người thật sự là bạn.
:::

:::figure grid
caption: Đồ thị ở trang ma trận kề. Mỗi cạnh có mặt hai lần: tổng độ dài 8 = 2 . 4 cạnh.
table "danh sách kề"
head "u" "Ke(u)"
row 1 "2, 3"
row 2 "1, 3"
row 3 "1, 2, 4"
row 4 "3"
mark cell 3 2 vang
table "danh sách cạnh"
head "cạnh"
row "1-2"
row "1-3"
row "2-3"
row "3-4"
:::

:::core
Danh sách kề ghi cho mỗi đỉnh các đỉnh kề nó: tổng độ dài là tổng các bậc, tức 2m, nên rất gọn khi đồ thị thưa.
:::

$$ n^2 \text{ (ma tran ke)}, \quad n + 2m \text{ (danh sach ke)} $$

Danh sách kề hợp với đồ thị thưa và việc duyệt các đỉnh kề. Ma trận kề hợp với đồ thị dày, hoặc khi cần hỏi nhanh hai đỉnh có kề nhau không.

> Lỗi thường gặp: coi mỗi phần tử danh sách kề vô hướng là một cạnh. Tổng độ dài là 2m.

:::check
Q: Đồ thị vô hướng 1000 đỉnh, 2000 cạnh. Ma trận kề có bao nhiêu ô? Danh sách kề có tổng độ dài bao nhiêu?
A: 1000^2 = 10^6 ô. Danh sách kề: 2 . 2000 = 4000 phần tử, cộng 1000 đầu danh sách.
:::

### Đổi dạng lưu và đồ thị có hướng

Đổi danh sách cạnh sang danh sách kề: tạo n danh sách rỗng, đọc từng cạnh u-v, thêm v vào Ke(u) và u vào Ke(v). Thời gian tỉ lệ với n + m. Với đồ thị có hướng, Ke(u) chỉ ghi các cung đi ra từ u.

Ví dụ: đồ thị có hướng, Ke(1) = 2, 3; Ke(2) = 3; Ke(3) = 1; Ke(4) = 3. Bao nhiêu cung đi vào đỉnh 3?

1. Ke(3) chỉ cho cung đi ra. Cung vào 3 là những lần 3 xuất hiện trong danh sách của đỉnh khác.
2. 3 có trong Ke(1), Ke(2), Ke(4): 3 cung đi vào. Còn cung đi ra khỏi 3 chỉ có 1.

:::check
Q: Đồ thị có hướng: Ke(1) = 3; Ke(2) = 1, 3; Ke(3) = rỗng. Đỉnh 3 có bao nhiêu cung đi ra, bao nhiêu cung đi vào?
A: Đi ra: 0, vì Ke(3) rỗng. Đi vào: 2, vì 3 có trong Ke(1) và Ke(2).
:::
