---
id: gt_lib_t5
title_vi: Định lý về hàm khả vi, khai triển Taylor và quy tắc L'Hospital
subject: giai_tich
floor: 5
summary_vi: Các định lý giá trị trung bình nối đạo hàm với sự thay đổi của hàm; khai triển Taylor thay một hàm bằng đa thức gần nó; và quy tắc L'Hospital cùng các khai triển đó giải các giới hạn vô định.
skills: [gt_t5_rolle_lagrange, gt_t5_taylor, gt_t5_maclaurin, gt_t5_lhospital, gt_t5_dang_vo_dinh]
---
## Định lý Rolle, Lagrange và Cauchy

Ba định lý cùng một giả thiết nền: f liên tục trên đoạn [a, b] và khả vi trên khoảng (a, b). Thiếu một trong hai, định lý có thể sai.

Định lý Rolle: nếu thêm f(a) = f(b) thì có c thuộc (a, b) với f'(c) = 0. Đồ thị đi rồi quay về cùng độ cao thì phải có chỗ nằm ngang.

Định lý Lagrange: có c thuộc (a, b) với

$$ f'(c) = \frac{f(b) - f(a)}{b - a} $$

nghĩa là có một tiếp tuyến song song với dây cung nối hai đầu. Ví dụ f(x) = x^3 trên [-1, 2]: dây cung có hệ số góc 9/3 = 3, giải 3c^2 = 3 được c = 1 hoặc c = -1; chỉ c = 1 nằm trong khoảng mở.

Định lý Cauchy cho hai hàm f, g (g' khác 0 trên khoảng): có c với

$$ \frac{f(b) - f(a)}{g(b) - g(a)} = \frac{f'(c)}{g'(c)} $$

Hai cách dùng hay gặp:

- Chặn số gia: nếu |f'(x)| <= M thì |f(b) - f(a)| <= M |b - a|. Ví dụ |sin b - sin a| <= |b - a|.
- Đếm nghiệm: giữa hai nghiệm của f có một nghiệm của f'. Nếu f' không bao giờ bằng 0 thì f có nhiều nhất một nghiệm.

> Lỗi thường gặp: dùng Rolle cho |x| trên [-1, 1] dù |x| không khả vi tại 0, hoặc nhận cả c ở đầu mút. Kiểm tra đủ giả thiết, và c phải nằm trong khoảng mở.

## Khai triển Taylor

Nếu f có đạo hàm tới cấp n tại a, đa thức Taylor bậc n của f quanh a là đa thức có cùng giá trị và cùng các đạo hàm tới cấp n với f tại a:

$$ f(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x - a)^k + R_n(x) $$

Phần dư dạng Peano: R_n(x) = o((x - a)^n), tức nhỏ hơn hẳn (x - a)^n khi x -> a. Phần dư dạng Lagrange, khi f có đạo hàm cấp n + 1:

$$ R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x - a)^{n+1} $$

với c nằm giữa a và x. Dạng này dùng để chặn sai số: thay e^x bằng 1 + x + x^2/2 trên [0, 1], sai số là e^c x^3/6 <= e/6 < 1/2.

Ví dụ ln x quanh 1: f(1) = 0, f'(1) = 1, f''(1) = -1, nên ln x = (x - 1) - (x - 1)^2/2 + o((x - 1)^2).

Một đa thức bậc n chính là đa thức Taylor bậc n của nó quanh mọi điểm: phần dư bằng 0.

> Lỗi thường gặp: quên chia cho k!, chẳng hạn viết số hạng bậc hai của e^x quanh 1 là e(x - 1)^2 thay vì (e/2)(x - 1)^2.

## Khai triển Maclaurin của các hàm cơ bản

Khai triển Taylor quanh a = 0 gọi là khai triển Maclaurin. Năm khai triển cần thuộc:

$$ e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots + \frac{x^n}{n!} + o(x^n) $$

$$ \sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \qquad \cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots $$

$$ \ln(1 + x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots + (-1)^{n-1}\frac{x^n}{n} + o(x^n) $$

$$ (1 + x)^{\alpha} = 1 + \alpha x + \frac{\alpha(\alpha - 1)}{2!}x^2 + \cdots + o(x^n) $$

Từ đó ghép ra khai triển của hàm phức tạp hơn:

- Thay biến: sin(2x) = 2x - (2x)^3/6 + ... = 2x - (4/3)x^3 + ...; nhớ lũy thừa cả hệ số.
- Nhân: e^(x^2) cos x, nhân hai khai triển rồi gom các số hạng cùng bậc; hệ số x^4 là 1/24 - 1/2 + 1/2 = 1/24.
- Đọc ngược đạo hàm: hệ số của x^n bằng f^(n)(0)/n!. Từ x^2 sin x = x^3 - x^5/6 + ... suy ra f^(5)(0) = -120/6 = -20.

sin x lẻ nên chỉ có lũy thừa lẻ; cos x chẵn nên chỉ có lũy thừa chẵn.

> Lỗi thường gặp: thay u = 2x vào ln(1 + u) mà chỉ đổi u thành 2x ở chỗ đầu, viết u^2/2 thành 2x^2/2. Đúng phải là (2x)^2/2 = 2x^2.

## Quy tắc L'Hospital

Khi giới hạn của f/g có dạng 0/0 hoặc vô cùng/vô cùng, và f, g khả vi quanh điểm đang xét với g' khác 0:

$$ \lim \frac{f(x)}{g(x)} = \lim \frac{f'(x)}{g'(x)} $$

nếu giới hạn bên phải tồn tại (hữu hạn hoặc vô cùng). Lấy đạo hàm riêng tử, riêng mẫu; không phải đạo hàm của cả phân thức.

Ví dụ:

1. (x^3 - 1)/ln x khi x -> 1: dạng 0/0, chuyển thành 3x^2/(1/x) = 3x^3 -> 3.
2. ln x / x khi x -> +vô cùng: dạng vô cùng/vô cùng, chuyển thành (1/x)/1 -> 0.
3. x^2/e^x khi x -> +vô cùng: dùng hai lần, được 2/e^x -> 0.

Sau mỗi lần dùng, kiểm tra lại dạng. Khi đã ra một số chia một số khác 0, dừng.

Quy tắc chỉ đi một chiều: nếu f'/g' không có giới hạn, chưa kết luận được gì về f/g. (x + sin x)/x có đạo hàm tử trên mẫu là 1 + cos x, dao động mãi, nhưng (x + sin x)/x = 1 + sin x / x -> 1.

> Lỗi thường gặp: dùng L'Hospital khi không có dạng vô định. (x^2 + 1)/(x + 1) khi x -> 1 bằng 2/2 = 1, còn lấy đạo hàm sẽ ra 2, sai.

## Các dạng vô định khác

Các dạng 0 . vô cùng, vô cùng - vô cùng, 1 mũ vô cùng, 0 mũ 0, vô cùng mũ 0 đều được đưa về 0/0 hoặc vô cùng/vô cùng.

- 0 . vô cùng: chuyển một thừa số xuống mẫu. x ln x = ln x / (1/x) -> 0 khi x -> 0+.
- vô cùng - vô cùng: quy đồng. 1/sin^2 x - 1/x^2 = (x^2 - sin^2 x)/(x^2 sin^2 x) -> 1/3.
- Ba dạng mũ: viết u^v = e^(v ln u), tính giới hạn của số mũ v ln u, rồi trả lại hàm mũ.

$$ \lim u(x)^{v(x)} = e^{\lim v(x)\ln u(x)} $$

Ví dụ (1 + 2/x)^x khi x -> +vô cùng: số mũ x ln(1 + 2/x) -> 2, nên giới hạn bằng e^2. Ví dụ x^x khi x -> 0+: số mũ x ln x -> 0, nên giới hạn bằng 1.

Dạng 1 mũ vô cùng còn có lối tắt: nếu u -> 1 và v(u - 1) -> k thì u^v -> e^k.

Khai triển Maclaurin thường nhanh hơn L'Hospital nhiều lần liên tiếp: (e^x - 1 - x)/x^2 = (x^2/2 + o(x^2))/x^2 -> 1/2.

> Lỗi thường gặp: tính xong giới hạn của số mũ rồi quên lấy e mũ, như kết luận (cos x)^(1/x^2) -> -1/2 thay vì e^(-1/2). Và coi 1 mũ vô cùng là 1: (1 + 1/x)^x -> e, không phải 1.
