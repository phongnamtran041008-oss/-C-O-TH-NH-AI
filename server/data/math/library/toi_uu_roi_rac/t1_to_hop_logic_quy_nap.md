---
id: tr_lib_t1
title_vi: Tổ hợp mở đầu, logic mệnh đề và quy nạp
subject: toi_uu_roi_rac
floor: 1
format: 2
summary_vi: Ba món đồ nghề đầu tiên: hỏi đúng hai câu trước khi đếm, đếm bằng cộng và nhân, nói cho chặt bằng mệnh đề và bảng chân trị, rồi chứng minh một điều đúng mãi mãi bằng quy nạp.
skills: [tr_t1_cau_hinh, tr_t1_cong_nhan, tr_t1_menh_de, tr_t1_bang_chan_tri, tr_t1_quy_nap]
---
## Cấu hình tổ hợp

:::hook
Đặt mật khẩu, chọn tổ đi bí cảnh, xếp đệ tử vào hàng: đều là câu hỏi "có bao nhiêu cách". Nhận sai loại cách là đếm sai từ đầu.
:::

:::figure grid
caption: Hai câu hỏi xếp mọi bài đếm vào bốn ô; mỗi ô là một loại cấu hình.
table
head "không lặp" "được lặp"
side "có thứ tự" "không thứ tự"
row "hoán vị, xếp chỗ" "xâu, mật khẩu"
row "tập con, nhóm" "chia kẹo (tầng 2)"
mark cell 1 2 xanh
mark cell 2 1 vang
:::

:::core
Cấu hình là một cách sắp đặt. Trước khi đếm, hỏi: đổi thứ tự có ra cách mới không, và một vật có được dùng lại không?
:::

Tập {1, 2} và {2, 1} là một, còn cặp (1, 2) khác (2, 1). Xâu nhị phân dài n có 2^n xâu. Vị trí bị ép có ít cách hơn: chữ đầu cố định chỉ có 1 cách; bảng m chữ mà chỉ cần khác chữ ngay trước thì còn m - 1 cách.

Ví dụ: liệt kê mọi tập con 3 phần tử của {a, b, c, d}.

1. Viết chữ theo thứ tự a, b, c, d, chỉ ghép chữ đứng sau.
2. Bắt đầu bằng a: {a, b, c}, {a, b, d}, {a, c, d}.
3. Bắt đầu bằng b: {b, c, d}. Có 4 tập.

> Lỗi thường gặp: liệt kê lộn xộn rồi đếm. Đếm xâu có "11" liền nhau mà quên 111 là sót ngay một cấu hình.

:::check
Q: Tô 4 ô thành hàng bằng 3 màu, hai ô kề nhau khác màu: mấy cách?
A: Ô đầu 3 cách; mỗi ô sau chỉ cần khác ô ngay trước: 2 cách. 3 . 2 . 2 . 2 = 24.
:::

## Quy tắc cộng và quy tắc nhân

:::hook
Gói tin đi từ máy A tới máy C: qua bộ định tuyến B, hoặc theo cáp thẳng. Có bao nhiêu tuyến gửi?
:::

:::figure graph
caption: Qua B phải đi XONG hai chặng: 3 . 2 = 6. Đi thẳng là trường hợp khác: thêm 2. Tổng 8.
size: 200 55
layout: free
node A 0 1 "A"
node B 2 2 "B"
node C 4 1 "C"
edge A B "3 đường" xanh
edge B C "2 đường" xanh
edge A C "2 đường thẳng" vang
:::

:::core
Chọn MỘT trong các trường hợp rời nhau thì cộng; phải làm XONG mọi bước nối tiếp thì nhân.
:::

Cộng cần các trường hợp không có cách nào chung. Nhân cần số cách mỗi bước không đổi, dù bước trước chọn gì.

Ví dụ: có bao nhiêu số chẵn có 3 chữ số khác nhau lập từ 0, 1, 2, 3, 4?

1. Số 0 vừa chẵn vừa cấm ở hàng trăm, nên chia theo hàng đơn vị.
2. Đơn vị là 0: hàng trăm 4 cách, hàng chục 3 cách: 12 số. Đơn vị là 2 hoặc 4: hàng trăm khác 0 và khác nó còn 3 cách, hàng chục 3 cách: 2 . 3 . 3 = 18 số.
3. Hai trường hợp rời nhau: 12 + 18 = 30.

> Lỗi thường gặp: nhân khi số cách của một bước còn tùy bước trước. Hãy đổi thứ tự các bước, hoặc chia trường hợp.

:::check
Q: 5 kiếm, 2 đao. Lấy 1 binh khí: mấy cách? Lấy 1 kiếm VÀ 1 đao: mấy cách?
A: Một binh khí: kiếm hoặc đao, 5 + 2 = 7. Một kiếm và một đao: hai bước, 5 . 2 = 10.
:::

## Mệnh đề và các phép nối

:::hook
Lệnh if chỉ hỏi điều kiện đúng hay sai. Logic mệnh đề tính đúng sai của những điều kiện ghép.
:::

:::figure grid
caption: Mỗi cột là luật của một phép nối. Kéo theo chỉ sai ở dòng đỏ: p đúng mà q sai.
table
head "p" "q" "p và q" "p hoặc q" "p => q" "p <=> q"
row Đ Đ Đ Đ Đ Đ
row Đ S S Đ S S
row S Đ S Đ Đ S
row S S S S Đ Đ
mark cell 2 5 do
:::

:::core
Và cần cả hai đúng; hoặc chỉ sai khi cả hai sai; kéo theo chỉ sai khi vế trước đúng, vế sau sai; tương đương đúng khi hai vế cùng chân trị.
:::

Mệnh đề là câu chỉ có một chân trị: đúng hoặc sai. Câu mệnh lệnh, hay "x > 3" khi chưa biết x, không phải mệnh đề. Phủ định của "mọi x đều P" là "có ít nhất một x không P".

Ví dụ: p sai, q đúng, r sai. Tính (p hoặc q) => r.

1. Trong ngoặc trước: q đúng nên p hoặc q đúng.
2. Đúng => sai là dòng duy nhất làm kéo theo sai: mệnh đề sai.

> Lỗi thường gặp: nghĩ p => q sai khi p sai. Như lời hứa "nếu mưa thì mang ô": trời không mưa thì không thể thất hứa.

:::check
Q: Biết p => q đúng và p đúng. q đúng hay sai? Nhìn bảng mà trả lời.
A: q đúng: trong các dòng có p đúng, chỉ dòng q đúng làm p => q đúng.
:::

## Bảng chân trị và tương đương logic

:::hook
Hai cách viết điều kiện if có chạy giống nhau không? Thử hết mọi tổ hợp đúng sai là biết chắc.
:::

:::figure grid
caption: Hai cột xanh trùng nhau ở cả 4 dòng nên tương đương. Cột q => p lệch ở dòng đỏ nên không.
table
head "p" "q" "p => q" "(không p) hoặc q" "q => p"
row Đ Đ Đ Đ Đ
row Đ S S S Đ
row S Đ Đ Đ S
row S S Đ Đ Đ
mark col 3 xanh
mark col 4 xanh
mark cell 3 5 do
:::

:::core
Hai mệnh đề tương đương khi cột chân trị trùng nhau ở MỌI dòng; một dòng lệch là đủ bác bỏ.
:::

n biến cho 2^n dòng. Đúng ở mọi dòng là hằng đúng, như p hoặc (không p).

- De Morgan: không (p và q) là (không p) hoặc (không q), và ngược lại.
- Phản đảo: p => q tương đương (không q) => (không p).
- Không (p => q) là p và (không q).

Ví dụ: (p hoặc q) và (không r) đúng ở mấy trong 8 dòng?

1. p hoặc q chỉ sai khi p, q cùng sai: đúng ở 3 trong 4 cách gán p, q.
2. Còn cần r sai (1 cách): 3 . 1 = 3 dòng.

> Lỗi thường gặp: lẫn đảo q => p với phản đảo. Chỉ phản đảo giữ nguyên nghĩa.

:::check
Q: (p và q) => p có phải hằng đúng không? Không cần lập bảng.
A: Có. Muốn sai thì p và q phải đúng, tức p đúng, mà vế sau p lại phải sai: vô lý.
:::

## Chứng minh bằng quy nạp

:::hook
Vòng lặp đúng ở lần đầu, và lần nào đúng thì lần sau cũng đúng: vậy nó đúng ở mọi lần.
:::

:::figure flow
caption: Cơ sở đẩy quân domino đầu; bước quy nạp: quân nào đổ cũng xô đổ quân kế.
box "P(1) đúng" luc
link "P(k) => P(k+1)"
box "P(2)" xanh
link "=>"
box "P(3)" xanh
link "=>"
box "..."
link ""
box "mọi n" luc
:::

:::core
Quy nạp cần cả cơ sở P(n_0) đúng lẫn bước P(k) => P(k + 1); thiếu một việc là cả chuỗi sụp.
:::

Ví dụ: chứng minh 2 + 4 + ... + 2n = n(n + 1) với mọi n >= 1.

1. Cơ sở n = 1: vế trái 2, vế phải 1 . 2 = 2.
2. Giả thiết quy nạp: 2 + 4 + ... + 2k = k(k + 1).
3. Thêm số hạng cuối khi n = k + 1, là 2(k + 1): được (k + 1)(k + 2).

Cơ sở có thể muộn: 2^n > 3n sai khi n <= 3, nên n_0 = 4. Tổng 1 + 3 + ... + 19 có 2n - 1 = 19, nên n = 10, tổng 100.

> Lỗi thường gặp: khai triển ẩu ở bước k sang k + 1.

:::check
Q: Bước quy nạp của "n^2 + n là số lẻ" chạy được. Vậy nó lẻ với mọi n?
A: Không: cơ sở sai, 1 + 1 = 2 chẵn. (k + 1)^2 + (k + 1) = (k^2 + k) + 2(k + 1) chỉ chuyển cái đúng đi tiếp; thực ra n^2 + n luôn chẵn.
:::
