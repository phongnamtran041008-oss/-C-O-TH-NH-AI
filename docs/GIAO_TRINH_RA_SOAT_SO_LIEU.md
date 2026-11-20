# Rà soát giáo trình: số liệu

Tệp này do `tools/audit_curriculum.py` sinh ra, đừng sửa tay. Chạy lại: `python tools/audit_curriculum.py`.

Một **ô** là một vi kỹ năng ở một bậc mà tầng của nó có thể hỏi. **Sức chứa** của ô là số câu khác nhau người học gặp được ở đó: mỗi câu viết tay tính 1, mỗi bộ sinh câu tính số câu khác nhau của 40 hạt giống. Ô **mỏng** là ô có sức chứa dưới 10.

## 1. Con số chính

| Chỉ số | Giá trị |
|---|---|
| nodes | 120 |
| nodes_luyen_khi_main | 58 |
| nodes_content_co | 37 |
| nodes_content_dang_viet | 38 |
| nodes_content_chua_co | 45 |
| luyen_khi_main_nodes_without_questions_or_exercises | 1 |
| skills_total | 215 |
| skills_cut | 11 |
| cells_main | 296 |
| cells_thin | 72 |
| cells_holes | 0 |
| cells_optional_thin | 8 |
| cut_items | 109 |
| cut_generators | 17 |
| main_skills_without_template | 0 |
| prerequisite_problems | 1 |
| hand_items | 1466 |
| generators | 351 |
| exercises | 71 |

## 2. Từng nhánh, từng nút

Cột `Tầng` là tầng của Luyện Khí (— = nút phụ). `Thật` là nút có thật câu hỏi hay bài tập (so với cờ `content` trong tree.json). `Thư viện` = số vi kỹ năng có tài liệu. `Chạm` = nơi khác trong game nhắc tới nút (quái, chiêu, kế hoạch thế giới, thành tựu, lộ trình).

### ds: Đại Số Tuyến Tính

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ds_ngon_ngu` | LK | 1 | chính | toan | co | co | — | 6 (6 có câu) | 1 | 6 | có | monsters×3, world_plan.weapons_placed×1 |
| `ds_vecto_ma_tran` | LK | 2 | chính | toan | co | co | `ds_ngon_ngu` | 6 (6 có câu) | 3 | 6 | có | chiêu×1, monsters×5, world_plan.lands×1 |
| `ds_nhan_ma_tran` | LK | 3 | chính | toan | dang_viet | co | `ds_vecto_ma_tran` | 6 (6 có câu) | 4 | 6 | có | monsters×6 |
| `ds_he_gauss` | LK | 4 | chính | toan | dang_viet | co | `ds_nhan_ma_tran` | 6 (6 có câu) | 5 | 6 | có | monsters×5, world_plan.weapons_placed×1 |
| `ds_dinh_thuc_nghich_dao` | LK | 5 | chính | toan | dang_viet | co | `ds_he_gauss` | 5 (5 có câu) | 6 | 5 | có | monsters×3 |
| `ds_khong_gian` | LK | 6 | chính | toan | dang_viet | co | `ds_dinh_thuc_nghich_dao` | 6 (6 có câu) | 7 | 6 | có | monsters×3 |
| `ds_anh_xa_tuyen_tinh` | LK | 7 | chính | toan | dang_viet | co | `ds_khong_gian`, `ds_ngon_ngu` | 6 (6 có câu) | 8 | 6 | có | monsters×3, world_plan.weapons_placed×1 |
| `ds_truc_giao_chieu` | LK | 7 | chính | toan | dang_viet | co | `ds_khong_gian` | 2 (2 có câu) | 9 | 2 | có | monsters×4, world_plan.weapons_placed×1 |
| `ds_tri_rieng` | LK | 8 | chính | toan | dang_viet | co | `ds_anh_xa_tuyen_tinh` | 2 (2 có câu) | 9 | 2 | có | monsters×5 |
| `ds_pca_svd` | LK | 9 | chính | toan | dang_viet | co | `ds_tri_rieng`, `ds_truc_giao_chieu` | 2 (2 có câu) | 9 | 2 | có | monsters×4, world_plan.weapons_placed×1 |
| `ds_cramer` | LK | — | phụ | toan | dang_viet | co | `ds_dinh_thuc_nghich_dao` | 1 (1 có câu) | 6 | 1 | có | — |
| `ds_so_phuc` | LK | — | phụ | toan | co | co | — | 6 (6 có câu) | 2 | 6 | có | — |

### gt: Giải Tích

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `gt_ham_so` | LK | 1 | chính | toan | co | co | — | 4 (4 có câu) | 1 | 4 | có | monsters×4, world_plan.weapons_placed×1 |
| `gt_gioi_han` | LK | 2 | chính | toan | co | co | `gt_ham_so` | 5 (5 có câu) | 2,3 | 5 | có | chiêu×1, monsters×3 |
| `gt_dao_ham` | LK | 3 | chính | toan | dang_viet | co | `gt_gioi_han` | 4 (4 có câu) | 4 | 4 | có | monsters×7 |
| `gt_cuc_tri` | LK | 4 | chính | toan | dang_viet | co | `gt_dao_ham` | 4 (4 có câu) | 6 | 4 | có | monsters×7, world_plan.weapons_placed×1 |
| `gt_taylor` | LK | 5 | chính | toan | dang_viet | co | `gt_dao_ham` | 2 (2 có câu) | 5 | 2 | có | monsters×3 |
| `gt_tich_phan` | LK | 5 | chính | toan | dang_viet | co | `gt_dao_ham` | 5 (5 có câu) | 7 | 5 | có | monsters×3 |
| `gt_nhieu_bien` | LK | 6 | chính | toan | dang_viet | co | `gt_dao_ham`, `gt_taylor`, `ds_vecto_ma_tran` | 3 (3 có câu) | 9 | 3 | có | monsters×2 |
| `gt_tich_phan_ung_dung` | LK | 6 | chính | toan | dang_viet | co | `gt_tich_phan`, `gt_gioi_han` | 2 (2 có câu) | 8 | 2 | có | monsters×3, world_plan.weapons_placed×1 |
| `gt_gradient` | LK | 7 | chính | toan | dang_viet | co | `gt_nhieu_bien`, `gt_cuc_tri`, `ds_nhan_ma_tran` | 3 (3 có câu) | 9 | 3 | có | monsters×6, world_plan.weapons_placed×2 |
| `gt_gioi_han_nang_cao` | LK | — | phụ | toan | co | co | `gt_gioi_han` | 5 (5 có câu) | 2,3 | 5 | có | — |
| `gt_ham_nguoc_tham_so` | LK | — | phụ | toan | dang_viet | co | `gt_dao_ham` | 1 (1 có câu) | 4 | 1 | có | — |
| `gt_hinh_hoc_tich_phan` | LK | — | phụ | toan | dang_viet | co | `gt_tich_phan_ung_dung`, `gt_ham_nguoc_tham_so`, `gt_gioi_han_nang_cao` | 4 (4 có câu) | 8 | 4 | có | — |
| `gt_khao_sat` | LK | — | phụ | toan | dang_viet | co | `gt_cuc_tri`, `gt_gioi_han_nang_cao` | 2 (2 có câu) | 6 | 2 | có | — |
| `gt_lhospital` | LK | — | phụ | toan | dang_viet | co | `gt_dao_ham`, `gt_gioi_han_nang_cao`, `gt_taylor` | 3 (3 có câu) | 5 | 3 | có | — |
| `gt_tich_phan_ky_thuat` | LK | — | phụ | toan | dang_viet | co | `gt_tich_phan` | 1 (1 có câu) | 7 | 1 | có | — |
| `gt_tinh_chat_ham` | LK | — | phụ | toan | co | co | `gt_ham_so` | 1 (1 có câu) | 1 | 1 | có | — |

### xs: Xác Suất và Thống Kê

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `xs_dem_su_kien` | LK | 1 | chính | toan | co | co | — | 5 (5 có câu) | 1 | 5 | có | monsters×2, world_plan.weapons_placed×1 |
| `xs_xac_suat` | LK | 2 | chính | toan | co | co | `xs_dem_su_kien` | 5 (5 có câu) | 2 | 5 | có | monsters×4 |
| `xs_dieu_kien` | LK | 3 | chính | toan | co | co | `xs_xac_suat` | 5 (5 có câu) | 3 | 5 | có | chiêu×1, monsters×6 |
| `xs_bayes` | LK | 4 | chính | toan | dang_viet | co | `xs_dieu_kien` | 5 (5 có câu) | 4 | 5 | có | monsters×5, world_plan.weapons_placed×1 |
| `xs_bnn_roi_rac` | LK | 5 | chính | toan | dang_viet | co | `xs_dieu_kien` | 3 (3 có câu) | 5 | 3 | có | monsters×3 |
| `xs_bnn_lien_tuc` | LK | 6 | chính | toan | dang_viet | co | `xs_bnn_roi_rac`, `gt_tich_phan` | 2 (2 có câu) | 5 | 2 | có | monsters×4 |
| `xs_ky_vong_phan_phoi` | LK | 7 | chính | toan | dang_viet | co | `xs_bnn_lien_tuc`, `gt_tich_phan_ung_dung` | 5 (5 có câu) | 6 | 5 | có | monsters×3, world_plan.weapons_placed×1 |
| `xs_mau_uoc_luong` | LK | 8 | chính | toan | dang_viet | co | `xs_ky_vong_phan_phoi`, `gt_cuc_tri` | 5 (5 có câu) | 7 | 5 | có | monsters×3 |
| `xs_tuong_quan_hoi_quy` | LK | 8 | chính | toan | co | co | `xs_mau_uoc_luong`, `ds_nhan_ma_tran` | 3 (3 có câu) | 10 | 3 | có | monsters×3 |
| `xs_kiem_dinh` | LK | 9 | chính | toan | dang_viet | co | `xs_tin_cay` | 5 (5 có câu) | 9 | 5 | có | monsters×4, world_plan.weapons_placed×1 |
| `xs_tin_cay` | LK | 9 | chính | toan | dang_viet | co | `xs_mau_uoc_luong` | 5 (5 có câu) | 8 | 5 | có | monsters×4 |
| `xs_ham_bnn` | LK | — | phụ | toan | co | co | `xs_ky_vong_phan_phoi` | 1 (1 có câu) | 10 | 1 | có | — |

### tr: Thuật Toán và Tối Ưu

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tr_logic_dem` | LK | 1 | chính | toan | co | co | — | 4 (4 có câu) | 1 | 4 | có | monsters×4, world_plan.weapons_placed×1 |
| `tr_dem` | LK | 2 | chính | toan | co | co | `tr_logic_dem`, `xs_dem_su_kien` | 4 (4 có câu) | 2 | 4 | có | monsters×4 |
| `tr_liet_ke_quay_lui` | LK | 3 | chính | toan | co | co | `tr_logic_dem` | 3 (3 có câu) | 3 | 3 | có | chiêu×1, monsters×3 |
| `tr_do_thi` | LK | 4 | chính | toan | dang_viet | co | `tr_logic_dem`, `ds_vecto_ma_tran` | 5 (5 có câu) | 5 | 5 | có | monsters×4, world_plan.weapons_placed×1 |
| `tr_thuat_toan` | LK | 4 | chính | toan | dang_viet | co | `tr_dem`, `tr_liet_ke_quay_lui` | 4 (4 có câu) | 4 | 4 | có | monsters×4, world_plan.weapons_placed×1 |
| `tr_tim_kiem` | LK | 5 | chính | toan | dang_viet | co | `tr_do_thi`, `tr_liet_ke_quay_lui` | 3 (3 có câu) | 6 | 3 | có | monsters×6 |
| `tr_cay_duong_di` | LK | 6 | chính | toan | dang_viet | co | `tr_tim_kiem`, `tr_thuat_toan` | 2 (2 có câu) | 7 | 2 | có | monsters×3 |
| `tr_toi_uu_loi` | LK | 7 | chính | toan | dang_viet | co | `tr_thuat_toan`, `gt_cuc_tri`, `gt_nhieu_bien` | 5 (5 có câu) | 8 | 5 | có | monsters×3, world_plan.weapons_placed×1 |
| `tr_gradient_descent` | LK | 8 | chính | toan | dang_viet | co | `tr_toi_uu_loi`, `gt_gradient` | 2 (2 có câu) | 9 | 2 | có | monsters×5, world_plan.weapons_placed×1 |
| `tr_cay_khung_luong` | LK | — | phụ | toan | dang_viet | co | `tr_cay_duong_di` | 3 (3 có câu) | 7 | 3 | có | — |
| `tr_dem_nang_cao` | LK | — | phụ | toan | co | co | `tr_dem` | 2 (2 có câu) | 2 | 2 | có | — |
| `tr_euler_hamilton` | LK | — | phụ | toan | dang_viet | co | `tr_tim_kiem` | 2 (2 có câu) | 6 | 2 | có | — |
| `tr_nhanh_can` | LK | — | phụ | toan | dang_viet | co | `tr_thuat_toan` | 1 (1 có câu) | 4 | 1 | có | — |
| `tr_phuong_phap_tinh` | LK | — | phụ | toan | co | co | `tr_toi_uu_loi` | 4 (4 có câu) | 10 | 4 | có | — |
| `tr_quy_hoach_tuyen_tinh` | LK | — | phụ | toan | dang_viet | co | `tr_toi_uu_loi` | 4 (4 có câu) | 9 | 4 | có | — |
| `tr_quy_nap` | LK | — | phụ | toan | co | co | `tr_logic_dem` | 1 (1 có câu) | 1 | 1 | có | — |
| `tr_ton_tai` | LK | — | phụ | toan | co | co | `tr_dem`, `tr_liet_ke_quay_lui` | 3 (3 có câu) | 3 | 3 | có | — |

### lt: Lập Trình

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lt_python_co_ban` | LK | 1 | chính | code | co | co | — | 5 bài | — | — | có | world_plan.lands×1, world_plan.weapons_placed×1 |
| `lt_cau_truc_du_lieu` | LK | 2 | chính | code | co | co | `lt_python_co_ban`, `ds_ngon_ngu` | 5 bài | — | — | có | world_plan.lands×1 |
| `lt_ham_de_quy` | LK | 3 | chính | code | co | co | `lt_python_co_ban`, `tr_logic_dem` | 5 bài | — | — | có | chiêu×1 |
| `lt_vecto_bang_code` | LK | 3 | chính | code | co | co | `lt_cau_truc_du_lieu`, `ds_vecto_ma_tran` | 5 bài | — | — | có | — |
| `lt_ma_tran_gauss` | LK | 4 | chính | code | co | co | `lt_vecto_bang_code`, `ds_he_gauss` | 5 bài | — | — | có | chiêu×1, world_plan.weapons_placed×1 |
| `lt_mo_phong_xac_suat` | LK | 4 | chính | code | co | co | `lt_cau_truc_du_lieu`, `xs_dieu_kien` | 5 bài | — | — | có | — |
| `lt_numpy` | LK | 4 | chính | code | chua_co | chua_co | `lt_vecto_bang_code`, `ds_nhan_ma_tran` | 0 bài | — | — | có | world_plan.weapons_placed×1 |
| `lt_dao_ham_so` | LK | 5 | chính | code | co | co | `lt_cau_truc_du_lieu`, `gt_cuc_tri` | 4 bài | — | — | có | chiêu×1 |
| `lt_do_phuc_tap` | LK | 5 | chính | code | co | co | `lt_ham_de_quy`, `tr_thuat_toan` | 5 bài | — | — | có | — |
| `lt_do_thi` | LK | 6 | chính | code | co | co | `lt_do_phuc_tap`, `tr_tim_kiem` | 5 bài | — | — | có | chiêu×2, world_plan.weapons_placed×2 |
| `tc_du_lieu` | truc_co | 1 | chính | code | chua_co | chua_co | `du_an_luyen_khi` | 0 bài | — | — | có | — |
| `tc_python_nang_cao` | truc_co | 1 | chính | code | chua_co | chua_co | `du_an_luyen_khi` | 0 bài | — | — | có | — |
| `tc_git` | truc_co | 3 | chính | code | chua_co | chua_co | `tc_python_nang_cao` | 0 bài | — | — | có | — |

### ud: Thực Chiến AI

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ud_knn` | LK | 3 | chính | thuc_chien | co | co | `lt_vecto_bang_code` | 3 bài | — | — | có | chiêu×1, world_plan.weapons_placed×1 |
| `ud_hoi_quy_1_bien` | LK | 5 | chính | thuc_chien | co | co | `lt_dao_ham_so` | 3 bài | — | — | có | chiêu×1, world_plan.weapons_placed×1 |
| `ud_naive_bayes` | LK | 5 | chính | thuc_chien | co | co | `xs_bayes`, `lt_cau_truc_du_lieu` | 3 bài | — | — | có | world_plan.weapons_placed×1 |
| `ud_binh_phuong_toi_thieu` | LK | 7 | chính | thuc_chien | co | co | `ds_truc_giao_chieu`, `lt_numpy`, `lt_ma_tran_gauss`, `ud_hoi_quy_1_bien` | 3 bài | — | — | có | chiêu×1 |
| `ud_mang_no_ron` | LK | 8 | chính | thuc_chien | co | co | `gt_gradient`, `tr_gradient_descent`, `lt_numpy` | 3 bài | — | — | có | chiêu×1, world_plan.weapons_placed×2 |
| `du_an_luyen_khi` | LK | 9 | chính | du_an | co | co | `ud_mang_no_ron`, `ud_logistic`, `ud_pca`, `ud_ab_test`, `ud_binh_phuong_toi_thieu`, `ud_naive_bayes`, `ud_knn`, `lt_do_thi`, `tr_cay_duong_di` | 3 bài | — | — | có | world_plan.lands×2, world_plan.weapons_placed×1 |
| `ud_ab_test` | LK | 9 | chính | thuc_chien | co | co | `xs_kiem_dinh`, `lt_mo_phong_xac_suat` | 3 bài | — | — | có | chiêu×1 |
| `ud_logistic` | LK | 9 | chính | thuc_chien | co | co | `xs_mau_uoc_luong`, `tr_gradient_descent`, `lt_numpy` | 2 bài | — | — | có | — |
| `ud_pca` | LK | 9 | chính | thuc_chien | co | co | `ds_pca_svd`, `xs_tuong_quan_hoi_quy`, `lt_numpy` | 3 bài | — | — | có | — |

### ml: Học Máy

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tc_hoc_co_giam_sat` | truc_co | 1 | chính | hoc_may | chua_co | chua_co | `du_an_luyen_khi` | 0 bài | — | — | có | world_plan.weapons_placed×1 |
| `tc_cay_quyet_dinh` | truc_co | 2 | chính | hoc_may | chua_co | chua_co | `tc_hoc_co_giam_sat` | 0 bài | — | — | có | world_plan.weapons_placed×1 |
| `tc_hoi_quy` | truc_co | 2 | chính | hoc_may | chua_co | chua_co | `tc_hoc_co_giam_sat`, `tc_du_lieu` | 0 bài | — | — | có | — |
| `tc_phan_loai` | truc_co | 2 | chính | hoc_may | chua_co | chua_co | `tc_hoc_co_giam_sat` | 0 bài | — | — | có | world_plan.weapons_placed×1 |
| `du_an_truc_co` | truc_co | 3 | chính | du_an | chua_co | chua_co | `tc_danh_gia`, `tc_cay_quyet_dinh`, `tc_git` | 0 bài | — | — | có | — |
| `tc_danh_gia` | truc_co | 3 | chính | hoc_may | chua_co | chua_co | `tc_hoi_quy`, `tc_phan_loai` | 0 bài | — | — | có | world_plan.weapons_placed×1 |
| `kd_ensemble` | ket_dan | 1 | chính | hoc_may | chua_co | chua_co | `du_an_truc_co` | 0 bài | — | — | có | — |
| `kd_thong_tin` | ket_dan | 1 | chính | hoc_may | chua_co | chua_co | `du_an_truc_co` | 0 bài | — | — | có | — |
| `kd_dac_trung` | ket_dan | 2 | chính | hoc_may | chua_co | chua_co | `kd_ensemble` | 0 bài | — | — | có | — |
| `kd_khong_giam_sat` | ket_dan | 2 | chính | hoc_may | chua_co | chua_co | `kd_ensemble` | 0 bài | — | — | có | — |
| `kd_toi_uu_ml` | ket_dan | 2 | chính | hoc_may | chua_co | chua_co | `kd_thong_tin` | 0 bài | — | — | có | — |
| `du_an_ket_dan` | ket_dan | 3 | chính | du_an | chua_co | chua_co | `kd_svm`, `kd_khong_giam_sat`, `kd_dac_trung` | 0 bài | — | — | có | — |
| `kd_svm` | ket_dan | 3 | chính | hoc_may | chua_co | chua_co | `kd_toi_uu_ml` | 0 bài | — | — | có | — |

### dl: Học Sâu

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `na_autograd` | nguyen_anh | 1 | chính | hoc_sau | chua_co | chua_co | `du_an_ket_dan` | 0 bài | — | — | có | — |
| `na_pytorch` | nguyen_anh | 1 | chính | hoc_sau | chua_co | chua_co | `na_autograd` | 0 bài | — | — | có | — |
| `na_cnn` | nguyen_anh | 2 | chính | hoc_sau | chua_co | chua_co | `na_pytorch` | 0 bài | — | — | có | — |
| `na_huan_luyen` | nguyen_anh | 2 | chính | hoc_sau | chua_co | chua_co | `na_pytorch` | 0 bài | — | — | có | — |
| `du_an_nguyen_anh` | nguyen_anh | 3 | chính | du_an | chua_co | chua_co | `na_cnn`, `na_chuoi` | 0 bài | — | — | có | — |
| `na_chuoi` | nguyen_anh | 3 | chính | hoc_sau | chua_co | chua_co | `na_huan_luyen` | 0 bài | — | — | có | — |
| `ht_attention` | hoa_than | 1 | chính | hoc_sau | chua_co | chua_co | `du_an_nguyen_anh` | 0 bài | — | — | có | — |
| `ht_gpt_nho` | hoa_than | 1 | chính | hoc_sau | chua_co | chua_co | `ht_attention` | 0 bài | — | — | có | — |
| `ht_tinh_chinh` | hoa_than | 2 | chính | hoc_sau | chua_co | chua_co | `ht_gpt_nho` | 0 bài | — | — | có | — |
| `ht_ung_dung_llm` | hoa_than | 2 | chính | hoc_sau | chua_co | chua_co | `ht_gpt_nho` | 0 bài | — | — | có | — |
| `du_an_hoa_than` | hoa_than | 3 | chính | du_an | chua_co | chua_co | `ht_danh_gia_llm` | 0 bài | — | — | có | — |
| `ht_danh_gia_llm` | hoa_than | 3 | chính | hoc_sau | chua_co | chua_co | `ht_tinh_chinh`, `ht_ung_dung_llm` | 0 bài | — | — | có | — |

### ht: Hệ Thống

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lh_du_lieu_lon` | luyen_hu | 1 | chính | he_thong | chua_co | chua_co | `du_an_hoa_than` | 0 bài | — | — | có | — |
| `lh_ky_thuat_phan_mem` | luyen_hu | 1 | chính | he_thong | chua_co | chua_co | `du_an_hoa_than` | 0 bài | — | — | có | — |
| `lh_huan_luyen_lon` | luyen_hu | 2 | chính | he_thong | chua_co | chua_co | `lh_ky_thuat_phan_mem` | 0 bài | — | — | có | — |
| `lh_trien_khai` | luyen_hu | 2 | chính | he_thong | chua_co | chua_co | `lh_ky_thuat_phan_mem`, `lh_du_lieu_lon` | 0 bài | — | — | có | — |
| `du_an_luyen_hu` | luyen_hu | 3 | chính | du_an | chua_co | chua_co | `lh_giam_sat`, `lh_huan_luyen_lon` | 0 bài | — | — | có | — |
| `lh_giam_sat` | luyen_hu | 3 | chính | he_thong | chua_co | chua_co | `lh_trien_khai` | 0 bài | — | — | có | — |

### nc: Nghiên Cứu và Dẫn Dắt

| Nút | Cảnh | Tầng | Loại | Kiểu | content | Thật | Cần | Vi kỹ năng / bài | Tầng toán | Thư viện | Nguồn | Chạm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hp_doc_bai_bao` | hop_the | 1 | chính | nghien_cuu | chua_co | chua_co | `du_an_luyen_hu` | 0 bài | — | — | có | — |
| `hp_tai_lap` | hop_the | 1 | chính | nghien_cuu | chua_co | chua_co | `hp_doc_bai_bao` | 0 bài | — | — | có | — |
| `hp_an_toan` | hop_the | 2 | chính | nghien_cuu | chua_co | chua_co | `hp_tai_lap` | 0 bài | — | — | có | — |
| `hp_hoc_tang_cuong` | hop_the | 2 | chính | nghien_cuu | chua_co | chua_co | `hp_tai_lap` | 0 bài | — | — | có | — |
| `du_an_hop_the` | hop_the | 3 | chính | du_an | chua_co | chua_co | `hp_viet` | 0 bài | — | — | có | — |
| `hp_viet` | hop_the | 3 | chính | nghien_cuu | chua_co | chua_co | `hp_hoc_tang_cuong`, `hp_an_toan` | 0 bài | — | — | có | — |
| `dt_gu_nghien_cuu` | dai_thua | 1 | chính | dan_dat | chua_co | chua_co | `du_an_hop_the` | 0 bài | — | — | có | — |
| `dt_chien_luoc` | dai_thua | 2 | chính | dan_dat | chua_co | chua_co | `dt_gu_nghien_cuu` | 0 bài | — | — | có | — |
| `dt_dan_dat_doi` | dai_thua | 2 | chính | dan_dat | chua_co | chua_co | `dt_gu_nghien_cuu` | 0 bài | — | — | có | — |
| `du_an_dai_thua` | dai_thua | 3 | chính | du_an | chua_co | chua_co | `dt_dan_dat_doi`, `dt_chien_luoc` | 0 bài | — | — | có | — |

## 3. Vi kỹ năng × bậc

Mỗi ô ghi `viết tay/bộ sinh→sức chứa`. Ô mỏng đánh dấu `!`. Vi kỹ năng thuộc danh sách cắt có ghi `cắt`.

### Đại Số Tuyến Tính

| Vi kỹ năng | Nút | Tầng toán | Bậc 1 | Bậc 2 | Bậc 3 | Bậc 4 | Bậc 5 |
|---|---|---|---|---|---|---|---|
| `dstt_t1_tap_hop` | `ds_ngon_ngu` | 1 | 3/1→43 | 3/1→42 |  |  |  |
| `dstt_t1_phep_toan_tap_hop` | `ds_ngon_ngu` | 1 | 4/2→84 | 4/1→44 |  |  |  |
| `dstt_t1_tich_descartes` | `ds_ngon_ngu` | 1 | 3/1→43 | 3/1→36 |  |  |  |
| `dstt_t1_anh_xa` | `ds_ngon_ngu` | 1 | 2/1→42 | 4/1→43 |  |  |  |
| `dstt_t1_don_toan_song_anh` | `ds_ngon_ngu` | 1 | 2/1→36 | 3/1→15 |  |  |  |
| `dstt_t1_hop_va_nguoc` | `ds_ngon_ngu` | 1 | 2/1→42 | 3/1→43 |  |  |  |
| `dstt_t2_dang_dai_so` | `ds_so_phuc` | 2 | 3/1→42 | 3/1→36 |  |  |  |
| `dstt_t2_cong_nhan` | `ds_so_phuc` | 2 | 2/1→42 | 2/1→42 |  |  |  |
| `dstt_t2_lien_hop_modun` | `ds_so_phuc` | 2 | 3/1→33 | 2/1→41 |  |  |  |
| `dstt_t2_chia` | `ds_so_phuc` | 2 | 2/1→41 | 3/1→43 |  |  |  |
| `dstt_t2_dang_luong_giac` | `ds_so_phuc` | 2 | 1/1→34 | 4/1→30 |  |  |  |
| `dstt_t2_can_bac_n` | `ds_so_phuc` | 2 | 2/1→42 | 3/1→32 |  |  |  |
| `dstt_t3_vecto_rn` | `ds_vecto_ma_tran` | 3 |  | 4/1→44 | 1/1→41 |  |  |
| `dstt_t3_kich_thuoc_phan_tu` | `ds_vecto_ma_tran` | 3 |  | 4/1→44 | 1/1→38 |  |  |
| `dstt_t3_cong_nhan_vo_huong` | `ds_vecto_ma_tran` | 3 |  | 2/1→42 | 2/1→42 |  |  |
| `dstt_t3_chuyen_vi` | `ds_vecto_ma_tran` | 3 |  | 3/1→43 | 3/1→43 |  |  |
| `dstt_t3_vet` | `ds_vecto_ma_tran` | 3 |  | 2/1→42 | 4/1→44 |  |  |
| `dstt_t3_ma_tran_dac_biet` | `ds_vecto_ma_tran` | 3 |  | 3/1→43 | 4/1→44 |  |  |
| `dstt_t4_tich_vo_huong` | `ds_nhan_ma_tran` | 4 |  | 4/1→44 | 2/0→2! |  |  |
| `dstt_t4_dieu_kien_kich_thuoc` | `ds_nhan_ma_tran` | 4 |  | 3/1→40 | 4/1→43 |  |  |
| `dstt_t4_nhan_ma_tran` | `ds_nhan_ma_tran` | 4 |  | 4/1→44 | 3/1→43 |  |  |
| `dstt_t4_khong_giao_hoan` | `ds_nhan_ma_tran` | 4 |  | 2/0→2! | 4/1→44 |  |  |
| `dstt_t4_tinh_chat_nhan` | `ds_nhan_ma_tran` | 4 |  | 3/0→3! | 3/1→43 |  |  |
| `dstt_t4_luy_thua` | `ds_nhan_ma_tran` | 4 |  | 2/1→42 | 4/1→41 |  |  |
| `dstt_t5_dang_ma_tran` | `ds_he_gauss` | 5 |  |  | 3/1→43 | 3/0→3! |  |
| `dstt_t5_bien_doi_hang` | `ds_he_gauss` | 5 |  |  | 3/1→43 | 4/0→4! |  |
| `dstt_t5_bac_thang` | `ds_he_gauss` | 5 |  |  | 4/0→4! | 4/0→4! |  |
| `dstt_t5_the_nguoc` | `ds_he_gauss` | 5 |  |  | 3/1→43 | 3/1→43 |  |
| `dstt_t5_so_nghiem` | `ds_he_gauss` | 5 |  |  | 3/1→43 | 5/1→45 |  |
| `dstt_t5_he_thuan_nhat` | `ds_he_gauss` | 5 |  |  | 2/1→42 | 2/1→42 |  |
| `dstt_t6_dinh_thuc_cap_2_3` | `ds_dinh_thuc_nghich_dao` | 6 |  |  | 4/1→44 | 1/1→41 |  |
| `dstt_t6_khai_trien` | `ds_dinh_thuc_nghich_dao` | 6 |  |  | 3/1→43 | 3/1→43 |  |
| `dstt_t6_tinh_chat_dinh_thuc` | `ds_dinh_thuc_nghich_dao` | 6 |  |  | 2/1→42 | 5/0→5! |  |
| `dstt_t6_hang` | `ds_dinh_thuc_nghich_dao` | 6 |  |  | 2/1→42 | 3/0→3! |  |
| `dstt_t6_nghich_dao` | `ds_dinh_thuc_nghich_dao` | 6 |  |  | 3/1→43 | 4/1→44 |  |
| `dstt_t6_giai_he_nghich_dao` | `ds_cramer` | 6 |  |  | 3/1→43 | 3/1→43 |  |
| `dstt_t7_khong_gian_vecto` | `ds_khong_gian` | 7 |  |  |  | 3/0→3! | 2/0→2! |
| `dstt_t7_khong_gian_con` | `ds_khong_gian` | 7 |  |  |  | 4/0→4! | 3/0→3! |
| `dstt_t7_to_hop_tuyen_tinh` | `ds_khong_gian` | 7 |  |  |  | 2/1→42 | 2/0→2! |
| `dstt_t7_doc_lap_tuyen_tinh` | `ds_khong_gian` | 7 |  |  |  | 2/1→42 | 3/0→3! |
| `dstt_t7_co_so_so_chieu` | `ds_khong_gian` | 7 |  |  |  | 4/1→44 | 3/0→3! |
| `dstt_t7_toa_do` | `ds_khong_gian` | 7 |  |  |  | 2/1→42 | 2/0→2! |
| `dstt_t8_anh_xa_tuyen_tinh` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 3/1→43 | 3/0→3! |
| `dstt_t8_nhan_va_anh` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 4/0→4! | 3/0→3! |
| `dstt_t8_dinh_ly_so_chieu` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 3/1→43 | 3/0→3! |
| `dstt_t8_ma_tran_anh_xa` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 2/1→42 | 3/0→3! |
| `dstt_t8_hop_anh_xa` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 3/1→43 | 2/0→2! |
| `dstt_t8_doi_co_so` | `ds_anh_xa_tuyen_tinh` | 8 |  |  |  | 2/1→42 | 2/0→2! |
| `dstt_t9_tri_rieng` | `ds_tri_rieng` | 9 |  |  |  |  | 6/1→46 |
| `dstt_t9_cheo_hoa` | `ds_tri_rieng` | 9 |  |  |  |  | 5/2→82 |
| `dstt_t9_khong_gian_euclide` | `ds_truc_giao_chieu` | 9 |  |  |  |  | 5/1→45 |
| `dstt_t9_dang_toan_phuong` | `ds_pca_svd` | 9 |  |  |  |  | 5/1→44 |
| `dstt_t9_phep_chieu` | `ds_truc_giao_chieu` | 9 |  |  |  |  | 5/1→45 |
| `dstt_t9_pca_svd` | `ds_pca_svd` | 9 |  |  |  |  | 4/0→4! |
| `dstt_t10_quan_he` cắt | — | 10 |  |  |  |  | 9/2→86 |
| `dstt_t10_phep_toan_hai_ngoi` cắt | — | 10 |  |  |  |  | 10/2→78 |
| `dstt_t10_nhom` cắt | — | 10 |  |  |  |  | 10/2→67 |
| `dstt_t10_vanh_truong` cắt | — | 10 |  |  |  |  | 9/2→85 |
| `dstt_t10_dang_song_tuyen_tinh` cắt | — | 10 |  |  |  |  | 10/2→90 |

### Giải Tích

| Vi kỹ năng | Nút | Tầng toán | Bậc 1 | Bậc 2 | Bậc 3 | Bậc 4 | Bậc 5 |
|---|---|---|---|---|---|---|---|
| `gt_t1_ham_so` | `gt_ham_so` | 1 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t1_tinh_chat_ham` | `gt_tinh_chat_ham` | 1 | 3/1→41 | 5/1→43 |  |  |  |
| `gt_t1_ham_hop` | `gt_ham_so` | 1 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t1_ham_nguoc` | `gt_ham_so` | 1 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t1_ham_so_cap` | `gt_ham_so` | 1 | 5/1→32 | 5/1→39 |  |  |  |
| `gt_t2_gioi_han_day` | `gt_gioi_han` | 2 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t2_gioi_han_ham` | `gt_gioi_han` | 2 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t2_gioi_han_vo_cuc` | `gt_gioi_han` | 2 | 4/1→44 | 5/1→45 |  |  |  |
| `gt_t2_gioi_han_dac_biet` | `gt_gioi_han_nang_cao` | 2 | 4/1→42 | 5/1→37 |  |  |  |
| `gt_t2_vo_cung_be` | `gt_gioi_han_nang_cao` | 2 | 4/1→37 | 5/1→43 |  |  |  |
| `gt_t3_lien_tuc_diem` | `gt_gioi_han` | 3 |  | 5/1→44 | 5/1→39 |  |  |
| `gt_t3_mot_phia` | `gt_gioi_han` | 3 |  | 5/1→45 | 5/1→43 |  |  |
| `gt_t3_tim_tham_so` | `gt_gioi_han_nang_cao` | 3 |  | 5/1→43 | 5/1→45 |  |  |
| `gt_t3_phan_loai_gian_doan` | `gt_gioi_han_nang_cao` | 3 |  | 5/1→45 | 5/1→45 |  |  |
| `gt_t3_lien_tuc_doan` | `gt_gioi_han_nang_cao` | 3 |  | 5/1→45 | 5/1→45 |  |  |
| `gt_t4_dinh_nghia_dao_ham` | `gt_dao_ham` | 4 |  | 3/1→43 | 4/1→44 |  |  |
| `gt_t4_quy_tac_tinh` | `gt_dao_ham` | 4 |  | 4/1→44 | 4/1→44 |  |  |
| `gt_t4_day_chuyen` | `gt_dao_ham` | 4 |  | 4/2→83 | 5/1→45 |  |  |
| `gt_t4_ham_nguoc_tham_so` | `gt_ham_nguoc_tham_so` | 4 |  | 3/1→43 | 5/1→45 |  |  |
| `gt_t4_vi_phan_cap_cao` | `gt_dao_ham` | 4 |  | 4/1→37 | 5/1→43 |  |  |
| `gt_t5_rolle_lagrange` | `gt_lhospital` | 5 |  |  | 5/2→78 | 4/1→26 |  |
| `gt_t5_taylor` | `gt_taylor` | 5 |  |  | 4/1→44 | 4/1→26 |  |
| `gt_t5_maclaurin` | `gt_taylor` | 5 |  |  | 4/1→36 | 5/1→39 |  |
| `gt_t5_lhospital` | `gt_lhospital` | 5 |  |  | 5/1→43 | 4/1→35 |  |
| `gt_t5_dang_vo_dinh` | `gt_lhospital` | 5 |  |  | 4/1→31 | 5/1→40 |  |
| `gt_t6_don_dieu` | `gt_cuc_tri` | 6 |  |  | 4/1→44 | 3/1→39 |  |
| `gt_t6_cuc_tri` | `gt_cuc_tri` | 6 |  |  | 4/1→44 | 3/1→32 |  |
| `gt_t6_gtln_gtnn` | `gt_cuc_tri` | 6 |  |  | 4/1→33 | 5/1→44 |  |
| `gt_t6_loi_lom` | `gt_cuc_tri` | 6 |  |  | 4/1→44 | 4/1→40 |  |
| `gt_t6_tiem_can` | `gt_khao_sat` | 6 |  |  | 4/2→84 | 3/0→3! |  |
| `gt_t6_khao_sat` | `gt_khao_sat` | 6 |  |  | 4/0→4! | 4/1→35 |  |
| `gt_t7_nguyen_ham` | `gt_tich_phan` | 7 |  |  |  | 3/1→43 | 2/0→2! |
| `gt_t7_doi_bien` | `gt_tich_phan` | 7 |  |  |  | 3/1→32 | 2/0→2! |
| `gt_t7_tung_phan` | `gt_tich_phan` | 7 |  |  |  | 3/1→35 | 3/0→3! |
| `gt_t7_ham_huu_ty` | `gt_tich_phan_ky_thuat` | 7 |  |  |  | 6/1→44 | 2/0→2! |
| `gt_t7_newton_leibniz` | `gt_tich_phan` | 7 |  |  |  | 4/1→28 | 3/0→3! |
| `gt_t7_can_bien_thien` | `gt_tich_phan` | 7 |  |  |  | 5/1→44 | 2/0→2! |
| `gt_t8_dien_tich` | `gt_tich_phan_ung_dung` | 8 |  |  |  | 3/1→39 | 3/0→3! |
| `gt_t8_the_tich` | `gt_hinh_hoc_tich_phan` | 8 |  |  |  | 5/1→26 | 2/0→2! |
| `gt_t8_do_dai_cung` | `gt_hinh_hoc_tich_phan` | 8 |  |  |  | 4/1→19 | 2/0→2! |
| `gt_t8_suy_rong_loai_1` | `gt_tich_phan_ung_dung` | 8 |  |  |  | 4/1→31 | 2/0→2! |
| `gt_t8_suy_rong_loai_2` | `gt_hinh_hoc_tich_phan` | 8 |  |  |  | 3/1→29 | 2/0→2! |
| `gt_t8_tieu_chuan_hoi_tu` | `gt_hinh_hoc_tich_phan` | 8 |  |  |  | 3/1→15 | 4/0→4! |
| `gt_t9_gioi_han_lien_tuc` | `gt_nhieu_bien` | 9 |  |  |  |  | 5/0→5! |
| `gt_t9_dao_ham_rieng` | `gt_nhieu_bien` | 9 |  |  |  |  | 5/1→45 |
| `gt_t9_vi_phan_ham_an` | `gt_nhieu_bien` | 9 |  |  |  |  | 6/1→42 |
| `gt_t9_cuc_tri` | `gt_gradient` | 9 |  |  |  |  | 6/2→86 |
| `gt_t9_cuc_tri_dieu_kien` | `gt_gradient` | 9 |  |  |  |  | 6/1→38 |
| `gt_t9_gradient_lan_truyen` | `gt_gradient` | 9 |  |  |  |  | 8/2→88 |
| `gt_t10_tien_de_so_thuc` cắt | — | 10 |  |  |  |  | 11/1→47 |
| `gt_t10_gioi_han_tren_duoi` cắt | — | 10 |  |  |  |  | 10/1→49 |
| `gt_t10_kha_tich_riemann` cắt | — | 10 |  |  |  |  | 11/1→51 |
| `gt_t10_ham_loi` cắt | — | 10 |  |  |  |  | 10/2→89 |
| `gt_t10_khong_gian_metric` cắt | — | 10 |  |  |  |  | 11/2→61 |

### Xác Suất và Thống Kê

| Vi kỹ năng | Nút | Tầng toán | Bậc 1 | Bậc 2 | Bậc 3 | Bậc 4 | Bậc 5 |
|---|---|---|---|---|---|---|---|
| `xs_t1_khong_gian_mau` | `xs_dem_su_kien` | 1 | 4/1→21 | 4/0→4! |  |  |  |
| `xs_t1_quan_he_su_kien` | `xs_dem_su_kien` | 1 | 4/1→35 | 4/0→4! |  |  |  |
| `xs_t1_quy_tac_dem` | `xs_dem_su_kien` | 1 | 4/1→36 | 3/1→30 |  |  |  |
| `xs_t1_hoan_vi_chinh_hop` | `xs_dem_su_kien` | 1 | 3/1→13 | 4/1→27 |  |  |  |
| `xs_t1_to_hop` | `xs_dem_su_kien` | 1 | 4/1→27 | 3/2→70 |  |  |  |
| `xs_t2_co_dien` | `xs_xac_suat` | 2 | 4/1→26 | 4/1→25 |  |  |  |
| `xs_t2_co_dien_to_hop` | `xs_xac_suat` | 2 | 3/0→3! | 4/2→51 |  |  |  |
| `xs_t2_hoan_lai` | `xs_xac_suat` | 2 | 4/0→4! | 4/1→39 |  |  |  |
| `xs_t2_tinh_chat` | `xs_xac_suat` | 2 | 3/0→3! | 4/1→15 |  |  |  |
| `xs_t2_thong_ke` | `xs_xac_suat` | 2 | 3/1→43 | 4/1→44 |  |  |  |
| `xs_t3_cong_thuc_cong` | `xs_dieu_kien` | 3 |  | 4/1→42 | 4/1→44 |  |  |
| `xs_t3_dieu_kien` | `xs_dieu_kien` | 3 |  | 4/1→44 | 4/1→27 |  |  |
| `xs_t3_cong_thuc_nhan` | `xs_dieu_kien` | 3 |  | 4/1→37 | 3/0→3! |  |  |
| `xs_t3_doc_lap` | `xs_dieu_kien` | 3 |  | 5/1→44 | 3/1→24 |  |  |
| `xs_t3_bernoulli` | `xs_dieu_kien` | 3 |  | 4/1→39 | 4/1→36 |  |  |
| `xs_t4_he_day_du` | `xs_bayes` | 4 |  | 4/1→43 | 4/0→4! |  |  |
| `xs_t4_so_do_cay` | `xs_bayes` | 4 |  | 4/1→44 | 4/0→4! |  |  |
| `xs_t4_day_du` | `xs_bayes` | 4 |  | 4/1→44 | 4/1→43 |  |  |
| `xs_t4_bayes` | `xs_bayes` | 4 |  | 4/0→4! | 4/1→44 |  |  |
| `xs_t4_bayes_ung_dung` | `xs_bayes` | 4 |  | 4/0→4! | 4/1→40 |  |  |
| `xs_t5_bien_ngau_nhien` | `xs_bnn_roi_rac` | 5 |  |  | 4/0→4! | 3/0→3! |  |
| `xs_t5_bang_phan_phoi` | `xs_bnn_roi_rac` | 5 |  |  | 4/2→79 | 4/0→4! |  |
| `xs_t5_ham_phan_phoi` | `xs_bnn_roi_rac` | 5 |  |  | 4/1→44 | 3/0→3! |  |
| `xs_t5_mat_do` | `xs_bnn_lien_tuc` | 5 |  |  | 4/2→43 | 4/0→4! |  |
| `xs_t5_xac_suat_khoang` | `xs_bnn_lien_tuc` | 5 |  |  | 4/0→4! | 4/1→39 |  |
| `xs_t6_ky_vong` | `xs_ky_vong_phan_phoi` | 6 |  |  | 4/1→44 | 4/0→4! |  |
| `xs_t6_phuong_sai` | `xs_ky_vong_phan_phoi` | 6 |  |  | 4/1→44 | 4/1→44 |  |
| `xs_t6_nhi_thuc_poisson` | `xs_ky_vong_phan_phoi` | 6 |  |  | 4/1→43 | 4/1→33 |  |
| `xs_t6_deu_mu` | `xs_ky_vong_phan_phoi` | 6 |  |  | 4/1→44 | 4/0→4! |  |
| `xs_t6_chuan` | `xs_ky_vong_phan_phoi` | 6 |  |  | 4/0→4! | 4/1→43 |  |
| `xs_t7_tong_the_mau` | `xs_mau_uoc_luong` | 7 |  |  |  | 4/0→4! | 2/0→2! |
| `xs_t7_dac_trung_mau` | `xs_mau_uoc_luong` | 7 |  |  |  | 4/2→84 | 2/0→2! |
| `xs_t7_phan_phoi_mau` | `xs_mau_uoc_luong` | 7 |  |  |  | 4/1→44 | 2/0→2! |
| `xs_t7_uoc_luong_diem` | `xs_mau_uoc_luong` | 7 |  |  |  | 4/1→43 | 2/0→2! |
| `xs_t7_hop_ly_cuc_dai` | `xs_mau_uoc_luong` | 7 |  |  |  | 4/1→44 | 2/0→2! |
| `xs_t8_tin_cay_trung_binh` | `xs_tin_cay` | 8 |  |  |  | 3/2→83 | 2/0→2! |
| `xs_t8_tin_cay_ty_le` | `xs_tin_cay` | 8 |  |  |  | 4/1→36 | 2/0→2! |
| `xs_t8_co_mau` | `xs_tin_cay` | 8 |  |  |  | 4/1→41 | 2/0→2! |
| `xs_t8_luat_so_lon` | `xs_tin_cay` | 8 |  |  |  | 4/1→42 | 2/0→2! |
| `xs_t8_gioi_han_trung_tam` | `xs_tin_cay` | 8 |  |  |  | 4/1→44 | 2/0→2! |
| `xs_t9_gia_thuyet` | `xs_kiem_dinh` | 9 |  |  |  |  | 6/1→46 |
| `xs_t9_kiem_dinh_trung_binh` | `xs_kiem_dinh` | 9 |  |  |  |  | 6/2→86 |
| `xs_t9_kiem_dinh_ty_le` | `xs_kiem_dinh` | 9 |  |  |  |  | 6/1→40 |
| `xs_t9_so_sanh_trung_binh` | `xs_kiem_dinh` | 9 |  |  |  |  | 6/1→46 |
| `xs_t9_so_sanh_ty_le` | `xs_kiem_dinh` | 9 |  |  |  |  | 6/0→6! |
| `xs_t10_ham_bien_ngau_nhien` | `xs_ham_bnn` | 10 |  |  |  |  | 10/1→50 |
| `xs_t10_vecto_ngau_nhien` | `xs_tuong_quan_hoi_quy` | 10 |  |  |  |  | 9/2→89 |
| `xs_t10_tuong_quan` | `xs_tuong_quan_hoi_quy` | 10 |  |  |  |  | 11/2→91 |
| `xs_t10_hoi_quy` | `xs_tuong_quan_hoi_quy` | 10 |  |  |  |  | 11/1→51 |
| `xs_t10_tien_de` cắt | — | 10 |  |  |  |  | 8/0→8 |

### Tối Ưu và Toán Rời Rạc

| Vi kỹ năng | Nút | Tầng toán | Bậc 1 | Bậc 2 | Bậc 3 | Bậc 4 | Bậc 5 |
|---|---|---|---|---|---|---|---|
| `tr_t1_cau_hinh` | `tr_logic_dem` | 1 | 3/1→28 | 4/1→28 |  |  |  |
| `tr_t1_cong_nhan` | `tr_logic_dem` | 1 | 4/1→42 | 4/1→38 |  |  |  |
| `tr_t1_menh_de` | `tr_logic_dem` | 1 | 4/1→29 | 3/1→43 |  |  |  |
| `tr_t1_bang_chan_tri` | `tr_logic_dem` | 1 | 3/1→38 | 5/1→44 |  |  |  |
| `tr_t1_quy_nap` | `tr_quy_nap` | 1 | 3/1→40 | 4/1→33 |  |  |  |
| `tr_t2_chinh_hop` | `tr_dem` | 2 | 3/1→26 | 2/1→25 |  |  |  |
| `tr_t2_hoan_vi` | `tr_dem` | 2 | 2/1→18 | 5/2→50 |  |  |  |
| `tr_t2_to_hop` | `tr_dem` | 2 | 4/1→30 | 4/1→38 |  |  |  |
| `tr_t2_to_hop_lap` | `tr_dem_nang_cao` | 2 | 3/1→26 | 4/1→28 |  |  |  |
| `tr_t2_bu_tru` | `tr_dem_nang_cao` | 2 | 3/1→43 | 4/1→43 |  |  |  |
| `tr_t2_truy_hoi` | `tr_dem` | 2 | 4/1→43 | 3/1→20 |  |  |  |
| `tr_t3_dirichlet` | `tr_ton_tai` | 3 |  | 3/2→75 | 3/1→18 |  |  |
| `tr_t3_bat_bien` | `tr_ton_tai` | 3 |  | 3/1→34 | 3/1→35 |  |  |
| `tr_t3_tu_dien` | `tr_liet_ke_quay_lui` | 3 |  | 3/1→43 | 2/0→2! |  |  |
| `tr_t3_sinh_ke_tiep` | `tr_liet_ke_quay_lui` | 3 |  | 3/2→76 | 3/1→39 |  |  |
| `tr_t3_thu_hang` | `tr_ton_tai` | 3 |  | 3/1→38 | 3/2→77 |  |  |
| `tr_t3_quay_lui` | `tr_liet_ke_quay_lui` | 3 |  | 3/1→23 | 3/1→33 |  |  |
| `tr_t4_phat_bieu` | `tr_thuat_toan` | 4 |  | 3/0→3! | 2/1→42 |  |  |
| `tr_t4_duyet_toan_bo` | `tr_thuat_toan` | 4 |  | 3/1→21 | 3/2→83 |  |  |
| `tr_t4_nhanh_can` | `tr_nhanh_can` | 4 |  | 2/0→2! | 3/1→43 |  |  |
| `tr_t4_tham_lam` | `tr_thuat_toan` | 4 |  | 2/1→42 | 2/1→39 |  |  |
| `tr_t4_ky_hieu_o` | `tr_thuat_toan` | 4 |  | 3/1→38 | 4/1→43 |  |  |
| `tr_t5_khai_niem` | `tr_do_thi` | 5 |  |  | 4/1→36 | 2/1→42 |  |
| `tr_t5_bac` | `tr_do_thi` | 5 |  |  | 3/1→43 | 3/1→38 |  |
| `tr_t5_duong_di_lien_thong` | `tr_do_thi` | 5 |  |  | 4/1→44 | 2/0→2! |  |
| `tr_t5_ma_tran_ke` | `tr_do_thi` | 5 |  |  | 2/2→72 | 2/1→41 |  |
| `tr_t5_danh_sach_ke` | `tr_do_thi` | 5 |  |  | 3/1→43 | 2/0→2! |  |
| `tr_t6_bfs` | `tr_tim_kiem` | 6 |  |  | 3/2→83 | 2/0→2! |  |
| `tr_t6_dfs` | `tr_tim_kiem` | 6 |  |  | 3/1→43 | 2/0→2! |  |
| `tr_t6_ung_dung_tim_kiem` | `tr_tim_kiem` | 6 |  |  | 3/1→43 | 1/1→41 |  |
| `tr_t6_euler` | `tr_euler_hamilton` | 6 |  |  | 4/1→44 | 2/1→42 |  |
| `tr_t6_hamilton` | `tr_euler_hamilton` | 6 |  |  | 3/1→11 | 2/1→38 |  |
| `tr_t7_cay` | `tr_cay_duong_di` | 7 |  |  |  | 3/1→41 | 2/0→2! |
| `tr_t7_cay_khung` | `tr_cay_khung_luong` | 7 |  |  |  | 3/1→43 | 2/1→33 |
| `tr_t7_kruskal_prim` | `tr_cay_khung_luong` | 7 |  |  |  | 3/1→43 | 3/2→83 |
| `tr_t7_dijkstra` | `tr_cay_duong_di` | 7 |  |  |  | 3/1→43 | 2/1→42 |
| `tr_t7_luong` | `tr_cay_khung_luong` | 7 |  |  |  | 2/1→42 | 2/1→42 |
| `tr_t8_bai_toan_toi_uu` | `tr_toi_uu_loi` | 8 |  |  |  | 3/1→41 | 2/1→19 |
| `tr_t8_tap_loi` | `tr_toi_uu_loi` | 8 |  |  |  | 3/1→41 | 2/1→42 |
| `tr_t8_ham_loi` | `tr_toi_uu_loi` | 8 |  |  |  | 3/2→83 | 2/0→2! |
| `tr_t8_dieu_kien_toi_uu` | `tr_toi_uu_loi` | 8 |  |  |  | 3/1→43 | 2/1→42 |
| `tr_t8_bai_toan_loi` | `tr_toi_uu_loi` | 8 |  |  |  | 3/1→43 | 2/1→42 |
| `tr_t9_mo_hinh_qhtt` | `tr_quy_hoach_tuyen_tinh` | 9 |  |  |  |  | 4/1→44 |
| `tr_t9_hinh_hoc` | `tr_quy_hoach_tuyen_tinh` | 9 |  |  |  |  | 4/3→124 |
| `tr_t9_don_hinh` | `tr_quy_hoach_tuyen_tinh` | 9 |  |  |  |  | 4/1→44 |
| `tr_t9_doi_ngau` | `tr_quy_hoach_tuyen_tinh` | 9 |  |  |  |  | 4/2→84 |
| `tr_t9_lagrange_kkt` | `tr_gradient_descent` | 9 |  |  |  |  | 3/2→82 |
| `tr_t9_gradient_descent` | `tr_gradient_descent` | 9 |  |  |  |  | 3/3→123 |
| `tr_t10_sai_so` | `tr_phuong_phap_tinh` | 10 |  |  |  |  | 12/3→129 |
| `tr_t10_chia_doi` | `tr_phuong_phap_tinh` | 10 |  |  |  |  | 10/2→76 |
| `tr_t10_lap_don` | `tr_phuong_phap_tinh` | 10 |  |  |  |  | 10/3→114 |
| `tr_t10_newton` | `tr_phuong_phap_tinh` | 10 |  |  |  |  | 11/2→90 |

## 4. Các ô mỏng nhất (nút chính)

72 ô có sức chứa dưới 10, xếp từ mỏng nhất. `Thứ tự` = tầng của nút.

| Vi kỹ năng | Bậc | Viết tay | Bộ sinh | Sức chứa | Nút | Tầng nút |
|---|---|---|---|---|---|---|
| `dstt_t4_khong_giao_hoan` | 2 | 2 | 0 | 2 | `ds_nhan_ma_tran` | 3 |
| `dstt_t4_tich_vo_huong` | 3 | 2 | 0 | 2 | `ds_nhan_ma_tran` | 3 |
| `tr_t3_tu_dien` | 3 | 2 | 0 | 2 | `tr_liet_ke_quay_lui` | 3 |
| `tr_t5_danh_sach_ke` | 4 | 2 | 0 | 2 | `tr_do_thi` | 4 |
| `tr_t5_duong_di_lien_thong` | 4 | 2 | 0 | 2 | `tr_do_thi` | 4 |
| `gt_t7_can_bien_thien` | 5 | 2 | 0 | 2 | `gt_tich_phan` | 5 |
| `gt_t7_doi_bien` | 5 | 2 | 0 | 2 | `gt_tich_phan` | 5 |
| `gt_t7_nguyen_ham` | 5 | 2 | 0 | 2 | `gt_tich_phan` | 5 |
| `tr_t6_bfs` | 4 | 2 | 0 | 2 | `tr_tim_kiem` | 5 |
| `tr_t6_dfs` | 4 | 2 | 0 | 2 | `tr_tim_kiem` | 5 |
| `dstt_t7_khong_gian_vecto` | 5 | 2 | 0 | 2 | `ds_khong_gian` | 6 |
| `dstt_t7_to_hop_tuyen_tinh` | 5 | 2 | 0 | 2 | `ds_khong_gian` | 6 |
| `dstt_t7_toa_do` | 5 | 2 | 0 | 2 | `ds_khong_gian` | 6 |
| `gt_t8_suy_rong_loai_1` | 5 | 2 | 0 | 2 | `gt_tich_phan_ung_dung` | 6 |
| `tr_t7_cay` | 5 | 2 | 0 | 2 | `tr_cay_duong_di` | 6 |
| `dstt_t8_doi_co_so` | 5 | 2 | 0 | 2 | `ds_anh_xa_tuyen_tinh` | 7 |
| `dstt_t8_hop_anh_xa` | 5 | 2 | 0 | 2 | `ds_anh_xa_tuyen_tinh` | 7 |
| `tr_t8_ham_loi` | 5 | 2 | 0 | 2 | `tr_toi_uu_loi` | 7 |
| `xs_t7_dac_trung_mau` | 5 | 2 | 0 | 2 | `xs_mau_uoc_luong` | 8 |
| `xs_t7_hop_ly_cuc_dai` | 5 | 2 | 0 | 2 | `xs_mau_uoc_luong` | 8 |
| `xs_t7_phan_phoi_mau` | 5 | 2 | 0 | 2 | `xs_mau_uoc_luong` | 8 |
| `xs_t7_tong_the_mau` | 5 | 2 | 0 | 2 | `xs_mau_uoc_luong` | 8 |
| `xs_t7_uoc_luong_diem` | 5 | 2 | 0 | 2 | `xs_mau_uoc_luong` | 8 |
| `xs_t8_co_mau` | 5 | 2 | 0 | 2 | `xs_tin_cay` | 9 |
| `xs_t8_gioi_han_trung_tam` | 5 | 2 | 0 | 2 | `xs_tin_cay` | 9 |
| `xs_t8_luat_so_lon` | 5 | 2 | 0 | 2 | `xs_tin_cay` | 9 |
| `xs_t8_tin_cay_trung_binh` | 5 | 2 | 0 | 2 | `xs_tin_cay` | 9 |
| `xs_t8_tin_cay_ty_le` | 5 | 2 | 0 | 2 | `xs_tin_cay` | 9 |
| `xs_t2_co_dien_to_hop` | 1 | 3 | 0 | 3 | `xs_xac_suat` | 2 |
| `xs_t2_tinh_chat` | 1 | 3 | 0 | 3 | `xs_xac_suat` | 2 |
| `dstt_t4_tinh_chat_nhan` | 2 | 3 | 0 | 3 | `ds_nhan_ma_tran` | 3 |
| `xs_t3_cong_thuc_nhan` | 3 | 3 | 0 | 3 | `xs_dieu_kien` | 3 |
| `dstt_t5_dang_ma_tran` | 4 | 3 | 0 | 3 | `ds_he_gauss` | 4 |
| `tr_t4_phat_bieu` | 2 | 3 | 0 | 3 | `tr_thuat_toan` | 4 |
| `dstt_t6_hang` | 4 | 3 | 0 | 3 | `ds_dinh_thuc_nghich_dao` | 5 |
| `gt_t7_newton_leibniz` | 5 | 3 | 0 | 3 | `gt_tich_phan` | 5 |
| `gt_t7_tung_phan` | 5 | 3 | 0 | 3 | `gt_tich_phan` | 5 |
| `xs_t5_bien_ngau_nhien` | 4 | 3 | 0 | 3 | `xs_bnn_roi_rac` | 5 |
| `xs_t5_ham_phan_phoi` | 4 | 3 | 0 | 3 | `xs_bnn_roi_rac` | 5 |
| `dstt_t7_co_so_so_chieu` | 5 | 3 | 0 | 3 | `ds_khong_gian` | 6 |
| `dstt_t7_doc_lap_tuyen_tinh` | 5 | 3 | 0 | 3 | `ds_khong_gian` | 6 |
| `dstt_t7_khong_gian_con` | 5 | 3 | 0 | 3 | `ds_khong_gian` | 6 |
| `dstt_t7_khong_gian_vecto` | 4 | 3 | 0 | 3 | `ds_khong_gian` | 6 |
| `gt_t8_dien_tich` | 5 | 3 | 0 | 3 | `gt_tich_phan_ung_dung` | 6 |
| `dstt_t8_anh_xa_tuyen_tinh` | 5 | 3 | 0 | 3 | `ds_anh_xa_tuyen_tinh` | 7 |
| `dstt_t8_dinh_ly_so_chieu` | 5 | 3 | 0 | 3 | `ds_anh_xa_tuyen_tinh` | 7 |
| `dstt_t8_ma_tran_anh_xa` | 5 | 3 | 0 | 3 | `ds_anh_xa_tuyen_tinh` | 7 |
| `dstt_t8_nhan_va_anh` | 5 | 3 | 0 | 3 | `ds_anh_xa_tuyen_tinh` | 7 |
| `xs_t1_khong_gian_mau` | 2 | 4 | 0 | 4 | `xs_dem_su_kien` | 1 |
| `xs_t1_quan_he_su_kien` | 2 | 4 | 0 | 4 | `xs_dem_su_kien` | 1 |
| `xs_t2_hoan_lai` | 1 | 4 | 0 | 4 | `xs_xac_suat` | 2 |
| `dstt_t5_bac_thang` | 3 | 4 | 0 | 4 | `ds_he_gauss` | 4 |
| `dstt_t5_bac_thang` | 4 | 4 | 0 | 4 | `ds_he_gauss` | 4 |
| `dstt_t5_bien_doi_hang` | 4 | 4 | 0 | 4 | `ds_he_gauss` | 4 |
| `xs_t4_bayes` | 2 | 4 | 0 | 4 | `xs_bayes` | 4 |
| `xs_t4_bayes_ung_dung` | 2 | 4 | 0 | 4 | `xs_bayes` | 4 |
| `xs_t4_he_day_du` | 3 | 4 | 0 | 4 | `xs_bayes` | 4 |
| `xs_t4_so_do_cay` | 3 | 4 | 0 | 4 | `xs_bayes` | 4 |
| `xs_t5_bang_phan_phoi` | 4 | 4 | 0 | 4 | `xs_bnn_roi_rac` | 5 |
| `xs_t5_bien_ngau_nhien` | 3 | 4 | 0 | 4 | `xs_bnn_roi_rac` | 5 |
| `dstt_t7_khong_gian_con` | 4 | 4 | 0 | 4 | `ds_khong_gian` | 6 |
| `xs_t5_mat_do` | 4 | 4 | 0 | 4 | `xs_bnn_lien_tuc` | 6 |
| `xs_t5_xac_suat_khoang` | 3 | 4 | 0 | 4 | `xs_bnn_lien_tuc` | 6 |
| `dstt_t8_nhan_va_anh` | 4 | 4 | 0 | 4 | `ds_anh_xa_tuyen_tinh` | 7 |
| `xs_t6_chuan` | 3 | 4 | 0 | 4 | `xs_ky_vong_phan_phoi` | 7 |
| `xs_t6_deu_mu` | 4 | 4 | 0 | 4 | `xs_ky_vong_phan_phoi` | 7 |
| `xs_t6_ky_vong` | 4 | 4 | 0 | 4 | `xs_ky_vong_phan_phoi` | 7 |
| `xs_t7_tong_the_mau` | 4 | 4 | 0 | 4 | `xs_mau_uoc_luong` | 8 |
| `dstt_t9_pca_svd` | 5 | 4 | 0 | 4 | `ds_pca_svd` | 9 |
| `dstt_t6_tinh_chat_dinh_thuc` | 4 | 5 | 0 | 5 | `ds_dinh_thuc_nghich_dao` | 5 |
| `gt_t9_gioi_han_lien_tuc` | 5 | 5 | 0 | 5 | `gt_nhieu_bien` | 6 |
| `xs_t9_so_sanh_ty_le` | 5 | 6 | 0 | 6 | `xs_kiem_dinh` | 9 |

Ô mỏng thuộc nút phụ: 8. Ô không có câu nào ở nút chính: 0.

## 5. Câu hỏi không bao giờ được hỏi

- Danh sách cắt có 11 vi kỹ năng; trong kho vẫn còn 109 câu viết tay và 17 bộ sinh câu trên các vi kỹ năng đó.
- Số vi kỹ năng cắt theo tầng: dai_so_tuyen_tinh tầng 10: 5, giai_tich tầng 10: 5, xac_suat_thong_ke tầng 10: 1
- Vi kỹ năng của nút chính chưa có câu nào: 0.
- Vi kỹ năng của nút phụ chưa có câu nào: 0.

- Nút chính Luyện Khí không có câu hỏi lẫn bài tập (tính là 'đang biên soạn', coi như xong): `lt_numpy`
- Nút các cảnh sau Luyện Khí: truc_co: 9, ket_dan: 7, nguyen_anh: 6, hoa_than: 6, luyen_hu: 6, hop_the: 6, dai_thua: 4 (tất cả `chua_co`: là thiết kế, chưa nối vào game).

- Cờ `content` = `dang_viet` nhưng nút đã có đủ câu hỏi: 38 nút (cờ này chỉ để hiển thị 'đang viết'; xem phần khuyến nghị).
- Cờ `content` lệch với thực tế theo hướng ngược lại: không có.

## 6. Điều kiện tiên quyết

- gt_gioi_han_nang_cao: needs gt_gioi_han, but gt_gioi_han has floors [2, 3] and gt_gioi_han_nang_cao [2, 3] (floor order inverted)

## 7. Khối lượng từng tầng (Luyện Khí, nút chính, không tính vi kỹ năng bị cắt)

Mỗi ô: `số nút / số vi kỹ năng / số bài tập`.

| Tầng | ds | gt | xs | tr | lt | ud | Cộng |
|---|---|---|---|---|---|---|---|
| 1 | 1/6/0 | 1/4/0 | 1/5/0 | 1/4/0 | 1/0/5 | — | 5/19/5 |
| 2 | 1/6/0 | 1/5/0 | 1/5/0 | 1/4/0 | 1/0/5 | — | 5/20/5 |
| 3 | 1/6/0 | 1/4/0 | 1/5/0 | 1/3/0 | 2/0/10 | 1/0/3 | 7/18/13 |
| 4 | 1/6/0 | 1/4/0 | 1/5/0 | 2/9/0 | 3/0/10 | — | 8/24/10 |
| 5 | 1/5/0 | 2/7/0 | 1/3/0 | 1/3/0 | 2/0/9 | 2/0/6 | 9/18/15 |
| 6 | 1/6/0 | 2/5/0 | 1/2/0 | 1/2/0 | 1/0/5 | — | 6/15/5 |
| 7 | 2/8/0 | 1/3/0 | 1/5/0 | 1/5/0 | — | 1/0/3 | 6/21/3 |
| 8 | 1/2/0 | — | 2/8/0 | 1/2/0 | — | 1/0/3 | 5/12/3 |
| 9 | 1/2/0 | — | 2/10/0 | — | — | 4/0/11 | 7/12/11 |

Số vi kỹ năng mỗi tầng: trung vị 18, thấp nhất 12, cao nhất 24. Tầng nặng (trên 1,4 lần trung vị): không. Tầng nhẹ (dưới 0,6 lần): không.

## 8. Lập trình chạy song song với toán

Với mỗi nút toán của Luyện Khí: sau bao nhiêu tầng thì có một nút code/thực chiến dùng nó trực tiếp (cần hoặc ôn lại nó), và sau bao nhiêu tầng thì có nút code/thực chiến nào ở sau nó trên đường đi. `—` = chưa có nút code nào dùng.

| Nút toán | Nhánh | Tầng | Dùng trực tiếp sau (tầng) | Dùng gián tiếp sau (tầng) |
|---|---|---|---|---|
| `ds_ngon_ngu` | ds | 1 | 1 | 1 |
| `ds_vecto_ma_tran` | ds | 2 | 1 | 1 |
| `ds_nhan_ma_tran` | ds | 3 | 1 | 1 |
| `ds_he_gauss` | ds | 4 | 0 | 0 |
| `ds_dinh_thuc_nghich_dao` | ds | 5 | — | 2 |
| `ds_khong_gian` | ds | 6 | — | 1 |
| `ds_truc_giao_chieu` | ds | 7 | 0 | 0 |
| `ds_anh_xa_tuyen_tinh` | ds | 7 | — | 2 |
| `ds_tri_rieng` | ds | 8 | 1 | 1 |
| `ds_pca_svd` | ds | 9 | 0 | 0 |
| `gt_ham_so` | gt | 1 | 8 | 4 |
| `gt_gioi_han` | gt | 2 | — | 3 |
| `gt_dao_ham` | gt | 3 | 2 | 2 |
| `gt_cuc_tri` | gt | 4 | 1 | 1 |
| `gt_taylor` | gt | 5 | — | 3 |
| `gt_tich_phan` | gt | 5 | — | 4 |
| `gt_tich_phan_ung_dung` | gt | 6 | — | 3 |
| `gt_nhieu_bien` | gt | 6 | — | 2 |
| `gt_gradient` | gt | 7 | 1 | 1 |
| `xs_dem_su_kien` | xs | 1 | — | 3 |
| `xs_xac_suat` | xs | 2 | 2 | 2 |
| `xs_dieu_kien` | xs | 3 | 1 | 1 |
| `xs_bayes` | xs | 4 | 1 | 1 |
| `xs_bnn_roi_rac` | xs | 5 | — | 4 |
| `xs_bnn_lien_tuc` | xs | 6 | — | 3 |
| `xs_ky_vong_phan_phoi` | xs | 7 | — | 2 |
| `xs_mau_uoc_luong` | xs | 8 | 1 | 1 |
| `xs_tuong_quan_hoi_quy` | xs | 8 | 1 | 1 |
| `xs_tin_cay` | xs | 9 | 0 | 0 |
| `xs_kiem_dinh` | xs | 9 | 0 | 0 |
| `tr_logic_dem` | tr | 1 | 2 | 2 |
| `tr_dem` | tr | 2 | 3 | 3 |
| `tr_liet_ke_quay_lui` | tr | 3 | — | 2 |
| `tr_thuat_toan` | tr | 4 | 1 | 1 |
| `tr_do_thi` | tr | 4 | 2 | 2 |
| `tr_tim_kiem` | tr | 5 | 1 | 1 |
| `tr_cay_duong_di` | tr | 6 | 3 | 3 |
| `tr_toi_uu_loi` | tr | 7 | — | 1 |
| `tr_gradient_descent` | tr | 8 | 0 | 0 |

25/39 nút toán có nút code/thực chiến dùng trực tiếp; độ trễ trung vị 1 tầng.

| Tầng | Nút toán | Nút code / thực chiến / dự án |
|---|---|---|
| 1 | 4 | 1 |
| 2 | 4 | 1 |
| 3 | 4 | 3 |
| 4 | 5 | 3 |
| 5 | 5 | 4 |
| 6 | 5 | 1 |
| 7 | 5 | 1 |
| 8 | 4 | 1 |
| 9 | 3 | 4 |

## 9. Liên kết giữa các nhánh và ôn tập cuốn chiếu

Số cạnh `requires` + `reinforces` đi từ nhánh hàng sang nhánh cột:

| từ \ sang | ds | gt | xs | tr | lt | ud | ml | dl | ht | nc |
|---|---|---|---|---|---|---|---|---|---|---|
| ds | · | · | · | · | · | · | · | · | · | · |
| gt | 4 | · | · | · | · | · | · | · | · | · |
| xs | 2 | 6 | · | · | · | · | · | · | · | · |
| tr | 2 | 6 | 2 | · | · | · | · | · | · | · |
| lt | 10 | 3 | 4 | 8 | · | 2 | · | · | · | · |
| ud | 8 | 5 | 10 | 5 | 15 | · | · | · | · | · |
| ml | 1 | 1 | 5 | 4 | 3 | 8 | · | · | · | · |
| dl | 4 | 1 | 3 | 1 | 3 | 3 | 6 | · | · | · |
| ht | · | · | · | 1 | 4 | 1 | 1 | 5 | · | · |
| nc | 1 | · | 1 | 1 | 1 | · | 1 | 4 | 3 | · |

Nút chính Luyện Khí không liên kết với nhánh khác (không cạnh ra, không cạnh vào): `ds_dinh_thuc_nghich_dao`, `ds_anh_xa_tuyen_tinh`, `gt_gioi_han`, `gt_taylor`, `xs_bnn_roi_rac`, `tr_liet_ke_quay_lui`, `lt_python_co_ban`

Nút chính Luyện Khí chưa nút nào ôn lại (không có trong `reinforces` của nút nào) - dễ phai:

không có.

Nguồn câu ôn của từng nút toán chính (vi kỹ năng có câu hỏi, lấy từ các nút trong `reinforces`; nếu rỗng thì lấy từ tổ tiên đã xong): `nguồn khác môn` là số vi kỹ năng thuộc môn khác.

| Nút | Số vi kỹ năng ôn | Khác môn | Dùng tổ tiên thay thế |
|---|---|---|---|
| `ds_ngon_ngu` | 0 | 0 | có |
| `ds_vecto_ma_tran` | 6 | 0 |  |
| `ds_nhan_ma_tran` | 6 | 0 |  |
| `ds_he_gauss` | 6 | 0 |  |
| `ds_dinh_thuc_nghich_dao` | 12 | 0 |  |
| `ds_khong_gian` | 11 | 0 |  |
| `ds_truc_giao_chieu` | 12 | 0 |  |
| `ds_anh_xa_tuyen_tinh` | 18 | 0 |  |
| `ds_tri_rieng` | 11 | 0 |  |
| `ds_pca_svd` | 4 | 0 |  |
| `gt_ham_so` | 0 | 0 | có |
| `gt_gioi_han` | 4 | 0 |  |
| `gt_dao_ham` | 9 | 0 |  |
| `gt_cuc_tri` | 4 | 0 |  |
| `gt_taylor` | 8 | 0 |  |
| `gt_tich_phan` | 4 | 0 |  |
| `gt_tich_phan_ung_dung` | 10 | 0 |  |
| `gt_nhieu_bien` | 12 | 6 |  |
| `gt_gradient` | 13 | 6 |  |
| `xs_dem_su_kien` | 0 | 0 | có |
| `xs_xac_suat` | 5 | 0 |  |
| `xs_dieu_kien` | 10 | 0 |  |
| `xs_bayes` | 5 | 0 |  |
| `xs_bnn_roi_rac` | 10 | 0 |  |
| `xs_bnn_lien_tuc` | 8 | 5 |  |
| `xs_ky_vong_phan_phoi` | 7 | 2 |  |
| `xs_mau_uoc_luong` | 9 | 4 |  |
| `xs_tuong_quan_hoi_quy` | 16 | 6 |  |
| `xs_tin_cay` | 10 | 0 |  |
| `xs_kiem_dinh` | 5 | 0 |  |
| `tr_logic_dem` | 0 | 0 | có |
| `tr_dem` | 9 | 5 |  |
| `tr_liet_ke_quay_lui` | 4 | 0 |  |
| `tr_thuat_toan` | 7 | 0 |  |
| `tr_do_thi` | 10 | 6 |  |
| `tr_tim_kiem` | 8 | 0 |  |
| `tr_cay_duong_di` | 7 | 0 |  |
| `tr_toi_uu_loi` | 11 | 7 |  |
| `tr_gradient_descent` | 8 | 3 |  |

Nút toán chính không có nguồn câu ôn nào (ôn tập im lặng): ['ds_ngon_ngu', 'gt_ham_so', 'xs_dem_su_kien', 'tr_logic_dem']. Nút có ít hơn 3 vi kỹ năng để ôn: không.

## 10. Tài liệu và nguồn

- Nút toán chính Luyện Khí có đủ tài liệu thư viện cho mọi vi kỹ năng: 39/39.
- Nút chính Luyện Khí chưa có nguồn đọc (sources/*.json): 0.

## 11. Nút nào trong game chạm tới

Nút chính Luyện Khí mà không quái, chiêu, kế hoạch thế giới, thành tựu, lộ trình nào nhắc tới và không có bài tập: không có.

Số nút được nhắc tới, theo nơi: chiêu: 13, monsters: 39, world_plan.lands: 4, world_plan.weapons_placed: 31.

