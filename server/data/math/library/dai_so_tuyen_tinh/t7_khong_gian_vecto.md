---
id: dstt_lib_t7
title_vi: Không gian vectơ
subject: dai_so_tuyen_tinh
floor: 7
summary_vi: Khi nào một tập với hai phép toán là không gian vectơ, không gian con, tổ hợp và bao tuyến tính, độc lập tuyến tính, cơ sở và số chiều, tọa độ và ma trận chuyển cơ sở.
skills: [dstt_t7_khong_gian_vecto, dstt_t7_khong_gian_con, dstt_t7_to_hop_tuyen_tinh, dstt_t7_doc_lap_tuyen_tinh, dstt_t7_co_so_so_chieu, dstt_t7_toa_do]
---
## Không gian vectơ và các tiên đề

Một không gian vectơ là một tập V cùng hai phép toán: cộng hai vectơ và nhân một vectơ với một số thực, sao cho kết quả vẫn nằm trong V và tám tiên đề sau đúng với mọi u, v, w thuộc V và mọi số k, l:

- u + v = v + u và (u + v) + w = u + (v + w).
- Có vectơ 0 với u + 0 = u; mỗi u có vectơ đối -u với u + (-u) = 0.
- k(u + v) = ku + kv và (k + l)u = ku + lu.
- (kl)u = k(lu) và 1u = u.

$$ (k + l)u = ku + lu, \qquad k(u + v) = ku + kv $$

Ví dụ quen thuộc: R^n, các ma trận cùng cỡ, các đa thức bậc không quá n, đều với phép toán thông thường.

Muốn chỉ ra một tập KHÔNG là không gian vectơ, chỉ cần một tiên đề sai với một ví dụ cụ thể. Ví dụ R^2 với k.(x, y) = (kx, 0): 1.(1, 2) = (1, 0), nên tiên đề 1u = u sai.

Từ các tiên đề suy ra được 0u = 0 và (-1)u = -u. Chứng minh 0u = 0: viết 0u = (0 + 0)u = 0u + 0u, rồi cộng vectơ đối của 0u vào hai vế.

> Lỗi thường gặp: dùng nhầm tiên đề. Tổng 1u + (-1)u gộp lại bằng tiên đề (k + l)u = ku + lu, không phải bằng (kl)u = k(lu).

## Không gian con

Tập con W của không gian vectơ V là không gian con khi W khác rỗng và đóng với hai phép toán:

$$ u, v \in W \Rightarrow u + v \in W, \qquad u \in W \Rightarrow ku \in W $$

Khi đó W tự nó là một không gian vectơ. Không gian con luôn chứa 0 (lấy k = 0), nên tập không chứa 0 không thể là không gian con.

Dấu hiệu nhanh trong R^n: tập nghiệm của một hệ phương trình tuyến tính THUẦN NHẤT luôn là không gian con; có vế phải khác 0 (như x + y = 1), có bình phương, tích, giá trị tuyệt đối hay bất đẳng thức thì thường không.

- {(x, y, z) : x - 2y + z = 0} là không gian con.
- {(x, y) : xy = 0} không phải: (1, 0) + (0, 1) = (1, 1) ra ngoài.
- {(x, y) : x >= 0} không phải: nhân với -1 ra ngoài.

Giao của hai không gian con là không gian con; hợp của chúng thì nói chung không.

> Lỗi thường gặp: chỉ kiểm tra u + v và ku "có dạng (x, y, z)". Phải kiểm tra chúng thỏa ĐIỀU KIỆN định nghĩa W.

## Tổ hợp tuyến tính và bao tuyến tính

Tổ hợp tuyến tính của u1, ..., uk là mọi vectơ dạng

$$ a_{1}u_{1} + a_{2}u_{2} + \ldots + a_{k}u_{k} $$

Tập mọi tổ hợp đó là bao tuyến tính span{u1, ..., uk}, một không gian con.

Muốn biết w có thuộc span{u, v} không: viết au + bv = w theo từng tọa độ, được một hệ phương trình với ẩn a, b. Có nghiệm thì thuộc, vô nghiệm thì không.

Ví dụ u = (1, 0, 2), v = (2, 1, 3), w = (4, 1, 7): a + 2b = 4, b = 1, 2a + 3b = 7. Từ hai phương trình đầu a = 2, b = 1; phương trình thứ ba cũng đúng, nên w = 2u + v.

Với ba vectơ của R^3, có một cách nhanh: w thuộc span{u, v} (u, v không cùng phương) khi và chỉ khi ma trận có ba hàng u, v, w có định thức bằng 0.

> Lỗi thường gặp: giải hai phương trình rồi kết luận ngay. Nghiệm phải thỏa MỌI phương trình của hệ.

## Độc lập và phụ thuộc tuyến tính

Họ u1, ..., uk độc lập tuyến tính khi tổ hợp bằng 0 chỉ có thể có mọi hệ số bằng 0:

$$ a_{1}u_{1} + \ldots + a_{k}u_{k} = 0 \Rightarrow a_{1} = \ldots = a_{k} = 0 $$

Ngược lại thì họ phụ thuộc tuyến tính: có một vectơ là tổ hợp của các vectơ còn lại (nhưng không nhất thiết là vectơ cuối).

Cách xét: lập ma trận có các cột (hoặc các hàng) là các vectơ, khử Gauss. Họ độc lập khi hạng bằng số vectơ; với n vectơ của R^n, khi định thức khác 0.

:::matrix
A = 1 2 1 ; 0 1 3 ; 2 m 5
:::

Ba hàng của A phụ thuộc khi det A = 15 - 3m = 0, tức m = 5.

Hai dấu hiệu nhanh: họ có vectơ 0 luôn phụ thuộc; trong R^n mọi họ nhiều hơn n vectơ đều phụ thuộc.

> Lỗi thường gặp: thấy hệ "có nghiệm a = b = c = 0" rồi kết luận độc lập. Hệ thuần nhất nào cũng có nghiệm đó; câu hỏi là nó có nghiệm KHÁC 0 hay không.

## Cơ sở và số chiều

Một cơ sở của V là một họ vừa độc lập tuyến tính vừa sinh ra V. Mọi cơ sở của V có cùng số vectơ, gọi là số chiều dim V.

$$ \text{dim} \, \mathbb{R}^{n} = n, \qquad \text{dim} \, \text{span}\{u_{1}, \ldots, u_{k}\} = \text{rank} \, A $$

với A là ma trận có các hàng u1, ..., uk.

Tìm cơ sở của span: khử Gauss ma trận có các vectơ làm cột; các cột có trụ của CHÍNH ma trận ban đầu là một cơ sở.

Tìm cơ sở của không gian nghiệm Ax = 0: giải theo ẩn tự do, mỗi ẩn tự do cho một vectơ cơ sở. Số chiều bằng số ẩn trừ hạng.

$$ \text{dim} \{x : Ax = 0\} = n - \text{rank} \, A $$

Ví dụ W = {x - 2y + 3z = 0}: x = 2y - 3z nên (x, y, z) = y(2, 1, 0) + z(-3, 0, 1); cơ sở gồm hai vectơ đó, dim W = 2.

Với hai không gian con U, W:

$$ \text{dim}(U + W) = \text{dim} \, U + \text{dim} \, W - \text{dim}(U \cap W) $$

> Lỗi thường gặp: nói số chiều bằng số ẩn hay số tọa độ. Số chiều là số vectơ của một cơ sở.

## Tọa độ và ma trận chuyển cơ sở

Nếu B = {b1, ..., bn} là cơ sở của V thì mỗi x viết được duy nhất x = a1 b1 + ... + an bn; bộ (a1, ..., an) là tọa độ [x]_B.

Trong R^n: đặt b1, ..., bn làm các CỘT của ma trận P, khi đó

$$ x = P \, [x]_{B}, \qquad [x]_{B} = P^{-1} x $$

Ví dụ b1 = (2, 1), b2 = (3, 2), x = (5, 3):

:::matrix
P = 2 3 ; 1 2
:::

det P = 1, P^(-1) có hàng (2, -3) và (-1, 2), nên [x]_B = (1, 1). Thử lại: b1 + b2 = (5, 3).

Đổi giữa hai cơ sở B và B': nếu P có cột j là tọa độ của vectơ thứ j của B' trong B, thì

$$ [x]_{B} = P \, [x]_{B'}, \qquad [x]_{B'} = P^{-1} [x]_{B} $$

Với đa thức, so sánh hệ số: 5 + 4x + x^2 = 1 . 1 + 3(1 + x) + 1(1 + x + x^2), nên tọa độ trong cơ sở 1, 1 + x, 1 + x + x^2 là (1, 3, 1).

> Lỗi thường gặp: đặt các vectơ cơ sở làm HÀNG của P. Tổ hợp a b1 + b b2 là P nhân (a, b) chỉ khi b1, b2 là các cột.
