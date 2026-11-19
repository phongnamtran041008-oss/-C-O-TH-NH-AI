---
id: tr_lib_t7
title_vi: Cây, liệt kê cây và bài toán tối ưu trên đồ thị
subject: toi_uu_roi_rac
floor: 7
summary_vi: Cây và các tính chất tương đương của nó, cách dựng và đếm cây khung, rồi ba bài toán tối ưu kinh điển trên đồ thị: cây khung nhỏ nhất, đường đi ngắn nhất và luồng cực đại.
skills: [tr_t7_cay, tr_t7_cay_khung, tr_t7_kruskal_prim, tr_t7_dijkstra, tr_t7_luong]
---
## Cây và tính chất của cây

Cây là đồ thị vô hướng liên thông và không có chu trình. Rừng là đồ thị không có chu trình; mỗi thành phần liên thông của rừng là một cây.

Với đồ thị đơn G có n đỉnh, các điều sau tương đương (mỗi điều đều nói G là cây):

- G liên thông và không có chu trình.
- G liên thông và có đúng n - 1 cạnh.
- G không có chu trình và có đúng n - 1 cạnh.
- Giữa hai đỉnh bất kỳ của G có đúng một đường đi.
- G liên thông, và bỏ đi bất kỳ cạnh nào thì G mất liên thông.

$$ \text{cay } n \text{ dinh} \Rightarrow m = n - 1, \quad \text{rung } n \text{ dinh}, k \text{ cay} \Rightarrow m = n - k $$

Mọi cây có ít nhất hai đỉnh đều có ít nhất hai lá: hai đầu của một đường đi dài nhất là lá. Bỏ một lá khỏi cây được một cây nhỏ hơn, nên nhiều chứng minh về cây đi bằng quy nạp theo số đỉnh.

Ví dụ: một cây có 2 đỉnh bậc 4, 3 đỉnh bậc 3, còn lại là lá. Gọi L là số lá; cây có 5 + L đỉnh và 4 + L cạnh. Định lý bắt tay: 8 + 9 + L = 2(4 + L), nên L = 9 và cây có 14 đỉnh.

> Lỗi thường gặp: thấy n đỉnh và n - 1 cạnh là kết luận ngay "cây". Phải biết thêm đồ thị liên thông hoặc không có chu trình: tam giác 1-2-3 cùng một đỉnh 4 đứng riêng có 4 đỉnh, 3 cạnh mà không phải cây.

## Cây khung và liệt kê cây

Cây khung của đồ thị liên thông G là một cây chứa mọi đỉnh của G, dùng một phần các cạnh của G. Đồ thị liên thông n đỉnh, m cạnh phải bỏ đúng m - n + 1 cạnh để còn một cây khung; đồ thị có k thành phần liên thông có rừng khung n - k cạnh.

Dựng cây khung bằng BFS hoặc DFS: mỗi lần một đỉnh mới được thăm từ đỉnh u, giữ lại cạnh nối nó với u. Khi đã cố định thứ tự xét các đỉnh kề (ví dụ tăng dần), cây khung BFS và cây khung DFS là duy nhất, nhưng thường khác nhau.

Đếm cây khung:

- K_n có n^(n - 2) cây khung (công thức Cayley); chu trình n đỉnh có n cây khung; một cây chỉ có chính nó.
- Định lý Kirchhoff: số cây khung N(G) bằng định thức của ma trận Laplace L = D - A (D là ma trận bậc, A là ma trận kề) sau khi bỏ một hàng và cột cùng chỉ số.
- Hai phần chỉ chung nhau một đỉnh: số cây khung là tích số cây khung của hai phần.

$$ N(K_n) = n^{n-2}, \quad N(G) = \text{det} \, L' $$

Ví dụ: hai tam giác 1-2-3 và 3-4-5 chung đỉnh 3. Mỗi tam giác phải bỏ đúng một cạnh, nên có 3 . 3 = 9 cây khung. Với ma trận Laplace của K_4 bỏ hàng 1 cột 1:

:::matrix
L = 3 -1 -1 ; -1 3 -1 ; -1 -1 3
:::

định thức bằng 16 = 4^2, đúng như công thức Cayley.

> Lỗi thường gặp: đếm số cách chọn n - 1 cạnh (C_m^(n - 1)) rồi quên loại các cách còn chu trình. Với hai tam giác chung đỉnh có C_6^4 = 15 cách chọn 4 cạnh, nhưng 6 cách giữ nguyên một tam giác nên chỉ 9 cách là cây.

## Cây khung nhỏ nhất

Cho đồ thị liên thông có trọng số trên cạnh. Cây khung nhỏ nhất là cây khung có tổng trọng số nhỏ nhất. Hai thuật toán tham lam đều cho đáp án đúng:

1. Kruskal: sắp các cạnh theo trọng số tăng dần; lần lượt nhận một cạnh nếu nó không tạo chu trình với các cạnh đã nhận (hai đầu đang ở hai cây khác nhau của rừng); dừng khi đủ n - 1 cạnh.
2. Prim: bắt đầu từ một đỉnh; mỗi bước thêm cạnh nhẹ nhất nối một đỉnh đã ở trong cây với một đỉnh ngoài cây.

Vì sao đúng (tính chất lát cắt): chia các đỉnh thành hai phần bất kỳ, cạnh nhẹ nhất nối hai phần luôn thuộc một cây khung nhỏ nhất; nếu một cây khung không chứa nó, đổi cạnh đó lấy một cạnh nặng hơn trên chu trình tạo thành sẽ được cây nhẹ hơn. Khi mọi trọng số đôi một khác nhau, cây khung nhỏ nhất là duy nhất, và Kruskal, Prim cho cùng một cây.

$$ w(T) = \sum_{e \in T} w(e) \to \min $$

Ví dụ: các cạnh 1-2 (4), 1-3 (2), 2-3 (5), 2-4 (10), 3-4 (9), 3-5 (3), 4-5 (7), 4-6 (6), 5-6 (8). Kruskal nhận 1-3, 3-5, 1-2, bỏ 2-3 (tạo chu trình 1-2-3), nhận 4-6, 4-5 và dừng: tổng 22, cạnh nhận cuối 4-5 (7). Prim từ 1 thêm các đỉnh theo thứ tự 1, 3, 5, 2, 4, 6 và ra đúng cây đó.

> Lỗi thường gặp: nhận một cạnh chỉ vì nó có một đầu "mới". Kruskal kiểm tra hai đầu có đang nối với nhau chưa; một cạnh nối hai đỉnh đã cùng một cây khép một chu trình và phải bỏ, dù trọng số của nó nhỏ.

## Đường đi ngắn nhất

Bài toán: tìm độ dài d(s, v) của đường đi ngắn nhất từ đỉnh s đến mọi đỉnh v, khi mọi trọng số không âm. Thuật toán Dijkstra giữ một nhãn d(v) cho mỗi đỉnh:

1. d(s) = 0, mọi nhãn khác bằng vô cùng; chưa đỉnh nào được cố định.
2. Chọn đỉnh u chưa cố định có nhãn nhỏ nhất và cố định nó: d(u) đã là khoảng cách đúng.
3. Với mỗi đỉnh v kề u chưa cố định, nếu d(u) + w(u, v) < d(v) thì giảm d(v) và ghi trước(v) = u.
4. Lặp lại bước 2 cho đến khi mọi đỉnh được cố định; lần ngược theo trước(v) để có đường đi.

$$ d(v) := \min( d(v), \, d(u) + w(u, v) ) $$

Bước 2 đúng vì trọng số không âm: mọi đường khác đến u phải rời tập đã cố định ở một đỉnh có nhãn không nhỏ hơn d(u), rồi chỉ dài thêm.

Ví dụ: các cạnh 1-2 (7), 1-3 (2), 2-3 (4), 2-4 (1), 3-4 (8), 3-5 (10), 4-5 (3), 4-6 (9), 5-6 (2). Từ 1, các đỉnh được cố định theo thứ tự 1 (0), 3 (2), 2 (6), 4 (7), 5 (10), 6 (12); đường đi ngắn nhất đến 6 là 1 - 3 - 2 - 4 - 5 - 6.

> Lỗi thường gặp: dùng Dijkstra khi có trọng số âm. Với các cung 1->2 (2), 1->3 (4), 3->2 (-4), Dijkstra cố định d(2) = 2 trong khi đường 1->3->2 chỉ dài 0. Khi có trọng số âm phải dùng thuật toán khác (Bellman-Ford). Cũng sai khi nghĩ cộng cùng một số vào mọi trọng số không đổi đường ngắn nhất: đường nhiều cạnh bị cộng nhiều hơn.

## Luồng cực đại

Mạng là đồ thị có hướng với đỉnh phát s, đỉnh thu t, mỗi cung u->v có khả năng thông qua c(u, v). Luồng gán cho mỗi cung một lượng từ 0 đến c(u, v), sao cho ở mỗi đỉnh khác s, t lượng vào bằng lượng ra. Giá trị luồng là lượng rời s.

Lát cắt (S, T) chia các đỉnh thành hai phần với s thuộc S, t thuộc T; khả năng thông qua của nó là tổng c(u, v) trên các cung đi từ S sang T. Mọi luồng không vượt mọi lát cắt, và định lý Ford-Fulkerson nói thêm:

$$ \max \text{ gia tri luong} = \min \text{ kha nang thong qua lat cat} $$

Thuật toán đường tăng luồng:

1. Bắt đầu với luồng 0.
2. Trên mạng thặng dư (cung u->v còn c - f, cung ngược v->u bằng f), tìm một đường từ s đến t.
3. Tăng luồng dọc đường đó thêm lượng nhỏ nhất còn lại trên đường; lặp lại.
4. Khi không còn đường, các đỉnh còn tới được từ s tạo thành S của một lát cắt hẹp nhất.

Ví dụ: cung 1->2 (3), 1->3 (2), 2->3 (3), 2->4 (2), 3->4 (3), s = 1, t = 4. Đẩy 3 theo 1->2->3->4; mạng thặng dư còn đường 1->3->2->4 qua cung ngược 3->2, tăng thêm 2. Luồng 5 bằng lát cắt S = {1}, nên là cực đại.

> Lỗi thường gặp: quên các cung ngược trong mạng thặng dư. Không có chúng, ở ví dụ trên ta dừng ở 3 và tưởng đã cực đại; cung ngược cho phép "rút lại" luồng đã đẩy sai chỗ.
