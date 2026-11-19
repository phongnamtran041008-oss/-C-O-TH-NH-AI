# Luận Đạo Đài — bài tự luận, chứng minh, và giám khảo AI tuỳ chọn

> Bản thiết kế, **chưa nối vào game** (`"wired": false`). Viết ngày 2026-11-19 trong phiên "tối ưu nguồn
> tài liệu". Không đụng tới `tree.json`, `world_plan.json`, ngân hàng câu hỏi hay mỹ thuật của hai phiên kia.

## 1. Vì sao cần một chỗ riêng

Đạo Thụ đã quyết: **chính đạo không hỏi chứng minh** (`rules.no_proof_items`). Nhưng đề thi kết thúc học
phần ở trường vẫn có phần tự luận: tính đạo hàm bằng định nghĩa, chứng minh một tập là không gian con,
chứng minh ước lượng không chệch, chứng minh bằng quy nạp... Các bài ấy:

- không chấm được bằng trắc nghiệm hay so đáp số, vì cái được chấm là **lập luận**;
- không nên chặn đường tu luyện của người chỉ muốn làm AI;
- nhưng người sắp thi thì rất cần luyện, và cần có người đọc bài.

Nên chúng ở một nơi riêng, **tuỳ chọn**: Luận Đạo Đài.

## 2. Luận Đạo Đài là gì trong game

| | |
|---|---|
| Ở đâu | Một đài đá ở Trúc Lâm Thôn, cạnh Tàng Thư Các. Vào được từ Luyện Khí tầng 1. |
| Mở đề nào | Mỗi đề gắn với một nút của Đạo Thụ; đề mở khi nút ấy đã xong (đã học khái niệm thì mới luận). |
| Có bắt buộc không | Không. Không nút nào, tầng nào, thiên kiếp nào cần tới nó. |
| Thưởng | **Đạo tâm** (điểm riêng của đài), danh hiệu, và một ít linh thạch. Không cho tu vi, để không ai thấy bị ép. |
| Ôn thi | Chế độ "Khảo thí": rút 3-4 đề của một bí cảnh, có đồng hồ, giống một đề thi cuối kỳ thu nhỏ. |

Người chơi viết bài làm ngay trong game (gõ chữ, công thức viết kiểu `x^2`, `lim_{x->0}`, `sqrt(...)`), hoặc
làm ra giấy rồi **tự chấm**. Sau khi nộp, luôn được xem lời giải mẫu và thang điểm.

## 3. Ba cách chấm

1. **Tự chấm (mặc định, không cần gì).** Game hiện lời giải mẫu và thang điểm từng ý; người chơi tự đánh
   dấu ý nào mình có. Đây là cách các lò luyện thi vẫn làm, và nó dạy đúng thứ cần dạy: biết một bài chứng
   minh được chấm ở đâu.
2. **Thiên Đạo Giám Khảo (tuỳ chọn, người chơi tự gắn khoá API).** Một mô hình ngôn ngữ đọc bài, chấm từng ý
   của thang điểm, chỉ ra dòng sai đầu tiên và gợi ý cách sửa. Xem mục 5.
3. **Đồng đạo thẩm định (làm sau).** Bạn bè trong thế giới chấm cho nhau theo cùng thang điểm. Cần thêm phần
   mạng nên để sau; dữ liệu đề đã đủ cho việc này.

Cả ba dùng **chung một thang điểm**, nên điểm tự chấm, điểm AI chấm và điểm bạn chấm so được với nhau. Khi
AI chấm xong, game vẫn cho người chơi sửa lại từng ý ("khiếu nại") — điểm cuối là của người chơi quyết, vì
đây là luyện tập cho chính mình.

## 4. Dữ liệu một đề

File: `server/data/math/essays/<bí cảnh>.json` (bốn bí cảnh toán). Lời giải mẫu và thang điểm **không rời
server** cho tới khi người chơi nộp bài, giống đáp án bài tập lập trình M6.

```json
{
  "subject": "giai_tich",
  "wired": false,
  "essays": [
    {
      "id": "gt_tl_dao_ham_dinh_nghia_1",
      "node": "gt_dao_ham",
      "kind": "tinh_co_lap_luan",
      "level": 1,
      "minutes": 10,
      "title_vi": "Đạo hàm bằng định nghĩa của x|x|",
      "statement_vi": "...",
      "why_vi": "vì sao người làm AI nên biết bài này",
      "hints_vi": ["..."],
      "solution_vi": ["từng dòng của lời giải mẫu"],
      "rubric": [
        {"id": "r1", "points": 2, "need_vi": "Viết đúng tỉ số sai phân tại điểm đang xét."},
        {"id": "r2", "points": 3, "need_vi": "..."}
      ],
      "fatal_vi": ["Dùng quy tắc đạo hàm thay cho định nghĩa trong khi đề yêu cầu định nghĩa."],
      "reviewed": false
    }
  ]
}
```

- `kind`: `chung_minh` (chứng minh một mệnh đề), `tinh_co_lap_luan` (tính nhưng phải trình bày lập luận),
  `phat_bieu_chung_minh` (phát biểu định lý rồi chứng minh), `phan_bien` (cho một "chứng minh" sai, tìm và
  sửa — nối tiếp dạng Tìm chỗ sai đã có trong game).
- `level` 1-3: 1 = một ý chính, 3 = đề cuối kỳ nhiều bước.
- `rubric`: tổng điểm luôn là 10. Mỗi ý là **một việc nhìn thấy được trong bài làm**, không phải "hiểu bài".
- `fatal_vi`: lỗi chí mạng. Mắc một lỗi thì điểm bài không quá 4, dù các ý khác có đủ.
- Quy tắc nội dung như mọi câu hỏi khác: đề và lời giải **tự viết**, không chép đề thi hay sách; mọi đề
  `reviewed: false` cho tới khi người duyệt.

Chọn dạng đề nào: theo danh sách `exam_proofs` trong `server/data/math/sources/{ds,gt,xs,tr}.json` — 68
dạng tự luận, mỗi dạng gắn với một nút (bảng đọc được ở `docs/NGUON_HOC.md`). **Lưu ý:** không tìm được đề
thi cuối kỳ thật nào của Bách khoa Hà Nội đăng công khai một cách chính thống, nên mức "hay gặp" trong danh
sách ấy là ước lượng từ đề cương học phần và từ đề thi mở của MIT, chưa đối chiếu với đề thật. Nếu bạn có đề
cũ của trường, chỉ cần cho biết dạng nào có mặt là xếp lại được ngay.

Bản mầm hiện có **20 đề** (mỗi bí cảnh 5), kiểm bằng `python tools/check_essays.py`:

| Bí cảnh | Đề |
|---|---|
| Giải Tích | đạo hàm bằng định nghĩa của x\|x\|; giới hạn epsilon - delta; tìm tham số để liên tục; e^x >= 1 + x bằng đạo hàm; tích phân cận vô hạn |
| Đại Số Tuyến Tính | không gian con và cơ sở; độc lập tuyến tính; nhân, ảnh và định lý số chiều; vectơ riêng của ma trận đối xứng trực giao; nghịch đảo của tích |
| Xác Suất và Thống Kê | Bayes ba dây chuyền; kỳ vọng và phương sai nhị thức; trung bình mẫu không chệch; hợp lý cực đại cho phân phối mũ; độc lập khác xung khắc |
| Thuật Toán và Tối Ưu | quy nạp công thức tổng; định lý bắt tay; cây n đỉnh có n - 1 cạnh; hàm lồi theo định nghĩa; khi nào hạ gradient hội tụ |

Mỗi đề có thêm `why_vi`: một câu nối bài chứng minh với việc làm AI (ví dụ bất đẳng thức e^x >= 1 + x là
lý do độ lệch KL không âm), để phần tự luận không tách rời mục tiêu của cả giáo trình.

## 5. Thiên Đạo Giám Khảo — chấm bằng khoá API của người chơi

### 5.1 Nguyên tắc

- **Tuỳ chọn hoàn toàn.** Không có khoá thì đài vẫn dùng được bằng tự chấm. Không dòng nào trong game nhắc
  người chơi "hãy mua khoá".
- **Khoá không bao giờ rời máy người chơi tới server của game.** Thế giới LAN là do bạn bè mở; khoá của ai
  người ấy giữ. Máy khách gọi thẳng nhà cung cấp mô hình.
- **Game không kèm khoá nào**, không trả tiền hộ, không gọi mô hình nào khi người chơi chưa bật.
- **Điểm AI chấm là tham khảo.** Nó không mở khoá gì và người chơi sửa được (mục 3).

### 5.2 Gắn khoá ở đâu

Màn Cài đặt có thêm mục "Thiên Đạo Giám Khảo" với bốn ô:

| Ô | Ý nghĩa |
|---|---|
| Nhà cung cấp | `claude` · `tuong_thich_openai` (OpenAI, Gemini, OpenRouter, Groq... và **máy nhà** qua Ollama/LM Studio) |
| Khoá | Dán khoá. Hiện dạng `sk-...abcd`. Để trống nếu chạy mô hình ngay trên máy. |
| Mô hình | Tên mô hình. Có gợi ý sẵn theo nhà cung cấp, người chơi đổi được. |
| Địa chỉ | Chỉ cho `tuong_thich_openai`: địa chỉ gốc của API (ví dụ `http://localhost:11434/v1` cho Ollama). |

Lưu ở `giam_khao.json` cạnh `config.json` (cùng thư mục dữ liệu của máy khách), **tách khỏi `config.json`**
để người chơi gửi `config.json` cho bạn mà không lộ khoá. Biến môi trường `TOAN_TU_TIEN_API_KEY` được ưu
tiên hơn file, cho ai không muốn ghi khoá ra đĩa. Nút "Thử khoá" gửi một câu hỏi rất ngắn để báo ngay: khoá
sai, hết hạn mức, hay sai tên mô hình.

Đường miễn phí cho người học, nêu rõ trong màn hướng dẫn: chạy mô hình ngay trên máy bằng Ollama (không cần
khoá, không mất tiền, nhưng chấm yếu hơn), hoặc bậc miễn phí của vài nhà cung cấp (hạn mức đổi thường xuyên
— game chỉ dẫn tới trang chính thức, không ghi con số).

### 5.3 Một lần chấm chạy thế nào

```
người chơi nộp bài ──► server (đã có bài làm) trả về: đề + lời giải mẫu + thang điểm + lỗi chí mạng
                          │
máy khách ghép lời nhắc ──┴─► gọi mô hình bằng khoá của người chơi (thẳng từ máy khách)
                               │
                 phán quyết JSON ◄┘   → máy khách **tự cộng điểm bằng code** → hiện kết quả
                               │
                 gửi server: điểm từng ý + ai chấm (tu_cham / ai / dong_dao) để ghi Đạo tâm
```

Lời nhắc cho mô hình gồm ba phần cố định (đề, lời giải mẫu, thang điểm — đặt trước để nhà cung cấp lưu đệm
được) và bài làm của người chơi ở cuối. Mô hình phải trả về đúng cấu trúc:

```json
{
  "items": [
    {"id": "r1", "met": "du | mot_phan | khong", "evidence": "trích nguyên văn dòng trong bài làm", "comment_vi": "..."}
  ],
  "fatal": [{"which": 0, "evidence": "...", "comment_vi": "..."}],
  "first_error_vi": "dòng sai đầu tiên và vì sao",
  "next_step_vi": "một việc nên làm tiếp để sửa bài"
}
```

- Với Claude: gọi qua SDK chính thức `anthropic` (phụ thuộc **tuỳ chọn**, chỉ nạp khi người chơi chọn nhà
  cung cấp này), dùng structured outputs (`output_config.format`) để phán quyết luôn đúng lược đồ; mô hình
  gợi ý sẵn là `claude-opus-5-5` vì chấm chứng minh là việc cần suy luận chắc, người chơi đổi sang mô hình
  rẻ hơn (`claude-haiku-5-5`) được. Bật `fallbacks` phía server của API và xử lý `stop_reason: "refusal"`.
- Với nhà cung cấp tương thích OpenAI: gọi `chat/completions` bằng `httpx` (máy khách đã có), yêu cầu JSON;
  nếu JSON hỏng thì thử lại một lần, vẫn hỏng thì báo "giám khảo trả lời không đọc được" và chuyển sang tự
  chấm — không bao giờ đoán điểm. Địa chỉ `http://` chỉ được dùng cho mô hình trên chính máy này: có khoá mà
  địa chỉ không phải `https://` thì game từ chối, để khoá không đi trên mạng ở dạng đọc được.
- Mỗi lần gọi mô hình (kể cả lần thử lại) tính vào trần mỗi ngày; lần gọi hỏng vì mạng hay sai khoá thì
  không tính.
- **Điểm do code tính, không do mô hình tính:** `du` = trọn điểm của ý, `mot_phan` = nửa điểm, `khong` = 0;
  có lỗi chí mạng thì trần là 4. Mô hình không được tự đưa ra tổng điểm.

### 5.4 Chấm bằng AI tin được tới đâu

Nghiên cứu gần đây cho thấy mô hình chấm chứng minh **chưa khớp với người chấm chuyên môn**, và sai theo
một hướng rõ: chấm rộng tay.

- QEDBench (arXiv 2602.20629): so 7 mô hình giám khảo với người chấm trên chứng minh bậc đại học năm cuối;
  phần tóm tắt nêu một "khoảng lệch có hệ thống", các giám khảo mạnh vẫn cho điểm trung bình cao hơn người
  từ +0,18 tới +0,36.
- Nghiên cứu ở một lớp chứng minh đại học (arXiv 2602.23635): mô hình và trợ giảng bất đồng đáng kể ở mức
  từng ý của thang điểm, nhưng **lời nhận xét** của mô hình hữu ích với bài có lỗi lớn.

Thiết kế ở trên đi theo đúng những gì các kết quả ấy gợi ý:

1. Chấm **từng ý**, mỗi ý phải kèm trích dẫn nguyên văn từ bài làm. Không trích được thì ý ấy là `khong`.
   Máy khách kiểm tra chuỗi trích có thật trong bài làm; trích bịa thì ý ấy bị bỏ.
2. Có **lời giải mẫu** trong lời nhắc, nên mô hình so bài với một lời giải đúng chứ không tự nghĩ lời giải.
3. Lời nhắc nói rõ: nghi ngờ thì chấm chặt; lập luận vòng quanh, dùng điều phải chứng minh, bỏ qua trường hợp
   là lỗi, không phải "cách trình bày khác".
4. Giá trị chính là **nhận xét và dòng sai đầu tiên**, không phải con số. Màn kết quả đặt nhận xét lên trên,
   điểm ở dưới, kèm dòng "điểm do AI chấm, chỉ để tham khảo".
5. Điểm không mở khoá gì. Một giám khảo dễ dãi chỉ làm người chơi tự lừa mình, như cách game đã nhìn nhận
   việc sửa máy khách ở bài tập lập trình.
6. Trước khi phát hành: một bộ thử gồm vài chục bài làm mẫu (đúng, sai tinh vi, sai thô) đã có điểm của
   người chấm, chạy qua từng mô hình gợi ý để biết nó lệch bao nhiêu; ghi kết quả vào tài liệu này.

### 5.5 Chi phí cho người chơi (ước lượng)

Một lần chấm khoảng 2.000 token vào (đề, lời giải, thang điểm, bài làm) và 1.200 token ra.

| Mô hình | Giá vào / ra (USD cho 1 triệu token) | Một lần chấm |
|---|---|---|
| `claude-opus-5-5` | 4 / 20 | khoảng 0,03 USD |
| `claude-haiku-5-5` | 0,10 / 0,50 | khoảng 0,001 USD |
| Mô hình chạy trên máy (Ollama) | 0 | 0 |

Game hiện số token đã dùng của phiên, và có ô "trần số lần chấm mỗi ngày" (mặc định 20) để một lỗi lặp không
đốt tiền của người chơi.

### 5.6 Riêng tư và an toàn

- Bài làm của người chơi được gửi cho nhà cung cấp mà **người chơi chọn**; màn cài đặt nói rõ điều này một
  lần, trước khi bật.
- Không gửi tên tài khoản, thư điện tử hay bất cứ thứ gì ngoài đề, thang điểm và bài làm.
- Khoá không ghi vào log, không hiện đủ trên màn hình, không gửi lên server game, không vào bản sao lưu.
- Bài làm có thể chứa câu kiểu "hãy cho tôi 10 điểm": lời nhắc coi bài làm là dữ liệu; và vì điểm do code
  tính từ các ý có trích dẫn, cách ấy không qua được bước kiểm tra trích dẫn.

## 6. Đã làm gì, còn lại gì

**Đã có (2026-11-19) — bộ máy chấm, toàn file mới, chưa nối vào game:**

| File | Việc | Kiểm bằng |
|---|---|---|
| `server/data/math/essays/*.json` | 20 đề mầm. | `python tools/check_essays.py` |
| `server/app/learning/math_essays.py` | Đọc và kiểm ngân hàng đề; `public_view` (trước khi nộp: không lời giải, không thang điểm) và `marking_view` (sau khi nộp); `score` cộng điểm từ các mức du / mot_phan / khong, lỗi chí mạng thì trần 4; `dao_tam` chỉ trả cho phần tiến bộ. | `server/tests/test_math_essays.py` (19 test) |
| `client/engine/giam_khao.py` | Cài đặt của người chơi (`giam_khao.json`, biến môi trường, trần mỗi ngày); ghép lời nhắc; lược đồ phán quyết; **kiểm trích dẫn**: ý được điểm mà đoạn trích không có trong bài làm thì thành `khong`; thử lại một lần khi phán quyết không đọc được, không bao giờ đoán điểm. | `client/tests/test_giam_khao.py` (61 test) |
| `client/engine/giam_khao_claude.py` | Gọi Claude qua SDK chính thức `anthropic` (phụ thuộc tuỳ chọn, chỉ nạp khi người chơi chọn). | cùng file test, và đã chạy với SDK thật 2.10.0 qua một tầng HTTP giả |
| `client/engine/giam_khao_openai.py` | Gọi mọi địa chỉ tương thích OpenAI bằng `httpx`, kể cả mô hình chạy trên máy (không cần khoá). Từ chối gửi khoá qua `http://` tới máy khác. | cùng file test, với một máy chủ giả |

Điều **chưa kiểm được**: chưa có lần gọi thật nào tới một mô hình (không có khoá, và không tiêu tiền của
bạn khi chưa hỏi). Hình dạng yêu cầu gửi đi đã được kiểm với SDK thật; chất lượng chấm của từng mô hình thì
chưa đo — đó là việc của bộ thử ở mục 5.4, điểm 6.

Mã lỗi mà màn hình sẽ cần một câu tiếng Việt cho mỗi cái: `off`, `no_key`, `no_model`, `no_url`,
`insecure_url`, `bad_provider`, `no_sdk`, `bad_key`, `no_permission`, `bad_model`, `rate_limit`,
`bad_request`, `server`, `network`, `timeout`, `refused`, `cut_off`, `unreadable`, `daily_cap`,
`empty_answer`, `answer_too_long`.

**Còn lại — đụng tới file dùng chung, làm sau khi phiên viết câu hỏi và phiên mỹ thuật đã ghi xong:**

| File | Việc |
|---|---|
| `client/scenes/math_essay.py` (mới) | Màn Luận Đạo Đài: đọc đề, viết bài, tự chấm, xem phán quyết. Gọi `giam_khao.grade` ở luồng phụ. |
| `client/scenes/settings.py`, `client/strings_vi.py` | Mục "Thiên Đạo Giám Khảo" và các câu tiếng Việt. |
| đường dẫn API + bảng dữ liệu + migration | Nộp bài, nhận `marking_view`, ghi điểm tốt nhất và Đạo tâm. |
| `tools/check_all.py` | Gọi thêm `math_essays.validate_all()`. |
| `CREDITS.md` | Ghi nguồn tài liệu, bộ dữ liệu và SDK tuỳ chọn. |

## 7. Những điều cần bạn quyết

1. Tên và chỗ đặt: "Luận Đạo Đài" ở Trúc Lâm Thôn — hay bạn muốn tên khác, chỗ khác?
2. Thưởng: chỉ Đạo tâm và danh hiệu (đề xuất), hay có cả tu vi?
3. Nhà cung cấp gợi ý sẵn trong màn cài đặt: Claude + tương thích OpenAI (gồm máy nhà) là đủ chưa?
4. Có cho nộp **ảnh chụp bài viết tay** không? Làm được với mô hình đọc ảnh, nhưng tốn hơn và dễ đọc nhầm
   chữ; đề xuất để sau.
5. Số đề mỗi bí cảnh cho bản đầu: đề xuất 20 (bản mầm hiện có ít hơn, xem các file dữ liệu).
