# Đạo Thụ — cây giáo trình và bản đồ mở khoá

> File này do `python tools/check_tree.py --doc` dựng từ `server/data/math/tree.json` và `server/data/math/world_plan.json`. Muốn đổi thì sửa hai file dữ liệu ấy rồi chạy lại, đừng sửa ở đây.

**Mục tiêu:** Trở thành người dẫn đầu ngành AI: hiểu bản chất, tự tay làm được, biết chọn việc đáng làm.

## Cách cây vận hành

- Không còn học hết môn này mới sang môn kia. Mỗi **nút** là một cụm bài nhỏ; nút mở khi các nút nó cần (kể cả của nhánh khác) đã xong, nên Đại Số, Giải Tích, Xác Suất, Thuật Toán và Lập Trình đi song song.
- Mỗi nút ghi rõ nó **ôn lại** những nút cũ nào: khoảng một phần tư số câu của nút lấy từ đó, để học cái mới mà cái cũ không mai một.
- Lên một **tầng** tu vi khi mọi nút chính đạo của tầng ấy xong — luôn gồm cả toán lẫn code.
- Chính đạo không hỏi chứng minh. Mọi câu là: hiểu khái niệm, tính được, tìm chỗ sai, hoặc viết code chạy được.
- **Bàng môn** là phần tuỳ chọn, không chặn gì. Phần **bị loại** không bao giờ được hỏi.

Trong 215 vi kỹ năng của bốn bí cảnh: **159 chính đạo**, 45 bàng môn (tuỳ chọn), 11 bị loại.

## 1. Luyện Khí — Toán nền tảng và Python: đủ để tự viết một mô hình học máy nhỏ từ con số không.

### Luyện Khí tầng 1 — mở khoá: Né Đòn, Nhặt binh khí

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Tập hợp và ánh xạ** | Toán | Đại Số Tuyến Tính | Tập hợp và phần tử, Phép toán trên tập hợp, Tích Descartes, Ánh xạ, ảnh và tạo ảnh, Đơn ánh, toàn ánh, song ánh, Ánh xạ hợp và ánh xạ ngược | — | — | đã có câu hỏi |
| **Hàm số, hàm hợp, mũ và logarit** | Toán | Giải Tích | Hàm số và tập xác định, Hàm hợp, Hàm ngược, Các hàm sơ cấp cơ bản | — | — | đã có câu hỏi |
| **Python nhập môn** | Lập trình | Lập Trình | Biến, số, chuỗi, Điều kiện if, Vòng lặp for và while, Hàm, Đọc đề, in kết quả | — | — | đã có câu hỏi |
| **Logic mệnh đề và quy tắc đếm** | Toán | Thuật Toán và Tối Ưu | Cấu hình tổ hợp, Quy tắc cộng và quy tắc nhân, Mệnh đề và các phép nối, Bảng chân trị và tương đương logic | — | — | đã có câu hỏi |
| **Sự kiện và phép đếm** | Toán | Xác Suất và Thống Kê | Phép thử và không gian mẫu, Quan hệ giữa các sự kiện, Quy tắc cộng và quy tắc nhân, Hoán vị và chỉnh hợp, Tổ hợp | — | — | đã có câu hỏi |

### Luyện Khí tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Vectơ và ma trận** | Toán | Đại Số Tuyến Tính | Vectơ trong R^n, Kích thước ma trận và phần tử a_ij, Cộng ma trận và nhân với một số, Ma trận chuyển vị A^T, Vết của ma trận vuông, Các ma trận đặc biệt | Tập hợp và ánh xạ | Tập hợp và ánh xạ | đã có câu hỏi |
| **Giới hạn và liên tục** | Toán | Giải Tích | Giới hạn của dãy số, Giới hạn hàm số tại một điểm, Giới hạn ở vô cùng và giới hạn vô cùng, Liên tục tại một điểm, Giới hạn một phía và liên tục một phía | Hàm số, hàm hợp, mũ và logarit | Hàm số, hàm hợp, mũ và logarit | đã có câu hỏi |
| **Danh sách, tập hợp và từ điển** | Lập trình | Lập Trình | list và duyệt list, set và các phép toán tập hợp, dict để đếm và tra cứu, list lồng nhau | Python nhập môn, Tập hợp và ánh xạ | Tập hợp và ánh xạ | đã có câu hỏi |
| **Đếm và hệ thức truy hồi** | Toán | Thuật Toán và Tối Ưu | Chỉnh hợp lặp và không lặp, Hoán vị và hoán vị lặp, Tổ hợp, Hệ thức truy hồi | Logic mệnh đề và quy tắc đếm, Sự kiện và phép đếm | Logic mệnh đề và quy tắc đếm, Sự kiện và phép đếm | đã có câu hỏi |
| **Xác suất** | Toán | Xác Suất và Thống Kê | Xác suất cổ điển, Xác suất cổ điển dùng tổ hợp, Lấy có hoàn lại và không hoàn lại, Tính chất của xác suất và sự kiện đối, Định nghĩa thống kê: tần suất | Sự kiện và phép đếm | Sự kiện và phép đếm | đã có câu hỏi |

### Luyện Khí tầng 3 — mở khoá: Thu phục linh thú

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Tích vô hướng và nhân ma trận** | Toán | Đại Số Tuyến Tính | Tích vô hướng: một hàng nhân một cột, Điều kiện kích thước để nhân, Nhân hai ma trận, AB != BA, Tính chất của phép nhân ma trận, Ma trận đơn vị và lũy thừa ma trận | Vectơ và ma trận | Vectơ và ma trận | đang viết |
| **Đạo hàm và quy tắc dây chuyền** | Toán | Giải Tích | Đạo hàm theo định nghĩa, Quy tắc tính đạo hàm, Quy tắc dây chuyền, Vi phân và đạo hàm cấp cao | Giới hạn và liên tục | Hàm số, hàm hợp, mũ và logarit, Giới hạn và liên tục | đang viết |
| **Hàm, đệ quy và chia nhỏ bài toán** | Lập trình | Lập Trình | Hàm gọi hàm, Đệ quy và điều kiện dừng, Giai thừa, Fibonacci, tháp số, Sinh hoán vị bằng quay lui | Python nhập môn, Logic mệnh đề và quy tắc đếm | Logic mệnh đề và quy tắc đếm | đã có câu hỏi |
| **Vectơ và ma trận bằng code** | Lập trình | Lập Trình | Vectơ là list, Tích vô hướng, độ dài, Ma trận là list của list, Chuyển vị | Danh sách, tập hợp và từ điển, Vectơ và ma trận | Vectơ và ma trận | đã có câu hỏi |
| **Liệt kê và quay lui** | Toán | Thuật Toán và Tối Ưu | Thứ tự từ điển, Phương pháp sinh, Thuật toán quay lui | Logic mệnh đề và quy tắc đếm | Logic mệnh đề và quy tắc đếm | đã có câu hỏi |
| **Mô hình đầu tiên: k láng giềng gần nhất** | Thực chiến AI | Thực Chiến AI | Khoảng cách giữa hai vectơ, Tìm k điểm gần nhất, Bỏ phiếu, Đo độ chính xác trên dữ liệu chưa thấy | Vectơ và ma trận bằng code | Vectơ và ma trận, Vectơ và ma trận bằng code | đã có câu hỏi |
| **Xác suất có điều kiện và độc lập** | Toán | Xác Suất và Thống Kê | Công thức cộng xác suất, Xác suất có điều kiện, Công thức nhân xác suất, Sự kiện độc lập, Công thức Bernoulli | Xác suất | Xác suất, Sự kiện và phép đếm | đã có câu hỏi |

### Luyện Khí tầng 4 — mở khoá: Rèn nâng phẩm

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Hệ phương trình và khử Gauss** | Toán | Đại Số Tuyến Tính | Viết hệ dưới dạng Ax = b, Ba phép biến đổi sơ cấp trên hàng, Khử Gauss về dạng bậc thang, Thế ngược tìm nghiệm, Biện luận số nghiệm, Hệ thuần nhất Ax = 0 | Tích vô hướng và nhân ma trận | Tích vô hướng và nhân ma trận | đang viết |
| **Đơn điệu, cực trị, lồi lõm** | Toán | Giải Tích | Tính đơn điệu, Cực trị, Giá trị lớn nhất và nhỏ nhất trên đoạn, Lồi, lõm và điểm uốn | Đạo hàm và quy tắc dây chuyền | Đạo hàm và quy tắc dây chuyền | đang viết |
| **Nhân ma trận và khử Gauss bằng code** | Lập trình | Lập Trình | Nhân hai ma trận, Kiểm tra kích thước, Khử Gauss, Giải hệ bằng thế ngược | Vectơ và ma trận bằng code, Hệ phương trình và khử Gauss | Tích vô hướng và nhân ma trận, Hệ phương trình và khử Gauss | đã có câu hỏi |
| **Mô phỏng xác suất** | Lập trình | Lập Trình | random và hạt giống, Ước lượng xác suất bằng tần suất, Mô phỏng bài toán rút bi, gieo xúc xắc, Kiểm lại công thức xác suất có điều kiện | Danh sách, tập hợp và từ điển, Xác suất có điều kiện và độc lập | Xác suất, Xác suất có điều kiện và độc lập | đã có câu hỏi |
| **NumPy: mảng và vector hoá** | Lập trình | Lập Trình | ndarray, shape, Cắt lát và chỉ số, Broadcasting, Phép @ và các hàm tổng hợp theo trục | Vectơ và ma trận bằng code, Tích vô hướng và nhân ma trận | Tích vô hướng và nhân ma trận, Vectơ và ma trận | chưa có |
| **Đồ thị và cách biểu diễn** | Toán | Thuật Toán và Tối Ưu | Đỉnh, cạnh và các loại đồ thị, Bậc của đỉnh và định lý bắt tay, Đường đi, chu trình và liên thông, Ma trận kề, Danh sách kề và danh sách cạnh | Logic mệnh đề và quy tắc đếm, Vectơ và ma trận | Logic mệnh đề và quy tắc đếm, Vectơ và ma trận | đang viết |
| **Duyệt, tham lam và ký hiệu O lớn** | Toán | Thuật Toán và Tối Ưu | Phát biểu bài toán tối ưu tổ hợp, Duyệt toàn bộ, Thuật toán tham lam, Ký hiệu O lớn | Đếm và hệ thức truy hồi, Liệt kê và quay lui | Đếm và hệ thức truy hồi, Liệt kê và quay lui | đang viết |
| **Xác suất đầy đủ và Bayes** | Toán | Xác Suất và Thống Kê | Hệ đầy đủ các sự kiện, Sơ đồ cây cho phép thử nhiều giai đoạn, Công thức xác suất đầy đủ, Công thức Bayes, Bayes trong xét nghiệm và phân loại | Xác suất có điều kiện và độc lập | Xác suất có điều kiện và độc lập | đang viết |

### Luyện Khí tầng 5 — mở khoá: Bày pháp trận

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Định thức, hạng và nghịch đảo** | Toán | Đại Số Tuyến Tính | Định thức cấp 2 và cấp 3, Khai triển theo hàng hoặc cột, Tính chất của định thức, Hạng của ma trận, Ma trận nghịch đảo | Hệ phương trình và khử Gauss | Hệ phương trình và khử Gauss, Tích vô hướng và nhân ma trận | đang viết |
| **Khai triển Taylor** | Toán | Giải Tích | Khai triển Taylor, Khai triển Maclaurin của các hàm cơ bản | Đạo hàm và quy tắc dây chuyền | Đạo hàm và quy tắc dây chuyền, Hàm số, hàm hợp, mũ và logarit | đang viết |
| **Tích phân** | Toán | Giải Tích | Nguyên hàm và bảng nguyên hàm, Phương pháp đổi biến, Tích phân từng phần, Tích phân xác định và công thức Newton-Leibniz, Tích phân với cận biến thiên | Đạo hàm và quy tắc dây chuyền | Đạo hàm và quy tắc dây chuyền | đang viết |
| **Đạo hàm số và hạ gradient một biến** | Lập trình | Lập Trình | Đạo hàm bằng sai phân, So với đạo hàm tính tay, Vòng lặp hạ gradient, Tốc độ học quá lớn và quá nhỏ | Danh sách, tập hợp và từ điển, Đơn điệu, cực trị, lồi lõm | Đạo hàm và quy tắc dây chuyền, Đơn điệu, cực trị, lồi lõm | đã có câu hỏi |
| **Đo độ phức tạp, tìm kiếm và sắp xếp** | Lập trình | Lập Trình | Đếm phép toán, Tìm kiếm tuyến tính và nhị phân, Sắp xếp, So thời gian chạy khi n tăng | Hàm, đệ quy và chia nhỏ bài toán, Duyệt, tham lam và ký hiệu O lớn | Duyệt, tham lam và ký hiệu O lớn, Đếm và hệ thức truy hồi | đã có câu hỏi |
| **Tìm kiếm theo chiều rộng và chiều sâu** | Toán | Thuật Toán và Tối Ưu | Tìm kiếm theo chiều rộng, Tìm kiếm theo chiều sâu, Ứng dụng của tìm kiếm | Đồ thị và cách biểu diễn, Liệt kê và quay lui | Đồ thị và cách biểu diễn, Liệt kê và quay lui | đang viết |
| **Khớp đường thẳng bằng hạ gradient** | Thực chiến AI | Thực Chiến AI | Sai số bình phương, Đạo hàm của mất mát theo hai tham số, Vòng huấn luyện, Vẽ mất mát giảm dần | Đạo hàm số và hạ gradient một biến | Đạo hàm và quy tắc dây chuyền, Đơn điệu, cực trị, lồi lõm, Đạo hàm số và hạ gradient một biến | đã có câu hỏi |
| **Lọc thư rác bằng Bayes** | Thực chiến AI | Thực Chiến AI | Đếm từ theo nhãn, Xác suất có điều kiện của từng từ, Áp dụng Bayes, Vì sao gọi là 'ngây thơ' | Xác suất đầy đủ và Bayes, Danh sách, tập hợp và từ điển | Xác suất đầy đủ và Bayes, Xác suất có điều kiện và độc lập, Danh sách, tập hợp và từ điển | đã có câu hỏi |
| **Biến ngẫu nhiên rời rạc** | Toán | Xác Suất và Thống Kê | Biến ngẫu nhiên rời rạc và liên tục, Bảng phân phối xác suất, Hàm phân phối F(x) | Xác suất có điều kiện và độc lập | Xác suất có điều kiện và độc lập, Xác suất | đang viết |

### Luyện Khí tầng 6 — mở khoá: Đạp Kiếm Lướt

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Không gian vectơ: bao tuyến tính, cơ sở, số chiều** | Toán | Đại Số Tuyến Tính | Không gian vectơ và các tiên đề, Không gian con, Tổ hợp tuyến tính và bao tuyến tính, Độc lập và phụ thuộc tuyến tính, Cơ sở và số chiều, Tọa độ và ma trận chuyển cơ sở | Định thức, hạng và nghịch đảo | Hệ phương trình và khử Gauss, Định thức, hạng và nghịch đảo | đang viết |
| **Hàm nhiều biến và đạo hàm riêng** | Toán | Giải Tích | Miền xác định, giới hạn và liên tục, Đạo hàm riêng, Vi phân toàn phần, hàm ẩn và công thức Taylor | Đạo hàm và quy tắc dây chuyền, Khai triển Taylor, Vectơ và ma trận | Đạo hàm và quy tắc dây chuyền, Khai triển Taylor, Vectơ và ma trận | đang viết |
| **Diện tích và tích phân cận vô hạn** | Toán | Giải Tích | Diện tích hình phẳng, Tích phân suy rộng cận vô hạn | Tích phân, Giới hạn và liên tục | Tích phân, Giới hạn và liên tục | đang viết |
| **Đồ thị bằng code** | Lập trình | Lập Trình | Danh sách kề bằng dict, BFS bằng hàng đợi, DFS bằng đệ quy, Đường đi ngắn nhất | Đo độ phức tạp, tìm kiếm và sắp xếp, Tìm kiếm theo chiều rộng và chiều sâu | Tìm kiếm theo chiều rộng và chiều sâu, Đồ thị và cách biểu diễn | đã có câu hỏi |
| **Cây và đường đi ngắn nhất** | Toán | Thuật Toán và Tối Ưu | Cây và tính chất của cây, Đường đi ngắn nhất | Tìm kiếm theo chiều rộng và chiều sâu, Duyệt, tham lam và ký hiệu O lớn | Tìm kiếm theo chiều rộng và chiều sâu, Duyệt, tham lam và ký hiệu O lớn | đang viết |
| **Biến ngẫu nhiên liên tục và hàm mật độ** | Toán | Xác Suất và Thống Kê | Hàm mật độ xác suất, Xác suất rơi vào một khoảng | Biến ngẫu nhiên rời rạc, Tích phân | Biến ngẫu nhiên rời rạc, Tích phân | đang viết |

### Luyện Khí tầng 7

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Ánh xạ tuyến tính và đổi cơ sở** | Toán | Đại Số Tuyến Tính | Ánh xạ tuyến tính, Nhân Ker f và ảnh Im f, Định lý số chiều, Ma trận của ánh xạ tuyến tính, Hợp ánh xạ và tích ma trận, Đổi cơ sở và ma trận đồng dạng | Không gian vectơ: bao tuyến tính, cơ sở, số chiều, Tập hợp và ánh xạ | Tập hợp và ánh xạ, Tích vô hướng và nhân ma trận, Không gian vectơ: bao tuyến tính, cơ sở, số chiều | đang viết |
| **Trực giao và phép chiếu** | Toán | Đại Số Tuyến Tính | Không gian Euclide và trực giao hóa, Phép chiếu trực giao | Không gian vectơ: bao tuyến tính, cơ sở, số chiều | Tích vô hướng và nhân ma trận, Không gian vectơ: bao tuyến tính, cơ sở, số chiều | đang viết |
| **Gradient, Jacobian và lan truyền ngược** | Toán | Giải Tích | Cực trị của hàm hai biến, Cực trị có điều kiện, Gradient, Jacobian và lan truyền ngược | Hàm nhiều biến và đạo hàm riêng, Đơn điệu, cực trị, lồi lõm, Tích vô hướng và nhân ma trận | Hàm nhiều biến và đạo hàm riêng, Đơn điệu, cực trị, lồi lõm, Tích vô hướng và nhân ma trận | đang viết |
| **Bài toán tối ưu, tập lồi và hàm lồi** | Toán | Thuật Toán và Tối Ưu | Phát biểu bài toán tối ưu, Tập lồi, Hàm lồi, Điều kiện tối ưu không ràng buộc, Bài toán tối ưu lồi | Duyệt, tham lam và ký hiệu O lớn, Đơn điệu, cực trị, lồi lõm, Hàm nhiều biến và đạo hàm riêng | Duyệt, tham lam và ký hiệu O lớn, Đơn điệu, cực trị, lồi lõm, Hàm nhiều biến và đạo hàm riêng | đang viết |
| **Bình phương tối thiểu bằng phương trình chuẩn** | Thực chiến AI | Thực Chiến AI | Viết bài toán dưới dạng Ax gần bằng b, Phương trình chuẩn, Giải bằng NumPy, So với kết quả hạ gradient | Trực giao và phép chiếu, NumPy: mảng và vector hoá, Nhân ma trận và khử Gauss bằng code, Khớp đường thẳng bằng hạ gradient | Trực giao và phép chiếu, Hệ phương trình và khử Gauss, NumPy: mảng và vector hoá | đã có câu hỏi |
| **Kỳ vọng, phương sai và các phân phối quen thuộc** | Toán | Xác Suất và Thống Kê | Kỳ vọng, Phương sai và độ lệch chuẩn, Phân phối nhị thức và Poisson, Phân phối đều và phân phối mũ, Phân phối chuẩn | Biến ngẫu nhiên liên tục và hàm mật độ, Diện tích và tích phân cận vô hạn | Biến ngẫu nhiên liên tục và hàm mật độ, Biến ngẫu nhiên rời rạc, Diện tích và tích phân cận vô hạn | đang viết |

### Luyện Khí tầng 8 — mở khoá: Cưỡi linh thú

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Giá trị riêng và chéo hoá** | Toán | Đại Số Tuyến Tính | Giá trị riêng và vectơ riêng, Chéo hóa ma trận | Ánh xạ tuyến tính và đổi cơ sở | Định thức, hạng và nghịch đảo, Ánh xạ tuyến tính và đổi cơ sở | đang viết |
| **Hạ gradient và nhân tử Lagrange** | Toán | Thuật Toán và Tối Ưu | Hạ gradient và hàm mất mát, Nhân tử Lagrange và điều kiện KKT | Bài toán tối ưu, tập lồi và hàm lồi, Gradient, Jacobian và lan truyền ngược | Bài toán tối ưu, tập lồi và hàm lồi, Gradient, Jacobian và lan truyền ngược | đang viết |
| **Mạng nơ-ron hai lớp tự viết** | Thực chiến AI | Thực Chiến AI | Lan truyền xuôi là nhân ma trận, Gradient của từng lớp bằng quy tắc dây chuyền, Kiểm gradient bằng sai phân, Huấn luyện trên bài XOR | Gradient, Jacobian và lan truyền ngược, Hạ gradient và nhân tử Lagrange, NumPy: mảng và vector hoá | Gradient, Jacobian và lan truyền ngược, Tích vô hướng và nhân ma trận, Hạ gradient và nhân tử Lagrange | đã có câu hỏi |
| **Mẫu, ước lượng và hợp lý cực đại** | Toán | Xác Suất và Thống Kê | Tổng thể và mẫu ngẫu nhiên, Trung bình mẫu và phương sai mẫu, Phân phối của trung bình mẫu, Ước lượng điểm không chệch, Ước lượng hợp lý cực đại | Kỳ vọng, phương sai và các phân phối quen thuộc, Đơn điệu, cực trị, lồi lõm | Kỳ vọng, phương sai và các phân phối quen thuộc, Đơn điệu, cực trị, lồi lõm | đang viết |
| **Hiệp phương sai, tương quan và hồi quy** | Toán | Xác Suất và Thống Kê | Vectơ ngẫu nhiên hai chiều, Hiệp phương sai và hệ số tương quan, Hồi quy tuyến tính đơn | Mẫu, ước lượng và hợp lý cực đại, Tích vô hướng và nhân ma trận | Kỳ vọng, phương sai và các phân phối quen thuộc, Xác suất có điều kiện và độc lập, Tích vô hướng và nhân ma trận | đã có câu hỏi |

### Luyện Khí tầng 9

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Dạng toàn phương, PCA và SVD** | Toán | Đại Số Tuyến Tính | Dạng toàn phương, Làm quen PCA và SVD | Giá trị riêng và chéo hoá, Trực giao và phép chiếu | Giá trị riêng và chéo hoá, Trực giao và phép chiếu | đang viết |
| **Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay** | Dự án | Thực Chiến AI | Dữ liệu ảnh là ma trận, Nén bằng PCA, Huấn luyện mạng nơ-ron tự viết, Đo độ chính xác kèm khoảng tin cậy | Mạng nơ-ron hai lớp tự viết, Hồi quy logistic, PCA: nén dữ liệu, Thí nghiệm A/B: mô hình nào thật sự tốt hơn, Bình phương tối thiểu bằng phương trình chuẩn, Lọc thư rác bằng Bayes, Mô hình đầu tiên: k láng giềng gần nhất, Đồ thị bằng code, Cây và đường đi ngắn nhất | Mạng nơ-ron hai lớp tự viết, PCA: nén dữ liệu, Thí nghiệm A/B: mô hình nào thật sự tốt hơn | đã có câu hỏi |
| **Thí nghiệm A/B: mô hình nào thật sự tốt hơn** | Thực chiến AI | Thực Chiến AI | So hai tỉ lệ đúng, Khoảng tin cậy của hiệu, Mô phỏng để thấy sai lầm loại một, Cần bao nhiêu mẫu | Kiểm định giả thuyết, Mô phỏng xác suất | Kiểm định giả thuyết, Khoảng tin cậy và định lý giới hạn trung tâm, Mô phỏng xác suất | đã có câu hỏi |
| **Hồi quy logistic** | Thực chiến AI | Thực Chiến AI | Sigmoid và xác suất, Mất mát log, Gradient của mất mát, Ngưỡng quyết định | Mẫu, ước lượng và hợp lý cực đại, Hạ gradient và nhân tử Lagrange, NumPy: mảng và vector hoá | Mẫu, ước lượng và hợp lý cực đại, Hàm số, hàm hợp, mũ và logarit, Hạ gradient và nhân tử Lagrange | đã có câu hỏi |
| **PCA: nén dữ liệu** | Thực chiến AI | Thực Chiến AI | Ma trận hiệp phương sai, Vectơ riêng lớn nhất, Chiếu dữ liệu xuống ít chiều, Giữ lại bao nhiêu phần trăm thông tin | Dạng toàn phương, PCA và SVD, Hiệp phương sai, tương quan và hồi quy, NumPy: mảng và vector hoá | Dạng toàn phương, PCA và SVD, Giá trị riêng và chéo hoá, Hiệp phương sai, tương quan và hồi quy | đã có câu hỏi |
| **Kiểm định giả thuyết** | Toán | Xác Suất và Thống Kê | Giả thuyết, mức ý nghĩa và hai loại sai lầm, Kiểm định trung bình một tổng thể, Kiểm định tỷ lệ một tổng thể, So sánh hai trung bình, So sánh hai tỷ lệ | Khoảng tin cậy và định lý giới hạn trung tâm | Khoảng tin cậy và định lý giới hạn trung tâm | đang viết |
| **Khoảng tin cậy và định lý giới hạn trung tâm** | Toán | Xác Suất và Thống Kê | Khoảng tin cậy cho trung bình, Khoảng tin cậy cho tỷ lệ, Chọn cỡ mẫu theo độ chính xác, Luật số lớn, Định lý giới hạn trung tâm | Mẫu, ước lượng và hợp lý cực đại | Mẫu, ước lượng và hợp lý cực đại, Xác suất | đang viết |

**Vì sao cần từng nút (Luyện Khí):**

- *Tập hợp và ánh xạ* — Mọi mô hình là một ánh xạ từ dữ liệu vào tới kết quả ra; hàm hợp chính là các lớp của mạng nơ-ron xếp chồng.
- *Hàm số, hàm hợp, mũ và logarit* — Hàm mất mát, sigmoid, softmax, log-likelihood: toàn là hàm mũ và logarit ghép lại.
- *Python nhập môn* — Ngôn ngữ của ngành. Học vừa đủ để viết được lời giải của chính mình ngay từ tầng 1.
- *Logic mệnh đề và quy tắc đếm* — Điều kiện if, and, or trong code là logic mệnh đề. Đếm số trường hợp là bước đầu để ước lượng một thuật toán chạy bao lâu.
- *Sự kiện và phép đếm* — Muốn nói 'mô hình đúng 95%' thì phải biết đang đếm cái gì trên cái gì.
- *Vectơ và ma trận* — Một bức ảnh, một câu văn, một khách hàng: vào máy đều thành vectơ. Một tập dữ liệu là một ma trận.
- *Giới hạn và liên tục* — Chỉ cần đủ để hiểu đạo hàm là gì và vì sao ReLU gãy ở 0. Không sa vào epsilon-delta.
- *Danh sách, tập hợp và từ điển* — Tập hợp trong toán và set trong Python là một. Viết ra bằng code là cách nhớ lâu nhất.
- *Đếm và hệ thức truy hồi* — Truy hồi là cách mô tả đệ quy và quy hoạch động: lời giải lớn dựng từ lời giải nhỏ.
- *Xác suất* — Đầu ra của một bộ phân loại là xác suất. Tần suất trên dữ liệu là cách ta ước lượng nó.
- *Tích vô hướng và nhân ma trận* — Một lớp mạng nơ-ron là một phép nhân ma trận. Tích vô hướng đo hai vectơ giống nhau đến đâu.
- *Đạo hàm và quy tắc dây chuyền* — Quy tắc dây chuyền chính là lan truyền ngược. Đây là nút quan trọng nhất của nhánh giải tích.
- *Hàm, đệ quy và chia nhỏ bài toán* — Tư duy lập trình cốt lõi: chia một việc lớn thành các việc nhỏ giống nhau.
- *Vectơ và ma trận bằng code* — Tự viết phép cộng vectơ, tích vô hướng, chuyển vị một lần, để sau này hiểu thư viện đang làm gì thay mình.
- *Liệt kê và quay lui* — Tìm kiếm có hệ thống trong một không gian lời giải: tư duy nền của mọi thuật toán tìm kiếm.
- *Mô hình đầu tiên: k láng giềng gần nhất* — Chỉ cần khoảng cách giữa hai vectơ là đã phân loại được. Mô hình học máy đầu tay, ngay ở tầng 3.
- *Xác suất có điều kiện và độc lập* — Mô hình ngôn ngữ đoán từ tiếp theo KHI BIẾT các từ trước: đó là xác suất có điều kiện.
- *Hệ phương trình và khử Gauss* — Tìm tham số khớp dữ liệu, ở dạng đơn giản nhất, là giải một hệ Ax = b.
- *Đơn điệu, cực trị, lồi lõm* — Huấn luyện mô hình là đi tìm cực tiểu. Lồi hay không lồi quyết định bài toán dễ hay khó.
- *Nhân ma trận và khử Gauss bằng code* — Ba vòng lặp lồng nhau của phép nhân ma trận là đoạn code đáng tự viết nhất của người học AI.
- *Mô phỏng xác suất* — Không chắc công thức của mình đúng? Gieo một triệu lần rồi đếm. Đây là cách người làm nghề tự kiểm tra.
- *NumPy: mảng và vector hoá* — Từ đây trở đi không viết vòng lặp cho phép toán ma trận nữa. Mọi thư viện học sâu đều theo cách nghĩ của NumPy.
- *Đồ thị và cách biểu diễn* — Mạng nơ-ron là một đồ thị tính toán; mạng xã hội, bản đồ, phân tử đều là đồ thị. Ma trận kề nối đồ thị với đại số tuyến tính.
- *Duyệt, tham lam và ký hiệu O lớn* — Biết một cách làm sẽ chạy trong một giây hay một năm trước khi viết nó.
- *Xác suất đầy đủ và Bayes* — Cập nhật niềm tin khi có bằng chứng mới. Sai lầm bỏ quên tỉ lệ nền là lỗi kinh điển khi đọc kết quả mô hình.
- *Định thức, hạng và nghịch đảo* — Hạng cho biết dữ liệu thật sự có bao nhiêu chiều; nghịch đảo và định thức cho biết một phép biến đổi có làm mất thông tin không.
- *Khai triển Taylor* — Xấp xỉ một hàm phức tạp bằng đường thẳng hoặc parabol quanh một điểm: đó là cách mọi thuật toán tối ưu nhìn hàm mất mát.
- *Tích phân* — Xác suất của biến liên tục là diện tích dưới đường cong; kỳ vọng là một tích phân.
- *Đạo hàm số và hạ gradient một biến* — Viết mười dòng code để máy tự lăn xuống đáy một hàm số: lần đầu thấy 'học' nghĩa là gì.
- *Đo độ phức tạp, tìm kiếm và sắp xếp* — Đếm số phép toán của chính đoạn code mình viết, và thấy tận mắt O(n) khác O(n^2) thế nào.
- *Tìm kiếm theo chiều rộng và chiều sâu* — Hai cách đi qua một đồ thị. Lan truyền ngược đi qua đồ thị tính toán theo thứ tự ngược của một phép duyệt.
- *Khớp đường thẳng bằng hạ gradient* — Hàm mất mát, đạo hàm, bước cập nhật: vòng huấn luyện của mọi mô hình, ở dạng nhỏ nhất.
- *Lọc thư rác bằng Bayes* — Công thức Bayes trở thành một bộ lọc thư rác chạy thật.
- *Biến ngẫu nhiên rời rạc* — Nhãn, số lần bấm, số lỗi: dữ liệu đếm được đều là biến ngẫu nhiên rời rạc.
- *Không gian vectơ: bao tuyến tính, cơ sở, số chiều* — Embedding, đặc trưng, không gian ẩn của mô hình: tất cả là không gian vectơ, và cơ sở là hệ trục để nhìn nó.
- *Hàm nhiều biến và đạo hàm riêng* — Hàm mất mát phụ thuộc hàng triệu tham số. Đạo hàm riêng cho biết từng tham số ảnh hưởng thế nào.
- *Diện tích và tích phân cận vô hạn* — Đủ để kiểm một hàm mật độ có tổng xác suất bằng 1, kể cả khi nó trải ra vô cùng như phân phối mũ hay chuẩn.
- *Đồ thị bằng code* — Cài BFS, DFS và Dijkstra một lần cho biết: cấu trúc dữ liệu chọn đúng thì thuật toán gần như tự viết ra.
- *Cây và đường đi ngắn nhất* — Cây quyết định, cây tìm kiếm, và bài toán tìm đường: các cấu trúc gặp lại suốt trong học máy.
- *Biến ngẫu nhiên liên tục và hàm mật độ* — Chiều cao, thời gian, điểm số của mô hình: muốn nói về chúng cần hàm mật độ, tức là cần tích phân.
- *Ánh xạ tuyến tính và đổi cơ sở* — Ma trận không chỉ là bảng số: nó là một phép biến hình. Hiểu điều này thì hiểu mạng nơ-ron đang bẻ không gian ra sao.
- *Trực giao và phép chiếu* — Khớp một đường thẳng vào dữ liệu chính là chiếu vuông góc lên một không gian con: gốc của bình phương tối thiểu.
- *Gradient, Jacobian và lan truyền ngược* — Gradient chỉ hướng dốc nhất. Lan truyền ngược là quy tắc dây chuyền viết bằng phép nhân ma trận.
- *Bài toán tối ưu, tập lồi và hàm lồi* — Bài toán lồi thì mọi cực tiểu địa phương là toàn cục. Biết bài toán của mình lồi hay không là biết mình có thể tin kết quả tối ưu đến đâu.
- *Bình phương tối thiểu bằng phương trình chuẩn* — Cùng bài khớp dữ liệu, giải một phát bằng đại số tuyến tính, rồi so với hạ gradient.
- *Kỳ vọng, phương sai và các phân phối quen thuộc* — Hàm mất mát là một kỳ vọng. Nhiễu trong dữ liệu thường được coi là phân phối chuẩn.
- *Giá trị riêng và chéo hoá* — Vectơ riêng là những hướng mà phép biến đổi chỉ kéo giãn chứ không xoay: chìa khoá của PCA và của việc hiểu tốc độ hội tụ.
- *Hạ gradient và nhân tử Lagrange* — Hạ gradient là thuật toán huấn luyện gần như mọi mô hình hiện nay. Lagrange là cách tối ưu khi có ràng buộc.
- *Mạng nơ-ron hai lớp tự viết* — Lan truyền ngược bằng NumPy, không thư viện học sâu. Ai tự viết được cái này thì không còn sợ học sâu.
- *Mẫu, ước lượng và hợp lý cực đại* — Huấn luyện một mô hình xác suất chính là ước lượng hợp lý cực đại: chọn tham số làm dữ liệu đã thấy trở nên dễ xảy ra nhất.
- *Hiệp phương sai, tương quan và hồi quy* — Ma trận hiệp phương sai là đầu vào của PCA; hồi quy tuyến tính là mô hình học máy đầu tiên. (Lấy từ tầng ẩn của bí cảnh Xác Suất lên chính đạo.)
- *Dạng toàn phương, PCA và SVD* — Nén dữ liệu mà giữ được nhiều thông tin nhất; ma trận xác định dương là điều kiện để một điểm là cực tiểu.
- *Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay* — Dự án độ kiếp lên Trúc Cơ: dùng mọi nhánh đã học để tự xây một bộ nhận dạng chữ số, và báo cáo kết quả cho đàng hoàng.
- *Thí nghiệm A/B: mô hình nào thật sự tốt hơn* — Kỹ năng phân biệt người làm AI nghiêm túc: không kết luận từ một lần chạy.
- *Hồi quy logistic* — Hợp lý cực đại cộng hạ gradient thành bộ phân loại dùng nhiều nhất trong thực tế, và là nơ-ron cuối của mọi mạng phân loại.
- *PCA: nén dữ liệu* — Giá trị riêng của ma trận hiệp phương sai cho biết dữ liệu trải theo hướng nào: đại số tuyến tính và thống kê gặp nhau.
- *Kiểm định giả thuyết* — Mô hình mới hơn mô hình cũ 0,5 điểm: thật, hay do may? Kiểm định là công cụ để không tự lừa mình.
- *Khoảng tin cậy và định lý giới hạn trung tâm* — Độ chính xác đo trên 200 mẫu thì tin được đến đâu? Người dẫn đầu phải trả lời được câu này trước khi công bố kết quả.

## 2. Trúc Cơ — Công cụ dữ liệu và học máy nền tảng.

Vừa độ kiếp lên Trúc Cơ là mở khoá: **Ngự Kiếm Phi Hành**.

### Trúc Cơ tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Dữ liệu bảng và trực quan hoá** | Lập trình | Lập Trình | pandas, Làm sạch dữ liệu thiếu và sai, Vẽ phân phối và tương quan, Đặt câu hỏi cho dữ liệu | Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay | NumPy: mảng và vector hoá, Kỳ vọng, phương sai và các phân phối quen thuộc | chưa có |
| **Python cho dự án thật** | Lập trình | Lập Trình | Lớp và đối tượng, Module và gói, Xử lý lỗi, Viết test | Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay | Hàm, đệ quy và chia nhỏ bài toán | chưa có |
| **Học có giám sát: tập huấn luyện, kiểm định, kiểm tra** | Học máy | Học Máy | Bài toán học từ ví dụ, Chia train / validation / test, Quá khớp và chưa khớp, Rò rỉ dữ liệu | Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay | Mô hình đầu tiên: k láng giềng gần nhất, Khoảng tin cậy và định lý giới hạn trung tâm | chưa có |

### Trúc Cơ tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Cây quyết định** | Học máy | Học Máy | Chia theo đặc trưng, Độ thuần của nút, Cắt tỉa, Vì sao cây dễ quá khớp | Học có giám sát: tập huấn luyện, kiểm định, kiểm tra | Cây và đường đi ngắn nhất, Duyệt, tham lam và ký hiệu O lớn | chưa có |
| **Hồi quy tuyến tính và chính quy hoá** | Học máy | Học Máy | Hồi quy nhiều biến, Ridge và Lasso, Chuẩn hoá đặc trưng, Đọc hệ số | Học có giám sát: tập huấn luyện, kiểm định, kiểm tra, Dữ liệu bảng và trực quan hoá | Bình phương tối thiểu bằng phương trình chuẩn, Hiệp phương sai, tương quan và hồi quy | chưa có |
| **Phân loại và cách đo** | Học máy | Học Máy | Logistic và softmax, Ma trận nhầm lẫn, Precision, recall, F1, ROC và chọn ngưỡng | Học có giám sát: tập huấn luyện, kiểm định, kiểm tra | Hồi quy logistic, Xác suất đầy đủ và Bayes | chưa có |

### Trúc Cơ tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Git và thí nghiệm tái lập được** | Lập trình | Lập Trình | Git cơ bản, Môi trường và phiên bản thư viện, Cố định hạt giống ngẫu nhiên, Ghi nhật ký thí nghiệm | Python cho dự án thật | Mô phỏng xác suất | chưa có |
| **Thiên kiếp Trúc Cơ: một bài toán dữ liệu bảng từ đầu đến cuối** | Dự án | Học Máy | Hiểu bài toán, Mô hình nền, Cải tiến có kiểm soát, Báo cáo | Đánh giá mô hình cho đáng tin, Cây quyết định, Git và thí nghiệm tái lập được | Đánh giá mô hình cho đáng tin | chưa có |
| **Đánh giá mô hình cho đáng tin** | Học máy | Học Máy | Kiểm định chéo, Thiên lệch và phương sai, Đường cong học, So hai mô hình bằng kiểm định | Hồi quy tuyến tính và chính quy hoá, Phân loại và cách đo | Thí nghiệm A/B: mô hình nào thật sự tốt hơn, Kiểm định giả thuyết | chưa có |

## 3. Kết Đan — Học máy cổ điển cho thành thạo, lý thuyết thông tin, tối ưu cho học máy.

Vừa độ kiếp lên Kết Đan là mở khoá: **Bản Mệnh Pháp Bảo**.

### Kết Đan tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Rừng ngẫu nhiên và boosting** | Học máy | Học Máy | Bagging, Rừng ngẫu nhiên, Gradient boosting, Tầm quan trọng của đặc trưng | Thiên kiếp Trúc Cơ: một bài toán dữ liệu bảng từ đầu đến cuối | Cây quyết định, Đánh giá mô hình cho đáng tin | chưa có |
| **Entropy, cross-entropy và KL** | Học máy | Học Máy | Entropy, Cross-entropy, Phân kỳ KL, Liên hệ với hợp lý cực đại | Thiên kiếp Trúc Cơ: một bài toán dữ liệu bảng từ đầu đến cuối | Mẫu, ước lượng và hợp lý cực đại, Hàm số, hàm hợp, mũ và logarit | chưa có |

### Kết Đan tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Kỹ nghệ đặc trưng và dữ liệu khó** | Học máy | Học Máy | Mã hoá biến phân loại, Dữ liệu mất cân bằng, Dữ liệu thiếu, Nhiễu nhãn | Rừng ngẫu nhiên và boosting | Dữ liệu bảng và trực quan hoá, Phân loại và cách đo | chưa có |
| **Học không giám sát** | Học máy | Học Máy | k-means, PCA trong thực hành, Giảm chiều để nhìn dữ liệu, Phát hiện bất thường | Rừng ngẫu nhiên và boosting | PCA: nén dữ liệu, Mô hình đầu tiên: k láng giềng gần nhất | chưa có |
| **Tối ưu cho học máy: SGD, momentum, Adam** | Học máy | Học Máy | Hạ gradient ngẫu nhiên, Momentum, Adam, Lịch tốc độ học | Entropy, cross-entropy và KL | Hạ gradient và nhân tử Lagrange, Mạng nơ-ron hai lớp tự viết | chưa có |

### Kết Đan tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Thiên kiếp Kết Đan: một cuộc thi dữ liệu** | Dự án | Học Máy | Mô hình nền nhanh, Kiểm định chéo đáng tin, Kết hợp mô hình, Viết lại bài học | Lề và kernel, Học không giám sát, Kỹ nghệ đặc trưng và dữ liệu khó | Rừng ngẫu nhiên và boosting | chưa có |
| **Lề và kernel** | Học máy | Học Máy | Lề phân cách, Vectơ hỗ trợ, Mẹo kernel, Khi nào dùng | Tối ưu cho học máy: SGD, momentum, Adam | Hạ gradient và nhân tử Lagrange, Trực giao và phép chiếu | chưa có |

## 4. Nguyên Anh — Học sâu: tự viết lan truyền ngược, PyTorch, mạng tích chập.

Vừa độ kiếp lên Nguyên Anh là mở khoá: **Nguyên Anh Xuất Khiếu**.

### Nguyên Anh tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Tự viết autograd** | Học sâu | Học Sâu | Đồ thị tính toán, Lan truyền ngược tổng quát, Mạng nhiều lớp, Kiểm gradient | Thiên kiếp Kết Đan: một cuộc thi dữ liệu | Mạng nơ-ron hai lớp tự viết, Tìm kiếm theo chiều rộng và chiều sâu, Gradient, Jacobian và lan truyền ngược | chưa có |
| **PyTorch** | Học sâu | Học Sâu | Tensor, Module và tham số, Dataset và DataLoader, Vòng huấn luyện chuẩn | Tự viết autograd | NumPy: mảng và vector hoá, Python cho dự án thật | chưa có |

### Nguyên Anh tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Mạng tích chập** | Học sâu | Học Sâu | Phép tích chập, Pooling, Kết nối tắt, Học chuyển giao | PyTorch | Tích vô hướng và nhân ma trận, Tự viết autograd | chưa có |
| **Nghề huấn luyện mạng** | Học sâu | Học Sâu | Khởi tạo trọng số, Chuẩn hoá theo lô và theo lớp, Dropout và weight decay, Đọc đường mất mát để gỡ lỗi | PyTorch | Tối ưu cho học máy: SGD, momentum, Adam, Kỳ vọng, phương sai và các phân phối quen thuộc | chưa có |

### Nguyên Anh tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Thiên kiếp Nguyên Anh: một mô hình ảnh huấn luyện tử tế** | Dự án | Học Sâu | Mô hình nền, Thí nghiệm loại bỏ từng phần, Phân tích lỗi, Báo cáo | Mạng tích chập, Embedding và mô hình chuỗi | Đánh giá mô hình cho đáng tin, Nghề huấn luyện mạng | chưa có |
| **Embedding và mô hình chuỗi** | Học sâu | Học Sâu | Embedding, Mạng hồi quy ở mức ý tưởng, Mô hình ngôn ngữ đơn giản, Vì sao cần attention | Nghề huấn luyện mạng | Xác suất có điều kiện và độc lập, Không gian vectơ: bao tuyến tính, cơ sở, số chiều, Entropy, cross-entropy và KL | chưa có |

## 5. Hóa Thần — Transformer và mô hình ngôn ngữ lớn.

Vừa độ kiếp lên Hóa Thần là mở khoá: **Thuấn Di**.

### Hóa Thần tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Attention và Transformer** | Học sâu | Học Sâu | Tự chú ý là tích vô hướng, Nhiều đầu, Mã hoá vị trí, Khối Transformer | Thiên kiếp Nguyên Anh: một mô hình ảnh huấn luyện tử tế | Tích vô hướng và nhân ma trận, Embedding và mô hình chuỗi | chưa có |
| **Tự xây một mô hình ngôn ngữ nhỏ** | Học sâu | Học Sâu | Tách token, Huấn luyện dự đoán token kế tiếp, Lấy mẫu, Đo perplexity | Attention và Transformer | Entropy, cross-entropy và KL, PyTorch | chưa có |

### Hóa Thần tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Tiền huấn luyện và tinh chỉnh** | Học sâu | Học Sâu | Tiền huấn luyện, Tinh chỉnh toàn phần, Tinh chỉnh hạng thấp, Khi nào cần, khi nào không | Tự xây một mô hình ngôn ngữ nhỏ | Dạng toàn phương, PCA và SVD, Nghề huấn luyện mạng | chưa có |
| **Dựng ứng dụng với mô hình ngôn ngữ lớn** | Học sâu | Học Sâu | Viết lời nhắc, Truy xuất tăng cường, Gọi công cụ, Tác tử nhiều bước | Tự xây một mô hình ngôn ngữ nhỏ | Mô hình đầu tiên: k láng giềng gần nhất, Python cho dự án thật | chưa có |

### Hóa Thần tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Thiên kiếp Hóa Thần: một sản phẩm dùng mô hình ngôn ngữ** | Dự án | Học Sâu | Chọn bài toán, Bản mẫu, Bộ đánh giá, Lặp theo số liệu | Đánh giá mô hình sinh | Dựng ứng dụng với mô hình ngôn ngữ lớn | chưa có |
| **Đánh giá mô hình sinh** | Học sâu | Học Sâu | Thiết kế bộ đánh giá, Chấm tự động và chấm bằng người, Ý nghĩa thống kê, Các bẫy thường gặp | Tiền huấn luyện và tinh chỉnh, Dựng ứng dụng với mô hình ngôn ngữ lớn | Thí nghiệm A/B: mô hình nào thật sự tốt hơn, Kiểm định giả thuyết, Đánh giá mô hình cho đáng tin | chưa có |

## 6. Luyện Hư — Hệ thống: đưa mô hình ra dùng thật, ở quy mô lớn.

Vừa độ kiếp lên Luyện Hư là mở khoá: **Xé Hư Không**.

### Luyện Hư tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Đường ống dữ liệu** | Hệ thống | Hệ Thống | SQL, Đường ống xử lý, Kiểm soát chất lượng dữ liệu, Phiên bản hoá dữ liệu | Thiên kiếp Hóa Thần: một sản phẩm dùng mô hình ngôn ngữ | Dữ liệu bảng và trực quan hoá, Kỹ nghệ đặc trưng và dữ liệu khó | chưa có |
| **Kỹ thuật phần mềm cho học máy** | Hệ thống | Hệ Thống | Thiết kế mô-đun, Kiểm thử cho code học máy, Duyệt code, Tài liệu | Thiên kiếp Hóa Thần: một sản phẩm dùng mô hình ngôn ngữ | Git và thí nghiệm tái lập được, Python cho dự án thật | chưa có |

### Luyện Hư tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Huấn luyện ở quy mô lớn** | Hệ thống | Hệ Thống | GPU và bộ nhớ, Độ chính xác hỗn hợp, Huấn luyện nhiều GPU, Đo và tìm nút thắt | Kỹ thuật phần mềm cho học máy | Nghề huấn luyện mạng, Đo độ phức tạp, tìm kiếm và sắp xếp | chưa có |
| **Triển khai và phục vụ mô hình** | Hệ thống | Hệ Thống | Phục vụ qua API, Lượng tử hoá và chưng cất, Độ trễ và chi phí, Triển khai an toàn | Kỹ thuật phần mềm cho học máy, Đường ống dữ liệu | Dựng ứng dụng với mô hình ngôn ngữ lớn, Duyệt, tham lam và ký hiệu O lớn | chưa có |

### Luyện Hư tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Thiên kiếp Luyện Hư: vận hành một hệ thống học máy** | Dự án | Hệ Thống | Thiết kế hệ thống, Triển khai, Giám sát, Bài học sau sự cố | Giám sát và thí nghiệm trực tuyến, Huấn luyện ở quy mô lớn | Triển khai và phục vụ mô hình | chưa có |
| **Giám sát và thí nghiệm trực tuyến** | Hệ thống | Hệ Thống | Trôi dữ liệu, Chỉ số giám sát, Thí nghiệm A/B trực tuyến, Vòng phản hồi | Triển khai và phục vụ mô hình | Thí nghiệm A/B: mô hình nào thật sự tốt hơn, Đánh giá mô hình sinh | chưa có |

## 7. Hợp Thể — Nghiên cứu: đọc, tái lập và cải tiến công trình của người khác.

Vừa độ kiếp lên Hợp Thể là mở khoá: **Nhân Thú Hợp Thể**.

### Hợp Thể tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Đọc bài báo** | Nghiên cứu | Nghiên Cứu và Dẫn Dắt | Đọc ba lượt, Tìm đóng góp thật, Soi phần thí nghiệm, Ghi chú để dùng lại | Thiên kiếp Luyện Hư: vận hành một hệ thống học máy | Đánh giá mô hình sinh, Đánh giá mô hình cho đáng tin | chưa có |
| **Tái lập một công trình** | Nghiên cứu | Nghiên Cứu và Dẫn Dắt | Chọn bài vừa sức, Cài lại từ mô tả, So với kết quả gốc, Giải thích chỗ lệch | Đọc bài báo | Nghề huấn luyện mạng, Git và thí nghiệm tái lập được | chưa có |

### Hợp Thể tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **An toàn, độ bền và diễn giải mô hình** | Nghiên cứu | Nghiên Cứu và Dẫn Dắt | Các kiểu thất bại của mô hình, Độ bền trước đầu vào lạ, Nhìn vào bên trong mô hình, Đánh giá rủi ro | Tái lập một công trình | Đánh giá mô hình sinh, Không gian vectơ: bao tuyến tính, cơ sở, số chiều | chưa có |
| **Học tăng cường và tác tử** | Nghiên cứu | Nghiên Cứu và Dẫn Dắt | Phần thưởng và chính sách, Hàm giá trị, Gradient chính sách, Tác tử dùng mô hình ngôn ngữ | Tái lập một công trình | Kỳ vọng, phương sai và các phân phối quen thuộc, Cây và đường đi ngắn nhất, Dựng ứng dụng với mô hình ngôn ngữ lớn | chưa có |

### Hợp Thể tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Thiên kiếp Hợp Thể: một đóng góp công khai** | Dự án | Nghiên Cứu và Dẫn Dắt | Chọn câu hỏi, Thí nghiệm, Viết, Công bố | Viết và trình bày kỹ thuật | Tái lập một công trình | chưa có |
| **Viết và trình bày kỹ thuật** | Nghiên cứu | Nghiên Cứu và Dẫn Dắt | Viết rõ một ý, Hình và bảng, Trình bày trước người khác, Nhận và cho phản biện | Học tăng cường và tác tử, An toàn, độ bền và diễn giải mô hình | Đọc bài báo | chưa có |

## 8. Đại Thừa — Dẫn đầu: chọn bài toán, dẫn dắt đội, tạo ra thứ người khác dùng.

Vừa độ kiếp lên Đại Thừa là mở khoá: **Khai Tông Lập Phái**.

### Đại Thừa tầng 1

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Chọn bài toán đáng làm** | Dẫn dắt | Nghiên Cứu và Dẫn Dắt | Bài toán quan trọng và làm được, Đặt cược có tính toán, Biết dừng đúng lúc, Học từ người đi trước | Thiên kiếp Hợp Thể: một đóng góp công khai | Đọc bài báo | chưa có |

### Đại Thừa tầng 2

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Chiến lược sản phẩm và trách nhiệm** | Dẫn dắt | Nghiên Cứu và Dẫn Dắt | Kinh tế của mô hình, Từ nghiên cứu ra sản phẩm, Đạo đức và chính sách, Nhìn xa năm năm | Chọn bài toán đáng làm | An toàn, độ bền và diễn giải mô hình, Triển khai và phục vụ mô hình | chưa có |
| **Dẫn dắt một đội** | Dẫn dắt | Nghiên Cứu và Dẫn Dắt | Đặt mục tiêu rõ, Kèm cặp, Ra quyết định khi thiếu thông tin, Văn hoá kỹ thuật | Chọn bài toán đáng làm | Viết và trình bày kỹ thuật, Kỹ thuật phần mềm cho học máy | chưa có |

### Đại Thừa tầng 3

| Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |
|---|---|---|---|---|---|---|
| **Phi thăng: công trình của riêng mình** | Dự án | Nghiên Cứu và Dẫn Dắt | Tầm nhìn, Đội, Thực thi, Truyền lại cho người sau | Dẫn dắt một đội, Chiến lược sản phẩm và trách nhiệm | Chọn bài toán đáng làm | chưa có |

## Bàng môn (tuỳ chọn, không chặn tu vi)

| Nút | Gồm | Vì sao để ngoài chính đạo |
|---|---|---|
| Số phức | Dạng đại số của số phức, Cộng, trừ, nhân số phức, Số phức liên hợp và môđun, Chia số phức, Dạng lượng giác và công thức Moivre, Căn bậc n của số phức | Không cần cho học máy cơ bản. Chỉ gặp lại ở xử lý tín hiệu và biến đổi Fourier. |
| Quy tắc Cramer | Giải hệ bằng nghịch đảo và quy tắc Cramer | Mẹo tính tay của phòng thi; ngoài đời không ai giải hệ bằng cách này. |
| Hàm chẵn, lẻ, tuần hoàn | Hàm chẵn, hàm lẻ, hàm tuần hoàn | Hữu ích khi vẽ đồ thị bằng tay, không cần cho học máy. |
| Kỹ thuật tính giới hạn và phân loại gián đoạn | Hai giới hạn đáng nhớ, Vô cùng bé, vô cùng lớn và tương đương, Tìm tham số để hàm liên tục, Phân loại điểm gián đoạn, Hàm liên tục trên đoạn và giá trị trung gian | Vô cùng bé tương đương, tìm tham số để liên tục, phân loại điểm gián đoạn: bài tập phòng thi. |
| Đạo hàm hàm ngược và hàm tham số | Đạo hàm của hàm ngược và hàm cho bởi tham số | Hiếm khi cần. |
| Định lý giá trị trung bình và L'Hospital | Định lý Rolle, Lagrange và Cauchy, Quy tắc L'Hospital, Các dạng vô định khác | Các định lý nền và mẹo khử dạng vô định: đẹp, nhưng không nằm trên đường tới AI. |
| Tiệm cận và lược đồ khảo sát hàm số | Tiệm cận, Lược đồ khảo sát hàm số | Vẽ đồ thị bằng tay theo lược đồ. Máy vẽ giúp được. |
| Tích phân hàm hữu tỉ và lượng giác | Tích phân hàm hữu tỉ và lượng giác | Kỹ thuật tính tay nặng mẹo. |
| Thể tích, độ dài cung và tiêu chuẩn hội tụ | Thể tích vật thể tròn xoay, Độ dài đường cong, Tích phân suy rộng của hàm không bị chặn, Tiêu chuẩn hội tụ | Ứng dụng hình học và lý thuyết hội tụ của tích phân suy rộng. |
| Hàm của biến ngẫu nhiên | Hàm của biến ngẫu nhiên | Cần khi đi sâu vào mô hình sinh; chưa cần ở Luyện Khí. |
| Chứng minh bằng quy nạp | Chứng minh bằng quy nạp | Là chứng minh. Ý tưởng 'từ n suy ra n+1' đã có trong nút đệ quy của nhánh Lập Trình. |
| Tổ hợp lặp và nguyên lý bù trừ | Tổ hợp lặp và nghiệm nguyên, Nguyên lý bù trừ | Đếm nâng cao, ít dùng trong học máy. |
| Dirichlet, bất biến và thứ hạng cấu hình | Nguyên lý Dirichlet, Chẵn lẻ và bất biến, Thứ hạng của cấu hình | Toán thi đấu. |
| Nhánh cận | Thuật toán nhánh cận | Kỹ thuật tối ưu tổ hợp chuyên biệt. |
| Đồ thị Euler và Hamilton | Đồ thị Euler, Đồ thị Hamilton | Kinh điển của lý thuyết đồ thị, không cần cho AI. |
| Cây khung và luồng cực đại | Cây khung và liệt kê cây, Cây khung nhỏ nhất, Luồng cực đại | Thuật toán đồ thị nâng cao. |
| Quy hoạch tuyến tính và đơn hình | Mô hình quy hoạch tuyến tính, Phương pháp hình học hai biến, Phương pháp đơn hình, Bài toán đối ngẫu | Tối ưu của ngành vận trù. Học máy dùng hạ gradient, không dùng đơn hình. |
| Phương pháp tính | Sai số và chữ số đáng tin, Phương pháp chia đôi, Phương pháp lặp đơn, Phương pháp Newton | Sai số, chia đôi, lặp đơn, Newton: hay, nhưng để sau. |

## Bị loại khỏi lộ trình

Bị loại khỏi lộ trình: nội dung hệ tài năng, thiên về chứng minh và cấu trúc trừu tượng. Câu hỏi (nếu có) vẫn nằm trong kho, không ai bị hỏi.

- Quan hệ hai ngôi
- Phép toán hai ngôi
- Nhóm và nhóm con
- Vành và trường
- Dạng tuyến tính và song tuyến tính
- Tiên đề của tập số thực
- Giới hạn trên và giới hạn dưới
- Điều kiện khả tích Riemann
- Hàm lồi
- Không gian metric và không gian định chuẩn
- Tiên đề xác suất

## Tiên quyết được bỏ

- *Tính đơn điệu* không còn cần *Định lý Rolle, Lagrange và Cauchy*: Chỉ cần quy tắc: f' > 0 thì hàm tăng. Định lý Lagrange đứng sau quy tắc ấy là phần chứng minh.
- *Hệ thức truy hồi* không còn cần *Chứng minh bằng quy nạp*: Lập và giải hệ thức truy hồi không cần chứng minh quy nạp.
- *Cây và tính chất của cây* không còn cần *Chứng minh bằng quy nạp*: Dùng các tính chất của cây, không chứng minh chúng.

## Tài liệu nên đọc kèm (chọn loại dễ hiểu nhất)

- **Đại Số Tuyến Tính:** 3Blue1Brown - Essence of Linear Algebra (video); Gilbert Strang - Introduction to Linear Algebra; Deisenroth, Faisal, Ong - Mathematics for Machine Learning, phần đại số tuyến tính
- **Giải Tích:** 3Blue1Brown - Essence of Calculus (video); Deisenroth, Faisal, Ong - Mathematics for Machine Learning, chương Vector Calculus
- **Xác Suất và Thống Kê:** Seeing Theory (Đại học Brown, trang trực quan); Blitzstein, Hwang - Introduction to Probability; Allen Downey - Think Stats
- **Thuật Toán và Tối Ưu:** Aditya Bhargava - Grokking Algorithms; Deisenroth, Faisal, Ong - Mathematics for Machine Learning, chương Continuous Optimization
- **Lập Trình:** Eric Matthes - Python Crash Course; CS50's Introduction to Programming with Python; NumPy: the absolute basics for beginners
- **Thực Chiến AI:** Vũ Hữu Tiệp - Machine Learning cơ bản (tiếng Việt); Joel Grus - Data Science from Scratch
- **Học Máy:** Andrew Ng - Machine Learning Specialization; Aurélien Géron - Hands-On Machine Learning; James, Witten, Hastie, Tibshirani - An Introduction to Statistical Learning
- **Học Sâu:** Andrej Karpathy - Neural Networks: Zero to Hero (video); Đắm mình vào học sâu (bản dịch tiếng Việt của Dive into Deep Learning); Jay Alammar - The Illustrated Transformer
- **Hệ Thống:** Chip Huyen - Designing Machine Learning Systems; Full Stack Deep Learning
- **Nghiên Cứu và Dẫn Dắt:** Richard Hamming - You and Your Research; S. Keshav - How to Read a Paper; Andrej Karpathy - A Recipe for Training Neural Networks

# Thiên Địa Đồ — tu vi mở khoá gì

## Luật đánh quái mới

- Người chơi đánh thường và dùng chiêu thức tự do, không phải trả lời câu hỏi để ra đòn.
- Quái ra đòn có báo trước: vùng đánh (hình tròn, hình quạt hoặc đường thẳng) hiện trên mặt đất và đầy dần trong thời gian 'windup'.
- Né ra khỏi vùng đánh trước khi nó đầy: không mất máu, không có câu hỏi.
- Bị đánh trúng: thế giới dừng lại và một câu hỏi hiện ra (đúng vi kỹ năng mà con quái ấy đại diện).
- Trả lời đúng = Phản Đòn: không mất máu, quái choáng và nhận đòn phản, người chơi được tu vi và linh lực.
- Trả lời sai hoặc hết giờ = trúng đòn: mất máu, và xem lời giải.
- Sau mỗi câu hỏi có thời gian nghỉ; trong lúc ấy đòn trúng chỉ gây nửa sát thương và không hỏi.
- Quái thường có thể hạ bằng đòn thường, nhưng tu vi chủ yếu đến từ Phản Đòn. Khiên của tinh anh và trùm chỉ vỡ khi Phản Đòn.

## Mở khoá theo tu vi

| Tu vi | Mở khoá | Là gì |
|---|---|---|
| Luyện Khí tầng 1 | **Né Đòn** | Lướt nhanh ra khỏi vùng đánh của quái. |
| Luyện Khí tầng 1 | **Nhặt binh khí** | Nhặt và dùng vũ khí nằm rải rác ở các vùng đất, nếu đủ yêu cầu. |
| Luyện Khí tầng 3 | **Thu phục linh thú** | Dùng Phong Ấn Phù để thu linh thú đã chịu phục. |
| Luyện Khí tầng 4 | **Rèn nâng phẩm** | Lò rèn nâng vũ khí từ hạ phẩm lên trung phẩm. |
| Luyện Khí tầng 5 | **Bày pháp trận** | Đặt một pháp trận trên mặt đất: quái trong trận ra đòn chậm lại, dễ né và dễ Phản Đòn hơn. |
| Luyện Khí tầng 6 | **Đạp Kiếm Lướt** | Đứng trên kiếm lướt một quãng ngắn qua vực và mặt nước: tới được các vùng cao. |
| Luyện Khí tầng 8 | **Cưỡi linh thú** | Cưỡi linh thú đã thu phục để đi nhanh. |
| Vừa lên Trúc Cơ | **Ngự Kiếm Phi Hành** | Bay tự do trên kiếm. Mở Vân Hải Thiên Đảo và mọi nơi trước đây không tới được. |
| Vừa lên Kết Đan | **Bản Mệnh Pháp Bảo** | Luyện một vũ khí thành bản mệnh: nó lớn lên cùng chủ. |
| Vừa lên Nguyên Anh | **Nguyên Anh Xuất Khiếu** | Thả một phân thân đánh cùng mình. |
| Vừa lên Hóa Thần | **Thuấn Di** | Dịch chuyển tức thời giữa các vùng đất đã tới. |
| Vừa lên Luyện Hư | **Xé Hư Không** | Mở khe nứt vào bí cảnh ở bất cứ đâu. |
| Vừa lên Hợp Thể | **Nhân Thú Hợp Thể** | Hợp thể với linh thú thành hình thái chiến đấu. |
| Vừa lên Đại Thừa | **Khai Tông Lập Phái** | Lập tông môn của riêng mình và truyền lại cho người sau. |

## Vùng đất, và binh khí riêng của từng vùng

| Vùng đất | Nhánh giáo trình | Binh khí | Kỳ binh (chỉ rơi từ tinh anh, trùm) | Mô tả |
|---|---|---|---|---|
| **Trúc Lâm Thôn** | — | — | — | Thôn tre: nơi bắt đầu, có Tàng Thư Các, lò rèn và động phủ. |
| **Kiếm Trủng Sơn** | Đại Số Tuyến Tính | Kiếm | Kích | Núi mộ kiếm: kiếm gãy cắm đầy sườn đá. Quái: Kiếm Linh, Thạch Khôi; tinh anh: Ma Trận Thú. |
| **Lưu Vân Cốc** | Giải Tích | Đao | Roi | Thung lũng mây trôi: suối uốn lượn, gió không ngừng. Quái: Vân Xà; tinh anh: Phong Lang. |
| **Vạn Tượng Trạch** | Xác Suất và Thống Kê | Hồ Lô | Ám Khí | Đầm vạn tượng: sương mù, mỗi bước một điều chưa chắc. Quái: Đầu Tử Oa; tinh anh: Hồ Lô Tinh. |
| **Mê Đồ Lâm** | Thuật Toán và Tối Ưu | Thương | Luân | Rừng mê cung: lối đi chằng chịt như một đồ thị. Quái: Tri Chu Tinh; tinh anh: Mộc Yêu. |
| **Thiên Công Phường** | Lập Trình | Chùy | Phủ | Phường thợ bỏ hoang: lò rèn, bánh răng và những cơ quan nhân còn chạy. Quái: Cơ Quan Nhân; tinh anh: Cơ Quan Nhân Đầu Đàn. |
| **Linh Xạ Nguyên** | Thực Chiến AI | Cung | Cầm | Thảo nguyên bia bắn: nơi luyện Thực Chiến AI. Quái: Tâm Ma của chính mình; tinh anh: Tâm Ma Chấp Niệm. |
| **Lôi Kiếp Đài** | — | — | — | Đài độ kiếp: nơi đối mặt Thiên Kiếp Lôi Long để lên Trúc Cơ. |
| **Vân Hải Thiên Đảo** | Học Máy | Trượng | — | Quần đảo trên biển mây: chỉ tới được bằng ngự kiếm phi hành. |

- **Kiếm** (Đại Số Tuyến Tính): Vectơ là mũi tên thẳng: kiếm là binh khí của Đại Số Tuyến Tính.
- **Đao** (Giải Tích): Lưỡi đao là một đường cong: binh khí của Giải Tích.
- **Hồ Lô** (Xác Suất và Thống Kê): Rút bi từ trong bình: binh khí của Xác Suất.
- **Thương** (Thuật Toán và Tối Ưu): Đi thẳng tới đích theo đường ngắn nhất: binh khí của Thuật Toán và Tối Ưu.
- **Chùy** (Lập Trình): Búa của thợ rèn: lập trình là tự tay rèn ra công cụ.
- **Cung** (Thực Chiến AI): Nhắm vào đích và chỉnh dần cho trúng: đó chính là huấn luyện một mô hình.
- **Trượng** (Học Máy): Pháp trượng của người điều khiển mô hình, từ Trúc Cơ.
- **Phiến** (Học Sâu): Quạt nhiều nan xếp lớp như mạng nhiều tầng, từ Nguyên Anh.
- **Kích** (Đại Số Tuyến Tính) *(chờ hình vẽ)*: Cán dài cộng lưỡi sắc, mỗi phần một hệ số: kích là tổ hợp tuyến tính, binh khí của Đại Số Tuyến Tính.
- **Roi** (Giải Tích) *(chờ hình vẽ)*: Sợi roi quất ra vẽ một đường cong liền mạch: binh khí của Giải Tích.
- **Ám Khí** (Xác Suất và Thống Kê) *(chờ hình vẽ)*: Phi đao ném ra, trúng hay trật là một phép thử ngẫu nhiên: binh khí của Xác Suất.
- **Luân** (Thuật Toán và Tối Ưu) *(chờ hình vẽ)*: Vòng luân bay ra rồi quay về tay như một vòng lặp: binh khí của Thuật Toán.
- **Phủ** (Lập Trình) *(chờ hình vẽ)*: Một nhát búa rìu bổ đôi khúc gỗ lớn: chia để trị, cách người lập trình xẻ một bài toán.
- **Cầm** (Thực Chiến AI) *(chờ hình vẽ)*: Đàn lên dây từng sợi cho đúng âm, như tinh chỉnh một mô hình: binh khí của Thực Chiến AI.

Phẩm của binh khí, thấp đến cao: Hạ phẩm, Trung phẩm, Thượng phẩm, Cực phẩm, Tuyệt phẩm.

## Binh khí rải trong thế giới

| Binh khí | Phẩm | Ở đâu | Yêu cầu tu vi | Yêu cầu giáo trình |
|---|---|---|---|---|
| Mộc Kiếm | Hạ phẩm | Kiếm Trủng Sơn: Cắm trên bia đá ngay cổng núi. | Luyện Khí tầng 1 | Tập hợp và ánh xạ |
| Mộc Kiếm | Trung phẩm | Kiếm Trủng Sơn: Trong hang sau thác, do Thạch Khôi canh. | Luyện Khí tầng 4 | Hệ phương trình và khử Gauss |
| Mộc Kiếm | Thượng phẩm | Kiếm Trủng Sơn: Giữa bãi kiếm gãy, do Ma Trận Thú canh. | Luyện Khí tầng 7 | Ánh xạ tuyến tính và đổi cơ sở, Trực giao và phép chiếu |
| Thiết Kiếm | Hạ phẩm | Kiếm Trủng Sơn: Trên đỉnh núi, phải Đạp Kiếm Lướt qua vực mới tới. (cần Đạp Kiếm Lướt) | Luyện Khí tầng 9 | Dạng toàn phương, PCA và SVD |
| Mộc Đao | Hạ phẩm | Lưu Vân Cốc: Gác trên tảng đá đầu suối. | Luyện Khí tầng 1 | Hàm số, hàm hợp, mũ và logarit |
| Mộc Đao | Trung phẩm | Lưu Vân Cốc: Dưới đáy khúc suối cong nhất. | Luyện Khí tầng 4 | Đơn điệu, cực trị, lồi lõm |
| Mộc Đao | Thượng phẩm | Lưu Vân Cốc: Trên mỏm đá cao nhất thung lũng: điểm cực đại. | Luyện Khí tầng 7 | Gradient, Jacobian và lan truyền ngược |
| Thiết Đao | Hạ phẩm | Lưu Vân Cốc: Trong mây trên đầu thác, phải Đạp Kiếm Lướt. (cần Đạp Kiếm Lướt) | Luyện Khí tầng 9 | Gradient, Jacobian và lan truyền ngược, Diện tích và tích phân cận vô hạn |
| Mộc Hồ Lô | Hạ phẩm | Vạn Tượng Trạch: Treo trên cành liễu ở bến đầm. | Luyện Khí tầng 1 | Sự kiện và phép đếm |
| Mộc Hồ Lô | Trung phẩm | Vạn Tượng Trạch: Trên đảo sương giữa đầm. | Luyện Khí tầng 4 | Xác suất đầy đủ và Bayes |
| Mộc Hồ Lô | Thượng phẩm | Vạn Tượng Trạch: Trong miếu chìm, do Hồ Lô Tinh canh. | Luyện Khí tầng 7 | Kỳ vọng, phương sai và các phân phối quen thuộc |
| Thiết Hồ Lô | Hạ phẩm | Vạn Tượng Trạch: Dưới gốc cổ thụ giữa đầm sâu. | Luyện Khí tầng 9 | Kiểm định giả thuyết |
| Mộc Thương | Hạ phẩm | Mê Đồ Lâm: Dựng ở ngã ba đầu tiên của rừng. | Luyện Khí tầng 1 | Logic mệnh đề và quy tắc đếm |
| Mộc Thương | Trung phẩm | Mê Đồ Lâm: Ở ngõ cụt sâu nhất, phải tìm đúng đường. | Luyện Khí tầng 4 | Duyệt, tham lam và ký hiệu O lớn, Đồ thị và cách biểu diễn |
| Mộc Thương | Thượng phẩm | Mê Đồ Lâm: Trong hốc cây mẹ, do Mộc Yêu canh. | Luyện Khí tầng 7 | Bài toán tối ưu, tập lồi và hàm lồi |
| Thiết Thương | Hạ phẩm | Mê Đồ Lâm: Dưới đáy thung lũng thấp nhất của rừng: điểm cực tiểu. | Luyện Khí tầng 9 | Hạ gradient và nhân tử Lagrange |
| Mộc Chùy | Hạ phẩm | Thiên Công Phường: Trên đe của lò rèn nguội. | Luyện Khí tầng 1 | Python nhập môn |
| Mộc Chùy | Trung phẩm | Thiên Công Phường: Trong xưởng bánh răng, sau cơ quan cửa. | Luyện Khí tầng 4 | NumPy: mảng và vector hoá, Nhân ma trận và khử Gauss bằng code |
| Mộc Chùy | Thượng phẩm | Thiên Công Phường: Trong tay Cơ Quan Nhân đầu đàn. | Luyện Khí tầng 6 | Đồ thị bằng code |
| Thiết Chùy | Hạ phẩm | Thiên Công Phường: Trong lò lớn, chỉ mở khi đốt lại được lò. | Luyện Khí tầng 9 | Đồ thị bằng code, Mạng nơ-ron hai lớp tự viết |
| Mộc Cung | Hạ phẩm | Linh Xạ Nguyên: Trên giá cung ở trường bắn. | Luyện Khí tầng 3 | Mô hình đầu tiên: k láng giềng gần nhất |
| Mộc Cung | Trung phẩm | Linh Xạ Nguyên: Sau hàng bia thứ hai. | Luyện Khí tầng 5 | Khớp đường thẳng bằng hạ gradient, Lọc thư rác bằng Bayes |
| Mộc Cung | Thượng phẩm | Linh Xạ Nguyên: Trong tay Tâm Ma của chính mình. | Luyện Khí tầng 8 | Mạng nơ-ron hai lớp tự viết |
| Thiết Cung | Hạ phẩm | Lôi Kiếp Đài: Rơi ra khi vượt Thiên Kiếp Luyện Khí. | Luyện Khí tầng 9 | Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay |
| Thiết Trượng | Hạ phẩm | Vân Hải Thiên Đảo: Trên đảo mây đầu tiên. (cần Ngự Kiếm Phi Hành) | Trúc Cơ tầng 1 | Học có giám sát: tập huấn luyện, kiểm định, kiểm tra |
| Thiết Trượng | Trung phẩm | Vân Hải Thiên Đảo: Trên đảo có cây quyết định cổ thụ. (cần Ngự Kiếm Phi Hành) | Trúc Cơ tầng 2 | Cây quyết định, Phân loại và cách đo |
| Thiết Trượng | Thượng phẩm | Vân Hải Thiên Đảo: Trên đảo cao nhất. (cần Ngự Kiếm Phi Hành) | Trúc Cơ tầng 3 | Đánh giá mô hình cho đáng tin |

## Linh thú

Thu phục linh thú cũng theo luật đánh mới: không có câu hỏi riêng. Để linh thú đánh trúng rồi Phản Đòn đủ số lần là nó chịu phục; sau đó dùng Phong Ấn Phù để thu.

| Linh thú | Ở đâu | Từ tu vi | Phản Đòn để thu phục | Giúp gì |
|---|---|---|---|---|
| **Linh Hồ** | Mê Đồ Lâm: Sâu trong rừng, chỉ hiện ở ngõ cụt. | Luyện Khí tầng 3 | 3 lần | Đánh hơi vũ khí và rương ẩn ở gần. |
| **Huyền Quy** | Vạn Tượng Trạch: Phơi mình trên đảo sương. | Luyện Khí tầng 4 | 3 lần | Giảm sát thương khi trả lời sai. |
| **Bạch Hạc** | Lưu Vân Cốc: Đậu trên mỏm đá cao. | Luyện Khí tầng 5 | 4 lần | Né đòn hồi nhanh hơn. |
| **Hỏa Tước** | Kiếm Trủng Sơn: Tổ trên vách núi, phải Đạp Kiếm Lướt mới tới. | Luyện Khí tầng 6 | 4 lần | Đòn phản thêm sát thương hoả. |
| **Tiểu Long** | Thiên Công Phường: Cuộn trong lò lớn của phường. | Luyện Khí tầng 8 | 5 lần | Cưỡi được: chạy nhanh trên mặt đất. |
| **Kỳ Lân Con** | Vân Hải Thiên Đảo: Trên đảo mây xa nhất. | Trúc Cơ tầng 1 | 6 lần | Mỗi ngày tặng một lần trả lời lại câu vừa sai. |
