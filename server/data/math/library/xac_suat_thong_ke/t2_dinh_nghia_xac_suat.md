---
id: xs_lib_t2
title_vi: Định nghĩa xác suất: cổ điển và thống kê
subject: xac_suat_thong_ke
floor: 2
summary_vi: Hai cách gán cho mỗi sự kiện một con số từ 0 đến 1: đếm khi các kết quả đồng khả năng, và đo tần suất khi đã thử rất nhiều lần.
skills: [xs_t2_co_dien, xs_t2_co_dien_to_hop, xs_t2_hoan_lai, xs_t2_tinh_chat, xs_t2_thong_ke]
---
## Xác suất cổ điển

Khi phép thử có n kết quả đồng khả năng (không kết quả nào dễ xảy ra hơn kết quả nào), và sự kiện A gồm m trong số đó, thì xác suất của A là:

$$ P(A) = \frac{m}{n} $$

m gọi là số kết quả thuận lợi cho A. Đồng xu cân đối, xúc xắc cân đối, rút ngẫu nhiên một phiếu trong hộp là những phép thử đồng khả năng quen thuộc.

Điều kiện "đồng khả năng" là cốt lõi. Hộp có 3 bi đỏ, 5 bi xanh, 2 bi vàng thì ba màu không đồng khả năng; mười viên bi mới đồng khả năng. Lấy bi không phải màu xanh có xác suất 5/10 = 1/2, không phải 2/3.

Ví dụ gieo hai xúc xắc cân đối, tính xác suất tổng số chấm bằng 5:

1. Một kết quả là cặp có thứ tự (xúc xắc 1, xúc xắc 2); có 36 cặp đồng khả năng.
2. Các cặp có tổng 5: (1, 4), (2, 3), (3, 2), (4, 1), tức 4 cặp.
3. P = 4/36 = 1/9.

Tổng t của hai xúc xắc (t từ 2 đến 12) đến từ 6 - |t - 7| cặp: tổng 7 nhiều cặp nhất (6 cặp), tổng 2 và 12 ít nhất (1 cặp).

> Lỗi thường gặp: tung ba đồng xu rồi coi "0, 1, 2, 3 mặt ngửa" là bốn kết quả đồng khả năng. Các kết quả đồng khả năng là 8 bộ mặt; đúng hai mặt ngửa có 3 bộ, nên xác suất là 3/8 chứ không phải 1/4.

## Xác suất cổ điển dùng tổ hợp

Khi không gian mẫu quá lớn để liệt kê, đếm m và n bằng các công cụ của tầng 1. Lấy đồng thời k vật thì kết quả là một nhóm không có thứ tự, nên đếm bằng tổ hợp.

Hộp có a bi đỏ và b bi xanh, lấy đồng thời k bi, xác suất được đúng r bi đỏ:

$$ P = \frac{C_a^r \cdot C_b^{k-r}}{C_{a+b}^k} $$

Ví dụ hộp có 5 bi trắng và 3 bi đen, lấy đồng thời 3 bi, tính xác suất có đúng 1 bi đen:

1. Không gian mẫu: C(8, 3) = 56 nhóm 3 bi.
2. Thuận lợi: 1 bi đen trong 3 và 2 bi trắng trong 5, C(3, 1) . C(5, 2) = 3 . 10 = 30.
3. P = 30/56 = 15/28.

Rút bài cũng vậy: rút đồng thời 2 lá từ bộ 52 lá có C(52, 2) = 1326 kết quả. Hai lá cùng là át có C(4, 2) = 6 kết quả, xác suất 6/1326 = 1/221.

Xếp người thành hàng thì kết quả là một hoán vị: 5 người xếp hàng có 5! = 120 cách đồng khả năng, An và Bình đứng cạnh nhau có 48 cách, nên xác suất là 2/5.

> Lỗi thường gặp: đếm mẫu số có thứ tự (A(8, 3) = 336) mà tử số không thứ tự (C(3, 1) . C(5, 2) = 30). Tử và mẫu phải đếm cùng một kiểu, nếu không đáp số sai hẳn: 30/336 thay vì 30/56.

## Lấy có hoàn lại và không hoàn lại

Lấy hai lần từ một hộp có n vật có ba cách hiểu khác nhau, và mỗi cách cho một không gian mẫu khác:

- Lần lượt, có hoàn lại (lấy xong trả vào hộp): mỗi lần đều có n cách, n . n kết quả có thứ tự.
- Lần lượt, không hoàn lại: lần sau còn n - 1 cách, n(n - 1) kết quả có thứ tự.
- Đồng thời: nhóm hai vật không thứ tự, C(n, 2) kết quả.

$$ n^2, \qquad n(n-1), \qquad C_n^2 = \frac{n(n-1)}{2} $$

Hai cách sau thực chất cho cùng xác suất cho mọi sự kiện không phụ thuộc thứ tự, vì mỗi nhóm hai vật ứng với đúng hai cặp có thứ tự. Chỉ cần tử và mẫu đếm cùng một kiểu.

Ví dụ hộp 4 bi trắng, 2 bi đen, lấy lần lượt 2 bi không hoàn lại, tính xác suất hai bi khác màu:

1. Không gian mẫu có thứ tự: 6 . 5 = 30.
2. Trắng rồi đen: 4 . 2 = 8; đen rồi trắng: 2 . 4 = 8; tổng 16.
3. P = 16/30 = 8/15. Đếm theo nhóm cũng ra 4 . 2 / C(6, 2) = 8/15.

Một điều bất ngờ: không hoàn lại thì xác suất lần thứ hai được bi đỏ vẫn bằng tỷ lệ bi đỏ ban đầu, vì khi chưa biết lần đầu ra gì, mọi viên bi đều có cùng khả năng nằm ở lần thứ hai.

> Lỗi thường gặp: lấy không hoàn lại mà vẫn viết không gian mẫu n . n. Với 5 bi đỏ và 3 bi xanh, cả hai đều đỏ có xác suất 20/56 = 5/14; viết 20/64 là đã trộn hai cách lấy với nhau.

## Tính chất của xác suất và sự kiện đối

Mọi xác suất đều nằm giữa 0 và 1. Sự kiện không thể có xác suất 0, sự kiện chắc chắn có xác suất 1. Hai sự kiện xung khắc thì xác suất của tổng bằng tổng các xác suất.

$$ 0 \le P(A) \le 1, \qquad P(\Omega) = 1 $$

Vì A và Ā xung khắc và gộp lại thành sự kiện chắc chắn, ta có P(A) + P(Ā) = 1, tức là P(Ā) = 1 - P(A).

Công thức này mạnh nhất với các câu "có ít nhất một": sự kiện đối của nó là "không có cái nào", thường đếm rất dễ.

Ví dụ gieo hai xúc xắc, tính xác suất có ít nhất một mặt 6:

1. Sự kiện đối: không xúc xắc nào ra 6, mỗi xúc xắc có 5 cách, tức 25 trong 36 kết quả.
2. P = 1 - 25/36 = 11/36.

Mật khẩu 4 chữ số ngẫu nhiên có ít nhất hai chữ số trùng nhau: sự kiện đối là bốn chữ số khác nhau, 10 . 9 . 8 . 7 = 5040 trong 10000, nên xác suất là 1 - 5040/10000 = 62/125.

> Lỗi thường gặp: viết sự kiện đối của "có ít nhất một mặt ngửa" là "có ít nhất một mặt sấp". Hai sự kiện này cùng xảy ra được (ví dụ SN), nên chúng không đối nhau. Đối đúng là "không có mặt ngửa nào".

## Định nghĩa thống kê: tần suất

Nhiều phép thử không có các kết quả đồng khả năng: một sản phẩm có hỏng không, một xạ thủ có bắn trúng không. Khi đó ta làm thử nhiều lần. Nếu trong n lần thử, sự kiện A xảy ra m lần thì tần suất của A là:

$$ f_n(A) = \frac{m}{n} $$

Khi n rất lớn, tần suất dao động ngày càng sát một số cố định, và số đó được lấy làm xác suất của A. Đó là định nghĩa thống kê.

Ví dụ một xạ thủ tập ba ngày: bắn 20 trúng 15, bắn 30 trúng 24, bắn 10 trúng 9:

1. Gộp tất cả: bắn 20 + 30 + 10 = 60 phát, trúng 15 + 24 + 9 = 48 phát.
2. Tần suất bắn trúng: 48/60 = 4/5.

Dùng ngược lại: nếu tần suất hỏng ổn định quanh 1/50 thì trong 1500 sản phẩm có khoảng 1500 . 1/50 = 30 sản phẩm hỏng. Ước lượng số cá trong hồ bằng cách đánh dấu rồi bắt lại cũng dựa vào ý này.

> Lỗi thường gặp: tưởng tần suất sau ít lần thử phải bằng xác suất. Tung đồng xu cân đối 10 lần không chắc ra đúng 5 lần ngửa, và gieo xúc xắc 60 lần thấy 12 lần mặt 6 cũng chưa đủ để nói xúc xắc lệch.
