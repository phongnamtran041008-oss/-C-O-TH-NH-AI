---
id: dstt_lib_t1
title_vi: Tập hợp và ánh xạ
subject: dai_so_tuyen_tinh
floor: 1
summary_vi: Nền móng của cả bí cảnh: cách gọi tên một nhóm vật, cách ghép hai nhóm lại, và cách một quy tắc đưa vật này thành vật kia.
skills: [dstt_t1_tap_hop, dstt_t1_phep_toan_tap_hop, dstt_t1_tich_descartes, dstt_t1_anh_xa, dstt_t1_don_toan_song_anh, dstt_t1_hop_va_nguoc]
---
## Tập hợp và phần tử

Một tập hợp chỉ là một nhóm vật được gom lại và gọi chung một tên. Mỗi vật trong nhóm là một phần tử. Muốn cho biết một tập hợp, cách đơn giản nhất là liệt kê phần tử của nó trong hai dấu ngoặc nhọn.

$$ A = \{1, 2, 3\} $$

Chỉ có đúng hai câu trả lời cho câu hỏi "x có trong A không": thuộc hoặc không thuộc. Viết là x thuộc A hoặc x không thuộc A.

Hai điều hay bị lẫn với nhau:

- Phần tử là vật nằm trong tập hợp.
- Tập con là cả một tập hợp mà mọi phần tử của nó đều nằm trong tập hợp kia.

Tập rỗng là tập hợp không có phần tử nào. Nó là tập con của mọi tập hợp, vì muốn nó không phải là tập con thì phải chỉ ra một phần tử của nó nằm ngoài, mà nó có phần tử nào đâu.

Nếu A có n phần tử thì A có đúng 2^n tập con: khi lập một tập con, mỗi phần tử được chọn hoặc không, hai khả năng cho mỗi phần tử.

$$ |A| = n \Rightarrow A \text{ co } 2^{n} \text{ tap con} $$

> Lỗi thường gặp: coi tập {1, {2, 3}} là có ba phần tử. Nó chỉ có hai: số 1 và tập {2, 3}. Số 2 là phần tử của phần tử, không phải phần tử của nó.

## Phép toán trên tập hợp

Từ hai tập hợp A và B lập ra tập mới theo ba cách chính.

$$ A \cap B = \{x : x \in A \text{ va } x \in B\} $$

$$ A \cup B = \{x : x \in A \text{ hoac } x \in B\} $$

$$ A \setminus B = \{x : x \in A \text{ va } x \notin B\} $$

Giao là phần chung, hợp là gom tất cả lại, hiệu A \ B là phần của A sau khi bỏ đi những gì cũng có trong B. Khi gom, mỗi phần tử chỉ viết một lần.

Ví dụ với A = {1, 2, 3, 4} và B = {3, 4, 5}:

1. Phần chung của hai tập là 3 và 4, nên A giao B = {3, 4}.
2. Gom hết lại và viết mỗi số một lần: A hợp B = {1, 2, 3, 4, 5}.
3. Bỏ khỏi A những gì có trong B: A \ B = {1, 2}.
4. Đổi vai trò: B \ A = {5}, khác hẳn A \ B.

Đếm số phần tử của hợp thì không cộng thẳng được, vì phần chung bị đếm hai lần:

$$ |A \cup B| = |A| + |B| - |A \cap B| $$

> Lỗi thường gặp: tưởng A \ B = B \ A. Phép hiệu không đổi chỗ được, như phép trừ số vậy.

## Tích Descartes

Tích Descartes A x B là tập hợp mọi cặp có thứ tự, lấy thành phần đầu trong A và thành phần sau trong B.

$$ A \times B = \{(a, b) : a \in A, b \in B\} $$

Có thứ tự nghĩa là (1, 2) và (2, 1) là hai cặp khác nhau. Vì vậy A x B và B x A nói chung khác nhau, dù số phần tử của chúng bằng nhau.

Đếm thì dễ: mỗi cách chọn thành phần đầu ghép được với mọi cách chọn thành phần sau.

$$ |A \times B| = |A| \cdot |B| $$

Chỗ này sẽ còn gặp lại ở tầng trên: một ma trận cỡ m x n chính là một bảng có vị trí đánh số bằng các cặp (hàng, cột), tức là bằng một tích Descartes.

> Lỗi thường gặp: viết (a, b) thuộc A x B khi a thuộc B. Thành phần đứng trước luôn lấy trong tập đứng trước.

## Ánh xạ, ảnh và tạo ảnh

Ánh xạ f từ X vào Y là quy tắc cho mỗi phần tử của X đúng một phần tử của Y.

$$ f : X \to Y, \quad x \mapsto f(x) $$

Hai chữ "đúng một" là phần quan trọng nhất. Quy tắc cho x hai kết quả không phải là ánh xạ; quy tắc bỏ sót một x nào đó cũng không phải.

Ảnh của một tập A con của X là tập gom mọi kết quả:

$$ f(A) = \{f(x) : x \in A\} $$

Tạo ảnh của một tập B con của Y là tập gom mọi x cho kết quả rơi vào B. Chú ý tạo ảnh có thể rỗng, có thể có nhiều phần tử, và vẫn luôn viết được.

Ví dụ với f(x) = x^2 trên R và A = {-2, -1, 0, 1, 2}:

1. Tính từng ảnh: f(-2) = 4, f(-1) = 1, f(0) = 0, f(1) = 1, f(2) = 4.
2. Gom lại, mỗi giá trị một lần: f(A) = {0, 1, 4}.
3. Tạo ảnh của {4} là mọi x có x^2 = 4, tức là {-2, 2}.

> Lỗi thường gặp: viết f(A) có đúng 5 phần tử vì A có 5 phần tử. Ảnh có thể ít phần tử hơn, vì hai phần tử khác nhau được phép chung một ảnh.

## Đơn ánh, toàn ánh, song ánh

Ba tính chất này trả lời ba câu hỏi khác nhau về cùng một ánh xạ f từ X vào Y.

- Đơn ánh: hai phần tử khác nhau luôn có ảnh khác nhau, không ai dùng chung ảnh.
- Toàn ánh: mọi phần tử của Y đều là ảnh của ít nhất một phần tử của X, không chỗ nào của Y bị bỏ trống.
- Song ánh: vừa đơn ánh vừa toàn ánh, mỗi phần tử của Y ứng với đúng một phần tử của X.

Cách kiểm tra đơn ánh hay dùng nhất là giả sử hai ảnh bằng nhau rồi suy ngược:

$$ f(u) = f(v) \Rightarrow u = v $$

Ví dụ f(x) = 2x + 3 trên R: từ 2u + 3 = 2v + 3 suy ra u = v, nên đơn ánh. Với mọi y, phương trình 2x + 3 = y có nghiệm x = (y - 3)/2, nên toàn ánh. Vậy f là song ánh.

Còn f(x) = x^2 trên R không đơn ánh vì f(1) = f(-1), và cũng không toàn ánh vì số âm không phải là ảnh của ai.

Đếm trên tập hữu hạn: số đơn ánh từ tập m phần tử vào tập n phần tử là n(n-1)...(n-m+1), vì ảnh sau không được trùng ảnh trước.

> Lỗi thường gặp: kết luận "f không toàn ánh" mà không nói rõ Y là tập nào. Đổi Y thì câu trả lời đổi theo: f(x) = x^2 từ R vào R không toàn ánh, nhưng từ R vào tập các số không âm thì lại toàn ánh.

## Ánh xạ hợp và ánh xạ ngược

Hợp thành của f và g là làm f trước rồi lấy kết quả làm cho g.

$$ (g \circ f)(x) = g(f(x)) $$

Thứ tự rất quan trọng: chữ đứng gần x nhất được làm trước. Nói chung g hợp f khác f hợp g. Lấy f(x) = x^2 và g(x) = x + 1 thì g(f(2)) = 5 còn f(g(2)) = 9.

Ánh xạ ngược chỉ có khi f là song ánh. Khi đó ánh xạ ngược gửi mỗi y về đúng cái x đã sinh ra nó:

$$ f^{-1}(y) = x \Leftrightarrow f(x) = y $$

Muốn tìm ánh xạ ngược của một hàm bậc nhất, cứ giải phương trình f(x) = y theo x. Với f(x) = 2x + 1 và y = 7: giải 2x + 1 = 7 được x = 3.

> Lỗi thường gặp: viết f^-1 cho một ánh xạ không phải song ánh. Ký hiệu tạo ảnh f^-1(B) của một tập thì luôn dùng được, nhưng ánh xạ ngược f^-1(y) của một phần tử thì không.
