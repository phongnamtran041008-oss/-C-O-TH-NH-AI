# Thực chiến trong game — huấn luyện mô hình và làm dự án AI như thế nào

> Bản thiết kế, **chưa nối vào game**. Viết ngày 2026-11-19 trong phiên "tối ưu nguồn tài liệu". Dựa trên
> các nút `thuc_chien` và `du_an` của Đạo Thụ (`tree.json` của phiên giáo trình) và bộ chạy bài tập lập
> trình M6 đã có (`client/engine/coderun.py`, `server/app/learning/math_problems.py`). Không sửa file nào
> của hai phiên kia.

## 1. Bài toán

Đạo Thụ có 8 nút thực chiến, 8 thiên kiếp dự án (mỗi cảnh giới một cái) và hơn 30 nút học máy, học sâu, hệ
thống, nghiên cứu. Không nút nào trong số đó hỏi được bằng trắc nghiệm: phải **làm**. Câu hỏi là làm ở đâu,
và game biết người chơi làm xong bằng cách nào.

Ba nguyên tắc:

1. **Huấn luyện thật, không giả lập.** Mô hình do người chơi viết, chạy trên dữ liệu thật, sai thật.
2. **Mỗi việc kết thúc bằng một con số mà game tự đo được** trên dữ liệu người chơi chưa thấy nhãn — hoặc,
   khi không đo được, bằng một thang điểm rõ ràng (mục 5).
3. **Nhỏ trước.** Thứ gì chạy được trong vài giây trên máy xách tay thì ở trong game. Chỉ khi thật sự cần
   GPU mới ra ngoài.

Từ đó có ba bậc.

| Bậc | Tên trong game | Chạy ở đâu | Game kiểm bằng gì | Dùng cho |
|---|---|---|---|---|
| 1 | **Xạ Trường** | Ngay trên máy người chơi, do game khởi chạy | Dự đoán của mô hình trên bia ẩn | Luyện Khí, đầu Trúc Cơ |
| 2 | **Ngoại Giới Bí Cảnh** | Sổ tay Colab/Kaggle hoặc máy riêng | File nộp: dự đoán trên bia ẩn + nhật ký huấn luyện | Trúc Cơ tới Hóa Thần |
| 3 | **Công Trình** | Ngoài đời thật: kho mã, bài viết, sản phẩm | Bằng chứng + thang điểm | Luyện Hư trở lên |

## 2. Bậc 1 — Xạ Trường: huấn luyện ngay trong game

Thiên Địa Đồ đã đặt Thực Chiến AI ở **Linh Xạ Nguyên**, binh khí là cung: "nhắm vào đích và chỉnh dần cho
trúng: đó chính là huấn luyện một mô hình". Xạ Trường dùng đúng hình ảnh ấy:

| Trong học máy | Ở Xạ Trường |
|---|---|
| Một mẫu dữ liệu kiểm tra | Một tấm bia |
| Dự đoán của mô hình | Một mũi tên |
| Độ chính xác | Tỉ lệ trúng bia |
| Hàm mất mát | Khoảng cách trung bình từ tên tới hồng tâm |
| Một vòng huấn luyện (epoch) | Một loạt bắn tập |
| Tốc độ học | Chỉnh tay nhiều hay ít sau mỗi loạt |
| Quá khớp | Bắn trăm phát trăm trúng ở bia tập, ra bia lạ thì trượt |
| Tập kiểm định | Dãy bia thử, bắn trước khi vào bia thật |

### 2.1 Một bài ở Xạ Trường chạy thế nào

Dùng lại gần như nguyên bộ chạy M6:

1. Người chơi mở bài (ví dụ "k láng giềng gần nhất"), đọc đề, viết `bai_lam.py` trong trình soạn của game.
2. **Bắn tập** (Chạy thử): chương trình chạy trên dữ liệu mẫu có sẵn nhãn. Game vẽ kết quả: bia nào trúng,
   bia nào trượt, và **đường mất mát** nếu chương trình có in.
3. **Bắn thật** (Nộp bài): server giao dữ liệu huấn luyện và các bia ẩn (chỉ có đầu vào). Chương trình
   huấn luyện, rồi in ra một dự đoán cho mỗi bia. Máy khách gửi các dự đoán lên; **nhãn thật không rời
   server**, server đếm số bia trúng.
4. Phẩm chất theo ngưỡng của bài: dưới ngưỡng = chưa đạt; đạt = hạ phẩm; cao hơn = trung, thượng phẩm.
   Điểm thưởng theo cách M6 đã làm: chỉ trả cho phần **tiến bộ** so với lần tốt nhất trước đó.

Thứ phải thêm vào M6 rất ít:

- **Phép chấm mới** bên cạnh `exact` và `float`: `do_chinh_xac` (so từng dòng nhãn, đạt khi tỉ lệ đúng ≥
  ngưỡng), `sai_so` (RMSE ≤ ngưỡng), `log_loss` (cho bài in xác suất). Một hàm thuần trong
  `math_problems.py`, mỗi phép một ngưỡng cho từng phẩm.
- **Đường mất mát:** chương trình in ra `stderr` các dòng `#loss <bước> <giá trị>` (và `#val <bước> <giá
  trị>` nếu có tập kiểm định). `coderun` đã giữ `stderr`; màn kết quả đọc các dòng ấy và vẽ. Không in cũng
  không sao — nhưng đề của các bài từ `ud_hoi_quy_1_bien` trở đi yêu cầu in, vì nhìn đường mất mát là kỹ
  năng phải luyện.
- **Giới hạn thời gian dài hơn** cho bài huấn luyện (`time_limit_ms` đã là trường của từng bài): 10-60 giây.
- **Nhiều hạt giống:** bài có yếu tố ngẫu nhiên được chấm trên 3-5 bộ bia sinh từ hạt giống khác nhau (mỗi
  bộ là một "test" của M6). Mô hình chỉ gặp may một lần thì không qua. Đây cũng là nội dung của nút
  `ud_ab_test`.

### 2.2 Dữ liệu

Nhỏ, đi kèm game hoặc sinh ngay từ hạt giống, giấy phép rõ. Danh sách cụ thể cho từng nút — bộ dữ liệu, kích
thước, giấy phép, mốc điểm đã kiểm chứng — nằm ở trường `project` trong
`server/data/math/sources/{ud,ml,dl,lt}.json` và được tóm lại ở mục 6.

- Dữ liệu **sinh ra** (điểm 2 chiều, đường thẳng có nhiễu, hai cụm, hai vầng trăng): không cần giấy phép,
  bia ẩn mỗi lần một khác, hợp nhất cho các nút đầu.
- Dữ liệu **thật nhỏ**: chữ số 8×8, hoa Iris, tin nhắn rác... dưới 1 MB mỗi bộ.
- Dữ liệu vào bài qua `stdin` như M6. Bộ nào lớn hơn vài trăm KB thì nằm trong một file cạnh bài làm.

### 2.3 Thư viện được dùng

| Nút | Được dùng | Vì sao |
|---|---|---|
| Luyện Khí tầng 1-3 (`ud_knn`, các nút `lt_*` đầu) | Python thuần | Tự viết khoảng cách, tích vô hướng một lần cho biết. |
| Từ `lt_numpy` (Luyện Khí tầng 4) | NumPy | Đúng như cây đã định. |
| Từ Trúc Cơ | pandas, scikit-learn | Công cụ nghề. |
| Từ Nguyên Anh | PyTorch | Chủ yếu ở bậc 2. |

Game không kèm các thư viện này (bản đóng gói vốn đã phải tìm Python của người chơi để chạy bài). Khi một
bài cần NumPy, game thử `import numpy` bằng trình thông dịch chạy bài; thiếu thì hiện đúng một dòng lệnh cài
và nút "thử lại". Đây cũng là bài học thật đầu tiên về môi trường.

### 2.4 Luyện tay không cần code: bàn chỉnh cung

Trước mỗi nút thực chiến có một màn tương tác ngắn, không viết code, để có trực giác trước khi viết:

- **Kéo đường thẳng cho khớp:** người chơi kéo độ dốc và điểm cắt, game hiện tổng bình phương sai số đổi
  theo. Rồi bấm "để máy tự chỉnh" và nhìn hạ gradient làm đúng việc mình vừa làm bằng tay.
- **Tốc độ học:** ba cần gạt (tốc độ học, số loạt bắn, cỡ lô). Quá nhỏ: tên nhích từng li. Quá lớn: tên
  văng qua văng lại rồi bay mất (mất mát thành `nan` — "tẩu hoả nhập ma").
- **Quá khớp:** tăng bậc đa thức, đường mất mát trên bia tập cứ xuống còn trên bia thử thì quay đầu đi lên.
  Người chơi phải bấm dừng đúng lúc (dừng sớm).

Các màn này tính toán ngay trong game bằng Python thuần (vài trăm điểm, vài tham số: đủ nhanh cho mỗi khung
hình), không cần bộ chạy bài. Chúng không cho tu vi; chúng mở bài code tương ứng.

## 3. Bậc 2 — Ngoại Giới Bí Cảnh: việc cần GPU hoặc cần nhiều giờ

Mạng tích chập, mô hình ngôn ngữ nhỏ, tinh chỉnh mô hình có sẵn: không chạy được trong vài giây, và không
nên bắt game làm việc của một sổ tay. Cách làm giống một cuộc thi dữ liệu:

1. Ở cửa bí cảnh, game phát **quyển trục**: một sổ tay mẫu (`.ipynb`) và gói dữ liệu, gồm dữ liệu huấn
   luyện có nhãn và **bia ẩn không nhãn**. Người chơi mở bằng Colab, Kaggle hay máy mình.
2. Sổ tay kết thúc bằng một ô đã viết sẵn, ghi ra `nop_bai.json`:

   ```json
   {
     "project": "du_an_nguyen_anh",
     "format": 1,
     "predictions": [3, 8, 8, 0, 6],
     "log": {"train": [[0, 2.31], [100, 1.72]], "val": [[0, 2.30], [100, 1.80]]},
     "config": {"lr": 0.001, "epochs": 12, "params": 61706, "seed": 0},
     "minutes": 14
   }
   ```

3. Người chơi quay lại game, chọn file ấy. Server chấm `predictions` với nhãn ẩn và trả về điểm.
4. Bia ẩn chia đôi như Kaggle: **điểm lộ** (nửa bia, thấy ngay sau mỗi lần nộp) và **điểm ẩn** (nửa còn
   lại, quyết định thiên kiếp, chỉ hiện khi người chơi bấm "chốt"). Mỗi ngày nộp tối đa 5 lần. Ai chỉnh mô
   hình theo điểm lộ quá tay sẽ thấy điểm ẩn tụt — bài học về tập kiểm tra, học bằng chính điểm của mình.
5. `log` được vẽ thành đường mất mát trong game, và là đầu vào cho các câu hỏi sau thiên kiếp: "nhìn đường
   này, mô hình của bạn đang quá khớp hay chưa học đủ?".

Với **mô hình sinh** (nút `ht_gpt_nho`): bia ẩn là một đoạn văn kiểm định; sổ tay ghi xác suất mô hình gán
cho ký tự/token đúng kế tiếp tại từng vị trí; server tính perplexity. Với **ứng dụng mô hình ngôn ngữ** và
**bộ đánh giá** (`ht_ung_dung_llm`, `ht_danh_gia_llm`): file nộp là bảng kết quả của bộ đánh giá do chính
người chơi viết (số ca, số đạt, từng ca kèm đầu vào và đầu ra), chấm theo thang điểm ở bậc 3.

Giới hạn thật thà của bậc này: nhãn của các bộ dữ liệu công khai thì ai cũng tìm được, và file nộp sửa tay
được. Game không cố chống — như ở M6, đó là tự lừa mình. Thứ game làm là khiến đường thẳng thắn dễ đi nhất:
sổ tay mẫu chạy được ngay, mốc điểm vừa sức, và nhật ký huấn luyện được đọc lại.

## 4. Bậc 3 — Công Trình: việc không có đáp số

Từ Luyện Hư trở lên, các nút là: vận hành một hệ thống có người dùng, tái lập một bài báo, một đóng góp
công khai, dẫn dắt một đội, công trình của riêng mình. Không máy chấm nào đo được. Ở đây game là **người
giữ sổ**, không phải giám khảo:

- Mỗi nút có một **bản khai**: đường dẫn tới bằng chứng (kho mã, bài viết, bản chạy thử, yêu cầu gộp đã
  được nhận) và một báo cáo ngắn theo mẫu: câu hỏi — dữ liệu — cách làm — kết quả kèm khoảng tin cậy — đối
  chứng — hạn chế — làm lại thì đổi gì.
- Mỗi nút có **thang điểm** viết sẵn, cùng định dạng với đề ở Luận Đạo Đài (`rubric`, tổng 10), ví dụ cho
  "tái lập một công trình": có số của bài gốc và số của mình đặt cạnh nhau; chạy lại được từ một lệnh; nêu
  rõ chỗ lệch và giả thuyết vì sao; có ít nhất một thí nghiệm bài gốc không có.
- Chấm bằng **hai cách**: tự chấm theo thang, hoặc đồng đạo thẩm định. (Chấm bằng giám khảo AI với khoá
  của người chơi đã bị bỏ ngày 2026-11-20: game không gọi mô hình nào.) Thiên kiếp ở các cảnh giới này
  qua khi người chơi chốt bản khai và thang điểm đạt ngưỡng — game tin người chơi, vì tới đây phần thưởng
  thật nằm ngoài game.

## 5. Vì sao chia như vậy

- Bậc 1 giữ người chơi **trong game** suốt Luyện Khí, lúc động lực còn mong manh nhất; vòng "viết — bắn —
  xem bia" mất vài giây.
- Bậc 2 dạy đúng quy trình người làm nghề đang dùng (sổ tay, GPU miễn phí, tập kiểm tra ẩn, nộp dự đoán),
  và game không phải gánh PyTorch.
- Bậc 3 thừa nhận rằng "dẫn đầu" không chấm tự động được, và dùng lại hạ tầng thang điểm thay vì bày thêm
  một hệ thống.
- Cả ba dùng lại thứ đã có: bộ chạy M6, định dạng thang điểm của đề tự luận (`rubric`), vùng đất Linh Xạ Nguyên.

## 6. Từng nút làm ở bậc nào

Dữ liệu, giấy phép và mốc điểm lấy từ trường `project` của `server/data/math/sources/*.json` (tra cứu
2026-11-19). "Chưa kiểm chứng" nghĩa là chưa có nguồn công bố con số ấy: phải đo bằng lời giải mẫu của
chính game trước khi đặt ngưỡng.

### Bậc 1 — Xạ Trường

| Nút | Tầng | Dữ liệu (giấy phép) | Chấm bằng | Mốc đề xuất |
|---|---|---|---|---|
| `ud_knn` k láng giềng | Luyện Khí 3 | Chữ số 8×8 của UCI, 0,58 MB (CC BY 4.0); điểm 2 chiều tự sinh | độ chính xác | ≥ 95% (ví dụ của scikit-learn đạt 96,1%) |
| `ud_hoi_quy_1_bien` khớp đường thẳng | Luyện Khí 5 | Tự sinh y = ax + b + nhiễu; Palmer Penguins (CC0) | sai số | hệ số lệch vài phần trăm so với a, b thật; chưa kiểm chứng trên Penguins |
| `ud_naive_bayes` lọc thư rác | Luyện Khí 5 | SMS Spam Collection của UCI, 0,47 MB (CC BY 4.0) | độ chính xác + precision/recall | ≥ 96% (các báo cáo công khai: 96,6% tới 99%); lớp lệch nên phải báo cả recall |
| `ud_binh_phuong_toi_thieu` | Luyện Khí 7 | Tự sinh nhiều biến | sai số | trùng nghiệm của thư viện tới sai số làm tròn, và trùng nghiệm hạ gradient |
| `ud_mang_no_ron` mạng hai lớp | Luyện Khí 8 | XOR (4 điểm); chữ số 8×8 | độ chính xác + đường mất mát | XOR đúng cả 4; chữ số ≥ 93% (chưa kiểm chứng) |
| `ud_logistic` | Luyện Khí 9 | SMS Spam; Breast Cancer Wisconsin (**giấy phép chưa rõ, không kèm game**) | log-loss + độ chính xác | ≥ 95% (chưa kiểm chứng) |
| `ud_pca` | Luyện Khí 9 | Chữ số 8×8 | sai số tái tạo | vectơ riêng trùng thư viện |
| `ud_ab_test` | Luyện Khí 9 | Dự đoán của hai mô hình của chính người chơi | khoảng tin cậy | khoảng tin cậy 95% đúng, kết luận đúng khi khoảng chứa 0 |
| `du_an_luyen_khi` thiên kiếp chữ số | Luyện Khí 9 | Chữ số 8×8 (bắt buộc); MNIST là thử thách thêm, người chơi tự tải (**giấy phép chưa rõ**) | độ chính xác trên 5 hạt giống + báo cáo | ≥ 95% trên 8×8 |
| `na_autograd` tự viết autograd | Nguyên Anh 1 | Hai vầng trăng tự sinh | so gradient với sai phân | gradient lệch dưới 1e-6; chưa kiểm chứng mốc phân loại |

Các nút `lt_*` (lập trình) dùng bộ chạy M6 như hiện nay, không cần dữ liệu ngoài.

### Bậc 2 — Ngoại Giới Bí Cảnh

| Nút | Tầng | Dữ liệu (giấy phép) | File nộp chứa | Mốc đề xuất |
|---|---|---|---|---|
| `du_an_truc_co` dữ liệu bảng | Trúc Cơ 3 | Adult / Census Income của UCI, 5,7 MB (CC BY 4.0) | dự đoán + báo cáo kiểm định chéo | vượt rõ mô hình nền (đoán lớp đa số); chưa kiểm chứng con số |
| `du_an_ket_dan` cuộc thi dữ liệu | Kết Đan 3 | Một cuộc thi nhập môn trên Kaggle (dữ liệu theo điều khoản cuộc thi, **không kèm game**) hoặc bia ẩn của game trên Adult | dự đoán | nửa trên bảng xếp hạng, hoặc điểm ẩn vượt mốc của lời giải mẫu |
| `du_an_nguyen_anh` mô hình ảnh | Nguyên Anh 3 | Fashion-MNIST, 35 MB (MIT) | dự đoán + nhật ký + một thí nghiệm đối chứng | khoảng 92% với mạng 2 lớp tích chập (số người dùng tự báo trong kho của Zalando) |
| `ht_gpt_nho` mô hình ngôn ngữ nhỏ | Hóa Thần 1 | Tiny Shakespeare, 1 MB | xác suất của ký tự đúng kế tiếp trên đoạn kiểm định | mất mát kiểm định khoảng 1,88 chạy được trên CPU; 1,47 với GPU (README của nanoGPT) |
| `ht_tinh_chinh` tinh chỉnh | Hóa Thần 2 | Một bộ phân loại văn bản nhỏ | dự đoán trước và sau tinh chỉnh | cải thiện có đối chứng; chưa kiểm chứng con số |
| `hp_tai_lap` tái lập | Hợp Thể 1 | Tiny Shakespeare; Fashion-MNIST | số của mình đặt cạnh số bài gốc | khớp số công bố tới chữ số thập phân thứ hai |

GPU miễn phí: Colab không bảo đảm có GPU và mỗi phiên tối đa 12 giờ (trang hỏi đáp chính thức). Hạn mức của
Kaggle (khoảng 30 giờ GPU mỗi tuần) mới thấy ở nguồn thứ cấp — chưa kiểm chứng; game chỉ dẫn tới trang chính
thức chứ không ghi con số.

### Bậc 3 — Công Trình

| Nút | Tầng | Bằng chứng | Thang điểm xoay quanh |
|---|---|---|---|
| `ht_ung_dung_llm`, `ht_danh_gia_llm` | Hóa Thần 2-3 | Bộ đánh giá tự viết (50-100 ca có đáp án) và bảng kết quả trước/sau | ca thử có đại diện không; số trước và sau mỗi thay đổi; phân tích ca hỏng |
| `du_an_hoa_than` sản phẩm LLM | Hóa Thần 3 | Đường dẫn sản phẩm + bộ đánh giá | có người dùng thật ngoài mình; bộ đánh giá cho thấy tốt lên qua vài vòng |
| `du_an_luyen_hu` vận hành hệ thống | Luyện Hư 3 | Kho mã + nhật ký vận hành một tuần | cảnh báo khi độ chính xác giảm; một bản ghi sự cố; chạy lại được |
| `du_an_hop_the` đóng góp công khai | Hợp Thể 3 | Bài viết hoặc yêu cầu gộp công khai | mã chạy lại được; có người ngoài phản hồi |
| `dt_*`, `du_an_dai_thua` | Đại Thừa | Công trình của riêng mình | chọn bài toán vì sao; ai dùng; trách nhiệm với hệ quả |

Hai bộ dữ liệu hay được nhắc nhưng **không nên kèm game**: CIFAR-10 (trang gốc không ghi giấy phép, chỉ yêu
cầu trích dẫn) và mọi dữ liệu cuộc thi Kaggle (theo điều khoản từng cuộc thi).

## 7. Rủi ro và giới hạn

| Rủi ro | Cách xử lý |
|---|---|
| **Bản web (M12, pygbag).** Trình duyệt không khởi chạy được tiến trình con, nên bộ chạy M6 và Xạ Trường không chạy như trên máy bàn. NumPy trên pygbag: chưa kiểm chứng. | Vấn đề này M6 đã có sẵn, không phải do Xạ Trường sinh ra. Hướng xử lý khi tới M12: chạy bài làm ngay trong tiến trình của game với `stdout` được bắt lại, chỉ cho các bài Python thuần; bài cần NumPy thì bản web chỉ sang bản máy bàn. |
| Máy yếu, bài huấn luyện chạy lâu | Mốc thời gian đặt theo lời giải mẫu chạy trên máy thường × 5; dữ liệu của bậc 1 luôn dưới vài nghìn mẫu. |
| Người chơi chưa cài NumPy / cài hỏng | Màn kiểm môi trường một dòng lệnh (mục 2.3). |
| Mốc điểm đặt sai (quá khó hoặc quá dễ) | Mỗi bài có lời giải mẫu trên server; `tools/check_all.py` chạy lời giải mẫu và kiểm nó đạt thượng phẩm, còn một lời giải "ngây thơ" (đoán lớp nhiều nhất) thì không đạt. |
| Gian lận file nộp | Không chống (mục 3). Điểm ẩn, giới hạn lượt nộp và nhật ký huấn luyện chỉ để việc học thật là đường dễ nhất. |
| Giấy phép dữ liệu | Chỉ kèm game các bộ có giấy phép cho phép phát hành lại; bộ nào chưa rõ thì game tải từ nguồn gốc lúc cần, không kèm. Ghi vào CREDITS.md khi nối. |

## 8. Thứ tự làm đề xuất

1. **Phép chấm theo độ chính xác / sai số + đường mất mát** trong bộ chạy M6 (nhỏ, thử được bằng pytest).
2. **Ba bài Xạ Trường đầu**: `ud_knn`, `ud_hoi_quy_1_bien`, `ud_naive_bayes`, kèm dữ liệu sinh từ hạt giống.
3. **Bàn chỉnh cung** cho hạ gradient và quá khớp (mục 2.4).
4. Các bài Xạ Trường còn lại của Luyện Khí và thiên kiếp nhận dạng chữ số.
5. Định dạng `nop_bai.json`, màn nộp file, điểm lộ/điểm ẩn; quyển trục đầu tiên (thiên kiếp Trúc Cơ).
6. Bản khai và thang điểm cho bậc 3 (cùng định dạng `rubric` với đề tự luận đã gác).

Bước 1-4 chỉ cần phiên viết câu hỏi ghi xong phần của mình (cùng đụng `math_problems.py` và
`check_all.py`). Bước 5-6 nên làm sau khi cây được nối vào game.

## 9. Những điều cần bạn quyết

1. Dùng hình ảnh **cung và bia** (theo Linh Xạ Nguyên trong Thiên Địa Đồ) cho việc huấn luyện — đồng ý chứ?
2. Từ Luyện Khí tầng 4 yêu cầu người chơi **tự cài NumPy** — chấp nhận được không, hay muốn bản đóng gói kèm
   sẵn một Python có NumPy (bản tải nặng thêm vài chục MB)?
3. Bậc 2 đưa người chơi **ra khỏi game** sang Colab/Kaggle. Đây là chủ ý; bạn có muốn thay bằng "chỉ chạy
   trên máy mình" cho các thiên kiếp từ Nguyên Anh không (sẽ loại người không có GPU)?
4. Thiên kiếp từ Luyện Hư trở lên **tin lời khai** của người chơi. Nếu muốn chặt hơn thì bắt buộc đồng đạo
   thẩm định (cần ít nhất một người bạn trong thế giới).
