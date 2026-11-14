---
id: dstt_lib_t2
title_vi: Số phức
subject: dai_so_tuyen_tinh
floor: 2
summary_vi: Thêm một số mới để phương trình nào cũng có nghiệm, rồi học cách cộng, nhân, chia và quay nó trên mặt phẳng.
skills: [dstt_t2_dang_dai_so, dstt_t2_cong_nhan, dstt_t2_lien_hop_modun, dstt_t2_chia, dstt_t2_dang_luong_giac, dstt_t2_can_bac_n]
---
## Dạng đại số của số phức

Không có số thực nào bình phương lên ra số âm. Vậy thì đặt thêm một số mới, gọi là đơn vị ảo i, với đúng một tính chất:

$$ i^{2} = -1 $$

Số phức là số viết được dưới dạng a + bi với a và b là số thực. Số a là phần thực, số b là phần ảo. Chú ý phần ảo là số b, không kèm chữ i.

$$ z = a + bi, \quad a \in \mathbb{R}, \quad b \in \mathbb{R} $$

Vì mỗi số phức viết được theo đúng một cách như vậy, hai số phức bằng nhau khi và chỉ khi phần thực bằng nhau và phần ảo bằng nhau. Một phương trình giữa hai số phức luôn tách được thành hai phương trình thực.

- Số thực là số phức có phần ảo bằng 0.
- Số thuần ảo là số phức có phần thực bằng 0 và phần ảo khác 0.

Lũy thừa của i quay vòng sau mỗi bốn bước: i, -1, -i, 1, rồi lặp lại. Muốn tính i^n, chỉ cần lấy n chia 4 rồi xem số dư.

> Lỗi thường gặp: nói phần ảo của 3 - 4i là -4i. Phần ảo là -4.

## Cộng, trừ và nhân số phức

Cộng và trừ thì làm riêng từng phần, giống như cộng hai vectơ tọa độ.

$$ (a + bi) + (c + di) = (a + c) + (b + d)i $$

Nhân thì cứ nhân bung ra như nhân đa thức, rồi dùng i^2 = -1 để thu gọn.

$$ (a + bi)(c + di) = (ac - bd) + (ad + bc)i $$

Không cần thuộc công thức này. Chỉ cần nhớ nhân bung rồi thay i^2 = -1, công thức sẽ tự hiện ra. Ví dụ với (2 + 3i)(1 - i):

1. Nhân bung: 2 . 1 + 2 . (-i) + 3i . 1 + 3i . (-i).
2. Gom lại: 2 - 2i + 3i - 3i^2.
3. Thay i^2 = -1: số hạng cuối thành +3.
4. Kết quả: 5 + i.

Phép cộng và phép nhân số phức giữ nguyên mọi tính chất quen thuộc: giao hoán, kết hợp, phân phối. Nhờ vậy mọi biến đổi đại số cũ vẫn dùng được.

> Lỗi thường gặp: quên rằng i^2 = -1 làm số hạng chứa i^2 đổi dấu khi nhập vào phần thực.

## Số phức liên hợp và môđun

Số phức liên hợp giữ phần thực, đổi dấu phần ảo. Trên mặt phẳng, đó là phép lấy đối xứng qua trục thực.

$$ \overline{z} = a - bi $$

Môđun là khoảng cách từ điểm biểu diễn z đến gốc tọa độ.

$$ |z| = \sqrt{a^{2} + b^{2}} $$

Hai đại lượng này gắn với nhau bằng một đẳng thức dùng suốt:

$$ z \cdot \overline{z} = a^{2} + b^{2} = |z|^{2} $$

Điều đáng chú ý là tích của z với liên hợp của nó luôn là một số thực không âm. Đó chính là mẹo để chia số phức ở mục sau.

Vài tính chất hay dùng:

- Tổng của z và liên hợp của nó bằng 2a, một số thực.
- Môđun của tích bằng tích các môđun.
- Môđun của tổng nói chung nhỏ hơn hoặc bằng tổng các môđun.

> Lỗi thường gặp: viết |z + w| = |z| + |w|. Lấy z = 1 và w = -1 là thấy sai ngay: vế trái bằng 0, vế phải bằng 2.

## Chia số phức

Chia cho một số phức khác 0 luôn làm được, bằng một mẹo duy nhất: nhân cả tử và mẫu với số phức liên hợp của mẫu, để mẫu thành số thực.

$$ \frac{a + bi}{c + di} = \frac{(a + bi)(c - di)}{c^{2} + d^{2}} $$

Sau bước đó, chỉ còn việc chia phần thực và phần ảo của tử cho số thực c^2 + d^2.

Ví dụ tính (1 + 2i) / (3 - i):

1. Liên hợp của mẫu là 3 + i.
2. Mẫu mới: 3^2 + (-1)^2 = 10.
3. Tử mới: (1 + 2i)(3 + i) = 3 + i + 6i + 2i^2 = 1 + 7i.
4. Kết quả: 1/10 + (7/10)i.

Trường hợp hay gặp nhất là chia cho i. Liên hợp của i là -i, nên nhân cả hai vế với -i là xong: 1/i = -i.

> Lỗi thường gặp: nhân tử và mẫu với liên hợp của tử. Phải là liên hợp của mẫu, vì mục đích là làm cho mẫu hết phần ảo.

## Dạng lượng giác và công thức Moivre

Thay vì mô tả z bằng hai tọa độ, mô tả nó bằng khoảng cách tới gốc và góc quay. Khoảng cách là môđun r, góc là acgumen.

$$ z = r(\cos \varphi + i \sin \varphi) $$

Ở dạng này, phép nhân trở nên rất đơn giản: nhân hai số phức thì nhân môđun và cộng acgumen. Nói cách khác, nhân với một số phức là vừa phóng to vừa quay.

Lặp lại phép nhân đó n lần cho công thức Moivre:

$$ z^{n} = r^{n}(\cos n\varphi + i \sin n\varphi) $$

Ví dụ với z = 1 + i: môđun là căn bậc hai của 2, acgumen là 45 độ. Vậy z^4 có môđun 4 và acgumen 180 độ, tức là z^4 = -4.

Tìm acgumen thì cứ nhìn vị trí của điểm (a, b) trên mặt phẳng: trục thực dương ứng với 0 độ, trục ảo dương 90 độ, trục thực âm 180 độ, trục ảo âm 270 độ.

> Lỗi thường gặp: dùng công thức Moivre mà quên nhân acgumen với n, chỉ nâng môđun lên lũy thừa.

## Căn bậc n của số phức

Trong tập số thực, số âm không có căn bậc hai. Trong tập số phức, mọi số khác 0 đều có đủ n căn bậc n khác nhau.

$$ z^{n} = w \quad \Leftrightarrow \quad z \text{ la can bac } n \text{ cua } w $$

Lý do nằm ở dạng lượng giác: môđun của mọi căn đều bằng căn bậc n của môđun w, còn acgumen thì có n lựa chọn, cách đều nhau 360/n độ.

Vì vậy n căn bậc n của một số nằm trên cùng một đường tròn, chia đường tròn đó thành n phần bằng nhau. Với n = 2 là hai điểm đối xứng qua gốc; với n = 6 là sáu đỉnh của một lục giác đều.

Ví dụ bốn căn bậc bốn của 16: môđun đều bằng 2, acgumen là 0, 90, 180, 270 độ. Vậy chúng là 2, 2i, -2 và -2i, trong đó hai căn là số thực.

Muốn tìm căn bậc hai mà không dùng lượng giác, đặt căn cần tìm là x + yi rồi bình phương lên, so phần thực với phần thực và phần ảo với phần ảo.

> Lỗi thường gặp: trả lời "phương trình z^5 = 1 có một nghiệm z = 1". Trong tập số phức nó có đúng 5 nghiệm.
