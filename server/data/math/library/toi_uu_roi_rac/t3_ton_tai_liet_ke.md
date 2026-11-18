---
id: tr_lib_t3
title_vi: Bài toán tồn tại và bài toán liệt kê
subject: toi_uu_roi_rac
floor: 3
summary_vi: Khi không cần đếm hết mà chỉ cần chỉ ra có hay không, và khi phải đi qua từng cấu hình một không sót cái nào: nguyên lý Dirichlet, bất biến, thứ tự từ điển, phương pháp sinh và quay lui.
skills: [tr_t3_dirichlet, tr_t3_bat_bien, tr_t3_tu_dien, tr_t3_sinh_ke_tiep, tr_t3_thu_hang, tr_t3_quay_lui]
---
## Nguyên lý Dirichlet

Nhốt N con chim vào k cái lồng, N > k, thì có một lồng chứa ít nhất hai con. Dạng tổng quát:

$$ N \text{ vat vao } k \text{ hop } \Rightarrow \text{ co hop chua it nhat } \left\lceil \frac{N}{k} \right\rceil \text{ vat} $$

Trần của N/k là số nguyên nhỏ nhất không nhỏ hơn N/k: trần của 9/4 là 3, trần của 8/4 là 2.

Muốn chắc chắn có m vật trong cùng một hộp, cần ít nhất:

$$ k(m-1) + 1 $$

vì k(m - 1) vật vẫn có thể chia mỗi hộp đúng m - 1 vật.

Phần khó là chọn hộp cho khéo. Ví dụ: trong 6 số nguyên bất kỳ luôn có hai số có hiệu chia hết cho 5.

1. Hộp là số dư khi chia cho 5: có 5 hộp 0, 1, 2, 3, 4.
2. 6 số vào 5 hộp nên có hai số cùng hộp.
3. Hai số cùng số dư có hiệu chia hết cho 5.

Một ví dụ khéo hơn: chọn 11 số trong {1, 2, ..., 20} thì có hai số mà số này chia hết cho số kia. Mỗi số viết được thành 2^a . m với m lẻ; 10 số lẻ từ 1 đến 19 là 10 hộp; hai số cùng hộp thì số nhỏ chia hết số lớn.

> Lỗi thường gặp: kết luận về từng hộp cụ thể. Nguyên lý chỉ nói có một hộp đầy, không nói hộp nào. Lỗi thứ hai là đánh giá sai trong một hộp, như cho rằng hai điểm trong hình vuông cạnh 1 cách nhau không quá 1, trong khi đường chéo dài căn bậc hai của 2.

## Chẵn lẻ và bất biến

Khi một trò chơi hay quá trình cho phép biến đổi theo luật, muốn chứng minh một trạng thái không bao giờ đạt được, hãy tìm một bất biến: một đại lượng không đổi qua mọi bước (hoặc không đổi tính chẵn lẻ, không đổi số dư).

Cách làm luôn gồm ba bước:

1. Chọn đại lượng: tổng, tính chẵn lẻ của tổng, số ô mỗi màu, hiệu hai tổng xen kẽ.
2. Chứng minh mỗi bước của luật chơi không làm nó đổi.
3. So giá trị lúc đầu với giá trị mà trạng thái đích phải có. Khác nhau thì không đạt được.

Ví dụ: trên bảng có 1, 2, ..., 10, mỗi lượt xóa a, b và viết |a - b|. Tổng mới bằng tổng cũ trừ 2 . min(a, b), nên tính chẵn lẻ của tổng không đổi. Tổng lúc đầu 55 là số lẻ, nên số cuối cùng chắc chắn là số lẻ.

Ví dụ kinh điển về tô màu: bàn cờ 8 x 8 bị cắt hai ô góc đối diện. Hai ô đó cùng màu, nên còn 32 ô màu này và 30 ô màu kia; mỗi domino phủ một ô mỗi màu, nên không thể lát kín.

> Lỗi thường gặp: kiểm tra bất biến không đủ mọi trường hợp của một bước. Lật hai cốc gồm ba khả năng: hai cốc úp, hai cốc ngửa, một úp một ngửa; khả năng cuối không làm đổi số cốc úp, chứ không phải làm giảm 1.

## Thứ tự từ điển

Thứ tự từ điển so sánh hai dãy cùng độ dài như cách xếp chữ trong từ điển: đi từ trái sang phải, dừng ở vị trí khác nhau đầu tiên; dãy có phần tử nhỏ hơn ở vị trí đó đứng trước.

$$ (a_1, \ldots, a_n) < (b_1, \ldots, b_n) \Leftrightarrow a_i < b_i \text{ tai vi tri khac nhau dau tien } i $$

Ví dụ: (2, 3, 4, 1) đứng trước (2, 4, 1, 3) vì ở vị trí thứ hai 3 nhỏ hơn 4; những gì đứng sau vị trí đó không còn ý nghĩa.

Ba loại cấu hình hay được xếp theo thứ tự từ điển:

- Xâu nhị phân độ dài n: thứ tự trùng với thứ tự của các số 0, 1, ..., 2^n - 1 viết trong hệ nhị phân.
- Hoán vị của {1, ..., n}: đầu tiên là (1, 2, ..., n), cuối cùng là (n, ..., 2, 1).
- Tập con k phần tử của {1, ..., n}, mỗi tập viết tăng dần: đầu tiên là {1, ..., k}, cuối cùng là {n - k + 1, ..., n}.

> Lỗi thường gặp: so sánh theo tổng hay theo phần tử lớn nhất thay vì theo vị trí khác nhau đầu tiên. 1012 đứng trước 1021 vì ở vị trí thứ ba 1 nhỏ hơn 2, dù hai xâu có cùng các chữ số.

## Phương pháp sinh

Phương pháp sinh liệt kê các cấu hình bằng cách đi từ cấu hình đầu tiên, mỗi lần dựng cấu hình liền sau theo thứ tự từ điển, đến khi gặp cấu hình cuối cùng. Cần hai thứ: biết cấu hình đầu, cuối, và một quy tắc tìm cấu hình liền sau.

Xâu nhị phân liền sau: từ phải sang trái tìm chữ số 0 đầu tiên, đổi nó thành 1 và đổi mọi chữ số bên phải nó thành 0. Ví dụ 10111 thành 11000. Xâu toàn số 1 là cấu hình cuối.

Tập con k phần tử liền sau: phần tử ở vị trí i lớn nhất được phép là n - k + i. Từ phải sang trái tìm phần tử đầu tiên chưa đạt giá trị lớn nhất, tăng nó lên 1, các phần tử sau nó lấy các số liền tiếp. Ví dụ với n = 6, k = 3: {1, 5, 6} thành {2, 3, 4}.

Hoán vị liền sau:

1. Từ phải sang trái tìm vị trí i đầu tiên có a_i < a_(i + 1). Đoạn sau i đang giảm dần.
2. Trong đoạn sau i tìm số nhỏ nhất còn lớn hơn a_i, đổi chỗ nó với a_i.
3. Đảo ngược đoạn sau i cho thành tăng dần.

Ví dụ (1, 3, 5, 4, 2): vị trí i là chỗ của số 3, đổi 3 với 4 được (1, 4, 5, 3, 2), đảo đoạn sau được (1, 4, 2, 3, 5).

> Lỗi thường gặp: quên bước đảo ngược ở hoán vị. Sau khi đổi chỗ, đoạn sau vẫn giảm dần, tức là lớn nhất có thể; giữ nguyên nó là nhảy qua rất nhiều hoán vị ở giữa.

## Thứ hạng của cấu hình

Thứ hạng của một cấu hình là vị trí của nó trong danh sách xếp theo thứ tự từ điển, đánh số từ 1. Không cần liệt kê hết: đếm số cấu hình đứng trước rồi cộng 1.

Với xâu nhị phân, xâu ứng với số m (đọc trong hệ nhị phân) đứng thứ m + 1. Ví dụ 01101 = 13 đứng thứ 14.

Với hoán vị, đi từ trái sang phải. Ở vị trí i, gọi c_i là số các số nhỏ hơn a_i chưa dùng ở các vị trí trước; đặt một số như vậy vào vị trí i thì mọi cách xếp (n - i)! phần còn lại đều đứng trước.

$$ \text{hang} = 1 + \sum_{i=1}^{n} c_i \, (n-i)! $$

Ví dụ (2, 3, 1, 4): c_1 = 1 cho 1 . 3! = 6; c_2 = 1 (chỉ có số 1) cho 1 . 2! = 2; c_3 = 0. Có 8 hoán vị đứng trước, nên nó đứng thứ 9.

Với tập con, làm tương tự: giữ các phần tử đầu, đặt ở một vị trí một số nhỏ hơn rồi đếm bằng tổ hợp số cách chọn các phần tử còn lại lớn hơn nó.

> Lỗi thường gặp: lệch một vị trí. Số cấu hình đứng trước là m thì cấu hình đứng thứ m + 1, vì cấu hình đầu tiên đứng thứ 1 chứ không phải thứ 0.

## Thuật toán quay lui

Quay lui xây cấu hình từng thành phần một. Ở bước i, thử lần lượt mọi giá trị hợp lệ cho x_i; với mỗi giá trị, hoặc in ra khi cấu hình đã đủ, hoặc đi tiếp sang bước i + 1. Thử hết thì trở về bước i - 1: đó là quay lui.

1. Try(i): với mỗi giá trị v còn hợp lệ cho x_i, gán x_i = v.
2. Nếu i là thành phần cuối thì in ra cấu hình.
3. Ngược lại gọi Try(i + 1).
4. Thử hết các giá trị thì Try(i) kết thúc và trả quyền về Try(i - 1).

Sức mạnh của quay lui là cắt nhánh: nếu cấu hình bộ phận x_1, ..., x_i đã vi phạm ràng buộc mà không thành phần nào thêm vào sửa được, thì bỏ qua toàn bộ nhánh mở rộng từ nó.

Ví dụ: liệt kê các tập con của {1, 2, 3, 4, 5} có tổng 6. Chọn các phần tử tăng dần, dừng nhánh khi tổng vượt 6. Bắt đầu bằng 1 được {1, 5} và {1, 2, 3}; bắt đầu bằng 2 được {2, 4}; bắt đầu bằng 3, 4, 5 không được gì. Có 3 tập.

Bài 4 quân hậu trên bàn 4 x 4: đặt mỗi hàng một quân, quay lui khi không còn cột an toàn; tìm được đúng 2 cách đặt.

> Lỗi thường gặp: để một giá trị được dùng lại khi bài không cho phép, như ghép {3, 3} thành tập có tổng 6, hay cho x_2 trùng x_1 khi liệt kê hoán vị. Mỗi bước phải chỉ thử những giá trị chưa dùng.
