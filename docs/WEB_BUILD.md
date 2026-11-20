# Bản web của Toán Tu Tiên (M12, pygbag)

Bản web là **đúng game trên máy tính** (cùng mã `client/`), được pygbag đóng gói để chạy trong trình duyệt,
nối vào **máy chủ game bình thường**. Mục tiêu: mở game trên điện thoại cùng Wi-Fi với máy tính.

**Kết quả ngày 2026-11-20:** chạy được trong trình duyệt (Chrome 156 nhúng trong ứng dụng Claude, trên máy
Windows): đăng ký, đăng nhập, tạo nhân vật, vào động phủ, xuống Trúc Lâm Thôn, sang Rừng Mực Loang (thế giới
chung qua WebSocket), đánh quái, nhận một câu Vấn Đạo từ máy chủ, trả lời đúng, được cộng Tu Vi. Ảnh chụp ở
`art/preview/web_*.png`. **Chưa thử trên một chiếc điện thoại thật** (xem mục "Phải tự kiểm trên điện thoại").

## Cần có

- Python của game (thư mục `.venv` hoặc Python cài sẵn) với thư viện của máy chủ (`server/requirements.txt`).
- **Internet** hai lần: lúc build lần đầu (tải pygbag và khuôn trang), và **mỗi máy mở game** cần tải bộ chạy
  Python cho trình duyệt từ `pygame-web.github.io` (khoảng 22 MB, trình duyệt giữ lại cho lần sau). Không có
  Internet thì trang đứng ở "Loading".
- pygbag **0.9.3**, tự cài vào môi trường riêng `.venv-web/` (không đụng tới `.venv` của game). pygbag tự nó
  chạy được bằng Python 3.14 của máy; trong trình duyệt game chạy trên CPython **3.12** bản WebAssembly.

## Build (một lệnh)

```
python tools/build_web.py
```

Lệnh này: tạo `.venv-web/` và cài pygbag nếu chưa có; chép `client/` (bỏ `tests/`, `__pycache__`, tệp của
người chơi) cùng `web/main.py` vào `build/web_src/toantutien/`; ghi một `config.json` riêng cho web (không
địa chỉ máy chủ, không thế giới LAN); gọi pygbag; kết quả ở **`build/web/`** (`index.html`,
`toantutien.tar.gz` khoảng 9,5 MB, `toantutien.apk` là bản cho itch.io, không dùng tới). Mất chừng nửa phút.

## Mở cho cả Wi-Fi (một lệnh)

```
python tools/build_web.py serve
```

(hoặc bấm đúp **`chay_web.bat`**: cài thư viện máy chủ, build, rồi mở.) Lệnh này build rồi chạy **máy chủ
game** ở cổng 8000 cho mọi máy trong mạng, và chính máy chủ phát bản web ở **`/web/`**. Cửa sổ in ra địa chỉ:

```
   Trên máy này:         http://127.0.0.1:8000/web/
   Điện thoại cùng Wi-Fi: http://192.168.1.8:8000/web/
```

Đã build rồi thì `python tools/build_web.py serve --no-build`. Máy chủ chạy bằng `chay_server_choi_chung.bat`
cũng tự phát `/web/` nếu `build/web/` đã có (biến `WEB_BUILD_DIR` đổi được thư mục).

### Mở trên điện thoại

1. Máy tính và điện thoại **cùng một Wi-Fi**. Lần đầu Windows hỏi tường lửa cho Python: bấm **Allow / Cho
   phép** (mạng riêng). Đã lỡ chặn: Windows Security → Tường lửa → Cho phép ứng dụng → bật Python.
2. Trên điện thoại mở Chrome (hoặc Safari) và gõ địa chỉ "Điện thoại cùng Wi-Fi" ở trên, **có `/web/` ở cuối**.
3. Chờ tải (lần đầu khoảng 30 MB), **chạm vào màn hình một lần** để bắt đầu (trình duyệt chỉ cho phát âm thanh
   sau một lần chạm). Xoay ngang điện thoại.
4. Đăng nhập: chạm vào ô, rồi chạm nút **⌨** góc phải để bàn phím hiện lên (xem mục cảm ứng).

### Vì sao trang và máy chủ phải cùng một địa chỉ

Lúc thử, trang mở ở `http://192.168.1.8:8080` (một cổng riêng) **không gọi được** máy chủ ở
`http://192.168.1.8:8000`: Chrome đời mới chặn trang không có HTTPS gọi sang địa chỉ trong mạng nhà (quy tắc
"Local Network Access", quyền `local-network-access` = `denied`), dù máy chủ đã bật CORS. Mở ở
`http://127.0.0.1:8080` trên chính máy tính thì được. Vì vậy cách chính là `/web/` trên chính máy chủ game:
cùng một địa chỉ thì trình duyệt không có gì để chặn, và điện thoại chỉ cần một cổng.

### Chỉ mở trang, máy chủ ở chỗ khác

```
python tools/build_web.py static --port 8080
```

Trang tự gọi cổng 8000 của máy đã phát trang; muốn chỗ khác thì thêm vào địa chỉ:
`http://127.0.0.1:8080/?server=http://dia-chi-may-chu:8000`. Máy chủ phải cho phép CORS: mặc định
`CORS_ORIGINS=*` (đăng nhập đi bằng header Bearer, không có cookie, nên `*` không cho trang nào thêm quyền gì);
muốn hẹp lại thì đặt `CORS_ORIGINS=http://a:8080,http://b:8080` trong `server/.env`. Như mục trên, từ điện
thoại cách này dễ bị Chrome chặn; dùng `serve`.

Các tham số khác trên địa chỉ trang: `?pad=1` luôn hiện nút cảm ứng, `?pad=0` luôn ẩn.

## Đã chạy được (thử thật trong trình duyệt)

| Phần | Kết quả |
|---|---|
| Tải trang, chạm để bắt đầu, màn hình tiêu đề | được, khung 960x540, trang tự co theo màn hình |
| Đăng ký (mã khôi phục), đăng nhập, tạo nhân vật | được, qua `fetch` của trình duyệt |
| Lưu đăng nhập | được: tải lại trang, bấm "Bắt đầu" là vào thẳng chỗ đã đứng (lưu trong `localStorage`) |
| Động phủ, Lộ Trình, hướng dẫn của Trúc Lão | được |
| Thế giới chung (thôn, rừng), thông báo máy chủ, quái | được, qua `WebSocket` của trình duyệt |
| Câu Vấn Đạo trong trận, trả lời, cộng Tu Vi | được ("Chính xác! Tu Vi +3") |
| Mở bằng địa chỉ Wi-Fi `http://192.168.1.8:<cổng>/web/` | được tới đăng nhập, thôn và rừng |
| Console của trình duyệt | không lỗi Python; chỉ có hai dòng của chính pygbag ("BrowserFS not found", hộp hỏi khi rời trang) |

Tốc độ: phần việc của game mất **17 ms mỗi khung** ở màn hình tiêu đề và **23 ms** trong rừng có mưa và quái
(trên máy tính này; xem `window.kvtt_fps` và `window.kvtt_frame_ms` trong console). Điện thoại tầm trung chậm
hơn máy tính vài lần, nên đoán chừng **10-20 khung/giây**: chơi được nhưng không mượt. Chưa đo trên điện thoại.

## Khác bản máy tính / không có trên web

- **Thế giới LAN (Firebase, mở thế giới trên máy mình, quét mạng):** không có. Trang không mở được máy chủ,
  không gửi được gói UDP. Bản web luôn dùng tài khoản tên + mật khẩu của máy chủ thường.
- **Bài tập lập trình:** chạy **ngay trong trang** (trình duyệt không chạy được chương trình khác): đầu vào đưa
  qua `input()` / `sys.stdin`, `print` được bắt lại, giới hạn thời gian giữ bằng cách dò từng dòng lệnh. Vì dò
  làm Python chậm đi, mỗi bài được **gấp 3 lần** thời gian; thời gian báo lên là thời gian thật. Trong lúc chạy
  trang đứng yên (tối đa 3 x giới hạn mỗi test). Một lệnh dựng sẵn chạy rất lâu (ví dụ `sum(range(10**10))`)
  không ngắt được giữa chừng. Bài làm lưu trong trang, **mất khi tải lại**. Phần này đã có test trên máy tính,
  **chưa bấm thử trong trình duyệt**.
- **Giám khảo AI (Luận Đạo Đài):** cần thư viện `anthropic` / `httpx`, không có trên web. Chọn nhà cung cấp
  kiểu OpenAI trên web hiện sẽ báo lỗi nhập thư viện thay vì một câu tiếng Việt (tệp của phiên khác, đã ghi
  trong báo cáo M12).
- **Kiểm tra bản mới trên GitHub:** tắt (trang luôn là bản build mới nhất).
- **Nút "Thoát":** trang không tự đóng được, chỉ quay về màn hình tiêu đề.
- **Sao chép mã khôi phục**, **mở liên kết ngoài:** có thể không làm được trong trình duyệt; game báo
  "Không sao chép được, hãy chép tay nhé" thay vì dừng.
- **Âm thanh:** game tự tổng hợp tiếng (không có tệp âm thanh); chưa nghe thử trên web.
- **Dung lượng:** 9,5 MB game (ảnh v2 7,8 MB, phông 2 MB, công thức 1,9 MB; ảnh PNG không nén thêm được) + khoảng
  22 MB bộ chạy của pygbag. Qua Wi-Fi tải một lần là được, nên chưa cắt bớt.

## Cảm ứng: chơi bằng tay trên điện thoại được tới đâu

Game vốn chơi bằng bàn phím và chuột. Trên điện thoại:

- **Chạm = bấm chuột** (SDL tự đổi): nút, ô, thẻ câu hỏi, ghép cặp đều chạm được.
- Ô chữ trong game (canvas) **không tự bật bàn phím điện thoại**. Vì vậy trên màn hình cảm ứng (hoặc với
  `?pad=1`) trang hiện thêm một lớp nút HTML gửi đúng phím như bàn phím thật: **mũi tên** (giữ để đi), **Đánh**
  (Space), **E** (tương tác), **↵** (Enter), **Esc**, **1 2 3** (chiêu), và **⌨**: chạm vào thì bàn phím
  điện thoại hiện lên, chữ gõ được chuyển vào ô đang chọn trong game (cả chữ có dấu, Backspace, Enter).
- Lớp nút này **chưa thử trên điện thoại thật và chưa bấm thử trong trình duyệt** (phiên thử bị dừng trước
  bước đó); cú pháp JavaScript đã kiểm bằng `node --check`.
- Thật lòng: đi lại bằng mũi tên trên kính và đánh quái bằng nút là chơi được nhưng vụng; phần **học toán**
  (bấm chọn đáp án, ghép cặp, Tàng Thư Các, Lộ Trình) hợp với điện thoại hơn phần đánh nhau. Câu phải gõ
  công thức dài thì gõ trên điện thoại khó. Phím tắt khác (B, J, K, L, M, F1, Tab...) chưa có nút; phần lớn
  đã có nút bấm được trên thanh dưới của game.

## Phải tự kiểm trên điện thoại

1. `chay_web.bat` trên máy tính, điện thoại mở `http://<địa chỉ>:8000/web/`: trang tải xong và chạm để bắt đầu.
2. Chạm "Bắt đầu" → ô Tên đăng nhập → nút ⌨: bàn phím hiện lên, gõ được, Backspace xoá được.
3. Đăng nhập, tạo nhân vật, ra cổng động phủ bằng mũi tên, bấm E.
4. Ở rừng: đánh quái bằng nút Đánh, trả lời một câu bằng cách chạm.
5. Xoay ngang/dọc: khung game co lại đúng, các nút không che mất nút trả lời.
6. Tải lại trang: vào lại không cần đăng nhập.
7. Ghi lại `window.kvtt_fps` (Chrome trên máy tính: `chrome://inspect` khi cắm cáp) để biết điện thoại chạy
   mấy khung/giây.

## Cấu trúc mã

- `client/net/transport.py`: chỗ duy nhất hỏi "đang ở trình duyệt không?" và chọn đường mạng.
- `client/net/web.py`: `WebApi` / `WebWsClient` (cùng giao diện `Api` / `WsClient` của máy tính) chạy trên
  `fetch` / `WebSocket` qua một đoạn JavaScript nhỏ; `localStorage`; lớp nút cảm ứng. Chữ gửi từ Python sang
  JavaScript luôn là ASCII (`\u` escape), vì cầu nối của pygbag làm hỏng dấu tiếng Việt theo chiều đó (chiều
  ngược lại thì không).
- `client/main.py`: `Game.run_async()` (mỗi khung nhường trình duyệt một lần) và `web_main()`.
- `client/config.py`: trên web, cấu hình và phiên đăng nhập lưu cả vào `localStorage`.
- `client/engine/coderun.py`: `run_in_process()` cho bài tập lập trình trên web.
- `web/main.py`: điểm vào của pygbag. `tools/build_web.py`: build / serve / static.
- `server/app/main.py`, `server/app/config.py`: CORS (`CORS_ORIGINS`) và phát `build/web/` ở `/web/`.
- Test: `client/tests/test_web_build.py` (đường mạng qua cầu JavaScript giả, chạy bài trong trang, lưu cấu
  hình, build), `server/tests/test_web_build.py` (CORS, `/web/`).
