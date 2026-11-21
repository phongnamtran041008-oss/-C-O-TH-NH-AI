# Thực chiến trong game — huấn luyện mô hình và làm dự án AI như thế nào

> Bản thiết kế viết ngày 2026-11-19 trong phiên "tối ưu nguồn tài liệu". Dựa trên các nút `thuc_chien` và
> `du_an` của Đạo Thụ (`tree.json` của phiên giáo trình) và bộ chạy bài tập lập trình M6 đã có
> (`client/engine/coderun.py`, `server/app/learning/math_problems.py`).
>
> **2026-11-20: bậc 1 (Xạ Trường) đã nối vào game cho Luyện Khí**, theo bước 1-4 của mục 8, với một thay đổi
> lớn: **chỉ Python thuần**, không NumPy (game không bắt người chơi cài gì). Cái gì đã làm, làm thế nào, mốc
> điểm đo ra sao và giới hạn chống gian lận: mục 10. Bậc 2 và 3 vẫn là thiết kế.

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
| Từ `lt_numpy` (Luyện Khí tầng 4) | Python thuần, theo cách nghĩ của NumPy | Game không cài NumPy: năm bài của `lt_numpy` dạy hình dạng, phát sóng, tổng theo trục, `X @ w + b`, `X.T @ X` trên danh sách (rà soát giáo trình, 2026-11-20). |
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

## 10. Xạ Trường đã làm (2026-11-20)

Bậc 1 cho mọi nút Thực Chiến của Luyện Khí và thiên kiếp `du_an_luyen_khi`: 26 bài (id `xt_*`), trong đó 9 bài
chấm theo phẩm. Chỉ Python thuần và thư viện chuẩn: không NumPy, không mô hình AI nào, không tải gì về.

### 10.1 Chấm theo phẩm

Một bài chấm theo phẩm (`server/data/math/problems/<môn>.json`) có thêm:

- `checker`: `do_chinh_xac` (tỉ lệ dự đoán đúng, càng cao càng tốt) hoặc `sai_so` (căn của sai số bình phương
  trung bình, càng thấp càng tốt). Phép `log_loss` của mục 2.1 chưa làm: chưa bài nào cần.
- `grades`: ba mốc hạ, trung, thượng phẩm.
- `data`: `{"gen", "seeds", "practice_seeds", "params"}`. Mỗi hạt giống trong `seeds` là một **bộ bia ẩn**, sinh bởi
  `server/app/learning/xa_truong_data.py`: dữ liệu huấn luyện có nhãn, rồi các điểm cần đoán không nhãn. Mỗi hạt
  giống trong `practice_seeds` là một **bộ bia tập**, đi kèm đề như một ví dụ (thấy cả nhãn) để Chạy thử có ý nghĩa.
  Bài chấm theo phẩm không có `tests` viết sẵn.
- `starter`: đoạn code mở đầu trong trình soạn (đọc dữ liệu, chỗ in `#loss`). Bài thường cũng dùng được.
- Lời giải ngây thơ `problems/<môn>/ngay_tho/<id>.py` (đoán lớp nhiều nhất, đoán trung bình, trả nguyên điểm đo...).

Chấm (`math_problems.judge_scored`): mỗi bộ bia một điểm; in sai số dự đoán so với số điểm thì bộ ấy 0 điểm
(độ chính xác) hoặc không có điểm (sai số); có dự đoán không phải số thì không có điểm. Điểm của bài là trung bình
các bộ; phẩm là số mốc điểm ấy vượt qua. Phẩm được ghi vào hàng `math_submissions` như M6 ghi số test đạt:
`passed` = phẩm (0-3), `total` = 3. Nhờ vậy luật cũ chạy nguyên: Tu Vi = XP của bậc × phẩm / 3, chỉ trả phần vượt
lần tốt nhất; bài "xong" (và nút Đạo Thụ tính là xong) khi đạt **thượng phẩm**. Verdict là AC ở thượng phẩm, còn lại
WA (hoặc RE/TLE/CE nếu chương trình hỏng giữa chừng).

Bài của một nút Thực Chiến hay của thiên kiếp chỉ mở khi **chính nút ấy** mở (hoặc xong), ngoài luật R10 (vi kỹ năng
của bài nằm trong nút đang mở): vi kỹ năng thuộc nút toán mở sớm hơn nhiều, nhưng Xạ Trường phải vào qua nút của nó
(`math_code.problem_open`). Thẻ nút mở danh sách bài của nút, kể cả khi bài thuộc nhiều môn (thiên kiếp có bài của
ba môn): `/math/problems?ids=...`.

### 10.2 Nhật ký huấn luyện

Chương trình in ra **stderr** các dòng `#loss <vòng> <giá trị>` (và `#val <vòng> <giá trị>`).
`client/engine/coderun.py` đọc chúng (`parse_log`, cả đường chạy trong trình duyệt), bỏ chúng khỏi phần lỗi hiện
cho người chơi, và màn bài tập vẽ đường mất mát của bộ có nhật ký dài nhất (thang log khi mất mát giảm hơn 20 lần;
`nan`/`inf` hiện chữ "tẩu hỏa nhập ma"). Nhật ký **không gửi lên server**. Màn kết quả của bài chấm theo phẩm
("Xem bia"): phẩm, điểm, mốc, điểm từng bộ với một tấm bia nhỏ tô màu theo phẩm của bộ ấy, đường mất mát.

### 10.3 Ai chấm, và giới hạn chống gian lận

Server vẫn là người chấm: nhãn của bia ẩn không rời server, chương trình của người chơi chỉ nhận dữ liệu huấn luyện
và tọa độ các bia, gửi về dự đoán, server tính điểm. Nhưng nói thẳng, cách này **không chống được gian lận**:

1. Mã nguồn của game mở: ai đọc `xa_truong_data.py` và hạt giống trong JSON thì tự sinh lại được nhãn của bia ẩn.
2. Máy khách sửa được thì gửi dự đoán nào cũng được, như M6 gửi verdict nào cũng được.
3. Bia ẩn cố định theo hạt giống và mỗi lần nộp thấy điểm từng bộ, nên nộp đi nộp lại có thể dò dần nhãn.
4. Game không kiểm được *cách* làm: bài hạ gradient giải bằng công thức cũng qua, nhật ký `#loss` in bừa cũng được vẽ.

Như mục 3 đã nói: đó là tự lừa mình. Game làm cho đường thẳng thắn dễ đi nhất (code mở đầu, bia tập, đường mất mát),
không đặt hàng rào.

### 10.4 Bài của từng nút

| Nút | Bài (bài cuối chấm theo phẩm) | Môn / vi kỹ năng |
|---|---|---|
| `ud_knn` | đo khoảng cách, bỏ phiếu, lãnh địa linh thú | Đại Số `dstt_t3_vecto_rn` |
| `ud_naive_bayes` | đếm từ, công thức Bayes, bộ lọc thư rác | Xác Suất `xs_t4_bayes_ung_dung` |
| `ud_hoi_quy_1_bien` | mất mát và đạo hàm, vòng lặp hạ gradient, khớp đường thẳng | Giải Tích `gt_t6_cuc_tri` |
| `ud_binh_phuong_toi_thieu` | lập phương trình chuẩn, giải nó, sản lượng linh điền | Đại Số `dstt_t9_phep_chieu` |
| `ud_mang_no_ron` | lan truyền xuôi, lan truyền ngược, trận đồ hình tròn | Giải Tích `gt_t9_gradient_lan_truyen` |
| `ud_logistic` | mất mát log và gradient, linh thảo thật giả | Xác Suất `xs_t7_hop_ly_cuc_dai` |
| `ud_pca` | hiệp phương sai, lặp lũy thừa, lọc nhiễu bằng PCA | Đại Số `dstt_t9_pca_svd` |
| `ud_ab_test` | khoảng tin cậy một tỉ lệ, hiệu hai tỉ lệ, trăm cuộc A/B | Xác Suất `xs_t8_tin_cay_ty_le`, `xs_t9_so_sanh_ty_le` |
| `du_an_luyen_khi` | ảnh là vectơ, báo cáo (độ chính xác, khoảng tin cậy, lỗi hay gặp), đọc chữ số | Đại Số, Xác Suất, Giải Tích |

Chữ số của thiên kiếp là **chữ số tổng hợp** (nét vẽ bằng code, có nhiều kiểu viết cho 0, 1, 3, 4, 7, 9, rồi nghiêng,
xoay, co giãn, dịch, đổi độ đậm, rắc nhiễu), 8 × 8 điểm ảnh 0-16; đề nói rõ điều này. Thư rác là mẫu câu tiếng Việt không
dấu tự viết (dữ liệu đi qua stdin phải là ASCII).

### 10.5 Mốc điểm và thời gian, đo bằng chính lời giải mẫu

`python tools/build_problem_tests.py --measure --seeds 20` (máy phát triển, 2026-11-20). "Ẩn" là trung bình trên các
bộ bia ẩn thật của bài (4 bộ; thiên kiếp 5 bộ); "1-20" là trung bình, thấp nhất và cao nhất của từng bộ trên hạt giống
1 tới 20. Mốc thượng phẩm đặt dưới điểm của lời giải mẫu một khoảng rộng hơn độ dao động giữa các hạt giống; mốc hạ
phẩm đặt trên điểm cao nhất mà lời giải ngây thơ đạt được ở bất kỳ hạt giống nào.

| Bài | Mốc hạ / trung / thượng | Mẫu: ẩn; 1-20 (thấp-cao) | Ngây thơ: ẩn; 1-20 (thấp-cao) | Mẫu chậm nhất | Giới hạn |
|---|---|---|---|---|---|
| lãnh địa linh thú (độ chính xác) | 65% / 75% / 82% | 87,8%; 87,1% (82-92) | 43,5%; 43,7% (30-70) | 84 ms | 2 s |
| bộ lọc thư rác (độ chính xác) | 80% / 88% / 93% | 97,2%; 96,9% (95,3-98,7) | 66,7%; 64,5% (56-71,3) | 71 ms | 2 s |
| khớp đường thẳng (sai số) | 2,0 / 1,5 / 1,2 | 0,915; 1,018 (0,84-1,18) | 4,82; 5,81 (3,35-8,10) | 78 ms | 2 s |
| sản lượng linh điền (sai số) | 1,5 / 0,9 / 0,7 | 0,494; 0,514 (0,43-0,63) | 3,51; 4,21 (2,55-6,62) | 69 ms | 2 s |
| trận đồ hình tròn (độ chính xác) | 70% / 80% / 86% | 91,5%; 91,3% (87-96) | 51,5%; 52,0% (33-62) | 509 ms | 2,5 s |
| linh thảo thật giả (độ chính xác) | 72% / 80% / 86% | 89,5%; 92,1% (86-95) | 57,8%; 60,2% (50-68) | 224 ms | 2 s |
| lọc nhiễu bằng PCA (sai số) | 0,42 / 0,36 / 0,31 | 0,273; 0,261 (0,24-0,29) | 0,501; 0,495 (0,46-0,53) | 81 ms | 2 s |
| trăm cuộc A/B (độ chính xác) | 75% / 85% / 90% | 97,5%; 96,9% (94-99) | 49,8%; 50,9% (39-60) | 64 ms | 2 s |
| đọc chữ số (độ chính xác) | 86% / 88% / 90% | 93,2%; 92,5% (86-96,7) | 78,8%; 81,6% (76-88,7) | 520 ms | 3 s |

Lời giải mẫu: k láng giềng (k = 5; chữ số k = 3), Bayes ngây thơ làm trơn Laplace, hạ gradient trên x đã trừ trung bình,
phương trình chuẩn + khử Gauss, mạng 2-8-1 tanh/sigmoid với hạ gradient ngẫu nhiên, logistic trên đặc trưng chuẩn hóa,
PCA bằng lặp lũy thừa có xuống thang, kiểm định z hai tỉ lệ. Lời giải ngây thơ: lớp nhiều nhất (linh thú, thư rác,
linh thảo), trung bình y (đường thẳng, linh điền), hồi quy logistic không lớp ẩn (hình tròn), trả nguyên điểm đo
(PCA), bên nào cao hơn thì thắng (A/B), so với ảnh trung bình của từng chữ số (chữ số). Giới hạn thời gian là khoảng 5
lần thời gian của lời giải mẫu, không dưới 2 giây (mức mặc định của M6, vì riêng việc khởi động Python đã mất khoảng
50 ms); `tools/check_all.py` kiểm lời giải mẫu không dùng quá nửa giới hạn.

### 10.6 Chưa làm, và chỗ còn hở

- **Bàn chỉnh cung** (mục 2.4) chưa làm: nó là một màn tương tác riêng (cần gạt, vẽ đường theo khung hình), không gói
  gọn được trong `client/scenes/math_code.py` mà không làm màn bài tập rối thêm. Nên làm thành một màn riêng mở từ thẻ nút.
- Tên và chủ đề của hai nút trong `tree.json` từng nhắc NumPy ("Giải bằng NumPy", "Lan truyền ngược bằng NumPy"), đã sửa
  thành Python thuần theo cách nghĩ của NumPy (rà soát giáo trình, 2026-11-20); bài thì
  viết bằng Python thuần. Nút `lt_numpy` đã có năm bài trên danh sách (không cần NumPy).
- Bản web (M12): các bài chạy trong tiến trình của trang, có bộ theo dõi thời gian. Trên máy bàn, lời giải mẫu của bài
  chữ số chạy theo cách ấy mất khoảng 3,4 giây cho một bộ (giới hạn của bản web là 3 × 3 = 9 giây); trong trình duyệt
  thật chưa đo, có thể quá giờ. Trang đứng hình trong lúc chạy.
- Chưa có bài nào kiểm tập kiểm định (`#val`) hay dừng sớm; đường `#val` đã vẽ được.
