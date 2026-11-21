---
id: gt_lib_t3
title_vi: Hàm liên tục và điểm gián đoạn
subject: giai_tich
floor: 3
format: 2
summary_vi: Hàm liên tục là hàm vẽ một nét không nhấc bút: kiểm tra tại một điểm, nhìn từng phía, chỉnh tham số cho các mảnh nối khít, gọi tên chỗ đứt, và dùng nét liền để săn nghiệm.
skills: [gt_t3_lien_tuc_diem, gt_t3_mot_phia, gt_t3_tim_tham_so, gt_t3_phan_loai_gian_doan, gt_t3_lien_tuc_doan]
---
## Liên tục tại một điểm

:::hook
Nhiệt độ trong ngày đi từ 20 lên 30 độ thì phải qua 25 độ, không nhảy cóc. Hàm liên tục là hàm vẽ được không nhấc bút: x nhích một chút thì f chỉ nhích một chút.
:::

:::figure plane
caption: Đồ thị đi tới độ cao 4 tại x = 2 (chấm rỗng), nhưng f(2) lại đặt ở 5 (chấm đặc): đứt. Dời chấm đặc về 4 là liền.
size: 140 100
x: -1 4 1
y: -1 6 1
curve "x + 2" xanh
point 2 4 do open
point 2 5 do "f(2) = 5" pos=w
drop 2 4
:::

:::core
f liên tục tại a khi f(a) đúng bằng chỗ đồ thị đang tiến tới. Cần đủ ba điều: f(a) có, giới hạn có, hai số bằng nhau.
:::

$$ \lim_{x \to a} f(x) = f(a) $$

Ví dụ: f(x) = (x^3 - 8)/(x - 2) khi x khác 2. Gán f(2) bằng bao nhiêu để f liên tục tại 2?

1. Cần f(2) bằng giới hạn của f tại 2.
2. x^3 - 8 = (x - 2)(x^2 + 2x + 4), rút gọn còn x^2 + 2x + 4.
3. Cho x -> 2: 4 + 4 + 4 = 12. Gán f(2) = 12.

Hàm sơ cấp (đa thức, phân thức, căn, mũ, log, sin, ...) liên tục tại mọi điểm thuộc tập xác định. Cộng, trừ, nhân, lấy hàm hợp vẫn liên tục; chia thì trừ chỗ mẫu bằng 0. Vì vậy (x^2 + 1)/(x - 4) liên tục tại 1, còn tan x đứt tại pi/2. |x| liên tục tại 0, dù đồ thị có góc nhọn.

> Lỗi thường gặp: tính ra giới hạn khác f(a) mà vẫn kết luận liên tục. Liên tục đòi hai số phải bằng nhau.

:::check
Q: f(x) = (x^2 - 5x)/x khi x khác 0, và f(0) = 5. f có liên tục tại 0 không?
A: Không. Rút gọn được x - 5, giới hạn tại 0 là -5, khác f(0) = 5.
:::

## Giới hạn một phía và liên tục một phía

:::hook
Đèn giao thông đổi màu lúc 8 giờ: ngay trước là xanh, ngay sau là đỏ. Nhìn từ hai phía cho hai câu trả lời khác nhau, nên phải hỏi riêng từng phía.
:::

:::figure plane
caption: Từ trái, đồ thị tiến tới 2 (chấm rỗng); từ phải tới 3 = f(1). Hai phía lệch nhau: không có giới hạn tại 1, nhưng f liên tục phải.
size: 140 100
x: -1 2.5 1
y: -0.5 7 1
curve "x + 1" xanh "x + 1" -1 1 pos=nw
curve "x^2 + 2" luc "x^2 + 2" 1 2.2 pos=e
point 1 2 do open
point 1 3 do
:::

:::core
Giới hạn trái chỉ nhìn x < a, giới hạn phải chỉ nhìn x > a. Giới hạn tại a tồn tại khi và chỉ khi hai phía cho cùng một số.
:::

$$ \lim_{x \to a} f(x) = L \;\Leftrightarrow\; \lim_{x \to a^{-}} f(x) = \lim_{x \to a^{+}} f(x) = L $$

Ví dụ: f(x) = (x^2 - 4)/|x - 2|. Tìm hai giới hạn một phía tại 2.

1. x < 2: x - 2 âm, nên |x - 2| = -(x - 2) và f(x) = -(x + 2) -> -4.
2. x > 2: |x - 2| = x - 2, nên f(x) = x + 2 -> 4.
3. Hai phía -4 và 4 khác nhau: không có giới hạn tại 2.

Hàm nhiều công thức: mỗi phía dùng công thức của phía đó, f(a) dùng công thức có dấu bằng. Liên tục trái nghĩa là giới hạn trái = f(a); liên tục phải tương tự. sqrt(x) chỉ sống bên phải 0 và liên tục phải ở đó. Với mũ 1/x: x -> 0 từ trái thì 1/x -> -vô cùng nên 2^(1/x) -> 0; từ phải thì 2^(1/x) -> +vô cùng.

> Lỗi thường gặp: bỏ dấu giá trị tuyệt đối mà quên đổi dấu ở phía x < a.

:::check
Q: f(x) = 3x - 1 khi x < 2, f(2) = 4, f(x) = x^2 + 1 khi x > 2. f có giới hạn tại 2 không? Có liên tục không?
A: Trái 5, phải 5: giới hạn bằng 5. Nhưng f(2) = 4 khác 5, nên không liên tục, kể cả một phía.
:::

## Tìm tham số để hàm liên tục

:::hook
Hai đoạn đường ray nối nhau thì đầu ray phải khớp, lệch một chút là tàu trật bánh. Tìm tham số để hàm liên tục là chỉnh mối nối cho hai mảnh gặp đúng một điểm.
:::

:::figure plane
caption: Mảnh phải chạm độ cao 3 tại x = 2. Mảnh trái ax - 1 với a = 1 chỉ tới 1, hở; với a = 2 tới đúng 3, liền.
size: 160 110
x: -0.5 3.2 1
y: -2 8 1
curve "x - 1" xam "a = 1" -0.5 2 pos=e
curve "2*x - 1" luc "a = 2" -0.5 2 pos=nw
curve "x^2 - 1" xanh "x^2 - 1" 2 3.2 pos=e
point 2 1 xam open
point 2 3 do
:::

:::core
Bên trong mỗi khoảng, mỗi mảnh đã liền; chỉ mối nối có thể hở. Cho giới hạn trái = giới hạn phải = f(c), rồi giải ra tham số.
:::

Ví dụ: f(x) = ax - 1 khi x < 2, f(x) = x^2 - 1 khi x >= 2. Tìm a để f liên tục trên R.

1. Mỗi mảnh là đa thức: chỉ cần xét mối nối x = 2.
2. Giới hạn phải và f(2): 2^2 - 1 = 3. Giới hạn trái: 2a - 1.
3. 2a - 1 = 3 nên a = 2. Thử lại: 2 . 2 - 1 = 3, khớp.

Khi tham số là một giá trị riêng f(c) = a, chỉ cần a bằng giới hạn của phần còn lại: sin(4x)/x -> 4 nên a = 4. Hai tham số thì cần hai mối nối, giải hệ hai phương trình. Nếu giới hạn tại mối nối là vô cùng, như 1/(x - 1) tại 1, thì không a nào nối được.

> Lỗi thường gặp: chuyển vế sai dấu khi giải phương trình nối. Luôn thay đáp số vào cả hai mảnh để thử.

:::check
Q: f(x) = 2x + 3 khi x < 1, f(x) = mx^2 + 1 khi x >= 1. Tìm m để f liên tục.
A: Trái: 2 + 3 = 5. Phải và f(1): m + 1. Cho bằng nhau: m = 4.
:::

## Phân loại điểm gián đoạn

:::hook
Tín hiệu cảm biến có thể hỏng ba kiểu: mất một điểm đo (vá được), nhảy bậc đột ngột, hay vọt lên vô cùng. Gọi đúng tên chỗ đứt thì biết có sửa được không.
:::

:::figure plane
caption: Khử được: chỉ thiếu một điểm, vá vào là liền.
size: 100 80
x: -1 3 1
y: -1 4 1
curve "x + 1" xanh
point 1 2 do open
:::

:::figure plane
caption: Loại một: hai phía hữu hạn mà lệch nhau, có bước nhảy.
size: 100 80
x: -1 3 1
y: -1 4 1
curve "x + 1" xanh -1 1
curve "x - 1" xanh 1 3
point 1 2 do open
point 1 0 do
:::

:::figure plane
caption: Loại hai: có phía vọt ra vô cùng (hoặc dao động mãi).
size: 100 80
x: -1 3 1
y: -1 6 1
curve "1/(x - 1)^2" xanh
line 1 -1 1 6 xam dash
:::

:::core
Nhìn hai giới hạn một phía: bằng nhau và hữu hạn là khử được; hữu hạn mà lệch là loại một; có phía vô cùng hay không tồn tại là loại hai.
:::

Ví dụ: phân loại các điểm gián đoạn của f(x) = (x^2 - 1)/(x^2 - 3x + 2).

1. Mẫu (x - 1)(x - 2) = 0 tại 1 và 2: hai điểm gián đoạn.
2. Tử (x - 1)(x + 1): rút (x - 1), còn (x + 1)/(x - 2).
3. Tại 1: giới hạn 2/(-1) = -2, hữu hạn: khử được.
4. Tại 2: mẫu vẫn -> 0 còn tử -> 3: loại hai.

$$ \lim_{x \to a^{+}} f(x) - \lim_{x \to a^{-}} f(x) $$

Bước nhảy (công thức trên) là phải trừ trái. |x|/x tại 0: -1 bên trái, 1 bên phải, bước nhảy 2. arctan(1/x) tại 0 nhảy từ -pi/2 lên pi/2: bước nhảy pi. sin(1/x) dao động mãi, e^(1/x) vọt lên bên phải: loại hai. Hai công thức khác nhau mà nối khít thì vẫn liên tục, không gián đoạn gì cả.

> Lỗi thường gặp: thấy hai phía cùng ra +vô cùng rồi gọi là khử được. Khử được cần giới hạn hữu hạn; vô cùng luôn là loại hai.

:::check
Q: f(x) = 2x + 1 khi x < 1, f(x) = 5 - x khi x >= 1. Phân loại x = 1 và tính bước nhảy.
A: Trái 3, phải 4: hữu hạn mà lệch, loại một. Bước nhảy = 4 - 3 = 1.
:::

## Hàm liên tục trên đoạn và giá trị trung gian

:::hook
Leo từ chân núi (0 m) lên đỉnh (1000 m), đường vòng vèo đến đâu bạn cũng phải qua độ cao 500 m. Máy tính dùng đúng ý này để săn nghiệm phương trình.
:::

:::figure plane
caption: f(1) âm, f(2) dương, đồ thị liền nét: nó buộc phải cắt trục hoành ở một điểm c giữa 1 và 2.
size: 150 110
x: 0.5 2.3 0.5
y: -3 6 1
curve "x^3 - 3" xanh "x^3 - 3" 0.8 2.1 pos=w
point 1 -2 do "f(1) = -2" pos=e
point 2 5 luc "f(2) = 5" pos=w
point 1.442 0 muc "c" pos=nw
:::

:::core
Hàm liền nét trên [a, b] không thể đi từ âm sang dương mà không chạm 0: f(a) . f(b) < 0 thì có nghiệm trong (a, b).
:::

$$ f(a) \cdot f(b) < 0 \;\Rightarrow\; \exists\, c \in (a, b) : f(c) = 0 $$

Ví dụ (chia đôi): khoanh nghiệm của x^3 - 3 = 0 trong [1, 2].

1. f(1) = -2 < 0, f(2) = 5 > 0: có nghiệm trong (1, 2).
2. Điểm giữa 1.5: f(1.5) = 0.375 > 0, giữ (1, 1.5).
3. Điểm giữa 1.25: f(1.25) xấp xỉ -1.05 < 0, giữ (1.25, 1.5).
4. Mỗi bước khoảng ngắn đi một nửa; nghiệm thật khoảng 1.442.

Định lý cần liền nét trên cả đoạn: 1/x đổi dấu trên [-1, 1] mà không bao giờ bằng 0, vì đứt tại 0. Liên tục trên đoạn đóng còn đạt giá trị lớn nhất và nhỏ nhất; x trên khoảng mở (0, 1) thì không đạt 1. Định lý chỉ hứa ít nhất một nghiệm; hàm tăng ngặt thì đúng một. Tìm khoảng (k, k + 1): thử các số nguyên liên tiếp tới khi đổi dấu.

> Lỗi thường gặp: thấy f(a) và f(b) cùng dấu rồi kết luận vô nghiệm. Định lý khi đó không nói gì; x^2 - 1 trên [-2, 2] vẫn có hai nghiệm.

:::check
Q: p(x) = x^3 + 2x + 5 tăng ngặt nên có đúng một nghiệm. Tìm số nguyên k để nghiệm nằm trong (k, k + 1).
A: p(-2) = -7 < 0, p(-1) = 2 > 0: đổi dấu, nên k = -2.
:::
