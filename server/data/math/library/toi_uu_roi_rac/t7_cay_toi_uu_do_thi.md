---
id: tr_lib_t7
title_vi: Cây, liệt kê cây và bài toán tối ưu trên đồ thị
subject: toi_uu_roi_rac
floor: 7
format: 2
summary_vi: Cây là bộ khung liên thông không thừa một cạnh (n đỉnh, n - 1 cạnh). Từ đó: dựng và đếm cây khung, chọn cây khung rẻ nhất bằng tham lam (Kruskal, Prim), tìm đường ngắn nhất bằng nhãn (Dijkstra), và đẩy luồng lớn nhất qua lát cắt hẹp nhất.
skills: [tr_t7_cay, tr_t7_cay_khung, tr_t7_kruskal_prim, tr_t7_dijkstra, tr_t7_luong]
---
## Cây và tính chất của cây

:::hook
Cây thư mục trên máy tính: từ gốc tới mỗi tệp có đúng một đường dẫn. Thêm một lối tắt vòng là có chu trình; cắt một nhánh là cả cụm thư mục rời ra.
:::

:::figure graph
caption: Giữa 4 và 7 chỉ có một đường đi (đỏ). Các lá 4, 5, 6, 7 có bậc 1.
size: 140 75
layout: tree
node 1
node 2
node 3
node 4 vang
node 5 vang
node 6 vang
node 7 vang
edge 1 2 do
edge 1 3 do
edge 2 4 do
edge 2 5
edge 3 6
edge 3 7 do
:::

:::core
Cây là đồ thị liên thông vừa đủ: thêm một cạnh là có chu trình, bớt một cạnh là rời ra.
:::

Đồ thị đơn n đỉnh là cây khi và chỉ khi có một trong các điều:

- liên thông và không có chu trình;
- có n - 1 cạnh, và liên thông hoặc không có chu trình;
- giữa hai đỉnh bất kỳ có đúng một đường đi;
- liên thông, và bỏ cạnh nào cũng mất liên thông.

Rừng (không chu trình) gồm k cây, n đỉnh thì có n - k cạnh.

> Lỗi thường gặp: thấy n - 1 cạnh là kết luận "cây". Tam giác 1-2-3 cùng đỉnh 4 đứng riêng có 4 đỉnh, 3 cạnh.

:::check
Q: Một rừng có 20 đỉnh và 16 cạnh. Nó gồm mấy cây, và cần thêm ít nhất mấy cạnh để thành một cây?
A: 16 = 20 - k nên k = 4 cây. Mỗi cạnh nối hai cây giảm số cây đi 1: cần 3 cạnh (cây 20 đỉnh có 19 = 16 + 3 cạnh).
:::

### Đếm lá bằng định lý bắt tay

:::figure graph
caption: Số trong mỗi đỉnh là bậc: một đỉnh bậc 4, hai đỉnh bậc 3, còn lại là lá. Đếm được 6 lá, 9 đỉnh.
size: 170 80
layout: tree
node a "4" vang
node b "3" xanh
node c "3" xanh
node l1 "1"
node l2 "1"
node l3 "1"
node l4 "1"
node l5 "1"
node l6 "1"
edge a b
edge a c
edge a l1
edge a l2
edge b l3
edge b l4
edge c l5
edge c l6
:::

Hai sự thật đủ để đếm: cây n đỉnh có n - 1 cạnh, và tổng bậc bằng hai lần số cạnh. Mọi cây có ít nhất 2 đỉnh đều có ít nhất hai lá: hai đầu của một đường đi dài nhất. Bỏ một lá được cây nhỏ hơn, nên nhiều chứng minh về cây đi bằng quy nạp theo số đỉnh.

Ví dụ: cây có 1 đỉnh bậc 4, 2 đỉnh bậc 3, còn lại là lá. Gọi L là số lá.

1. Số đỉnh 3 + L, số cạnh 2 + L.
2. Tổng bậc: 4 + 3 . 2 + L = 10 + L.
3. Bắt tay: 10 + L = 2(2 + L), nên L = 6 và cây có 9 đỉnh.

:::check
Q: Cây có 3 đỉnh bậc 3, còn lại là lá. Có bao nhiêu lá?
A: Số đỉnh 3 + L, cạnh 2 + L. Tổng bậc 9 + L = 2(2 + L), nên L = 5.
:::

## Cây khung và liệt kê cây

:::hook
Nối mạng cho 6 phòng: cần mọi phòng thông nhau mà không thừa dây nào. Đó là một cây khung: giữ đủ đỉnh, bỏ bớt cạnh đến khi hết chu trình.
:::

:::figure graph
caption: Cây khung BFS từ 1 (lục): mỗi đỉnh giữ cạnh đã đưa nó vào hàng đợi. 8 cạnh, giữ 5, bỏ 3 (nét đứt).
size: 160 85
layout: free
node 1 0 1 vang
node 2 1 2
node 3 1 0
node 4 2 2
node 5 2 0
node 6 3 1
edge 1 2 luc
edge 1 3 luc
edge 2 4 luc
edge 3 5 luc
edge 4 6 luc
edge 2 3 dash
edge 4 5 dash
edge 5 6 dash
:::

:::core
Cây khung là cây chứa mọi đỉnh và chỉ dùng cạnh của đồ thị. Đồ thị liên thông n đỉnh, m cạnh phải bỏ đúng m - n + 1 cạnh.
:::

Đồ thị có k thành phần liên thông thì giữ một rừng khung n - k cạnh, bỏ m - (n - k) cạnh. Dựng bằng BFS hay DFS: mỗi lần thăm đỉnh mới từ u, giữ cạnh nối nó với u. Thứ tự xét đỉnh kề đã cố định thì cây BFS và cây DFS là duy nhất, nhưng thường khác nhau.

> Lỗi thường gặp: nghĩ cạnh nào nối hai đỉnh kề nhau cũng vào cây BFS. Ở hình, 5 được đưa vào từ 3 trước khi xét 4, nên cạnh 4-5 bị bỏ.

:::check
Q: Cùng đồ thị trong hình, DFS từ 1 (đỉnh kề xét tăng dần) cho cây khung nào?
A: 1 sang 2, sang 3, sang 5, sang 4, sang 6: cây 1-2, 2-3, 3-5, 5-4, 4-6. Khác cây BFS.
:::

### Đếm cây khung

:::matrix
L = 3 -1 -1 ; -1 3 -1 ; -1 -1 3
:::

Ma trận Laplace L = D - A: bậc trên đường chéo, -1 ở mỗi cặp đỉnh kề. Bỏ một hàng và cột cùng chỉ số, định thức còn lại là số cây khung (định lý Kirchhoff). Với K_4 bỏ hàng 1 cột 1 (trên), định thức bằng 16.

$$ N(K_n) = n^{n-2}, \quad N(G) = \text{det} \, L' $$

- Chu trình n đỉnh: bỏ một trong n cạnh, có n cây khung. Một cây: chỉ chính nó.
- Hai phần chỉ chung một đỉnh: nhân số cây khung của hai phần.
- K_n bỏ một cạnh: mỗi cạnh nằm trong n^(n-2)(n-1)/C(n,2) cây; trừ đi. K_4: 16 - 16 . 3/6 = 8.

> Lỗi thường gặp: đếm cách chọn n - 1 cạnh mà quên loại cách còn chu trình.

:::check
Q: Một tam giác và một hình vuông chung đúng một đỉnh. Đồ thị có bao nhiêu cây khung?
A: Tam giác có 3 cây khung, hình vuông (chu trình 4 đỉnh) có 4; chung một đỉnh nên nhân: 3 . 4 = 12.
:::

## Cây khung nhỏ nhất

:::hook
Kéo cáp quang nối 6 làng, mỗi đoạn có giá riêng. Mạng phải thông mà rẻ nhất: chọn cây khung có tổng trọng số nhỏ nhất.
:::

:::figure graph
caption: Kruskal nhận 5 cạnh đỏ, tổng 17; cạnh 1-3 và 2-4 (nét đứt) bị bỏ.
size: 170 90
layout: free
node 1 0 1
node 2 1 1.5
node 3 1 0
node 4 2 2
node 5 2 0
node 6 3 1
edge 5 6 1 do
edge 3 4 2 do
edge 1 2 3 do
edge 2 3 4 do
edge 3 5 7 do
edge 1 3 5 dash
edge 2 4 6 dash
edge 4 5 8
edge 4 6 9
:::

:::figure grid
caption: Kruskal xét cạnh theo trọng số tăng dần, đủ 5 cạnh thì dừng.
table
row 5-6 3-4 1-2 2-3 1-3 2-4 3-5
row 1 2 3 4 5 6 7
row nhận nhận nhận nhận bỏ bỏ nhận
mark col 5 do
mark col 6 do
:::

:::core
Cạnh rẻ nhất nối hai phần bất kỳ của tập đỉnh luôn nằm trong một cây khung nhỏ nhất: vì thế tham lam đúng.
:::

Kruskal: xét cạnh theo trọng số tăng dần; nhận cạnh nếu hai đầu đang ở hai cây khác nhau của rừng đang xây, bỏ nếu nó khép chu trình; dừng khi đủ n - 1 cạnh.

Ở hình, 1-3 (5) bị bỏ vì 1 và 3 đã nối qua 1-2-3; 2-4 (6) bỏ vì đã có 2-3-4. Còn 3-5 (7) nối {5, 6} với phần còn lại nên được nhận.

> Lỗi thường gặp: nhận cạnh chỉ vì nó có một đầu "mới".

:::check
Q: Nếu trọng số cạnh 1-3 giảm từ 5 xuống 2.5, cạnh nào bị bỏ đầu tiên, và tổng mới là bao nhiêu?
A: 5-6, 3-4, 1-3, 1-2 đều được nhận. 2-3 (4) khép chu trình 1-2-3 nên bị bỏ đầu tiên. Rồi 2-4 bỏ, 3-5 nhận: tổng 1 + 2 + 2.5 + 3 + 7 = 15.5.
:::

### Prim và vì sao tham lam đúng

Prim mọc một cây từ một đỉnh: mỗi bước thêm cạnh nhẹ nhất nối một đỉnh trong cây với một đỉnh ngoài cây.

Ví dụ: Prim từ đỉnh 6 trên đồ thị trang trước.

1. Từ {6}: 6-5 (1) nhẹ nhất, thêm 5.
2. Từ {5, 6}: các cạnh ra ngoài 3-5 (7), 4-5 (8), 4-6 (9): thêm 3.
3. Rồi 3-4 (2) thêm 4, 2-3 (4) thêm 2, 1-2 (3) thêm 1.
4. Thứ tự 6, 5, 3, 4, 2, 1; tổng 17, đúng cây Kruskal.

Vì sao đúng: nếu một cây khung không chứa cạnh rẻ nhất e qua một lát cắt, thêm e tạo chu trình đi qua lát cắt ở một cạnh f đắt hơn; đổi f lấy e được cây rẻ hơn. Khi mọi trọng số khác nhau, cây khung nhỏ nhất là duy nhất, nên Kruskal và Prim từ bất kỳ đỉnh nào cho cùng một cây.

:::check
Q: Prim từ đỉnh 1 trên cùng đồ thị thêm các đỉnh theo thứ tự nào?
A: 1, 2 (qua 1-2, 3), 3 (qua 2-3, 4), 4 (qua 3-4, 2), 5 (qua 3-5, 7), 6 (qua 5-6, 1). Tổng vẫn 17.
:::

## Đường đi ngắn nhất

:::hook
Bản đồ tìm đường nhanh nhất qua các ngã tư: Dijkstra mở rộng dần vùng "đã chắc chắn" quanh điểm xuất phát.
:::

:::figure graph
caption: Đường ngắn nhất từ 1 tới mỗi đỉnh (đỏ): đến 6 là 1-3-2-4-5-6, dài 13.
size: 160 90
layout: free
node 1 0 1 vang
node 2 1 1.5
node 3 1 0
node 4 2 2
node 5 2 0
node 6 3 1
edge 1 3 1 do
edge 3 2 2 do
edge 2 4 5 do
edge 4 5 2 do
edge 5 6 3 do
edge 1 2 4
edge 3 4 8
edge 3 5 10
edge 4 6 6
:::

:::figure grid
caption: Nhãn sau mỗi lần cố định (ô vàng); cuối cùng cố định 6 với nhãn 13.
table
head 1 2 3 4 5 6
row 0 4 1 - - -
row 0 3 1 9 11 -
row 0 3 1 8 11 -
row 0 3 1 8 10 14
row 0 3 1 8 10 13
mark cell 1 1 vang
mark cell 2 3 vang
mark cell 3 2 vang
mark cell 4 4 vang
mark cell 5 5 vang
:::

:::core
Đỉnh chưa cố định có nhãn nhỏ nhất đã có khoảng cách đúng: trọng số không âm nên đi vòng chỉ dài thêm.
:::

1. d(s) = 0, mọi nhãn khác là vô cùng. Cố định đỉnh u chưa cố định có nhãn nhỏ nhất.
2. Với v kề u chưa cố định: nếu d(u) + w(u, v) < d(v) thì giảm d(v), ghi trước(v) = u.
3. Lặp lại đến khi mọi đỉnh cố định; lần ngược trước(v) để có đường đi.

:::check
Q: Trong bảng, lúc cố định 4 (nhãn 8), vì sao nhãn của 5 giảm từ 11 xuống 10?
A: Qua 4: 8 + w(4, 5) = 8 + 2 = 10 < 11 (nhãn cũ đi qua 3: 1 + 10). Ghi trước(5) = 4.
:::

### Khi nào Dijkstra sai

Dijkstra chỉ đúng khi mọi trọng số không âm. Với các cung 1->2 (3), 1->3 (5), 3->2 (-4), Dijkstra cố định d(2) = 3, trong khi đường 1->3->2 chỉ dài 1. Có trọng số âm thì dùng thuật toán khác, như Bellman-Ford.

Cộng cùng một số c vào mọi cạnh cũng làm đổi đường ngắn nhất: đường k cạnh dài thêm k . c, nên đường nhiều cạnh bị phạt nặng hơn.

Ví dụ: cạnh 1-2 (2), 2-3 (2), 1-3 (5).

1. Ngắn nhất từ 1 đến 3: 1-2-3, dài 4 (so với 5).
2. Cộng c = 3 vào mọi cạnh: 1-2-3 dài 10, còn 1-3 dài 8.
3. Đường ngắn nhất đổi thành 1-3.

> Lỗi thường gặp: cố định đỉnh theo số thứ tự. Ở bảng, 3 (nhãn 1) được cố định trước 2.

:::check
Q: Dijkstra từ đỉnh 6 trên đồ thị trang trước: khoảng cách tới 1 là bao nhiêu, đi đường nào?
A: Cố định 6 (0), 5 (3), 4 (5), 2 (10), 3 (12), 1 (13). Đến 1 dài 13: 6-5-4-2-3-1.
:::

## Luồng cực đại

:::hook
Đường ống dẫn linh khí từ mỏ (1) về tông môn (5), mỗi đoạn ống chỉ chịu được một lưu lượng. Tối đa chuyển được bao nhiêu mỗi giờ? Chỗ hẹp nhất quyết định.
:::

:::figure graph
caption: Nhãn là luồng/khả năng. Lát cắt quanh đỉnh 5 chỉ có cung đỏ 3->5 (2) và 4->5 (6): luồng 8 đã chạm trần 8.
size: 190 90
layout: free
directed: yes
node 1 0 1 vang
node 2 1 1.6
node 3 1 0
node 4 2 2
node 5 3 1 luc
edge 1 2 "4/5"
edge 1 3 "4/4"
edge 2 3 "1/2"
edge 2 4 "3/3"
edge 3 4 "3/4"
edge 3 5 "2/2" do
edge 4 5 "6/6" do
:::

:::core
Luồng không thể vượt khả năng của bất kỳ lát cắt nào; và luồng cực đại đúng bằng lát cắt hẹp nhất (Ford-Fulkerson).
:::

Mạng: đồ thị có hướng, phát s, thu t, cung u->v chịu tối đa c(u, v). Luồng gán mỗi cung một lượng từ 0 đến c, ở mỗi đỉnh khác s, t vào bằng ra; giá trị luồng là lượng rời s. Lát cắt (S, T) có s thuộc S, t thuộc T; khả năng của nó là tổng c trên các cung đi từ S sang T (cung đi ngược từ T về S không tính).

:::check
Q: Trong hình, lát cắt S = {1}, rồi S = {1, 2}, có khả năng bao nhiêu? Lát cắt nào hẹp nhất?
A: S = {1}: 5 + 4 = 9. S = {1, 2}: 1->3 (4), 2->3 (2), 2->4 (3), tổng 9. Hẹp nhất là S = {1, 2, 3, 4}: 2 + 6 = 8, bằng luồng.
:::

### Đường tăng luồng và cung ngược

:::figure graph
caption: Luồng 5, không còn đường đi xuôi. Đường đỏ 1->3->2->4 đi ngược cung 2->3 (nét đứt): bớt 1 trên 2->3, luồng thành 6.
size: 160 80
layout: free
directed: yes
node 1 0 1 vang
node 2 1 1.6
node 3 1 0
node 4 2 1 luc
edge 1 2 "4/4"
edge 1 3 "1/3" do
edge 2 3 "3/3" do dash
edge 2 4 "1/2" do
edge 3 4 "4/4"
:::

1. Bắt đầu với luồng 0.
2. Mạng thặng dư: cung u->v còn c - f; cung ngược v->u bằng f (có thể rút lại).
3. Tìm một đường từ s tới t trên mạng thặng dư; tăng luồng thêm lượng nhỏ nhất còn lại dọc đường.
4. Hết đường thì dừng: các đỉnh còn tới được từ s là S của lát cắt hẹp nhất.

Ở hình, đẩy 3 theo 1-2-3-4, rồi 1 theo 1-2-4, 1 theo 1-3-4: được 5 và kẹt. Cung ngược 3->2 mở thêm 1, đạt 6 = lát cắt quanh 4 (2 + 4).

> Lỗi thường gặp: quên cung ngược, dừng ở 5 và tưởng đã cực đại.

:::check
Q: Sau khi đạt 6, đỉnh nào còn tới được từ 1 trên mạng thặng dư, và lát cắt tương ứng là gì?
A: 1->2 đầy, 1->3 còn 1: tới 3. Từ 3: 3->4 đầy, cung ngược 3->2 còn 2: tới 2. Từ 2: 2->4 đầy. S = {1, 2, 3}, cắt 2->4 (2) và 3->4 (4): 6.
:::
