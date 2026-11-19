---
id: xs_lib_t4
title_vi: Công thức xác suất đầy đủ và công thức Bayes
subject: xac_suat_thong_ke
floor: 4
summary_vi: Khi một phép thử đi qua nhiều giai đoạn, ta chia nó theo các trường hợp của giai đoạn đầu: cộng lại để được xác suất của kết quả cuối (công thức đầy đủ), hoặc đi ngược lại để biết kết quả đó nhiều khả năng đến từ trường hợp nào (công thức Bayes).
skills: [xs_t4_he_day_du, xs_t4_so_do_cay, xs_t4_day_du, xs_t4_bayes, xs_t4_bayes_ung_dung]
---
## Hệ đầy đủ các sự kiện

Một họ sự kiện H_1, H_2, ..., H_n là một hệ đầy đủ khi có đủ hai điều:

- Đôi một xung khắc: không có hai sự kiện nào cùng xảy ra.
- Tổng của chúng là sự kiện chắc chắn: lần thử nào cũng có một H_i xảy ra.

Nói gọn: mỗi kết quả của phép thử thuộc đúng một H_i. Khi đó các xác suất cộng lại bằng 1:

$$ P(H_1) + P(H_2) + \cdots + P(H_n) = 1 $$

Ví dụ gieo một xúc xắc: {1}, {2, 3}, {4, 5, 6} là hệ đầy đủ. Họ {1, 2}, {2, 3, 4}, {5, 6} thì không (mặt 2 thuộc hai sự kiện), họ {1, 2}, {3, 4} cũng không (thiếu mặt 5 và 6).

Hệ đầy đủ đơn giản nhất là A và Ā. Rút một lá bài: {đỏ, đen} và {cơ, rô, bích, nhép} đều là hệ đầy đủ; còn {đỏ, cơ, đen} phủ hết bộ bài nhưng không xung khắc.

Bài ngược: H_1, H_2, H_3 là hệ đầy đủ, P(H_1) = 2P(H_2), P(H_2) = 2P(H_3). Đặt P(H_3) = t thì 4t + 2t + t = 1, nên P(H_1) = 4/7.

> Lỗi thường gặp: chỉ kiểm tra tổng là sự kiện chắc chắn mà quên điều xung khắc. Sinh viên học tiếng Anh và sinh viên học tiếng Pháp phủ cả lớp khi ai cũng học ít nhất một thứ tiếng, nhưng người học cả hai làm hai sự kiện chồng lên nhau; hệ đầy đủ đúng là: chỉ Anh, chỉ Pháp, cả hai.

## Sơ đồ cây cho phép thử nhiều giai đoạn

Một phép thử làm qua nhiều bước (chọn hộp rồi lấy bi, chọn súng rồi bắn) được vẽ thành cây:

- Mỗi nút là một tình huống, các nhánh đi ra là các khả năng của bước tiếp theo; các nhánh từ một nút có xác suất cộng lại bằng 1.
- Số trên một nhánh ở tầng sau là xác suất có điều kiện, khi đã biết các bước trước.
- Xác suất của một đường đi bằng tích các số dọc đường đi (công thức nhân).

$$ P(H_i A) = P(H_i)\,P(A \mid H_i) $$

Ví dụ hộp I có 2 bi đỏ, 3 bi xanh; hộp II có 4 bi đỏ, 1 bi xanh; tung đồng xu chọn hộp rồi lấy 1 bi:

1. Nhánh đầu: hộp I với xác suất 1/2.
2. Nhánh sau: đỏ với xác suất P(đỏ | hộp I) = 2/5.
3. Đường đi "hộp I rồi bi đỏ" có xác suất 1/2 . 2/5 = 1/5.

Lấy không hoàn lại cũng là cây: hộp 2 bi đỏ, 2 bi xanh, lấy đến khi được bi đỏ, đường đi "xanh, xanh, đỏ" có xác suất 2/4 . 1/3 . 1 = 1/6.

> Lỗi thường gặp: ghi trên nhánh tầng sau xác suất như lúc chưa lấy gì. Hộp 3 đỏ, 2 xanh, sau khi lấy 1 bi xanh thì hộp còn 4 bi với 3 bi đỏ: nhánh "đỏ" là 3/4, không phải 3/5.

## Công thức xác suất đầy đủ

Nếu H_1, ..., H_n là một hệ đầy đủ thì sự kiện A xảy ra theo đúng một trong các đường đi H_i rồi A. Cộng các đường đi đó:

$$ P(A) = \sum_{i=1}^{n} P(H_i)\,P(A \mid H_i) $$

Ví dụ phân xưởng I làm 3/5 sản phẩm với tỉ lệ phế phẩm 1/20, phân xưởng II làm 2/5 với tỉ lệ 1/10:

1. Hệ đầy đủ: H_1, H_2 là sản phẩm của phân xưởng I, II.
2. P(phế phẩm) = 3/5 . 1/20 + 2/5 . 1/10 = 3/100 + 4/100 = 7/100.

Bài chuyển bi: hộp I có 3 trắng, 2 đen; hộp II có 2 trắng, 4 đen; chuyển 1 bi từ I sang II rồi lấy 1 bi từ II. Hệ đầy đủ là màu bi được chuyển: P(trắng) = 3/5 . 3/7 + 2/5 . 2/7 = 13/35.

Công thức còn dùng ngược: biết tỉ lệ chung 1/20 và phân xưởng I (2/3 sản phẩm) có tỉ lệ 1/30, giải 2/3 . 1/30 + 1/3 . x = 1/20 được tỉ lệ của phân xưởng II là x = 1/12.

> Lỗi thường gặp: lấy trung bình cộng các P(A | H_i). Ba máy làm 1/2, 3/10, 1/5 sản phẩm với tỉ lệ phế phẩm 1/50, 1/25, 1/20 cho P(A) = 4/125; chia đều cho 3 là coi ba máy làm số sản phẩm như nhau.

## Công thức Bayes

Biết A đã xảy ra, xác suất của giả thuyết H_k được tính lại bằng phần của đường đi H_k trong tổng P(A):

$$ P(H_k \mid A) = \frac{P(H_k)\,P(A \mid H_k)}{P(A)} $$

trong đó P(A) tính bằng công thức đầy đủ. P(H_k) gọi là xác suất tiên nghiệm (trước khi biết A), P(H_k | A) là xác suất hậu nghiệm.

Ví dụ hai phân xưởng ở trên, lấy được một phế phẩm:

1. P(A) = 7/100 (công thức đầy đủ).
2. P(H_2 | A) = (2/5 . 1/10)/(7/100) = (4/100)/(7/100) = 4/7.

Phân xưởng II làm ít sản phẩm hơn nhưng lại có nhiều khả năng là nơi làm ra phế phẩm đó. Các P(H_k | A) cộng lại bằng 1, dùng để tự kiểm tra.

> Lỗi thường gặp: lẫn P(H_k | A) với P(A | H_k). "Phế phẩm này do phân xưởng II làm ra" là P(H_2 | A); còn P(A | H_2) chỉ là tỉ lệ phế phẩm của phân xưởng II. Một lỗi khác là bỏ P(H_k) ở tử số: 9 hộp loại I (1 đỏ, 9 xanh) và 1 hộp loại II (9 đỏ, 1 xanh), lấy được bi đỏ thì hộp loại II chỉ có xác suất 1/2, không phải 9/10.

## Bayes trong xét nghiệm và phân loại

Bài xét nghiệm là Bayes với hệ đầy đủ {mắc bệnh, không mắc bệnh}. Gọi B là sự kiện mắc bệnh, D là kết quả dương tính, p = P(B) là tỉ lệ mắc bệnh (tỉ lệ nền), s = P(D | B), và f là xác suất dương tính nhầm ở người khỏe:

$$ P(B \mid D) = \frac{p\,s}{p\,s + (1-p)\,f} $$

Ví dụ p = 1/100, s = 9/10, f = 1/10. Nghĩ theo 1000 người:

1. 10 người bệnh, 9 người dương tính.
2. 990 người khỏe, 99 người dương tính nhầm.
3. P(bệnh | dương tính) = 9/(9 + 99) = 1/12.

Bệnh càng hiếm thì người khỏe dương tính nhầm càng lấn át. Xét nghiệm lần hai (độc lập khi đã biết tình trạng bệnh) làm xác suất tăng mạnh: hai lần dương tính cho 81/(81 + 99) = 9/20. Cùng một xét nghiệm, vùng có tỉ lệ bệnh cao hơn thì kết quả dương tính đáng tin hơn.

Lọc thư rác cũng vậy: thư rác chiếm 1/4, từ "trúng thưởng" có trong 2/5 thư rác và 1/30 thư thường. P(có từ) = 1/10 + 1/40 = 1/8, nên P(rác | có từ) = (1/10)/(1/8) = 4/5.

> Lỗi thường gặp: bỏ qua tỉ lệ nền. Xét nghiệm "chỉ sai 1/50 ở người khỏe" không có nghĩa người dương tính mắc bệnh với xác suất 49/50: với tỉ lệ bệnh 1/1000 con số đúng là 50/1049, chưa đến 5%.
