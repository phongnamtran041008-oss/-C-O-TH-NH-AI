# Bài giảng trực quan (Tàng Thư Các, format 2)

Hướng dẫn cho người viết bài giảng của Toán Tu Tiên. Mỗi tầng là một file
`server/data/math/library/<môn>/tN_<tên>.md`. Người chơi đọc **mỗi trang một kỹ năng con
(micro-skill)**, như một tấm thẻ: thấy hình trước, nhớ một câu bản chất, làm một ví dụ nhỏ,
tự kiểm. Không viết sách giáo khoa. Hai bài mẫu phải bắt chước:

- `dai_so_tuyen_tinh/t3_vecto_ma_tran.md` (bars, plane, grid, sets, matrix)
- `giai_tich/t4_dao_ham.md` (plane, grid, flow)

## 1. Khung file

```
---
id: gt_lib_t4                  # giữ nguyên id cũ
title_vi: Đạo hàm và vi phân
subject: giai_tich             # giữ nguyên
floor: 4                       # giữ nguyên
format: 2                      # bật luật thẻ (ngân sách bên dưới)
summary_vi: Một câu tóm tắt cả tầng (hiện trong danh sách).
skills: [gt_t4_dinh_nghia_dao_ham, gt_t4_quy_tac_tinh]   # giữ nguyên danh sách VÀ thứ tự
---
## Đạo hàm theo định nghĩa      # mục 1 = kỹ năng 1 của skills; mỗi ## là một trang
...
## Quy tắc tính đạo hàm         # mục 2 = kỹ năng 2
```

Câu hỏi trỏ vào trang theo kỹ năng, nên số `##` phải đúng bằng số kỹ năng, đúng thứ tự.

## 2. Các khối

| Viết | Hiện thành | Ghi chú |
|---|---|---|
| đoạn văn thường | chữ thân bài | dòng liền nhau gộp thành một đoạn; dòng trống ngắt đoạn |
| `- ý` | gạch đầu dòng | |
| `1. bước` | các bước có số | dùng cho ví dụ giải mẫu |
| `$$ TeX $$` | ảnh công thức | chỉ ASCII; phải build ảnh (mục 7) |
| `> Lỗi thường gặp: ...` | ô "Trúc Lão nhắc" | giọng Trúc Lão, một lỗi cụ thể |
| `### Tiêu đề nhỏ` | tiêu đề phụ | hạn chế dùng trong thẻ |
| `:::matrix` ... `:::` | ma trận vẽ sẵn | `A = 1 2 ; 3 -4`, mỗi dòng một ma trận, tối đa 3 |
| `:::hook` ... `:::` | dải xanh "Vì sao phải học?" | 1-2 câu, <= 220 ký tự, tình huống cụ thể (AI/ML, đời sống) |
| `:::core` ... `:::` | hộp vàng "Bản chất" | MỘT câu, <= 180 ký tự, điều còn nhớ sau một tháng |
| `:::check` `Q: ...` `A: ...` `:::` | hộp "Tự kiểm" | đáp án ẩn, người chơi bấm hoặc Enter mới hiện; mỗi dòng <= 200 ký tự |
| `:::figure <loại>` ... `:::` | hình do game tự vẽ | mục 5 |

Mọi khối `:::` phải đóng bằng một dòng `:::`. Quên đóng thì validator báo, và khối không
nuốt mất mục sau.

Chữ hiển thị: tiếng Việt, toán viết ASCII như cả game: `A^T`, `x^2`, `a_ij`, `<=`, `!=`,
`->`, `sqrt(x)`, `f'(x)`, `[1, 2; 3, 4]`. Không chữ Hán, không ký hiệu Unicode toán học
(game sẽ tự làm đẹp khi vẽ). Giọng tu tiên nhẹ: Trúc Lão, đệ tử, linh thạch; đừng lạm dụng.

## 3. Ngân sách mỗi trang (format: 2, validator kiểm)

- đúng **1** `:::core`
- ít nhất **1** `:::figure` hoặc `:::matrix`
- ít nhất **1** `:::check`
- chữ (đoạn văn + gạch đầu dòng) **<= 110 từ**; hook, core, bước, ghi chú, tự kiểm không tính
- **<= 2** công thức `$$`
- mỗi danh sách bước **<= 5** bước
- trang đầu tiên phải có `:::hook` (bài mẫu có hook ở MỌI trang: hãy làm vậy)

### Một kỹ năng có hai ý: tách trang bằng `###`

Trang lý tưởng dài không quá hai màn hình. Khi một kỹ năng (một mục `##`) chứa hai hoặc ba ý riêng, **đừng nén
thành câu cụt và đừng để trang dài ba bốn màn hình**: đặt một dòng `### Tên ý thứ hai` trước ý đó. Trong bài
`format: 2`, mỗi `###` mở một trang mới của cùng mục (tiêu đề hiện "Tên mục (2/2)"), nhiều nhất 3 trang một mục.

- Giới hạn 110 từ và 2 công thức tính **theo từng trang**; `core`, hình và `check` vẫn tính theo cả mục (một
  `core` cho cả kỹ năng, đặt ở trang đầu).
- Mỗi trang con nên tự đứng được: một hình hoặc một ví dụ, và nếu được thì một `:::check` riêng.
- Câu hỏi sai vẫn mở đúng trang đầu của kỹ năng; "Luyện ngay" nằm ở trang cuối của bài.

## 4. Trình tự sư phạm của một trang

1. `:::hook` Vì sao: một tình huống cụ thể, tốt nhất từ AI/ML hoặc đời sống.
2. `:::figure` Nhìn thấy nó.
3. `:::core` Bản chất trong một câu.
4. Một ví dụ số nhỏ: một câu đề (`Ví dụ: ...`) rồi `1. 2. 3.`.
5. `$$` Công thức SAU trực giác, chỉ khi đáng có.
6. `> Lỗi thường gặp: ...`
7. `:::check` Tự kiểm.

Checklist trước khi nộp:

- [ ] Nói nó LÀ gì và DÙNG để làm gì trước khi nói cách tính.
- [ ] Có hình hoặc ví dụ nhỏ thay cho định nghĩa dài.
- [ ] Câu ngắn, không câu đệm ("Như chúng ta đã biết...", "Rất quan trọng là...").
- [ ] Không chép sách. Không chép nguyên đề trong ngân hàng câu hỏi vào ví dụ/tự kiểm (đổi số).
- [ ] Mọi con số đã tính lại (dùng sympy nếu cần). Sai toán là không được phép.
- [ ] Chú thích hình là một câu nói hình đang cho thấy điều gì, không lặp lại tiêu đề.
- [ ] Đã xem ảnh chụp từng trang (mục 7) và không có gì chen chúc.

## 5. Hình (`:::figure`)

Mỗi dòng là một **thiết lập** `khóa: giá trị` hoặc một **lệnh** với các đối số:

- số: `2`, `-1.5`, `1/2`, `pi/2`, `sqrt(2)`
- màu: `do xanh luc vang tim xam muc`
- chữ hiển thị trong ngoặc kép: `"u + v"` (bắt buộc ngoặc kép, kể cả một chữ)
- từ khóa của lệnh: `dash`, `open`, ...
- tùy chọn `khóa=giá trị`: `pos=ne` (vị trí nhãn: `n s e w ne nw se sw c`), `len=22`
- dòng bắt đầu bằng `#` là ghi chú, bị bỏ qua

Chung cho mọi loại: `caption:` (bắt buộc, một câu), `size: rộng cao` (tùy chọn, đơn vị
gốc; màn hình là 480 x 270). Hình tối đa **400 x 130**. Hình rộng <= khoảng 240 được đặt
bên trái, chữ chảy bên phải; ví dụ có bước luôn xuống dưới hình, đủ bề ngang. Hai hình
liền nhau đứng cạnh nhau nếu vừa.

### 5.1 `plane` - mặt phẳng tọa độ

Dùng cho: vectơ 2 chiều, đồ thị hàm, tiếp tuyến, diện tích dưới đường cong, hình học.

```
:::figure plane
caption: Dây cung AB quay thành tiếp tuyến khi h -> 0.
size: 200 120
x: -0.5 3 1            # từ, đến, bước vạch (bước tùy chọn)
y: -1 6 1
curve "x^2" xanh "y = x^2" pos=w
segment 1 1 2 4 xam dash "dây cung"
tangent "x^2" 1 do "tiếp tuyến" pos=sw
point 1 1 muc "A" pos=se
point 2 4 muc "B" pos=e
:::
```

Lệnh: `point x y` (thêm `open` = chấm rỗng) · `vector x1 y1 x2 y2` hoặc `vector x y` (từ gốc)
· `segment x1 y1 x2 y2` · `line x1 y1 x2 y2` (đường thẳng kéo dài) · `curve "f(x)" [a b]`
· `param "x(t)" "y(t)" t0 t1` · `area "f(x)" a b` (tô dưới đường cong) · `tangent "f(x)" x0
[len=22]` (len: chỉ vẽ một đoạn ngắn) · `poly x1 y1 x2 y2 x3 y3 ...` (đa giác tô màu, nhãn ở
giữa) · `text x y "chữ"` · `drop x y` (đường gióng nét đứt xuống hai trục).
Thiết lập: `axes: off`, `grid: on`, `aspect: equal|free`, `names: t s` (tên trục).
Có `vector` hoặc `poly` thì mặc định `aspect: equal` (góc và độ dài đúng), còn lại `free`.

Biểu thức: số, `x` (`t` trong param, `n` trong seq), `+ - * / ^`, ngoặc, `pi`, `e`, `sin cos
tan exp ln log sqrt abs` (`log` là log10). Viết `2*x`, không viết `2x`. Ngoài miền xác định
thì đường cong tự đứt (1/x, tan x), ra khỏi khung thì bị cắt.

### 5.2 `bars` - biểu đồ cột

Dùng cho: phân phối rời rạc, đếm, một vectơ nhiều chiều (mỗi tọa độ một cột).

```
:::figure bars
caption: Số mặt ngửa khi tung 3 đồng xu; kỳ vọng là điểm cân bằng.
bar 0 1/8
bar 1 3/8
bar 2 3/8
bar 3 1/8
mark 1.5 do "E(X) = 1.5"
:::
```

`bar <nhãn> <giá trị> [màu]` (giá trị hiện đúng như viết: `3/8` vẫn là `3/8`; giá trị âm vẽ
xuống dưới). `mark <vị trí>`: vạch đứng, cột đầu là 0, cột cuối là n-1, 1.5 là giữa cột 1 và 2.
Thiết lập: `max:`, `min:`, `values: off`. Tối đa 12 cột.

### 5.3 `graph` - đồ thị, cây

Dùng cho: đồ thị, đường đi (tô màu cạnh), cây xác suất, cây đệ quy, cây tìm kiếm.

```
:::figure graph
caption: P(mưa và tắc) = 0.3 . 0.8: nhân dọc nhánh đỏ.
layout: ltr
node S "Bắt đầu"
node M "Mưa"
node N "Nắng"
node MT "Tắc"
node MK "Không"
edge S M "0.3" do
edge S N "0.7"
edge M MT "0.8" do
edge M MK "0.2"
:::
```

`node <tên> [x y] ["nhãn"] [màu]` · `edge <a> <b> [trọng số hoặc "nhãn"] [màu] [dash]`.
`layout: free` (dùng x y của mỗi đỉnh) · `circle` · `tree` (từ trên xuống, gốc là đỉnh đầu
tiên) · `ltr` (cây từ trái sang phải). `directed: yes` vẽ mũi tên. Tối đa 16 đỉnh.

### 5.4 `sets` - biểu đồ Venn

Dùng cho: tập hợp, biến cố, xác suất có điều kiện, quan hệ giữa các loại đối tượng.

```
:::figure sets
caption: Tam giác trên giao đối xứng đúng bằng ma trận chéo.
size: 220 100
universe: "Omega"          # tùy chọn: khung không gian mẫu
set T "tam giác trên" xanh
set D "đối xứng" do
shade T&D vang
in T-D "U"
in D-T "S"
in T&D "chéo"
:::
```

2 hoặc 3 `set`. Vùng viết bằng tên tập với `&` (giao), `|` (hợp), `-` (hiệu), `~` (phần bù),
ngoặc: `A&B`, `A-B`, `(A|B)-C`, `~(A|B)`. `shade <vùng> [màu]` tô vùng, `in <vùng> "chữ"`
đặt chữ vào chỗ rộng nhất của vùng. Chữ trong vùng nên ngắn (1-6 ký tự).

### 5.5 `map` - ánh xạ

Dùng cho: ánh xạ, đơn ánh/toàn ánh/song ánh, hàm hợp (3 cột), hàm ngược.

```
:::figure map
caption: 2 và 3 cùng tới b: f không đơn ánh.
col "X" 1 2 3
col "Y" a b c
gap 1 "f"
1 -> a
2 -> b do
3 -> b do
:::
```

`col "tên" phần tử...` (2 hoặc 3 cột, mỗi cột <= 7 phần tử, có thể thêm màu ở cuối),
`a -> b [màu]` (mũi tên giữa hai cột kề nhau), `gap 1 "f"` (tên ánh xạ giữa cột 1 và 2).

### 5.6 `grid` - bảng, ma trận

Dùng cho: hàng nhân cột, chuyển vị, vết, bảng chân trị, bảng quy hoạch động, bảng tra.

```
:::figure grid
caption: Hàng 1 của A nhân cột 2 của B ra ô (1, 2) của AB.
style: matrix              # matrix: ngoặc vuông; table (mặc định): kẻ ô
table "A"
row 1 2 3
row 4 5 6
mark row 1 do
op "x"
table "B"
row 1 0
row 0 1
row 2 -1
mark col 2 xanh
op "="
table "AB"
row 7 -1
row 16 -1
mark cell 1 2 vang
:::
```

`table ["tên"]` mở bảng mới (tối đa 4) · `row ô ô ...` · `head ...` (tiêu đề cột) · `side
...` (tiêu đề hàng) · `mark row i`, `mark col j`, `mark cell i j`, `mark diag` (đánh số từ 1)
· `op "+"` chữ giữa hai bảng. Ô có dấu cách thì đặt trong ngoặc kép. Tối đa 8 x 8 mỗi bảng.

### 5.7 `numberline` - trục số

Dùng cho: khoảng, bất phương trình, lân cận epsilon, giới hạn dãy, khoảng tin cậy.

```
:::figure numberline
caption: Mọi số hạng 1/n từ n = 3 trở đi nằm trong lân cận bán kính 0.4 của 0.
range: -1 2 0.5
nbhd 0 0.4 luc "epsilon = 0.4"
seq "1/n" 1 8 xanh "1/n"
interval 1 inf [ tim
point 1.5 do "a" open
:::
```

`point x [open]` · `interval a b [ ( ] )` (ngoặc vuông = đóng, tròn = mở; `-inf`/`inf` cho
đầu vô hạn) · `nbhd tâm bán_kính` · `seq "biểu thức của n" n0 n1`.

### 5.8 `flow` - sơ đồ luồng

Dùng cho: hàm hợp, chuỗi biến đổi, pipeline dữ liệu, các bước thuật toán.

```
:::figure flow
caption: Tốc độ dọc chuỗi nhân với nhau.
box "x"
link "u' = 3"
box "u = 3x" xanh
link "dy/du = cos u"
box "y = sin u" luc
:::
```

`box "chữ" [màu]`, `link "chữ"` (nhãn mũi tên tới hộp kế tiếp). Quá rộng thì tự xuống
hàng. 2 đến 9 hộp.

## 6. Lỗi thường gặp khi viết

- Đoạn văn dài thay cho hình. Nếu cần hơn 110 từ, nội dung đó nên là hình hoặc ví dụ.
- Core là hai câu, hay là định nghĩa chép lại. Core là điều trực giác: "nó là gì".
- Công thức đứng trước hình. Công thức luôn sau trực giác.
- Ví dụ quá to (số lớn, nhiều bước). Số nhỏ, <= 5 bước, mỗi bước một ý.
- Nhãn trong hình dài hoặc chồng nhau: rút ngắn, dùng `pos=`, mở rộng `x:`/`y:` hoặc `size:`.
- Viết `2x` trong biểu thức của hình (phải là `2*x`), quên ngoặc kép quanh nhãn.
- Tự kiểm trùng nguyên câu trong ngân hàng câu hỏi: đổi số.
- Tên trong hình khác tên trong chữ (hình gọi A, ví dụ cũng gọi A cho một ma trận khác).

## 7. Lệnh

Chạy từ thư mục gốc repo, với Python của dự án (`"/e/TU TIÊN AI/.venv/Scripts/python.exe"`).

Kiểm tra toàn bộ (cú pháp, ngân sách, hình, công thức, phông chữ):

```
python tools/check_all.py
```

Ảnh công thức (sau khi thêm hoặc sửa `$$`). Lần đầu chép node_modules, không `npm install`:

```
cp -r "/e/TU TIÊN AI/.claude/worktrees/floor10-content-1dab1f/tools/formulas/node_modules" tools/formulas/
python tools/build_formulas.py
```

Commit ảnh mới trong `client/assets/formulas/` và `server/data/math/formulas.json`; không
commit `node_modules`. Công thức cũ không còn dùng thì `check_all` báo; chỉ xóa đúng những
ảnh của bài mình đã viết lại (`--prune` xóa mọi ảnh không còn dùng, cẩn thận khi người khác
đang viết song song).

Chụp và kiểm từng trang (scale 3, kiểm cả scale 2, đáp án ẩn và hiện):

```
python tools/shot_library.py out/ gt_lib_t4               # một bài, ảnh trong out/
python tools/shot_library.py out/ path/to/nhap.md        # bản nháp, kể cả khi chưa hợp lệ
python tools/shot_library.py --check                     # mọi bài, không lưu ảnh
```

Trang dài hơn khung được lưu thành nhiều ảnh `_p2_2.png`, ... Công cụ báo lỗi khi có gì ra
ngoài khung, chồng lên nhau, dòng rộng hơn cột, hay nhãn ra ngoài hình. Luôn MỞ ẢNH RA XEM:
công cụ không biết một hình có rõ nghĩa hay không.
