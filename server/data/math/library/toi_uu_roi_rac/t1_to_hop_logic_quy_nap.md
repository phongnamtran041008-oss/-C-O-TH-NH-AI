---
id: tr_lib_t1
title_vi: Tổ hợp mở đầu, logic mệnh đề và quy nạp
subject: toi_uu_roi_rac
floor: 1
summary_vi: Ba món đồ nghề của người tu toán rời rạc: liệt kê và đếm những cách sắp đặt, nói cho chặt bằng mệnh đề, và chứng minh một điều đúng mãi mãi bằng quy nạp.
skills: [tr_t1_cau_hinh, tr_t1_cong_nhan, tr_t1_menh_de, tr_t1_bang_chan_tri, tr_t1_quy_nap]
---
## Cấu hình tổ hợp

Toán rời rạc hỏi rất nhiều câu dạng "có bao nhiêu cách". Mỗi cách là một cấu hình: một cách sắp đặt các vật theo đúng luật của bài. Trước khi đếm, phải trả lời rõ hai câu hỏi.

- Thứ tự có quan trọng không? Xếp An rồi Bình vào hai ghế khác với xếp Bình rồi An; nhưng chọn An và Bình vào một tổ thì chỉ là một cách.
- Một vật có được dùng lại không? Mật lệnh được lặp ký tự; một hàng người thì không ai đứng hai chỗ.

Bốn loại cấu hình gặp suốt bí cảnh này:

- Dãy có thứ tự, không lặp: xếp người vào ghế, trao giải nhất nhì ba.
- Dãy có thứ tự, được lặp: xâu ký tự, mật lệnh, xâu nhị phân.
- Hoán vị: dãy có thứ tự dùng hết mọi vật, mỗi vật một lần.
- Tập con: chọn một nhóm, không kể thứ tự.

Khi bài còn nhỏ, cách chắc chắn nhất là liệt kê có hệ thống, để không sót và không trùng. Ví dụ các tập con 2 phần tử của {a, b, c, d}:

1. Ghép a với từng chữ đứng sau nó: {a, b}, {a, c}, {a, d}.
2. Ghép b với từng chữ đứng sau nó: {b, c}, {b, d}.
3. Ghép c với chữ đứng sau nó: {c, d}.
4. Không ghép ngược lại (như {b, a}) vì đó là tập đã có. Tất cả 6 tập.

Xâu nhị phân độ dài n là dãy n chữ số 0 hoặc 1. Mỗi vị trí có 2 khả năng nên có tất cả 2^n xâu.

> Lỗi thường gặp: liệt kê không theo thứ tự nào cả rồi đếm. Gần như chắc chắn sẽ sót một cấu hình (như sót 111 khi tìm xâu có hai chữ số 1 liền nhau) hoặc đếm một cấu hình hai lần.

## Quy tắc cộng và quy tắc nhân

Hai quy tắc này là gốc của mọi phép đếm.

Quy tắc cộng: nếu mọi cách làm rơi vào đúng một trong các trường hợp rời nhau, thì số cách bằng tổng số cách của từng trường hợp.

$$ |A_1 \cup A_2 \cup \cdots \cup A_k| = |A_1| + |A_2| + \cdots + |A_k| $$

Quy tắc nhân: nếu một việc gồm các bước nối tiếp, bước thứ i luôn có n_i cách dù các bước trước chọn gì, thì số cách bằng tích.

$$ |A_1 \times A_2 \times \cdots \times A_k| = |A_1| \cdot |A_2| \cdots |A_k| $$

Cách nhớ: chữ "hoặc" giữa các trường hợp thường dẫn tới phép cộng, chữ "rồi" giữa các bước thường dẫn tới phép nhân.

Ví dụ: có bao nhiêu số chẵn có 3 chữ số đôi một khác nhau?

1. Chữ số 0 làm khó hàng trăm, nên chia trường hợp theo hàng đơn vị.
2. Hàng đơn vị là 0: hàng trăm 9 cách, hàng chục 8 cách, được 72 số.
3. Hàng đơn vị là 2, 4, 6 hoặc 8: 4 cách; hàng trăm khác 0 và khác hàng đơn vị nên 8 cách; hàng chục 8 cách; được 4 . 8 . 8 = 256 số.
4. Hai trường hợp rời nhau, cộng lại: 72 + 256 = 328.

> Lỗi thường gặp: nhân khi số cách ở một bước lại phụ thuộc vào lựa chọn trước đó. Nếu chọn hàng đơn vị sau cùng thì số cách của nó tùy vào việc hàng trăm, hàng chục đã dùng số chẵn chưa. Hãy đổi thứ tự các bước hoặc chia trường hợp cho số cách ở mỗi bước luôn cố định.

## Mệnh đề và các phép nối

Mệnh đề là một câu khẳng định đúng hoặc sai, chỉ một trong hai. "7 là số nguyên tố" là mệnh đề đúng; "2 + 2 = 5" là mệnh đề sai; "Hãy ngồi xuống!" hay "x lớn hơn 3" (khi chưa biết x) không phải mệnh đề.

Từ các mệnh đề p, q ta lập mệnh đề mới bằng năm phép nối. Trong game chúng được viết bằng chữ:

- không p (phủ định): đúng khi p sai.
- p và q (hội): đúng khi cả hai đều đúng.
- p hoặc q (tuyển): sai chỉ khi cả hai đều sai.
- p => q (kéo theo): sai chỉ khi p đúng mà q sai.
- p <=> q (tương đương): đúng khi p và q cùng chân trị.

$$ p \Rightarrow q \text{ sai } \Leftrightarrow p \text{ dung va } q \text{ sai} $$

Phép kéo theo hay làm người mới bối rối nhất. Hãy coi p => q như một lời hứa: "Nếu trời mưa thì ta mang ô". Lời hứa chỉ bị phá khi trời mưa mà không mang ô. Trời không mưa thì mang hay không, lời hứa vẫn giữ. Vì vậy "Nếu 2 + 2 = 5 thì 3 là số chẵn" là mệnh đề đúng.

Phủ định của "mọi x đều có tính chất P" là "có ít nhất một x không có tính chất P", không phải "mọi x đều không có P".

Ví dụ với p đúng, q sai, r đúng, tính (p => q) hoặc (q <=> r):

1. p đúng, q sai nên p => q sai.
2. q sai, r đúng, khác chân trị, nên q <=> r sai.
3. Hai vế của phép hoặc đều sai nên cả mệnh đề sai.

> Lỗi thường gặp: nghĩ p => q sai khi p sai. Vế trước sai thì phép kéo theo luôn đúng, bất kể vế sau.

## Bảng chân trị và tương đương logic

Bảng chân trị liệt kê mọi cách gán đúng, sai cho các biến và chân trị của mệnh đề ở từng dòng. n biến cho 2^n dòng: 2 biến 4 dòng, 3 biến 8 dòng.

Hai mệnh đề tương đương logic khi chúng có cùng chân trị ở mọi dòng. Muốn chứng tỏ hai mệnh đề không tương đương, chỉ cần chỉ ra một dòng mà chúng khác nhau.

Một mệnh đề đúng ở mọi dòng là hằng đúng, như p hoặc (không p).

Những tương đương dùng nhiều nhất:

$$ p \Rightarrow q \equiv \neg p \lor q $$

$$ \neg(p \land q) \equiv \neg p \lor \neg q $$

$$ \neg(p \lor q) \equiv \neg p \land \neg q $$

$$ p \Rightarrow q \equiv \neg q \Rightarrow \neg p $$

Hai công thức giữa là luật De Morgan: đưa phủ định vào trong ngoặc thì "và" đổi thành "hoặc", "hoặc" đổi thành "và". Công thức cuối nói mệnh đề phản đảo (không q) => (không p) tương đương với p => q, và đó là gốc của cách chứng minh phản chứng.

Ví dụ rút gọn không (p => q):

1. Viết p => q thành (không p) hoặc q.
2. Phủ định và dùng De Morgan: (không (không p)) và (không q).
3. Bỏ phủ định kép: p và (không q).

> Lỗi thường gặp: nhầm mệnh đề đảo q => p với mệnh đề phản đảo. Đảo không tương đương với mệnh đề gốc: lấy p sai, q đúng thì p => q đúng còn q => p sai.

## Chứng minh bằng quy nạp

Quy nạp chứng minh một mệnh đề P(n) đúng với mọi n từ một số n_0 trở đi, bằng hai bước:

- Bước cơ sở: kiểm tra P(n_0) đúng.
- Bước quy nạp: giả sử P(k) đúng với một k >= n_0 nào đó (giả thiết quy nạp), chứng minh P(k + 1) đúng.

$$ P(1) \land \big(P(k) \Rightarrow P(k+1)\big) \Rightarrow \forall n \ge 1,\ P(n) $$

Hãy hình dung một hàng quân domino: bước cơ sở đẩy quân đầu tiên, bước quy nạp bảo đảm quân nào đổ cũng làm quân sau đổ.

Ví dụ chứng minh 1 + 3 + 5 + ... + (2n - 1) = n^2:

1. Cơ sở: n = 1, vế trái là 1, vế phải là 1^2 = 1.
2. Giả thiết quy nạp: 1 + 3 + ... + (2k - 1) = k^2.
3. Cộng số lẻ tiếp theo, 2k + 1, vào hai vế: tổng của k + 1 số lẻ đầu tiên bằng k^2 + 2k + 1 = (k + 1)^2.
4. Đó chính là công thức với n = k + 1, nên đẳng thức đúng với mọi n >= 1.

Với bất đẳng thức, bước cơ sở không phải lúc nào cũng là n = 1. Chẳng hạn 2^n > n^2 sai ở n = 2, 3, 4 nhưng đúng với mọi n >= 5, nên phải bắt đầu từ n_0 = 5.

> Lỗi thường gặp: bỏ bước cơ sở. Mệnh đề "n = n + 1" có bước quy nạp đúng (cộng 1 vào hai vế) nhưng sai với mọi n. Lỗi thứ hai hay gặp là biến đổi đại số ẩu ở bước k sang k + 1: luôn khai triển lại để kiểm tra.
