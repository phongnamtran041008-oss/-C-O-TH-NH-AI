---
id: tr_lib_t9
title_vi: Quy hoạch tuyến tính và quy hoạch phi tuyến
subject: toi_uu_roi_rac
floor: 9
summary_vi: Mô hình quy hoạch tuyến tính, cách giải bằng hình học và bằng đơn hình, bài toán đối ngẫu; rồi phần mở rộng cho trí tuệ nhân tạo: nhân tử Lagrange, điều kiện KKT, và hạ gradient trên một hàm mất mát.
skills: [tr_t9_mo_hinh_qhtt, tr_t9_hinh_hoc, tr_t9_don_hinh, tr_t9_doi_ngau, tr_t9_lagrange_kkt, tr_t9_gradient_descent]
---
## Mô hình quy hoạch tuyến tính

Quy hoạch tuyến tính (QHTT) là bài toán tối ưu có hàm mục tiêu và mọi ràng buộc đều tuyến tính:

$$ \max c^T x \quad \text{voi} \quad A x \le b, \; x \ge 0 $$

Lập mô hình theo ba câu hỏi: ta chọn gì (biến), ta muốn gì (hàm mục tiêu, max lãi hay min chi phí), và cái gì giới hạn ta (mỗi tài nguyên, mỗi yêu cầu tối thiểu là một ràng buộc).

Dạng chính tắc chỉ có ràng buộc đẳng thức và biến không âm. Các phép đưa về dạng chính tắc:

- Ràng buộc <=: cộng một biến bù không âm vào vế trái. Ràng buộc >=: trừ một biến bù không âm.
- Biến x_j <= 0: thay x_j = -x_j'. Biến không ràng buộc dấu: thay x_j = x_j' - x_j'' với hai biến mới không âm.
- max f tương đương min (-f).

Ví dụ: max 2x1 - x2 + 3x3 với x1 + x2 + x3 <= 10, 2x1 - x2 >= 3, x1 - x3 = 2, x1 >= 0, x2 <= 0, x3 tự do. Dạng chính tắc có 6 biến (x1, x2', x3', x3'', s1, s2) và 3 ràng buộc đẳng thức.

> Lỗi thường gặp: viết sai chiều ràng buộc ("cần ít nhất" là >=, "có tối đa" là <=) hoặc ghép sai hệ số: mỗi ràng buộc là lượng của một tài nguyên lấy từ mọi sản phẩm. Viết đẳng thức khi đề chỉ nói "không vượt quá" cũng sai: không bắt buộc dùng hết tài nguyên.

## Phương pháp hình học hai biến

Với hai biến x, y:

1. Vẽ đường biên của mỗi ràng buộc và chọn nửa mặt phẳng thỏa mãn nó.
2. Giao các nửa mặt phẳng là miền ràng buộc D, một đa giác lồi.
3. Tìm các đỉnh của D: giao điểm của hai đường biên mà thỏa mọi ràng buộc.
4. Tính hàm mục tiêu tại từng đỉnh và chọn đỉnh tốt nhất.

Nếu D khác rỗng và bị chặn thì bài toán có nghiệm tối ưu, và có một nghiệm là đỉnh của D. Hai đỉnh kề nhau cùng tốt nhất thì cả cạnh nối chúng đều tối ưu. Một ràng buộc là chặt tại nghiệm nếu dấu bằng xảy ra, lỏng nếu còn dư.

$$ \text{QHTT co nghiem} \Rightarrow \text{co nghiem toi uu tai mot dinh} $$

Ví dụ: max 2x + 3y với x + y <= 6, x + 3y <= 12, 2x + y <= 10, x, y >= 0. Các đỉnh (0, 0), (5, 0), (4, 2), (3, 3), (0, 4) cho z = 0, 10, 14, 15, 12. Nghiệm tối ưu (3, 3), z = 15; ràng buộc 2x + y <= 10 lỏng (2 . 3 + 3 = 9).

> Lỗi thường gặp: tìm nghiệm tối ưu ở bên trong miền bằng cách cho đạo hàm bằng 0. Hàm tuyến tính khác hằng có gradient khác 0 ở mọi nơi, nên nó luôn đạt tối ưu trên biên, tại một đỉnh. Cũng hay quên kiểm tra một giao điểm có thỏa các ràng buộc còn lại không.

## Phương pháp đơn hình

Phương pháp đơn hình đi từ đỉnh này sang đỉnh kề tốt hơn, bằng đại số thay cho hình vẽ. Viết bài toán dạng từ vựng: mỗi biến bù (biến cơ sở) biểu diễn qua các biến ngoài cơ sở, ví dụ s1 = 8 - x1 - 2x2, s2 = 12 - 3x1 - 2x2, z = 2x1 + 3x2. Phương án hiện tại cho các biến ngoài cơ sở bằng 0.

1. Biến vào: một biến ngoài cơ sở có hệ số dương trong z (thường chọn hệ số lớn nhất). Không còn hệ số dương thì đã tối ưu.
2. Biến ra: tăng biến vào đến khi một biến cơ sở chạm 0. Chỉ xét các hàng mà biến cơ sở giảm khi biến vào tăng; lấy tỉ số nhỏ nhất.
3. Đổi vai: rút biến vào từ hàng của biến ra, thế vào các hàng khác và vào z.

$$ \text{ti so} = \min \frac{b_i}{a_{ij}} \quad \text{voi} \quad a_{ij} > 0 $$

Ví dụ trên: x2 vào; tỉ số 8/2 = 4 và 12/2 = 6, s1 ra, z = 12. Từ vựng mới có z = 12 + x1/2 - 3s1/2; x1 vào, tỉ số nhỏ nhất ở hàng s2, x1 = 2, x2 = 3, z = 13, và không còn hệ số dương: tối ưu.

> Lỗi thường gặp: chọn tỉ số lớn nhất "để z tăng nhiều", hoặc lập tỉ số với cả hàng có hệ số không làm biến cơ sở giảm. Khi đó một biến cơ sở thành âm và phương án không còn chấp nhận được.

## Bài toán đối ngẫu

Mỗi bài QHTT có một bài đối ngẫu. Với bài gốc max c^T x, Ax <= b, x >= 0:

$$ \min b^T y \quad \text{voi} \quad A^T y \ge c, \; y \ge 0 $$

Quy tắc lập (bài gốc là max): ràng buộc <= ứng với biến đối ngẫu >= 0, ràng buộc = ứng với biến đối ngẫu tự do; biến x_j >= 0 ứng với ràng buộc đối ngẫu >=, biến tự do ứng với ràng buộc đối ngẫu =.

- Đối ngẫu yếu: với mọi x chấp nhận được của bài gốc và y của bài đối ngẫu, c^T x <= b^T y.
- Đối ngẫu mạnh: nếu một bài có nghiệm tối ưu thì bài kia cũng có, và hai giá trị tối ưu bằng nhau.
- Độ lệch bù: tại cặp nghiệm tối ưu, ràng buộc gốc lỏng thì biến đối ngẫu tương ứng bằng 0; biến gốc dương thì ràng buộc đối ngẫu tương ứng chặt.

Ví dụ: max 3x + 4y với x + y <= 5, x + 3y <= 9, x, y >= 0. Đoán x = 3, y = 2, z = 17. Vì x, y > 0, giải u + v = 3, u + 3v = 4 được u = 5/2, v = 1/2 >= 0, và 5u + 9v = 17 = z: theo đối ngẫu yếu, cả hai nghiệm đều tối ưu.

> Lỗi thường gặp: đảo chiều độ lệch bù, cho biến đối ngẫu của một ràng buộc lỏng là số dương. Ràng buộc còn dư thì thêm một chút tài nguyên đó không làm tăng lãi, nên "giá" của nó, biến đối ngẫu, bằng 0.

## Nhân tử Lagrange và điều kiện KKT

Tìm cực trị của f(x, y) với ràng buộc g(x, y) = 0: lập hàm Lagrange và giải hệ ba phương trình.

$$ L = f - \lambda g, \quad L_x = 0, \; L_y = 0, \; g = 0 $$

Nhân tử lambda đo tốc độ thay đổi của giá trị tối ưu khi nới ràng buộc g = 0 thành g = h: đạo hàm của giá trị tối ưu theo h bằng lambda.

Ví dụ: max xy với x + 2y = 8. L_x = y - lambda = 0, L_y = x - 2lambda = 0, nên x = 2lambda, y = lambda; thay vào ràng buộc được lambda = 2, x = 4, y = 2, giá trị lớn nhất 8. Với vế phải c, giá trị lớn nhất là c^2/8, có đạo hàm c/4 = 2 tại c = 8.

Với ràng buộc bất đẳng thức g(x) <= 0 (bài min), điều kiện KKT tại nghiệm là: grad f + mu grad g = 0, mu >= 0, g <= 0 và mu g = 0. Nghĩa là hoặc ràng buộc lỏng và mu = 0 (nghiệm như khi không có ràng buộc), hoặc ràng buộc chặt và mu >= 0. Với bài lồi, KKT là điều kiện đủ.

> Lỗi thường gặp: quên phương trình ràng buộc khi giải hệ. Với min x^2 + y^2, x + y = 2, cho grad f = 0 được (0, 0) không thỏa ràng buộc; phải dùng thêm x + y = 2 để được lambda = 2, x = y = 1, giá trị nhỏ nhất 2.

## Hạ gradient và hàm mất mát

Hạ gradient tìm cực tiểu của f bằng cách đi ngược hướng gradient với bước học eta > 0:

$$ x_{k+1} = x_k - \eta \nabla f(x_k) $$

Trong học máy, f là hàm mất mát. Mô hình y = wx học từ các điểm (x_i, y_i) với mất mát bình phương:

$$ L(w) = \sum (w x_i - y_i)^2, \quad L'(w) = 2 \sum x_i (w x_i - y_i) $$

L lồi, cực tiểu tại w* = (tổng x_i y_i)/(tổng x_i^2).

Bước học quyết định số phận: với f(x) = a x^2 (a > 0), một bước cho x mới = (1 - 2a eta) x. Dãy hội tụ về 0 khi và chỉ khi |1 - 2a eta| < 1, tức 0 < eta < 1/a; eta = 1/a làm điểm nhảy qua lại mãi; eta > 1/a làm điểm văng ra xa.

Ví dụ: hai điểm (1, 2), (2, 3), L(w) = (w - 2)^2 + (2w - 3)^2, L'(w) = 10w - 16. Từ w0 = 0 với eta = 1/20: w1 = 0 - (1/20)(-16) = 4/5, và L giảm từ 13 xuống 17/5. Cực tiểu w* = 8/5.

> Lỗi thường gặp: tin rằng hạ gradient luôn làm f giảm. Với f = 5x^2 và eta = 3/10, x mới = -2x: từ x0 = 1 được -2, 4, -8, ... và f tăng 5, 20, 80. Bước học phải nhỏ hơn 1/5 ở đây.
