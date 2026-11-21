---
id: gt_lib_t8
title_vi: Ứng dụng của tích phân và tích phân suy rộng
subject: giai_tich
floor: 8
format: 2
summary_vi: Diện tích, thể tích, độ dài đều là tổng của vô số mảnh mỏng, nên đều là tích phân; khi cận ra vô cùng hay hàm vọt lên vô cùng, tích phân là một giới hạn, và so với 1/x^p là biết nó hữu hạn hay không.
skills: [gt_t8_dien_tich, gt_t8_the_tich, gt_t8_do_dai_cung, gt_t8_suy_rong_loai_1, gt_t8_suy_rong_loai_2, gt_t8_tieu_chuan_hoi_tu]
---
## Diện tích hình phẳng

:::hook
Đo một hồ nước có bờ cong: cắt hồ thành vô số dải đứng thật mỏng, mỗi dải cao bằng bờ trên trừ bờ dưới, rồi cộng lại.
:::

:::figure plane
caption: Miền giữa y = x + 2 và y = x^2, từ giao điểm -1 tới 2.
size: 160 105
x: -1.6 2.6 1
y: -0.5 4.5 1
poly -1 1 2 4 1.7 2.89 1.4 1.96 1 1 0.6 0.36 0.3 0.09 0 0 -0.3 0.09 -0.6 0.36 -0.8 0.64 vang
curve "x + 2" do -1.5 2.4
text 0.5 3.5 "y = x + 2" do
curve "x^2" xanh -1.5 2.1
segment 0.5 0.25 0.5 2.5 muc
:::

:::core
Diện tích giữa hai đường là tổng các dải mỏng cao (trên - dưới): tìm giao điểm, rồi tích phân hiệu.
:::

$$ S = \int_a^b \big|f(x) - g(x)\big|\,dx $$

Khi biên cho dạng x theo y (như y^2 = 2x), cắt dải nằm ngang dài (phải - trái) rồi lấy tích phân theo dy. Parabol a(x - r)(x - s) bao với Ox diện tích |a|(s - r)^3/6; như x^2 - 1 cho 8/6 = 4/3.

Ví dụ: diện tích giữa y = x^2 và y = x + 2.

1. x^2 = x + 2 khi x = -1 hoặc x = 2.
2. Thử x = 0: đường thẳng cho 2 > 0, nằm trên.
3. S = tích phân từ -1 đến 2 của (x + 2 - x^2) dx = 9/2.

> Lỗi thường gặp: bỏ trị tuyệt đối khi hiệu đổi dấu. Giữa y = x^3 và y = x trên [-1, 1], tích phân có dấu bằng 0, diện tích thật là 1/2.

:::check
Q: Diện tích miền giữa parabol y = 4 - x^2 và trục Ox?
A: Cắt Ox tại -2 và 2, a = -1: |a|(s - r)^3/6 = 64/6 = 32/3. Tính thẳng tích phân cũng ra 32/3.
:::

## Thể tích vật thể tròn xoay

:::hook
Thợ tiện quay một miếng gỗ phẳng thành chân bàn tròn. Thể tích chân bàn là tổng của vô số đồng xu mỏng xếp dọc trục quay.
:::

:::figure plane
caption: Quay y = sqrt(x) quanh Ox: lát tại x là đồng xu bán kính sqrt(x).
size: 160 100
aspect: equal
x: -0.4 4.6 1
y: -2.3 2.3 1
curve "sqrt(x)" xanh 0 4
curve "-sqrt(x)" xanh 0 4
param "1 + 0.18*sin(t)" "cos(t)" 0 2*pi do
param "2.5 + 0.25*sin(t)" "sqrt(2.5)*cos(t)" 0 2*pi do
param "4 + 0.3*sin(t)" "2*cos(t)" 0 2*pi do
:::

:::core
Thể tích là tổng các lát mỏng: quay quanh Ox, lát tại x là hình tròn diện tích pi f(x)^2.
:::

$$ V_{Ox} = \pi\int_a^b f(x)^2\,dx $$

Miền nằm giữa hai đường f >= g >= 0 thì lát có lỗ ở giữa, là vành khăn: hình tròn lớn trừ hình tròn nhỏ, pi(f^2 - g^2).

Ví dụ: quay đoạn y = x, 0 <= x <= 3 quanh Ox (được một hình nón).

1. Lát tại x là hình tròn bán kính x, diện tích pi x^2.
2. V = pi . tích phân từ 0 đến 3 của x^2 dx = 9pi.
3. Khớp với pi r^2 h/3 khi r = h = 3.

> Lỗi thường gặp: viết vành khăn là pi(f - g)^2. Đúng là hình tròn lớn trừ hình tròn nhỏ: pi(f^2 - g^2).

:::figure plane
caption: Quay quanh Oy: dải đứng tại x quay thành một vỏ ống bán kính x. Trải vỏ ra được tấm mỏng dài 2pi x, cao f(x).
size: 160 95
x: -1.3 1.3 0.5
y: -0.3 1.3 0.5
curve "1 - x^2" xanh -1 1
poly 0.6 0 0.7 0 0.7 0.51 0.6 0.64 do
poly -0.7 0 -0.6 0 -0.6 0.64 -0.7 0.51 xam
param "0.65*cos(t)" "0.12*sin(t)" 0 2*pi do
:::

Quay quanh trục Oy thì cắt dải đứng thay vì lát. Dải tại x, cao f(x), dày dx, quay thành vỏ ống có thể tích 2pi x . f(x) dx; cộng lại: V = 2pi . tích phân của x f(x) dx.

:::check
Q: Quay miền giữa y = 1 và y = x^2 (0 <= x <= 1) quanh Ox. Thể tích bằng bao nhiêu?
A: Vành khăn bán kính ngoài 1, trong x^2: V = pi . tích phân từ 0 đến 1 của (1 - x^4) dx = 4pi/5.
:::

:::check
Q: Quay miền dưới y = 1 - x^2 (0 <= x <= 1) quanh trục Oy. Thể tích bằng bao nhiêu?
A: Vỏ trụ: V = 2pi . tích phân từ 0 đến 1 của x(1 - x^2) dx = 2pi(1/2 - 1/4) = pi/2.
:::

## Độ dài đường cong

:::hook
Đo con đường núi quanh co bằng một cây thước thẳng: đi từng bước thật ngắn, mỗi bước gần như một đoạn thẳng, rồi cộng các bước.
:::

:::figure plane
caption: Mỗi bước nhỏ là cạnh huyền sqrt(dx^2 + dy^2), mà dy = y' dx.
size: 160 100
x: -0.2 2.6 1
y: -0.2 3 1
curve "x^2/2" xanh 0 2.4
segment 1 0.5 1.8 0.5 xam dash "dx" pos=s
segment 1.8 0.5 1.8 1.62 xam dash "dy" pos=e
segment 1 0.5 1.8 1.62 do "ds" pos=nw
:::

:::core
Độ dài cung là tổng các cạnh huyền nhỏ sqrt(dx^2 + dy^2) = sqrt(1 + (y')^2) dx.
:::

Đề thường chọn đường cong để 1 + (y')^2 là một bình phương, khai căn ra gọn. Nhớ sqrt(t^2) = |t|: biểu thức đổi dấu thì phải tách đoạn.

$$ L = \int_a^b \sqrt{1 + f'(x)^2}\,dx, \qquad L = \int_{\alpha}^{\beta} \sqrt{x'(t)^2 + y'(t)^2}\,dt $$

Ví dụ: độ dài cung y = (2/3)x^(3/2), 0 <= x <= 8.

1. y' = sqrt(x), nên 1 + (y')^2 = 1 + x.
2. L = tích phân từ 0 đến 8 của sqrt(1 + x) dx.
3. = (2/3)(9^(3/2) - 1) = (2/3) . 26 = 52/3.

> Lỗi thường gặp: dùng y thay cho y' dưới căn, hoặc quên số 1. Công thức là sqrt(1 + (y')^2).

:::check
Q: Độ dài cung của đường nào trên [0, 1] bằng tích phân từ 0 đến 1 của sqrt(1 + 9x^4) dx?
A: Cần (y')^2 = 9x^4, tức y' = 3x^2: y = x^3 (cộng hằng số tùy ý).
:::

## Tích phân suy rộng cận vô hạn

:::hook
Phân phối xác suất trải tới vô cùng, như thời gian chờ một sự kiện, vẫn phải có tổng xác suất bằng 1: diện tích dưới một cái đuôi dài vô hạn phải hữu hạn.
:::

:::figure plane
caption: Đuôi 1/x^2 teo nhanh: diện tích từ 1 tới vô cùng là 1. Đuôi 1/x: vô hạn.
size: 150 95
x: -0.2 6.2 1
y: -0.2 1.6 1
area "1/x^2" 1 6 xanh
curve "1/x^2" xanh 0.8 6 "1/x^2" pos=sw
curve "1/x" do 0.65 6 "1/x" pos=nw
:::

:::core
Tích phân tới vô cùng là giới hạn của tích phân tới R: đuôi teo đủ nhanh thì hữu hạn, gọi là hội tụ.
:::

$$ \int_a^{+\infty} \frac{dx}{x^p} < +\infty \iff p > 1 $$

Tích phân trên cả trục thì tách tại một điểm (thường là 0) thành hai nửa, mỗi nửa một cận vô hạn chạy riêng; hội tụ khi cả hai nửa hội tụ. Ví dụ 1/(1 + x^2): mỗi nửa ra pi/2, tổng pi.

Phân kỳ không nhất thiết là ra vô cùng: tích phân của sin x tới R là 1 - cos R, dao động mãi không có giới hạn.

Ví dụ: tính tích phân từ 1 đến +vô cùng của 3/x^4 dx.

1. Tới R: [-1/x^3] từ 1 đến R = 1 - 1/R^3.
2. R -> +vô cùng: 1/R^3 -> 0.
3. Hội tụ, bằng 1.

> Lỗi thường gặp: cắt đối xứng [-R, R] rồi cho R -> vô cùng. Với f = x, tích phân từ -R đến R luôn bằng 0 vì hai nửa triệt tiêu nhau, nhưng riêng nửa từ 0 đến R là R^2/2 -> vô cùng. Mỗi nửa phải tự hội tụ, nên tích phân này phân kỳ.

:::check
Q: Tính tích phân từ 0 đến +vô cùng của e^(-2x) dx.
A: Tới R: (1 - e^(-2R))/2, mà e^(-2R) -> 0: bằng 1/2.
:::

## Tích phân suy rộng của hàm không bị chặn

:::hook
Một cây cột cao vô hạn vẫn có thể có diện tích hữu hạn, nếu nó đủ mảnh. 1/sqrt(x) vọt lên vô cùng tại 0 mà vẫn bao một diện tích bằng 2 trên [0, 1].
:::

:::figure plane
caption: 1/sqrt(x) vọt lên mà đủ mảnh: diện tích 2. 1/x béo hơn: vô hạn.
size: 150 95
x: -0.1 1.6 0.5
y: -0.3 6 1
area "1/sqrt(x)" 0.03 1 xanh
curve "1/sqrt(x)" xanh 0.03 1.5 "1/sqrt(x)" pos=ne
curve "1/x" do 0.17 1.5
text 0.5 4.3 "1/x" do
:::

:::core
Hàm vọt lên vô cùng ở đầu mút thì cắt bỏ khúc nhỏ tới c, tính, rồi cho c dần tới đầu mút.
:::

$$ \int_0^1 \frac{dx}{x^p} < +\infty \iff p < 1 $$

Điểm bất thường nằm giữa đoạn thì tách đoạn tại đó; tích phân hội tụ khi mọi phần đều hội tụ. Ở đầu mút hay gặp c ln c, dạng 0 . vô cùng: viết thành ln c/(1/c) rồi L'Hospital, ra 0.

Ví dụ: tính tích phân từ 0 đến 1 của 1/x^(2/3) dx.

1. Từ c đến 1: [3x^(1/3)] = 3 - 3c^(1/3).
2. c -> 0+: c^(1/3) -> 0.
3. Hội tụ, bằng 3 (p = 2/3 < 1, khớp).

> Lỗi thường gặp: không thấy điểm bất thường ở giữa. Tích phân từ 0 đến 2 của 1/(x - 1)^2 dx không phải -2: quanh x = 1 nó phân kỳ.

:::check
Q: Tích phân từ 0 đến 1 của 1/x^(1/4) dx hội tụ không? Nếu có, bằng bao nhiêu?
A: p = 1/4 < 1 nên hội tụ. Nguyên hàm (4/3)x^(3/4): bằng 4/3.
:::

## Tiêu chuẩn hội tụ

:::hook
Nhiều tích phân không có nguyên hàm đẹp, nhưng ta chỉ cần biết nó hữu hạn hay không. Đặt nó cạnh một hàm mẫu 1/x^p là đủ trả lời.
:::

:::figure numberline
caption: Các giá trị p cho 1/x^p hội tụ: ở vô cùng cần p > 1, gần 0 cần p < 1. p = 1 hỏng cả hai.
size: 200 60
range: 0 3 1
interval 1 inf ( luc "ở vô cùng"
interval 0 1 [ ) xanh "gần 0"
point 1 do open
:::

:::core
Ở vô cùng chỉ lũy thừa cao nhất lên tiếng: f giống C/x^p thì tích phân của f hội tụ khi và chỉ khi p > 1.
:::

Ví dụ: tích phân từ 1 đến +vô cùng của (x + 1)/(x^3 + 2) dx hội tụ không?

1. Giữ lũy thừa cao nhất: (x + 1)/(x^3 + 2) giống x/x^3 = 1/x^2.
2. Tỉ số với 1/x^2 dần tới 1, nên hai tích phân cùng số phận.
3. p = 2 > 1: hội tụ.

So sánh thẳng, với 0 <= f <= g: nằm dưới một hàm có diện tích hữu hạn thì f cũng hữu hạn; nằm trên một hàm có diện tích vô hạn thì g cũng vô hạn. Tích phân từ 0 tới vô cùng có hai chỗ nguy hiểm: xét riêng gần 0 và gần vô cùng.

> Lỗi thường gặp: so sánh sai chiều. 1/(x + sqrt(x)) <= 1/x mà 1/x phân kỳ thì chưa nói được gì; phải chặn dưới: 1/(x + sqrt(x)) >= 1/(2x).

:::check
Q: Với p > 0, tích phân từ 1 đến +vô cùng của x/(x^p + 1) dx hội tụ khi nào?
A: Hàm giống x/x^p = 1/x^(p - 1). Hội tụ khi p - 1 > 1, tức p > 2.
:::
