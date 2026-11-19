---
id: dstt_lib_t5
title_vi: Hệ phương trình tuyến tính và khử Gauss
subject: dai_so_tuyen_tinh
floor: 5
summary_vi: Viết hệ thành Ax = b, dùng ba phép biến đổi hàng để khử dần từng ẩn, thế ngược để lấy nghiệm, và đọc ra hệ có bao nhiêu nghiệm.
skills: [dstt_t5_dang_ma_tran, dstt_t5_bien_doi_hang, dstt_t5_bac_thang, dstt_t5_the_nguoc, dstt_t5_so_nghiem, dstt_t5_he_thuan_nhat]
---
## Viết hệ dưới dạng Ax = b

Một hệ m phương trình tuyến tính, n ẩn viết gọn thành một phép nhân ma trận:

$$ Ax = b, \quad A \text{ co } m \times n, \quad x \in \mathbb{R}^{n}, \quad b \in \mathbb{R}^{m} $$

Mỗi phương trình cho một hàng của A, mỗi ẩn cho một cột. Ẩn nào vắng mặt trong một phương trình thì hệ số ở đó bằng 0.

Ví dụ hệ x + 2y - z = 3, 2x - y = 1, y + 4z = -2 có ma trận hệ số A với các hàng (1, 2, -1), (2, -1, 0), (0, 1, 4) và vế phải b = (3, 1, -2). Ghép b vào làm cột cuối được ma trận bổ sung, viết (A | b):

:::matrix
M = 1 2 -1 3 ; 2 -1 0 1 ; 0 1 4 -2
:::

Mọi phép khử về sau đều làm trên ma trận bổ sung.

Dạng Ax = b cho thấy ngay hai điều: hiệu của hai nghiệm của Ax = b là nghiệm của Ax = 0, vì A(u - v) = b - b; còn tổng của hai nghiệm thì không còn là nghiệm khi b khác 0, vì A(u + v) = 2b.

> Lỗi thường gặp: bỏ quên hệ số 0 của ẩn vắng mặt, làm các cột bị lệch. Hãy viết mọi phương trình theo cùng thứ tự ẩn x, y, z trước khi lập ma trận.

## Ba phép biến đổi sơ cấp trên hàng

Ba phép sau không làm thay đổi tập nghiệm của hệ, vì mỗi phép đều có phép ngược cùng loại:

- Đổi chỗ hai hàng: R_i <-> R_j.
- Nhân một hàng với một số k khác 0: R_i <- kR_i.
- Cộng k lần hàng j vào hàng i: R_i <- R_i + kR_j. Hàng bị thay là hàng đứng bên trái mũi tên.

Ví dụ với hàng 1 là (1, 2 | 3) và hàng 2 là (3, 4 | 5), phép R2 <- R2 - 3R1 cho:

$$ (3, 4 \mid 5) - 3(1, 2 \mid 3) = (0, -2 \mid -4) $$

Phép biến đổi làm trên cả hàng, kể cả cột vế phải. Mỗi lần chỉ thay một hàng; làm hai phép cùng lúc, mỗi phép dùng các hàng cũ, có thể biến hai hàng thành một và làm mất thông tin.

> Lỗi thường gặp: sai dấu ở cột vế phải, như viết 5 - 9 thành 5 + 9. Và không bao giờ nhân một hàng với 0.

## Khử Gauss về dạng bậc thang

Một ma trận có dạng bậc thang khi các hàng toàn số 0 nằm dưới cùng, và phần tử khác 0 đầu tiên của mỗi hàng (gọi là trụ) nằm bên phải trụ của hàng trên nó.

:::matrix
U = 1 2 0 3 ; 0 0 1 4 ; 0 0 0 0
:::

Khử Gauss đi từng cột, từ trái sang phải:

1. Chọn trụ ở cột đang xét: một hàng có phần tử khác 0 ở cột đó; nếu hàng trên cùng có số 0 ở đó thì đổi chỗ với một hàng bên dưới.
2. Dùng hàng có trụ để làm mọi số bên dưới trụ thành 0, bằng phép R_i <- R_i + kR_j.
3. Bỏ hàng đó ra, làm tiếp với cột sau và các hàng còn lại.

Ví dụ với các hàng (1, 1, 1 | 6), (1, 2, 3 | 14), (1, 3, 6 | 25): R2 - R1 và R3 - R1 cho (0, 1, 2 | 8) và (0, 2, 5 | 19); rồi R3 - 2R2 cho (0, 0, 1 | 3). Ma trận bổ sung cuối cùng, với cột cuối là vế phải:

$$ \begin{pmatrix} 1 & 1 & 1 & 6 \\ 0 & 1 & 2 & 8 \\ 0 & 0 & 1 & 3 \end{pmatrix} $$

Dạng bậc thang không duy nhất (nhân một hàng với số khác 0 vẫn được dạng bậc thang), nhưng vị trí các trụ thì luôn như nhau.

> Lỗi thường gặp: chia cho một trụ bằng 0. Khi phần tử ở vị trí trụ bằng 0, phải đổi chỗ hàng chứ không chia.

## Thế ngược tìm nghiệm

Từ dạng bậc thang, giải phương trình cuối trước, rồi thay ngược lên trên.

Ví dụ với các hàng (1, -1, 1 | 2), (0, 1, 2 | 7), (0, 0, 2 | 4):

1. Hàng 3: 2z = 4 nên z = 2.
2. Hàng 2: y + 2 . 2 = 7 nên y = 3.
3. Hàng 1: x - 3 + 2 = 2 nên x = 3.

Khi một ẩn không có trụ, nó là ẩn tự do: đặt nó bằng một tham số t rồi tính các ẩn có trụ theo t. Với các hàng (1, 2, -1 | 3) và (0, 1, 1 | 2), đặt z = t:

$$ (x, y, z) = (-1 + 3t, \; 2 - t, \; t), \quad t \in \mathbb{R} $$

> Lỗi thường gặp: quên đổi dấu khi chuyển vế. Từ 2x - 1 - 2 = 3 phải được 2x = 3 + 1 + 2, không phải 3 - 1 - 2.

## Biện luận số nghiệm

Nhìn dạng bậc thang của ma trận bổ sung là biết hệ có bao nhiêu nghiệm:

- Có một hàng (0, ..., 0 | c) với c khác 0: hệ vô nghiệm, vì hàng đó nói 0 = c.
- Không có hàng như vậy và ẩn nào cũng có trụ: nghiệm duy nhất.
- Không có hàng như vậy nhưng còn ẩn tự do: vô số nghiệm.

Một hệ tuyến tính không bao giờ có đúng hai nghiệm: nếu u và v là hai nghiệm khác nhau thì mọi điểm u + t(v - u) cũng là nghiệm, vì

$$ A(u + t(v - u)) = b + t \cdot 0 = b $$

Với hệ có tham số, khử Gauss bình thường rồi xem tham số làm hàng cuối thành dạng nào. Ví dụ hàng cuối (0, 0, m | 1): m = 0 cho vô nghiệm, m khác 0 cho nghiệm duy nhất.

> Lỗi thường gặp: kết luận vô số nghiệm chỉ vì số ẩn nhiều hơn số phương trình. Điều đó chỉ loại trừ nghiệm duy nhất; hệ vẫn có thể vô nghiệm.

## Hệ thuần nhất Ax = 0

Hệ có vế phải bằng 0 luôn có nghiệm x = 0, gọi là nghiệm tầm thường. Câu hỏi duy nhất là nó có nghiệm khác 0 hay không.

$$ A \cdot 0 = 0 $$

Số ẩn tự do bằng số ẩn trừ số trụ. Hệ có nghiệm khác 0 khi và chỉ khi có ít nhất một ẩn tự do. Đặc biệt, hệ thuần nhất có nhiều ẩn hơn phương trình luôn có nghiệm khác 0.

Ví dụ hệ x + y - z = 0, 2x + 3y + z = 0: R2 - 2R1 cho (0, 1, 3 | 0); z tự do, đặt z = t thì y = -3t và x = 4t:

$$ (x, y, z) = t(4, -3, 1) $$

Khi giải hệ thuần nhất có thể bỏ cột vế phải, vì phép biến đổi hàng giữ nguyên cột toàn số 0.

> Lỗi thường gặp: nói hệ thuần nhất "vô nghiệm". Nó luôn có ít nhất nghiệm x = 0.
