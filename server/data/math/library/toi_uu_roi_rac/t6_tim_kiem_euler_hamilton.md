---
id: tr_lib_t6
title_vi: Tìm kiếm trên đồ thị, đồ thị Euler và Hamilton
subject: toi_uu_roi_rac
floor: 6
summary_vi: Hai cách đi khắp một đồ thị (theo chiều rộng và theo chiều sâu), những bài toán chúng giải được, và hai câu hỏi cổ điển: đi qua mọi cạnh, đi qua mọi đỉnh.
skills: [tr_t6_bfs, tr_t6_dfs, tr_t6_ung_dung_tim_kiem, tr_t6_euler, tr_t6_hamilton]
---
## Tìm kiếm theo chiều rộng

BFS (tìm kiếm theo chiều rộng) từ đỉnh s dùng một hàng đợi: đỉnh vào trước được lấy ra trước. Để thứ tự thăm là duy nhất, các đỉnh kề luôn được xét theo thứ tự số tăng dần.

1. Đánh dấu s đã thăm và đưa s vào hàng đợi.
2. Lấy đỉnh u ở đầu hàng đợi ra.
3. Với mỗi đỉnh v kề u chưa thăm: đánh dấu v, ghi trước(v) = u, đưa v vào cuối hàng đợi.
4. Lặp lại từ bước 2 cho đến khi hàng đợi rỗng.

BFS thăm các đỉnh theo từng lớp: s, rồi các đỉnh cách s một cạnh, rồi hai cạnh, ... Khoảng cách d(s, v), số cạnh ít nhất của một đường đi từ s đến v, thỏa:

$$ d(s, v) = d(s, \text{truoc}(v)) + 1 $$

Ví dụ: các đỉnh 1..7, các cạnh 1-3, 1-4, 2-5, 2-7, 3-5, 3-6, 4-6, 5-7, 6-7. BFS từ 2 thăm 2, 5, 7, 3, 6, 1, 4; các lớp là {2}, {5, 7}, {3, 6}, {1, 4}. Lần ngược trước(4) = 6, trước(6) = 7, trước(7) = 2 được đường đi ngắn nhất 2 - 7 - 6 - 4.

> Lỗi thường gặp: đưa đỉnh vào hàng đợi mà quên đánh dấu ngay, nên một đỉnh vào hàng đợi hai lần; hoặc thêm các đỉnh kề theo thứ tự tùy ý khi đề đã cố định thứ tự tăng dần.

## Tìm kiếm theo chiều sâu

DFS (tìm kiếm theo chiều sâu) đi xa nhất có thể rồi mới quay lui:

1. DFS(u): đánh dấu u đã thăm.
2. Với mỗi đỉnh v kề u (theo thứ tự tăng dần), nếu v chưa thăm thì gọi DFS(v).
3. Hết đỉnh kề chưa thăm thì DFS(u) kết thúc, quay về đỉnh đã gọi nó.

Viết không đệ quy thì dùng ngăn xếp: đỉnh vào sau được xét trước.

Ví dụ: cùng đồ thị trên, DFS từ 4 thăm 4, 1, 3, 5, 2, 7, 6. Từ 4 sang 1, từ 1 sang 3, từ 3 sang 5, từ 5 sang 2, từ 2 sang 7, từ 7 sang 6.

Với cùng đỉnh xuất phát, BFS và DFS thăm cùng một tập đỉnh (thành phần liên thông chứa s), chỉ khác thứ tự.

> Lỗi thường gặp: khi một đỉnh hết đỉnh kề chưa thăm, nhảy sang đỉnh chưa thăm nhỏ nhất của cả đồ thị. DFS phải quay lui theo đường đã đi; ví dụ với các cạnh 1-2, 1-5, 2-3, 4-5, 4-6, DFS từ 1 thăm 1, 2, 3, rồi quay về 1 để sang 5, 4, 6, chứ không nhảy từ 3 sang 4.

## Ứng dụng của tìm kiếm

- Hai đỉnh s, t có nối được không: chạy BFS hoặc DFS từ s, xem t có được thăm không.
- Đếm thành phần liên thông: duyệt v = 1, ..., n, gặp đỉnh chưa thăm thì gọi DFS(v); số lần gọi là số thành phần.
- Đồ thị có liên thông không: một lần duyệt có thăm đủ n đỉnh không.
- Đường đi ít cạnh nhất từ s đến t: chạy BFS từ s, lần ngược từ t theo trước(v) đến s, rồi đảo ngược dãy.

Mỗi đỉnh và mỗi cạnh được xét một số lần không đổi, nên với danh sách kề, BFS và DFS chạy trong thời gian:

$$ O(n + m) $$

Ví dụ: các đỉnh 1..9, các cạnh 1-5, 2-6, 3-7, 5-9, 6-8. Vòng duyệt gọi DFS(1), DFS(2), DFS(3), DFS(4): có 4 thành phần {1, 5, 9}, {2, 6, 8}, {3, 7}, {4}.

> Lỗi thường gặp: lấy đường đi trên cây DFS làm đường đi ngắn nhất. Cây DFS cho một đường đi, nhưng không nhất thiết ít cạnh nhất: chỉ BFS mới bảo đảm điều đó.

## Đồ thị Euler

Chu trình Euler đi qua mỗi cạnh đúng một lần rồi trở về đỉnh xuất phát; đường đi Euler đi qua mỗi cạnh đúng một lần, không cần trở về.

Định lý Euler, cho đồ thị vô hướng liên thông (bỏ qua các đỉnh cô lập):

- Có chu trình Euler khi và chỉ khi mọi đỉnh có bậc chẵn.
- Có đường đi Euler mà không có chu trình Euler khi và chỉ khi có đúng hai đỉnh bậc lẻ; khi đó mọi đường đi Euler bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia.

$$ \text{so dinh bac le} = 0 \Rightarrow \text{chu trinh Euler}, \quad = 2 \Rightarrow \text{duong di Euler} $$

Lý do: mỗi lần đi qua một đỉnh ở giữa, ta dùng hai cạnh của nó, một vào một ra.

Ví dụ: đồ thị liên thông 6 đỉnh với các bậc 2, 3, 4, 4, 3, 2 có 18/2 = 9 cạnh, không có chu trình Euler, và mọi đường đi Euler bắt đầu ở đỉnh 2 hoặc đỉnh 5. K_n có chu trình Euler khi và chỉ khi n lẻ.

Tìm chu trình Euler bằng cách ghép chu trình: đi một chu trình C bằng các cạnh chưa dùng; nếu còn cạnh chưa dùng, từ một đỉnh trên C đi một chu trình mới và chèn vào C; lặp lại.

> Lỗi thường gặp: nhầm Euler với Hamilton. Euler nói về cạnh, Hamilton nói về đỉnh. Chu trình 1-2-3-4-5-1 đi qua mọi đỉnh của đồ thị có thêm cạnh 1-3 là chu trình Hamilton, nhưng không phải chu trình Euler vì bỏ sót cạnh 1-3.

## Đồ thị Hamilton

Chu trình Hamilton đi qua mỗi đỉnh đúng một lần rồi trở về đỉnh đầu; đường đi Hamilton không cần trở về. Khác với Euler, không có điều kiện đơn giản nào vừa cần vừa đủ: thường phải thử bằng quay lui.

Điều kiện cần (dùng để chứng minh không có): mọi đỉnh có bậc ít nhất 2; không có đỉnh nào mà bỏ nó đi đồ thị rời ra; đồ thị hai phía thì hai phần phải có số đỉnh bằng nhau.

Điều kiện đủ, định lý Dirac (n >= 3):

$$ \deg(v) \ge \frac{n}{2} \text{ voi moi } v \Rightarrow \text{ co chu trinh Hamilton} $$

Số chu trình Hamilton của đồ thị đầy đủ K_n và của K_(n, n), coi hai chu trình chỉ khác đỉnh xuất phát hoặc chiều đi là một:

$$ \frac{(n-1)!}{2}, \quad \frac{n! \, (n-1)!}{2} $$

Ví dụ: K_5 có 4!/2 = 12 chu trình Hamilton; K_(3, 3) có 3! . 2!/2 = 6.

> Lỗi thường gặp: dùng định lý Dirac theo chiều ngược lại. Chu trình 6 đỉnh có mọi bậc bằng 2, nhỏ hơn 6/2, mà chính nó là một chu trình Hamilton: không thỏa điều kiện đủ thì chưa kết luận được gì.
