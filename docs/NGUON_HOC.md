# Nguồn học tốt nhất cho từng nút của Đạo Thụ

> File này do `python tools/check_sources.py --doc` dựng từ `server/data/math/sources/*.json`. Muốn đổi thì sửa các file dữ liệu ấy rồi chạy lại, đừng sửa ở đây.

Mỗi nút có **một nguồn chính** (học từ đầu thì đọc/xem cái này), vài nguồn **xem thêm** cho một góc nhìn khác, chỗ **luyện tập** có đáp án, và nguồn **tiếng Việt** khi có nguồn thật sự tốt. Game chỉ dẫn tên và đường tới nguồn; không chép nội dung của nguồn nào.

Tổng cộng 646 nguồn cho 120 nút, tra cứu ngày 2026-11-19.

## Đại Số Tuyến Tính

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Essence of Linear Algebra (16 chương)](https://www.3blue1brown.com/topics/linear-algebra), 3Blue1Brown (Grant Sanderson) — xem trước, 10-15 phút mỗi chương, theo thứ tự chương (Video, tiếng Anh, 3 giờ). Cho trực giác hình học cho mọi nút từ ma trận tới trị riêng; xem trước rồi mới vào bài giảng chặt chẽ.
2. [MIT 18.06 Linear Algebra (Spring 2010)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/), Gilbert Strang (MIT OpenCourseWare) — 34 bài giảng, có bài tập và đề thi kèm đáp án (Khoá học, tiếng Anh, 28 giờ). Giáo trình chuẩn, giảng đơn giản mà đúng; có pset và đề thi có lời giải để tự kiểm tra.
3. [Interactive Linear Algebra](https://textbooks.math.gatech.edu/ila/), Margalit, Rabinoff (Georgia Tech) — 6 chương, có hình tương tác và bài tập có đáp án (Sách, tiếng Anh). Sách miễn phí có hình tương tác, tiếng Anh dễ đọc, bù cho phần tính tay mà 3Blue1Brown bỏ qua.
4. [Mathematics for Machine Learning, chương 2-4](https://mml-book.github.io/), Deisenroth, Faisal, Ong — chương 2 Linear Algebra, 3 Analytic Geometry, 4 Matrix Decompositions (Sách, tiếng Anh). Nối thẳng đại số tuyến tính với học máy; đọc sau khi đã quen ma trận để thấy vì sao cần.

### Tập hợp và ánh xạ · Luyện Khí tầng 1

`ds_ngon_ngu`

*Chỉ cần khái niệm: ánh xạ, hàm hợp, đơn/toàn/song ánh. Đọc chương 12 trước, chương 1 sau, bỏ hết phần chứng minh.*

- **Chính:** [Book of Proof, chương 1 (Sets) và chương 12 (Functions)](https://richardhammack.github.io/BookOfProof/), Richard Hammack — chương 1 Tập hợp; chương 12 Ánh xạ (đơn ánh, toàn ánh, hàm hợp, hàm ngược) (Sách, tiếng Anh). Sách miễn phí giải thích tập hợp và ánh xạ từ đầu; lướt phần chứng minh, chỉ lấy khái niệm.
- **Xem thêm:** [Paul's Online Math Notes: Combining Functions (hàm hợp)](https://tutorial.math.lamar.edu/Classes/Alg/CombineFunctions.aspx), Paul Dawkins (Lamar University) — hàm hợp f∘g (Bài viết, tiếng Anh, 15 phút). Trang ngắn có ví dụ về hàm hợp, chính là các lớp mạng xếp chồng.
- **Xem thêm:** [Paul's Online Math Notes: Inverse Functions](https://tutorial.math.lamar.edu/Classes/Alg/InverseFunctions.aspx), Paul Dawkins (Lamar University) — hàm ngược, đơn ánh (Bài viết, tiếng Anh, 20 phút). Giải thích khi nào hàm có ngược và cách tìm, kèm bài luyện có lời giải.
- **Luyện tập:** [Paul's Online Math Notes: The Definition of a Function](https://tutorial.math.lamar.edu/Classes/Alg/FunctionDefn.aspx), Paul Dawkins (Lamar University) — định nghĩa hàm và bài luyện (Bài viết, tiếng Anh, 20 phút). Có bài luyện kèm lời giải để kiểm tra khái niệm ánh xạ.

### Vectơ và ma trận · Luyện Khí tầng 2

`ds_vecto_ma_tran`

*Xem 3Blue1Brown chương 1, rồi làm quen bảng số và chuyển vị bằng NumPy; vết và các ma trận đặc biệt chỉ cần nhớ tên.*

- **Chính:** [Essence of Linear Algebra, chương 1: Vectors, what even are they?](https://www.3blue1brown.com/lessons/vectors), 3Blue1Brown (Grant Sanderson) — chương 1 (Video, tiếng Anh, 10 phút). Ba cách nhìn một vectơ (mũi tên, dãy số, phần tử trừu tượng); nền cho cả nhánh.
- **Xem thêm:** [Immersive Linear Algebra: chương 2 Vectors](https://immersivemath.com/ila/ch02_vectors/ch02.html), J. Ström, K. Åström, T. Akenine-Möller — chương 2 (Tương tác, tiếng Anh, 40 phút). Vectơ với hình tương tác kéo thả, dễ thấy phép cộng và nhân với số.
- **Xem thêm:** [Immersive Linear Algebra: chương 6 The Matrix](https://immersivemath.com/ila/ch06_matrices/ch06.html), J. Ström, K. Åström, T. Akenine-Möller — chương 6 (Tương tác, tiếng Anh, 40 phút). Giới thiệu ma trận, chuyển vị và ma trận đặc biệt bằng hình.
- **Luyện tập:** [Interactive Linear Algebra: chương 3 Linear Transformations and Matrix Algebra](https://textbooks.math.gatech.edu/ila/chap-matrices.html), Margalit, Rabinoff (Georgia Tech) — đầu chương 3 (ma trận, chuyển vị) (Sách, tiếng Anh). Có bài tập có đáp án cho ma trận và phép toán cơ bản.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.1 Các phép toán hình học và đại số tuyến tính](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/geometry-linear-algebraic-ops_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.1.1 và 18.1.9 (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Tích vô hướng và nhân ma trận · Luyện Khí tầng 3

`ds_nhan_ma_tran`

*Xem chương 4 trước khi tính tay; luôn tự kiểm tra điều kiện kích thước và thử AB so với BA bằng NumPy.*

- **Chính:** [Essence of Linear Algebra, chương 4: Matrix multiplication as composition](https://www.3blue1brown.com/lessons/matrix-multiplication), 3Blue1Brown (Grant Sanderson) — chương 4 (Video, tiếng Anh, 10 phút). Cho thấy nhân ma trận là ghép hai phép biến đổi, và vì sao AB khác BA.
- **Xem thêm:** [MIT 18.06 Lecture 3: Multiplication and inverse matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-3-multiplication-and-inverse-matrices/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 3 (video + ghi chú) (Video, tiếng Anh, 40 phút). Bốn cách nhìn phép nhân ma trận, rất hợp để tính tay có hiểu.
- **Xem thêm:** [Essence of Linear Algebra, chương 9: Dot products and duality](https://www.3blue1brown.com/lessons/dot-products), 3Blue1Brown (Grant Sanderson) — chương 9 (Video, tiếng Anh, 14 phút). Tích vô hướng là phép chiếu, giải thích vì sao đo được độ giống nhau.
- **Luyện tập:** [MIT 18.06 Problem Set 1 (có lời giải)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_pset1_s10_soln/), MIT OpenCourseWare — mục 1.2 tới 2.5 của sách Strang (Bài tập, tiếng Anh). Bài tập về nhân ma trận và khử Gauss, có đáp án đầy đủ.

### Hệ phương trình và khử Gauss · Luyện Khí tầng 4

`ds_he_gauss`

*Học bài 2, rồi 7 và 8 của MIT 18.06; tập luyện tới khi tự khử nhanh một hệ 3x3 và gọi tên số nghiệm.*

- **Chính:** [MIT 18.06 Lecture 2: Elimination with matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 2 (video + ghi chú) (Video, tiếng Anh, 48 phút). Giảng khử Gauss và thế ngược rất rõ ràng, từng bước.
- **Xem thêm:** [MIT 18.06 Lecture 7: Solving Ax = 0: pivot variables, special solutions](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-7-solving-ax-0-pivot-variables-special-solutions/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 7 (video + ghi chú) (Video, tiếng Anh, 45 phút). Hệ thuần nhất, biến tự do và nghiệm cơ sở.
- **Xem thêm:** [MIT 18.06 Lecture 8: Solving Ax = b: row reduced form R](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-8-solving-ax-b-row-reduced-form-r/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 8 (video + ghi chú) (Video, tiếng Anh, 48 phút). Biện luận khi nào vô nghiệm, một nghiệm hay vô số nghiệm.
- **Xem thêm:** [Immersive Linear Algebra: chương 5 Gaussian Elimination](https://immersivemath.com/ila/ch05_gausselim/ch05.html), J. Ström, K. Åström, T. Akenine-Möller — chương 5 (Tương tác, tiếng Anh, 40 phút). Khử Gauss tương tác, tự bấm từng phép biến đổi hàng.
- **Luyện tập:** [Interactive Linear Algebra: chương 1 Systems of Linear Equations: Algebra](https://textbooks.math.gatech.edu/ila/chap-algebra.html), Margalit, Rabinoff (Georgia Tech) — mục 1.2 Row Reduction (Sách, tiếng Anh). Có nhiều bài khử hàng với đáp án, tự kiểm tra dạng bậc thang.
- **Luyện tập:** [Linear Algebra (Hefferon), sách đáp án đầy đủ](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf), Jim Hefferon — chương 1 Linear Systems (Bài tập, tiếng Anh). Mọi bài tập đều có lời giải chi tiết, tiện luyện biện luận nghiệm.

### Định thức, hạng và nghịch đảo · Luyện Khí tầng 5

`ds_dinh_thuc_nghich_dao`

*Xem chương 6-7 của 3Blue1Brown để hiểu, rồi bài 18-19 của MIT để tính tay; hạng nên nắm bằng ý 'số chiều thật của dữ liệu'.*

- **Chính:** [Essence of Linear Algebra, chương 6: The determinant](https://www.3blue1brown.com/lessons/determinant), 3Blue1Brown (Grant Sanderson) — chương 6 (Video, tiếng Anh, 10 phút). Định thức là hệ số co giãn diện tích; bằng 0 nghĩa là mất một chiều.
- **Xem thêm:** [Essence of Linear Algebra, chương 7: Inverse matrices, column space and null space](https://www.3blue1brown.com/lessons/inverse-matrices), 3Blue1Brown (Grant Sanderson) — chương 7 (Video, tiếng Anh, 12 phút). Nối nghịch đảo, hạng và không gian cột trong một bài.
- **Xem thêm:** [MIT 18.06 Lecture 18: Properties of determinants](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 18 (video + ghi chú) (Video, tiếng Anh, 50 phút). Ba tính chất nền của định thức rồi suy ra mọi thứ khác.
- **Xem thêm:** [MIT 18.06 Lecture 19: Determinant formulas and cofactors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 19 (video + ghi chú) (Video, tiếng Anh, 50 phút). Khai triển theo hàng/cột (cofactor) kiểu thi cử.
- **Luyện tập:** [Interactive Linear Algebra: chương 4 Determinants](https://textbooks.math.gatech.edu/ila/chap-determinant.html), Margalit, Rabinoff (Georgia Tech) — cả chương 4 (Sách, tiếng Anh). Tính định thức bằng khử hàng và cofactor, có bài tập kèm đáp án.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.1 Các phép toán hình học và đại số tuyến tính](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/geometry-linear-algebraic-ops_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.1.6 Hạng, 18.1.7 Khả nghịch, 18.1.8 Định thức (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Không gian vectơ: bao tuyến tính, cơ sở, số chiều · Luyện Khí tầng 6

`ds_khong_gian`

*Học bài 6 rồi 9 của MIT; tiên đề không gian vectơ chỉ cần biết, tập trung vào độc lập, cơ sở, số chiều và tọa độ.*

- **Chính:** [MIT 18.06 Lecture 9: Independence, basis, and dimension](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-9-independence-basis-and-dimension/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 9 (video + ghi chú) (Video, tiếng Anh, 50 phút). Bài giảng chuẩn về độc lập tuyến tính, cơ sở và số chiều.
- **Xem thêm:** [Essence of Linear Algebra, chương 2: Linear combinations, span, and basis vectors](https://www.3blue1brown.com/lessons/span), 3Blue1Brown (Grant Sanderson) — chương 2 (Video, tiếng Anh, 10 phút). Bao tuyến tính và cơ sở bằng hình, rất dễ nhớ.
- **Xem thêm:** [Essence of Linear Algebra, chương 16: Abstract vector spaces](https://www.3blue1brown.com/lessons/abstract-vector-spaces), 3Blue1Brown (Grant Sanderson) — chương 16 (Video, tiếng Anh, 16 phút). Cho thấy vì sao hàm và đa thức cũng là vectơ, phần tiên đề.
- **Xem thêm:** [Essence of Linear Algebra, chương 13: Change of basis](https://www.3blue1brown.com/lessons/change-of-basis), 3Blue1Brown (Grant Sanderson) — chương 13 (Video, tiếng Anh, 12 phút). Tọa độ và ma trận chuyển cơ sở bằng cách hai người quan sát dùng hai hệ trục.
- **Luyện tập:** [MIT 18.06 Exam 1 (có lời giải)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam1_s10/), MIT OpenCourseWare — đề thi 1 (kèm lời giải ở trang kế) (Đề thi, tiếng Anh, 60 phút). Đề thi thật về không gian cột, nullspace, độc lập tuyến tính, có đáp án để so.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.1 Các phép toán hình học và đại số tuyến tính](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/geometry-linear-algebraic-ops_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.1.5 Phụ thuộc tuyến tính (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Trực giao và phép chiếu · Luyện Khí tầng 7

`ds_truc_giao_chieu`

*Học bài 14-17 của MIT theo thứ tự; nối ngay với bài toán 'khớp đường thẳng' để thấy phép chiếu dùng vào đâu.*

- **Chính:** [MIT 18.06 Lecture 15: Projections onto subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-15-projections-onto-subspaces/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 15 (video + ghi chú) (Video, tiếng Anh, 50 phút). Dẫn ra công thức phép chiếu từ hình học, chính là gốc của bình phương tối thiểu.
- **Xem thêm:** [MIT 18.06 Lecture 16: Projection matrices and least squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 16 (video + ghi chú) (Video, tiếng Anh, 50 phút). Từ phép chiếu tới khớp đường thẳng vào dữ liệu.
- **Xem thêm:** [MIT 18.06 Lecture 17: Orthogonal matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 17 (video + ghi chú) (Video, tiếng Anh, 50 phút). Trực giao hóa Gram-Schmidt từng bước.
- **Xem thêm:** [Mathematics for Machine Learning (sách miễn phí)](https://mml-book.github.io/book/mml-book.pdf), Deisenroth, Faisal, Ong — chương 3 Analytic Geometry, mục 3.4 tới 3.8 (Sách, tiếng Anh). Chương về trực giao và phép chiếu viết cho học máy, có bài tập.
- **Luyện tập:** [Interactive Linear Algebra: chương 6 Orthogonality](https://textbooks.math.gatech.edu/ila/chap-orthogonality.html), Margalit, Rabinoff (Georgia Tech) — mục 6.1 tới 6.5 (Sách, tiếng Anh). Trực giao, chiếu và bình phương tối thiểu có hình tương tác và bài có đáp án.

### Ánh xạ tuyến tính và đổi cơ sở · Luyện Khí tầng 7

`ds_anh_xa_tuyen_tinh`

*Xem chương 3 trước, rồi bài 30-31 của MIT; Ker, Im và số chiều chỉ cần hiểu và tính được trên ma trận.*

- **Chính:** [Essence of Linear Algebra, chương 3: Linear transformations and matrices](https://www.3blue1brown.com/lessons/linear-transformations), 3Blue1Brown (Grant Sanderson) — chương 3 (Video, tiếng Anh, 10 phút). Ma trận là phép biến hình không gian; đúng điều nút này cần.
- **Xem thêm:** [MIT 18.06 Lecture 30: Linear transformations and their matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-30-linear-transformations-and-their-matrices/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 30 (video + ghi chú) (Video, tiếng Anh, 50 phút). Ma trận của ánh xạ tuyến tính theo cơ sở, kèm ví dụ đạo hàm.
- **Xem thêm:** [MIT 18.06 Lecture 31: Change of basis; image compression](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-31-change-of-basis-image-compression/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 31 (video + ghi chú) (Video, tiếng Anh, 50 phút). Đổi cơ sở và ma trận đồng dạng.
- **Xem thêm:** [Mathematics for Machine Learning (sách miễn phí)](https://mml-book.github.io/book/mml-book.pdf), Deisenroth, Faisal, Ong — chương 2, mục 2.7 Linear Mappings (kể cả Ker, Im và định lý số chiều) (Sách, tiếng Anh). Định nghĩa gọn của Ker, Im và rank-nullity theo phong cách học máy.
- **Luyện tập:** [MIT 18.06 Exam 3 (có lời giải)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam3_s10/), MIT OpenCourseWare — đề thi 3 (lời giải ở trang kế) (Đề thi, tiếng Anh, 60 phút). Có câu về ma trận của ánh xạ tuyến tính, đổi cơ sở và SVD.

### Giá trị riêng và chéo hoá · Luyện Khí tầng 8

`ds_tri_rieng`

*Xem chương 14, rồi bài 21-22 của MIT; trị riêng phức và dạng Jordan có thể bỏ qua.*

- **Chính:** [Essence of Linear Algebra, chương 14: Eigenvectors and eigenvalues](https://www.3blue1brown.com/lessons/eigenvalues), 3Blue1Brown (Grant Sanderson) — chương 14 (Video, tiếng Anh, 17 phút). Trị riêng là hướng chỉ bị kéo giãn; chéo hóa nghĩa là chọn đúng hệ trục.
- **Xem thêm:** [MIT 18.06 Lecture 21: Eigenvalues and eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 21 (video + ghi chú) (Video, tiếng Anh, 50 phút). Cách tìm trị riêng bằng tay, từ phương trình đặc trưng.
- **Xem thêm:** [MIT 18.06 Lecture 22: Diagonalization and powers of A](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-22-diagonalization-and-powers-of-a/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 22 (video + ghi chú) (Video, tiếng Anh, 50 phút). Chéo hóa và tính lũy thừa ma trận, như dãy Fibonacci.
- **Xem thêm:** [Essence of Linear Algebra, chương 15: A quick trick for computing eigenvalues](https://www.3blue1brown.com/lessons/quick-eigen), 3Blue1Brown (Grant Sanderson) — chương 15 (Video, tiếng Anh, 12 phút). Mẹo tính trị riêng ma trận 2x2 rất nhanh.
- **Luyện tập:** [Interactive Linear Algebra: chương 5 Eigenvalues and Eigenvectors](https://textbooks.math.gatech.edu/ila/chap-eigenvalues.html), Margalit, Rabinoff (Georgia Tech) — mục 5.1 tới 5.4 (Sách, tiếng Anh). Hình tương tác cho trị riêng và chéo hóa, có bài tập kèm đáp án.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.2 Phân rã trị riêng](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/eigendecomposition_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — toàn bài 18.2 (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Dạng toàn phương, PCA và SVD · Luyện Khí tầng 9

`ds_pca_svd`

*Học bài 29 SVD, rồi bài 26-27 của Vũ Hữu Tiệp để làm PCA bằng tay; dạng toàn phương chỉ cần biết 'xác định dương = cực tiểu'.*

- **Chính:** [MIT 18.06 Lecture 29: Singular value decomposition](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-29-singular-value-decomposition/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 29 (video + ghi chú) (Video, tiếng Anh, 50 phút). Bài giảng SVD của Strang, ngắn mà đủ ý, nối được với nén dữ liệu.
- **Xem thêm:** [MIT 18.06 Lecture 25: Symmetric matrices and positive definiteness](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 25 (video + ghi chú) (Video, tiếng Anh, 50 phút). Ma trận đối xứng, xác định dương, dạng toàn phương.
- **Xem thêm:** [Mathematics for Machine Learning (sách miễn phí)](https://mml-book.github.io/book/mml-book.pdf), Deisenroth, Faisal, Ong — chương 4 mục 4.5 Singular Value Decomposition và chương 10 PCA (Sách, tiếng Anh). Dẫn xuất PCA từ phương sai lớn nhất rồi từ SVD, dành cho người học máy.
- **Luyện tập:** [MML tutorial: PCA (notebook có lời giải)](https://mml-book.github.io/tutorials/tutorial_pca.solution.ipynb), Deisenroth, Faisal, Ong — cả notebook (Code, tiếng Anh, 90 phút). Tự cài đặt PCA bằng NumPy rồi so với đáp án.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 26: Singular Value Decomposition](https://machinelearningcoban.com/2017/06/07/svd/), Vũ Hữu Tiệp — toàn bài (SVD, SVD rút gọn, nén ảnh) (Bài viết, tiếng Việt, 40 phút). Bài SVD tiếng Việt rõ ràng, có ví dụ nén ảnh và mã Python.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 27: Principal Component Analysis (phần 1)](https://machinelearningcoban.com/2017/06/15/pca/), Vũ Hữu Tiệp — toàn bài, các bước thực hiện PCA (Bài viết, tiếng Việt, 40 phút). Dẫn PCA từ ma trận hiệp phương sai, có bảy bước làm.

### Bàng môn: Số phức · Luyện Khí

`ds_so_phuc`

*Chỉ học dạng đại số và liên hợp khi cần; dạng lượng giác và công thức Moivre chưa tìm được nguồn tốt, xem sách giáo trình trên lớp.*

- **Chính:** [Paul's Online Math Notes: Complex Numbers](https://tutorial.math.lamar.edu/Classes/Alg/ComplexNumbers.aspx), Paul Dawkins (Lamar University) — dạng đại số, cộng, trừ, nhân, chia, liên hợp (Bài viết, tiếng Anh, 20 phút). Gọn, đủ cho dạng đại số; dạng lượng giác phải tìm thêm.
- **Xem thêm:** [MIT 18.06 Lecture 26: Complex matrices; fast Fourier transform](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-26-complex-matrices-fast-fourier-transform/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 26 (video + ghi chú) (Video, tiếng Anh, 50 phút). Chỗ số phức thật sự được dùng: ma trận phức và FFT (để sau).

### Bàng môn: Quy tắc Cramer · Luyện Khí

`ds_cramer`

*Chỉ cần biết công thức cho thi cử; đời thực dùng khử Gauss.*

- **Chính:** [MIT 18.06 Lecture 20: Cramer's rule, inverse matrix, and volume](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/), Gilbert Strang (MIT OpenCourseWare) — bài giảng 20 (video + ghi chú) (Video, tiếng Anh, 50 phút). Giải thích quy tắc Cramer và công thức nghịch đảo bằng phần phụ đại số.
- **Xem thêm:** [Interactive Linear Algebra: chương 4 Determinants](https://textbooks.math.gatech.edu/ila/chap-determinant.html), Margalit, Rabinoff (Georgia Tech) — mục 4.3 Cramer's rule (Sách, tiếng Anh). Có phần Cramer kèm giải thích hình học.

### Dạng tự luận hay gặp trong đề cuối kỳ — Đại Số Tuyến Tính

Các dạng này không nằm trên chính đạo; chúng là đề của Luận Đạo Đài (`docs/LUAN_DAO_DAI.md`).

| Dạng | Thuộc nút | Hay gặp | Mô tả | Xem ở đâu |
|---|---|---|---|---|
| **Biện luận hệ phương trình theo tham số** | Hệ phương trình và khử Gauss | rất hay gặp | Cho hệ có tham số m; khử Gauss rồi biện luận vô nghiệm, một nghiệm, vô số nghiệm và viết nghiệm tổng quát. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 1 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam1_s10_sol/) |
| **Chứng minh một tập là không gian con** | Không gian vectơ: bao tuyến tính, cơ sở, số chiều | rất hay gặp | Cho tập vectơ hoặc ma trận thỏa một điều kiện; kiểm tra chứa 0, đóng với phép cộng và nhân với số. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 1 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam1_s10_sol/) |
| **Độc lập hoặc phụ thuộc tuyến tính** | Không gian vectơ: bao tuyến tính, cơ sở, số chiều | rất hay gặp | Chứng minh một hệ vectơ độc lập tuyến tính, hoặc tìm điều kiện của tham số để hệ phụ thuộc. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 1 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam1_s10_sol/) |
| **Cơ sở, số chiều và tọa độ** | Không gian vectơ: bao tuyến tính, cơ sở, số chiều | rất hay gặp | Chứng minh một hệ là cơ sở của không gian, tìm số chiều của bao tuyến tính, tọa độ và ma trận chuyển cơ sở. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 1 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam1_s10_sol/) |
| **Chứng minh một ánh xạ là tuyến tính** | Ánh xạ tuyến tính và đổi cơ sở | rất hay gặp | Cho ánh xạ định nghĩa bằng công thức hoặc trên đa thức, ma trận; kiểm tra cộng tính và thuần nhất. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 3 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam3_s10_soln/) |
| **Nhân, ảnh và định lý số chiều** | Ánh xạ tuyến tính và đổi cơ sở | rất hay gặp | Tìm cơ sở và số chiều của Ker f và Im f, rồi dùng định lý số chiều để kiểm tra hoặc kết luận đơn ánh, toàn ánh. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 3 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam3_s10_soln/) |
| **Ma trận ánh xạ trong cơ sở và đồng dạng** | Ánh xạ tuyến tính và đổi cơ sở | hay gặp | Viết ma trận của ánh xạ theo hai cơ sở, đổi cơ sở, chứng minh hai ma trận đồng dạng có cùng định thức, vết, trị riêng. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 3 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam3_s10_soln/) |
| **Chéo hóa ma trận và điều kiện chéo hóa được** | Giá trị riêng và chéo hoá | rất hay gặp | Tìm trị riêng, vectơ riêng, ma trận làm chéo hóa, tính lũy thừa; hoặc chứng minh không chéo hóa được. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 2 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam2_s10_soln/); [MIT 18.06 Final exam và đáp án](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_final_answers/) |
| **Chứng minh tính chất trị riêng** | Giá trị riêng và chéo hoá | hay gặp | Từ điều kiện như A bình phương bằng A, ma trận lũy linh, ma trận trực giao, suy ra các trị riêng khả dĩ; trị riêng của A và A chuyển vị. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf); [MIT 18.06 Exam 2 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam2_s10_soln/) |
| **Trực giao hóa Gram-Schmidt và không gian Euclide** | Trực giao và phép chiếu | hay gặp | Trực giao hóa một hệ vectơ, tìm cơ sở trực chuẩn; chứng minh bất đẳng thức Cauchy-Schwarz hoặc tính chất của tích vô hướng và chuẩn. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 2 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam2_s10_soln/) |
| **Phép chiếu trực giao và khoảng cách** | Trực giao và phép chiếu | hay gặp | Tìm hình chiếu của một vectơ lên không gian con, khoảng cách tới không gian con, hoặc nghiệm bình phương tối thiểu. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 2 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam2_s10_soln/) |
| **Tính chất của định thức** | Định thức, hạng và nghịch đảo | hay gặp | Tính định thức cấp n có cấu trúc đặc biệt; chứng minh det(AB)=det(A)det(B), det của ma trận chuyển vị, hoặc ma trận suy biến. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 2 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam2_s10_soln/); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf) |
| **Nghịch đảo, chuyển vị và hạng** | Định thức, hạng và nghịch đảo | hay gặp | Chứng minh (AB) nghịch đảo bằng B nghịch đảo nhân A nghịch đảo, tính chất chuyển vị, hạng của tích và tổng; tìm nghịch đảo bằng biến đổi sơ cấp. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf) |
| **Chứng minh đẳng thức ma trận** | Tích vô hướng và nhân ma trận | hay gặp | Cho điều kiện như A^2 = A hoặc AB = BA; chứng minh một đẳng thức hoặc tính lũy thừa A^n bằng quy nạp. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [Linear Algebra (Hefferon): sách đáp án mọi bài tập](https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf) |
| **Dạng toàn phương và xác định dương** | Dạng toàn phương, PCA và SVD | hay gặp | Đưa dạng toàn phương về dạng chính tắc bằng Lagrange hoặc trực giao hóa; xét xác định dương theo tham số. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf); [MIT 18.06 Exam 3 và lời giải](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/mit18_06s10_exam3_s10_soln/) |
| **Đơn ánh, toàn ánh, song ánh** | Tập hợp và ánh xạ | thỉnh thoảng | Chứng minh một ánh xạ là đơn ánh, toàn ánh hoặc song ánh, tìm ánh xạ ngược; mệnh đề về tạo ảnh của tập con. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf) |
| **Số phức: lượng giác, Moivre, căn bậc n** | Bàng môn: Số phức | thỉnh thoảng | Tính lũy thừa số phức bằng công thức Moivre, giải phương trình bậc cao trên số phức. | [Đề cương học phần MI1141 Đại số (CTĐT tài năng, bản 2023)](https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf) |

**Đã xem và không chọn:**

- Khan Academy Linear Algebra (video): Không mở được trang để kiểm; video dài, dạy tính tay; không bản tiếng Việt cho môn này.
- MIT 18.06 toàn bộ 34 bài làm đường chính: Mỗi bài ~50 phút, quá dài cho đường chính; dùng như bài đọc sâu sau khi xem 3Blue1Brown.
- Linear Algebra Done Right (Axler): Chặt chẽ nhưng gần như không có tính toán, hợp người thích chứng minh hơn là người muốn xây mô hình.
- Các bộ đề thi đăng trên studocu, 123doc, scribd: Không phải nguồn chính thức, có thể vi phạm bản quyền; chỉ dùng đề minh họa của fami.hust.edu.vn.
- Trang Pressbooks eCampusOntario Đại số tuyến tính tiếng Việt: Trang trả lỗi 403 khi kiểm, chưa xác nhận được nội dung.
- Sách The Matrix Cookbook: Là bảng tra cứu công thức, không phải bài học cho người mới.
- d2l.aivivn.com (trang cũ của Đắm mình vào Học Sâu): Tên miền đã bị chiếm: trang chủ hiện là quảng cáo cờ bạc. Dùng bản dịch tay trên GitHub (thẻ v0.15).
- vi.d2l.ai (Đắm mình vào Học Sâu 0.17.5): Bản dịch máy, sai thuật ngữ (mạng tích chập thành 'mạng thần kinh phức tạp'). Không dùng làm nguồn tiếng Việt.

## Giải Tích

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Essence of Calculus (chương 1-14)](https://www.3blue1brown.com/topics/calculus), 3Blue1Brown (Grant Sanderson) — xem trước, 10-20 phút mỗi chương (Video, tiếng Anh, 3 giờ). Cho trực giác cho đạo hàm, tích phân, Taylor trước khi tính tay.
2. [MIT 18.01SC Single Variable Calculus (Fall 2010)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/), David Jerison và đồng nghiệp (MIT OpenCourseWare) — 5 đơn vị, mỗi đơn vị có bài tập và đề thi kèm lời giải (Khoá học, tiếng Anh, 33 giờ). Giáo trình một biến chuẩn, mỗi buổi ngắn; có bài tập và đề thi có lời giải.
3. [Paul's Online Math Notes: Calculus I, II, III](https://tutorial.math.lamar.edu/Classes/CalcI/CalcI.aspx), Paul Dawkins (Lamar University) — mọi trang có bài luyện kèm lời giải (Bài viết, tiếng Anh). Tra cứu và luyện tập rất tốt, từng mục nhỏ có bài tập với lời giải chi tiết.
4. [Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/), Terence Parr, Jeremy Howard — toàn bài, cho nút gradient (Bài viết, tiếng Anh, 90 phút). Nối giải tích nhiều biến với lan truyền ngược trong mạng nơ-ron.

### Hàm số, hàm hợp, mũ và logarit · Luyện Khí tầng 1

`gt_ham_so`

*Chỉ cần ôn lại; ưu tiên hàm mũ và logarit vì sigmoid, softmax, log-likelihood dùng ngay.*

- **Chính:** [Paul's Online Math Notes: Calculus I Review: Functions](https://tutorial.math.lamar.edu/Classes/CalcI/Functions.aspx), Paul Dawkins (Lamar University) — mục Functions trong chương Review (Bài viết, tiếng Anh, 25 phút). Ôn tập tập xác định và hàm hợp gọn kèm bài luyện.
- **Xem thêm:** [Paul's Online Math Notes: Exponential Functions](https://tutorial.math.lamar.edu/Classes/CalcI/ExpFunctions.aspx), Paul Dawkins (Lamar University) — chương Review (Bài viết, tiếng Anh, 20 phút). Hàm mũ và tính chất, nền cho softmax và sigmoid.
- **Xem thêm:** [Paul's Online Math Notes: Logarithm Functions](https://tutorial.math.lamar.edu/Classes/CalcI/LogFcns.aspx), Paul Dawkins (Lamar University) — chương Review (Bài viết, tiếng Anh, 20 phút). Logarit và tính chất, nền cho log-likelihood.
- **Xem thêm:** [Paul's Online Math Notes: Inverse Functions](https://tutorial.math.lamar.edu/Classes/CalcI/InverseFunctions.aspx), Paul Dawkins (Lamar University) — chương Review (Bài viết, tiếng Anh, 20 phút). Hàm ngược và điều kiện tồn tại.
- **Luyện tập:** [Paul's Online Math Notes: Exponential and Logarithm Equations](https://tutorial.math.lamar.edu/Classes/CalcI/ExpLogEqns.aspx), Paul Dawkins (Lamar University) — chương Review (Bài viết, tiếng Anh, 25 phút). Giải phương trình mũ và logarit, có lời giải.

### Giới hạn và liên tục · Luyện Khí tầng 2

`gt_gioi_han`

*Xem chương 8 để hiểu giới hạn; chỉ cần tính được giới hạn đơn giản và phát hiện chỗ gãy như ReLU.*

- **Chính:** [Essence of Calculus, chương 8: Limits and the definition of derivatives](https://www.3blue1brown.com/lessons/limits), 3Blue1Brown (Grant Sanderson) — chương 8 (Video, tiếng Anh, 15 phút). Giới hạn là gì bằng hình, không sa vào epsilon-delta.
- **Xem thêm:** [MIT 18.01SC, Session 4: Limits and Continuity (và Session 5 Discontinuity)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-4-limits-and-continuity/), MIT OpenCourseWare — session 4 và 5 (Video, tiếng Anh, 30 phút). Bài giảng ngắn về giới hạn một phía và liên tục, rồi tới các loại gián đoạn.
- **Xem thêm:** [Paul's Online Math Notes: Limits (chương Giới hạn)](https://tutorial.math.lamar.edu/Classes/CalcI/limitsIntro.aspx), Paul Dawkins (Lamar University) — mục The Limit, One-Sided Limits, Continuity (Bài viết, tiếng Anh, 60 phút). Có cả loạt mục nhỏ kèm lời giải, tiện tra cứu.
- **Luyện tập:** [Paul's Online Math Notes: Continuity](https://tutorial.math.lamar.edu/Classes/CalcI/Continuity.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 25 phút). Bài luyện liên tục có lời giải.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.3 Giải tích một biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/single-variable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.3.1 Giải tích vi phân (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Đạo hàm và quy tắc dây chuyền · Luyện Khí tầng 3

`gt_dao_ham`

*Đây là nút quan trọng nhất: xem chương 2 rồi bài dây chuyền, tự tay làm 10 bài của Paul; đạo hàm theo định nghĩa chuyển sang đường tự luận.*

- **Chính:** [Essence of Calculus, chương 2: The paradox of the derivative](https://www.3blue1brown.com/lessons/derivatives), 3Blue1Brown (Grant Sanderson) — chương 2 (Video, tiếng Anh, 17 phút). Đạo hàm là độ dốc, hiểu qua nhân từng cái nhích nhỏ.
- **Xem thêm:** [Essence of Calculus: Visualizing the chain rule and product rule](https://www.3blue1brown.com/lessons/chain-rule-and-product-rule), 3Blue1Brown (Grant Sanderson) — bài về tổng, tích, dây chuyền (Video, tiếng Anh, 15 phút). Quy tắc dây chuyền bằng ba trục số; chính là lan truyền ngược.
- **Xem thêm:** [MIT 18.01SC, Session 11: Chain Rule](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-11-chain-rule/), MIT OpenCourseWare — session 11 (cùng Part A: định nghĩa, quy tắc) (Video, tiếng Anh, 20 phút). Quy tắc dây chuyền có thêm ví dụ tính tay.
- **Xem thêm:** [Matrix Calculus You Need For Deep Learning: Scalar derivative rules](https://explained.ai/matrix-calculus/#sec:1.2), Parr, Howard — mục 'Review: Scalar derivative rules' (Bài viết, tiếng Anh, 15 phút). Bảng quy tắc đạo hàm ngắn, đúng chuẩn bị cho học sâu.
- **Luyện tập:** [Paul's Online Math Notes: Chain Rule](https://tutorial.math.lamar.edu/Classes/CalcI/ChainRule.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 30 phút). Nhiều bài dây chuyền có lời giải chi tiết.
- **Luyện tập:** [MIT 18.01SC Exam 1 (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/exam-1/), MIT OpenCourseWare — Unit 1 Exam 1 (Đề thi, tiếng Anh, 60 phút). Đề thi thật về định nghĩa và quy tắc đạo hàm, kèm lời giải.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.3 Giải tích một biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/single-variable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.3.2 Quy tắc giải tích (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Đơn điệu, cực trị, lồi lõm · Luyện Khí tầng 4

`gt_cuc_tri`

*Học Paul phần I rồi II; nhớ 'đạo hàm bằng 0 chưa đủ': dùng đạo hàm cấp hai để biết cực tiểu hay cực đại.*

- **Chính:** [Paul's Online Math Notes: The Shape of a Graph, Part I](https://tutorial.math.lamar.edu/Classes/CalcI/ShapeofGraphPtI.aspx), Paul Dawkins (Lamar University) — đơn điệu, cực trị; phần II nói lồi lõm và điểm uốn (Bài viết, tiếng Anh, 40 phút). Nối dấu đạo hàm với dạng đồ thị, có bài luyện kèm lời giải.
- **Xem thêm:** [Paul's Online Math Notes: The Shape of a Graph, Part II](https://tutorial.math.lamar.edu/Classes/CalcI/ShapeofGraphPtII.aspx), Paul Dawkins (Lamar University) — lồi, lõm, điểm uốn, kiểm tra đạo hàm cấp hai (Bài viết, tiếng Anh, 35 phút). Đạo hàm cấp hai và độ lồi: nền cho Hessian.
- **Xem thêm:** [Paul's Online Math Notes: Finding Absolute Extrema](https://tutorial.math.lamar.edu/Classes/CalcI/AbsExtrema.aspx), Paul Dawkins (Lamar University) — giá trị lớn nhất, nhỏ nhất trên đoạn (Bài viết, tiếng Anh, 20 phút). Quy trình tìm min, max trên đoạn rõ ràng.
- **Xem thêm:** [Machine Learning cơ bản, bài 16: Convex sets và convex functions](https://machinelearningcoban.com/2017/03/12/convexity/), Vũ Hữu Tiệp — hàm lồi và tính chất (Bài viết, tiếng Việt, 40 phút). Giải thích hàm lồi bằng tiếng Việt vì sao bài toán tối ưu dễ hay khó.
- **Luyện tập:** [MIT 18.01SC Exam 2 (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-2-applications-of-differentiation/exam-2/), MIT OpenCourseWare — Unit 2 Exam 2 (Đề thi, tiếng Anh, 60 phút). Đề thi thật về cực trị, tối ưu, kèm lời giải.

### Khai triển Taylor · Luyện Khí tầng 5

`gt_taylor`

*Xem chương 14, rồi chỉ cần thuộc Maclaurin của e^x, sin, cos, ln(1+x); bỏ phần bán kính hội tụ.*

- **Chính:** [Essence of Calculus, chương 14: Taylor series](https://www.3blue1brown.com/lessons/taylor-series), 3Blue1Brown (Grant Sanderson) — chương 14 (Video, tiếng Anh, 22 phút). Xấp xỉ hàm bằng đa thức quanh một điểm, trực giác rõ ràng.
- **Xem thêm:** [MIT 18.01SC, Session 98 và 99: Taylor's Series](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-5-exploring-the-infinite/part-b-taylor-series/), MIT OpenCourseWare — sessions 98-99 trong Unit 5 Part B (Video, tiếng Anh, 30 phút). Bài giảng chuẩn về công thức Taylor và Maclaurin cho các hàm cơ bản.
- **Xem thêm:** [Đắm mình vào học sâu, phụ lục toán: 18.3 Giải tích một biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/single-variable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.3.2.3 Xấp xỉ tuyến tính và 18.3.2.5 Chuỗi Taylor (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.
- **Luyện tập:** [Paul's Online Math Notes: Series and Sequences (chương), mục Taylor Series](https://tutorial.math.lamar.edu/Classes/CalcII/SeriesIntro.aspx), Paul Dawkins (Lamar University) — mục 16 Taylor Series trong chương (Bài viết, tiếng Anh, 30 phút). Bài luyện Taylor có lời giải; bỏ qua phần hội tụ chuỗi.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.3 Giải tích một biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/single-variable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.3.2.5 Chuỗi Taylor (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Tích phân · Luyện Khí tầng 5

`gt_tich_phan`

*Xem chương 11, rồi luyện đổi biến và từng phần với Paul; Newton-Leibniz và cận biến thiên là phần thi hay hỏi.*

- **Chính:** [Essence of Calculus, chương 11: Integration and the fundamental theorem of calculus](https://www.3blue1brown.com/lessons/integration), 3Blue1Brown (Grant Sanderson) — chương 11 (Video, tiếng Anh, 20 phút). Tích phân là diện tích dưới đường cong và là ngược của đạo hàm.
- **Xem thêm:** [MIT 18.01SC Unit 3 Part A: Definite integral and first fundamental theorem](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-3-the-definite-integral-and-its-applications/part-a-definition-of-the-definite-integral-and-first-fundamental-theorem/), MIT OpenCourseWare — sessions 43 tới 50 (Video, tiếng Anh, 90 phút). Tổng Riemann và định lý cơ bản, có bài tập kèm.
- **Xem thêm:** [Paul's Online Math Notes: Integration by Parts](https://tutorial.math.lamar.edu/Classes/CalcII/IntegrationByParts.aspx), Paul Dawkins (Lamar University) — tích phân từng phần (Bài viết, tiếng Anh, 35 phút). Công thức và mẹo chọn u, dv, có nhiều ví dụ.
- **Xem thêm:** [Paul's Online Math Notes: Substitution Rule for Indefinite Integrals](https://tutorial.math.lamar.edu/Classes/CalcI/SubstitutionRuleIndefinite.aspx), Paul Dawkins (Lamar University) — đổi biến (Bài viết, tiếng Anh, 30 phút). Quy tắc đổi biến, bài luyện có lời giải.
- **Luyện tập:** [Paul's Online Math Notes: Computing Definite Integrals](https://tutorial.math.lamar.edu/Classes/CalcI/ComputingDefiniteIntegrals.aspx), Paul Dawkins (Lamar University) — Newton-Leibniz, cận biến thiên (Bài viết, tiếng Anh, 30 phút). Bài tích phân xác định có lời giải.
- **Luyện tập:** [MIT 18.01SC Exam 3 (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-3-the-definite-integral-and-its-applications/exam-3/), MIT OpenCourseWare — Unit 3 Exam 3 (Đề thi, tiếng Anh, 60 phút). Đề thi thật về tích phân xác định.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.5 Giải tích tích phân](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/integral-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — toàn bài (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Diện tích và tích phân cận vô hạn · Luyện Khí tầng 6

`gt_tich_phan_ung_dung`

*Học Paul phần Improper Integrals rồi phần Probability; mục tiêu là kiểm hàm mật độ mũ và chuẩn có tích phân 1.*

- **Chính:** [Paul's Online Math Notes: Improper Integrals](https://tutorial.math.lamar.edu/Classes/CalcII/ImproperIntegrals.aspx), Paul Dawkins (Lamar University) — cận vô hạn và hàm không bị chặn (Bài viết, tiếng Anh, 40 phút). Giải thích rõ cách tính tích phân suy rộng bằng giới hạn, kèm bài luyện.
- **Xem thêm:** [Paul's Online Math Notes: Probability (ứng dụng của tích phân)](https://tutorial.math.lamar.edu/Classes/CalcII/Probability.aspx), Paul Dawkins (Lamar University) — hàm mật độ và kỳ vọng (Bài viết, tiếng Anh, 30 phút). Dùng đúng tích phân suy rộng để kiểm hàm mật độ có tổng bằng 1.
- **Xem thêm:** [Paul's Online Math Notes: Area Between Curves](https://tutorial.math.lamar.edu/Classes/CalcI/AreaBetweenCurves.aspx), Paul Dawkins (Lamar University) — diện tích hình phẳng (Bài viết, tiếng Anh, 30 phút). Diện tích giữa hai đường cong có ví dụ rõ.
- **Xem thêm:** [MIT 18.01SC Unit 5 Part A: L'Hospital's rule and improper integrals](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-5-exploring-the-infinite/), MIT OpenCourseWare — Unit 5 Part A (Video, tiếng Anh, 60 phút). Bài giảng về tích phân suy rộng, kèm bài tập.

### Hàm nhiều biến và đạo hàm riêng · Luyện Khí tầng 6

`gt_nhieu_bien`

*Hiểu đạo hàm riêng là 'giữ các biến khác cố định'; giới hạn hai biến và hàm ẩn chỉ cần đọc lướt.*

- **Chính:** [MIT 18.02SC Unit 2 Part A: Functions of two variables, tangent approximation and optimization](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/part-a-functions-of-two-variables-tangent-approximation-and-optimization/), MIT OpenCourseWare — sessions 24 tới 31 (đồ thị, đường mức, đạo hàm riêng, xấp xỉ) (Video, tiếng Anh, 2 giờ). Bài giảng đạo hàm riêng và xấp xỉ tuyến tính từng bước, kèm bài tập và đề thi.
- **Xem thêm:** [Paul's Online Math Notes: Partial Derivatives](https://tutorial.math.lamar.edu/Classes/CalcIII/PartialDerivatives.aspx), Paul Dawkins (Lamar University) — đạo hàm riêng, cấp cao (Bài viết, tiếng Anh, 40 phút). Cách tính đạo hàm riêng với nhiều ví dụ giải.
- **Xem thêm:** [OpenStax Calculus Volume 3, chương 4: Differentiation of Functions of Several Variables](https://openstax.org/books/calculus-volume-3/pages/4-introduction), OpenStax (Rice University) — mục 4.1 tới 4.4 (Sách, tiếng Anh). Sách miễn phí, có bài tập kèm đáp án.
- **Luyện tập:** [Paul's Online Math Notes: Functions of Several Variables](https://tutorial.math.lamar.edu/Classes/CalcIII/MultiVrbleFcns.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 20 phút). Bài luyện miền xác định và đồ thị, có lời giải.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.4 Giải tích nhiều biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/multivariable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.4.1 Đạo hàm trong không gian nhiều chiều (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Gradient, Jacobian và lan truyền ngược · Luyện Khí tầng 7

`gt_gradient`

*Đọc Parr và Howard cạnh bài d2l tiếng Việt, tự tính tay một mạng hai lớp; Lagrange chỉ cần một hai bài mẫu.*

- **Chính:** [Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/), Terence Parr, Jeremy Howard — Jacobian, quy tắc dây chuyền, đạo hàm của mạng nơ-ron (Bài viết, tiếng Anh, 90 phút). Nối gradient, Jacobian và quy tắc dây chuyền thành lan truyền ngược, ví dụ từng bước.
- **Xem thêm:** [MIT 18.02SC Unit 2 Part B: Chain rule, gradient and directional derivatives](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/part-b-chain-rule-gradient-and-directional-derivatives/), MIT OpenCourseWare — sessions 32 tới 38 (Video, tiếng Anh, 2 giờ). Gradient vuông góc với đường mức, đạo hàm theo hướng.
- **Xem thêm:** [MIT 18.02SC Unit 2 Part C: Lagrange multipliers](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/), MIT OpenCourseWare — Part C Lagrange Multipliers and Constrained Differentials (Video, tiếng Anh, 90 phút). Cực trị có điều kiện bằng nhân tử Lagrange.
- **Xem thêm:** [Mathematics for Machine Learning (sách miễn phí)](https://mml-book.github.io/book/mml-book.pdf), Deisenroth, Faisal, Ong — chương 5 Vector Calculus, mục 5.3 tới 5.6 (Sách, tiếng Anh). Gradient của hàm vectơ, Jacobian và lan truyền ngược viết cho học máy.
- **Luyện tập:** [Paul's Online Math Notes: Lagrange Multipliers](https://tutorial.math.lamar.edu/Classes/CalcIII/LagrangeMultipliers.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 40 phút). Bài nhân tử Lagrange có lời giải chi tiết.
- **Tiếng Việt:** [Đắm mình vào học sâu, phụ lục toán: 18.4 Giải tích nhiều biến](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_appendix-mathematics-for-deep-learning/multivariable-calculus_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — mục 18.4.2 Gradient, 18.4.4 Quy tắc dây chuyền, 18.4.5 Lan truyền ngược (Sách, tiếng Việt, 30 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Bàng môn: Hàm chẵn, lẻ, tuần hoàn · Luyện Khí

`gt_tinh_chat_ham`

*Chưa tìm được nguồn riêng cho hàm tuần hoàn; chỉ cần biết sin, cos tuần hoàn, hàm chẵn lẻ đối xứng thế nào.*

- **Chính:** [Paul's Online Math Notes: Symmetry (đối xứng, hàm chẵn lẻ)](https://tutorial.math.lamar.edu/Classes/Alg/Symmetry.aspx), Paul Dawkins (Lamar University) — đối xứng qua trục và gốc (Bài viết, tiếng Anh, 15 phút). Giải thích hàm chẵn và lẻ qua đối xứng đồ thị, gọn.

### Bàng môn: Kỹ thuật tính giới hạn và phân loại gián đoạn · Luyện Khí

`gt_gioi_han_nang_cao`

*Bàng môn: làm đủ bài luyện của Paul là xong; vô cùng bé tương đương chưa tìm được nguồn tiếng Anh riêng, xem giáo trình trên lớp.*

- **Chính:** [Paul's Online Math Notes: Computing Limits](https://tutorial.math.lamar.edu/Classes/CalcI/ComputingLimits.aspx), Paul Dawkins (Lamar University) — kỹ thuật tính giới hạn, rút gọn, liên hợp (Bài viết, tiếng Anh, 40 phút). Các kỹ thuật tính giới hạn có nhiều ví dụ giải.
- **Xem thêm:** [MIT 18.01SC, Session 5 Discontinuity và Session 8 Limits of sine and cosine](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-5-discontinuity/), MIT OpenCourseWare — sessions 5 và 8 (Video, tiếng Anh, 40 phút). Phân loại điểm gián đoạn và giới hạn lượng giác đáng nhớ.
- **Xem thêm:** [Paul's Online Math Notes: Continuity](https://tutorial.math.lamar.edu/Classes/CalcI/Continuity.aspx), Paul Dawkins (Lamar University) — liên tục và định lý giá trị trung gian (Bài viết, tiếng Anh, 30 phút). Có cả định lý giá trị trung gian với ví dụ.
- **Luyện tập:** [Paul's Online Math Notes: Limits at Infinity, Part I](https://tutorial.math.lamar.edu/Classes/CalcI/LimitsAtInfinityI.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 25 phút). Giới hạn ở vô cùng có lời giải.

### Bàng môn: Đạo hàm hàm ngược và hàm tham số · Luyện Khí

`gt_ham_nguoc_tham_so`

*Bàng môn: xem chương 7 để hiểu; hàm cho bởi tham số xem Unit 4 Part C của MIT 18.01SC khi cần.*

- **Chính:** [MIT 18.01SC Unit 1 Part B: Implicit differentiation and inverse functions](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-b-implicit-differentiation-and-inverse-functions/), MIT OpenCourseWare — Part B (Video, tiếng Anh, 60 phút). Đạo hàm hàm ngược và hàm ẩn kèm bài tập.
- **Xem thêm:** [Essence of Calculus, chương 7: Implicit differentiation, what's going on here?](https://www.3blue1brown.com/lessons/implicit-differentiation), 3Blue1Brown (Grant Sanderson) — chương 7 (Video, tiếng Anh, 15 phút). Giải thích đạo hàm ẩn và suy ra đạo hàm của ln.
- **Xem thêm:** [Paul's Online Math Notes: Derivatives of Inverse Trig Functions](https://tutorial.math.lamar.edu/Classes/CalcI/DiffInvTrigFcns.aspx), Paul Dawkins (Lamar University) — đạo hàm hàm ngược lượng giác (Bài viết, tiếng Anh, 25 phút). Công thức đạo hàm hàm ngược cụ thể.

### Bàng môn: Định lý giá trị trung bình và L'Hospital · Luyện Khí

`gt_lhospital`

*Bàng môn: học L'Hospital để khử dạng vô định; Rolle, Lagrange chuyển sang đường tự luận vì hay thi chứng minh.*

- **Chính:** [Paul's Online Math Notes: L'Hospital's Rule and Indeterminate Forms](https://tutorial.math.lamar.edu/Classes/CalcI/LHospitalsRule.aspx), Paul Dawkins (Lamar University) — toàn bài (Bài viết, tiếng Anh, 40 phút). Quy tắc và các dạng vô định, có bài luyện kèm lời giải.
- **Xem thêm:** [Paul's Online Math Notes: The Mean Value Theorem](https://tutorial.math.lamar.edu/Classes/CalcI/MeanValueTheorem.aspx), Paul Dawkins (Lamar University) — Rolle và Lagrange (Bài viết, tiếng Anh, 25 phút). Phát biểu và ví dụ cho định lý Rolle và giá trị trung bình.
- **Xem thêm:** [MIT 18.01SC, Sessions 34-35: Mean value theorem](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-2-applications-of-differentiation/part-c-mean-value-theorem-antiderivatives-and-differential-equations/), MIT OpenCourseWare — sessions 34 và 35 (Video, tiếng Anh, 30 phút). Bài giảng ngắn về định lý giá trị trung bình và ứng dụng.

### Bàng môn: Tiệm cận và lược đồ khảo sát hàm số · Luyện Khí

`gt_khao_sat`

*Bàng môn: có thể dùng máy vẽ đồ thị; chỉ cần biết tìm tiệm cận qua giới hạn.*

- **Chính:** [MIT 18.01SC Unit 2 Part A: Approximation and curve sketching](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-2-applications-of-differentiation/part-a-approximation-and-curve-sketching/), MIT OpenCourseWare — Part A (Video, tiếng Anh, 60 phút). Vẽ đồ thị theo lược đồ khảo sát, kèm bài tập.
- **Xem thêm:** [Paul's Online Math Notes: Limits at Infinity, Part I](https://tutorial.math.lamar.edu/Classes/CalcI/LimitsAtInfinityI.aspx), Paul Dawkins (Lamar University) — tiệm cận ngang (Bài viết, tiếng Anh, 25 phút). Giới hạn ở vô cùng chính là tiệm cận ngang.
- **Xem thêm:** [Paul's Online Math Notes: Infinite Limits](https://tutorial.math.lamar.edu/Classes/CalcI/InfiniteLimits.aspx), Paul Dawkins (Lamar University) — tiệm cận đứng (Bài viết, tiếng Anh, 25 phút). Giới hạn vô cùng chính là tiệm cận đứng.

### Bàng môn: Tích phân hàm hữu tỉ và lượng giác · Luyện Khí

`gt_tich_phan_ky_thuat`

*Bàng môn: nặng mẹo, tra khi cần; có Wolfram hoặc SymPy làm hộ.*

- **Chính:** [Paul's Online Math Notes: Partial Fractions](https://tutorial.math.lamar.edu/Classes/CalcII/PartialFractions.aspx), Paul Dawkins (Lamar University) — tích phân hàm hữu tỉ (Bài viết, tiếng Anh, 40 phút). Phân tích thành phân thức đơn giản rồi tích phân, nhiều ví dụ.
- **Xem thêm:** [Paul's Online Math Notes: Integrals Involving Trig Functions](https://tutorial.math.lamar.edu/Classes/CalcII/IntegralsWithTrig.aspx), Paul Dawkins (Lamar University) — tích phân lượng giác (Bài viết, tiếng Anh, 35 phút). Kỹ thuật cho sin, cos mũ.
- **Xem thêm:** [Paul's Online Math Notes: Trig Substitutions](https://tutorial.math.lamar.edu/Classes/CalcII/TrigSubstitutions.aspx), Paul Dawkins (Lamar University) — đổi biến lượng giác (Bài viết, tiếng Anh, 35 phút). Đổi biến lượng giác cho căn.
- **Xem thêm:** [MIT 18.01SC Unit 4 Part A và B: Techniques of integration](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-4-techniques-of-integration/), MIT OpenCourseWare — Part A, Part B (Video, tiếng Anh, 2 giờ). Bài giảng đầy đủ về các kỹ thuật, có bài tập.
- **Luyện tập:** [Paul's Online Math Notes: Integration Strategy](https://tutorial.math.lamar.edu/Classes/CalcII/IntegrationStrategy.aspx), Paul Dawkins (Lamar University) — bài luyện cuối trang (Bài viết, tiếng Anh, 30 phút). Chọn kỹ thuật phù hợp cho một tích phân.

### Bàng môn: Thể tích, độ dài cung và tiêu chuẩn hội tụ · Luyện Khí

`gt_hinh_hoc_tich_phan`

*Bàng môn: học khi cần; tiêu chuẩn hội tụ liên quan tới đường tự luận.*

- **Chính:** [Paul's Online Math Notes: Volumes of Solids of Revolution / Method of Rings](https://tutorial.math.lamar.edu/Classes/CalcI/VolumeWithRings.aspx), Paul Dawkins (Lamar University) — thể tích vật thể tròn xoay (Bài viết, tiếng Anh, 35 phút). Thể tích bằng phương pháp vòng, có hình và ví dụ.
- **Xem thêm:** [Paul's Online Math Notes: Arc Length](https://tutorial.math.lamar.edu/Classes/CalcII/ArcLength.aspx), Paul Dawkins (Lamar University) — độ dài cung (Bài viết, tiếng Anh, 25 phút). Công thức độ dài cung và ví dụ.
- **Xem thêm:** [Paul's Online Math Notes: Comparison Test for Improper Integrals](https://tutorial.math.lamar.edu/Classes/CalcII/ImproperIntegralsCompTest.aspx), Paul Dawkins (Lamar University) — tiêu chuẩn hội tụ (Bài viết, tiếng Anh, 30 phút). Tiêu chuẩn so sánh cho tích phân suy rộng.

### Dạng tự luận hay gặp trong đề cuối kỳ — Giải Tích

Các dạng này không nằm trên chính đạo; chúng là đề của Luận Đạo Đài (`docs/LUAN_DAO_DAI.md`).

| Dạng | Thuộc nút | Hay gặp | Mô tả | Xem ở đâu |
|---|---|---|---|---|
| **Tính đạo hàm bằng định nghĩa** | Đạo hàm và quy tắc dây chuyền | rất hay gặp | Hàm ghép hoặc cho bởi nhiều công thức; dùng định nghĩa xét khả vi tại một điểm và tính đạo hàm ở đó (đạo hàm trái, phải). | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proof of Various Derivative Properties](https://tutorial.math.lamar.edu/Classes/CalcI/DerivativeProofs.aspx); [MIT 18.01SC Exam 1 (đạo hàm) (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/exam-1/) |
| **Xét liên tục và tìm tham số, phân loại gián đoạn** | Bàng môn: Kỹ thuật tính giới hạn và phân loại gián đoạn | rất hay gặp | Cho hàm nhiều công thức chứa tham số; tìm tham số để liên tục hoặc khả vi, phân loại điểm gián đoạn. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Continuity](https://tutorial.math.lamar.edu/Classes/CalcI/Continuity.aspx) |
| **Ứng dụng định lý Rolle và Lagrange** | Bàng môn: Định lý giá trị trung bình và L'Hospital | rất hay gặp | Chứng minh tồn tại điểm c thỏa một đẳng thức, chứng minh phương trình có nghiệm duy nhất hoặc đếm nghiệm bằng Rolle. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proofs of Derivative Applications Facts](https://tutorial.math.lamar.edu/Classes/CalcI/DerivativeAppsProofs.aspx); [MIT 18.01SC Exam 2 (ứng dụng đạo hàm) (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-2-applications-of-differentiation/exam-2/) |
| **Chứng minh bất đẳng thức bằng đạo hàm** | Đơn điệu, cực trị, lồi lõm | rất hay gặp | Xét hàm phụ, dùng tính đơn điệu hoặc lồi lõm để chứng minh bất đẳng thức giữa hàm sơ cấp. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proofs of Derivative Applications Facts](https://tutorial.math.lamar.edu/Classes/CalcI/DerivativeAppsProofs.aspx); [MIT 18.01SC Exam 2 (ứng dụng đạo hàm) (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-2-applications-of-differentiation/exam-2/) |
| **Xét hội tụ tích phân suy rộng** | Diện tích và tích phân cận vô hạn | rất hay gặp | Dùng tiêu chuẩn so sánh hoặc tính trực tiếp để xét hội tụ của tích phân suy rộng, có tham số. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Comparison Test for Improper Integrals](https://tutorial.math.lamar.edu/Classes/CalcII/ImproperIntegralsCompTest.aspx); [MIT 18.01SC Final exam](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/final-exam/) |
| **Giới hạn bằng định nghĩa (epsilon-delta) và giới hạn dãy** | Giới hạn và liên tục | hay gặp | Chứng minh giới hạn bằng định nghĩa, hoặc dùng nguyên lý kẹp và dãy đơn điệu bị chặn để chứng minh dãy hội tụ. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proof of Various Limit Properties](https://tutorial.math.lamar.edu/Classes/CalcI/LimitProofs.aspx); [Paul's Online Math Notes: The Definition of the Limit](https://tutorial.math.lamar.edu/Classes/CalcI/DefnOfLimit.aspx) |
| **Định lý giá trị trung gian** | Bàng môn: Kỹ thuật tính giới hạn và phân loại gián đoạn | hay gặp | Chứng minh phương trình có nghiệm trong một khoảng bằng hàm liên tục trên đoạn. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Continuity](https://tutorial.math.lamar.edu/Classes/CalcI/Continuity.aspx) |
| **Chứng minh bất đẳng thức bằng Lagrange** | Bàng môn: Định lý giá trị trung bình và L'Hospital | hay gặp | Áp dụng định lý giá trị trung bình trên một đoạn để chặn hiệu f(b)-f(a). | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proofs of Derivative Applications Facts](https://tutorial.math.lamar.edu/Classes/CalcI/DerivativeAppsProofs.aspx) |
| **Khai triển Taylor, Maclaurin để tính giới hạn và xấp xỉ** | Khai triển Taylor | hay gặp | Khai triển tới bậc cần thiết để tính giới hạn dạng vô định, hoặc đánh giá sai số xấp xỉ. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Series and Sequences (mục Taylor Series)](https://tutorial.math.lamar.edu/Classes/CalcII/SeriesIntro.aspx); [MIT 18.01SC Final exam](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/final-exam/) |
| **Đạo hàm của tích phân cận biến thiên** | Tích phân | hay gặp | Tính đạo hàm của hàm xác định bởi tích phân, hoặc giới hạn có tích phân bằng định lý cơ bản. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [MIT 18.01SC Exam 3 (tích phân) (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-3-the-definite-integral-and-its-applications/exam-3/) |
| **Chứng minh đẳng thức tích phân** | Tích phân | hay gặp | Dùng đổi biến hoặc đối xứng để chứng minh đẳng thức của tích phân xác định, so sánh hai tích phân. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Proof of Various Integral Properties](https://tutorial.math.lamar.edu/Classes/CalcI/ProofIntProp.aspx); [MIT 18.01SC Exam 3 (tích phân) (có lời giải)](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/unit-3-the-definite-integral-and-its-applications/exam-3/) |
| **Tích phân suy rộng của hàm không bị chặn** | Bàng môn: Thể tích, độ dài cung và tiêu chuẩn hội tụ | hay gặp | Xét hội tụ tích phân có kỳ dị ở một đầu mút, so sánh với 1/x^a. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Improper Integrals](https://tutorial.math.lamar.edu/Classes/CalcII/ImproperIntegrals.aspx) |
| **Giới hạn, liên tục, khả vi của hàm hai biến** | Hàm nhiều biến và đạo hàm riêng | hay gặp | Xét giới hạn và liên tục của hàm hai biến tại gốc, kiểm tra tồn tại đạo hàm riêng và khả vi theo định nghĩa. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [MIT 18.02SC Exam 2 (đạo hàm riêng)](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/exam-2/) |
| **Đạo hàm hàm hợp và hàm ẩn nhiều biến** | Hàm nhiều biến và đạo hàm riêng | hay gặp | Tính đạo hàm riêng của hàm hợp, hàm ẩn; chứng minh một phương trình đạo hàm riêng. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Chain Rule (Calculus III)](https://tutorial.math.lamar.edu/Classes/CalcIII/ChainRule.aspx); [MIT 18.02SC Exam 2 (đạo hàm riêng)](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/exam-2/) |
| **Cực trị tự do và cực trị có điều kiện** | Gradient, Jacobian và lan truyền ngược | rất hay gặp | Tìm điểm dừng, dùng Hessian để phân loại; cực trị có điều kiện bằng nhân tử Lagrange hoặc thế. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf); [Paul's Online Math Notes: Lagrange Multipliers](https://tutorial.math.lamar.edu/Classes/CalcIII/LagrangeMultipliers.aspx); [MIT 18.02SC Exam 2 (đạo hàm riêng)](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/exam-2/) |
| **Đạo hàm cấp n và công thức Leibniz** | Đạo hàm và quy tắc dây chuyền | thỉnh thoảng | Tính đạo hàm cấp cao bằng quy nạp hoặc công thức Leibniz, tính đạo hàm cấp n của hàm hữu tỉ hoặc lượng giác. | [Đề cương học phần MI1111 Giải tích 1 (CTĐT tài năng)](https://fami.hust.edu.vn/wp-content/uploads/MI1111-Decuong-Giaitich1-Tainang.pdf) |

**Đã xem và không chọn:**

- Khan Academy Calculus / Multivariable Calculus: Không mở được trang để kiểm và không có bản tiếng Việt cho môn này; MIT 18.01SC, 18.02SC có đề thi lời giải nên chọn.
- OpenStax Calculus Volume 1 và 2 làm nguồn chính: Sách dày, tốt nhưng dài; chỉ dùng Volume 3 chương 4 cho nhiều biến.
- Calculus của Stewart: Sách thương mại, nặng, không cần cho người học để làm AI.
- Đề thi giải tích chép trên studocu, 123doc: Không chính thức, có thể vi phạm bản quyền; dùng đề minh họa của fami.hust.edu.vn.
- Giáo trình Toán cao cấp (Nguyễn Đình Trí): Sách thương mại, không có bản miễn phí hợp pháp; chỉ nêu tên như sách tham khảo trên lớp.
- Active Calculus: Không kịp kiểm trang; thiên về học qua câu hỏi khám phá, chậm cho người muốn đi nhanh.
- d2l.aivivn.com (trang cũ của Đắm mình vào Học Sâu): Tên miền đã bị chiếm: trang chủ hiện là quảng cáo cờ bạc. Dùng bản dịch tay trên GitHub (thẻ v0.15).
- vi.d2l.ai (Đắm mình vào Học Sâu 0.17.5): Bản dịch máy, sai thuật ngữ (mạng tích chập thành 'mạng thần kinh phức tạp'). Không dùng làm nguồn tiếng Việt.

## Xác Suất và Thống Kê

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Seeing Theory: sáu chương trực quan (Basic Probability đến Regression Analysis)](https://seeing-theory.brown.edu/), Brown University — đọc nhanh từng chương trước khi học nút tương ứng (Tương tác, tiếng Anh, 3 giờ). Kéo thả và xem xác suất, phân phối, suy luận, hồi quy chạy ngay trên màn hình; dựng trực giác rất nhanh.
2. [Introduction to Probability (RES.6-012), 13 bài đầu của Phần I](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/pages/part-i-the-fundamentals/), MIT OpenCourseWare (Tsitsiklis) — Lecture 1 đến 13: mỗi bài chia thành video ngắn 5-10 phút (Khoá học, tiếng Anh, 10 giờ). Video ngắn, giải thích chậm và đúng; mỗi khái niệm một video nên dễ quay lại đúng chỗ cần.
3. [StatQuest: chỉ mục video theo chủ đề](https://statquest.org/video_index.html), Josh Starmer (StatQuest) — các video về MLE, khoảng tin cậy, p-value, tương quan (Video, tiếng Anh). Giải thích thống kê bằng hình và ví dụ rất đơn giản, hợp người đọc tiếng Anh chậm.
4. [Think Stats (bản 3), chương 1-14](https://allendowney.github.io/ThinkStats/), Allen Downey — đọc song song với phần thống kê (ước lượng, kiểm định, hồi quy) (Sách, tiếng Anh). Dạy thống kê bằng code Python trên dữ liệu thật, đúng kiểu vừa học vừa dựng.

### Sự kiện và phép đếm · Luyện Khí tầng 1

`xs_dem_su_kien`

*Xem RES.6-012 bài 1 (không gian mẫu) rồi bài 4 (đếm); bỏ phần 'Mathematical Background' về chuỗi vô hạn và tập đếm được.*

- **Chính:** [RES.6-012 Lecture 4: Counting](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-3/), MIT OpenCourseWare (Tsitsiklis) — bài 4: nguyên lý đếm, tổ hợp, chia nhóm (xem 8 video ngắn) (Video, tiếng Anh, 60 phút). Đi từ nguyên lý nhân đến tổ hợp bằng ví dụ xúc xắc, đồng xu, bài tây; rất sát phần học của nút.
- **Xem thêm:** [RES.6-012 Lecture 1: Sample Space (không gian mẫu)](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/sample-space/), MIT OpenCourseWare — video Sample Space và Sample Space Examples (Video, tiếng Anh, 20 phút). Phép thử, không gian mẫu và sự kiện được nói rõ trước khi đếm.
- **Xem thêm:** [Seeing Theory: Basic Probability](https://seeing-theory.brown.edu/basic-probability/index.html), Brown University — phần Random Variables/Set Theory ở đầu chương (Tương tác, tiếng Anh, 20 phút). Xem quan hệ giữa các sự kiện bằng hình tập hợp.
- **Xem thêm:** [Stat 110 Lecture 1: Probability and Counting](https://stat110.hsites.harvard.edu/youtube), Joe Blitzstein (Harvard) — bài 1 trong danh sách phát (khoảng 46 phút) (Video, tiếng Anh, 46 phút). Cách nghĩ bằng câu chuyện về phép đếm; hay nhưng nhanh hơn RES.6-012.
- **Luyện tập:** [18.05 Class 1: Counting and Sets (bài đọc kèm câu hỏi)](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class01-prep-a_pdf/), MIT OpenCourseWare — bài chuẩn bị 1a; đáp án nằm ở trang problem sets của khóa (Bài tập, tiếng Anh, 40 phút). Bài tập đếm cỡ đại học năm nhất, có lời giải để đối chiếu.
- **Tiếng Việt:** [OpenIntro Statistics (bản dịch tiếng Việt), chương 3: Xác suất](https://www.openintro.org/go?id=os4_vn_ch3), OpenIntro — chương 3, các mục xác suất và sự kiện (Sách, tiếng Việt, 60 phút). Trang sách nói có bản dịch tiếng Việt chương 1-6; chưa mở được bản PDF để kiểm tra chất lượng dịch.

### Xác suất · Luyện Khí tầng 2

`xs_xac_suat`

*Chơi Seeing Theory chương 1 trước; sau đó mới làm bài tập đếm kiểu bốc bi, bốc bài.*

- **Chính:** [Seeing Theory: Basic Probability](https://seeing-theory.brown.edu/basic-probability/index.html), Brown University — Chapter 1: xác suất cổ điển và luật số lớn bằng mô phỏng (Tương tác, tiếng Anh, 30 phút). Tung xúc xắc hàng nghìn lần và thấy tần suất tiến tới xác suất; đúng ý tưởng 'định nghĩa thống kê'.
- **Xem thêm:** [RES.6-012 Lecture 1: Probability Axioms và tính chất đơn giản](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/probability-axioms/), MIT OpenCourseWare — các video Probability Axioms, Simple Properties of Probabilities (Video, tiếng Anh, 30 phút). Tính chất của xác suất và sự kiện đối được suy ra gọn từ ba tiên đề.
- **Xem thêm:** [Think Stats, chương 2: Distributions](https://allendowney.github.io/ThinkStats/chap02.html), Allen Downey — tần suất và histogram trên dữ liệu (Sách, tiếng Anh, 40 phút). Nối tần suất với xác suất bằng code trên dữ liệu thật.
- **Luyện tập:** [18.05 Class 2: Probability, Terminology and Examples](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class02-prep_pdf/), MIT OpenCourseWare — bài đọc chuẩn bị lớp 2 (Bài tập, tiếng Anh, 40 phút). Có bài tập xác suất cổ điển và lấy có/không hoàn lại.
- **Tiếng Việt:** [Bài tập Xác suất thống kê MI2020 (Bách khoa Hà Nội), chương 1](https://fami.hust.edu.vn/wp-content/uploads/2023_MI2020_Baitap_Xacsuatthongke_DHCQ.pdf), Viện Toán ứng dụng và Tin học, ĐHBK Hà Nội — chương 1 về biến cố và xác suất (Bài tập, tiếng Việt, 60 phút). Bài tập tiếng Việt đúng khung học phần của trường; chưa xác minh có đáp số hay không.

### Xác suất có điều kiện và độc lập · Luyện Khí tầng 3

`xs_dieu_kien`

*Xem bài 2 đến Multiplication Rule rồi bài 3; công thức Bernoulli học trong bài 4 (nhị thức) của RES.6-012.*

- **Chính:** [RES.6-012 Lecture 2: Conditioning and Bayes' Rule (phần xác suất có điều kiện)](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-1/), MIT OpenCourseWare (Tsitsiklis) — bài 2: các video đến Multiplication Rule (Video, tiếng Anh, 45 phút). Xác suất có điều kiện được dựng chậm từ ví dụ xúc xắc và radar, rồi đến quy tắc nhân.
- **Xem thêm:** [RES.6-012 Lecture 3: Independence](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-2/), MIT OpenCourseWare — bài 3: độc lập hai sự kiện, độc lập có điều kiện (Video, tiếng Anh, 50 phút). Phân biệt độc lập và độc lập từng đôi; có ví dụ độ tin cậy hệ thống.
- **Xem thêm:** [Seeing Theory: Compound Probability](https://seeing-theory.brown.edu/compound-probability/index.html), Brown University — mục Conditional Probability và Independence (Tương tác, tiếng Anh, 20 phút). Xem điều kiện thu hẹp không gian mẫu thế nào.
- **Xem thêm:** [StatQuest: Conditional probability](https://youtu.be/_IgyaD7vOOA), Josh Starmer — video ngắn về xác suất có điều kiện (Video, tiếng Anh, 10 phút). Bản giải thích rất nhẹ nếu cần nhắc lại.
- **Luyện tập:** [18.05 Class 3: Conditional Probability, Independence, Bayes' Theorem](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class03-prep_pdf/), MIT OpenCourseWare — bài đọc chuẩn bị lớp 3 (Bài tập, tiếng Anh, 45 phút). Bài tập có điều kiện và độc lập; gần với nút kế tiếp là Bayes.

### Xác suất đầy đủ và Bayes · Luyện Khí tầng 4

`xs_bayes`

*Xem video 3Blue1Brown trước để có hình, rồi làm một bảng Bayes tay với số xét nghiệm; bỏ phần Bayes liên tục.*

- **Chính:** [Bayes theorem, the geometry of changing beliefs](https://www.3blue1brown.com/lessons/bayes-theorem), 3Blue1Brown (Grant Sanderson) — cả video (khoảng 15 phút) (Video, tiếng Anh, 15 phút). Dùng hình vuông 1x1 để thấy công thức Bayes và sai lầm bỏ quên tỉ lệ nền.
- **Xem thêm:** [RES.6-012 Lecture 2: Total Probability Theorem và Bayes' Rule](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/total-probability-theorem/), MIT OpenCourseWare — video Total Probability Theorem, rồi Bayes' Rule (Video, tiếng Anh, 25 phút). Công thức xác suất đầy đủ và Bayes có sơ đồ cây, đúng thứ tự của nút.
- **Xem thêm:** [Think Bayes (bản 2), chương 1-2: Probability, Bayes's Theorem](https://allendowney.github.io/ThinkBayes2/chap02.html), Allen Downey — chương 1 và 2 (Sách, tiếng Anh, 60 phút). Cài đặt Bayes bằng bảng trong Python, rất gần việc tự dựng bộ phân loại sau này.
- **Xem thêm:** [StatQuest: Bayes' Theorem](https://youtu.be/9wCnvr7Xw4E), Josh Starmer — toàn video (Video, tiếng Anh, 15 phút). Ví dụ đếm số người thay vì công thức; dễ đọc phụ đề.
- **Luyện tập:** [18.05 Class 3 (phần Bayes) và Class 11: Bayesian Updating with Discrete Priors](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class11-prep_pdf/), MIT OpenCourseWare — bài đọc lớp 11, bảng cập nhật Bayes (Bài tập, tiếng Anh, 40 phút). Có bảng Bayes từng bước để tự làm lại với số khác.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 30: Ôn tập Xác suất cho Machine Learning](https://machinelearningcoban.com/2017/07/09/prob/), Vũ Hữu Tiệp — mục 2.4 xác suất có điều kiện và 2.5 quy tắc Bayes (Bài viết, tiếng Việt, 25 phút). Tóm tắt tiếng Việt đúng ngữ cảnh học máy; ngắn nhưng ít ví dụ.

### Biến ngẫu nhiên rời rạc · Luyện Khí tầng 5

`xs_bnn_roi_rac`

*Xem bài 5 rồi video CDF ở bài 8; có thể bỏ hai video Supplement: Functions.*

- **Chính:** [RES.6-012 Lecture 5: Discrete Random Variables, Part I](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-4/), MIT OpenCourseWare (Tsitsiklis) — bài 5: biến ngẫu nhiên, bảng phân phối (PMF), Bernoulli, nhị thức (Video, tiếng Anh, 60 phút). Định nghĩa biến ngẫu nhiên và PMF rõ ràng; hàm phân phối F(x) xem tiếp ở bài 8.
- **Xem thêm:** [Think Stats, chương 3-4: Probability Mass Functions và Cumulative Distribution Functions](https://allendowney.github.io/ThinkStats/chap04.html), Allen Downey — chương 3 và 4 (CDF) (Sách, tiếng Anh, 60 phút). Vẽ PMF và CDF của dữ liệu thật bằng code; dễ nhớ F(x).
- **Xem thêm:** [RES.6-012: Cumulative Distribution Functions](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/cumulative-distribution-functions/), MIT OpenCourseWare — video CDF trong bài 8 (Video, tiếng Anh, 10 phút). Hàm phân phối tích lũy cho cả rời rạc và liên tục.
- **Luyện tập:** [18.05 Class 4: Discrete Random Variables, Expected Value](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class04-prep-a_pdf/), MIT OpenCourseWare — bài đọc 4a (Bài tập, tiếng Anh, 40 phút). Câu hỏi về bảng phân phối và hàm phân phối.

### Biến ngẫu nhiên liên tục và hàm mật độ · Luyện Khí tầng 6

`xs_bnn_lien_tuc`

*Chỉ cần video Probability Density Functions, Uniform & Piecewise Constant, rồi CDF; hai mục Conditioning và Joint để dành.*

- **Chính:** [RES.6-012 Lecture 8: Continuous Random Variables, Part I](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-7/), MIT OpenCourseWare (Tsitsiklis) — bài 8: hàm mật độ, phân phối đều, mũ, chuẩn (Video, tiếng Anh, 65 phút). Giải thích 'xác suất là diện tích dưới đường cong' và vì sao một điểm có xác suất 0.
- **Xem thêm:** [Seeing Theory: Probability Distributions](https://seeing-theory.brown.edu/probability-distributions/index.html), Brown University — phần Continuous Distributions (Tương tác, tiếng Anh, 20 phút). Kéo tham số và xem diện tích thay đổi.
- **Xem thêm:** [Think Stats, chương 6: Probability Density Functions](https://allendowney.github.io/ThinkStats/chap06.html), Allen Downey — cả chương (Sách, tiếng Anh, 40 phút). Ước lượng hàm mật độ từ dữ liệu bằng code.
- **Luyện tập:** [18.05 Class 5: Continuous RVs, bài đọc 5b-5c](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class05-prep-b_pdf/), MIT OpenCourseWare — bài đọc 5b (Bài tập, tiếng Anh, 40 phút). Bài tập tích phân hàm mật độ tính xác suất trong khoảng.

### Kỳ vọng, phương sai và các phân phối quen thuộc · Luyện Khí tầng 7

`xs_ky_vong_phan_phoi`

*Làm tuần tự kỳ vọng, phương sai, nhị thức, đều, mũ, chuẩn; Poisson xem thêm video ngắn ở Seeing Theory hoặc 18.05.*

- **Chính:** [RES.6-012 Lecture 5-6: Expectation, Variance (và Binomial, Geometric)](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-5/), MIT OpenCourseWare (Tsitsiklis) — bài 6 (Variance) sau phần Expectation của bài 5; rồi Exponential và Normal trong bài 8 (Video, tiếng Anh, 90 phút). Kỳ vọng, phương sai và từng phân phối được dựng bằng ví dụ; có cả tính kỳ vọng nhị thức bằng tuyến tính.
- **Xem thêm:** [StatQuest: Expected value, phần 1 (rời rạc) và phần 2 (liên tục)](https://youtu.be/KLs_7b7SKi4), Josh Starmer — phần 1 rồi phần 2 (youtu.be/OSPr6G6Ka-U) (Video, tiếng Anh, 20 phút). Kỳ vọng như 'trung bình có trọng số', ví dụ rất gần đời sống.
- **Xem thêm:** [StatQuest: The Normal Distribution](https://youtu.be/rzFX5NWojp0), Josh Starmer — toàn video (Video, tiếng Anh, 12 phút). Phân phối chuẩn và độ lệch chuẩn bằng hình.
- **Xem thêm:** [Seeing Theory: Probability Distributions](https://seeing-theory.brown.edu/probability-distributions/index.html), Brown University — kỳ vọng, phương sai, và các phân phối quen thuộc (Tương tác, tiếng Anh, 30 phút). Chơi với nhị thức, Poisson, chuẩn và xem kỳ vọng, phương sai đổi theo tham số.
- **Luyện tập:** [18.05 Class 5: Variance and Gallery of Continuous RVs](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class05-prep-a_pdf/), MIT OpenCourseWare — bài đọc 5a, 5c (Bài tập, tiếng Anh, 40 phút). Bảng các phân phối thường gặp kèm bài tập.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 30: Ôn tập Xác suất cho Machine Learning](https://machinelearningcoban.com/2017/07/09/prob/), Vũ Hữu Tiệp — mục 2.7 kỳ vọng và mục 3 các phân phối thường gặp (Bài viết, tiếng Việt, 30 phút). Chuẩn, Bernoulli, categorical, tiếng Việt, ngắn; không có Poisson hay phân phối mũ.

### Mẫu, ước lượng và hợp lý cực đại · Luyện Khí tầng 8

`xs_mau_uoc_luong`

*Hiểu MLE bằng ví dụ đồng xu trước; ước lượng điểm không chệch học bằng video N trừ 1 và mô phỏng của Think Stats.*

- **Chính:** [Maximum Likelihood (StatQuest)](https://youtu.be/XepXtl9YKwc), Josh Starmer — toàn video; sau đó xem ví dụ chuẩn youtu.be/Dn6b9fCIUpM (Video, tiếng Anh, 25 phút). Cho thấy 'chọn tham số làm dữ liệu dễ xảy ra nhất' bằng cách trượt đường cong chuẩn.
- **Xem thêm:** [18.05 Class 10: Introduction to Statistics; Maximum Likelihood Estimates](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class10-prep-a_pdf/), MIT OpenCourseWare — bài đọc 10a và 10b (Bài viết, tiếng Anh, 45 phút). Các bước viết hàm hợp lý, lấy log, đạo hàm, rất đúng thứ tự cần nhớ.
- **Xem thêm:** [StatQuest: Vì sao chia cho N trừ 1 (ước lượng phương sai)](https://youtu.be/sHRBg6BhKjI), Josh Starmer — toàn video (Video, tiếng Anh, 10 phút). Cho thấy vì sao chia cho N làm ước lượng lệch; đúng ý 'không chệch'.
- **Xem thêm:** [Think Stats, chương 8: Estimation](https://allendowney.github.io/ThinkStats/chap08.html), Allen Downey — cả chương (Sách, tiếng Anh, 45 phút). Mô phỏng phân phối của trung bình mẫu và so ước lượng chệch với không chệch.
- **Luyện tập:** [StatQuest: MLE cho phân phối nhị thức và mũ](https://youtu.be/4KKV9yZCoM4), Josh Starmer — ví dụ nhị thức; mũ ở youtu.be/p3T-_LMrvBc (Video, tiếng Anh, 25 phút). Hai ví dụ tự làm lại được trên giấy.
- **Tiếng Việt:** [Đề cương Xác suất thống kê MI2020 (Bách khoa Hà Nội), chương 4: ước lượng](https://fami.hust.edu.vn/wp-content/uploads/2024_MI2020_Xacsuatthongke_DHCQ_Final.pdf), Viện Toán ứng dụng và Tin học, ĐHBK Hà Nội — chương 4 trong đề cương (Bài viết, tiếng Việt). Để biết trường dạy nội dung nào; đề cương không phải giáo trình nên chỉ dùng để đối chiếu.

### Hiệp phương sai, tương quan và hồi quy · Luyện Khí tầng 8

`xs_tuong_quan_hoi_quy`

*Xem tương quan trước, hồi quy đơn sau; bài ML cơ bản chỉ đọc khi đã có tuyến tính.*

- **Chính:** [RES.6-012 Lecture 12: Covariance and Correlation](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-11/), MIT OpenCourseWare (Tsitsiklis) — bài 12: các video Covariance đến Interpreting the Correlation Coefficient (Video, tiếng Anh, 60 phút). Dựng hiệp phương sai và hệ số tương quan từ định nghĩa, có ví dụ vì sao tương quan quan trọng.
- **Xem thêm:** [StatQuest: Covariance và Pearson's correlation](https://youtu.be/qtaqvPAeEJY), Josh Starmer — covariance; sau đó correlation youtu.be/xZ_z8KWkhXE (Video, tiếng Anh, 25 phút). Hình ảnh trực quan trước khi xem công thức.
- **Xem thêm:** [StatQuest: Linear Regression (least squares)](https://youtu.be/PaFPbb66DxQ), Josh Starmer — toàn video (Video, tiếng Anh, 25 phút). Thấy vì sao đường hồi quy là đường làm tổng bình phương sai số nhỏ nhất.
- **Xem thêm:** [Seeing Theory: Regression Analysis](https://seeing-theory.brown.edu/regression-analysis/index.html), Brown University — cả chương (Tương tác, tiếng Anh, 20 phút). Kéo điểm dữ liệu và xem đường hồi quy dịch chuyển.
- **Luyện tập:** [18.05 Class 26: Linear Regression](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class26-prep_pdf/), MIT OpenCourseWare — bài đọc lớp 26 (Bài tập, tiếng Anh, 45 phút). Hồi quy bình phương tối thiểu có công thức đầy đủ và bài tập.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 3: Linear Regression](https://machinelearningcoban.com/2016/12/28/linearregression/), Vũ Hữu Tiệp — toàn bài: hàm mất mát, nghiệm, ví dụ Python (Bài viết, tiếng Việt, 40 phút). Hồi quy như mô hình học máy đầu tiên, có code NumPy; dùng ma trận nên cần đại số tuyến tính.

### Khoảng tin cậy và định lý giới hạn trung tâm · Luyện Khí tầng 9

`xs_tin_cay`

*Luật số lớn và CLT bằng video; sau đó mới làm công thức khoảng tin cậy và cỡ mẫu.*

- **Chính:** [But what is the Central Limit Theorem?](https://www.3blue1brown.com/lessons/clt), 3Blue1Brown (Grant Sanderson) — cả video (khoảng 31 phút) (Video, tiếng Anh, 31 phút). Thấy tổng nhiều biến bất kỳ tiến dần tới hình chuông; nền cho khoảng tin cậy.
- **Xem thêm:** [StatQuest: Confidence Intervals](https://youtu.be/TqOeMYtOc1w), Josh Starmer — toàn video (Video, tiếng Anh, 20 phút). Khoảng tin cậy và ý nghĩa 'tin cậy 95%' bằng ví dụ lấy mẫu lặp.
- **Xem thêm:** [18.05 Class 22-23: Confidence Intervals](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class22-prep_pdf/), MIT OpenCourseWare — bài đọc lớp 22 rồi lớp 23 (Bài viết, tiếng Anh, 60 phút). Công thức khoảng tin cậy cho trung bình, có cả khi không chuẩn.
- **Xem thêm:** [StatQuest: Central Limit Theorem (có app thử)](https://youtu.be/YAlJCEDH2uY), Josh Starmer — toàn video (Video, tiếng Anh, 15 phút). Bản ngắn hơn 3Blue1Brown, kèm app mô phỏng.
- **Luyện tập:** [Seeing Theory: Frequentist Inference](https://seeing-theory.brown.edu/frequentist-inference/index.html), Brown University — mục Confidence Intervals (Tương tác, tiếng Anh, 20 phút). Tự lấy mẫu và đếm bao nhiêu khoảng chứa trung bình thật.
- **Tiếng Việt:** [Bài tập Xác suất thống kê MI2021 (Bách khoa Hà Nội)](https://fami.hust.edu.vn/wp-content/uploads/2023_MI2021_BaitapXSTK_1.0.pdf), Viện Toán ứng dụng và Tin học, ĐHBK Hà Nội — chương ước lượng khoảng (Bài tập, tiếng Việt, 60 phút). Bài tập khoảng tin cậy trung bình và tỷ lệ theo khung trường; chưa xác minh đáp số.

### Kiểm định giả thuyết · Luyện Khí tầng 9

`xs_kiem_dinh`

*Hiểu p-value và hai loại sai lầm bằng video trước; làm kiểm định một mẫu, rồi hai mẫu; phiên bản hoán vị của Think Stats tùy chọn.*

- **Chính:** [StatQuest: p-values, what they are and how to interpret them](https://youtu.be/vemZtEM63GY), Josh Starmer — toàn video; sau đó Null hypothesis youtu.be/0oc49DyA3hU (Video, tiếng Anh, 25 phút). Giải thích kiểm định như 'có đáng ngạc nhiên không' mà không cần công thức dày.
- **Xem thêm:** [18.05 Class 17-19: NHST I, II, III](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class17-prep-a_pdf/), MIT OpenCourseWare — bài đọc 17a, 17b, rồi 18 và 19 (Bài viết, tiếng Anh, 75 phút). Giả thuyết, mức ý nghĩa, hai loại sai lầm viết rất gọn và đúng.
- **Xem thêm:** [Think Stats, chương 9: Hypothesis Testing](https://allendowney.github.io/ThinkStats/chap09.html), Allen Downey — cả chương (Sách, tiếng Anh, 45 phút). Kiểm định bằng hoán vị, tức là tự dựng từ mô phỏng, đúng kiểu vừa học vừa làm.
- **Xem thêm:** [OpenIntro Statistics, chương 6-7: Inference for Categorical / Numerical Data](https://www.openintro.org/book/os/), OpenIntro — chương 6 (tỷ lệ) và chương 7 (trung bình, so sánh hai nhóm) (Sách, tiếng Anh, 2 giờ). Sách miễn phí có bài tập cuối chương, bao đủ kiểm định một và hai mẫu.
- **Luyện tập:** [Seeing Theory: Frequentist Inference (Hypothesis Testing)](https://seeing-theory.brown.edu/frequentist-inference/index.html), Brown University — phần giả thuyết (Tương tác, tiếng Anh, 20 phút). Chạy thử vùng bác bỏ và sai lầm loại I.
- **Tiếng Việt:** [Minh họa đề giữa kỳ MI2020 học kỳ 2023.1](https://fami.hust.edu.vn/wp-content/uploads/Minhhoa_GK1_2023.1_MI2020.pdf), Viện Toán ứng dụng và Tin học, ĐHBK Hà Nội — đề minh họa giữa kỳ (không phải đề cuối kỳ) (Đề thi, tiếng Việt, 30 phút). Cho thấy dạng đề của trường; chỉ là giữa kỳ nên ít về kiểm định.

### Bàng môn: Hàm của biến ngẫu nhiên · Luyện Khí

`xs_ham_bnn`

*Chỉ cần ba video đầu của bài 11 trước; phần nhiều biến để dành khi học mô hình sinh.*

- **Chính:** [RES.6-012 Lecture 11: Derived Distributions](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-10/), MIT OpenCourseWare (Tsitsiklis) — bài 11: PMF của hàm, hàm tuyến tính của biến chuẩn, phương pháp đơn điệu (Video, tiếng Anh, 60 phút). Đúng chủ đề 'hàm của biến ngẫu nhiên', đi từ rời rạc tới liên tục và có phần mô phỏng.
- **Xem thêm:** [RES.6-012: The Monotonic Case](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/the-monotonic-case/), MIT OpenCourseWare — video trong bài 11 (Video, tiếng Anh, 10 phút). Công thức đổi biến cho hàm đơn điệu, hữu ích về sau với mô hình sinh.

### Dạng tự luận hay gặp trong đề cuối kỳ — Xác Suất và Thống Kê

Các dạng này không nằm trên chính đạo; chúng là đề của Luận Đạo Đài (`docs/LUAN_DAO_DAI.md`).

| Dạng | Thuộc nút | Hay gặp | Mô tả | Xem ở đâu |
|---|---|---|---|---|
| **Trình bày đầy đủ một bài kiểm định giả thuyết** | Kiểm định giả thuyết | rất hay gặp | Cho số liệu mẫu; nêu giả thuyết và đối thuyết, chọn thống kê kiểm định, tính giá trị quan sát, so với miền bác bỏ hoặc p-value và kết luận bằng lời. | [Bài tập Xác suất thống kê MI2020, chương kiểm định](https://fami.hust.edu.vn/wp-content/uploads/2023_MI2020_Baitap_Xacsuatthongke_DHCQ.pdf) |
| **Dựng và giải thích khoảng tin cậy** | Khoảng tin cậy và định lý giới hạn trung tâm | rất hay gặp | Tìm khoảng tin cậy cho trung bình hoặc tỷ lệ ở mức cho trước, tìm cỡ mẫu tối thiểu, và giải thích ý nghĩa của mức tin cậy. | [Bài tập Xác suất thống kê MI2021](https://fami.hust.edu.vn/wp-content/uploads/2023_MI2021_BaitapXSTK_1.0.pdf) |
| **Xác suất đầy đủ và Bayes, trình bày lời giải đầy đủ** | Xác suất đầy đủ và Bayes | rất hay gặp | Bài toán nhiều giai đoạn hoặc nhiều nguồn: đặt hệ biến cố đầy đủ, viết công thức xác suất đầy đủ, rồi tính xác suất hậu nghiệm bằng Bayes. | [18.05 Class 3: Conditional Probability, Independence, Bayes' Theorem](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class03-prep_pdf/) |
| **Tính kỳ vọng và phương sai của một phân phối** | Kỳ vọng, phương sai và các phân phối quen thuộc | rất hay gặp | Cho bảng phân phối hoặc hàm mật độ, tính kỳ vọng và phương sai; hoặc suy ra E và Var của nhị thức, Poisson, mũ, đều từ định nghĩa. | [RES.6-012 Lecture 6: Variance](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-5/) |
| **Tìm hằng số chuẩn hóa và hàm phân phối từ hàm mật độ** | Biến ngẫu nhiên liên tục và hàm mật độ | rất hay gặp | Cho hàm mật độ có tham số; tìm tham số cho tổng xác suất bằng 1, lập hàm phân phối F(x), tính xác suất một khoảng, kỳ vọng. | [18.05 Class 5: Continuous RVs, bài đọc 5b](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class05-prep-b_pdf/) |
| **Chứng minh hoặc kiểm tra hai biến cố độc lập** | Xác suất có điều kiện và độc lập | hay gặp | Dùng định nghĩa P(AB)=P(A)P(B) để kết luận độc lập hay không; chứng minh phần bù của biến cố độc lập cũng độc lập. | [RES.6-012 Lecture 3: Independence](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/independence-of-event-complements/) |
| **Chứng minh ước lượng không chệch** | Mẫu, ước lượng và hợp lý cực đại | hay gặp | Chứng minh trung bình mẫu là ước lượng không chệch của kỳ vọng; chứng minh phương sai mẫu chia cho n-1 là không chệch (hoặc chia cho n thì chệch). | [StatQuest: vì sao chia cho N trừ 1](https://youtu.be/sHRBg6BhKjI) |
| **Tìm ước lượng hợp lý cực đại** | Mẫu, ước lượng và hợp lý cực đại | hay gặp | Viết hàm hợp lý của mẫu, lấy logarit, đạo hàm theo tham số, giải ra ước lượng cho tham số của nhị thức, Poisson, mũ hoặc chuẩn. | [18.05 Class 10: Maximum Likelihood Estimates](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class10-prep-b_pdf/) |
| **Suy ra tính chất xác suất từ tiên đề** | Xác suất | thỉnh thoảng | Chứng minh P(A^c)=1-P(A), P(A∪B)=P(A)+P(B)-P(AB), hoặc bất đẳng thức Bonferroni từ ba tiên đề. | [RES.6-012 Lecture 1: Bonferroni's Inequality và More Properties](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/more-properties-of-probabilities/) |
| **Tính chất hiệp phương sai và tương quan** | Hiệp phương sai, tương quan và hồi quy | hay gặp | Chứng minh Var(X+Y)=Var X + Var Y + 2Cov(X,Y); chỉ ra độc lập suy ra không tương quan nhưng ngược lại không đúng; chứng minh |ρ| ≤ 1. | [RES.6-012 Lecture 12: Proof of Key Properties of the Correlation Coefficient](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/proof-of-key-properties-of-the-correlation-coefficient/) |
| **Suy ra hệ số hồi quy bình phương tối thiểu** | Hiệp phương sai, tương quan và hồi quy | hay gặp | Cực tiểu hóa tổng bình phương sai số theo hệ số góc và hệ số chặn, rút ra công thức qua hiệp phương sai và phương sai. | [18.05 Class 26: Linear Regression](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class26-prep_pdf/) |
| **Dùng bất đẳng thức Chebyshev và luật số lớn** | Khoảng tin cậy và định lý giới hạn trung tâm | thỉnh thoảng | Dùng Chebyshev để chặn xác suất lệch khỏi kỳ vọng, và nêu luật số lớn cho dãy biến độc lập cùng phân phối. | [MIT 6.042 (Mathematics for Computer Science), Lecture 24: Large Deviations](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Hai loại sai lầm và lực kiểm định** | Kiểm định giả thuyết | hay gặp | Tính xác suất sai lầm loại I, loại II và lực kiểm định cho một quy tắc quyết định đã cho; nêu ý nghĩa của mức ý nghĩa. | [18.05 Class 17: The Frequentist School of Statistics; NHST I](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/resources/mit18_05_s22_class17-prep-b_pdf/) |
| **Giải thích phép đếm bằng lời** | Sự kiện và phép đếm | hay gặp | Đếm số cách bằng quy tắc cộng, nhân, hoán vị, tổ hợp và giải thích vì sao chọn công thức đó; chứng minh đẳng thức tổ hợp bằng cách đếm hai lần. | [RES.6-012 Lecture 4: Counting](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-3/) |
| **Tìm phân phối của Y=g(X)** | Bàng môn: Hàm của biến ngẫu nhiên | thỉnh thoảng | Dùng hàm phân phối để tìm hàm mật độ của Y=g(X) khi X liên tục, kể cả trường hợp g không đơn điệu. | [RES.6-012 Lecture 11: A Nonmonotonic Example](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/a-nonmonotonic-example/) |

**Đã xem và không chọn:**

- Harvard Stat 110 (Blitzstein) làm nguồn chính: Rất hay nhưng nhanh và nhiều chứng minh, có tới 35 bài giảng; để dành cho đường tiểu luận, không hợp làm nguồn chính cho người mới. Trang chính của khóa chặn truy cập tự động nên chưa kiểm tra được.
- Khan Academy Statistics and Probability: Không có bản liên kết kiểm chứng được trong lần tìm này; nội dung giống Seeing Theory và StatQuest nên không cần thêm.
- Các trang tải đề thi XSTK trên studocu, 123doc, tailieu: Tài liệu người dùng tải lên, không rõ bản quyền; chỉ dùng nguồn chính thức của trường.
- Think Bayes đầy đủ 20 chương: Chỉ cần chương 1-2 cho nút Bayes; các chương sau thuộc suy luận Bayes nâng cao, ngoài phạm vi nhánh này.
- OpenIntro Statistics làm nguồn chính cho từng nút: Sách dày, tiếng Anh dài; dùng làm tra cứu cho chương 6-7 chứ không đọc từ đầu.
- Machine Learning cơ bản bài về MLE/MAP: Đường dẫn dự đoán trả về lỗi 404 khi thử, nên không đưa vào.

## Thuật Toán và Tối Ưu

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Algorithms (sách miễn phí), các chương Backtracking, Greedy, Graph, MST, Shortest Paths, Max Flow](https://jeffe.cs.illinois.edu/teaching/algorithms/), Jeff Erickson (UIUC) — chương 2, 4, 5, 7, 8, 10 (mỗi chương một PDF) (Sách, tiếng Anh). Sách miễn phí, giải thích thuật toán đồ thị và quay lui rất rõ, có bài tập cuối chương.
2. [Introduction to Algorithms (6.006), bài giảng mùa xuân 2020](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/video_galleries/lecture-videos/), MIT OpenCourseWare (Demaine, Devadas, Solomon) — bài 9 đến 13: BFS, DFS, đường đi ngắn nhất (Khoá học, tiếng Anh, 5 giờ). Video giảng đường rõ ràng, tập trung vào đồ thị và đường đi ngắn nhất.
3. [Machine Learning cơ bản: bài 7 (Gradient Descent), bài 16 (tập lồi, hàm lồi), bài 18 (Duality)](https://machinelearningcoban.com/2017/03/12/convexity/), Vũ Hữu Tiệp — ba bài nối tiếp cho nửa tối ưu của nhánh (Bài viết, tiếng Việt, 2 giờ). Tối ưu lồi, hạ gradient và đối ngẫu bằng tiếng Việt, đúng ngữ cảnh học máy.
4. [Discrete Mathematics: An Open Introduction](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — chương Counting, Logic, Graph Theory (Sách, tiếng Anh). Sách miễn phí, viết cho người mới, có bài tập; hợp cho phần logic, đếm và đồ thị.

### Logic mệnh đề và quy tắc đếm · Luyện Khí tầng 1

`tr_logic_dem`

*Học logic mệnh đề bằng bảng chân trị trước, rồi quy tắc cộng, nhân; bỏ phần quantifier phức tạp nếu thấy khó.*

- **Chính:** [Discrete Mathematics: An Open Introduction, chương Logic và Counting](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — mục Logic (mệnh đề, bảng chân trị) và đầu chương Counting (quy tắc cộng, nhân) (Sách, tiếng Anh, 3 giờ). Viết nhẹ nhàng cho người mới, có ví dụ và bài tập; chưa mở được từng mục để ghi mục số chính xác.
- **Xem thêm:** [MIT 6.1200J Mathematics for Computer Science: bài 1 Predicates, Sets, and Proofs](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 01: các mục 1.0 đến 1.7 của sách (Khoá học, tiếng Anh, 90 phút). Mệnh đề và logic trong ngữ cảnh khoa học máy tính.
- **Xem thêm:** [RES.6-012 Lecture 4: Counting](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/lecture-overview-3/), MIT OpenCourseWare — nguyên lý đếm (Video, tiếng Anh, 40 phút). Quy tắc nhân, hoán vị, tổ hợp qua video ngắn.

### Đếm và hệ thức truy hồi · Luyện Khí tầng 2

`tr_dem`

*Làm đếm trước, hệ thức truy hồi sau; bỏ phương pháp hàm sinh.*

- **Chính:** [Discrete Mathematics: An Open Introduction, chương Counting và Sequences](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — mục hoán vị, tổ hợp và recurrence relations (Sách, tiếng Anh, 4 giờ). Dạy đếm bằng bài tập nhiều, rồi hệ thức truy hồi; chưa ghi mục số.
- **Xem thêm:** [MIT 6.1200J: bài 7 Recurrences (mục 22.1 đến 22.5) và bài 16 Counting Techniques](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 07 và Lecture 16 (Khoá học, tiếng Anh, 2 giờ). Giải hệ thức truy hồi và các kỹ thuật đếm; hơi hàn lâm.
- **Xem thêm:** [CP-Algorithms: Binomial Coefficients](https://cp-algorithms.com/combinatorics/binomial-coefficients.html), CP-Algorithms — cả trang (Bài viết, tiếng Anh, 25 phút). Tổ hợp và tính nhanh bằng code.
- **Xem thêm:** [Algorithms, chương 1: Recursion](https://jeffe.cs.illinois.edu/teaching/algorithms/book/01-recursion.pdf), Jeff Erickson — phần giải hệ thức truy hồi của thuật toán chia để trị (Sách, tiếng Anh, 60 phút). Nối hệ thức truy hồi với đệ quy trong code.

### Liệt kê và quay lui · Luyện Khí tầng 3

`tr_liet_ke_quay_lui`

*Đọc Erickson chương 2 và tự viết N quân hậu; phần sinh tổ hợp để học sau.*

- **Chính:** [Algorithms, chương 2: Backtracking](https://jeffe.cs.illinois.edu/teaching/algorithms/book/02-backtracking.pdf), Jeff Erickson — toàn chương: bài N quân hậu và duyệt cây tìm kiếm (Sách, tiếng Anh, 90 phút). Giải thích quay lui như đệ quy trên cây lựa chọn, rõ và có bài tập.
- **Xem thêm:** [CP-Algorithms: Generating all K-combinations](https://cp-algorithms.com/combinatorics/generating_combinations.html), CP-Algorithms — cả trang (sinh theo thứ tự từ điển) (Bài viết, tiếng Anh, 30 phút). Phương pháp sinh tổ hợp theo thứ tự từ điển kèm code.
- **Xem thêm:** [CP-Algorithms: Gray code](https://cp-algorithms.com/algebra/gray-code.html), CP-Algorithms — cả trang (Bài viết, tiếng Anh, 15 phút). Một cách sinh khác, tùy chọn.
- **Xem thêm:** [VisuAlgo: Recursion Tree/DAG](https://visualgo.net/en/recursion), Steven Halim — các ví dụ đệ quy (Tương tác, tiếng Anh, 20 phút). Nhìn cây đệ quy chạy từng bước; không có mô-đun riêng cho quay lui.

### Duyệt, tham lam và ký hiệu O lớn · Luyện Khí tầng 4

`tr_thuat_toan`

*Làm tham lam trước, O lớn bằng bài 1 của 6.006; chứng minh tham lam đúng để cho đường tiểu luận.*

- **Chính:** [Algorithms, chương 4: Greedy Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/book/04-greedy.pdf), Jeff Erickson — toàn chương: lập lịch, mã Huffman, và cách chứng minh tham lam đúng (Sách, tiếng Anh, 90 phút). Dạy tham lam từ ví dụ và nói rõ khi nào tham lam thất bại.
- **Xem thêm:** [MIT 6.006 Lecture 1: Algorithms and Computation](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-1-algorithms-and-computation/), MIT OpenCourseWare — toàn bài (Video, tiếng Anh, 50 phút). Mô hình tính toán và cách nghĩ về thời gian chạy.
- **Xem thêm:** [MIT 6.1200J bài 6 Asymptotics (mục 14.7)](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 06 (Khoá học, tiếng Anh, 60 phút). Ký hiệu O lớn và hệ quả; nên xem nếu cần định nghĩa chặt.

### Đồ thị và cách biểu diễn · Luyện Khí tầng 4

`tr_do_thi`

*Học khái niệm bằng Levin, rồi nhìn ma trận kề và danh sách kề trong Erickson chương 5.*

- **Chính:** [Discrete Mathematics: An Open Introduction, chương Graph Theory](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — phần Graph Theory: đỉnh, cạnh, bậc, định lý bắt tay, đường đi (Sách, tiếng Anh, 2 giờ). Mở đầu nhẹ nhàng về đồ thị, định lý bắt tay và đường đi; chưa ghi mục số.
- **Xem thêm:** [Algorithms, chương 5: Basic Graph Algorithms (biểu diễn đồ thị)](https://jeffe.cs.illinois.edu/teaching/algorithms/book/05-graphs.pdf), Jeff Erickson — phần định nghĩa và biểu diễn bằng ma trận kề, danh sách kề (Sách, tiếng Anh, 60 phút). Cho thấy biểu diễn nào hợp thuật toán nào.
- **Xem thêm:** [MIT 6.1200J bài 11: Graphs and Coloring](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 11, mục 12.1 đến 12.3 (Khoá học, tiếng Anh, 60 phút). Cách nhìn chặt hơn về đồ thị; dùng khi cần.
- **Tiếng Việt:** [VNOI Wiki: Lý thuyết đồ thị, trang tổng hợp](https://wiki.vnoi.info/algo/graph-theory/everything), VNOI — mục biểu diễn đồ thị (Bài viết, tiếng Việt, 30 phút). Tiếng Việt, hướng tới thi lập trình; chưa mở được toàn trang nên chưa chắc mục biểu diễn đồ thị nằm ở đâu.

### Tìm kiếm theo chiều rộng và chiều sâu · Luyện Khí tầng 5

`tr_tim_kiem`

*Xem bài 9 trước (BFS), rồi bài 10; chơi VisuAlgo giữa hai bài.*

- **Chính:** [MIT 6.006 Lecture 9: Breadth-First Search và Lecture 10: Depth-First Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-9-breadth-first-search/), MIT OpenCourseWare — bài 9 rồi bài 10 (url: .../lecture-10-depth-first-search/) (Video, tiếng Anh, 100 phút). BFS và DFS có chứng minh đúng đắn, thứ tự duyệt và sắp xếp topo (nối với lan truyền ngược).
- **Xem thêm:** [CP-Algorithms: Breadth First Search và Depth First Search](https://cp-algorithms.com/graph/breadth-first-search.html), CP-Algorithms — trang BFS; DFS ở cp-algorithms.com/graph/depth-first-search.html (Bài viết, tiếng Anh, 40 phút). Code ngắn và ứng dụng thật.
- **Xem thêm:** [VisuAlgo: Graph Traversal (BFS/DFS)](https://visualgo.net/en/dfsbfs), Steven Halim — chạy BFS và DFS trên đồ thị tự vẽ (Tương tác, tiếng Anh, 20 phút). Thấy hàng đợi và ngăn xếp thay đổi từng bước.
- **Luyện tập:** [VisuAlgo: Graph Traversal, chế độ thử thách](https://visualgo.net/en/dfsbfs), Steven Halim — nút luyện tập/kiểm tra (Tương tác, tiếng Anh, 30 phút). Tự kiểm tra thứ tự duyệt; có chế độ hỏi đáp, chưa thử.
- **Tiếng Việt:** [VNOI Wiki: Breadth First Search](https://wiki.vnoi.info/algo/graph-theory/breadth-first-search), VNOI — cả trang (Bài viết, tiếng Việt, 20 phút). Tiếng Việt, có nguồn từ CP-Algorithms và sách Lê Minh Hoàng.

### Cây và đường đi ngắn nhất · Luyện Khí tầng 6

`tr_cay_duong_di`

*Tính chất cây học trước bằng bài 13 của 6.1200J, rồi Dijkstra; bỏ Johnson và APSP.*

- **Chính:** [MIT 6.006 Lecture 13: Dijkstra (kèm Lecture 11-12)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-13-dijkstra/), MIT OpenCourseWare — bài 13; xem bài 11 Weighted Shortest Paths trước, bài 12 Bellman-Ford sau nếu cần (Video, tiếng Anh, 2 giờ). Đường đi ngắn nhất có trọng số xây từ BFS, đúng thứ tự dễ học.
- **Xem thêm:** [CP-Algorithms: Dijkstra](https://cp-algorithms.com/graph/dijkstra.html), CP-Algorithms — cả trang (Bài viết, tiếng Anh, 30 phút). Cách cài đặt thực tế.
- **Xem thêm:** [MIT 6.1200J bài 13: Connectivity and Trees](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 13, mục 12.7 đến 12.9 (Khoá học, tiếng Anh, 60 phút). Tính chất của cây, đúng phần 'cây' của nút.
- **Xem thêm:** [VisuAlgo: Single-Source Shortest Paths](https://visualgo.net/en/sssp), Steven Halim — chạy Dijkstra và Bellman-Ford (Tương tác, tiếng Anh, 20 phút). Thấy khoảng cách cập nhật từng bước.
- **Tiếng Việt:** [VNOI Wiki: Đường đi ngắn nhất](https://wiki.vnoi.info/algo/graph-theory/shortest-path), VNOI — cả trang: Dijkstra (Bài viết, tiếng Việt, 30 phút). Tiếng Việt, có Dijkstra và so sánh các thuật toán.

### Bài toán tối ưu, tập lồi và hàm lồi · Luyện Khí tầng 7

`tr_toi_uu_loi`

*Đọc bài 16 trước; điều kiện bậc hai chỉ cần hiểu ví dụ hàm một biến.*

- **Chính:** [Machine Learning cơ bản, bài 16: Convex sets và convex functions](https://machinelearningcoban.com/2017/03/12/convexity/), Vũ Hữu Tiệp — toàn bài: tập lồi, hàm lồi, điều kiện bậc nhất và bậc hai (Bài viết, tiếng Việt, 60 phút). Tiếng Việt, có hình và ví dụ, bao đủ tập lồi và hàm lồi.
- **Xem thêm:** [Mathematics for Machine Learning, chương 7: Continuous Optimization](https://mml-book.github.io/), Deisenroth, Faisal, Ong — mục 7.3 Convex Optimization (Sách, tiếng Anh, 60 phút). Sách miễn phí, ngắn, đúng khung học máy.
- **Xem thêm:** [Convex Optimization, chương 2-4](https://web.stanford.edu/~boyd/cvxbook/), Boyd, Vandenberghe — chương 2 tập lồi, chương 3 hàm lồi, chương 4 bài toán lồi (Sách, tiếng Anh). Tham khảo chuẩn; khó và dài nên chỉ tra khi cần.

### Hạ gradient và nhân tử Lagrange · Luyện Khí tầng 8

`tr_gradient_descent`

*Hạ gradient (bài 7) rồi Lagrange (đầu bài 18); momentum và Adam đọc sau.*

- **Chính:** [Machine Learning cơ bản, bài 7: Gradient Descent (phần 1)](https://machinelearningcoban.com/2017/01/12/gradientdescent/), Vũ Hữu Tiệp — toàn bài; hàm một biến rồi nhiều biến, kèm code (Bài viết, tiếng Việt, 60 phút). Hạ gradient từ hàm một biến tới hồi quy tuyến tính, có code Python.
- **Xem thêm:** [An overview of gradient descent optimization algorithms](https://www.ruder.io/optimizing-gradient-descent/), Sebastian Ruder — các mục batch/SGD/mini-batch, Momentum, Adam (Bài viết, tiếng Anh, 60 phút). Tổng quan các biến thể hạ gradient đang dùng khi huấn luyện mạng.
- **Xem thêm:** [Why Momentum Really Works](https://distill.pub/2017/momentum/), Gabriel Goh (Distill) — cả bài; xem các hình tương tác (Tương tác, tiếng Anh, 40 phút). Cho thấy vì sao momentum làm hạ gradient nhanh hơn; khá toán nên chỉ xem hình.
- **Xem thêm:** [Machine Learning cơ bản, bài 18: Duality (nhân tử Lagrange, KKT)](https://machinelearningcoban.com/2017/04/02/duality/), Vũ Hữu Tiệp — mục 2 nhân tử Lagrange và mục 5.2 điều kiện KKT (Bài viết, tiếng Việt, 60 phút). Phần Lagrange và KKT bằng tiếng Việt; phần đối ngẫu có thể bỏ qua.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 18: Duality](https://machinelearningcoban.com/2017/04/02/duality/), Vũ Hữu Tiệp — mục nhân tử Lagrange và KKT (Bài viết, tiếng Việt, 60 phút). Bản tiếng Việt duy nhất kiểm chứng được cho Lagrange.

### Bàng môn: Chứng minh bằng quy nạp · Luyện Khí

`tr_quy_nap`

*Làm vài bài tổng và chia hết bằng quy nạp thường; quy nạp mạnh để cho lần sau.*

- **Chính:** [MIT 6.1200J bài 2-3: Contradiction and Induction, Casework and Strong Induction](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 02 (mục 5.1) và Lecture 03 (mục 5.2-5.3), kèm video bài giảng (Khoá học, tiếng Anh, 2 giờ). Quy nạp thường và quy nạp mạnh, có nhiều ví dụ lập luận.
- **Xem thêm:** [Discrete Mathematics: An Open Introduction, mục Induction](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — mục về quy nạp trong chương Sequences (Sách, tiếng Anh, 60 phút). Nhẹ hơn cho người mới, có bài tập.

### Bàng môn: Tổ hợp lặp và nguyên lý bù trừ · Luyện Khí

`tr_dem_nang_cao`

*Chỉ cần nguyên lý bù trừ cho 2-3 tập; tổ hợp lặp xem khi đã quen tổ hợp.*

- **Chính:** [CP-Algorithms: Inclusion-Exclusion](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html), CP-Algorithms — cả trang: công thức và các bài toán đếm (Bài viết, tiếng Anh, 40 phút). Nguyên lý bù trừ có công thức và ví dụ; phần tổ hợp lặp có thể xem trong Levin.
- **Xem thêm:** [MIT 6.1200J bài 17: More Counting Techniques](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 17 (mục 15.5-15.10) (Khoá học, tiếng Anh, 90 phút). Các kỹ thuật đếm nâng cao có chứng minh.
- **Xem thêm:** [RES.6-012 Lecture 7: The Inclusion-Exclusion Formula](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/resources/the-inclusion-exclusion-formula/), MIT OpenCourseWare — video ngắn trong bài 7 (Video, tiếng Anh, 10 phút). Dạng xác suất của nguyên lý bù trừ; ví dụ bài toán cái mũ.

### Bàng môn: Dirichlet, bất biến và thứ hạng cấu hình · Luyện Khí

`tr_ton_tai`

*Chưa tìm được nguồn tốt riêng cho thứ hạng của cấu hình; có thể bỏ phần đó.*

- **Chính:** [MIT 6.1200J bài 4: State Machines (bất biến)](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/), MIT OpenCourseWare — Lecture 04 và chương State Machines cập nhật (Khoá học, tiếng Anh, 90 phút). Bất biến được dạy như công cụ chứng minh, phù hợp mục chẵn lẻ và bất biến.
- **Xem thêm:** [Discrete Mathematics: An Open Introduction, mục Pigeonhole Principle](https://discrete.openmathbooks.org/dmoi3.html), Oscar Levin — mục Pigeonhole trong chương Counting (chưa xác nhận số mục) (Sách, tiếng Anh, 40 phút). Nguyên lý Dirichlet có ví dụ và bài tập.

### Bàng môn: Nhánh cận · Luyện Khí

`tr_nhanh_can`

*Đã quen quay lui thì nhánh cận chỉ thêm bước tính cận; chưa tìm được nguồn tiếng Việt tốt.*

- **Chính:** [Lecture 27: Branch and Bound (CS4321)](https://www.csl.mtu.edu/cs4321/www/Lectures/Lecture%2027%20-%20Branch%20and%20Bound.htm), Michigan Technological University — toàn bài: cây trạng thái, cận, knapsack, TSP (Bài viết, tiếng Anh, 40 phút). Giải thích nhánh cận như quay lui có cận để cắt nhánh; ví dụ knapsack và TSP.
- **Xem thêm:** [Branch and Bound, chương 22](https://cise.ufl.edu/~sahni/dsaaj/public/chapters/c22.pdf), Sartaj Sahni (University of Florida) — ví dụ knapsack 0/1 bằng tìm kiếm FIFO và theo lợi nhuận lớn nhất (Sách, tiếng Anh, 60 phút). Ví dụ giải đầy đủ hơn.

### Bàng môn: Đồ thị Euler và Hamilton · Luyện Khí

`tr_euler_hamilton`

*Chỉ cần điều kiện Euler và hiểu vì sao Hamilton khó; không cần chứng minh các điều kiện đủ.*

- **Chính:** [CS 280 handout: Euler and Hamilton paths](https://cs.cornell.edu/courses/cs280/2001sp/handouts/h31.pdf), Cornell University — toàn bài: điều kiện bậc chẵn cho Euler, định nghĩa Hamilton (Bài viết, tiếng Anh, 40 phút). Định lý Euler và khác biệt Hamilton gọn; bản cũ (2001) nhưng nội dung không đổi.
- **Xem thêm:** [CP-Algorithms: Finding the Eulerian path](https://cp-algorithms.com/graph/euler_path.html), CP-Algorithms — cả trang (Bài viết, tiếng Anh, 25 phút). Thuật toán tìm đường Euler, kèm code.

### Bàng môn: Cây khung và luồng cực đại · Luyện Khí

`tr_cay_khung_luong`

*Học cây khung nhỏ nhất trước bằng Kruskal; luồng cực đại để cuối.*

- **Chính:** [Algorithms, chương 7: Minimum Spanning Trees và chương 10: Maximum Flows & Minimum Cuts](https://jeffe.cs.illinois.edu/teaching/algorithms/book/07-mst.pdf), Jeff Erickson — chương 7 rồi chương 10 (book/10-maxflow.pdf) (Sách, tiếng Anh, 3 giờ). Kruskal, Prim và Ford-Fulkerson với chứng minh và bài tập.
- **Xem thêm:** [CP-Algorithms: Kruskal và Edmonds-Karp](https://cp-algorithms.com/graph/mst_kruskal.html), CP-Algorithms — trang Kruskal; luồng ở cp-algorithms.com/graph/edmonds_karp.html (Bài viết, tiếng Anh, 60 phút). Code gọn cho cây khung và luồng cực đại.
- **Xem thêm:** [VisuAlgo: Min Spanning Tree và Network Flow](https://visualgo.net/en/mst), Steven Halim — mô-đun MST; luồng ở visualgo.net/en/maxflow (Tương tác, tiếng Anh, 30 phút). Chạy thuật toán từng bước.
- **Tiếng Việt:** [VNOI Wiki: Luồng](https://wiki.vnoi.info/algo/graph-theory/flow), VNOI — cả trang (Bài viết, tiếng Việt, 40 phút). Tiếng Việt, hướng thi lập trình; chưa mở trang đầy đủ.

### Bàng môn: Quy hoạch tuyến tính và đơn hình · Luyện Khí

`tr_quy_hoach_tuyen_tinh`

*Chưa tìm được nguồn tiếng Việt tốt về đơn hình; có thể chỉ cần mô hình hóa và phương pháp hình học hai biến.*

- **Chính:** [MIT 6.251J Introduction to Mathematical Programming: ghi chú bài giảng (Simplex, Duality)](https://www.ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/pages/lecture-notes), MIT OpenCourseWare (Bertsimas) — bài 5-8 simplex, bài 8-9 duality (Khoá học, tiếng Anh, 5 giờ). Khóa chuẩn về quy hoạch tuyến tính; bậc cao học nên hơi nặng.
- **Xem thêm:** [Machine Learning cơ bản, bài 18: Duality](https://machinelearningcoban.com/2017/04/02/duality/), Vũ Hữu Tiệp — mục hàm và bài toán đối ngẫu (Bài viết, tiếng Việt, 40 phút). Đối ngẫu tiếng Việt, tổng quát hơn quy hoạch tuyến tính.

### Bàng môn: Phương pháp tính · Luyện Khí

`tr_phuong_phap_tinh`

*Chia đôi và Newton trước; sai số và chữ số đáng tin học sau khi cần.*

- **Chính:** [Math 128A, chương 2: Bisection, Fixed-Point, Newton (bài giảng)](https://persson.berkeley.edu/math128a/slides/ch2math128a.html), Per-Olof Persson (UC Berkeley) — slide chương 2 (Bài viết, tiếng Anh, 60 phút). Chia đôi, lặp đơn và Newton trong một chuỗi slide, nối Newton với lặp đơn.
- **Xem thêm:** [CP-Algorithms: Newton's method for finding roots](https://cp-algorithms.com/num_methods/roots_newton.html), CP-Algorithms — cả trang (Bài viết, tiếng Anh, 20 phút). Newton có code ngắn.

### Dạng tự luận hay gặp trong đề cuối kỳ — Thuật Toán và Tối Ưu

Các dạng này không nằm trên chính đạo; chúng là đề của Luận Đạo Đài (`docs/LUAN_DAO_DAI.md`).

| Dạng | Thuộc nút | Hay gặp | Mô tả | Xem ở đâu |
|---|---|---|---|---|
| **Chứng minh bằng quy nạp** | Bàng môn: Chứng minh bằng quy nạp | rất hay gặp | Chứng minh công thức tổng, bất đẳng thức hoặc tính chia hết đúng với mọi n bằng quy nạp thường hoặc quy nạp mạnh. | [MIT 6.1200J bài 2-3: Induction](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Giải hệ thức truy hồi và chứng minh nghiệm** | Đếm và hệ thức truy hồi | rất hay gặp | Giải hệ thức truy hồi tuyến tính bằng phương trình đặc trưng, rồi kiểm tra nghiệm bằng quy nạp. | [MIT 6.1200J bài 7: Recurrences](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Chứng minh đẳng thức tổ hợp bằng đếm hai lần** | Đếm và hệ thức truy hồi | hay gặp | Chứng minh một đẳng thức tổ hợp bằng cách đếm cùng một tập theo hai cách, hoặc bằng công thức Pascal. | [Discrete Mathematics: An Open Introduction, mục Combinatorial Proofs](https://discrete.openmathbooks.org/dmoi3.html) |
| **Chứng minh định lý bắt tay** | Đồ thị và cách biểu diễn | rất hay gặp | Chứng minh tổng bậc bằng hai lần số cạnh, rồi suy ra số đỉnh bậc lẻ là chẵn. | [Discrete Mathematics: An Open Introduction, chương Graph Theory](https://discrete.openmathbooks.org/dmoi3.html) |
| **Đặc trưng đồ thị hai phía** | Đồ thị và cách biểu diễn | hay gặp | Chứng minh một đồ thị là hai phía khi và chỉ khi không có chu trình độ dài lẻ. | [MIT 6.1200J bài 11: Graphs and Coloring](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Các tính chất tương đương của cây** | Cây và đường đi ngắn nhất | rất hay gặp | Chứng minh cây n đỉnh có n-1 cạnh, và các định nghĩa tương đương: liên thông không chu trình, thêm cạnh sinh một chu trình. | [MIT 6.1200J bài 13: Connectivity and Trees](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Điều kiện tồn tại chu trình và đường Euler** | Bàng môn: Đồ thị Euler và Hamilton | hay gặp | Chứng minh đồ thị liên thông có chu trình Euler khi và chỉ khi mọi đỉnh bậc chẵn; điều kiện cho đường Euler có hai đỉnh bậc lẻ. | [CS 280 handout: Euler and Hamilton paths](https://cs.cornell.edu/courses/cs280/2001sp/handouts/h31.pdf) |
| **Điều kiện đủ cho chu trình Hamilton** | Bàng môn: Đồ thị Euler và Hamilton | hay gặp | Vận dụng điều kiện Dirac hoặc Ore để kết luận một đồ thị có chu trình Hamilton, hoặc chỉ ra phản ví dụ. | [Hamilton paths and circuits, bài giảng](https://www.cs.fsu.edu/~lacher/courses/MAD3105/lectures/s2_3EulerHam.pdf) |
| **Nguyên lý Dirichlet** | Bàng môn: Dirichlet, bất biến và thứ hạng cấu hình | hay gặp | Dùng nguyên lý chuồng bồ câu để chứng minh có hai phần tử cùng tính chất; chọn thỏ và chuồng cho hợp lý. | [Discrete Mathematics: An Open Introduction, mục Pigeonhole](https://discrete.openmathbooks.org/dmoi3.html) |
| **Bất biến và chẵn lẻ** | Bàng môn: Dirichlet, bất biến và thứ hạng cấu hình | thỉnh thoảng | Tìm đại lượng bất biến để chứng minh một trạng thái không đạt được từ trạng thái ban đầu. | [MIT 6.1200J bài 4: State Machines](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
| **Nguyên lý bù trừ** | Bàng môn: Tổ hợp lặp và nguyên lý bù trừ | hay gặp | Đếm số phần tử không thuộc một họ tập bằng nguyên lý bù trừ, ví dụ số toàn ánh hay hoán vị không có điểm cố định. | [CP-Algorithms: Inclusion-Exclusion](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html) |
| **Chứng minh tương đương logic** | Logic mệnh đề và quy tắc đếm | hay gặp | Chứng minh hai mệnh đề tương đương bằng bảng chân trị hoặc biến đổi bằng các luật logic; phủ định mệnh đề có lượng từ. | [Discrete Mathematics: An Open Introduction, chương Logic](https://discrete.openmathbooks.org/dmoi3.html) |
| **Chứng minh đúng đắn của thuật toán đồ thị** | Cây và đường đi ngắn nhất | hay gặp | Giải thích vì sao BFS cho đường đi ngắn nhất không trọng số, hoặc Dijkstra đúng khi cạnh không âm, bằng bất biến vòng lặp. | [MIT 6.006 Lecture 13: Dijkstra](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-13-dijkstra/) |
| **Chứng minh Kruskal hoặc Prim đúng** | Bàng môn: Cây khung và luồng cực đại | hay gặp | Chứng minh thuật toán Kruskal hoặc Prim cho cây khung nhỏ nhất bằng tính chất cắt hoặc lập luận hoán đổi. | [Algorithms, chương 7: Minimum Spanning Trees](https://jeffe.cs.illinois.edu/teaching/algorithms/book/07-mst.pdf) |
| **Chứng minh tham lam đúng và ước lượng độ phức tạp** | Duyệt, tham lam và ký hiệu O lớn | hay gặp | Chứng minh thuật toán tham lam cho đáp án tối ưu bằng lập luận hoán đổi, hoặc chứng minh f(n)=O(g(n)) bằng định nghĩa. | [Algorithms, chương 4: Greedy Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/book/04-greedy.pdf) |
| **Chứng minh tập hoặc hàm là lồi** | Bài toán tối ưu, tập lồi và hàm lồi | rất hay gặp | Chứng minh một tập là lồi bằng định nghĩa, hoặc một hàm là lồi bằng định nghĩa hay ma trận Hessian nửa xác định dương; mọi cực tiểu địa phương của hàm lồi là toàn cục. | [Machine Learning cơ bản, bài 16: Convex sets và convex functions](https://machinelearningcoban.com/2017/03/12/convexity/) |
| **Bài toán Lagrange và KKT trình bày đầy đủ** | Hạ gradient và nhân tử Lagrange | hay gặp | Viết Lagrangian, điều kiện KKT, giải hệ để tìm cực trị, rồi kết luận cực tiểu bằng tính lồi. | [Machine Learning cơ bản, bài 18: Duality](https://machinelearningcoban.com/2017/04/02/duality/) |
| **Hạ gradient trên hàm bậc hai** | Hạ gradient và nhân tử Lagrange | thỉnh thoảng | Viết vài bước hạ gradient với hàm bậc hai cụ thể; điều kiện bước học để hạ gradient hội tụ. | [Machine Learning cơ bản, bài 7: Gradient Descent](https://machinelearningcoban.com/2017/01/12/gradientdescent/) |
| **Lập bài toán đối ngẫu và giải bằng đơn hình** | Bàng môn: Quy hoạch tuyến tính và đơn hình | hay gặp | Chuyển mô hình thành dạng chuẩn, giải bằng phương pháp hình học hoặc đơn hình, viết bài toán đối ngẫu và so nghiệm. | [MIT 6.251J: Duality theory](https://www.ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/pages/lecture-notes) |
| **Đánh giá sai số của chia đôi và Newton** | Bàng môn: Phương pháp tính | hay gặp | Ước lượng số bước chia đôi cần cho sai số cho trước; đánh giá sai số lặp đơn khi ánh xạ co. | [Math 128A, chương 2](https://persson.berkeley.edu/math128a/slides/ch2math128a.html) |

**Đã xem và không chọn:**

- Grokking Algorithms (Bhargava): Sách thương mại, dễ đọc nhưng chưa tìm được trang chính thức kiểm chứng; không bao nhánh tối ưu. Giữ như nguồn cấp nhánh có sẵn trong tree.
- Boyd và Vandenberghe, Convex Optimization làm nguồn chính: Sách chuẩn nhưng dày và khó cho năm nhất; chỉ tra chương 2-4. Máy chủ báo lỗi chứng chỉ nên chưa kiểm tra được.
- Harvard CS50 và các khóa chung chung về thuật toán: Không đi sâu vào đồ thị và tối ưu như nút cần.
- Mathematics for Computer Science (Lehman, Leighton, Meyer) làm nguồn chính: Chính xác nhưng hàn lâm và dài; dùng làm nguồn tra cứu cho quy nạp, đồ thị, truy hồi.
- MIT 6.251J cho người mới học quy hoạch tuyến tính: Bậc cao học, nặng; chỉ hợp khi thật sự cần đơn hình.
- Đề thi Toán rời rạc IT3020 và MI2010 (Bách khoa Hà Nội): Không tìm được đề thi chính thức công khai; các tài liệu thấy được là của trường khác hoặc đăng lại không rõ bản quyền.
- Tạ Văn Đĩnh, Phương pháp tính (bản Word trên trang cá nhân): Tình trạng bản quyền không rõ; chỉ dùng đề cương chính thức MI2044.

## Lập Trình

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [CS50's Introduction to Programming with Python (OpenCourseWare)](https://cs50.harvard.edu/python/weeks/0/), David J. Malan, Harvard — tuần 0 đến 9; có video, ghi chú, bài tập tự chấm (Khoá học, tiếng Anh, 20 giờ). Khoá nhập môn Python bài bản nhất, miễn phí, bài tập có kiểm tra tự động; dùng cho các nút tầng thấp.
2. [Data Science from Scratch, 2nd ed. (code repo)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — thư mục scratch: linear_algebra.py, gradient_descent.py, probability.py, network_analysis.py (Code, tiếng Anh). Mã nguồn Python thuần cho vectơ, ma trận, hạ gradient: đúng tinh thần 'tự viết một lần'. Giấy phép MIT.
3. [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/), Jake VanderPlas — chương 2 (NumPy), 3 (pandas), 4 (Matplotlib) (Sách, tiếng Anh, 10 giờ). Sách đọc trực tuyến miễn phí, nối NumPy, pandas và vẽ biểu đồ thành một mạch.
4. [The Missing Semester of Your CS Education (2026)](https://missing.csail.mit.edu/), MIT (Anish, Jon, Jose) — bài Dòng lệnh, Môi trường phát triển, Git, Đóng gói mã (Khoá học, tiếng Anh, 10 giờ). Những thứ trường ít dạy nhưng làm dự án thật nào cũng cần: shell, git, gỡ lỗi.

### Python nhập môn · Luyện Khí tầng 1

`lt_python_co_ban`

*Làm CS50P tuần 0-2 kèm bài tập, đọc Think Python khi bí; bỏ qua OOP và biểu thức chính quy ở mức này.*

- **Chính:** [CS50P tuần 0: Functions, Variables](https://cs50.harvard.edu/python/weeks/0/), David J. Malan — tuần 0, rồi tuần 1 (Conditionals) và tuần 2 (Loops) (Khoá học, tiếng Anh, 6 giờ). Đi đúng thứ tự biến, điều kiện, vòng lặp, hàm; mỗi tuần có bài tập tự chấm.
- **Xem thêm:** [Think Python, 3rd edition](https://allendowney.github.io/ThinkPython/), Allen B. Downey — chương 1 đến 4 (chương và bài tập, bản trực tuyến) (Sách, tiếng Anh, 5 giờ). Giải thích chậm và chắc cho người chưa từng lập trình; giấy phép CC BY-NC-SA.
- **Xem thêm:** [Automate the Boring Stuff with Python, 3rd ed., chương 1 đến 4](https://automatetheboringstuff.com/3e/chapter1.html), Al Sweigart — chương 1 Python Basics, 2 Flow Control, 3 Loops, 4 Functions (Sách, tiếng Anh, 4 giờ). Nhiều ví dụ ngắn có thể gõ lại ngay, đáp án câu hỏi ôn ở phụ lục B.
- **Luyện tập:** [Exercism Python track](https://exercism.org/tracks/python), Exercism — các bài đầu của track (Basics, Conditionals, Loops) (Bài tập, tiếng Anh, 5 giờ). 146 bài miễn phí có bộ kiểm thử, có thể nhờ người hướng dẫn nhận xét.

### Danh sách, tập hợp và từ điển · Luyện Khí tầng 2

`lt_cau_truc_du_lieu`

*Đọc mục 5.1, 5.4, 5.5 rồi tự viết lại các phép giao, hợp, hiệu của tập hợp toán học bằng set; bỏ qua deque.*

- **Chính:** [Python Tutorial, mục 5: Data Structures](https://docs.python.org/3/tutorial/datastructures.html), Python Software Foundation — 5.1 (list), 5.4 (set), 5.5 (dict), 5.6 (kỹ thuật duyệt) (Bài viết, tiếng Anh, 60 phút). Tài liệu chính thức, ngắn, có ví dụ về set với các toán tử | & - ^ đúng như phép toán tập hợp.
- **Xem thêm:** [Think Python 3e, chương 9 Lists và chương 10 Dictionaries](https://allendowney.github.io/ThinkPython/chap10.html), Allen B. Downey — chương 9 và 10 (Sách, tiếng Anh, 90 phút). Cho thấy dict dùng để đếm và tra cứu bằng ví dụ đếm chữ cái.
- **Xem thêm:** [Python Numpy Tutorial, phần Containers](https://cs231n.github.io/python-numpy-tutorial/), Justin Johnson (Stanford CS231n) — mục Python > Containers (list, dict, set, tuple) (Bài viết, tiếng Anh, 30 phút). Bản tóm tắt gọn một trang, có sổ tay Colab chạy được.
- **Luyện tập:** [Exercism Python track (bài về list, dict, set)](https://exercism.org/tracks/python), Exercism — chọn các bài thuộc concept lists, dicts, sets (Bài tập, tiếng Anh, 2 giờ). Luyện đếm từ, tra cứu, lọc trùng với bộ kiểm thử có sẵn.

### Vectơ và ma trận bằng code · Luyện Khí tầng 3

`lt_vecto_bang_code`

*Tự gõ lại các hàm add, dot, norm, transpose trước khi đọc bản của Grus rồi so sánh; kiểm tra kích thước đầu vào bằng assert.*

- **Chính:** [Data Science from Scratch: linear_algebra.py (chương 4 Linear Algebra)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/linear_algebra.py: cộng vectơ, tích vô hướng, độ dài, ma trận là list của list, chuyển vị (Code, tiếng Anh, 90 phút). Đúng bài toán của nút: vectơ là list, ma trận là list của list, toàn bằng Python thuần; giấy phép MIT.
- **Xem thêm:** [Python Tutorial 5.1.4: Nested List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html), Python Software Foundation — mục 5.1.4, ví dụ chuyển vị ma trận bằng comprehension (Bài viết, tiếng Anh, 15 phút). Cho cách viết chuyển vị trong một dòng, rồi so với bản dùng vòng lặp.

### Hàm, đệ quy và chia nhỏ bài toán · Luyện Khí tầng 3

`lt_ham_de_quy`

*Học theo thứ tự: giai thừa, Fibonacci, tháp Hà Nội, rồi hoán vị bằng quay lui; chưa cần tối ưu bằng nhớ đệm.*

- **Chính:** [Think Python 3e, chương 5: Conditionals and Recursion](https://allendowney.github.io/ThinkPython/chap05.html), Allen B. Downey — chương 5 (đệ quy, điều kiện dừng) (Sách, tiếng Anh, 60 phút). Giới thiệu đệ quy từ hàm gọi hàm, có biểu đồ ngăn xếp gọi.
- **Xem thêm:** [CS50P tuần 0 và 3 (hàm, ngoại lệ)](https://cs50.harvard.edu/python/weeks/0/), David J. Malan — phần Functions của tuần 0 (Khoá học, tiếng Anh, 60 phút). Ôn cách viết hàm có tham số và giá trị trả về trước khi vào đệ quy.
- **Luyện tập:** [Exercism Python track (giai thừa, Fibonacci, hoán vị)](https://exercism.org/tracks/python), Exercism — tìm các bài tính toán đệ quy trong track (Bài tập, tiếng Anh, 2 giờ). Có kiểm thử tự động cho từng bài.

### Nhân ma trận và khử Gauss bằng code · Luyện Khí tầng 4

`lt_ma_tran_gauss`

*Xem bài giảng 2, tự giải một hệ 3x3 trên giấy, rồi viết nhân ma trận bằng ba vòng lặp và khử Gauss; kiểm lại bằng NumPy sau khi xong.*

- **Chính:** [MIT 18.06 Lecture 2: Elimination with Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/index.html), Gilbert Strang (MIT OpenCourseWare) — bài giảng 2 (khoảng 47 phút), phần khử và thế ngược (Video, tiếng Anh, 47 phút). Nắm thuật toán khử Gauss bằng tay trước, rồi mới đem viết thành ba vòng lặp.
- **Xem thêm:** [Data Science from Scratch: linear_algebra.py](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/linear_algebra.py: hàm tạo ma trận và nhân ma trận (không có sẵn khử Gauss, phải tự viết) (Code, tiếng Anh, 30 phút). Nền để dựng các hàm ma trận trước khi viết khử Gauss.

### NumPy: mảng và vector hoá · Luyện Khí tầng 4

`lt_numpy`

*Đọc absolute basics rồi làm 30 bài đầu của numpy-100; sau đó viết lại phép nhân ma trận của nút trước bằng @ và so thời gian.*

- **Chính:** [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html), NumPy developers — ndarray, shape, indexing and slicing, broadcasting, aggregation theo trục (Bài viết, tiếng Anh, 90 phút). Trang chính thức cho người mới, đủ bốn ý của nút: shape, cắt lát, broadcasting, hàm theo trục.
- **Xem thêm:** [Python Numpy Tutorial (with Jupyter and Colab)](https://cs231n.github.io/python-numpy-tutorial/), Justin Johnson (Stanford CS231n) — mục Numpy: Arrays, Array indexing, Array math, Broadcasting (Bài viết, tiếng Anh, 45 phút). Bản ngắn, ví dụ rõ về broadcasting; có sổ tay Colab.
- **Xem thêm:** [From Python to NumPy](https://www.labri.fr/perso/nrougier/from-python-to-numpy/), Nicolas P. Rougier — chương Anatomy of an array và Code vectorization (Sách, tiếng Anh, 2 giờ). Dạy cách nghĩ vector hoá thay vì vòng lặp; sách CC BY-NC-SA, mã BSD.
- **Luyện tập:** [100 numpy exercises (with solutions)](https://github.com/rougier/numpy-100), Nicolas P. Rougier — 100_Numpy_exercises.ipynb và file lời giải .md (Bài tập, tiếng Anh, 4 giờ). 100 bài có lời giải và gợi ý, giấy phép MIT.

### Mô phỏng xác suất · Luyện Khí tầng 4

`lt_mo_phong_xac_suat`

*Mô phỏng rút bi và gieo xúc xắc, rồi mô phỏng chính bài xác suất có điều kiện ở nhánh xác suất để kiểm công thức.*

- **Chính:** [Seeing Theory: Basic Probability và Compound Probability](https://seeing-theory.brown.edu/), Brown University (Daniel Kunin và cộng sự) — chương 1 và 2 (xác suất cơ bản, xác suất có điều kiện); trang đã ngừng cập nhật nhưng vẫn dùng được (Tương tác, tiếng Anh, 60 phút). Cho thấy tần suất tiến về xác suất khi gieo nhiều lần, đúng ý 'gieo triệu lần rồi đếm'.
- **Xem thêm:** [NumPy absolute basics: Generating random numbers](https://numpy.org/doc/stable/user/absolute_beginners.html), NumPy developers — mục Generating random numbers (default_rng, hạt giống) (Bài viết, tiếng Anh, 15 phút). Cách tạo số ngẫu nhiên có hạt giống bằng API hiện đại.
- **Xem thêm:** [Data Science from Scratch: probability.py](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/probability.py (xác suất có điều kiện, ví dụ hai đứa trẻ) (Code, tiếng Anh, 30 phút). Có bài mô phỏng xác suất có điều kiện để so với công thức.

### Đo độ phức tạp, tìm kiếm và sắp xếp · Luyện Khí tầng 5

`lt_do_phuc_tap`

*Cài tìm kiếm tuyến tính, nhị phân và một thuật toán sắp xếp, đếm số phép so sánh và đo thời gian với n tăng gấp đôi; chưa cần chứng minh cận.*

- **Chính:** [VisuAlgo: Sorting](https://visualgo.net/en), Steven Halim — mục Sorting: bubble, insertion, merge, quick; chạy từng bước và đếm phép so sánh (Tương tác, tiếng Anh, 60 phút). Thấy tận mắt vì sao O(n log n) nhanh hơn O(n^2) khi n lớn.
- **Xem thêm:** [Learn Big O Notation](https://www.freecodecamp.org/news/learn-big-o-notation/), freeCodeCamp — toàn bài (ký hiệu O, ví dụ vòng lặp) (Bài viết, tiếng Anh, 20 phút). Bài viết ngắn, chưa kiểm chất lượng sâu; chỉ dùng làm bản đọc nhanh.

### Đạo hàm số và hạ gradient một biến · Luyện Khí tầng 5

`lt_dao_ham_so`

*Viết hạ gradient cho f(x)=x^2 rồi thử tốc độ học 0,001 / 0,1 / 1,1 để thấy chậm, vừa và nổ; so sai phân với đạo hàm tính tay.*

- **Chính:** [Neural networks chapter 2: Gradient descent, how neural networks learn](https://3blue1brown.com/lessons/gradient-descent), 3Blue1Brown (Grant Sanderson) — bài 2 của chuỗi Neural Networks (khoảng 21 phút) (Video, tiếng Anh, 21 phút). Hình ảnh quả bóng lăn xuống thung lũng cho trực giác của hạ gradient và tốc độ học.
- **Xem thêm:** [Data Science from Scratch: gradient_descent.py (chương 8)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/gradient_descent.py: sai phân, bước hạ gradient, chọn tốc độ học (Code, tiếng Anh, 45 phút). Bản code ngắn dùng sai phân để xấp xỉ đạo hàm rồi hạ gradient.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 7: Gradient Descent (1/2)](https://machinelearningcoban.com/2017/01/12/gradientdescent/), Vũ Hữu Tiệp — toàn bài, phần một biến (Bài viết, tiếng Việt, 40 phút). Giải thích tiếng Việt rõ, có ví dụ một biến và bàn về tốc độ học.

### Đồ thị bằng code · Luyện Khí tầng 6

`lt_do_thi`

*Dùng dict làm danh sách kề, BFS dùng collections.deque, DFS bằng đệ quy, Dijkstra dùng heapq; bỏ qua Bellman-Ford.*

- **Chính:** [VisuAlgo: Graph Traversal (DFS/BFS) và SS Shortest Paths](https://visualgo.net/en), Steven Halim — các mục Graph Traversal và SSSP (BFS, Dijkstra) (Tương tác, tiếng Anh, 60 phút). Chạy từng bước BFS, DFS, Dijkstra trên đồ thị tự vẽ trước khi cài.
- **Xem thêm:** [Graph Algorithms in Python: BFS, DFS and Beyond](https://www.freecodecamp.org/news/graph-algorithms-in-python-bfs-dfs-and-beyond/), freeCodeCamp — toàn bài: danh sách kề bằng dict, BFS, DFS, Dijkstra (Bài viết, tiếng Anh, 40 phút). Mã Python dùng dict và deque, vừa với nút này; chất lượng blog, nên tự gõ lại.

### Python cho dự án thật · Trúc Cơ tầng 1

`tc_python_nang_cao`

*Chia dự án nhỏ thành module, viết lớp đơn giản, bắt lỗi cụ thể, rồi thêm vài test pytest; bỏ qua generator, decorator ở mức này.*

- **Chính:** [Python Tutorial, mục 8 và 9: Errors and Exceptions, Classes](https://docs.python.org/3/tutorial/classes.html), Python Software Foundation — mục 9.3 đến 9.5 (lớp, đối tượng, kế thừa) và mục 8 (xử lý lỗi) (Bài viết, tiếng Anh, 90 phút). Tài liệu chính thức, đủ cho lớp, module, ngoại lệ ở mức dự án nhỏ.
- **Xem thêm:** [CS50P tuần 3, 5, 8: Exceptions, Unit Tests, OOP](https://cs50.harvard.edu/python/weeks/5/), David J. Malan — tuần 3 (ngoại lệ), 4 (thư viện), 5 (kiểm thử), 8 (hướng đối tượng) (Khoá học, tiếng Anh, 5 giờ). Dạy cả viết test với pytest ngay trong bài tập.
- **Xem thêm:** [Think Python 3e, chương 14 đến 17: Classes](https://allendowney.github.io/ThinkPython/chap14.html), Allen B. Downey — chương 14 đến 17 (Sách, tiếng Anh, 2 giờ). Dẫn từ hàm sang lớp từng bước nhỏ.
- **Luyện tập:** [pytest: Get Started](https://docs.pytest.org/en/stable/getting-started.html), pytest-dev — toàn bài (assert, ngoại lệ, pytest.approx cho số thực) (Bài viết, tiếng Anh, 30 phút). Bắt đầu viết test; pytest.approx hữu ích cho code số học.

### Dữ liệu bảng và trực quan hoá · Trúc Cơ tầng 1

`tc_du_lieu`

*Học pandas và Kaggle Learn Pandas, rồi làm sạch một bảng thật (thiếu, sai kiểu) và vẽ phân phối; bỏ qua chuỗi thời gian và parquet.*

- **Chính:** [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html), pandas developers — toàn bài (selection, missing data, grouping, plotting) (Bài viết, tiếng Anh, 60 phút). Điểm khởi đầu chính thức, bản mới nhất của tài liệu (pandas 3).
- **Xem thêm:** [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas), Kaggle — cả khoá (khoảng 6 bài, mỗi bài có bài tập có đáp án) (Khoá học, tiếng Anh, 4 giờ). Bài tập tương tác trong notebook, có gợi ý và lời giải.
- **Xem thêm:** [Python Data Science Handbook, chương 3 và 4](https://jakevdp.github.io/PythonDataScienceHandbook/), Jake VanderPlas — chương 3 (pandas, 3.01 đến 3.13) và 4 (Matplotlib) (Sách, tiếng Anh, 5 giờ). Chi tiết hơn về làm sạch dữ liệu và vẽ phân phối, tương quan.

Thực chiến:

- Dữ liệu: [Palmer Penguins](https://github.com/allisonhorst/palmerpenguins) (giấy phép: CC0 (dữ liệu, theo Palmer Station LTER Data Policy), đã kiểm, 0.02 MB). 344 dòng, có giá trị thiếu, nhẹ và dùng tự do; hợp để thực hành làm sạch và vẽ.
- Dữ liệu: [Titanic (Kaggle)](https://www.kaggle.com/competitions/titanic) (giấy phép: chưa rõ giấy phép: dữ liệu thuộc điều khoản cuộc thi Kaggle, không nên đóng gói trong game, 0.1 MB). Bảng kinh điển nhưng cần tài khoản Kaggle và điều khoản riêng.
- Đích: Không có chỉ số cố định; xong khi bảng đã làm sạch, có ít nhất ba biểu đồ phân phối và tương quan, và viết được hai câu hỏi cho dữ liệu.
- Chạy ở đâu: Máy xách tay, pandas và Matplotlib, dưới 1 phút.

### Git và thí nghiệm tái lập được · Trúc Cơ tầng 3

`tc_git`

*Học git cơ bản và nhánh, rồi tự ghi nhật ký thí nghiệm (hạt giống, phiên bản thư viện, kết quả) vào repo; bỏ qua git nội bộ và máy chủ.*

- **Chính:** [Pro Git (2nd ed.), chương 2: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository), Scott Chacon, Ben Straub — chương 2 (init, add, commit, log, undo) rồi chương 3 (nhánh) (Sách, tiếng Anh, 2 giờ). Sách chuẩn về git, miễn phí; chưa có bản dịch tiếng Việt chính thức theo trang sách.
- **Xem thêm:** [Missing Semester 2026: Version Control and Git; Packaging and Shipping Code](https://missing.csail.mit.edu/2026/version-control/), MIT — bài Version Control and Git và bài Packaging and Shipping Code (môi trường, phiên bản) (Khoá học, tiếng Anh, 2 giờ). Cho mô hình tư duy của git và cách đóng gói, cố định môi trường.
- **Luyện tập:** [Learn Git Branching](https://learngitbranching.js.org/), Peter Cottle — các cấp Main (commit, branch, merge, rebase) (Tương tác, tiếng Anh, 90 phút). Trò chơi tương tác trong trình duyệt để hiểu nhánh; trang chưa nói rõ giấy phép.

Thực chiến:

- Đích: Chạy lại thí nghiệm trên máy khác từ repo và ra đúng cùng số (cùng hạt giống, requirements đã ghim).
- Chạy ở đâu: Chỉ cần git và Python; chưa kiểm chứng thêm.

**Đã xem và không chọn:**

- Runestone: Problem Solving with Algorithms and Data Structures using Python: Trang trả lỗi 403 khi kiểm tra, không xác nhận được nội dung.
- Khan Academy khoá Algorithms: Không tìm được trang chính thức trong kết quả tìm kiếm nên không đưa vào.
- Python Crash Course (Matthes): Sách in trả phí, đã nằm trong nguồn cấp nhánh; CS50P miễn phí và có tự chấm tốt hơn.
- Pro Git bản tiếng Việt: Trang sách không liệt kê tiếng Việt trong các bản dịch.
- Các trang dán lại sách thương mại (scribd, studocu): Vi phạm luật nguồn hợp pháp của hợp đồng.
- Python Data Science Handbook làm nguồn nền tảng cho từng nút nhỏ: Quá dài cho nút nhập môn; chỉ dùng ở nút dữ liệu bảng.

## Thực Chiến AI

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Machine Learning cơ bản (blog)](https://machinelearningcoban.com/), Vũ Hữu Tiệp — các bài KNN, Linear Regression, Gradient Descent, Logistic Regression, PCA, Naive Bayes, MLP (Bài viết, tiếng Việt, 10 giờ). Loạt bài tiếng Việt tự viết thuật toán bằng NumPy, mỗi bài có công thức và mã; hợp học từng mô hình nhỏ.
2. [Data Science from Scratch, 2nd ed. (code repo)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/: k_nearest_neighbors.py, naive_bayes.py, simple_linear_regression.py, logistic_regression.py, neural_networks.py (Code, tiếng Anh). Mỗi mô hình viết bằng Python thuần, MIT; dùng làm bản đối chiếu sau khi tự viết.
3. [Neural Networks: Zero to Hero, bài 1: building micrograd](https://youtu.be/VMj-3S1tku0), Andrej Karpathy — bài 1 (2 giờ 25 phút): lan truyền ngược viết từ đầu (Video, tiếng Anh, 2 giờ). Cách tốt nhất để thấy lan truyền ngược chỉ là quy tắc dây chuyền áp dụng nhiều lần.

### Mô hình đầu tiên: k láng giềng gần nhất · Luyện Khí tầng 3

`ud_knn`

*Tự viết khoảng cách, sắp xếp lấy k điểm gần nhất, bỏ phiếu; rồi đo độ chính xác trên tập tách riêng; chưa cần cây k-d.*

- **Chính:** [Machine Learning cơ bản, bài 6: K-nearest neighbors](https://machinelearningcoban.com/2017/01/08/knn/), Vũ Hữu Tiệp — toàn bài (khoảng cách, bỏ phiếu, chọn k) (Bài viết, tiếng Việt, 40 phút). Giải thích KNN bằng tiếng Việt với mã NumPy chạy được trên dữ liệu thật.
- **Xem thêm:** [Data Science from Scratch: k_nearest_neighbors.py (chương 12)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/k_nearest_neighbors.py (Code, tiếng Anh, 30 phút). Bản Python thuần, ngắn, có bỏ phiếu và xử lý hoà.
- **Luyện tập:** [Digits Classification Exercise](https://scikit-learn.org/1.5/auto_examples/exercises/plot_digits_classification_exercise.html), scikit-learn — tài liệu scikit-learn bản 1.5 (ví dụ này đã bị gỡ khỏi các bản mới hơn) (Bài tập, tiếng Anh, 30 phút). Đối chiếu kết quả của mình với bài mẫu chính thức.

Thực chiến:

- Dữ liệu: [Optical Recognition of Handwritten Digits (UCI, 8x8)](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) (giấy phép: CC BY 4.0 (đã kiểm trên trang UCI), 0.58 MB). 5620 ảnh 8x8, 64 đặc trưng; nhỏ, đóng gói được. scikit-learn có sẵn bản 1797 mẫu qua load_digits.
- Dữ liệu: [Iris (qua scikit-learn load_iris)](https://scikit-learn.org/stable/datasets/toy_dataset.html) (giấy phép: chưa rõ giấy phép (trang scikit-learn không nêu; dữ liệu Fisher 1936, thường coi như dùng tự do), 0.01 MB). 150 mẫu, 4 đặc trưng, để chạy thử nhanh.
- Bản mẫu: [Data Science from Scratch: k_nearest_neighbors.py](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/k_nearest_neighbors.py (Code, tiếng Anh, 30 phút). Bản Python thuần để so.
- Đích: Trên digits 8x8, KNN thường đạt khoảng 95% đến 99% tuỳ cách chia và k (trang mẫu scikit-learn cho 0,96; một notebook công khai cho 99,1% ở k=1); mục tiêu hợp lý: từ 95% trở lên.
- Chạy ở đâu: CPU máy xách tay, Python thuần hoặc NumPy, dưới 1 phút với 1797 mẫu.

### Lọc thư rác bằng Bayes · Luyện Khí tầng 5

`ud_naive_bayes`

*Đếm từ theo nhãn, làm trơn Laplace, cộng log xác suất để khỏi tràn số; không cần tinh lọc chữ.*

- **Chính:** [Machine Learning cơ bản, bài 32: Naive Bayes Classifier](https://machinelearningcoban.com/2017/08/08/nbc/), Vũ Hữu Tiệp — toàn bài, ví dụ phân loại văn bản (Bài viết, tiếng Việt, 40 phút). Có ví dụ phân loại văn bản và mã; đúng với bộ lọc thư rác.
- **Xem thêm:** [StatQuest: Naive Bayes](https://youtu.be/O2L2Uv9pdDA), Josh Starmer — toàn video (Video, tiếng Anh, 15 phút). Hình dung từng bước đếm từ và nhân xác suất; trang mục lục StatQuest dẫn tới video này.
- **Xem thêm:** [Data Science from Scratch: naive_bayes.py (chương 13)](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/naive_bayes.py (bộ lọc thư rác Python thuần) (Code, tiếng Anh, 30 phút). Cùng bài toán thư rác, có làm trơn Laplace.

Thực chiến:

- Dữ liệu: [SMS Spam Collection (UCI)](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) (giấy phép: CC BY 4.0 (đã kiểm trên trang UCI), 0.47 MB). 5574 tin nhắn có nhãn spam/ham, 467 KB; đóng gói được kèm ghi công.
- Bản mẫu: [Data Science from Scratch: naive_bayes.py](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/naive_bayes.py (Code, tiếng Anh, 30 phút). Bản đối chiếu.
- Đích: Naive Bayes đa thức trên SMS Spam thường đạt từ 96,6% đến 99% độ chính xác tuỳ cách chia (các báo cáo công khai: 96,6%, 98,995%); tập lệch lớp (spam khoảng 13%) nên cần báo thêm precision và recall; chưa có nguồn chuẩn duy nhất.
- Chạy ở đâu: CPU máy xách tay, Python thuần, vài giây.

### Khớp đường thẳng bằng hạ gradient · Luyện Khí tầng 5

`ud_hoi_quy_1_bien`

*Viết vòng lặp: dự đoán, tính mất mát, hai đạo hàm, cập nhật; vẽ mất mát theo bước. Bỏ qua hồi quy nhiều biến cho tới nút sau.*

- **Chính:** [Machine Learning cơ bản, bài 3: Linear Regression](https://machinelearningcoban.com/2016/12/28/linearregression/), Vũ Hữu Tiệp — hàm mất mát, nghiệm, ví dụ Python (Bài viết, tiếng Việt, 40 phút). Dẫn từ hàm mất mát tới đạo hàm theo tham số rồi tới mã.
- **Xem thêm:** [Machine Learning cơ bản, bài 7: Gradient Descent (1/2)](https://machinelearningcoban.com/2017/01/12/gradientdescent/), Vũ Hữu Tiệp — toàn bài (Bài viết, tiếng Việt, 40 phút). Đào sâu vòng huấn luyện và tốc độ học.
- **Xem thêm:** [StatQuest: Gradient Descent, Step-by-Step](https://youtu.be/sDv4f4s2SB8), Josh Starmer — toàn video (Video, tiếng Anh, 23 phút). Ví dụ hai tham số, tính tay từng bước.

Thực chiến:

- Dữ liệu: [Palmer Penguins (chiều dài cánh và khối lượng)](https://github.com/allisonhorst/palmerpenguins) (giấy phép: CC0 (đã kiểm), 0.02 MB). 344 dòng, quan hệ gần tuyến tính, hợp để khớp một biến.
- Dữ liệu: [Dữ liệu tự sinh y = a*x + b + nhiễu](https://numpy.org/doc/stable/user/absolute_beginners.html) (giấy phép: không áp dụng (tự sinh bằng NumPy), 0 MB). Biết đáp án đúng nên kiểm được mô hình học ra a và b.
- Đích: Hệ số học được gần với a, b đã sinh (sai lệch vài phần trăm); chưa có số chuẩn từ nguồn cho dữ liệu penguins, chưa kiểm chứng.
- Chạy ở đâu: CPU máy xách tay, NumPy, dưới 1 giây.

### Bình phương tối thiểu bằng phương trình chuẩn · Luyện Khí tầng 7

`ud_binh_phuong_toi_thieu`

*Đặt ma trận thiết kế, giải A^T A x = A^T b bằng np.linalg.solve, rồi so với kết quả hạ gradient ở nút trước; thử cả np.linalg.lstsq.*

- **Chính:** [MIT 18.06 Lecture 16: Projection Matrices and Least Squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/index.html), Gilbert Strang (MIT OpenCourseWare) — bài 16 (khoảng 48 phút), ví dụ khớp đường thẳng (Video, tiếng Anh, 48 phút). Cho thấy phương trình chuẩn là phép chiếu, đúng nút này.
- **Xem thêm:** [Machine Learning cơ bản, bài 3: Linear Regression (nghiệm đóng)](https://machinelearningcoban.com/2016/12/28/linearregression/), Vũ Hữu Tiệp — phần Nghiệm đóng và so với hạ gradient (Bài viết, tiếng Việt, 20 phút). Viết phương trình chuẩn bằng NumPy và so với kết quả hạ gradient.
- **Luyện tập:** [18.06SC Fall 2011, bài tập phiên 2.3 (least squares)](https://www.ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/33fdb9f7b7787e26752169e249def994_MIT18_06SCF11_Ses2.3prob.pdf), MIT OpenCourseWare — bài khớp đường thẳng, có đáp án ở file sol (Bài tập, tiếng Anh, 30 phút). Bài tay có đáp án để kiểm cách đặt Ax gần bằng b.

Thực chiến:

- Dữ liệu: [California Housing (scikit-learn fetch_california_housing)](https://scikit-learn.org/stable/datasets/real_world.html) (giấy phép: chưa rõ giấy phép (trang scikit-learn không nêu; nguồn StatLib 1990), 1.9 MB). 20640 mẫu, 8 đặc trưng, hợp để thấy nhiều biến; tải một lần. Kích thước là ước lượng, chưa kiểm.
- Dữ liệu: [Dữ liệu tự sinh nhiều biến](https://numpy.org/doc/stable/user/absolute_beginners.html) (giấy phép: không áp dụng, 0 MB). Biết hệ số thật nên kiểm được nghiệm.
- Đích: Nghiệm của phương trình chuẩn trùng np.linalg.lstsq tới sai số làm tròn, và trùng nghiệm hạ gradient đã hội tụ; chưa có số R^2 chuẩn từ nguồn.
- Chạy ở đâu: CPU máy xách tay, NumPy, dưới 1 giây.

### Mạng nơ-ron hai lớp tự viết · Luyện Khí tầng 8

`ud_mang_no_ron`

*Làm theo thứ tự: 3Blue1Brown, rồi tự viết hai lớp trên XOR, kiểm gradient bằng sai phân, rồi mới thử trên digits; bỏ qua thuật toán dùng ma trận Hadamard nếu thấy rối.*

- **Chính:** [Neural networks chapter 3 và 4: Backpropagation intuitively, và What is backpropagation really doing?](https://3blue1brown.com/lessons/backpropagation), 3Blue1Brown (Grant Sanderson) — trang bài 4 của chuỗi (backpropagation bằng quy tắc dây chuyền); bài 3 là bản trực giác (Video, tiếng Anh, 25 phút). Trực giác và quy tắc dây chuyền cho từng lớp, trước khi gõ code.
- **Xem thêm:** [Neural Networks and Deep Learning, chương 1 và 2](http://neuralnetworksanddeeplearning.com/chap2.html), Michael Nielsen — chương 1 (mạng sigmoid, MNIST) và chương 2 (4 phương trình lan truyền ngược) (Sách, tiếng Anh, 4 giờ). Mã Python/NumPy từng bước; trang bị lỗi chứng chỉ khi kiểm, nên chưa xác nhận được.
- **Xem thêm:** [Machine Learning cơ bản, bài 14: Multi-layer Perceptron và Backpropagation](https://machinelearningcoban.com/2017/02/24/mlp/), Vũ Hữu Tiệp — toàn bài, có mã NumPy (Bài viết, tiếng Việt, 60 phút). Tiếng Việt, có kiểm gradient và ví dụ chạy được.
- **Xem thêm:** [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtu.be/VMj-3S1tku0), Andrej Karpathy — toàn bài (2 giờ 25 phút) (Video, tiếng Anh, 2 giờ). Tự dựng bộ đạo hàm tự động; dài nhưng đáng làm sau khi viết bản NumPy.

Thực chiến:

- Dữ liệu: [XOR (4 điểm tự viết)](http://neuralnetworksanddeeplearning.com/chap2.html) (giấy phép: không áp dụng, 0 MB). Bài thử nhỏ nhất để thấy mạng hai lớp giải được thứ mô hình tuyến tính không giải được.
- Dữ liệu: [scikit-learn digits 8x8 (bản UCI optdigits)](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) (giấy phép: CC BY 4.0 (đã kiểm), 0.58 MB). Nhỏ, huấn luyện được trong vài chục giây trên CPU.
- Dữ liệu: [MNIST](http://yann.lecun.com/exdb/mnist/) (giấy phép: chưa rõ giấy phép (trang gốc không kiểm được; không đóng gói trong game, để người chơi tải một lần), 11 MB). Chuẩn ngành, 60000 ảnh 28x28; kích thước ước lượng, chưa kiểm.
- Bản mẫu: [Michael Nielsen, neural-networks-and-deep-learning (mã chương 1)](http://neuralnetworksanddeeplearning.com/chap1.html), Michael Nielsen — mã network.py trong chương 1 (Code, tiếng Anh, 60 phút). Bản NumPy chuẩn để đối chiếu; chưa xác nhận được trang.
- Đích: XOR: sai số về gần 0 và đúng cả 4 điểm. Digits 8x8: kỳ vọng từ 93% trở lên; MNIST mạng 30 nơ-ron ẩn thường đạt khoảng 95% sau vài chục epoch theo sách Nielsen; chưa kiểm chứng trực tiếp.
- Chạy ở đâu: CPU máy xách tay, NumPy; digits mất khoảng 10 đến 60 giây, MNIST vài phút.

### Hồi quy logistic · Luyện Khí tầng 9

`ud_logistic`

*Dùng mất mát log và gradient X^T(p - y)/n, thử các ngưỡng 0,3 / 0,5 / 0,7 và xem kết quả.*

- **Chính:** [Machine Learning cơ bản, bài 10: Logistic Regression](https://machinelearningcoban.com/2017/01/27/logisticregression/), Vũ Hữu Tiệp — toàn bài (sigmoid, hàm mất mát, gradient) (Bài viết, tiếng Việt, 50 phút). Đủ bốn ý của nút, có mã NumPy và hình minh hoạ.
- **Xem thêm:** [StatQuest: Logistic Regression](https://youtu.be/yIYKR4sgzI8), Josh Starmer — toàn video (Video, tiếng Anh, 9 phút). Trực giác về xác suất và hợp lý cực đại; chưa mở được YouTube để kiểm.
- **Xem thêm:** [Machine Learning Crash Course: Logistic regression](https://developers.google.com/machine-learning/crash-course/logistic-regression), Google — module Logistic Regression (sigmoid, mất mát log, ngưỡng) (Khoá học, tiếng Anh, 60 phút). Có bài tương tác và câu hỏi tự kiểm.

Thực chiến:

- Dữ liệu: [Breast Cancer Wisconsin (Diagnostic), qua scikit-learn](https://scikit-learn.org/stable/datasets/toy_dataset.html) (giấy phép: chưa rõ giấy phép (trang scikit-learn không nêu; nguồn UCI, cần xác nhận), 0.12 MB). 569 mẫu, 30 đặc trưng, 2 lớp; nhỏ, phân loại nhị phân kinh điển.
- Dữ liệu: [SMS Spam Collection (UCI)](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) (giấy phép: CC BY 4.0 (đã kiểm), 0.47 MB). Có thể so logistic với Naive Bayes trên cùng dữ liệu.
- Bản mẫu: [Data Science from Scratch: logistic_regression.py](https://github.com/joelgrus/data-science-from-scratch), Joel Grus — scratch/logistic_regression.py (Code, tiếng Anh, 30 phút). Bản Python thuần.
- Đích: Chưa kiểm chứng số cụ thể; logistic tự viết trên Breast Cancer thường đạt từ 95% trở lên nếu chuẩn hoá đặc trưng.
- Chạy ở đâu: CPU máy xách tay, NumPy, dưới 5 giây.

### PCA: nén dữ liệu · Luyện Khí tầng 9

`ud_pca`

*Trừ trung bình, tính hiệp phương sai, lấy np.linalg.eigh, chiếu xuống 2 chiều; không cần SVD tới khi nhánh đại số tuyến tính dạy.*

- **Chính:** [Machine Learning cơ bản, bài 27 và 28: Principal Component Analysis (1/2 và 2/2)](https://machinelearningcoban.com/2017/06/15/pca/), Vũ Hữu Tiệp — bài 27 (ma trận hiệp phương sai, vectơ riêng), bài 28 (cách tính khác và ví dụ) (Bài viết, tiếng Việt, 80 phút). Nối giá trị riêng của ma trận hiệp phương sai với giữ lại bao nhiêu phần trăm thông tin.
- **Xem thêm:** [StatQuest: Principal Component Analysis (PCA), Step-by-Step](https://youtu.be/FgakZw6K1QQ), Josh Starmer — toàn video (Video, tiếng Anh, 21 phút). Trực giác chiếu dữ liệu và tỉ lệ phương sai; chưa mở được YouTube để kiểm.
- **Xem thêm:** [Machine Learning cơ bản, bài 28: PCA (2/2)](https://machinelearningcoban.com/2017/06/21/pca2/), Vũ Hữu Tiệp — toàn bài (Bài viết, tiếng Việt, 40 phút). Phần hai, có mã và ví dụ trên ảnh.

Thực chiến:

- Dữ liệu: [Digits 8x8 (UCI optdigits)](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) (giấy phép: CC BY 4.0 (đã kiểm), 0.58 MB). 64 chiều nén xuống 2 chiều để vẽ và xuống 20 chiều để nhận dạng.
- Dữ liệu: [Wine (qua scikit-learn)](https://scikit-learn.org/stable/datasets/toy_dataset.html) (giấy phép: chưa rõ giấy phép (nguồn UCI, cần xác nhận), 0.01 MB). 178 mẫu, 13 đặc trưng, nhẹ.
- Đích: Vectơ riêng tự tính trùng np.linalg.eigh / sklearn.decomposition.PCA; chưa có phần trăm phương sai chuẩn từ nguồn cho digits, chưa kiểm chứng.
- Chạy ở đâu: CPU máy xách tay, NumPy, dưới 1 giây.

### Thí nghiệm A/B: mô hình nào thật sự tốt hơn · Luyện Khí tầng 9

`ud_ab_test`

*Mô phỏng nhiều lần A/A để thấy dương tính giả khoảng 5%, rồi tính khoảng tin cậy cho hiệu hai tỉ lệ; bỏ qua kiểm định tuần tự.*

- **Chính:** [How Not To Run an A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html), Evan Miller — toàn bài (ví dụ nhìn kết quả giữa chừng và sai lầm loại một) (Bài viết, tiếng Anh, 15 phút). Cho thấy dừng sớm khi 'có ý nghĩa' làm tỉ lệ dương tính giả vượt 5% thế nào.
- **Xem thêm:** [Seeing Theory chương 4: Frequentist Inference](https://seeing-theory.brown.edu/), Brown University — chương 4 (khoảng tin cậy, ước lượng khoảng) (Tương tác, tiếng Anh, 30 phút). Tương tác để hiểu khoảng tin cậy và mẫu lặp lại.
- **Xem thêm:** [Trustworthy Online Controlled Experiments](https://experimentguide.com/), Ron Kohavi, Diane Tang, Ya Xu — chương về thống kê của thí nghiệm A/B và kích thước mẫu (Sách, tiếng Anh, trả phí). Sách tham khảo nghiêm túc; trả phí qua Cambridge, trang phụ trợ chưa kiểm.

Thực chiến:

- Dữ liệu: [Kết quả dự đoán của hai mô hình trên cùng tập kiểm tra digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) (giấy phép: CC BY 4.0 (đã kiểm), 0.58 MB). So KNN với mạng nơ-ron tự viết bằng bootstrap hoặc kiểm định McNemar.
- Đích: Báo cáo được khoảng tin cậy 95% của hiệu độ chính xác hai mô hình và kết luận đúng khi khoảng chứa 0; chưa có số chuẩn.
- Chạy ở đâu: CPU máy xách tay, NumPy, dưới 1 phút cho 10000 lần bootstrap.

### Thiên kiếp Luyện Khí: nhận dạng chữ số viết tay · Luyện Khí tầng 9

`du_an_luyen_khi`

*Làm tuần tự: nạp ảnh thành ma trận, nén bằng PCA, huấn luyện mạng tự viết, rồi báo độ chính xác kèm khoảng tin cậy (dùng A/B ở nút trước).*

- **Chính:** [Neural Networks and Deep Learning, chương 1: phân loại chữ số viết tay](http://neuralnetworksanddeeplearning.com/chap1.html), Michael Nielsen — chương 1 (mạng sigmoid nhận dạng MNIST) (Sách, tiếng Anh, 2 giờ). Ví dụ gần như trùng dự án; trang bị lỗi chứng chỉ khi kiểm, chưa xác nhận.
- **Xem thêm:** [Machine Learning cơ bản, bài 14: MLP và Backpropagation](https://machinelearningcoban.com/2017/02/24/mlp/), Vũ Hữu Tiệp — toàn bài (Bài viết, tiếng Việt, 60 phút). Bản tiếng Việt cho phần mạng nơ-ron.
- **Xem thêm:** [Digits Classification Exercise](https://scikit-learn.org/1.5/auto_examples/exercises/plot_digits_classification_exercise.html), scikit-learn — tài liệu scikit-learn bản 1.5 (ví dụ này đã bị gỡ khỏi các bản mới hơn) (Bài tập, tiếng Anh, 20 phút). Mốc so sánh khi báo cáo.

Thực chiến:

- Dữ liệu: [Optical Recognition of Handwritten Digits (UCI, 8x8)](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) (giấy phép: CC BY 4.0 (đã kiểm), 0.58 MB). Dữ liệu chính của dự án: nhỏ, hợp đóng gói.
- Dữ liệu: [MNIST](http://yann.lecun.com/exdb/mnist/) (giấy phép: chưa rõ giấy phép (không kiểm được trang gốc), 11 MB). Bản đầy đủ 28x28 cho người muốn thử thách thêm.
- Dữ liệu: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) (giấy phép: MIT (đã kiểm, bản quyền Zalando SE), 30 MB). Khó hơn MNIST, cùng định dạng; 26 MB ảnh huấn luyện nén cộng 4,3 MB ảnh kiểm tra.
- Bản mẫu: [Digits Classification Exercise (scikit-learn)](https://scikit-learn.org/1.5/auto_examples/exercises/plot_digits_classification_exercise.html), scikit-learn — tài liệu scikit-learn bản 1.5 (ví dụ này đã bị gỡ khỏi các bản mới hơn) (Code, tiếng Anh, 20 phút). Mốc đối chiếu.
- Đích: Digits 8x8: mục tiêu từ 95% trở lên (KNN mẫu của scikit-learn đạt 96,1%, một notebook công khai 99,1%); MNIST với mạng 30 nơ-ron ẩn khoảng 95% theo Nielsen, chưa kiểm chứng trực tiếp.
- Chạy ở đâu: CPU máy xách tay, NumPy; digits dưới 1 phút, MNIST vài phút.

**Đã xem và không chọn:**

- Stanford CS229 lecture notes: Trang khoá chỉ dẫn tới bảng tính cần tài khoản Stanford, không có đường dẫn ghi chú công khai kiểm được.
- Andrew Ng Machine Learning Specialization cho nút nhỏ: Dài, dùng TensorFlow, chứng chỉ trả phí; không hợp mục tiêu tự viết bằng tay.
- Nielsen Neural Networks and Deep Learning (kiểm trực tiếp): Trang lỗi chứng chỉ khi tải nên không kiểm được, vẫn giữ vì nội dung phù hợp.
- Các bản đăng lại sách và slide trên scribd, studocu: Không hợp pháp, bị loại theo hợp đồng.
- Dữ liệu Titanic của Kaggle để đóng gói: Chịu điều khoản cuộc thi; không rõ quyền phân phối lại.

## Học Máy

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Machine Learning cơ bản (blog) và sách](https://machinelearningcoban.com/), Vũ Hữu Tiệp — các bài Linear Regression, Overfitting, K-means, PCA, SVM, Feature Engineering (Bài viết, tiếng Việt, 10 giờ). Tiếng Việt, có công thức, trực giác và mã; dùng làm lớp đầu tiên cho từng nút.
2. [An Introduction to Statistical Learning with Applications in Python (ISLP)](https://www.statlearning.com/), James, Witten, Hastie, Tibshirani, Taylor — chương 2 đến 10 và bài giảng video của các tác giả (Sách, tiếng Anh, 25 giờ). Sách giáo trình chuẩn, PDF miễn phí trên trang; có playlist video bài giảng chính thức cả bản R và Python.
3. [Hands-On Machine Learning, 3rd ed. (sổ tay công khai)](https://github.com/ageron/handson-ml3), Aurélien Géron — notebook chương 2 đến 9 (01 đến 09), giấy phép Apache-2.0 (Code, tiếng Anh, 15 giờ). Mã chạy được cho hầu hết nút; bản sách in trả phí nhưng các notebook miễn phí.
4. [MLU-Explain](https://mlu-explain.github.io/), Amazon MLU (Jared Wilber, Lucía Santamaría) — các bài cây quyết định, rừng ngẫu nhiên, ROC, kiểm định chéo, bias-variance (Tương tác, tiếng Anh, 2 giờ). Bài tương tác trực quan, đọc nhanh, đúng 'giải thích đơn giản nhưng đúng'.

### Học có giám sát: tập huấn luyện, kiểm định, kiểm tra · Trúc Cơ tầng 1

`tc_hoc_co_giam_sat`

*Đọc MLU, rồi làm bài tập rò rỉ dữ liệu của Kaggle; chia dữ liệu trước mọi bước chuẩn hoá hay điền thiếu.*

- **Chính:** [MLU-Explain: Train, Test, and Validation Sets](https://mlu-explain.github.io/train-test-validation/), Amazon MLU — toàn bài (Tương tác, tiếng Anh, 15 phút). Hình ảnh tương tác về chia tập; đọc nhanh, đúng ý nút.
- **Xem thêm:** [Machine Learning Crash Course: Datasets, generalization, and overfitting](https://developers.google.com/machine-learning/crash-course/overfitting), Google — module Datasets, Generalization, and Overfitting (bản làm mới) (Khoá học, tiếng Anh, 60 phút). Gồm cả rò rỉ dữ liệu và tập kiểm định.
- **Xem thêm:** [Kaggle Learn: Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning), Kaggle — bài 5 Underfitting and Overfitting, bài 6 Random Forests (Khoá học, tiếng Anh, 2 giờ). Học bằng cách chạy, có bài tập; chưa mở được danh sách bài nên chỉ ghi theo mô tả.
- **Luyện tập:** [Kaggle Learn: Intermediate Machine Learning (rò rỉ dữ liệu, kiểm định chéo)](https://www.kaggle.com/learn/intermediate-machine-learning), Kaggle — bài Data Leakage và Cross-Validation (Bài tập, tiếng Anh, 2 giờ). Bài tập có thể thấy rò rỉ làm điểm đẹp giả ra sao.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 15: Overfitting](https://machinelearningcoban.com/2017/03/04/overfitting/), Vũ Hữu Tiệp — toàn bài (quá khớp, validation, regularization) (Bài viết, tiếng Việt, 40 phút). Giải thích quá khớp bằng tiếng Việt kèm ví dụ.

### Hồi quy tuyến tính và chính quy hoá · Trúc Cơ tầng 2

`tc_hoi_quy`

*Chuẩn hoá đặc trưng trước ridge/lasso, đọc hệ số sau khi chuẩn hoá; bỏ qua mục chọn mô hình theo AIC, BIC.*

- **Chính:** [ISLP chương 3 (hồi quy tuyến tính) và chương 6 (chính quy hoá)](https://www.statlearning.com/), James, Witten, Hastie, Tibshirani — chương 3 và mục Ridge, Lasso của chương 6, có lab Python (Sách, tiếng Anh, 5 giờ). Cách đọc hệ số, ridge và lasso giải thích kỹ; PDF miễn phí.
- **Xem thêm:** [StatQuest: Regularization Part 1: Ridge (L2) và Part 2: Lasso (L1)](https://youtu.be/Q81RR3yKn30), Josh Starmer — Part 1 rồi Part 2 (https://youtu.be/NGf0voTMlcs) (Video, tiếng Anh, 40 phút). Trực giác ridge co hệ số, lasso về 0; chưa mở được YouTube để kiểm.
- **Xem thêm:** [Hands-On ML 3e, chương 4: Training Linear Models](https://github.com/ageron/handson-ml3), Aurélien Géron — 04_training_linear_models.ipynb (Code, tiếng Anh, 90 phút). Mã hồi quy nhiều biến, ridge, lasso chạy được.
- **Xem thêm:** [scikit-learn: Linear Models (Ridge, Lasso)](https://scikit-learn.org/stable/modules/linear_model.html), scikit-learn — mục 1.1.2 Ridge, 1.1.3 Lasso (Bài viết, tiếng Anh, 30 phút). Tài liệu tham chiếu khi cần chọn tham số chính quy hoá.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 3: Linear Regression](https://machinelearningcoban.com/2016/12/28/linearregression/), Vũ Hữu Tiệp — toàn bài; chính quy hoá nằm ở bài Overfitting (bài 15) (Bài viết, tiếng Việt, 40 phút). Tiếng Việt, nối được với nút ud_hoi_quy_1_bien.

### Phân loại và cách đo · Trúc Cơ tầng 2

`tc_phan_loai`

*Làm bài tập 'độ chính xác 99% vô dụng' trên dữ liệu lệch lớp; chưa cần ROC đa lớp.*

- **Chính:** [MLU-Explain: Precision & Recall và ROC & AUC](https://mlu-explain.github.io/roc-auc/), Amazon MLU — bài ROC & AUC, kèm bài Precision & Recall (https://mlu-explain.github.io/precision-recall/) (Tương tác, tiếng Anh, 30 phút). Kéo ngưỡng và xem ma trận nhầm lẫn, precision, recall, ROC đổi thế nào.
- **Xem thêm:** [StatQuest: The Confusion Matrix và ROC and AUC](https://youtu.be/4jRBRDbJemM), Josh Starmer — ROC and AUC; ma trận nhầm lẫn: https://youtu.be/Kdsp6soqA7o (Video, tiếng Anh, 30 phút). Giải thích chậm từng bước; chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Metrics and scoring](https://scikit-learn.org/stable/modules/model_evaluation.html), scikit-learn — mục Confusion matrix, Precision recall F-measures, ROC (Bài viết, tiếng Anh, 40 phút). Công thức và hàm dùng ngay.
- **Luyện tập:** [Hands-On ML 3e, chương 3: Classification](https://github.com/ageron/handson-ml3), Aurélien Géron — 03_classification.ipynb (đo bằng ma trận nhầm lẫn, đường cong precision-recall, ROC) (Code, tiếng Anh, 90 phút). Chạy sổ tay để chọn ngưỡng trên dữ liệu thật.

### Cây quyết định · Trúc Cơ tầng 2

`tc_cay_quyet_dinh`

*Đọc MLU rồi tự tính Gini cho một lần chia bằng tay; bỏ qua CART hồi quy tới nút rừng ngẫu nhiên.*

- **Chính:** [MLU-Explain: Decision Trees](https://mlu-explain.github.io/decision-tree/), Jared Wilber, Lucía Santamaría — toàn bài (entropy, thông tin thu được, quá khớp, cắt tỉa) (Tương tác, tiếng Anh, 20 phút). Trực quan hoá độ thuần của nút và vì sao cây quá khớp.
- **Xem thêm:** [StatQuest: Decision and Classification Trees, Clearly Explained](https://youtu.be/_L39rN6gz7Y), Josh Starmer — toàn video (Video, tiếng Anh, 18 phút). Tính Gini từng bước bằng tay; chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Decision Trees](https://scikit-learn.org/stable/modules/tree.html), scikit-learn — mục 1.10.5 Tips, 1.10.9 Minimal Cost-Complexity Pruning (Bài viết, tiếng Anh, 30 phút). Cho tham số max_depth, min_samples_leaf, ccp_alpha để cắt tỉa.
- **Luyện tập:** [Hands-On ML 3e, chương 6: Decision Trees](https://github.com/ageron/handson-ml3), Aurélien Géron — 06_decision_trees.ipynb (Code, tiếng Anh, 60 phút). Chạy cây và xem độ nhạy với dữ liệu xoay.

### Đánh giá mô hình cho đáng tin · Trúc Cơ tầng 3

`tc_danh_gia`

*Dùng K-fold phân tầng, báo trung bình và độ lệch chuẩn; để so hai mô hình hãy dùng cùng các lần chia. Bỏ qua kiểm định chéo cho chuỗi thời gian.*

- **Chính:** [MLU-Explain: Cross-Validation và The Bias Variance Tradeoff](https://mlu-explain.github.io/cross-validation/), Amazon MLU — bài Cross-Validation, kèm bài Bias-Variance (https://mlu-explain.github.io/bias-variance/) (Tương tác, tiếng Anh, 30 phút). Hai bài tương tác ngắn đúng hai chủ đề của nút.
- **Xem thêm:** [StatQuest: Cross Validation và Bias and Variance](https://youtu.be/fSytzGwwBVw), Josh Starmer — Cross Validation; Bias and Variance: https://youtu.be/EuBBz3bI-aA (Video, tiếng Anh, 25 phút). Ví dụ chuột và đường cong; chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Cross-validation và Validation curves, learning curves](https://scikit-learn.org/stable/modules/learning_curve.html), scikit-learn — mục 3.5.2 Learning curve; kiểm định chéo: https://scikit-learn.org/stable/modules/cross_validation.html (Bài viết, tiếng Anh, 40 phút). Vẽ đường cong học và đọc nó.

### Thiên kiếp Trúc Cơ: một bài toán dữ liệu bảng từ đầu đến cuối · Trúc Cơ tầng 3

`du_an_truc_co`

*Chọn một bảng nhỏ, dựng mô hình nền trước, mỗi lần cải tiến một thứ và ghi lại; báo cáo kèm kiểm định chéo.*

- **Chính:** [Hands-On ML 3e, chương 2: End-to-End Machine Learning Project](https://github.com/ageron/handson-ml3), Aurélien Géron — 02_end_to_end_machine_learning_project.ipynb (Code, tiếng Anh, 4 giờ). Đi trọn quy trình: hiểu bài toán, làm sạch, mô hình nền, cải tiến, đánh giá.
- **Xem thêm:** [Kaggle Learn: Intermediate Machine Learning](https://www.kaggle.com/learn/intermediate-machine-learning), Kaggle — thiếu dữ liệu, biến phân loại, pipeline, kiểm định chéo, XGBoost (Khoá học, tiếng Anh, 4 giờ). Bổ sung pipeline và xử lý thiếu dữ liệu.
- **Tiếng Việt:** [Machine Learning cơ bản (sách tabml)](https://machinelearningcoban.com/ebook/), Vũ Hữu Tiệp — trang giới thiệu ebook Machine Learning cơ bản (bản trả phí); chưa kiểm được trang tabml (Sách, tiếng Việt, trả phí). Sách tiếng Việt của tác giả; nội dung bảng nên xem trực tiếp trên trang.

Thực chiến:

- Dữ liệu: [Adult / Census Income (UCI)](https://archive.ics.uci.edu/dataset/2/adult) (giấy phép: CC BY 4.0 (đã kiểm), 5.7 MB). 48842 dòng, 14 đặc trưng, có thiếu và biến phân loại; adult.data 3,8 MB cộng adult.test 1,9 MB.
- Dữ liệu: [Palmer Penguins](https://github.com/allisonhorst/palmerpenguins) (giấy phép: CC0 (đã kiểm), 0.02 MB). 344 dòng, nhẹ, hợp bài làm nhanh.
- Dữ liệu: [California Housing (scikit-learn)](https://scikit-learn.org/stable/datasets/real_world.html) (giấy phép: chưa rõ giấy phép (trang scikit-learn không nêu; nguồn StatLib), 1.9 MB). 20640 mẫu cho hồi quy; kích thước ước lượng, chưa kiểm.
- Bản mẫu: [Hands-On ML 3e, chương 2](https://github.com/ageron/handson-ml3), Aurélien Géron — 02_end_to_end_machine_learning_project.ipynb (Code, tiếng Anh, 4 giờ). Bản mẫu cho cả quy trình.
- Đích: Chưa kiểm chứng chỉ số cụ thể từ nguồn. Xong khi mô hình vượt rõ mô hình nền (đoán lớp đa số hay đoán trung bình), kèm báo cáo kiểm định chéo và một đoạn về rò rỉ dữ liệu.
- Chạy ở đâu: CPU máy xách tay, scikit-learn, vài phút.

### Entropy, cross-entropy và KL · Kết Đan tầng 1

`kd_thong_tin`

*Đọc Olah tới hết Cross-Entropy, rồi tự tính tay entropy và cross-entropy cho hai phân phối nhỏ; bỏ qua thông tin tương hỗ.*

- **Chính:** [Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/), Christopher Olah — các mục Calculating Entropy và Cross-Entropy (KL nằm trong mục Cross-Entropy) (Bài viết, tiếng Anh, 40 phút). Hình ảnh trực quan nhất về entropy, cross-entropy và KL, không cần chứng minh.
- **Xem thêm:** [StatQuest: Entropy, Clearly Explained](https://youtu.be/YtebGVx-Fxw), Josh Starmer — toàn video (Video, tiếng Anh, 17 phút). Bản video ngắn cho entropy; chưa mở được YouTube để kiểm.
- **Xem thêm:** [Machine Learning cơ bản, bài 10: Logistic Regression (hợp lý cực đại)](https://machinelearningcoban.com/2017/01/27/logisticregression/), Vũ Hữu Tiệp — phần hàm mất mát cross-entropy từ hợp lý cực đại (Bài viết, tiếng Việt, 25 phút). Nối cross-entropy với hợp lý cực đại bằng tiếng Việt.

### Rừng ngẫu nhiên và boosting · Kết Đan tầng 1

`kd_ensemble`

*Học bagging, rừng ngẫu nhiên rồi gradient boosting theo thứ tự đó; XGBoost chỉ để biết, không cần đọc phần tối ưu hoá.*

- **Chính:** [MLU-Explain: Random Forest](https://mlu-explain.github.io/random-forest/), Amazon MLU — toàn bài (bagging, rừng ngẫu nhiên) (Tương tác, tiếng Anh, 20 phút). Trực quan cách nhiều cây bỏ phiếu giảm phương sai.
- **Xem thêm:** [StatQuest: Random Forests Part 1 và Gradient Boost Part 1](https://youtu.be/J4Wdy0Wc_xQ), Josh Starmer — Random Forests Part 1; Gradient Boost Part 1: https://youtu.be/3CC4N4z3GJc (Video, tiếng Anh, 35 phút). Giải thích bagging và boosting từng bước; chưa mở được YouTube để kiểm.
- **Xem thêm:** [XGBoost: Introduction to Boosted Trees](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), XGBoost developers — toàn bài (hàm mục tiêu, cộng dần, độ phức tạp) (Bài viết, tiếng Anh, 40 phút). Tài liệu chính thức giải thích boosting; phần toán có thể đọc lướt.
- **Xem thêm:** [scikit-learn: Ensembles](https://scikit-learn.org/stable/modules/ensemble.html), scikit-learn — mục 1.11.1 Gradient-boosted trees, 1.11.2 Random forests, Feature importance (Bài viết, tiếng Anh, 30 phút). Cho cách đọc tầm quan trọng đặc trưng và tham số chính.
- **Luyện tập:** [Hands-On ML 3e, chương 7: Ensemble Learning and Random Forests](https://github.com/ageron/handson-ml3), Aurélien Géron — 07_ensemble_learning_and_random_forests.ipynb (Code, tiếng Anh, 90 phút). Mã bagging, rừng, boosting.

### Tối ưu cho học máy: SGD, momentum, Adam · Kết Đan tầng 2

`kd_toi_uu_ml`

*Tự cài SGD, momentum, Adam trên một hàm hai biến dạng thung lũng hẹp và vẽ quỹ đạo; bỏ qua các biến thể như AMSGrad, Nadam.*

- **Chính:** [An overview of gradient descent optimization algorithms](https://www.ruder.io/optimizing-gradient-descent/), Sebastian Ruder — mục SGD, Mini-batch, Momentum, Adam (Bài viết, tiếng Anh, 60 phút). Bài tổng quan chuẩn về SGD, momentum, Adam; đọc mục theo thứ tự, bỏ phần xa hơn.
- **Xem thêm:** [Why Momentum Really Works](https://distill.pub/2017/momentum/), Gabriel Goh (Distill) — phần mở đầu và các ví dụ tương tác về bước nhảy (Tương tác, tiếng Anh, 40 phút). Trực quan vì sao momentum cho phép bước lớn hơn; phần toán có thể bỏ qua.
- **Xem thêm:** [StatQuest: Stochastic Gradient Descent](https://youtu.be/vMh0zPT0tLI), Josh Starmer — toàn video (Video, tiếng Anh, 10 phút). Giải thích SGD ngắn gọn; chưa mở được YouTube để kiểm.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 8: Gradient Descent (2/2)](https://machinelearningcoban.com/2017/01/16/gradientdescent2/), Vũ Hữu Tiệp — toàn bài (SGD, momentum, Nesterov) (Bài viết, tiếng Việt, 40 phút). Tiếng Việt, có SGD và momentum kèm mã.

### Học không giám sát · Kết Đan tầng 2

`kd_khong_giam_sat`

*K-means rồi PCA áp dụng cho trực quan hoá; phát hiện bất thường chỉ cần một phương pháp (Isolation Forest).*

- **Chính:** [Machine Learning cơ bản, bài 4 và 5: K-means Clustering](https://machinelearningcoban.com/2017/01/01/kmeans/), Vũ Hữu Tiệp — bài 4 (thuật toán), bài 5 (ứng dụng: https://machinelearningcoban.com/2017/01/04/kmeans2/) (Bài viết, tiếng Việt, 60 phút). Tiếng Việt, có mã và ví dụ nén ảnh.
- **Xem thêm:** [StatQuest: K-Means Clustering và PCA Step-by-Step](https://youtu.be/4b5d3muPQmA), Josh Starmer — K-Means; PCA: https://youtu.be/FgakZw6K1QQ (Video, tiếng Anh, 30 phút). Trực giác, chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Clustering (k-means) và Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html), scikit-learn — mục 2.7.3 Isolation Forest, Local Outlier Factor; k-means: mục 2.3.2 ở trang clustering (Bài viết, tiếng Anh, 40 phút). Cho phát hiện bất thường bằng Isolation Forest và LOF.
- **Xem thêm:** [Hands-On ML 3e, chương 8 và 9: Dimensionality Reduction, Unsupervised Learning](https://github.com/ageron/handson-ml3), Aurélien Géron — 08_dimensionality_reduction.ipynb, 09_unsupervised_learning.ipynb (Code, tiếng Anh, 2 giờ). Mã k-means, PCA, giảm chiều để nhìn dữ liệu.

### Kỹ nghệ đặc trưng và dữ liệu khó · Kết Đan tầng 2

`kd_dac_trung`

*Chưa tìm được nguồn tốt riêng cho nhiễu nhãn: chỉ cần biết nó tồn tại và thử bỏ mẫu có mất mát lớn; mọi bước điền, mã hoá, tăng mẫu làm bên trong pipeline và chỉ trên tập huấn luyện.*

- **Chính:** [Kaggle Learn: Feature Engineering](https://www.kaggle.com/learn/feature-engineering), Kaggle — bài Mutual Information, Target Encoding và các bài tạo đặc trưng (Khoá học, tiếng Anh, 4 giờ). Học bằng bài tập, có cả bài về mã hoá theo biến mục tiêu và nguy cơ rò rỉ; trang chưa được kiểm trực tiếp.
- **Xem thêm:** [StatQuest: One-Hot, Label, Target and K-Fold Target Encoding](https://youtu.be/589nCGeWG1w), Josh Starmer — toàn video (Video, tiếng Anh, 15 phút). Giải thích các cách mã hoá biến phân loại; chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Imputation of missing values](https://scikit-learn.org/stable/modules/impute.html), scikit-learn — SimpleImputer, KNNImputer, MissingIndicator (Bài viết, tiếng Anh, 30 phút). Điền thiếu và đánh dấu thiếu, đúng nội dung nút.
- **Xem thêm:** [imbalanced-learn User Guide](https://imbalanced-learn.org/stable/user_guide.html), imbalanced-learn developers — mục Over-sampling, Under-sampling, Common pitfalls and recommended practices (Bài viết, tiếng Anh, 40 phút). Chỉ cách xử lý lệch lớp và bẫy khi tăng mẫu trước kiểm định.
- **Tiếng Việt:** [Machine Learning cơ bản, bài 11: Feature Engineering](https://machinelearningcoban.com/general/2017/02/06/featureengineering/), Vũ Hữu Tiệp — toàn bài (Bài viết, tiếng Việt, 30 phút). Tiếng Việt, khái quát các kiểu đặc trưng.

### Lề và kernel · Kết Đan tầng 3

`kd_svm`

*Xem lề và kernel ở mức hình học; thử SVC với RBF trên dữ liệu hai trăng và đổi C, gamma.*

- **Chính:** [Machine Learning cơ bản, bài 19 đến 21: Support Vector Machine, Soft Margin, Kernel SVM](https://machinelearningcoban.com/2017/04/09/smv/), Vũ Hữu Tiệp — bài 19 (lề), bài 20 (soft margin: https://machinelearningcoban.com/2017/04/13/softmarginsmv/), bài 21 (kernel: https://machinelearningcoban.com/2017/04/22/kernelsmv/); đọc phần ý tưởng, bỏ phần đối ngẫu (Bài viết, tiếng Việt, 90 phút). Đủ lề, vectơ hỗ trợ và mẹo kernel bằng tiếng Việt.
- **Xem thêm:** [StatQuest: Support Vector Machines, Clearly Explained](https://youtu.be/efR1C6CvhmE), Josh Starmer — toàn video (Video, tiếng Anh, 20 phút). Trực giác lề và kernel không cần chứng minh; chưa mở được YouTube để kiểm.
- **Xem thêm:** [scikit-learn: Support Vector Machines, mục Kernel functions](https://scikit-learn.org/stable/modules/svm.html), scikit-learn — mục 1.4.6 Kernel functions, tham số C và gamma của RBF (Bài viết, tiếng Anh, 20 phút). Cách chọn C và gamma khi dùng thật.
- **Luyện tập:** [Hands-On ML 3e, chương 5: Support Vector Machines](https://github.com/ageron/handson-ml3), Aurélien Géron — 05_support_vector_machines.ipynb (Code, tiếng Anh, 60 phút). Chạy kernel tuyến tính, đa thức, RBF.

### Thiên kiếp Kết Đan: một cuộc thi dữ liệu · Kết Đan tầng 3

`du_an_ket_dan`

*Dựng mô hình nền trong ngày đầu, ghi điểm kiểm định chéo, thêm một thay đổi mỗi lần, rồi kết hợp vài mô hình; cuối cùng viết lại bài học.*

- **Chính:** [Kaggle: Spaceship Titanic (cuộc thi nhập môn)](https://www.kaggle.com/competitions/spaceship-titanic), Kaggle — cuộc thi; dùng làm cuộc thi bảng đầu tiên, đọc notebook công khai sau khi tự làm một bản (Bài tập, tiếng Anh, 10 giờ). Cuộc thi khởi đầu, dữ liệu bảng, có bảng xếp hạng; cần tài khoản Kaggle.
- **Xem thêm:** [Kaggle: House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques), Kaggle — cuộc thi hồi quy kinh điển (Bài tập, tiếng Anh, 10 giờ). Hợp để thực hành kiểm định chéo và kết hợp mô hình.
- **Xem thêm:** [Kaggle: Titanic - Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic), Kaggle — cuộc thi khởi đầu nổi tiếng (Bài tập, tiếng Anh, 5 giờ). Dễ làm nhưng bảng xếp hạng đã đầy điểm gian; dùng để học quy trình, không để so thứ hạng.

Thực chiến:

- Dữ liệu: [Spaceship Titanic (Kaggle)](https://www.kaggle.com/competitions/spaceship-titanic) (giấy phép: chưa rõ giấy phép: dữ liệu theo điều khoản cuộc thi Kaggle, không đóng gói trong game; kích thước ước lượng, 1 MB). Người chơi tải một lần bằng tài khoản Kaggle của mình.
- Dữ liệu: [House Prices (Kaggle)](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques) (giấy phép: chưa rõ giấy phép: điều khoản cuộc thi Kaggle; kích thước ước lượng, 1 MB). Dữ liệu Ames, hồi quy.
- Dữ liệu: [Adult / Census Income (UCI)](https://archive.ics.uci.edu/dataset/2/adult) (giấy phép: CC BY 4.0 (đã kiểm), 5.7 MB). Phương án đóng gói được trong game nếu muốn một 'cuộc thi' ngoại tuyến tự chấm.
- Bản mẫu: [Hands-On ML 3e, chương 7](https://github.com/ageron/handson-ml3), Aurélien Géron — 07_ensemble_learning_and_random_forests.ipynb (Code, tiếng Anh, 90 phút). Mã kết hợp mô hình.
- Đích: Chưa kiểm chứng điểm cụ thể: mục tiêu là vượt mô hình nền và vào nửa trên của bảng xếp hạng công khai; cần tự lấy số từ bảng xếp hạng lúc làm.
- Chạy ở đâu: CPU máy xách tay; mô hình cây và boosting trên vài chục nghìn dòng chạy trong vài phút; không cần GPU.

**Đã xem và không chọn:**

- Andrew Ng Machine Learning Specialization (làm nguồn chính): Trang cho thấy cập nhật tháng 9 năm 2026, có thể học miễn phí theo kiểu dự thính nhưng không có chứng chỉ; dùng TensorFlow, dài; chỉ nên coi là nguồn bổ sung.
- Stanford CS229 lecture notes: Trang khoá không cho đường dẫn ghi chú công khai; tài liệu chính nằm sau tài khoản Stanford.
- R2D3 A Visual Introduction to Machine Learning: Trang trả lỗi 522 khi kiểm, không xác nhận được; MLU-Explain thay thế được.
- Trustworthy Online Controlled Experiments làm nguồn chính cho người mới: Sách thương mại trả phí, dày; chỉ phù hợp tham khảo.
- ISLP chương 9 làm nguồn SVM chính: Chứng minh đối ngẫu nặng hơn mục tiêu của nút (chỉ cần trực giác).
- Nielsen Neural Networks and Deep Learning: Trang báo lỗi chứng chỉ khi kiểm nên không dùng làm nguồn đã kiểm.

## Học Sâu

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Neural Networks: Zero to Hero (8 bài)](https://karpathy.ai/zero-to-hero.html), Andrej Karpathy — xem theo thứ tự micrograd, makemore 1-5, GPT, tokenizer (Video, tiếng Anh, 13 giờ). Tuyến chính của nhánh: tự gõ lại từng dòng.
2. [Đắm mình vào Học Sâu (bản dịch tay v0.15)](https://github.com/d2l-ai/d2l-vi/tree/v0.15), Aston Zhang và cộng sự; nhóm dịch Việt — mã nguồn bản dịch, mỗi chương một thư mục, file *_vn.md (Sách, tiếng Việt). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.
3. [3Blue1Brown: Neural Networks](https://www.3blue1brown.com/neural-networks), 3Blue1Brown — chương 1-6, đủ để có trực giác trước khi viết mã (Video, tiếng Anh, 2 giờ). Dùng làm bước hình dung trước khi gõ mã.

### Tự viết autograd · Nguyên Anh tầng 1

`na_autograd`

*Xem video micrograd và gõ lại hết, đối chiếu gradient với PyTorch; bỏ qua phần vẽ biểu đồ Graphviz nếu thiếu thời gian.*

- **Chính:** [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtu.be/VMj-3S1tku0), Andrej Karpathy — toàn bộ video (2h25), gõ code theo (Video, tiếng Anh, 2 giờ). Tự viết bộ vi phân tự động từ số 0, thấy tận mắt lan truyền ngược chạy ra sao.
- **Xem thêm:** [micrograd (kho mã)](https://github.com/karpathy/micrograd), Andrej Karpathy — engine.py (~100 dòng) và nn.py (~50 dòng), notebook demo.ipynb (Code, tiếng Anh, 30 phút). Bản tham chiếu nhỏ gọn để đối chiếu với bản tự viết; giấy phép MIT.
- **Xem thêm:** [Deep Learning Systems, HW1: Building an automatic differentiation framework](https://dlsyscourse.org/), CMU (Kolter, Chen) — HW1 trong 5 bài tập (offering Fall 2026) (Khoá học, tiếng Anh, 10 giờ). Nếu muốn bản nghiêm túc hơn micrograd (tensor thay vì số vô hướng).
- **Luyện tập:** [PyTorch Learn the Basics: Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), PyTorch — toàn bài (Bài viết, tiếng Anh, 20 phút). Đối chiếu với autograd tự viết: cùng ý tưởng, thư viện thật.
- **Tiếng Việt:** [Đắm mình vào Học Sâu: 2.5 Tính vi phân tự động](https://github.com/d2l-ai/d2l-vi/blob/v0.15/chapter_preliminaries/autograd_vn.md), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — bản dịch tay v0.15 trên GitHub (Sách, tiếng Việt, 40 phút). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

Thực chiến:

- Dữ liệu: [Dữ liệu hai vầng trăng (tạo bằng sklearn make_moons)](https://github.com/karpathy/micrograd) (giấy phép: MIT (mã trong kho micrograd), 0.01 MB). Không cần tải, tự sinh 100 điểm; đủ nhỏ để chạy từng bước.
- Bản mẫu: [micrograd (kho mã)](https://github.com/karpathy/micrograd), Andrej Karpathy — engine.py (~100 dòng) và nn.py (~50 dòng), notebook demo.ipynb (Code, tiếng Anh, 30 phút). Bản tham chiếu nhỏ gọn để đối chiếu với bản tự viết; giấy phép MIT.
- Đích: Gradient tự viết khớp PyTorch (sai số dưới 1e-6) trên một biểu thức nhỏ, rồi mạng 2 lớp ẩn phân loại được tập hai vầng trăng; con số cụ thể chưa kiểm chứng, README không nêu.
- Chạy ở đâu: CPU laptop, dưới 1 phút, chỉ cần Python thuần (và PyTorch để so sánh).

### PyTorch · Nguyên Anh tầng 1

`na_pytorch`

*Làm trọn chuỗi 'Learn the Basics' theo thứ tự, mỗi bài gõ lại; chỉ khi quen mới đọc phụ lục A của Raschka.*

- **Chính:** [PyTorch Learn the Basics: Quickstart](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html), PyTorch — trang đầu trong chuỗi 8 bài (Bài viết, tiếng Anh, 30 phút). Một vòng huấn luyện hoàn chỉnh trên ảnh trong nửa giờ.
- **Xem thêm:** [PyTorch Learn the Basics: Tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html), PyTorch — toàn bài (Bài viết, tiếng Anh, 20 phút). Làm quen tensor, chuyển sang GPU, phép toán cơ bản.
- **Xem thêm:** [Build a Large Language Model (From Scratch), Phụ lục A: Giới thiệu PyTorch](https://github.com/rasbt/LLMs-from-scratch), Sebastian Raschka — thư mục appendix-A (Code, tiếng Anh, 90 phút). Phần dẫn nhập PyTorch hướng tới mô hình ngôn ngữ, có đáp án.
- **Luyện tập:** [PyTorch Learn the Basics: Optimization Loop](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html), PyTorch — toàn bài (Bài viết, tiếng Anh, 25 phút). Vòng lặp huấn luyện-kiểm tra chuẩn mà mọi dự án đều dùng.

### Nghề huấn luyện mạng · Nguyên Anh tầng 2

`na_huan_luyen`

*Xem makemore phần 3 trước, rồi đọc Recipe để có quy trình; phần 4 (backprop ninja) làm sau, không bắt buộc.*

- **Chính:** [Building makemore Part 3: Activations & Gradients, BatchNorm](https://youtu.be/P6sfmUTpUmc), Andrej Karpathy — toàn bộ (1h55): khởi tạo, thống kê kích hoạt, BatchNorm (Video, tiếng Anh, 115 phút). Dạy cách chẩn đoán mạng bằng biểu đồ kích hoạt và gradient, đúng tinh thần nút này.
- **Xem thêm:** [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/), Andrej Karpathy — toàn bài: sáu bước từ làm quen dữ liệu đến vắt kiệt hiệu năng (Bài viết, tiếng Anh, 25 phút). Quy trình huấn luyện thực tế: kiểm tra dữ liệu, overfit một batch, rồi mới regularize.
- **Xem thêm:** [CS231n: Neural Networks Part 3: Learning and Evaluation](https://cs231n.github.io/neural-networks-3/), Stanford CS231n — kiểm tra gradient, theo dõi mất mát, tối ưu, siêu tham số (Bài viết, tiếng Anh, 40 phút). Ghi chú ngắn, chuẩn, về những gì cần nhìn khi huấn luyện.
- **Xem thêm:** [CS231n: Neural Networks Part 2: Setting up the Data and the Loss](https://cs231n.github.io/neural-networks-2/), Stanford CS231n — tiền xử lý, khởi tạo trọng số, BatchNorm, regularization (Bài viết, tiếng Anh, 40 phút). Giải thích khởi tạo và chuẩn hoá bằng lời đơn giản.
- **Luyện tập:** [Building makemore Part 4: Becoming a Backprop Ninja](https://youtu.be/q8SA3rM6ckI), Andrej Karpathy — toàn bộ (1h55): tự tính ngược từng tensor bằng tay (Video, tiếng Anh, 115 phút). Bài tập tự viết lan truyền ngược cho cả mạng, nên làm sau micrograd.

### Mạng tích chập · Nguyên Anh tầng 2

`na_cnn`

*Đọc ghi chú CS231n về tích chập, rồi làm chương CNN của d2l; WaveNet chỉ xem khi muốn thấy chia sẻ trọng số theo chuỗi.*

- **Chính:** [CS231n: Convolutional Neural Networks: Architectures, Convolution / Pooling Layers](https://cs231n.github.io/convolutional-networks/), Stanford CS231n (bản Spring 2026) — toàn bài: lớp tích chập, pooling, kích thước đầu ra (Bài viết, tiếng Anh, 45 phút). Ghi chú kinh điển về tích chập, có minh hoạ kích thước từng lớp.
- **Xem thêm:** [Practical Deep Learning for Coders 2022, bài 8: Convolutions (CNNs)](https://course.fast.ai/), Jeremy Howard (fast.ai) — Part 1 (bản 2022), bài 8 (Khoá học, tiếng Anh, 90 phút). Dạy CNN bằng cách tự cài, hợp với người thích làm trước hiểu sau.
- **Xem thêm:** [Building makemore Part 5: Building a WaveNet](https://youtu.be/t3YJ5hKiMQ0), Andrej Karpathy — toàn bộ (56 phút) (Video, tiếng Anh, 56 phút). Cho thấy tích chập nhân quả và cách xếp tầng, cầu nối giữa MLP và mạng chuỗi.
- **Tiếng Việt:** [Đắm mình vào Học Sâu: chương 6 Mạng nơ-ron tích chập](https://github.com/d2l-ai/d2l-vi/tree/v0.15/chapter_convolutional-neural-networks), Aston Zhang và cộng sự; nhóm dịch Việt — bản dịch tay v0.15 trên GitHub (Sách, tiếng Việt). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Embedding và mô hình chuỗi · Nguyên Anh tầng 3

`na_chuoi`

*Đọc Word2vec bằng hình, rồi xem makemore phần 2 để tự dựng embedding; RNN/LSTM đọc lướt, vì attention sẽ thay thế.*

- **Chính:** [The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/), Jay Alammar — mục 'Word Embeddings' đến 'Skipgram with Negative Sampling' (Bài viết, tiếng Anh, 30 phút). Giải thích vì sao từ thành vectơ và vectơ mang nghĩa, bằng hình.
- **Xem thêm:** [Building makemore Part 2: MLP](https://youtu.be/TCH_1BHY58I), Andrej Karpathy — toàn bộ (1h15): embedding ký tự, tách train/val/test (Video, tiếng Anh, 75 phút). Embedding là bảng tra và học được; đây là bước đệm tự nhiên tới attention.
- **Xem thêm:** [Dive into Deep Learning, chương 9-10: mạng hồi quy](https://d2l.ai/), Aston Zhang và cộng sự — chương 9 (RNN) và 10 (RNN hiện đại) (Sách, tiếng Anh, 3 giờ). Hiểu giới hạn của RNN để thấy vì sao cần attention.
- **Tiếng Việt:** [Đắm mình vào Học Sâu: chương 8 Mạng nơ-ron hồi tiếp](https://github.com/d2l-ai/d2l-vi/tree/v0.15/chapter_recurrent-neural-networks), Aston Zhang và cộng sự; nhóm dịch tình nguyện tiếng Việt — bản dịch tay v0.15 trên GitHub (Sách, tiếng Việt, 3 giờ). Bản dịch tay của nhóm tình nguyện (v0.15), đọc trên GitHub vì tên miền của trang sách cũ đã bị chiếm; bản ở vi.d2l.ai là dịch máy, sai thuật ngữ.

### Thiên kiếp Nguyên Anh: một mô hình ảnh huấn luyện tử tế · Nguyên Anh tầng 3

`du_an_nguyen_anh`

*Làm đúng 6 bước của Recipe trên một tập ảnh nhỏ, có đối chứng (một thay đổi mỗi lần) và viết báo cáo ngắn kèm đường mất mát.*

- **Chính:** [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/), Andrej Karpathy — toàn bài: sáu bước từ làm quen dữ liệu đến vắt kiệt hiệu năng (Bài viết, tiếng Anh, 25 phút). Quy trình huấn luyện thực tế: kiểm tra dữ liệu, overfit một batch, rồi mới regularize.
- **Xem thêm:** [CS231n: Transfer Learning and Fine-tuning Convolutional Neural Networks](https://cs231n.github.io/transfer-learning/), Stanford CS231n — toàn bài (Bài viết, tiếng Anh, 15 phút). Ngắn gọn về khi nào đóng băng, khi nào tinh chỉnh.
- **Xem thêm:** [CS231n: Neural Networks Part 3: Learning and Evaluation](https://cs231n.github.io/neural-networks-3/), Stanford CS231n — kiểm tra gradient, theo dõi mất mát, tối ưu, siêu tham số (Bài viết, tiếng Anh, 40 phút). Ghi chú ngắn, chuẩn, về những gì cần nhìn khi huấn luyện.
- **Luyện tập:** [cifar10-airbench: huấn luyện CIFAR-10 đạt 94% trong vài giây](https://github.com/KellerJordan/cifar10-airbench), Keller Jordan — airbench94_muon.py và README (Code, tiếng Anh, 60 phút). Mốc tham chiếu về một đường ống tối ưu; MIT.

Thực chiến:

- Dữ liệu: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) (giấy phép: MIT, 35 MB). 60 nghìn ảnh 28x28, huấn luyện được trên CPU.
- Dữ liệu: [CIFAR-10 (bản Python)](https://cave.cs.toronto.edu/kriz/cifar.html) (giấy phép: Không ghi rõ giấy phép, chỉ yêu cầu trích dẫn Krizhevsky 2009, 163 MB). 60 nghìn ảnh màu 32x32; khó hơn, cần GPU miễn phí.
- Bản mẫu: [cifar10-airbench](https://github.com/KellerJordan/cifar10-airbench), Keller Jordan — airbench94_muon.py (Code, tiếng Anh, 60 phút). Bản tối ưu cao; README báo 94.01% trong 2.59 giây trên A100.
- Đích: Fashion-MNIST: CNN 2 lớp tích chập đạt khoảng 92% (bảng của kho Zalando, người dùng tự báo, chưa kiểm). CIFAR-10: CNN nhỏ không tăng cường dữ liệu khoảng 82-85% là hợp lý; bản airbench đạt 94% là mốc trần.
- Chạy ở đâu: Fashion-MNIST chạy trên CPU laptop vài phút mỗi lượt. CIFAR-10 nên dùng GPU miễn phí: Colab không đảm bảo GPU và phiên tối đa 12 giờ (trang FAQ chính thức); Kaggle theo các nguồn thứ cấp có khoảng 30 giờ GPU/tuần (chưa kiểm chứng trên trang chính thức).

### Attention và Transformer · Hóa Thần tầng 1

`ht_attention`

*Thứ tự: 3Blue1Brown (hình), Illustrated Transformer (chi tiết), rồi Let's build GPT (mã); Annotated Transformer chỉ để đối chiếu bài báo gốc.*

- **Chính:** [Neural Networks, chương 6: Attention in transformers, step-by-step](https://www.3blue1brown.com/lessons/attention), 3Blue1Brown — video ~26 phút (ra 4/2024) (Video, tiếng Anh, 26 phút). Hình dung truy vấn-khoá-giá trị chạy từng bước, trước khi đọc công thức.
- **Xem thêm:** [Neural Networks, chương 5: Transformers, the tech behind LLMs](https://www.3blue1brown.com/lessons/gpt), 3Blue1Brown — video ~27 phút (Video, tiếng Anh, 27 phút). Cái nhìn tổng thể về GPT và embedding bằng hình động.
- **Xem thêm:** [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), Jay Alammar — từ 'Self-Attention in Detail' đến 'The Decoder Side' (Bài viết, tiếng Anh, 40 phút). Hình minh hoạ tốt nhất cho Q/K/V và nhiều đầu attention.
- **Xem thêm:** [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/), Harvard NLP — toàn bài: bài báo 'Attention Is All You Need' kèm mã PyTorch (Code, tiếng Anh, 2 giờ). Đối chiếu từng câu của bài báo với từng dòng mã, vừa là bài tái lập.
- **Luyện tập:** [Let's build GPT (phần self-attention)](https://www.youtube.com/watch?v=kCc8FmEb1nY), Andrej Karpathy — đoạn tính trung bình có trọng số đến self-attention (Video, tiếng Anh, 60 phút). Tự cài attention một đầu trong vài chục dòng.

### Tự xây một mô hình ngôn ngữ nhỏ · Hóa Thần tầng 1

`ht_gpt_nho`

*Xem Let's build GPT và gõ lại trên shakespeare_char trước; tokenizer và CS336 assignment 1 là phần nâng cao.*

- **Chính:** [Let's build GPT: from scratch, in code, spelled out.](https://www.youtube.com/watch?v=kCc8FmEb1nY), Andrej Karpathy — toàn bộ (1h56): từ bigram đến khối Transformer (Video, tiếng Anh, 116 phút). Cách rõ nhất để thấy attention và Transformer chỉ là vài chục dòng PyTorch.
- **Xem thêm:** [Let's build the GPT Tokenizer](https://youtu.be/zduSFxRajkE), Andrej Karpathy — toàn bộ (2h13): BPE, regex tách từ, token đặc biệt (Video, tiếng Anh, 2 giờ). Giải thích vì sao tách từ gây ra nhiều lỗi lạ của mô hình ngôn ngữ.
- **Xem thêm:** [minbpe (kho mã)](https://github.com/karpathy/minbpe), Andrej Karpathy — exercise.md: làm từng bước BasicTokenizer rồi RegexTokenizer (Code, tiếng Anh, 2 giờ). Có sẵn bài tập từng bước và test; giấy phép MIT.
- **Xem thêm:** [Build a Large Language Model (From Scratch), chương 2-5](https://github.com/rasbt/LLMs-from-scratch), Sebastian Raschka — ch02 dữ liệu, ch03 attention, ch04 mô hình GPT, ch05 tiền huấn luyện (Sách, tiếng Anh, trả phí, 10 giờ). Bản sách có giải thích từng bước; mã miễn phí, sách trả phí.
- **Luyện tập:** [CS336 assignment 1: Basics (BPE, Transformer, AdamW)](https://github.com/stanford-cs336/assignment1-basics), Stanford CS336 — toàn bộ bài tập 1 (có test tự chấm) (Bài tập, tiếng Anh, 20 giờ). Bản khó và nghiêm túc nhất để tự dựng tokenizer và mô hình; không bắt buộc.

Thực chiến:

- Dữ liệu: [Tiny Shakespeare (data/shakespeare_char của nanoGPT)](https://github.com/karpathy/nanoGPT) (giấy phép: MIT cho mã; văn bản Shakespeare thuộc phạm vi công cộng (chưa xác nhận trong README), 1.0 MB). Nhỏ nhất để thấy văn bản sinh ra hợp lý.
- Dữ liệu: [TinyStories (nên dùng tập validation)](https://huggingface.co/datasets/roneneldan/TinyStories) (giấy phép: CDLA-Sharing-1.0). Truyện ngắn từ vựng nhỏ; cả bộ 7.62 GB nên chỉ lấy tập validation 22 nghìn truyện (dung lượng chưa kiểm).
- Bản mẫu: [nanoGPT (kho mã, đã ngừng cập nhật)](https://github.com/karpathy/nanoGPT), Andrej Karpathy — mục quickstart: data/shakespeare_char (Code, tiếng Anh, 30 phút). Bản tham chiếu train.py/model.py gọn; README nói đã cũ nhưng vẫn chạy được, MIT.
- Bản mẫu: [nanochat (kho mã)](https://github.com/karpathy/nanochat), Andrej Karpathy — README: speedrun.sh và tham số --depth (Code, tiếng Anh, 60 phút). Đường ống trọn vẹn từ tokenizer đến chat; bản mới thay nanoGPT, MIT.
- Đích: shakespeare_char: mô hình 6 lớp đạt validation loss 1.4697 sau khoảng 3 phút trên một A100; cấu hình nhỏ chạy CPU/MacBook (4 lớp, 128 chiều, 2000 bước) đạt loss khoảng 1.88 trong khoảng 3 phút, chữ sinh ra còn kém (theo README nanoGPT).
- Chạy ở đâu: Cấu hình nhỏ chạy được trên CPU laptop; bản 6 lớp cần GPU: dùng Colab (GPU không bảo đảm, phiên tối đa 12 giờ) hoặc Kaggle (khoảng 30 giờ GPU/tuần theo nguồn thứ cấp, chưa kiểm chứng).

### Tiền huấn luyện và tinh chỉnh · Hóa Thần tầng 2

`ht_tinh_chinh`

*Học chương 3 của khoá Hugging Face với Trainer, rồi dùng PEFT/LoRA; tự cài LoRA của Raschka là phần mở rộng.*

- **Chính:** [Hugging Face LLM Course, chương 3: Fine-tuning a pretrained model](https://huggingface.co/learn/llm-course/chapter3/1), Hugging Face — 3 mục: xử lý dữ liệu, Trainer, vòng lặp tự viết với Accelerate (Khoá học, tiếng Anh, 2 giờ). Đúng thứ tự cần: dùng Trainer rồi mới tự viết vòng lặp.
- **Xem thêm:** [PEFT: Parameter-Efficient Fine-Tuning (tài liệu)](https://huggingface.co/docs/peft/index), Hugging Face — Quicktour và Method overview (LoRA) (Bài viết, tiếng Anh, 40 phút). Cách tinh chỉnh bằng LoRA trên GPU nhỏ.
- **Xem thêm:** [Build a Large Language Model (From Scratch), chương 6-7 và phụ lục E (LoRA)](https://github.com/rasbt/LLMs-from-scratch), Sebastian Raschka — ch06 phân loại, ch07 làm theo chỉ dẫn, appendix-E LoRA (Code, tiếng Anh, 6 giờ). Tự cài LoRA bằng PyTorch thuần trước khi dùng thư viện.
- **Luyện tập:** [Hugging Face LLM Course, chương 1-4: Transformers và tinh chỉnh](https://huggingface.co/learn/llm-course/chapter1/1), Hugging Face — chương 1 (mô hình hoạt động ra sao) đến chương 4 (Khoá học, tiếng Anh, 5 giờ). Khoá miễn phí có sổ tay chạy trên Colab.

Thực chiến:

- Dữ liệu: [Bộ spam SMS dùng trong chương 6 của Raschka](https://github.com/rasbt/LLMs-from-scratch) (giấy phép: chưa kiểm chứng (nguồn UCI, kiểm tra trước khi đóng gói), 0.5 MB). Bài phân loại nhị phân nhỏ, quen tay trước khi tinh chỉnh to hơn.
- Dữ liệu: [Wikipedia tiếng Việt (wikimedia/wikipedia, cấu hình 20231101.vi)](https://huggingface.co/datasets/wikimedia/wikipedia) (giấy phép: CC BY-SA 3.0 và GFDL). Văn bản tiếng Việt có giấy phép rõ, 1.29 triệu bài; chỉ lấy vài nghìn bài.
- Bản mẫu: [Hugging Face LLM Course, chương 3: Fine-tuning a pretrained model](https://huggingface.co/learn/llm-course/chapter3/1), Hugging Face — 3 mục: xử lý dữ liệu, Trainer, vòng lặp tự viết với Accelerate (Khoá học, tiếng Anh, 2 giờ). Đúng thứ tự cần: dùng Trainer rồi mới tự viết vòng lặp.
- Đích: Chưa kiểm chứng: chưa tìm được con số do tác giả công bố; hãy đo độ chính xác trước và sau tinh chỉnh và chỉ cần thấy cải thiện có đối chứng.
- Chạy ở đâu: Mô hình nhỏ với LoRA chạy được trên GPU miễn phí của Colab/Kaggle trong vài chục phút; CPU thì quá chậm.

### Dựng ứng dụng với mô hình ngôn ngữ lớn · Hóa Thần tầng 2

`ht_ung_dung_llm`

*Đọc Building effective agents trước, tự dựng một vòng lặp gọi công cụ nhỏ không dùng framework; khoá agents của Hugging Face chỉ khi cần.*

- **Chính:** [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), Anthropic — toàn bài (12/2024): workflow và agent, năm mẫu workflow (Bài viết, tiếng Anh, 25 phút). Nguyên tắc gọn: bắt đầu đơn giản, chỉ thêm độ phức tạp khi đo được lợi.
- **Xem thêm:** [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/), Lilian Weng — ba thành phần: planning, memory, tool use (Bài viết, tiếng Anh, 45 phút). Khung khái niệm tốt dù bài viết từ 2023.
- **Xem thêm:** [LLM Bootcamp: Augmented Language Models](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/augmented-language-models/), Full Stack Deep Learning — bài về truy xuất và công cụ (Video, tiếng Anh, 60 phút). Giải thích RAG từ gốc; nội dung 2023 nên đọc kèm tài liệu hiện nay.
- **Xem thêm:** [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction), Hugging Face — chương 0-4 (Khoá học, tiếng Anh, 10 giờ). Khoá miễn phí có thực hành; cập nhật chưa rõ.
- **Luyện tập:** [LLM Bootcamp: Project Walkthrough askFSDL](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/askfsdl-walkthrough/), Full Stack Deep Learning — toàn bộ (Video, tiếng Anh, 45 phút). Ví dụ dựng hỏi-đáp trên tài liệu từ đầu đến cuối.

Thực chiến:

- Dữ liệu: [Wikipedia tiếng Việt (vài nghìn bài)](https://huggingface.co/datasets/wikimedia/wikipedia) (giấy phép: CC BY-SA 3.0 và GFDL). Kho văn bản tiếng Việt để làm hỏi-đáp truy xuất.
- Bản mẫu: [askFSDL walkthrough](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/askfsdl-walkthrough/), Full Stack Deep Learning — toàn bộ (Video, tiếng Anh, 45 phút). Mẫu tham chiếu.
- Đích: Chưa kiểm chứng con số chuẩn; tự đặt 20-30 câu hỏi có đáp án và đo tỉ lệ trả lời đúng, nêu rõ nguồn.
- Chạy ở đâu: Gọi API mô hình lớn từ CPU laptop (có phí theo lượt gọi), hoặc mô hình nhỏ tải về chạy trên Colab/Kaggle.

### Đánh giá mô hình sinh · Hóa Thần tầng 3

`ht_danh_gia_llm`

*Đọc Your AI Product Needs Evals, rồi tự xem 100 kết quả của chính sản phẩm mình; benchmark học thuật để sau.*

- **Chính:** [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), Hamel Husain — toàn bài (3/2024): ba cấp unit test, người/mô hình chấm, A/B (Bài viết, tiếng Anh, 30 phút). Giải thích đánh giá là gì và vì sao quan trọng nhất, có ví dụ thực.
- **Xem thêm:** [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/), Hamel Husain — mục 1 (phân tích lỗi) và mục 5 (giữ tin cậy vào eval) (Bài viết, tiếng Anh, 30 phút). Dạy phân tích lỗi trước khi viết bộ chấm.
- **Xem thêm:** [ARENA chương 3: LLM Evaluations](https://arena.education/chapter3), ARENA — xây benchmark trắc nghiệm, đánh giá agent (Khoá học, tiếng Anh, 10 giờ). Bài tập lập trình cho đánh giá.
- **Xem thêm:** [CS336 bài 12: Evaluation](https://cs336.stanford.edu/), Stanford CS336 (2026) — bài 12 trong lịch học (Video, tiếng Anh, 80 phút). Góc nhìn nghiên cứu về benchmark và những cái bẫy.

Thực chiến:

- Dữ liệu: [Bộ câu hỏi tự tạo 50-100 mục có đáp án](https://hamel.dev/blog/posts/evals/) (giấy phép: tự sở hữu, 0.1 MB). Đánh giá tốt nhất xuất phát từ dữ liệu thật của chính bạn.
- Bản mẫu: [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), Hamel Husain — mục Level 1: Unit Tests (Bài viết, tiếng Anh, 30 phút). Mẫu cấu trúc bộ test.
- Đích: Một bộ đánh giá chạy tự động được, có số liệu trước/sau mỗi thay đổi; không có con số chuẩn để so sánh.
- Chạy ở đâu: CPU laptop; chi phí chỉ là số lần gọi mô hình để chấm.

### Thiên kiếp Hóa Thần: một sản phẩm dùng mô hình ngôn ngữ · Hóa Thần tầng 3

`du_an_hoa_than`

*Chọn một vấn đề có người dùng thật quanh bạn, ra bản đầu trong hai tuần và đo bằng bộ đánh giá của mình.*

- **Chính:** [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/), Hamel Husain — toàn bài, nhất là mục 6: lộ trình đếm số thí nghiệm (Bài viết, tiếng Anh, 30 phút). Quy trình biến phản hồi người dùng thành cải tiến có đo lường.
- **Xem thêm:** [LLM Bootcamp: LLMOps](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/), Full Stack Deep Learning — toàn bài (Video, tiếng Anh, 60 phút). Đưa sản phẩm lên chạy thật: chi phí, giám sát, an toàn.
- **Xem thêm:** [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), Hamel Husain — toàn bài (Bài viết, tiếng Anh, 30 phút). Bộ đánh giá của riêng mình.

Thực chiến:

- Dữ liệu: [Tài liệu tiếng Việt có giấy phép rõ (Wikipedia vi)](https://huggingface.co/datasets/wikimedia/wikipedia) (giấy phép: CC BY-SA 3.0 và GFDL). Nguồn kiến thức an toàn về bản quyền cho sản phẩm thử.
- Bản mẫu: [askFSDL walkthrough](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/askfsdl-walkthrough/), Full Stack Deep Learning — toàn bộ (Video, tiếng Anh, 45 phút). Mẫu dự án trọn vẹn.
- Đích: Có ít nhất 3 người dùng thật ngoài bạn dùng, và bộ đánh giá riêng cho thấy xu hướng tốt lên qua vài vòng; không có con số chuẩn.
- Chạy ở đâu: Chủ yếu gọi API; phần chạy cục bộ dùng CPU laptop hoặc GPU miễn phí.

**Đã xem và không chọn:**

- d2l.aivivn.com (bản dịch cũ của Đắm mình vào học sâu): Khi kiểm tra ngày 2026-11-19 trang trả về nội dung quảng cáo cờ bạc, không phải sách; dùng vi.d2l.ai.
- Karpathy nanoGPT làm bản tham chiếu chính: README tự nói đã cũ, nên ưu tiên nanochat cho phần mới và chỉ dùng nanoGPT cho bài shakespeare nhỏ.
- Hugging Face Deep RL course làm nguồn RL chính: README nói ở trạng thái bảo trì thấp, đơn vị AI vs AI và bảng xếp hạng đã hỏng.
- Toàn bộ CS336 làm nguồn chính cho người mới: Quá nặng (19 buổi, 5 bài tập) cho năm nhất; chỉ lấy assignment 1 và vài buổi.
- Papers with Code: Chưa kiểm chứng được tình trạng 2026 trong lần này nên không dựa vào.
- d2l.aivivn.com (trang cũ của Đắm mình vào Học Sâu): Tên miền đã bị chiếm: trang chủ hiện là quảng cáo cờ bạc. Dùng bản dịch tay trên GitHub (thẻ v0.15).
- vi.d2l.ai (Đắm mình vào Học Sâu 0.17.5): Bản dịch máy, sai thuật ngữ (mạng tích chập thành 'mạng thần kinh phức tạp'). Không dùng làm nguồn tiếng Việt.

## Hệ Thống

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [Designing Machine Learning Systems](https://github.com/chiphuyen/dmls-book), Chip Huyen (O'Reilly 2022) — mục lục và tóm tắt chương trong kho; chương 1, 2 và 11 cho người không chuyên (Sách, tiếng Anh, trả phí). Sách trả phí; kho mã miễn phí có tóm tắt, giấy phép chưa rõ.
2. [Full Stack Deep Learning 2022, Bài 1: Course Vision and When to Use ML](https://fullstackdeeplearning.com/course/2022/lecture-1-course-vision-and-when-to-use-ml/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Bản đồ toàn bộ vòng đời hệ thống học máy.
3. [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club (Alexey Grigorev) — 6 mô-đun: theo dõi thí nghiệm, điều phối, triển khai, giám sát, thực hành tốt, dự án cuối (Khoá học, tiếng Anh, 67 giờ). Miễn phí, có bài tập; bản 2025 là lần mới nhất, trang nói chưa có khoá trực tiếp 2026.

### Kỹ thuật phần mềm cho học máy · Luyện Hư tầng 1

`lh_ky_thuat_phan_mem`

*Đọc Rules of ML và Made With ML (Testing, Styling, Pre-commit) song song; bài báo Technical Debt đọc để hiểu vì sao cần làm vậy.*

- **Chính:** [Made With ML](https://madewithml.com/), Goku Mohandas — mục MLOps: Testing (code, data, models), Reproducibility, Production (CI/CD, monitoring) (Khoá học, tiếng Anh, 20 giờ). Tập bài viết có mã đi từ thí nghiệm đến sản xuất; chưa kiểm tình trạng cập nhật.
- **Xem thêm:** [Rules of Machine Learning: Best Practices for ML Engineering](https://developers.google.com/machine-learning/guides/rules-of-ml), Martin Zinkevich (Google) — bốn giai đoạn: Before ML, Phase I pipeline, Phase II đặc trưng, Phase III (Bài viết, tiếng Anh, 90 phút). Những quy tắc thực chiến cho hệ thống học máy trong sản xuất.
- **Xem thêm:** [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html), Sculley và cộng sự (NIPS 2015) — toàn bài báo (nhấn mạnh các 'mùi' hệ thống) (Bài báo, tiếng Anh, 40 phút). Bài báo nền tảng giải thích vì sao mã học máy khó bảo trì.
- **Xem thêm:** [Full Stack Deep Learning 2022, Bài 3: Troubleshooting & Testing](https://fullstackdeeplearning.com/course/2022/lecture-3-troubleshooting-and-testing/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Cách kiểm thử và chẩn bệnh mã học máy.

### Đường ống dữ liệu · Luyện Hư tầng 1

`lh_du_lieu_lon`

*Xem bài 4 FSDL, rồi đọc tóm tắt chương dữ liệu của Chip Huyen; Zoomcamp mô-đun điều phối để thực hành đường ống.*

- **Chính:** [Full Stack Deep Learning 2022, Bài 4: Data Management](https://fullstackdeeplearning.com/course/2022/lecture-4-data-management/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Tổng quan về nguồn, gán nhãn, phiên bản và đường ống dữ liệu.
- **Xem thêm:** [Designing Machine Learning Systems](https://github.com/chiphuyen/dmls-book), Chip Huyen (O'Reilly 2022) — mục lục và tóm tắt chương trong kho; chương 1, 2 và 11 cho người không chuyên (Sách, tiếng Anh, trả phí). Sách trả phí; kho mã miễn phí có tóm tắt, giấy phép chưa rõ.
- **Xem thêm:** [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club (Alexey Grigorev) — 6 mô-đun: theo dõi thí nghiệm, điều phối, triển khai, giám sát, thực hành tốt, dự án cuối (Khoá học, tiếng Anh, 67 giờ). Miễn phí, có bài tập; bản 2025 là lần mới nhất, trang nói chưa có khoá trực tiếp 2026.

### Huấn luyện ở quy mô lớn · Luyện Hư tầng 2

`lh_huan_luyen_lon`

*Xem bài 2 và 5 của CS336 trước để hiểu bộ nhớ GPU; song song hoá (bài 7-8) chỉ cần nắm ý, không cần tự cài.*

- **Chính:** [CS336 bài 5, 7, 8: GPUs, Parallelism (Spring 2026)](https://cs336.stanford.edu/), Stanford CS336 — bài 2 (FLOPs/bộ nhớ), 5 (GPU, TPU), 7-8 (song song hoá) (Video, tiếng Anh, 4 giờ). Trình bày giới hạn bộ nhớ và cách chia dữ liệu/mô hình qua nhiều GPU.
- **Xem thêm:** [MIT 6.5940 TinyML and Efficient Deep Learning, bài 19-20: Distributed Training](https://hanlab.mit.edu/courses/2024-fall-65940), Song Han (MIT, Fall 2024) — bài 19 và 20 (Video, tiếng Anh, 3 giờ). Phiên bản dễ thở hơn, có video.
- **Xem thêm:** [nanochat (kho mã)](https://github.com/karpathy/nanochat), Andrej Karpathy — README: speedrun.sh và tham số --depth (Code, tiếng Anh, 60 phút). Đường ống trọn vẹn từ tokenizer đến chat; bản mới thay nanoGPT, MIT.
- **Luyện tập:** [CS336 assignment 2: Systems](https://github.com/stanford-cs336/assignment2-systems), Stanford CS336 — toàn bộ (Bài tập, tiếng Anh, 20 giờ). Bài tập tự viết attention bằng Triton và song song hoá; rất nặng.

### Triển khai và phục vụ mô hình · Luyện Hư tầng 2

`lh_trien_khai`

*Xem bài 5 FSDL rồi làm mô-đun Model Deployment của Zoomcamp; lượng tử hoá của MIT là phần mở rộng.*

- **Chính:** [Full Stack Deep Learning 2022, Bài 5: Deployment](https://fullstackdeeplearning.com/course/2022/lecture-5-deployment/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Các mẫu phục vụ mô hình: API, container, tối ưu.
- **Xem thêm:** [MIT 6.5940, bài 5-6: Quantization và bài 13: Efficient LLM Deployment](https://hanlab.mit.edu/courses/2024-fall-65940), Song Han (MIT, Fall 2024) — bài 5, 6, 13 (Video, tiếng Anh, 4 giờ). Lượng tử hoá để giảm chi phí và độ trễ.
- **Xem thêm:** [CS336 bài 10: Inference](https://cs336.stanford.edu/), Stanford CS336 (2026) — bài 10 (Video, tiếng Anh, 80 phút). Nút thắt khi phục vụ mô hình lớn.
- **Xem thêm:** [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club (Alexey Grigorev) — 6 mô-đun: theo dõi thí nghiệm, điều phối, triển khai, giám sát, thực hành tốt, dự án cuối (Khoá học, tiếng Anh, 67 giờ). Miễn phí, có bài tập; bản 2025 là lần mới nhất, trang nói chưa có khoá trực tiếp 2026.

### Giám sát và thí nghiệm trực tuyến · Luyện Hư tầng 3

`lh_giam_sat`

*Làm mô-đun giám sát của Zoomcamp trước; bài 6 FSDL cho bức tranh về vòng đời mô hình.*

- **Chính:** [MLOps Zoomcamp, mô-đun 5: Model Monitoring](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club — mô-đun Model Monitoring (Khoá học, tiếng Anh, 6 giờ). Thực hành đo trôi dữ liệu và dựng bảng giám sát.
- **Xem thêm:** [Full Stack Deep Learning 2022, Bài 6: Continual Learning](https://fullstackdeeplearning.com/course/2022/lecture-6-continual-learning/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Cách học liên tục và thí nghiệm trực tuyến.
- **Xem thêm:** [Rules of Machine Learning: Best Practices for ML Engineering](https://developers.google.com/machine-learning/guides/rules-of-ml), Martin Zinkevich (Google) — bốn giai đoạn: Before ML, Phase I pipeline, Phase II đặc trưng, Phase III (Bài viết, tiếng Anh, 90 phút). Những quy tắc thực chiến cho hệ thống học máy trong sản xuất.
- **Xem thêm:** [Made With ML](https://madewithml.com/), Goku Mohandas — mục MLOps: Testing (code, data, models), Reproducibility, Production (CI/CD, monitoring) (Khoá học, tiếng Anh, 20 giờ). Tập bài viết có mã đi từ thí nghiệm đến sản xuất; chưa kiểm tình trạng cập nhật.

### Thiên kiếp Luyện Hư: vận hành một hệ thống học máy · Luyện Hư tầng 3

`du_an_luyen_hu`

*Làm dự án cuối của Zoomcamp: huấn luyện, triển khai, giám sát, mô phỏng trôi dữ liệu và ghi lại sự cố.*

- **Chính:** [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club (Alexey Grigorev) — 6 mô-đun: theo dõi thí nghiệm, điều phối, triển khai, giám sát, thực hành tốt, dự án cuối (Khoá học, tiếng Anh, 67 giờ). Miễn phí, có bài tập; bản 2025 là lần mới nhất, trang nói chưa có khoá trực tiếp 2026.
- **Xem thêm:** [Made With ML](https://madewithml.com/), Goku Mohandas — mục MLOps: Testing (code, data, models), Reproducibility, Production (CI/CD, monitoring) (Khoá học, tiếng Anh, 20 giờ). Tập bài viết có mã đi từ thí nghiệm đến sản xuất; chưa kiểm tình trạng cập nhật.
- **Xem thêm:** [Full Stack Deep Learning 2022, Bài 8: ML Teams and Project Management](https://fullstackdeeplearning.com/course/2022/lecture-8-teams-and-pm/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Quản lý dự án học máy.

Thực chiến:

- Dữ liệu: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) (giấy phép: MIT, 35 MB). Nhỏ, dễ phục vụ và dễ giả lập trôi dữ liệu (xoay, nhiễu ảnh).
- Dữ liệu: [CIFAR-10 (bản Python)](https://cave.cs.toronto.edu/kriz/cifar.html) (giấy phép: không ghi rõ, yêu cầu trích dẫn, 163 MB). Dữ liệu khó hơn để giám sát chất lượng dự đoán.
- Bản mẫu: [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), DataTalks.Club (Alexey Grigorev) — 6 mô-đun: theo dõi thí nghiệm, điều phối, triển khai, giám sát, thực hành tốt, dự án cuối (Khoá học, tiếng Anh, 67 giờ). Miễn phí, có bài tập; bản 2025 là lần mới nhất, trang nói chưa có khoá trực tiếp 2026.
- Bản mẫu: [Made With ML](https://madewithml.com/), Goku Mohandas — mục MLOps: Testing (code, data, models), Reproducibility, Production (CI/CD, monitoring) (Khoá học, tiếng Anh, 20 giờ). Tập bài viết có mã đi từ thí nghiệm đến sản xuất; chưa kiểm tình trạng cập nhật.
- Đích: Chưa kiểm chứng con số chuẩn: mục tiêu là hệ thống chạy liên tục một tuần, có cảnh báo khi độ chính xác giảm và một bản ghi sự cố; độ chính xác Fashion-MNIST khoảng 92% từ CNN nhỏ.
- Chạy ở đâu: CPU laptop đủ cho mô hình nhỏ và Docker; GPU miễn phí (Colab không bảo đảm, Kaggle ~30 giờ/tuần theo nguồn thứ cấp) chỉ cần nếu dùng CIFAR-10.

**Đã xem và không chọn:**

- CMU Deep Learning Systems (dlsyscourse.org): Rất hay nhưng chủ yếu cho sinh viên ghi danh và bài tập nặng; chỉ dùng HW1 cho autograd.
- Stanford CS329S: Không tải được trang (chứng chỉ bị từ chối) nên không đưa vào.
- MLOps Zoomcamp làm nguồn duy nhất: Cần kiến thức Docker và cohort 2026 không mở; chỉ dùng tài liệu mở.
- Chip Huyen, AI Engineering (2025): Sách trả phí, chỉ có trang mua; không có phần miễn phí kiểm chứng được.
- FSDL 2022 làm nguồn mới nhất: Nội dung 2022 và bootcamp 2023: dùng cho khung ý tưởng, công cụ đã đổi nhiều.

## Nghiên Cứu và Dẫn Dắt

**Xương sống của nhánh** (theo thứ tự nên dùng):

1. [You and Your Research](https://www.cs.virginia.edu/~robins/YouAndYourResearch.html), Richard Hamming — toàn bài (bản chép lời bài nói 1986) (Bài viết, tiếng Anh, 60 phút). Bài nói kinh điển về chọn vấn đề lớn và làm việc cửa mở.
2. [How to Read a Paper](https://www.cs.princeton.edu/courses/archive/fall18/cos561/papers/HowToRead05.pdf), S. Keshav — toàn bài 3 trang: phương pháp ba lượt (Bài báo, tiếng Anh, 15 phút). Ba lượt đọc để quyết định có đọc tiếp hay không.
3. [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/), Andrej Karpathy — toàn bài: sáu bước từ làm quen dữ liệu đến vắt kiệt hiệu năng (Bài viết, tiếng Anh, 25 phút). Quy trình huấn luyện thực tế: kiểm tra dữ liệu, overfit một batch, rồi mới regularize.

### Đọc bài báo · Hợp Thể tầng 1

`hp_doc_bai_bao`

*Dùng phương pháp ba lượt của Keshav cho một bài ngắn mỗi tuần; đọc Ng để có nhịp đều đặn, bỏ qua lời khuyên nghề nghiệp.*

- **Chính:** [How to Read a Paper](https://www.cs.princeton.edu/courses/archive/fall18/cos561/papers/HowToRead05.pdf), S. Keshav — toàn bài 3 trang: phương pháp ba lượt (Bài báo, tiếng Anh, 15 phút). Ba lượt đọc để quyết định có đọc tiếp hay không.
- **Xem thêm:** [CS230 bài 8: Career Advice / Reading Research Papers](https://www.kdnuggets.com/2019/09/advice-building-machine-learning-career-research-papers-andrew-ng.html), Andrew Ng (Stanford, Autumn 2018) — tóm tắt bài giảng (video gốc nằm trên YouTube Stanford) (Video, tiếng Anh, 15 phút). Cách lập danh sách và đọc 2-3 bài mỗi tuần.
- **Xem thêm:** [Research Debt](https://distill.pub/2017/research-debt/), Chris Olah, Shan Carter (Distill 2017) — mục 'Interpretive Labor' và 'Research Distillation' (Bài viết, tiếng Anh, 25 phút). Nói vì sao viết giải thích rõ cũng là đóng góp nghiên cứu thật.

### Tái lập một công trình · Hợp Thể tầng 1

`hp_tai_lap`

*Bắt đầu bằng Annotated Transformer: đối chiếu bài báo với mã; chọn một kết quả nhỏ mà bài báo công bố rồi tự cài lại.*

- **Chính:** [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/), Harvard NLP — toàn bài: bài báo 'Attention Is All You Need' kèm mã PyTorch (Code, tiếng Anh, 2 giờ). Đối chiếu từng câu của bài báo với từng dòng mã, vừa là bài tái lập.
- **Xem thêm:** [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/), Andrej Karpathy — toàn bài: sáu bước từ làm quen dữ liệu đến vắt kiệt hiệu năng (Bài viết, tiếng Anh, 25 phút). Quy trình huấn luyện thực tế: kiểm tra dữ liệu, overfit một batch, rồi mới regularize.
- **Xem thêm:** [CS336 assignment 1: Basics](https://github.com/stanford-cs336/assignment1-basics), Stanford CS336 — toàn bộ (Bài tập, tiếng Anh, 20 giờ). Dạng tái lập có test tự chấm.

Thực chiến:

- Dữ liệu: [Tiny Shakespeare (shakespeare_char)](https://github.com/karpathy/nanoGPT) (giấy phép: MIT cho mã, 1.0 MB). Đủ nhỏ để tái lập số liệu trong README.
- Dữ liệu: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) (giấy phép: MIT, 35 MB). Có bảng kết quả công bố để so sánh.
- Bản mẫu: [nanoGPT (kho mã, đã ngừng cập nhật)](https://github.com/karpathy/nanoGPT), Andrej Karpathy — mục quickstart: data/shakespeare_char (Code, tiếng Anh, 30 phút). Bản tham chiếu train.py/model.py gọn; README nói đã cũ nhưng vẫn chạy được, MIT.
- Bản mẫu: [cifar10-airbench](https://github.com/KellerJordan/cifar10-airbench), Keller Jordan — README (Code, tiếng Anh, 60 phút). Mốc tái lập có con số rõ.
- Đích: Khớp số công bố: nanoGPT shakespeare_char val loss 1.4697 (A100, ~3 phút); airbench 94.01% CIFAR-10 trên A100. Khớp tới chữ số thập phân thứ hai là đạt, chênh vì hạt giống thì ghi lại.
- Chạy ở đâu: Cần GPU: Colab miễn phí (không bảo đảm GPU, phiên tối đa 12 giờ) hoặc Kaggle (~30 giờ GPU/tuần theo nguồn thứ cấp, chưa kiểm chứng); CPU chỉ chạy được bản thu nhỏ.

### Học tăng cường và tác tử · Hợp Thể tầng 2

`hp_hoc_tang_cuong`

*Spinning Up phần Introduction rồi tự cài một thuật toán policy gradient; RLVR hiện đại xem ở bài 16 của CS336.*

- **Chính:** [Spinning Up in Deep RL: Introduction to RL](https://spinningup.openai.com/en/latest/), OpenAI — ba phần của mục Introduction to RL, rồi Exercises (Bài viết, tiếng Anh, 3 giờ). Giới thiệu gọn nhất về RL sâu, có bài tập.
- **Xem thêm:** [Reinforcement Learning: An Introduction (2nd ed.)](http://incompleteideas.net/book/the-book-2nd.html), Sutton và Barto — chương 1-3, rồi 6 và 13 (Sách, tiếng Anh). Giáo trình gốc, bản PDF miễn phí trên trang tác giả.
- **Xem thêm:** [ARENA chương 2: Reinforcement Learning](https://arena.education/chapter2), ARENA — RL cơ bản và RLHF trên transformer (Khoá học, tiếng Anh, 10 giờ). Bài tập lập trình RL tới RLHF.
- **Xem thêm:** [Hugging Face Deep RL Course](https://huggingface.co/learn/deep-rl-course/unit0/introduction), Hugging Face — các đơn vị đầu (Khoá học, tiếng Anh, 7 giờ). Thực hành nhẹ, nhưng khoá ở trạng thái bảo trì thấp.

### An toàn, độ bền và diễn giải mô hình · Hợp Thể tầng 2

`hp_an_toan`

*Chọn một: BlueDot nếu muốn học theo nhóm, ARENA nếu muốn lập trình; NIST chỉ để biết ngôn ngữ quản trị rủi ro.*

- **Chính:** [Technical AI Safety (BlueDot Impact)](https://bluedot.org/courses/technical-ai-safety), BlueDot Impact — khoá 30 giờ: alignment, RLHF, interpretability, đánh giá, AI control (Khoá học, tiếng Anh, 30 giờ). Khoá có nhóm hướng dẫn, miễn phí theo trang.
- **Xem thêm:** [How To Become A Mechanistic Interpretability Researcher](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher), Neel Nanda — ba giai đoạn: Learning the Ropes, mini-projects, full projects (Bài viết, tiếng Anh, 66 phút). Kế hoạch học đến làm nghiên cứu, hữu ích cả ngoài diễn giải mô hình.
- **Xem thêm:** [ARENA chương 1 và 4: Transformer Interpretability, Alignment Science](https://arena.education/chapter1), ARENA — chương 1 và chương 4 (Khoá học, tiếng Anh, 15 giờ). Bài tập lập trình cho diễn giải và khoa học căn chỉnh.
- **Xem thêm:** [AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework), NIST — trang tổng quan và Playbook (Bài viết, tiếng Anh, 60 phút). Khung quản trị rủi ro phổ biến cho trách nhiệm.

### Viết và trình bày kỹ thuật · Hợp Thể tầng 3

`hp_viet`

*Xem video Peyton Jones, viết một trang tóm tắt ý chính, rồi soát bằng danh sách kiểm; bài Research Debt để thấy giá trị của giải thích rõ.*

- **Chính:** [How to write a great research paper](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/), Simon Peyton Jones — video ~34 phút và slide: bảy gợi ý (Video, tiếng Anh, 34 phút). Bảy lời khuyên cụ thể để bài viết có một ý chính rõ.
- **Xem thêm:** [Heuristics for Scientific Writing (a Machine Learning Perspective)](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/), Zachary C. Lipton — bài gốc trên blog Approximately Correct (2018) (Bài viết, tiếng Anh, 10 phút). Danh sách ngắn để soát bài viết; bản gốc của Lipton không tìm thấy.
- **Xem thêm:** [Research Debt](https://distill.pub/2017/research-debt/), Chris Olah, Shan Carter (Distill 2017) — mục 'Interpretive Labor' và 'Research Distillation' (Bài viết, tiếng Anh, 25 phút). Nói vì sao viết giải thích rõ cũng là đóng góp nghiên cứu thật.

### Thiên kiếp Hợp Thể: một đóng góp công khai · Hợp Thể tầng 3

`du_an_hop_the`

*Chọn một đóng góp nhỏ: bài giải thích kỹ thuật có mã chạy lại được, hoặc một PR chấp nhận được vào kho mở; xuất bản và xin người ngoài thử.*

- **Chính:** [Research Debt](https://distill.pub/2017/research-debt/), Chris Olah, Shan Carter (Distill 2017) — mục 'Interpretive Labor' và 'Research Distillation' (Bài viết, tiếng Anh, 25 phút). Nói vì sao viết giải thích rõ cũng là đóng góp nghiên cứu thật.
- **Xem thêm:** [How To Become A Mechanistic Interpretability Researcher](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher), Neel Nanda — ba giai đoạn: Learning the Ropes, mini-projects, full projects (Bài viết, tiếng Anh, 66 phút). Kế hoạch học đến làm nghiên cứu, hữu ích cả ngoài diễn giải mô hình.
- **Xem thêm:** [How to write a great research paper](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/), Simon Peyton Jones — video ~34 phút và slide: bảy gợi ý (Video, tiếng Anh, 34 phút). Bảy lời khuyên cụ thể để bài viết có một ý chính rõ.

Thực chiến:

- Dữ liệu: [Tiny Shakespeare / names.txt (tái dùng làm thí nghiệm nhỏ)](https://github.com/karpathy/makemore) (giấy phép: MIT cho mã; names.txt không ghi giấy phép riêng, 0.3 MB). Thí nghiệm nhỏ để viết bài có đối chứng.
- Bản mẫu: [makemore (kho mã)](https://github.com/karpathy/makemore), Andrej Karpathy — names.txt và makemore.py (Code, tiếng Anh, 20 phút). Bộ tên 32 nghìn dòng dùng chung cho cả chuỗi video; MIT.
- Bản mẫu: [nanoGPT (kho mã, đã ngừng cập nhật)](https://github.com/karpathy/nanoGPT), Andrej Karpathy — mục quickstart: data/shakespeare_char (Code, tiếng Anh, 30 phút). Bản tham chiếu train.py/model.py gọn; README nói đã cũ nhưng vẫn chạy được, MIT.
- Đích: Bài đăng công khai có mã chạy lại được; ít nhất một người ngoài chạy lại hoặc phản hồi. Không có con số chuẩn.
- Chạy ở đâu: CPU laptop cho thí nghiệm nhỏ; GPU miễn phí nếu cần.

### Chọn bài toán đáng làm · Đại Thừa tầng 1

`dt_gu_nghien_cuu`

*Đọc Hamming trước, rồi tự làm một bài tập trong Research Taste Exercises: chấm điểm ý tưởng của mình và so sánh với người hướng dẫn.*

- **Chính:** [You and Your Research](https://www.cs.virginia.edu/~robins/YouAndYourResearch.html), Richard Hamming — toàn bài (bản chép lời bài nói 1986) (Bài viết, tiếng Anh, 60 phút). Bài nói kinh điển về chọn vấn đề lớn và làm việc cửa mở.
- **Xem thêm:** [Research Taste Exercises](https://colah.github.io/notes/taste/), Chris Olah — toàn bài (1/2021): các bài tập luyện khẩu vị nghiên cứu (Bài viết, tiếng Anh, 20 phút). Biến 'khẩu vị' thành các bài tập cụ thể.
- **Xem thêm:** [Principles of Effective Research](https://www.bumc.bu.edu/preventive-med/files/2020/06/Principls-of-effective-reserache-nielsen-0404.pdf), Michael Nielsen — bản PDF của tiểu luận (2004); blog gốc của tác giả hiện không mở được (Bài viết, tiếng Anh, 40 phút). Nguyên tắc cá nhân cho người làm nghiên cứu dài hạn.
- **Xem thêm:** [An Opinionated Guide to ML Research](http://joschu.net/blog/opinionated-guide-ml-research.html), John Schulman — toàn bài (Bài viết, tiếng Anh, 30 phút). Hướng dẫn chọn hướng và nhịp làm việc của một nhà nghiên cứu; chưa tải được trang khi kiểm.

### Dẫn dắt một đội · Đại Thừa tầng 2

`dt_dan_dat_doi`

*Đọc hai bài StaffEng ngắn rồi xem bài 8 FSDL; chưa tìm được sách quản lý đã kiểm chứng nên bỏ.*

- **Chính:** [StaffEng: To lead, you have to follow](https://staffeng.com/guides/to-lead-follow/), Will Larson — toàn bài (Bài viết, tiếng Anh, 20 phút). Nói về dẫn dắt bằng cách lắng nghe và hợp tác.
- **Xem thêm:** [StaffEng: Create space for others](https://staffeng.com/guides/create-space-for-others/), Will Larson — toàn bài (Bài viết, tiếng Anh, 20 phút). Tạo chỗ cho người khác làm và học.
- **Xem thêm:** [Full Stack Deep Learning 2022, Bài 8: ML Teams and Project Management](https://fullstackdeeplearning.com/course/2022/lecture-8-teams-and-pm/), Full Stack Deep Learning — toàn bài giảng (Video, tiếng Anh, 75 phút). Cách tổ chức đội học máy và quản lý dự án.

### Chiến lược sản phẩm và trách nhiệm · Đại Thừa tầng 2

`dt_chien_luoc`

*Lấy NIST để có ngôn ngữ trách nhiệm, StaffEng cho viết chiến lược; chưa tìm được nguồn tốt riêng về chi phí-giá trị của sản phẩm AI.*

- **Chính:** [Responsible AI risk framing: AI RMF 1.0 và Playbook](https://www.nist.gov/itl/ai-risk-management-framework), NIST — trang tổng quan và Playbook (Bài viết, tiếng Anh, 60 phút). Khung nhìn hệ quả và trách nhiệm khi đưa AI ra thế giới.
- **Xem thêm:** [StaffEng: Writing engineering strategy](https://staffeng.com/guides/engineering-strategy/), Will Larson — toàn bài (Bài viết, tiếng Anh, 20 phút). Cách viết chiến lược kỹ thuật ngắn và dùng được.
- **Xem thêm:** [AGI Strategy (BlueDot)](https://bluedot.org/courses/agi-strategy), BlueDot Impact — khoá 25-40 giờ (Khoá học, tiếng Anh, 25 giờ). Góc nhìn chiến lược, giá chưa ghi rõ trên trang.
- **Xem thêm:** [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/), Hamel Husain — mục 6: lộ trình đếm thí nghiệm (Bài viết, tiếng Anh, 30 phút). Lộ trình sản phẩm tính bằng thí nghiệm thay vì tính năng.

### Phi thăng: công trình của riêng mình · Đại Thừa tầng 3

`du_an_dai_thua`

*Viết một đề xuất một trang: vấn đề, vì sao đáng làm, ai dùng, cách đo; rồi bắt đầu và công bố tiến độ mỗi tháng.*

- **Chính:** [Principles of Effective Research](https://www.bumc.bu.edu/preventive-med/files/2020/06/Principls-of-effective-reserache-nielsen-0404.pdf), Michael Nielsen — bản PDF của tiểu luận (2004); blog gốc của tác giả hiện không mở được (Bài viết, tiếng Anh, 40 phút). Nguyên tắc cá nhân cho người làm nghiên cứu dài hạn.
- **Xem thêm:** [StaffEng: Work on what matters](https://staffeng.com/guides/work-on-what-matters/), Will Larson — toàn bài (Bài viết, tiếng Anh, 20 phút). Cách chọn việc đáng làm trong tổ chức.
- **Xem thêm:** [You and Your Research](https://www.cs.virginia.edu/~robins/YouAndYourResearch.html), Richard Hamming — toàn bài (bản chép lời bài nói 1986) (Bài viết, tiếng Anh, 60 phút). Bài nói kinh điển về chọn vấn đề lớn và làm việc cửa mở.

Thực chiến:

- Dữ liệu: [Tuỳ dự án](https://github.com/karpathy/nanochat) (giấy phép: tuỳ dự án (nanochat: MIT)). Dự án tự khởi xướng nên dữ liệu do người chơi chọn; nanochat là mẫu đường ống trọn vẹn.
- Bản mẫu: [nanochat (kho mã)](https://github.com/karpathy/nanochat), Andrej Karpathy — README: speedrun.sh và tham số --depth (Code, tiếng Anh, 60 phút). Đường ống trọn vẹn từ tokenizer đến chat; bản mới thay nanoGPT, MIT.
- Đích: Một sản phẩm hoặc bài báo có người dùng/người theo thật; không có con số chuẩn.
- Chạy ở đâu: Tuỳ dự án; nanochat speedrun cần 8 GPU H100 khoảng 2 giờ (~48 USD theo README), phiên bản nhỏ chạy được trên GPU đơn chậm hơn 8 lần.

**Đã xem và không chọn:**

- Papers with Code: Chưa kiểm chứng được tình trạng năm 2026.
- Google re:Work (hướng dẫn quản lý): Trang quản lý bạn thử trả lỗi 404; chưa có URL đã kiểm.
- The Manager's Path, An Elegant Puzzle (sách): Sách trả phí và không có URL chính thức đã kiểm chứng trong lần này.
- ML Reproducibility Challenge: Chưa kiểm chứng được nguồn trong lần này.
- Lipton: Heuristics for Scientific Writing bản gốc: Không tìm được trang gốc, chỉ có bản tóm tắt của dair.ai.
- Vũ Hữu Tiệp: Machine Learning cơ bản: Còn trực tuyến nhưng bài mới nhất 2018, chỉ là ML cổ điển; không dùng cho nhánh này.
- Sutton & Barto qua incompleteideas.net: Lần kiểm tra trình duyệt báo lỗi chứng chỉ; giữ link, checked false.
