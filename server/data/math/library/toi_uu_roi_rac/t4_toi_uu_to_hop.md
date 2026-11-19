---
id: tr_lib_t4
title_vi: Bài toán tối ưu tổ hợp và độ phức tạp thuật toán
subject: toi_uu_roi_rac
floor: 4
summary_vi: Khi không chỉ cần đếm mà phải chọn ra cấu hình tốt nhất: phát biểu bài toán, duyệt toàn bộ, nhánh cận, tham lam, và cách đo một thuật toán chạy nhanh hay chậm bằng ký hiệu O.
skills: [tr_t4_phat_bieu, tr_t4_duyet_toan_bo, tr_t4_nhanh_can, tr_t4_tham_lam, tr_t4_ky_hieu_o]
---
## Phát biểu bài toán tối ưu tổ hợp

Một bài toán tối ưu tổ hợp gồm hai thứ: tập phương án D (hữu hạn, gồm các cấu hình tổ hợp thỏa ràng buộc) và hàm mục tiêu f gán cho mỗi phương án một số. Cần tìm phương án x* làm f lớn nhất (hoặc nhỏ nhất):

$$ f(x^*) = \text{max} \{ f(x) : x \in D \} $$

Ba bài toán mẫu:

- Bài toán cái túi: n đồ vật, đồ vật i nặng a_i, giá trị c_i, túi chứa tối đa b. Phương án là xâu nhị phân x_1 ... x_n; lấy đồ vật i khi x_i = 1.
- Người du lịch: n thành phố, khoảng cách d(i, j). Phương án là một hoán vị (1, j_2, ..., j_n); hàm mục tiêu là độ dài hành trình kể cả đoạn trở về thành phố 1.
- Phân việc: n người, n việc, chi phí c_ij. Phương án là một hoán vị (j_1, ..., j_n): người i làm việc j_i.

Bài toán cái túi viết đầy đủ:

$$ \sum_{i=1}^{n} c_i x_i \to \text{max} $$

$$ \sum_{i=1}^{n} a_i x_i \le b, \quad x_i \in \{0, 1\} $$

Ví dụ: khối lượng (3, 4, 5, 2), giá trị (4, 5, 7, 3), b = 9. Phương án (0, 1, 1, 0) nặng 9, giá trị 12, chấp nhận được; phương án (1, 0, 1, 1) có giá trị 14 nhưng nặng 10, không chấp nhận được.

> Lỗi thường gặp: viết sai tập phương án. Trong bài phân việc, hai người không được nhận cùng một việc, nên phương án là hoán vị (n! phương án) chứ không phải ánh xạ bất kỳ (n^n). Lỗi thứ hai là quên đoạn trở về trong hàm mục tiêu của người du lịch.

## Duyệt toàn bộ

Duyệt toàn bộ đi qua từng phương án (bằng phương pháp sinh hoặc quay lui), tính hàm mục tiêu và giữ lại phương án tốt nhất trong một biến gọi là kỷ lục. Nếu tập phương án hữu hạn và khác rỗng, duyệt toàn bộ luôn cho lời giải đúng.

1. Đặt kỷ lục bằng một số rất lớn (khi tìm giá trị nhỏ nhất).
2. Với mỗi phương án, tính giá trị hàm mục tiêu.
3. Nếu tốt hơn kỷ lục thì cập nhật kỷ lục và ghi lại phương án.
4. Hết phương án: kỷ lục là giá trị tối ưu.

Vấn đề là số phương án. Với n đồ vật, n thành phố (cố định thành phố 1), n người:

$$ 2^n, \quad (n-1)!, \quad n! $$

Ví dụ: bốn thành phố với d(1, 2) = 5, d(1, 3) = 9, d(1, 4) = 4, d(2, 3) = 3, d(2, 4) = 8, d(3, 4) = 6. Chỉ cần xét 3 hành trình (mỗi hành trình và hành trình ngược chiều dài bằng nhau): 1-2-3-4-1 dài 18, 1-2-4-3-1 dài 28, 1-3-2-4-1 dài 24. Hành trình ngắn nhất dài 18.

> Lỗi thường gặp: đánh giá thấp số phương án. Với 40 đồ vật có 2^40, hơn 10^12 phương án, chứ không phải 40^2; máy xét 10^6 phương án mỗi giây cũng mất gần 13 ngày.

## Thuật toán nhánh cận

Nhánh cận là quay lui có thêm phép cắt. Ở mỗi cấu hình bộ phận x_1, ..., x_k, ta tính một cận: với bài toán tìm giá trị nhỏ nhất là cận dưới g, nghĩa là mọi phương án mở rộng từ cấu hình đó có giá trị ít nhất g.

- Bài toán tìm giá trị nhỏ nhất: nếu g lớn hơn hoặc bằng kỷ lục thì cắt nhánh.
- Bài toán tìm giá trị lớn nhất: cận là cận trên; nếu cận trên nhỏ hơn hoặc bằng kỷ lục thì cắt nhánh.

Với bài toán cái túi, xếp các đồ vật theo tỉ số giá trị/khối lượng giảm dần. Đã quyết định k đồ vật đầu, có giá trị v và sức chứa còn lại b_k, thì một cận trên là:

$$ g = v + b_k \cdot \frac{c_{k+1}}{a_{k+1}} $$

Ví dụ: sức chứa 10, các đồ vật (khối lượng, giá trị) = (4, 12), (3, 6), (5, 9), (2, 3). Nhánh x_1 = 1, x_2 = 0 có v = 12, b_k = 6, cận trên 12 + 6 . 9/5 = 114/5. Nếu kỷ lục là 23 thì 114/5 < 23: cắt nhánh.

> Lỗi thường gặp: dùng nhầm chiều so sánh. Với bài toán tìm giá trị lớn nhất, cận trên 23 lớn hơn kỷ lục 20 nghĩa là nhánh có thể còn phương án tốt hơn: phải xét tiếp, không được cắt.

## Thuật toán tham lam

Tham lam xây phương án từng bước, mỗi bước chọn cái tốt nhất trước mắt theo một tiêu chí, và không bao giờ quay lại sửa. Nó rất nhanh, nhưng chỉ đúng với một số bài toán.

Đúng: xếp nhiều buổi nhất vào một phòng. Mỗi bước chọn buổi kết thúc sớm nhất trong các buổi còn xếp được; cách chọn này để lại nhiều thời gian nhất cho các buổi sau, nên luôn tối ưu.

Sai: bài toán cái túi với tiêu chí tỉ số

$$ \frac{c_1}{a_1} \ge \frac{c_2}{a_2} \ge \cdots \ge \frac{c_n}{a_n} $$

Sức chứa 7, đồ vật (5, 10), (4, 7), (3, 5): tham lam lấy đồ vật đầu được giá trị 10, trong khi lấy hai đồ vật sau được 12.

Sai: trả tiền bằng đồng 1, 3, 4. Trả 6, tham lam lấy 4 + 1 + 1 (3 đồng), nhưng 3 + 3 chỉ cần 2 đồng.

> Lỗi thường gặp: tin rằng kết quả tham lam là tối ưu mà không chứng minh. Một ví dụ nhỏ như trả 6 bằng đồng 1, 3, 4 là đủ để bác bỏ; muốn chắc chắn phải chứng minh, hoặc so với duyệt toàn bộ trên các trường hợp nhỏ.

## Ký hiệu O lớn

Để so sánh thuật toán, ta đếm số phép toán T(n) theo kích thước dữ liệu n và chỉ giữ tốc độ tăng của nó.

$$ f(n) = O(g(n)) \Leftrightarrow f(n) \le C \cdot g(n) \text{ khi } n \ge n_0 $$

với một hằng số C > 0 và một n_0 nào đó. Hệ quả: bỏ hằng số nhân và các số hạng tăng chậm hơn. Ví dụ 3n^2 + 5n + 100 <= 108n^2 với n >= 1, nên nó là O(n^2).

Các lớp hay gặp, từ chậm đến nhanh:

$$ \log n < n < n \log n < n^2 < 2^n < n! $$

Đếm số phép toán của vòng lặp:

- Hai vòng for lồng nhau, mỗi vòng chạy n lần: n^2 lần.
- for i = 1 to n: for j = i to n: được n + (n - 1) + ... + 1 = n(n + 1)/2 lần, vẫn là O(n^2).
- j = 1; while j <= n: j = 2j: khoảng log_2 n lần. Với n = 100, j nhận 1, 2, 4, ..., 64: 7 lần.

> Lỗi thường gặp: giữ hằng số trong O, như nói O(4n) chậm gấp đôi O(2n): cả hai là O(n). Ngược lại, hằng số trong số mũ không bỏ được: 4^n không là O(2^n). Và viết O(n^3) cho chắc khi T(n) = n^2 + n là đánh giá đúng nhưng lỏng; đánh giá chặt là O(n^2).
