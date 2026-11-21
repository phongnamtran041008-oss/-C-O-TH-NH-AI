---
id: gt_lib_t9
title_vi: Hàm nhiều biến
subject: giai_tich
floor: 9
format: 2
summary_vi: Hàm hai biến là một mặt địa hình: giới hạn phải đúng theo mọi đường, đạo hàm riêng là độ dốc dọc từng trục, gradient chỉ hướng lên dốc nhanh nhất, và lan truyền ngược là quy tắc dây chuyền chạy ngược trên đồ thị tính toán.
skills: [gt_t9_gioi_han_lien_tuc, gt_t9_dao_ham_rieng, gt_t9_vi_phan_ham_an, gt_t9_cuc_tri, gt_t9_cuc_tri_dieu_kien, gt_t9_gradient_lan_truyen]
---
## Miền xác định, giới hạn và liên tục

:::hook
Hàm loss của một mô hình hai trọng số là một mặt địa hình trên mặt phẳng. Đi tới một điểm có vô số lối vào, và giới hạn phải đúng theo mọi lối.
:::

:::figure plane
caption: xy/(x^2 + y^2): dọc trục x bằng 0, dọc y = x bằng 1/2. Hai lối, hai số.
size: 150 100
aspect: equal
x: -2 2 1
y: -1.5 1.5 1
line 0 0 1 0 xanh
line 0 0 1 1 do
text -1.3 0.3 "f = 0" xanh
text 1.4 0.6 "f = 1/2" do
point 0 0 muc open
:::

:::core
Giới hạn tại một điểm của mặt phẳng phải như nhau theo mọi đường đi tới; hai đường cho hai số khác nhau là không có giới hạn.
:::

Miền xác định: căn cần >= 0, ln cần > 0, mẫu khác 0. Liên tục tại (a, b): giới hạn bằng f(a, b).

Ví dụ: giới hạn của x^2 y/(x^2 + y^2) khi (x, y) -> (0, 0).

1. x^2 <= x^2 + y^2, nên x^2/(x^2 + y^2) <= 1.
2. Vậy |f| <= |y|, mọi đường đi đều thế.
3. |y| -> 0, kẹp lại: giới hạn bằng 0.

> Lỗi thường gặp: thử mọi đường thẳng rồi kết luận có giới hạn. x^2 y/(x^4 + y^2) cho 0 dọc mọi đường thẳng, nhưng 1/2 dọc parabol y = x^2.

:::check
Q: (x^2 - y^2)/(x^2 + y^2) có giới hạn tại (0, 0) không?
A: Không. Dọc trục x (y = 0) bằng 1, dọc trục y (x = 0) bằng -1.
:::

## Đạo hàm riêng

:::hook
Vặn một núm trên bàn trộn âm, giữ các núm khác yên: tiếng đổi bao nhiêu? Đó là đạo hàm riêng, mỗi lần chỉ cho một biến chạy.
:::

:::figure plane
caption: Lát y = 1 của z = x^2 y + y^3 là z = x^2 + 1; dốc tại x = 1 là f_x(1, 1) = 2.
size: 150 100
x: -1.5 2.2 1
y: -0.5 5 1
names: x z
curve "x^2 + 1" xanh "z = x^2 + 1" pos=w
tangent "x^2 + 1" 1 do len=34
point 1 2 do "dốc 2" pos=se
:::

:::core
Đạo hàm riêng theo x là đạo hàm thường khi coi mọi biến khác là hằng số: đi dọc trục x và đo độ dốc.
:::

$$ f_{xy} = \frac{\partial}{\partial y}\Big(\frac{\partial f}{\partial x}\Big), \qquad f_{xy} = f_{yx} $$

Hàm sơ cấp trơn thì f_xy = f_yx (Schwarz); điều kiện liên tục hỏng thì có thể khác.

Ví dụ: f = x^2 y^3 + 3xy. Tính f_xy(1, 1).

1. f_x = 2xy^3 + 3y (y đứng yên như hằng số).
2. f_xy = (f_x)_y = 6xy^2 + 3.
3. Tại (1, 1): 9. Tính f_y rồi lấy theo x cũng ra 9.

> Lỗi thường gặp: nhầm loại hàm. Với x^y, theo x là lũy thừa: y x^(y - 1); theo y là hàm mũ: x^y ln x.

:::check
Q: Tìm a để u = x^2 + a y^2 thỏa u_xx + u_yy = 0.
A: u_xx = 2, u_yy = 2a, nên 2 + 2a = 0: a = -1.
:::

## Vi phân toàn phần, hàm ẩn và công thức Taylor

:::hook
Đo một khoảnh ruộng linh thảo hình chữ nhật, cả hai cạnh đều lệch một chút: diện tích lệch bao nhiêu? Cộng phần lệch do từng cạnh.
:::

:::figure plane
caption: f = xy: x thêm dx góp dải y.dx, y thêm dy góp dải x.dy. Góc dx.dy quá nhỏ, bỏ.
size: 150 100
axes: off
x: -0.7 4.2
y: -0.6 3.2
poly 0 0 3 0 3 2 0 2 xanh "xy"
poly 3 0 4 0 4 2 3 2 vang "y.dx"
poly 0 2 3 2 3 3 0 3 luc "x.dy"
poly 3 2 4 2 4 3 3 3 do
text 1.5 -0.3 "x"
text 3.5 -0.3 "dx"
text -0.35 1 "y"
text -0.35 2.5 "dy"
:::

:::core
Vi phân toàn phần df = f_x dx + f_y dy: mỗi biến nhích một chút, cộng phần đổi theo từng hướng.
:::

Hàm ẩn: dọc đường cong F(x, y) = 0, F không đổi nên F_x dx + F_y dy = 0, tức y' = -F_x/F_y. Mặt F(x, y, z) = 0: giữ y yên thì F_x dx + F_z dz = 0, nên z_x = -F_x/F_z; z_y tương tự.

Taylor bậc hai thêm phần cong (f_xx dx^2 + 2f_xy dx dy + f_yy dy^2)/2; số 2 vì f_xy và f_yx cùng góp. Tích hàm một biến: nhân khai triển, e^x sin y = (1 + x + ...)(y - ...), phần bậc hai là xy.

Ví dụ: tính gần đúng 2.01^2 . 0.98 bằng f = x^2 y tại (2, 1).

1. f = 4, f_x = 2xy = 4, f_y = x^2 = 4.
2. dx = 0.01, dy = -0.02.
3. f xấp xỉ 4 + 4(0.01) + 4(-0.02) = 3.96 (thật: 3.9593).

> Lỗi thường gặp: quên dấu trừ trong y' = -F_x/F_y. Thử với đường tròn: tại (3, 4) dốc phải âm.

:::check
Q: x^2 + y^2 = 25 xác định y = y(x) gần (3, 4). Tính y'(3).
A: F_x = 2x, F_y = 2y: y' = -x/y = -3/4.
:::

:::check
Q: Mặt cầu x^2 + y^2 + z^2 = 9 xác định z = z(x, y) gần (2, 1, 2). Tính z_x và z_y.
A: F_x = 2x, F_y = 2y, F_z = 2z: z_x = -x/z = -1, z_y = -y/z = -1/2.
:::

## Cực trị của hàm hai biến

:::hook
Mặt loss của mạng nơ-ron có đáy, có đỉnh, và rất nhiều yên ngựa: chỗ phẳng mà không phải đáy. Gradient bằng 0 ở cả ba, nên phải phân loại.
:::

:::figure plane
caption: Yên ngựa x^2 - y^2: dọc trục x đi lên, dọc trục y đi xuống.
size: 140 100
x: -2 2 1
y: -3 3 1
names: t z
curve "x^2" xanh "dọc x" pos=w
curve "-x^2" do "dọc y" pos=w
point 0 0 muc
:::

:::figure grid
caption: Tại điểm dừng, D = f_xx f_yy - f_xy^2.
table
head "D" "f_xx" "điểm dừng là"
row "> 0" "> 0" "cực tiểu"
row "> 0" "< 0" "cực đại"
row "< 0" "bất kỳ" "yên ngựa"
row "= 0" "bất kỳ" "chưa biết"
:::

:::core
Chỗ phẳng có thể là đáy, đỉnh hay yên ngựa; D của các đạo hàm cấp hai phân xử.
:::

Ví dụ: cực trị của f = x^2 + xy + y^2 - 3x.

1. f_x = 2x + y - 3 = 0, f_y = x + 2y = 0: điểm dừng (2, -1).
2. f_xx = 2, f_yy = 2, f_xy = 1: D = 4 - 1 = 3 > 0.
3. f_xx > 0: cực tiểu, f(2, -1) = -3.

> Lỗi thường gặp: thấy D = 0 là kết luận không có cực trị. x^4 + y^4 có D = 0 tại gốc mà vẫn có đáy ở đó.

:::check
Q: Điểm dừng (0, 0) của f = x^2 + 6xy + y^2 là gì?
A: f_xx = f_yy = 2, f_xy = 6: D = 4 - 36 < 0, yên ngựa.
:::

## Cực trị có điều kiện

:::hook
Huấn luyện mô hình mà trọng số bị giới hạn độ lớn, hay xây hộp với số linh thạch có hạn: tối ưu mà phải đứng trên một đường ràng buộc.
:::

:::figure plane
caption: x + y = c trượt tới khi vừa chạm đường tròn: GTLN, grad f vuông góc cả hai.
size: 150 105
aspect: equal
x: -2.2 2.6 1
y: -2.2 2.6 1
param "sqrt(2)*cos(t)" "sqrt(2)*sin(t)" 0 2*pi xanh
line 2 0 0 2 do dash
line 0 0 1 -1 xam dash
line -2 0 0 -2 xam dash
vector 1 1 1.6 1.6 do "grad f" pos=e
point 1 1 muc
:::

:::core
Trên đường ràng buộc g = 0, cực trị của f nằm nơi đường mức của f vừa tiếp xúc đường ràng buộc: tại đó grad f song song grad g.
:::

$$ \nabla f = \lambda\,\nabla g, \qquad g(x, y) = 0 $$

Ràng buộc là đường đóng (tròn, elip) thì so f tại các điểm tìm được: lớn nhất là GTLN, nhỏ nhất là GTNN.

Ví dụ: GTLN, GTNN của x + y trên x^2 + y^2 = 2.

1. (1, 1) = lambda (2x, 2y), nên x = y.
2. Thay vào: 2x^2 = 2, x = 1 hoặc x = -1.
3. f(1, 1) = 2 là GTLN, f(-1, -1) = -2 là GTNN.

> Lỗi thường gặp: bỏ sót nghiệm. Từ 4 lambda^2 = 1 phải lấy cả 1/2 lẫn -1/2; từ x = lambda x phải xét cả x = 0.

:::check
Q: GTLN của 3x - 4y trên đường tròn x^2 + y^2 = 4?
A: grad f = (3, -4) song song (x, y): điểm 2 . (3, -4)/5. GTLN = 2 . 5 = 10.
:::

## Gradient, Jacobian và lan truyền ngược

:::hook
Mỗi bước huấn luyện mạng nơ-ron: lan truyền ngược để có gradient của loss, rồi bước một chút ngược hướng gradient.
:::

:::figure graph
caption: a = xy, b = x^2, f = a + b tại x = 2, y = 3. Từ x tới f có hai đường (đỏ): qua a và qua b.
size: 170 80
layout: free
directed: yes
node x 0 0 "x = 2"
node y 0 2 "y = 3"
node a 2 1 "a = 6" xanh
node b 2 -1 "b = 4" xanh
node f 4 0 "f = 10" vang
edge x a "y = 3" do
edge y a "x = 2"
edge x b "2x = 4" do
edge a f "1" do
edge b f "1" do
:::

:::core
Gradient chỉ hướng lên dốc nhanh nhất; lan truyền ngược tính nó: nhân đạo hàm cục bộ dọc mỗi đường từ đầu ra về, rồi cộng các đường.
:::

Ví dụ: với hình trên, tính df/dx và df/dy.

1. Đường x -> a -> f: 3 . 1 = 3. Đường x -> b -> f: 4 . 1 = 4.
2. Cộng hai đường: df/dx = 3 + 4 = 7 (khớp y + 2x).
3. y chỉ có một đường: df/dy = 2 . 1 = 2.

grad f = (f_x, f_y). Đi theo hướng đơn vị u, f đổi với tốc độ grad f . u = |grad f| cos(góc): lớn nhất |grad f| khi đi đúng hướng grad f, bằng 0 khi đi dọc đường mức.

Jacobian của (u, v) = (u(x, y), v(x, y)) là bảng [u_x, u_y; v_x, v_y]. Dây chuyền nhiều biến là nhân các bảng ấy; một ô của tích, z_x = z_u u_x + z_v v_x, chính là cộng hai đường x -> u -> z và x -> v -> z.

> Lỗi thường gặp: chỉ đi một đường. Ở hình trên, quên nhánh qua b sẽ ra df/dx = 3 thay vì 7.

:::check
Q: f = x^2 + y^2. Đạo hàm theo hướng u = (3/5, 4/5) tại (1, 2) bằng bao nhiêu?
A: grad f = (2, 4). Tích vô hướng: 6/5 + 16/5 = 22/5.
:::

:::check
Q: Nơ-ron z = wx + b, L = (z - t)^2 với w = 2, x = 3, b = -1, t = 4. Tính L, dL/dw, dL/db.
A: z = 5, L = 1. dL/dz = 2(z - t) = 2, rồi dL/dw = 2 . x = 6, dL/db = 2 . 1 = 2.
:::

:::check
Q: (u, v) = (x + y, xy). Tính định thức Jacobian tại (1, 2).
A: Bảng [u_x, u_y; v_x, v_y] = [1, 1; y, x] = [1, 1; 2, 1]. Định thức 1 . 1 - 1 . 2 = -1.
:::
