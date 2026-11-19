---
id: tr_lib_t5
title_vi: Đồ thị: khái niệm cơ bản và biểu diễn trên máy tính
subject: toi_uu_roi_rac
floor: 5
summary_vi: Đỉnh và cạnh, các loại đồ thị, bậc và định lý bắt tay, đường đi và liên thông, rồi ba cách lưu một đồ thị trong máy: ma trận kề, danh sách kề, danh sách cạnh.
skills: [tr_t5_khai_niem, tr_t5_bac, tr_t5_duong_di_lien_thong, tr_t5_ma_tran_ke, tr_t5_danh_sach_ke]
---
## Đỉnh, cạnh và các loại đồ thị

Một đồ thị G = (V, E) gồm tập đỉnh V và tập cạnh E; mỗi cạnh nối hai đỉnh. Trong Tàng Thư Các đồ thị luôn được cho bằng chữ: "các đỉnh 1, 2, ..., 6; các cạnh: 1-2, 2-3, ...". Cạnh 1-2 nối đỉnh 1 với đỉnh 2.

- Đồ thị đơn vô hướng: cạnh không có chiều, không có khuyên (cạnh nối một đỉnh với chính nó), giữa hai đỉnh nhiều nhất một cạnh.
- Đa đồ thị: cho phép nhiều cạnh nối cùng hai đỉnh.
- Đồ thị có hướng: mỗi cạnh (gọi là cung) đi từ đỉnh đầu đến đỉnh cuối.
- Đồ thị đầy đủ K_n: n đỉnh, mọi cặp đỉnh đều kề nhau.
- Đồ thị hai phía: tập đỉnh chia được thành hai phần, mỗi cạnh nối hai phần khác nhau. K_(m, n) là đồ thị hai phía đầy đủ.

Số cạnh của đồ thị đầy đủ và của đồ thị hai phía đầy đủ:

$$ |E(K_n)| = \frac{n(n-1)}{2}, \quad |E(K_{m,n})| = m \cdot n $$

Đồ thị bù của đồ thị đơn G có cùng tập đỉnh, và hai đỉnh kề nhau khi chúng không kề nhau trong G. Vì mỗi cặp đỉnh thuộc đúng một trong hai đồ thị, G có m cạnh thì đồ thị bù có n(n - 1)/2 - m cạnh.

Một đồ thị là hai phía khi và chỉ khi nó không có chu trình độ dài lẻ. Cách kiểm tra: tô màu dần, mỗi đỉnh kề một đỉnh màu A thì tô màu B; gặp một cạnh hai đầu cùng màu là có chu trình lẻ.

> Lỗi thường gặp: tô màu xong mà quên kiểm tra cạnh cuối cùng. Chu trình 1-2-3-4-5-1 tô được xanh, đỏ, xanh, đỏ, xanh, nhưng cạnh 5-1 có hai đầu cùng màu xanh: nó không là đồ thị hai phía.

## Bậc của đỉnh và định lý bắt tay

Bậc deg(v) của đỉnh v là số cạnh chạm vào v (một khuyên tính hai lần). Mỗi cạnh góp 1 vào bậc của mỗi đầu, nên:

$$ \sum_{v \in V} \deg(v) = 2|E| $$

Hệ quả: tổng các bậc luôn chẵn, và số đỉnh bậc lẻ luôn là số chẵn.

Ví dụ: 10 đỉnh, mỗi đỉnh bậc 3, có 30/2 = 15 cạnh. Còn 5 đỉnh mỗi đỉnh bậc 3 thì không thể: tổng 15 là số lẻ.

Muốn biết một dãy có là dãy bậc của một đồ thị đơn không, dùng Havel-Hakimi: bỏ đỉnh bậc lớn nhất d, trừ 1 ở d bậc lớn nhất còn lại, lặp lại. Còn toàn số 0 là dựng được; gặp số âm hoặc thiếu đỉnh là không.

1. 3, 3, 2, 2, 2: bỏ 3, còn 2, 1, 1, 2, xếp lại 2, 2, 1, 1.
2. Bỏ 2, còn 1, 0, 1, xếp lại 1, 1, 0.
3. Bỏ 1, còn 0, 0: dựng được.

Trong đồ thị đơn n đỉnh, mỗi bậc nằm trong 0, 1, ..., n - 1, và không thể vừa có đỉnh bậc 0 vừa có đỉnh bậc n - 1. Theo nguyên lý Dirichlet, luôn có hai đỉnh cùng bậc.

> Lỗi thường gặp: quên chia đôi. 9 người mỗi người bắt tay 3 người không cho 27 cái bắt tay mà cho 27/2, không nguyên: điều đó không thể xảy ra, vì số đỉnh bậc lẻ phải chẵn.

## Đường đi, chu trình và liên thông

- Đường đi từ u đến v: dãy đỉnh u = v_0, v_1, ..., v_k = v mà mỗi hai đỉnh liền nhau kề nhau; độ dài là k (số cạnh).
- Đường đi đơn: không đỉnh nào lặp lại. Có một đường đi từ u đến v (u khác v) thì có một đường đi đơn: cắt bỏ các vòng lặp.
- Chu trình: đường đi trở về đỉnh đầu, có ít nhất một cạnh, không dùng một cạnh hai lần.

Đồ thị liên thông khi mọi cặp đỉnh có đường đi nối nhau. Mỗi đồ thị chia thành các thành phần liên thông; một đỉnh cô lập tự nó là một thành phần.

Đồ thị đơn n đỉnh có nhiều hơn (n - 1)(n - 2)/2 cạnh thì chắc chắn liên thông. Với n = 6:

$$ \frac{(n-1)(n-2)}{2} = 10 $$

nên 11 cạnh là đủ, còn K_5 cộng một đỉnh cô lập có 10 cạnh mà không liên thông.

> Lỗi thường gặp: bỏ quên đỉnh cô lập khi đếm thành phần liên thông. Các đỉnh 1..7 với các cạnh 1-2, 2-3, 4-5, 5-6 có 3 thành phần: {1, 2, 3}, {4, 5, 6} và {7}.

## Ma trận kề

Ma trận kề A của đồ thị n đỉnh là ma trận n x n: a_ij là số cạnh nối i với j (với đồ thị có hướng: số cung đi từ i đến j). Ví dụ đồ thị có các cạnh 1-2, 1-3, 1-4, 2-3, 3-4:

:::matrix
A = 0 1 1 1 ; 1 0 1 0 ; 1 1 0 1 ; 1 0 1 0
:::

- Đồ thị vô hướng có ma trận kề đối xứng.
- Tổng hàng i là bậc của đỉnh i; tổng mọi phần tử là hai lần số cạnh.
- Với đồ thị có hướng: tổng hàng i là số cung đi ra khỏi i, tổng cột j là số cung đi vào j.

Lũy thừa của A đếm các hành trình (đường đi cho phép lặp đỉnh):

$$ (A^2)_{ij} = \sum_{k=1}^{n} a_{ik} a_{kj} $$

là số đỉnh k kề cả i lẫn j, tức số hành trình độ dài 2 từ i đến j; tổng quát, phần tử (i, j) của A^k là số hành trình độ dài k. Ở ví dụ trên, (A^2)_24 = 2 (qua đỉnh 1 và đỉnh 3), (A^2)_11 = 3 = deg(1). Mỗi tam giác cho 6 hành trình khép kín độ dài 3:

$$ \text{so tam giac} = \frac{1}{6} \operatorname{tr}(A^3) $$

> Lỗi thường gặp: với đồ thị có hướng, đọc số cung đi vào một đỉnh từ hàng của nó. Hàng ghi các cung đi ra, cột ghi các cung đi vào.

## Danh sách kề và danh sách cạnh

- Danh sách cạnh: liệt kê m cạnh, mỗi cạnh một cặp đỉnh.
- Danh sách kề: mỗi đỉnh u có một danh sách Ke(u) các đỉnh kề u. Với đồ thị có hướng, Ke(u) chỉ ghi các cung đi ra từ u.
- Ma trận kề: n^2 ô.

Trong đồ thị vô hướng, cạnh u-v có mặt hai lần (v trong Ke(u), u trong Ke(v)), nên tổng độ dài các danh sách kề là tổng các bậc, tức 2m. So sánh bộ nhớ:

$$ n^2 \text{ (ma tran ke)}, \quad n + 2m \text{ (danh sach ke)} $$

Ví dụ: 1000 đỉnh, 3000 cạnh. Ma trận kề cần 10^6 ô; danh sách kề cần khoảng 1000 + 6000. Danh sách kề hợp với đồ thị thưa và với việc duyệt các đỉnh kề; ma trận kề hợp với đồ thị dày và khi cần hỏi nhanh hai đỉnh có kề nhau không.

Chuyển danh sách cạnh sang danh sách kề: tạo n danh sách rỗng, đọc từng cạnh u-v, thêm v vào Ke(u) và u vào Ke(v).

> Lỗi thường gặp: đếm mỗi phần tử của danh sách kề là một cạnh. Ke(1) = 2, 3; Ke(2) = 1, 3, 4; Ke(3) = 1, 2; Ke(4) = 2 có tổng độ dài 8 nhưng chỉ 4 cạnh.
