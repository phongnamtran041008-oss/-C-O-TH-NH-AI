---
id: gt_lib_t9
title_vi: Hàm nhiều biến
subject: giai_tich
floor: 9
summary_vi: Hàm của hai biến có giới hạn, đạo hàm riêng, vi phân và cực trị như hàm một biến, nhưng mọi thứ phải xét theo mọi hướng cùng lúc; gradient gom các đạo hàm riêng thành một vector, và lan truyền ngược trong mạng nơ-ron chỉ là quy tắc dây chuyền chạy ngược trên một đồ thị tính toán.
skills: [gt_t9_gioi_han_lien_tuc, gt_t9_dao_ham_rieng, gt_t9_vi_phan_ham_an, gt_t9_cuc_tri, gt_t9_cuc_tri_dieu_kien, gt_t9_gradient_lan_truyen]
---
## Miền xác định, giới hạn và liên tục

Miền xác định của f(x, y) là tập các điểm (x, y) của mặt phẳng làm công thức có nghĩa: căn bậc hai cần biểu thức không âm, ln cần biểu thức dương, mẫu cần khác 0. Kết quả thường là một miền vẽ được: nửa mặt phẳng, hình tròn, vành khăn, phần trên một parabol.

Ví dụ sqrt(9 - x^2 - y^2)/sqrt(x^2 + y^2 - 1) xác định trên vành khăn 1 < x^2 + y^2 <= 9.

Giới hạn khi (x, y) -> (a, b) bằng L nghĩa là f(x, y) gần L khi (x, y) gần (a, b) theo bất kỳ cách nào:

$$ \lim_{(x, y) \to (a, b)} f(x, y) = L $$

Hai công cụ:

- Chứng minh không tồn tại: tìm hai đường đi tới (a, b) cho hai giới hạn khác nhau. xy/(x^2 + y^2) dọc y = kx cho k/(1 + k^2), phụ thuộc k.
- Chứng minh tồn tại: kẹp |f(x, y) - L| bởi một biểu thức dần tới 0, chẳng hạn |x^2 y^2/(x^2 + y^2)| <= y^2; hoặc chuyển sang tọa độ cực x = r cos t, y = r sin t và chặn theo r.

f liên tục tại (a, b) khi giới hạn tồn tại và bằng f(a, b). Tổng, tích, hợp của các hàm liên tục là liên tục (ở nơi xác định).

> Lỗi thường gặp: thử mọi đường thẳng qua gốc rồi kết luận giới hạn tồn tại. x^2 y/(x^4 + y^2) cho 0 dọc mọi đường thẳng nhưng cho 1/2 dọc parabol y = x^2.

## Đạo hàm riêng

Đạo hàm riêng theo x là đạo hàm khi giữ y cố định, và ngược lại:

$$ f_x(a, b) = \lim_{h \to 0} \frac{f(a + h, b) - f(a, b)}{h} = \frac{\partial f}{\partial x}(a, b) $$

Thực hành: coi biến kia là hằng số rồi dùng mọi quy tắc của hàm một biến. Với f = x^y (x > 0): f_x = y x^(y - 1) (lũy thừa của x) nhưng f_y = x^y ln x (hàm mũ của y).

Đạo hàm riêng cấp hai: f_xx, f_yy và hai đạo hàm hỗn hợp; trong bí cảnh này f_xy nghĩa là (f_x)_y.

$$ f_{xy} = \frac{\partial}{\partial y}\Big(\frac{\partial f}{\partial x}\Big), \qquad f_{xy} = f_{yx} $$

Định lý Schwarz (vế phải của dòng trên, đúng khi các đạo hàm hỗn hợp liên tục) cho phép đổi thứ tự lấy đạo hàm với mọi hàm sơ cấp quen thuộc ở những điểm chúng khả vi liên tục. Nó có thể sai khi điều kiện liên tục hỏng: xy(x^2 - y^2)/(x^2 + y^2) có f_xy(0, 0) = -1 và f_yx(0, 0) = 1.

Phương trình Laplace u_xx + u_yy = 0 là một ví dụ phương trình đạo hàm riêng; x^3 - 3xy^2 là một nghiệm.

> Lỗi thường gặp: quên rằng biến kia là hằng số chứ không phải 0, hoặc lấy đạo hàm hai lần theo cùng một biến khi đề hỏi đạo hàm hỗn hợp.

## Vi phân toàn phần, hàm ẩn và công thức Taylor

f khả vi tại (x, y) khi số gia của f xấp xỉ được bằng một biểu thức tuyến tính theo dx, dy; biểu thức đó là vi phân toàn phần:

$$ df = f_x\,dx + f_y\,dy, \qquad f(x + dx, y + dy) \approx f(x, y) + f_x\,dx + f_y\,dy $$

Ví dụ sqrt(3.02^2 + 3.97^2): tại (3, 4), f = 5, f_x = 3/5, f_y = 4/5, nên giá trị gần đúng là 5 + (3/5)(0.02) + (4/5)(-0.03) = 4.988.

Hàm ẩn: nếu F(x, y) = 0 và F_y khác 0 tại một điểm thì gần đó y là hàm khả vi của x. Lấy đạo hàm F(x, y(x)) = 0 theo x:

$$ y'(x) = -\frac{F_x}{F_y}, \qquad z_x = -\frac{F_x}{F_z},\; z_y = -\frac{F_y}{F_z} $$

Muốn y'' thì lấy đạo hàm thêm lần nữa đẳng thức đã có (nhớ y' cũng là hàm của x), rồi thay số.

Công thức Taylor bậc hai tại (a, b), với dx = x - a, dy = y - b:

$$ f(a + dx, b + dy) \approx f + f_x\,dx + f_y\,dy + \frac{1}{2}\big(f_{xx}\,dx^2 + 2f_{xy}\,dx\,dy + f_{yy}\,dy^2\big) $$

Với tích của các hàm một biến, nhân các khai triển Maclaurin đã biết là nhanh nhất: e^x ln(1 + y) = y + xy - y^2/2 + (bậc ba).

> Lỗi thường gặp: quên dấu trừ trong y' = -F_x/F_y, hoặc quên hệ số 2 của số hạng hỗn hợp trong Taylor (hệ số của dx dy là f_xy, không phải f_xy/2).

## Cực trị của hàm hai biến

Tại điểm cực trị bên trong miền, cả hai đạo hàm riêng bằng 0 (điểm dừng). Để phân loại điểm dừng (a, b), dùng ma trận đạo hàm cấp hai (ma trận Hesse) và định thức của nó:

$$ H = \begin{pmatrix} f_{xx} & f_{xy} \\ f_{xy} & f_{yy} \end{pmatrix}, \qquad D = f_{xx} f_{yy} - f_{xy}^2 $$

- D > 0 và f_xx > 0: cực tiểu địa phương.
- D > 0 và f_xx < 0: cực đại địa phương.
- D < 0: điểm yên ngựa (không phải cực trị).
- D = 0: dấu hiệu không kết luận được; xét trực tiếp.

Lý do nằm ở công thức Taylor: tại điểm dừng phần bậc nhất biến mất, dấu của phần bậc hai quyết định.

Ví dụ x^3 + y^3 - 3xy: điểm dừng (0, 0) và (1, 1). Tại (0, 0) D = -9, yên ngựa; tại (1, 1) D = 27, f_xx = 6, cực tiểu với giá trị -1.

Hàm bậc hai Ax^2 + Bxy + Cy^2 + Dx + Ey có H không đổi: nếu 4AC - B^2 > 0 và A > 0 thì điểm dừng là cực tiểu toàn cục.

> Lỗi thường gặp: kết luận "D = 0 nên không có cực trị". x^4 + y^4 có D = 0 tại gốc mà vẫn đạt cực tiểu ở đó.

## Cực trị có điều kiện

Tìm cực trị của f(x, y) khi (x, y) phải nằm trên đường g(x, y) = 0. Tại điểm cực trị (nơi grad g khác 0), gradient của f song song với gradient của g:

$$ \nabla f = \lambda\,\nabla g, \qquad g(x, y) = 0 $$

Tương đương: lập hàm Lagrange L = f - lambda g và giải L_x = L_y = 0, g = 0. Số lambda là nhân tử Lagrange.

Cách làm:

1. Viết hệ ba phương trình (bốn với ba biến), ẩn x, y, lambda.
2. Khử lambda (chia hai phương trình cho nhau, nhưng nhớ xét riêng trường hợp mẫu bằng 0).
3. Thay vào ràng buộc để tìm các điểm nghi ngờ, tính f tại mỗi điểm.
4. Nếu đường ràng buộc đóng và bị chặn (đường tròn, elip), số lớn nhất là GTLN, nhỏ nhất là GTNN.

Ví dụ x + 2y trên x^2 + y^2 = 5: (1, 2) = 2lambda(x, y) cho y = 2x, hai điểm (1, 2), (-1, -2), GTLN 5, GTNN -5. Bài toán thực tế (hộp thể tích cho trước, ít vật liệu nhất) giải cùng cách.

> Lỗi thường gặp: bỏ sót nghiệm khi giải. Từ 4lambda^2 = 1 phải lấy cả lambda = 1/2 lẫn lambda = -1/2; từ 2x = 2lambda x phải xét cả x = 0.

## Gradient, Jacobian và lan truyền ngược

Gradient gom các đạo hàm riêng thành một vector. Đạo hàm theo hướng vector đơn vị u là tích vô hướng:

$$ \nabla f = (f_x, f_y), \qquad D_u f = \nabla f \cdot u = |\nabla f|\cos\theta $$

Hệ quả: f tăng nhanh nhất theo hướng grad f với tốc độ |grad f|, giảm nhanh nhất theo hướng ngược lại, và không đổi theo hướng vuông góc với grad f (tiếp xúc với đường mức). Thuật toán hạ gradient trong học máy đi một bước nhỏ theo -grad f.

Với ánh xạ (u, v) = (u(x, y), v(x, y)), ma trận Jacobian là ma trận các đạo hàm riêng; quy tắc dây chuyền nhiều biến là nhân các ma trận này:

$$ J = \begin{pmatrix} u_x & u_y \\ v_x & v_y \end{pmatrix}, \qquad z_x = z_u\,u_x + z_v\,v_x $$

Lan truyền ngược trên một đồ thị tính toán nhỏ:

1. Lan truyền xuôi: tính giá trị mọi nút từ đầu vào tới đầu ra.
2. Bắt đầu từ đầu ra với đạo hàm 1, đi ngược từng cạnh: đạo hàm theo một nút = đạo hàm theo nút sau nó nhân đạo hàm cục bộ của cạnh.
3. Một nút đi vào nhiều nút sau thì cộng đóng góp của mọi đường.

Ví dụ u = xy, v = u + z, f = v^2 tại x = 1, y = 2, z = -4: xuôi u = 2, v = -2, f = 4; ngược df/dv = 2v = -4, df/dx = -4 . 1 . y = -8, df/dy = -4, df/dz = -4. Một nơ-ron z = wx + b với L = (z - t)^2 có dL/dw = 2(z - t)x và dL/db = 2(z - t).

> Lỗi thường gặp: bỏ sót một đường. Với a = xy, f = a + x^2, x đi vào f cả qua a lẫn trực tiếp, nên df/dx = y + 2x chứ không chỉ y.
