# Rà soát giáo trình (Đạo Thụ), 2026-11-20

Báo cáo cho chủ dự án. Số liệu đầy đủ từng nút, từng vi kỹ năng, từng bậc nằm ở
[`GIAO_TRINH_RA_SOAT_SO_LIEU.md`](GIAO_TRINH_RA_SOAT_SO_LIEU.md); tệp đó do `tools/audit_curriculum.py` sinh ra
(chạy lại bất cứ lúc nào: `python tools/audit_curriculum.py`, không cần mạng). Cây giáo trình đọc được ở
[`GIAO_TRINH_CAY.md`](GIAO_TRINH_CAY.md).

Cách đọc: một **ô** là một vi kỹ năng ở một bậc mà tầng của nó có thể hỏi. **Sức chứa** của ô là số câu khác nhau
người học gặp được ở đó (câu viết tay tính 1, bộ sinh câu tính số câu khác nhau của 40 hạt giống). Ô **mỏng** là ô
có sức chứa dưới 10: người học gặp lại đúng câu cũ chỉ sau vài câu trả lời.

## 1. Con số trước và sau

| | Trước | Sau |
|---|---|---|
| Ô mỏng trên đường chính (296 ô) | 72 | 31 |
| Ô không có câu nào | 0 | 0 |
| Vi kỹ năng của nút chính không có câu nào | 0 | 0 |
| Nút chính Luyện Khí không có câu hỏi lẫn bài tập (`lt_numpy`) | 1 | 0 |
| Nút Luyện Khí có cờ `content` sai (ghi "đang viết" mà đã đủ câu) | 38 | 0 |
| Bộ sinh câu | 351 | 392 |
| Bài tập lập trình | 71 | 76 |
| Vấn đề tiên quyết (vòng, tầng ngược, nút chính cần nút phụ) | 0 | 0 |
| Câu hỏi chứng minh trên đường chính | 18 | 18 (xem mục 5) |
| Câu không bao giờ được hỏi (vi kỹ năng trong danh sách cắt) | 109 câu + 17 bộ sinh | như cũ |

Cây vốn khá sạch: không vòng, không nút nào cần nút ở tầng sau, mọi vi kỹ năng nằm đúng một chỗ, mọi nút chính
Luyện Khí có nguồn đọc, mọi vi kỹ năng toán có tài liệu thư viện, mọi nút có quái, chiêu hoặc bài tập chạm tới.
Chỗ hỏng thật nằm ở độ dày của câu hỏi, không ở cấu trúc.

## 2. Đã sửa (nhỏ, có kiểm thử)

1. **Cờ `content` nói dối.** 38 nút Luyện Khí ghi `dang_viet` trong khi câu hỏi đã viết xong từ lâu. Cờ này quyết
   định nút nào được mở chiêu (`math_skills.py` chỉ nhận nút `co`) và chữ "đang biên soạn" hiện ra. Đã đổi hết sang `co`.
   Luật mới trong `math_tree.validate()`: nút có câu hỏi (vi kỹ năng không bị cắt có câu) hoặc có bài tập thì
   `content` phải là `co`, và nút `co` mà trống thì bị bắt. Hai chiều. Kiểm thử: `test_math_tree.py`.
2. **Một bài tập chỉ thuộc một nút.** Luật mới trong `validate()` (trước đây chỉ có kiểm thử cho các nút `lt_*`).
3. **`lt_numpy` có nội dung** (mục 4).
4. **Hai nút `ud_*` nhắc NumPy** ("Giải bằng NumPy", "Lan truyền ngược bằng NumPy") trong khi bài viết bằng Python
   thuần. Đã sửa chữ, và sửa `docs/THUC_CHIEN_TRONG_GAME.md` cho khớp.
5. **Ba cạnh ôn tập chéo nhánh** (`reinforces`, chỉ nhắc nút tổ tiên, không đổi thứ tự mở nút):
   `tr_thuat_toan` ôn `xs_dem_su_kien`, `tr_tim_kiem` ôn `ds_vecto_ma_tran`, `xs_tin_cay` ôn `gt_tich_phan_ung_dung`.
   Đó là ba nút có tổ tiên ở môn khác mà chưa bao giờ ôn nó. Phần còn lại của mục 6 là quyết định của anh.

Không phải lỗi dữ liệu: bước kiểm tiên quyết của công cụ rà soát báo một chỗ (`gt_gioi_han_nang_cao`) và đó là báo
nhầm của chính công cụ; đã sửa công cụ.

## 3. Đã thêm: 41 bộ sinh câu cho 41 ô mỏng nhất

Chọn những ô chỉ có hai ba câu viết tay và không có bộ sinh, ưu tiên bậc cao nhất của tầng (nơi cổng thăng tầng
hỏi người học, nên lặp câu đau nhất). Mỗi bộ sinh cho vô hạn biến thể, lời giải có các bước, đáp án được
`tools/math_verify_rasoat.py` tính lại bằng sympy theo đường khác (ma trận sympy, giải hệ, tích phân, đa thức sinh,
Floyd-Warshall, lũy thừa ma trận kề, ngăn xếp, đạo hàm log hợp lý). Không câu nào đã duyệt (`reviewed: false`).

| Môn | Bộ sinh | Bậc 1 | Bậc 2 | Bậc 3 | Bậc 4 | Bậc 5 |
|---|---|---|---|---|---|---|
| Đại Số Tuyến Tính | 11 | | 2 | 1 | 1 | 7 |
| Giải Tích | 4 | | | | | 4 |
| Xác Suất và Thống Kê | 19 | 3 | 2 | 3 | 1 | 10 |
| Thuật Toán và Tối Ưu | 7 | | | 1 | 4 | 2 |
| **Cộng** | **41** | 3 | 4 | 5 | 6 | 23 |

Câu viết tay thêm: 0 (bộ sinh tốt hơn cho mục đích này). Đa số ở bậc 5 của tầng 7-8 vì ở đó các bộ sinh cũ dừng ở
bậc 4, còn bậc 5 chỉ có hai câu Thiên kiếp hay sắp xếp viết tay. Các bộ sinh bậc 5 hỏi ngược lại với bộ bậc 4: tìm n
từ một khoảng tin cậy, tìm trọng số không chệch, ước lượng hợp lý cực đại từ số liệu, đổi cơ sở, hạng và nhân.
Vài bộ mang màu AI: lọc thư rác và bộ phát hiện gian lận bằng Bayes, tích vô hướng của vectơ đặc trưng, hàm mất mát
lồi qua ma trận Hesse, mô hình trả lời sai và xác suất toàn phần.

Còn 31 ô mỏng. Phần lớn là ô mà các câu viết tay là trắc nghiệm, ghép cặp hay tìm chỗ sai: không sinh tự động được,
cần người viết.

## 4. `lt_numpy`: năm bài bằng Python thuần

Trước: nút trống, "đang biên soạn", coi như đã xong nên các nút `ud_*` sau nó không bị chặn bởi gì. Giờ có năm bài
trên danh sách, mỗi bài nói rõ NumPy làm việc này thế nào trong một dòng:

| Bài | Ý tưởng | NumPy |
|---|---|---|
| `dstt_bt_np_hinh_dang_phat_song` | luật phát sóng: hai hình dạng cộng được không, kết quả cỡ gì | `A + B` |
| `dstt_bt_np_tong_theo_truc` | tổng theo trục 0 và 1 | `A.sum(axis=...)` |
| `dstt_bt_np_cong_phat_song` | cộng một vectơ độ lệch vào mọi hàng | `X + b` |
| `dstt_bt_np_cham_diem` | chấm điểm cả lô: một lớp mạng là nhân ma trận | `X @ w + b` |
| `dstt_bt_np_gram` | chuyển vị rồi nhân, nền của hồi quy và PCA | `X.T @ X` |

Nút nói thẳng trong chữ của nó rằng game chạy bằng Python thuần và không cài NumPy. Mỗi bài có mẫu, 10 đến 12 test
ẩn, lời giải mẫu, và ba chương trình sai (đổi trục, quên b, tính `X X^T`...) mà test ẩn phải từ chối (kiểm thử "test
có răng"). Hệ quả cần biết: nút này giờ **không còn trống**, nên người chơi phải giải năm bài mới mở được
`ud_binh_phuong_toi_thieu`, `ud_mang_no_ron`, `ud_logistic`, `ud_pca` (vẫn như thiết kế trong `tree.json`).

## 5. Quyết định của anh, xếp theo độ đáng bận tâm

1. **18 câu hỏi chứng minh trên đường chính** (`rules.no_proof_items` của `tree.json` nói không hỏi chứng minh):
   `dstt_t7_dltt_04`, `dstt_t7_kgc_06`, `dstt_t7_kgv_04`, `dstt_t7_kgv_05`, `dstt_t8_dlsc_06`, `dstt_t8_nva_06`,
   `dstt_t9_kge_05`, `dstt_t9_tr_05`, `gt_t6_dd_06`, `gt_t7_db_04`, `gt_t7_ng_04`, `gt_t7_nl_06`, `tr_t5_dd_05`,
   `tr_t7_cay_04`, `tr_t8_tl_04`, `xs_t7_dt_06`, `xs_t7_ud_05`, `xs_t8_sl_06`. Phần lớn là "sắp xếp các bước chứng
   minh" hoặc "tìm chỗ sai trong chứng minh". **Khuyến nghị:** gỡ chúng khỏi đường chính (đưa vào nút phụ hoặc viết
   lại thành câu tính toán); tôi không xóa vì mỗi cái gỡ đi có thể làm ô tụt dưới mức tối thiểu hai câu.
2. **Mười một vi kỹ năng tầng 10 đã cắt** (Đại Số 5, Giải Tích 5, Xác Suất 1) với 109 câu và 17 bộ sinh không bao giờ
   được hỏi. **Khuyến nghị:** giữ cắt. Chúng đúng là "hệ tài năng": quan hệ, nhóm, vành, tiên đề số thực, metric. Kiếm
   Vực đã mở bằng nút `ud_*`/`lt_*` có thật, không cần chúng. Nếu muốn một ngày làm nhánh Tài Năng, hãy làm nhánh phụ
   sau Luyện Khí và đưa phần này vào, không kéo vào đường chính.
3. **Các cảnh sau Luyện Khí bắt đầu từ đâu.** Trong Luyện Khí, nhánh Lập Trình hết ở tầng 6 (tầng 7-9 chỉ còn `ud_*`
   và dự án): 12 đến 21 vi kỹ năng toán mỗi tầng nhưng bài code thưa dần. **Khuyến nghị:** làm Trúc Cơ tiếp ngay, ba nút
   tầng 1 (`tc_python_nang_cao`, `tc_du_lieu`, `tc_hoc_co_giam_sat`) đều là code và dữ liệu, đúng chỗ đang thiếu; viết
   bằng Python thuần như `lt_numpy` (pandas và scikit-learn không có trong bản web). Chưa viết Kết Đan khi Trúc Cơ còn trống.
4. **Mười bốn nút toán không có nút code hay thực chiến nào dùng trực tiếp** (trông hàn lâm nhất): `ds_dinh_thuc_nghich_dao`,
   `ds_khong_gian`, `ds_anh_xa_tuyen_tinh`, `gt_gioi_han`, `gt_taylor`, `gt_tich_phan`, `gt_tich_phan_ung_dung`,
   `gt_nhieu_bien`, `xs_dem_su_kien`, `xs_bnn_roi_rac`, `xs_bnn_lien_tuc`, `xs_ky_vong_phan_phoi`,
   `tr_liet_ke_quay_lui`, `tr_toi_uu_loi`. **Khuyến nghị:** không cắt (đa số là nền cần thiết); thay vào đó, khi có
   thời gian, gắn mỗi nút một bài code ngắn (Taylor: xấp xỉ bằng chuỗi; tích phân: cộng diện tích; bnn: mô phỏng).
5. **Ôn tập cuốn chiếu hẹp hơn tưởng.** Câu ôn chỉ lấy từ các nút trong `reinforces`, không từ mọi tổ tiên: trung bình
   một nút ôn lại 47% vi kỹ năng của tổ tiên (thấp nhất 8%), nhìn lại trung vị 2 tầng (tối đa 7), và chỉ 10 trong 35 nút
   toán có câu ôn lấy từ môn khác. Nút `ds_*` không bao giờ ôn môn khác vì chúng là gốc. **Khuyến nghị:** thêm cạnh
   `reinforces` chéo môn ở những nút đã có tổ tiên chéo môn (còn khoảng mười nút như `xs_kiem_dinh`,
   `tr_cay_duong_di`, `tr_gradient_descent`); tôi chỉ làm ba nút rõ ràng nhất. Muốn xa hơn thì đổi luật lấy câu ôn:
   rút từ mọi tổ tiên, ưu tiên cái lâu chưa gặp (luật 6b đã có lịch 1, 3, 7, 14 ngày).
6. **Bảy nút Luyện Khí đứng riêng** (không nối nhánh khác ở cả hai chiều): `ds_dinh_thuc_nghich_dao`,
   `ds_anh_xa_tuyen_tinh`, `gt_gioi_han`, `gt_taylor`, `xs_bnn_roi_rac`, `tr_liet_ke_quay_lui`, `lt_python_co_ban`.
   Phần lớn hợp lý (gốc, hoặc toán thuần). **Khuyến nghị:** không làm gì ngoài việc xem mục 4.
7. **Khối lượng các tầng đều**: 12 đến 24 vi kỹ năng mỗi tầng (trung vị 18), không tầng nào quá 1,4 lần trung vị.
   Tầng nặng nhất là 4 (24 vi kỹ năng và ba nút code), tầng 8-9 nhẹ về toán (12) nhưng nặng về dự án. **Khuyến nghị:**
   giữ nguyên; muốn bớt gánh tầng 4 thì dời `tr_do_thi` sang tầng 5 (hợp lệ: `tr_tim_kiem`, nút cần nó, cũng ở tầng 5).
8. **Cờ `dang_viet`** không còn nút nào dùng. **Khuyến nghị:** giữ giá trị trong luật (nút mới viết dở vẫn cần), vì
   luật mới đã bắt nó khi nút xong.

## 6. Còn yếu, chưa kiểm

- Mọi bộ sinh và bài tập mới đều `reviewed: false`: chưa ai đọc lời giải bằng mắt. Đáp án đã tính lại bằng sympy; chữ
  và độ khó chưa ai xét.
- Ô mỏng còn lại là loại không sinh tự động được.
- Công cụ rà soát đo "câu khác nhau" bằng 40 hạt giống, không đo độ khó thật.
- Chưa chạy lại giao diện Đạo Thụ trên máy (chỉ kiểm thử máy chủ); bài kiểm thử `client/tests/test_math_tree_flow.py`
  được đổi nút "trống" từ `lt_numpy` sang `tc_python_nang_cao` vì `lt_numpy` không còn trống.
- `server/tests/test_math_tree_progress.py::test_the_working_stage_is_one_above_the_stage_reached` hỏng sẵn trên nhánh gốc
  (33dbd65): nó cho rằng chiêu của tầng 2 mở ngay ở tầng 2, trong khi nay chiêu mở bằng nút Đạo Thụ. Không thuộc đợt
  này; ai làm chiêu thức nên sửa kỳ vọng của bài kiểm thử đó.
- "Bàn chỉnh cung" của Xạ Trường vẫn chưa làm (ghi trong `docs/THUC_CHIEN_TRONG_GAME.md`).
