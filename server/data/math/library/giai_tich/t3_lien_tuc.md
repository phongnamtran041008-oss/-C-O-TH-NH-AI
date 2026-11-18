---
id: gt_lib_t3
title_vi: Hàm liên tục và điểm gián đoạn
subject: giai_tich
floor: 3
summary_vi: Một hàm liên tục là hàm vẽ được không nhấc bút; học cách kiểm tra điều đó tại một điểm, nối các mảnh của hàm cho liền, gọi tên chỗ đứt, và dùng sự liền mạch để tìm nghiệm.
skills: [gt_t3_lien_tuc_diem, gt_t3_mot_phia, gt_t3_tim_tham_so, gt_t3_phan_loai_gian_doan, gt_t3_lien_tuc_doan]
---
## Liên tục tại một điểm

Hàm f liên tục tại a khi giá trị tại a khớp đúng với nơi các giá trị gần đó tiến tới:

$$ \lim_{x \to a} f(x) = f(a) $$

Đẳng thức này gói ba điều, thiếu một điều là hỏng:

1. f(a) có nghĩa.
2. Giới hạn của f khi x -> a tồn tại (hữu hạn).
3. Hai số đó bằng nhau.

Mọi hàm sơ cấp liên tục tại mọi điểm của tập xác định. Tổng, hiệu, tích của hai hàm liên tục là liên tục; thương cũng vậy ở những điểm mẫu khác 0; hàm hợp của các hàm liên tục là liên tục. Vì vậy (x^2 + 1)/(x - 3) liên tục tại 1, còn sin(x^2 + 1) liên tục trên cả R.

Ví dụ: f(x) = (x^2 - 4)/(x - 2) với x khác 2 và f(2) = 4. Rút gọn được f(x) = x + 2 khi x khác 2, nên giới hạn tại 2 bằng 4, đúng bằng f(2): f liên tục tại 2. Nếu đề cho f(2) = 5 thì f không liên tục tại 2.

Khi một hàm chưa xác định tại a nhưng có giới hạn hữu hạn L ở đó, gán f(a) = L sẽ làm nó liên tục tại a.

> Lỗi thường gặp: tính ra giới hạn khác f(a) mà vẫn kết luận liên tục. Liên tục đòi hỏi hai số phải bằng nhau.

## Giới hạn một phía và liên tục một phía

Giới hạn trái tại a chỉ xét các x < a, giới hạn phải chỉ xét các x > a. Giới hạn tại a tồn tại khi và chỉ khi hai giới hạn một phía tồn tại và bằng nhau:

$$ \lim_{x \to a} f(x) = L \;\Leftrightarrow\; \lim_{x \to a^{-}} f(x) = \lim_{x \to a^{+}} f(x) = L $$

Với hàm cho bởi nhiều công thức, mỗi phía dùng công thức của phía đó. Ví dụ f(x) = x + 1 khi x < 0, f(0) = 5, f(x) = x^2 + 3 khi x > 0: giới hạn trái là 1, giới hạn phải là 3, f(0) = 5.

Giá trị tuyệt đối cũng tách thành hai phía: |x - a| = x - a khi x > a và = -(x - a) khi x < a. Ví dụ (x^2 - 1)/|x - 1| bằng -(x + 1) bên trái 1 và x + 1 bên phải 1, nên giới hạn trái là -2, giới hạn phải là 2.

f liên tục trái tại a khi giới hạn trái bằng f(a), liên tục phải khi giới hạn phải bằng f(a). sqrt(x) chỉ có phía phải tại 0 và liên tục phải ở đó.

> Lỗi thường gặp: bỏ dấu giá trị tuyệt đối mà quên đổi dấu ở phía x < a.

## Tìm tham số để hàm liên tục

Bài kiểu này cho một hàm nhiều mảnh có chứa tham số. Bên trong mỗi khoảng, mỗi mảnh là hàm sơ cấp nên đã liên tục; chỉ cần lo các điểm nối.

Tại điểm nối c, viết giới hạn trái, giới hạn phải và f(c), rồi cho chúng bằng nhau:

1. Với f(x) = ax + 1 khi x < 2 và f(x) = x^2 khi x >= 2: giới hạn trái là 2a + 1.
2. Giới hạn phải và f(2) đều bằng 4.
3. Giải 2a + 1 = 4 được a = 3/2.

Khi một mảnh là một giá trị riêng tại một điểm, như f(x) = sin(4x)/x khi x khác 0 và f(0) = a, chỉ cần a bằng giới hạn của mảnh còn lại: sin(4x)/x dần tới 4, nên a = 4.

Có hai tham số thì cần hai phương trình, thường từ hai điểm nối khác nhau, rồi giải hệ.

Không phải lúc nào cũng tìm được tham số: nếu giới hạn tại điểm nối là vô cùng hoặc không tồn tại, không giá trị nào làm hàm liên tục ở đó.

> Lỗi thường gặp: chuyển vế sai dấu khi giải phương trình nối, chẳng hạn từ 4m + 1 = 6 - m viết ra 3m = 5. Thay lại đáp số vào cả hai mảnh để kiểm tra.

## Phân loại điểm gián đoạn

f gián đoạn tại a khi f không liên tục ở đó. Gọi tên chỗ đứt bằng hai giới hạn một phía:

- Gián đoạn khử được: giới hạn tại a tồn tại hữu hạn, nhưng f(a) không có hoặc khác giới hạn. Gán lại f(a) là liền.
- Gián đoạn loại một: hai giới hạn một phía đều hữu hạn nhưng khác nhau. Hiệu của chúng là bước nhảy.
- Gián đoạn loại hai: ít nhất một giới hạn một phía bằng vô cùng hoặc không tồn tại.

Bước nhảy tính bằng giới hạn phải trừ giới hạn trái:

$$ \lim_{x \to a^{+}} f(x) - \lim_{x \to a^{-}} f(x) $$

Ví dụ: sin x / x tại 0 khử được (giới hạn 1); |x|/x tại 0 loại một, bước nhảy 2; 1/x tại 0 loại hai; sin(1/x) tại 0 cũng loại hai vì dao động mãi không có giới hạn.

Với phân thức, điểm gián đoạn là nơi mẫu bằng 0. Rút gọn thừa số chung: nơi nào rút gọn xong mẫu hết bằng 0 thì khử được, nơi nào mẫu vẫn bằng 0 còn tử khác 0 thì loại hai. Ví dụ (x^2 - 1)/(x^2 + x) rút gọn còn (x - 1)/x: x = -1 khử được, x = 0 loại hai.

> Lỗi thường gặp: thấy hai phía cùng ra +vô cùng rồi gọi là khử được. Khử được cần giới hạn hữu hạn; giới hạn vô cùng luôn là loại hai.

## Hàm liên tục trên đoạn và giá trị trung gian

Hàm liên tục trên cả đoạn [a, b] có hai tính chất mạnh. Thứ nhất, nó đạt giá trị lớn nhất và nhỏ nhất trên đoạn. Thứ hai, nó nhận mọi giá trị nằm giữa f(a) và f(b). Hệ quả dùng nhiều nhất:

$$ f(a) \cdot f(b) < 0 \;\Rightarrow\; \exists\, c \in (a, b) : f(c) = 0 $$

Muốn chứng minh một phương trình có nghiệm trong (a, b):

1. Chuyển về dạng g(x) = 0.
2. Chỉ ra g liên tục trên [a, b].
3. Tính g(a) và g(b), thấy trái dấu.
4. Kết luận theo định lý giá trị trung gian.

Ví dụ cos x = x: g(x) = cos x - x có g(0) = 1 > 0 và g(pi/2) = -pi/2 < 0, nên có nghiệm trong (0, pi/2).

Phương pháp chia đôi dùng đúng ý đó để khoanh nghiệm: lấy điểm giữa, xem dấu, giữ nửa đoạn mà hai đầu còn trái dấu. Với x^3 - 2 trên [1, 2]: tại 1.5 giá trị dương nên giữ (1, 1.5); tại 1.25 giá trị âm nên giữ (1.25, 1.5). Mỗi bước, khoảng chứa nghiệm ngắn đi một nửa.

Định lý chỉ nói có ít nhất một nghiệm. Nếu thêm hàm tăng ngặt (chẳng hạn x^3 + ax + b với a > 0) thì nghiệm là duy nhất.

> Lỗi thường gặp: quên điều kiện liên tục. 1/x đổi dấu từ -1 lên 1 nhưng không bao giờ bằng 0, vì nó đứt tại 0.
