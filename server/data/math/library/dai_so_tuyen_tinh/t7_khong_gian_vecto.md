---
id: dstt_lib_t7
title_vi: Không gian vectơ
subject: dai_so_tuyen_tinh
floor: 7
format: 2
summary_vi: Không gian vectơ là nơi cộng và nhân với số không bao giờ rơi ra ngoài; span là mọi điểm đi tới được từ vài hướng, độc lập là không hướng nào thừa, cơ sở là bộ hướng vừa đủ, tọa độ là công thức nấu theo bộ hướng đó.
skills: [dstt_t7_khong_gian_vecto, dstt_t7_khong_gian_con, dstt_t7_to_hop_tuyen_tinh, dstt_t7_doc_lap_tuyen_tinh, dstt_t7_co_so_so_chieu, dstt_t7_toa_do]
---
## Không gian vectơ và các tiên đề

:::hook
Ảnh, đoạn âm thanh, đa thức, bảng trọng số của mạng nơ-ron: máy học cộng chúng và nhân chúng với số như cộng mũi tên. Mọi thứ chơi được trò đó đều là không gian vectơ.
:::

:::figure plane
caption: Nửa mặt phẳng x > 0 (vàng) không là không gian vectơ: u ở trong nhưng (-1)u rơi ra ngoài.
size: 150 110
x: -2.5 2.5 1
y: -2 2 1
poly 0 -2 2.5 -2 2.5 2 0 2 vang
vector 0 0 1.5 1 xanh "u" pos=e
vector 0 0 -1.5 -1 do "(-1)u" pos=w
:::

:::core
Không gian vectơ là một tập mà cộng hai phần tử hay nhân một phần tử với số không bao giờ đưa ra ngoài, và các luật cộng, nhân quen thuộc vẫn đúng.
:::

Tám tiên đề chỉ là luật quen của số: giao hoán, kết hợp, có vectơ 0, có vectơ đối -u, hai luật phân phối, (kl)u = k(lu) và 1u = u. Từ tiên đề suy ra 0u = 0 và (-1)u = -u.

:::check
Q: Tập các điểm có tọa độ nguyên trong R^2, với phép toán thông thường, có là không gian vectơ không?
A: Không: cộng thì vẫn nguyên, nhưng (1/2).(1, 0) = (1/2, 0) rơi ra ngoài.
:::

### Bác bỏ bằng một phản ví dụ

Muốn bác bỏ thì chỉ cần một tiên đề sai ở một ví dụ cụ thể.

Ví dụ: R^2 với cộng thường nhưng k.(x, y) = (kx, y). Có là không gian vectơ?

1. Lấy u = (1, 1), k = l = 1.
2. (1 + 1).u = 2.(1, 1) = (2, 1).
3. 1.u + 1.u = (1, 1) + (1, 1) = (2, 2). Khác nhau: không phải.

$$ (k + l)u = ku + lu, \qquad k(u + v) = ku + kv $$

> Lỗi thường gặp: gộp 1u + (-1)u bằng luật (kl)u = k(lu). Đây là tổng hai vectơ, phải dùng (k + l)u = ku + lu: được (1 + (-1))u = 0u = 0.

:::check
Q: R^2 với cộng thường nhưng k.(x, y) = (kx, 0). Tiên đề nào sai?
A: 1u = u sai: 1.(1, 1) = (1, 0), khác (1, 1).
:::

## Không gian con

:::hook
Mọi tổ hợp của các ảnh mẫu tạo thành một không gian con của mọi ảnh: chỗ dữ liệu sống. Nhận ra nó là bước đầu của nén dữ liệu.
:::

:::figure plane
caption: Đường y = x/2 qua gốc (xanh) là không gian con. Đường y = x/2 + 1 (đỏ) không chứa 0 nên không phải.
size: 150 110
x: -3 3 1
y: -2 2.5 1
line 0 0 2 1 xanh "W" pos=se
line 0 1 2 2 do dash
point 0 0 muc "0" pos=se
:::

:::core
Không gian con là một tập con kín: chứa 0, cộng hai phần tử hay nhân với số vẫn ở trong; trong R^n đó là gốc, đường thẳng hay mặt phẳng... đi qua gốc.
:::

Tập nghiệm của một hệ thuần nhất luôn là không gian con. Điều kiện có vế phải khác 0, có bình phương, tích, trị tuyệt đối hay bất đẳng thức thường làm tập mất tính kín. Giao hai không gian con vẫn là không gian con; hợp thì nói chung không.

:::check
Q: Tập nghiệm của x + y = 1 trong R^2 có là không gian con không?
A: Không: nó không chứa (0, 0), vì 0 + 0 khác 1.
:::

### Kiểm tra từng điều kiện

Ví dụ: tìm m để W = {(x, y, z) : 2x - y + z = m + 1} là không gian con.

1. W phải chứa (0, 0, 0): 0 = m + 1, nên m = -1.
2. Khi đó vế phải bằng 0: cộng hay nhân hai vế với số vẫn ra 0, W kín.

$$ u, v \in W \Rightarrow u + v \in W, \qquad u \in W \Rightarrow ku \in W $$

> Lỗi thường gặp: chỉ thấy u + v "có dạng (x, y, z)" rồi kết luận. Phải kiểm tra u + v thỏa đúng ĐIỀU KIỆN của W.

:::check
Q: W là hợp của hai đường x = 0 và y = x trong R^2. W có là không gian con không?
A: Không: (0, 1) và (1, 1) đều thuộc W, nhưng tổng (1, 2) không nằm trên đường nào.
:::

## Tổ hợp tuyến tính và bao tuyến tính

:::hook
Mỗi màu trên màn hình là a phần đỏ + b phần lục + c phần lam: một tổ hợp tuyến tính. Mọi màu pha được là bao tuyến tính của ba màu gốc.
:::

:::figure plane
caption: w = 2u + v: đi 2 bước theo u rồi 1 bước theo v. Mọi điểm tới được kiểu đó tạo thành span{u, v}.
size: 170 110
x: -1.5 4.5 1
y: -0.5 3.5 1
vector 0 0 2 1 do "u" pos=e
segment 2 1 4 2 do dash
vector 0 0 -1 1 xanh "v" pos=w
vector 4 2 3 3 xanh
vector 0 0 3 3 luc "w" pos=nw
:::

:::core
Hỏi w có thuộc span{u, v} không là hỏi hệ au + bv = w, mỗi tọa độ một phương trình, có nghiệm hay không.
:::

Span của các vectơ là mọi tổ hợp a_1 u_1 + ... + a_k u_k của chúng, luôn là một không gian con. Hệ có nhiều phương trình hơn ẩn: tìm a, b từ vài phương trình, rồi phải thử lại các phương trình còn lại.

Ví dụ: u = (1, 2, 0), v = (0, 1, 1), w = (2, m, 3). Tìm m để w thuộc span{u, v}.

1. au + bv = (a, 2a + b, b). Tọa độ 1 và 3 cho a = 2, b = 3.
2. Tọa độ 2 phải khớp: m = 2 . 2 + 3 = 7.

> Lỗi thường gặp: giải hai phương trình rồi kết luận ngay. Nghiệm phải thỏa MỌI phương trình của hệ.

:::check
Q: (2, 3, 4) có thuộc span{(1, 0, 1), (0, 1, 1)} không?
A: a(1, 0, 1) + b(0, 1, 1) = (a, b, a + b). Cần a = 2, b = 3 thì tọa độ 3 là 5, khác 4: không thuộc.
:::

## Độc lập và phụ thuộc tuyến tính

:::hook
Đưa vào mô hình hai đặc trưng "chiều cao (cm)" và "chiều cao (m)" là thừa: một cái là bội của cái kia. Phụ thuộc tuyến tính chính là có thông tin thừa như vậy.
:::

:::figure plane
caption: Không cùng phương: độc lập.
size: 120 100
x: -2.5 2.5 5
y: -2 2 5
vector 0 0 2 1 do "u" pos=e
vector 0 0 -1 1.5 xanh "v" pos=w
:::

:::figure plane
caption: v = -u nằm trên đường của u: phụ thuộc, v thừa.
size: 120 100
x: -2.5 2.5 5
y: -2 2 5
vector 0 0 2 1 do "u" pos=e
vector 0 0 -2 -1 xanh "v" pos=w
:::

:::core
Một họ độc lập khi không vectơ nào thừa, tức tổ hợp của chúng bằng 0 chỉ khi mọi hệ số đều bằng 0.
:::

$$ a_{1}u_{1} + \ldots + a_{k}u_{k} = 0 \Rightarrow a_{1} = \ldots = a_{k} = 0 $$

:::check
Q: u, v, w độc lập. Họ u + v, v - w, u + w có độc lập không?
A: Không: (u + v) - (v - w) = u + w, nên vectơ thứ ba là tổ hợp của hai vectơ đầu.
:::

### Xét bằng hạng hoặc định thức

Cách xét: xếp các vectơ thành ma trận rồi khử Gauss; họ độc lập khi hạng bằng số vectơ. Với n vectơ trong R^n, họ độc lập khi định thức khác 0. Họ có vectơ 0, hay có nhiều hơn n vectơ trong R^n, luôn phụ thuộc. Phụ thuộc chỉ nói CÓ một vectơ thừa, không nói là vectơ nào.

Ví dụ: tìm m để (1, 0, 2), (2, 1, m), (0, 1, 3) phụ thuộc.

1. Định thức của ma trận ba hàng đó: 1 . (3 - m) - 0 + 2 . (2 - 0) = 7 - m.
2. Phụ thuộc khi định thức bằng 0: m = 7.

> Lỗi thường gặp: thấy hệ có nghiệm a = b = c = 0 rồi kết luận độc lập. Hệ thuần nhất nào cũng có nghiệm đó; phải hỏi có nghiệm KHÁC 0 không.

:::check
Q: (1, 2) và (2, 5) trong R^2 có độc lập không?
A: Có: định thức 1 . 5 - 2 . 2 = 1 khác 0.
:::

## Cơ sở và số chiều

:::hook
Ảnh khuôn mặt có 10000 điểm ảnh, nhưng mọi khuôn mặt gần như nằm trong một không gian chỉ vài trăm chiều. Số chiều là số "núm vặn" thật sự cần.
:::

:::figure grid
caption: Đặt u1 = (1, 1, 2), u2 = (2, 2, 4), u3 = (1, 0, 1) làm cột rồi khử. Trụ (vàng) ở cột 1 và 3: u1, u3 là một cơ sở, số chiều 2.
style: matrix
table "u1 u2 u3"
row 1 2 1
row 1 2 0
row 2 4 1
mark col 1 vang
mark col 3 vang
op "->"
table "bậc thang"
row 1 2 1
row 0 0 -1
row 0 0 0
mark cell 1 1 vang
mark cell 2 3 vang
:::

:::core
Cơ sở là bộ hướng vừa đủ: sinh ra cả không gian và không thừa cái nào; số chiều là số vectơ của nó, như nhau với mọi cơ sở.
:::

Số chiều của span{u_1, ..., u_k} bằng hạng của ma trận lập từ chúng. Cơ sở lấy các cột có trụ của CHÍNH ma trận ban đầu, không phải của bậc thang.

:::check
Q: Bốn vectơ trong R^3 xếp thành ma trận có hạng 2. Span của chúng có mấy chiều? Bốn vectơ đó có độc lập không?
A: 2 chiều. Không độc lập: 4 vectơ mà chỉ 2 hướng thật.
:::

### Không gian nghiệm và công thức số chiều

Với không gian nghiệm của Ax = 0, mỗi ẩn tự do cho một vectơ cơ sở.

Ví dụ: cơ sở và số chiều của W = {(x, y, z) : x + 2y - z = 0}.

1. Một phương trình, z = x + 2y; x, y tự do.
2. (x, y, z) = x(1, 0, 1) + y(0, 1, 2).
3. Cơ sở (1, 0, 1), (0, 1, 2); dim W = 2: một mặt phẳng qua gốc.

$$ \text{dim} \{x : Ax = 0\} = n - \text{rank} \, A $$

$$ \text{dim}(U + W) = \text{dim} \, U + \text{dim} \, W - \text{dim}(U \cap W) $$

> Lỗi thường gặp: nói số chiều bằng số ẩn hay số tọa độ. Mặt phẳng ở trên nằm trong R^3 nhưng chỉ có 2 chiều.

:::check
Q: Hai mặt phẳng khác nhau qua gốc trong R^3 cắt nhau theo một đường thẳng. dim(U + W) là bao nhiêu?
A: 2 + 2 - 1 = 3: tổng của chúng là cả R^3.
:::

## Tọa độ và ma trận chuyển cơ sở

:::hook
Cùng một màu có mã RGB và mã HSV khác nhau. Đổi cơ sở là đổi cách gọi tên, không đổi vật.
:::

:::figure plane
caption: Đi 2 bước b1 = (2, 1) rồi 2 bước b2 = (0, 1) tới (4, 4): tọa độ là (2, 2).
size: 150 95
x: -1 4.5 1
y: -0.5 4.5 1
vector 0 0 2 1 do
text 1.3 1.1 "b1"
segment 2 1 4 2 do dash
vector 0 0 0 1 xanh
text -0.5 0.6 "b2"
vector 4 2 4 4 xanh
point 4 4 muc "(4, 4)" pos=w
:::

:::core
Tọa độ trong cơ sở B là công thức pha: cần bao nhiêu phần mỗi vectơ cơ sở để ra x; đặt các b_i làm CỘT của P thì x = P [x]_B.
:::

Đổi giữa hai cơ sở: P có cột j là tọa độ trong B của vectơ thứ j của B', thì [x]_B = P [x]_B'. Với đa thức, so sánh hệ số từng lũy thừa của x.

Ví dụ: tọa độ của x = (3, 7) trong cơ sở b1 = (1, 2), b2 = (1, 3).

1. P có cột b1, b2: P = [1, 1; 2, 3], det P = 1, nên P^(-1) = [3, -1; -2, 1].
2. [x]_B = P^(-1) x = (9 - 7, -6 + 7) = (2, 1). Thử: 2b1 + b2 = (3, 7).

$$ x = P \, [x]_{B}, \qquad [x]_{B} = P^{-1} x $$

> Lỗi thường gặp: đặt b1, b2 làm HÀNG của P. Tổ hợp a b1 + b b2 bằng P nhân (a, b) chỉ khi b1, b2 là các cột.

:::check
Q: Tọa độ của đa thức 3 + 2x trong cơ sở 1, 1 + x là gì?
A: a . 1 + b(1 + x) = (a + b) + bx: b = 2, a = 1. Tọa độ (1, 2).
:::
