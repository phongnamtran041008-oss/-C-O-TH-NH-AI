---
id: dstt_lib_t2
title_vi: Số phức
subject: dai_so_tuyen_tinh
floor: 2
format: 2
summary_vi: Số phức là một điểm trên mặt phẳng: cộng là tịnh tiến, nhân là quay và co giãn, chia là nhân với liên hợp, và căn bậc n xếp đều trên một đường tròn.
skills: [dstt_t2_dang_dai_so, dstt_t2_cong_nhan, dstt_t2_lien_hop_modun, dstt_t2_chia, dstt_t2_dang_luong_giac, dstt_t2_can_bac_n]
---
## Dạng đại số của số phức

:::hook
x^2 = -1 không có nghiệm thực. Thêm một số i với i^2 = -1 thì phương trình đa thức nào cũng có nghiệm; phép biến đổi Fourier trong nhận dạng giọng nói tính hoàn toàn bằng số ấy.
:::

:::figure plane
caption: Số phức a + bi là điểm (a, b). 4 nằm trên trục thực, -2i nằm trên trục ảo.
size: 190 115
names: Re Im
x: -1 5 1
y: -3 3 1
drop 3 2
point 3 2 do "3 + 2i" pos=ne
point 4 0 xanh "4" pos=s
point 0 -2 luc "-2i" pos=e
:::

:::core
Số phức a + bi là một điểm (a, b) trên mặt phẳng: a là phần thực, b là phần ảo, và b là một số thực, không kèm i.
:::

Số thực là số có b = 0, nằm trên trục thực. Số thuần ảo có a = 0 và b != 0, nằm trên trục ảo. Hai số phức bằng nhau khi là cùng một điểm: cùng phần thực và cùng phần ảo.

> Lỗi thường gặp: nói phần ảo của 2 - 5i là -5i. Phần ảo là -5, chỉ là tọa độ dọc của điểm.

:::check
Q: Số -7i có phần thực và phần ảo bằng bao nhiêu? Nó nằm trên trục nào?
A: Phần thực 0, phần ảo -7. Nó là số thuần ảo, nằm trên trục ảo, tại (0, -7).
:::

### Lũy thừa của i

:::figure plane
caption: Nhân với i là quay 90 độ. Quay 4 lần về chỗ cũ, nên i^n lặp lại sau mỗi 4 bước.
size: 150 115
aspect: equal
names: Re Im
x: -1.6 1.6 5
y: -1.4 1.4 5
param "cos(t)" "sin(t)" 0 2*pi xam dash
point 1 0 do "1" pos=ne
point 0 1 do "i" pos=ne
point -1 0 do "-1" pos=nw
point 0 -1 do "-i" pos=se
:::

Từ i^2 = -1 suy ra i^3 = -i và i^4 = 1: bốn lũy thừa đầu đi trọn một vòng quanh đường tròn, rồi bắt đầu lại.

$$ i^{2} = -1 $$

Ví dụ: tính i^27.

1. Chu kỳ là 4: i, -1, -i, 1, rồi lặp lại.
2. 27 = 4 . 6 + 3, dư 3.
3. Vậy i^27 = i^3 = -i.

:::check
Q: Tính i^10.
A: 10 = 4 . 2 + 2, dư 2, nên i^10 = i^2 = -1.
:::

## Cộng, trừ và nhân số phức

:::hook
Trong đồ họa, cộng một số phức là dời một điểm, nhân là quay và phóng nó: hai phép biến hình gói gọn trong hai phép tính.
:::

:::figure plane
caption: Cộng số phức là nối đuôi mũi tên: (2 + i) + (1 + 2i) = 3 + 3i.
size: 150 115
names: Re Im
x: -0.5 3.5 1
y: -0.5 3.5 1
vector 0 0 2 1 do "2 + i" pos=se
vector 2 1 3 3 xanh "1 + 2i" pos=e
vector 0 0 3 3 luc "3 + 3i" pos=nw
:::

:::core
Cộng thì cộng riêng phần thực, riêng phần ảo; nhân thì nhân bung từng cặp như đa thức, rồi đổi i^2 thành -1.
:::

:::check
Q: Tính (2 - 3i) + (-5 + i).
A: Phần thực 2 - 5 = -3, phần ảo -3 + 1 = -2: kết quả -3 - 2i.
:::

### Nhân số phức

:::figure grid
caption: (3 + 2i)(1 + 4i): nhân từng cặp. Ô đỏ 8i^2 thành -8, nên tích là -5 + 14i.
table
head "1" "4i"
side "3" "2i"
row "3" "12i"
row "2i" "8i^2"
mark cell 2 2 do
:::

Ví dụ: tính (3 + 2i)(1 + 4i), như bảng trên.

1. Bốn tích: 3, 12i, 2i, 8i^2.
2. 8i^2 = -8 nhập vào phần thực: 3 - 8 = -5.
3. Phần ảo: 12 + 2 = 14. Tích là -5 + 14i.

Phép nhân số phức vẫn giao hoán: zw = wz.

$$ (a + bi)(c + di) = (ac - bd) + (ad + bc)i $$

> Lỗi thường gặp: để nguyên 8i^2 trong phần ảo, hoặc quên đổi dấu. Số hạng có i^2 là số thực, mang dấu ngược lại.

:::check
Q: Tính (1 - 2i)^2.
A: 1 - 4i + 4i^2 = 1 - 4i - 4 = -3 - 4i.
:::

## Số phức liên hợp và môđun

:::hook
Một tín hiệu số phức có "độ lớn" là thứ loa phát ra to hay nhỏ. Độ lớn ấy là môđun: khoảng cách từ điểm tới gốc tọa độ.
:::

:::figure plane
caption: |z| = 5: khoảng cách từ gốc tới z. Liên hợp: ảnh của z qua gương trục thực.
size: 200 105
names: Re Im
x: -1 6 1
y: -5 5 2
segment 0 0 3 4 luc "|z| = 5" pos=nw
segment 3 4 3 -4 xam dash
point 3 4 do "z = 3 + 4i" pos=e
point 3 -4 xanh "3 - 4i" pos=e
:::

:::core
Liên hợp là soi z qua gương trục thực (đổi dấu phần ảo); môđun là khoảng cách từ z tới gốc, và z nhân liên hợp của nó luôn ra |z|^2.
:::

Môđun là một khoảng cách nên luôn >= 0. Cộng z với liên hợp thì phần ảo triệt tiêu, còn 2a.

Ví dụ: z = -6 + 8i.

1. Liên hợp: -6 - 8i. Môđun: |z| = sqrt(36 + 64) = 10.
2. z nhân liên hợp: 36 + 64 = 100 = |z|^2. Tổng của chúng: -12.

$$ z \cdot \overline{z} = a^{2} + b^{2} = |z|^{2} $$

> Lỗi thường gặp: viết |z + w| = |z| + |w|. Thử z = 1, w = -1: vế trái 0, vế phải 2.

:::check
Q: Không tính toán: |2 - 7i| và |2 + 7i| có bằng nhau không? Vì sao?
A: Bằng nhau: hai điểm đối xứng qua trục thực nên cách gốc như nhau (đều là sqrt(53)).
:::

## Chia số phức

:::hook
"Một phần (1 + i)" là bao nhiêu? Mẹo là đổi mẫu thành số thực trước, rồi chia như chia thường.
:::

:::figure flow
caption: Nhân tử và mẫu với 1 - i: mẫu thành (1 + i)(1 - i) = 2.
box "(2 + 4i) / (1 + i)"
link "x (1 - i)"
box "(6 + 2i) / 2" xanh
link "chia 2"
box "3 + i" luc
:::

:::core
Chia số phức là làm mẫu thành số thực: nhân cả tử và mẫu với liên hợp của mẫu, vì (c + di)(c - di) = c^2 + d^2.
:::

Ví dụ: tính (4 - 3i) / i.

1. Liên hợp của i là -i; mẫu thành i . (-i) = 1.
2. Tử: (4 - 3i)(-i) = -4i + 3i^2 = -3 - 4i.
3. Thử lại: (-3 - 4i) . i = -3i + 4 = 4 - 3i. Đúng.

$$ \frac{a + bi}{c + di} = \frac{(a + bi)(c - di)}{c^{2} + d^{2}} $$

> Lỗi thường gặp: nhân với liên hợp của tử. Mục đích là làm mẫu hết phần ảo, nên phải dùng liên hợp của mẫu.

:::check
Q: Tính 10 / (3 + i).
A: Nhân tử và mẫu với 3 - i: 10(3 - i) / 10 = 3 - i.
:::

## Dạng lượng giác và công thức Moivre

:::hook
Quay 30 độ ba lần là quay 90 độ. Viết số phức theo độ dài và góc, lũy thừa chỉ còn là nâng độ dài và nhân góc.
:::

:::figure plane
caption: Mỗi lần nhân với z = 1 + i: quay thêm 45 độ, dài gấp sqrt(2).
size: 190 110
names: Re Im
x: -2.5 1.5 1
y: -0.5 2.5 2
vector 0 0 1 1 do "z" pos=e
vector 0 0 0 2 xanh "z^2" pos=e
vector 0 0 -2 2 luc "z^3" pos=w
:::

:::core
Ghi z bằng độ dài r và góc phi thì nhân là nhân độ dài, cộng góc; z^n có độ dài r^n và góc gấp n lần.
:::

Acgumen là góc đo từ trục thực dương: trục ảo dương 90 độ, trục thực âm 180, trục ảo âm 270; 3 + 3i nằm trên phân giác nên 45 độ.

Ví dụ: tính (-1 + i)^4.

1. Độ dài r = sqrt(2), góc 135 độ.
2. Lũy thừa 4: r^4 = 4, góc 4 . 135 = 540, tức 180 độ.
3. Kết quả: 4(cos 180 + i sin 180) = -4. Thử: (-1 + i)^2 = -2i, (-2i)^2 = -4.

$$ z^{n} = r^{n}(\cos n\varphi + i \sin n\varphi) $$

> Lỗi thường gặp: nâng r lên r^n mà quên nhân góc với n.

:::check
Q: z có môđun 3, acgumen 20 độ; w có môđun 2, acgumen 70 độ. zw là số nào?
A: Môđun 3 . 2 = 6, acgumen 20 + 70 = 90 độ: zw = 6i.
:::

## Căn bậc n của số phức

:::hook
Trong số thực, x^2 = -4 vô nghiệm và x^3 = 8 chỉ có nghiệm 2. Trong số phức, z^n = w luôn có đủ n nghiệm, xếp đều trên một đường tròn.
:::

:::figure plane
caption: Ba căn bậc ba của 8: cùng môđun 2, cách nhau 120 độ, là ba đỉnh tam giác đều. Chỉ một căn là số thực.
size: 230 120
aspect: equal
names: Re Im
x: -5.2 2.8 10
y: -2.4 2.4 10
param "2*cos(t)" "2*sin(t)" 0 2*pi xam dash
poly 2 0 -1 sqrt(3) -1 -sqrt(3) vang
point 2 0 do "2" pos=e
point -1 sqrt(3) do "-1 + sqrt(3)i" pos=w
point -1 -sqrt(3) do "-1 - sqrt(3)i" pos=w
:::

:::core
Mọi số phức w khác 0 có đúng n căn bậc n: cùng môđun bằng căn bậc n của |w|, góc cách đều nhau 360/n độ.
:::

> Lỗi thường gặp: nói z^5 = 1 chỉ có nghiệm z = 1. Trong số phức nó có đúng 5 nghiệm.

:::check
Q: z^6 = -1 có bao nhiêu nghiệm phức? Có nghiệm nào là số thực không?
A: 6 nghiệm, môđun 1, góc 30 + 60k độ. Không góc nào là 0 hay 180 nên không có nghiệm thực.
:::

### Căn bậc hai không cần lượng giác

Đặt căn là x + yi, bình phương lên rồi so từng phần với w = a + bi, thêm điều kiện x^2 + y^2 = |w|.

$$ x^{2} - y^{2} = a, \quad 2xy = b, \quad x^{2} + y^{2} = |w| $$

Ví dụ: tìm hai căn bậc hai của w = 3 + 4i.

1. x^2 - y^2 = 3 và x^2 + y^2 = |w| = 5.
2. Cộng, trừ: x^2 = 4, y^2 = 1.
3. 2xy = 4 dương nên x, y cùng dấu: 2 + i và -2 - i.
4. Thử: (2 + i)^2 = 4 + 4i - 1 = 3 + 4i.

:::check
Q: Tìm hai căn bậc hai của -3 + 4i.
A: x^2 - y^2 = -3, x^2 + y^2 = 5 nên x^2 = 1, y^2 = 4; 2xy = 4 > 0: 1 + 2i và -1 - 2i.
:::
