---
id: tr_lib_t6
title_vi: Tìm kiếm trên đồ thị, đồ thị Euler và Hamilton
subject: toi_uu_roi_rac
floor: 6
format: 2
summary_vi: BFS loang ra từng lớp nên đo được số cạnh ít nhất, DFS đi sâu rồi quay lui; cả hai thăm đúng một thành phần liên thông. Rồi hai câu hỏi đi khắp đồ thị: qua mọi cạnh (Euler, chỉ cần đếm bậc lẻ) và qua mọi đỉnh (Hamilton, không có dấu hiệu gọn).
skills: [tr_t6_bfs, tr_t6_dfs, tr_t6_ung_dung_tim_kiem, tr_t6_euler, tr_t6_hamilton]
---
## Tìm kiếm theo chiều rộng

:::hook
Mạng xã hội gợi ý "bạn của bạn": những người cách bạn đúng hai bước. BFS tìm họ bằng cách loang ra từng vòng, như gợn sóng quanh hòn sỏi ném xuống ao.
:::

:::figure graph
caption: BFS từ 1, màu là lớp: vàng 0, đỏ 1, xanh 2, lục 3. Nét đứt: cạnh không đưa đỉnh mới nào vào.
size: 130 80
layout: free
node 1 0 1 vang
node 2 1 1.5 do
node 3 2 1 xanh
node 4 0 0 do
node 5 1 0 xanh
node 6 2 0 luc
edge 1 2 muc
edge 1 4 muc
edge 2 3 muc
edge 2 5 muc
edge 3 6 muc
edge 4 5 dash
edge 5 6 dash
:::

:::figure grid
caption: Mỗi cột một lượt: lấy đỉnh đầu hàng đợi ra, đưa các đỉnh kề chưa thăm vào cuối.
table
side "lấy ra" "đưa vào" "còn chờ"
row 1 2 4 3 5 6
row "2 4" "3 5" "-" 6 "-" "-"
row "2 4" "4 3 5" "3 5" "5 6" 6 "-"
:::

:::core
Hàng đợi buộc BFS thăm xong mọi đỉnh cách s một cạnh rồi mới tới hai cạnh: lớp của một đỉnh là số cạnh ít nhất từ s tới nó.
:::

1. Đánh dấu s và đưa s vào hàng đợi.
2. Lấy đỉnh u ở đầu hàng đợi ra.
3. Với mỗi đỉnh v kề u (số tăng dần) chưa đánh dấu: đánh dấu v, ghi trước(v) = u, đưa v vào cuối hàng đợi.
4. Lặp lại bước 2 đến khi hàng đợi rỗng.

:::check
Q: Trong hình, lúc lấy 4 ra, vì sao 5 không được đưa vào hàng đợi nữa?
A: 5 đã được đánh dấu ngay lúc lấy 2 ra. BFS đánh dấu khi đưa vào (không đợi lúc lấy ra), nên mỗi đỉnh vào hàng đợi đúng một lần.
:::

### Lớp và đường đi ngắn nhất

Đỉnh lớp d + 1 chỉ vào hàng đợi khi lấy đỉnh lớp d ra, nên khoảng cách theo thứ tự thăm không bao giờ giảm. Lần ngược theo trước(v) từ một đỉnh về s cho đường đi ít cạnh nhất: mỗi bước lùi đúng một lớp.

$$ d(s, v) = d(s, \text{truoc}(v)) + 1 $$

Ví dụ: cùng đồ thị trong hình, chạy BFS từ đỉnh 6.

1. Lấy 6 ra, đưa 3, 5 vào. Lấy 3 ra, đưa 2 vào.
2. Lấy 5 ra: 2 đã đánh dấu, đưa 4 vào. Lấy 2 ra, đưa 1 vào.
3. Thứ tự thăm: 6, 3, 5, 2, 4, 1. Các lớp: {6}, {3, 5}, {2, 4}, {1}.
4. trước(1) = 2, trước(2) = 3, trước(3) = 6: đường 6 - 3 - 2 - 1, đúng 3 cạnh.

> Lỗi thường gặp: đợi đến lúc lấy ra mới đánh dấu, nên một đỉnh vào hàng đợi hai lần; hoặc đưa đỉnh kề vào theo thứ tự tùy thích khi đề đã cố định thứ tự tăng dần.

:::check
Q: Chạy BFS từ đỉnh 3 trên đồ thị trong hình. Thứ tự thăm là gì, và đỉnh 4 cách 3 bao nhiêu cạnh?
A: 3, 2, 6, 1, 5, 4. Các lớp {3}, {2, 6}, {1, 5}, {4}: đỉnh 4 cách 3 ba cạnh.
:::

## Tìm kiếm theo chiều sâu

:::hook
Đi mê cung bằng cách bám tay vào tường: cứ đi sâu mãi, gặp ngõ cụt thì lùi về ngã rẽ gần nhất còn lối chưa đi. Đó chính là DFS.
:::

:::figure graph
caption: DFS từ 1 đi một mạch theo cạnh đỏ, số trên cạnh là thứ tự đi: thứ tự thăm 1, 2, 3, 6, 5, 4. Hai cạnh nét đứt không dùng.
size: 170 95
layout: free
node 1 0 1 vang
node 2 1 1.5
node 3 2 1
node 4 0 0
node 5 1 0
node 6 2 0
edge 1 2 "1" do
edge 2 3 "2" do
edge 3 6 "3" do
edge 6 5 "4" do
edge 5 4 "5" do
edge 1 4 dash
edge 2 5 dash
:::

:::core
DFS luôn đi tiếp sang một đỉnh kề chưa thăm; hết đường thì quay lui về đỉnh đã gọi nó, theo đúng đường đã đi, chứ không nhảy sang chỗ khác.
:::

1. DFS(u): đánh dấu u đã thăm.
2. Với mỗi v kề u (số tăng dần), nếu v chưa thăm thì gọi DFS(v).
3. Hết đỉnh kề chưa thăm thì DFS(u) xong, quay về đỉnh đã gọi nó.

Viết không đệ quy thì thay bằng một ngăn xếp: đỉnh vào sau được xét trước, nên đi sâu trước. Cùng đỉnh xuất phát, BFS (1, 2, 4, 3, 5, 6) và DFS (1, 2, 3, 6, 5, 4) thăm cùng một tập đỉnh, chỉ khác thứ tự.

:::check
Q: Cùng đồ thị, DFS từ đỉnh 3 (đỉnh kề xét tăng dần) thăm theo thứ tự nào?
A: 3, 2, 1, 4, 5, 6: từ 3 sang 2, sang 1, sang 4, sang 5, sang 6, không lần nào phải quay lui.
:::

### Quay lui

:::figure graph
caption: Từ 5 hết đường: lùi về 3, rồi về 1, mới sang 4. Thứ tự thăm 1, 3, 5, 4, 2, 6.
size: 140 85
layout: tree
node 1 vang
node 3
node 4
node 5
node 2
node 6
edge 1 3 "1" do
edge 3 5 "2" do
edge 1 4 "3" do
edge 4 2 "4" do
edge 4 6 "5" do
:::

Đỉnh mới luôn kề với đỉnh sâu nhất trên đường đang đi mà còn đỉnh kề chưa thăm. Dùng điều đó để thử một dãy cho trước có phải thứ tự DFS không, kể cả khi đỉnh kề được xét theo thứ tự bất kỳ.

> Lỗi thường gặp: ở 5 hết đường thì nhảy sang đỉnh chưa thăm nhỏ nhất là 2. Nhưng 2 không kề 5, cũng không kề 3 hay 1: phải lùi về 1 rồi qua 4.

:::check
Q: Đồ thị bậc thang ở trang trước, đỉnh kề xét theo thứ tự bất kỳ. Dãy 1, 2, 5, 4, 3, 6 có thể là thứ tự DFS từ 1 không?
A: Không. Đến 4 thì hết đường, lùi về 5; 5 còn đỉnh kề 6 chưa thăm, nên phải sang 6 trước, không thể sang 3.
:::

## Ứng dụng của tìm kiếm

:::hook
Sau bão, khu dân cư nào còn nối với trạm điện? Chạy một lần duyệt từ trạm điện: khu nào được thăm thì còn điện, khu nào không thì đã bị cắt.
:::

:::figure graph
caption: Duyệt v = 1, ..., 8, gặp đỉnh chưa thăm thì gọi DFS: DFS(1), DFS(2), DFS(5). Ba lần gọi, ba thành phần.
size: 200 80
layout: free
node 1 0 1 vang
node 4 0 0 vang
node 2 1.5 1 do
node 8 2.5 1 do
node 6 1.5 0 do
node 3 2.5 0 do
node 5 4 1 xanh
node 7 4 0 xanh
edge 1 4 vang
edge 2 6 do
edge 2 8 do
edge 3 8 do
edge 5 7 xanh
:::

:::core
Một lần duyệt từ s thăm đúng những đỉnh nối được với s: trọn thành phần liên thông chứa s, không hơn không kém.
:::

- s và t có nối được không: duyệt từ s, xem t có được thăm.
- Đồ thị có liên thông không: một lần duyệt có thăm đủ n đỉnh không.
- Số thành phần liên thông: duyệt v = 1, ..., n, gọi DFS ở đỉnh chưa thăm, đếm số lần gọi.
- Đường đi ít cạnh nhất từ s đến t: BFS từ s rồi lần ngược (trang sau).

:::check
Q: Trong hình, BFS từ đỉnh 3 thăm tất cả bao nhiêu đỉnh? Có đường đi từ 3 đến 7 không?
A: 4 đỉnh: 3, 8, 2, 6, đúng thành phần chứa 3. 7 không được thăm nên không có đường đi từ 3 đến 7.
:::

### Đường đi ít cạnh nhất

:::figure graph
caption: Cây DFS đi từ 1 đến 4 bằng 5 cạnh đỏ; BFS thấy ngay cạnh lục 1 - 4.
size: 130 80
layout: free
node 1 0 1 vang
node 2 1 1.5
node 3 2 1
node 4 0 0 vang
node 5 1 0
node 6 2 0
edge 1 2 do
edge 2 3 do
edge 3 6 do
edge 6 5 do
edge 5 4 do
edge 1 4 luc
edge 2 5 dash
:::

1. Chạy BFS từ s, ghi trước(v) cho mỗi đỉnh được thăm.
2. t không được thăm: không có đường đi, dừng.
3. Từ t đi sang trước(t), trước(trước(t)), ... đến khi gặp s.
4. Đảo ngược dãy vừa được để có đường từ s đến t.

Mỗi đỉnh và mỗi cạnh chỉ được xét vài lần: với n đỉnh, m cạnh, BFS và DFS đều chạy trong thời gian O(n + m).

> Lỗi thường gặp: lấy đường trên cây DFS làm đường ngắn nhất. DFS cho một đường đi, nhưng chỉ BFS bảo đảm ít cạnh nhất.

:::check
Q: Đồ thị trong hình, BFS từ 1. Lần ngược từ 6 được dãy nào, và đường đi ít cạnh nhất từ 1 đến 6 là gì?
A: trước(6) = 3, trước(3) = 2, trước(2) = 1: dãy 6, 3, 2, 1. Đảo lại: 1 - 2 - 3 - 6, ba cạnh.
:::

## Đồ thị Euler

:::hook
Xe quét đường phải chạy qua mỗi con phố đúng một lần rồi về bãi. Có làm được không? Chỉ cần đếm số phố ở mỗi ngã tư.
:::

:::figure graph
caption: Ngôi nhà vẽ một nét: chỉ 3 và 4 bậc lẻ, nên nét vẽ đi từ 3 tới 4 (số là thứ tự cạnh).
size: 100 80
layout: free
node 5 1 2.6
node 4 0 1.6 vang
node 3 2 1.6 vang
node 1 0 0
node 2 2 0
edge 3 5 "1" do
edge 5 4 "2" do
edge 4 1 "3" do
edge 1 2 "4" do
edge 2 3 "5" do
edge 3 4 "6" do
:::

:::core
Đi qua một đỉnh tốn hai cạnh, một vào một ra: chỉ hai đầu nét vẽ được có bậc lẻ.
:::

Với đồ thị liên thông:

- 0 đỉnh lẻ: có chu trình Euler (qua mỗi cạnh một lần, về chỗ cũ);
- đúng 2 đỉnh lẻ: có đường đi Euler (không về), nối hai đỉnh lẻ đó, nhưng không có chu trình.

Ví dụ: đồ thị liên thông 6 đỉnh, bậc 2, 4, 3, 3, 2, 2.

1. Tổng bậc 16, nên có 16/2 = 8 cạnh.
2. Đỉnh 3, 4 bậc lẻ: không có chu trình, có đường đi Euler từ 3 tới 4 (hoặc ngược lại).

> Lỗi thường gặp: chỉ đếm đỉnh bậc lẻ mà quên kiểm tra liên thông. Hai tam giác rời nhau có mọi bậc chẵn nhưng không có chu trình Euler nào đi hết cả sáu cạnh.

:::check
Q: K_n có mọi đỉnh bậc n - 1. K_7 có chu trình Euler không? K_6 thì sao?
A: K_7: bậc 6 chẵn, có. K_6: bậc 5 lẻ ở cả 6 đỉnh, không có chu trình, cũng không có đường đi Euler.
:::

### Ghép chu trình

:::figure graph
caption: Mọi bậc chẵn: đi chu trình xanh 3-1-2-3, còn cạnh thừa ở 3 thì đi tiếp chu trình đỏ 3-4-5-3 và chèn vào.
size: 170 80
layout: free
node 1 0 1
node 2 0 0
node 3 1 0.5 vang
node 4 2 1
node 5 2 0
edge 3 1 xanh
edge 1 2 xanh
edge 2 3 xanh
edge 3 4 do
edge 4 5 do
edge 5 3 do
:::

1. Kiểm tra: liên thông và mọi bậc chẵn.
2. Từ một đỉnh, đi theo cạnh chưa dùng đến khi về chỗ cũ: được chu trình C.
3. Còn cạnh chưa dùng: chọn đỉnh trên C còn cạnh chưa dùng.
4. Từ đó đi một chu trình mới, chèn vào C tại đỉnh ấy.
5. Lặp lại đến khi C dùng hết cạnh. Ở hình: 3-1-2-3-4-5-3.

Thêm một cạnh đổi tính chẵn lẻ của đúng hai đỉnh. Đồ thị có k đỉnh lẻ cần thêm ít nhất k/2 cạnh để có chu trình Euler: ghép các đỉnh lẻ thành từng cặp.

:::check
Q: Đa đồ thị liên thông có 8 đỉnh bậc lẻ. Cần thêm ít nhất bao nhiêu cạnh (được thêm cạnh bội) để có chu trình Euler?
A: Mỗi cạnh sửa được nhiều nhất hai đỉnh lẻ: cần 8/2 = 4 cạnh, ghép 8 đỉnh lẻ thành 4 cặp.
:::

## Đồ thị Hamilton

:::hook
Shipper ghé mỗi khách đúng một lần rồi về kho: lần này là qua mọi đỉnh, và không phép đếm bậc nào trả lời gọn.
:::

:::figure graph
caption: Mọi bậc chẵn nên có chu trình Euler; nhưng bỏ đỉnh 3 thì rời làm hai, nên không có chu trình Hamilton.
size: 120 60
layout: free
node 1 0 1
node 2 0 0
node 3 1 0.5 do
node 4 2 1
node 5 2 0
edge 1 2
edge 1 3
edge 2 3
edge 3 4
edge 3 5
edge 4 5
:::

:::core
Hamilton qua mỗi ĐỈNH một lần, Euler qua mỗi CẠNH. Nói "có" thì chỉ ra chu trình; nói "không" thì tìm vật cản.
:::

Chu trình Hamilton về chỗ cũ, đường đi Hamilton thì không. Vật cản:

- có đỉnh bậc nhỏ hơn 2;
- có đỉnh mà bỏ đi thì đồ thị rời ra: chu trình phải qua nó hai lần;
- đồ thị hai phía có hai phần khác số đỉnh.

:::check
Q: Đồ thị hai phía có một phần 3 đỉnh, phần kia 4 đỉnh, mọi cạnh giữa hai phần đều có. Có chu trình Hamilton không?
A: Không. Chu trình đi xen kẽ hai phần nên dùng số đỉnh hai phần bằng nhau; 3 khác 4.
:::

### Dirac và đếm chu trình

:::figure graph
caption: K_4 có đúng 3 chu trình Hamilton: (4 - 1)!/2 = 3.
size: 300 70
layout: free
node a1 0 1 "1"
node a2 1 1 "2"
node a3 1 0 "3"
node a4 0 0 "4"
node b1 2 1 "1"
node b2 3 1 "2"
node b3 3 0 "3"
node b4 2 0 "4"
node c1 4 1 "1"
node c2 5 1 "2"
node c3 5 0 "3"
node c4 4 0 "4"
edge a1 a2 do
edge a2 a3 do
edge a3 a4 do
edge a4 a1 do
edge b1 b3 do
edge b3 b2 do
edge b2 b4 do
edge b4 b1 do
edge c1 c2 do
edge c2 c4 do
edge c4 c3 do
edge c3 c1 do
:::

Định lý Dirac (điều kiện đủ): đồ thị đơn n >= 3 đỉnh, mọi đỉnh bậc ít nhất n/2, thì có chu trình Hamilton.

Đếm chu trình, coi hai chu trình chỉ khác đỉnh đầu hay chiều đi là một: cố định đỉnh đầu, xếp các đỉnh còn lại, rồi chia 2 cho hai chiều.

$$ K_n: \frac{(n-1)!}{2}, \qquad K_{n,n}: \frac{n!\,(n-1)!}{2} $$

Ví dụ: K_5 có 4!/2 = 12 chu trình. K_(2, 2) có 2! . 1!/2 = 1: chính hình vuông.

> Lỗi thường gặp: dùng Dirac theo chiều ngược. Chu trình 6 đỉnh có mọi bậc 2 < 6/2, mà chính nó là chu trình Hamilton. Không thỏa điều kiện đủ thì chưa kết luận được gì.

:::check
Q: K_6 có bao nhiêu chu trình Hamilton? Nó có thỏa định lý Dirac không?
A: 5!/2 = 60. Mọi bậc là 5 >= 6/2 = 3, nên Dirac cũng bảo đảm có.
:::
