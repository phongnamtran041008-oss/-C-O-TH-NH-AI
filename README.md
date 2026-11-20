# Toán tu tiên

Game tu tiên 2D pixel, chơi online nhiều người, để **học toán cho AI**: đại số tuyến tính, giải tích, xác suất và
thống kê, tối ưu và toán rời rạc. Giao diện tiếng Việt. Muốn mạnh lên thì phải trả lời đúng: đả tọa, đột phá
cảnh giới, phá khiên quái, thi triển chiêu thức, câu cá, giữ thành, vượt bí cảnh cùng bạn bè đều hỏi câu toán ở
đúng chỗ con đang học trên **Đạo Thụ** (cây giáo trình).

Client pygame-ce, máy chủ FastAPI + WebSocket + SQLAlchemy. Chơi một mình trên máy, mở thế giới cho bạn bè cùng
mạng LAN, hoặc chạy một máy chủ riêng.

> Game này lớn lên từ một game học tiếng Trung cũ ("Khu Vườn Tu Tiên"). Mọi thứ của trò học chữ ấy (vườn, câu hỏi
> từ vựng, Pháp Chữ, khắc văn, dữ liệu từ vựng và bảng của nó) đã bị xoá hẳn ngày 2026-11-20 (`docs/DECISIONS.md`,
> mục cuối).

## Có gì trong game

**Học toán**
- **Đạo Thụ**: cây giáo trình bốn nhánh đi song song; mỗi nút là một nhóm vi kỹ năng, mở khi các nút cần trước đã
  xong. Luật nối cây vào game: [`docs/DAO_THU_TRONG_GAME.md`](docs/DAO_THU_TRONG_GAME.md); nội dung cây:
  [`docs/GIAO_TRINH_CAY.md`](docs/GIAO_TRINH_CAY.md).
- **Buổi luyện** (phím M ở Động Phủ): sáu loại câu — Đúng/Sai, Trắc nghiệm, Điền số, Ghép cặp, Sắp xếp bước giải,
  Tìm chỗ sai. Bậc khó thích ứng theo từng vi kỹ năng, câu ôn xoắn ốc từ phần đã qua, **cổng thuần thục** rồi
  **Thiên kiếp nhỏ** để vượt một phần. **Kiểm tra đầu vào** tuỳ chọn cho người đã biết trước.
- **Tàng Thư Các** (Thủ Thư ở Trúc Lâm Thôn, phím L): kinh thư toán của mọi tầng, công thức dựng sẵn thành ảnh,
  lời nhắc chỗ hay sai. Đóng kinh thư là thấy **kệ phổ**: Yêu Quái Phổ, Ong Phổ, Ngư Phổ, Bảo Vật Phổ, Linh Thú Phổ
  với quà ở mốc 25/50/75/100% (Linh Thạch, Tiên Ngọc, danh hiệu, khung avatar, ô tổ ong), và kệ **đan phương**
  của Thủ Thư (phải đứng cạnh bà mới mua được). Phím B mở riêng kệ phổ.
- **Bài tập lập trình**: đề trong game, bài làm chạy trên máy người chơi, máy chủ chấm bằng test ẩn
  (AC / WA / TLE / RE / CE).
- **Luận Đạo Đài** (bài tự luận, chứng minh): đã gác lại (bỏ chấm bằng API, 2026-11-20); đề còn làm dữ liệu — [`docs/LUAN_DAO_DAI.md`](docs/LUAN_DAO_DAI.md).

**Tu luyện và chiến đấu**
- **Tu Vi và cảnh giới** (Phàm Nhân → Luyện Khí → Trúc Cơ → ... → Đại Thừa). Đả tọa trên bồ đoàn: cứ một lúc
  một câu. Cuối mỗi cảnh giới cần đan đột phá và vượt **Thiên Kiếp** (chuỗi câu toán ở tầng của chính con).
- **Quái = lỗi sai** (Loạn Số Cốc, cổng bắc Trúc Lâm Thôn): mỗi con quái là một lỗi thường gặp, Mặc Thuẫn của nó
  chỉ vỡ khi con trả lời đúng một câu của đúng vi kỹ năng ấy. Hạ quái rơi nguyên liệu và **ghi chú lỗi sai**
  (mở đúng mục trong Tàng Thư Các). **Lò Toán** rèn đồ từ nguyên liệu + ghi chú đã hiểu.
- **Chiêu thức gắn câu hỏi** (phím 1–6): mỗi chiêu thi triển bằng một câu đúng loại của nó; đúng liên tiếp tăng
  sát thương, sai là chiêu hụt (mất linh khí, không mất máu).
- Trang bị 6 ô, 5 độ hiếm, cường hóa ở Lò Rèn; đan dược luyện ở **Đan Lô** (động phủ) hoặc lò của **Đan Sư**.

**Thế giới và bạn bè**
- **Trúc Lâm Thôn** (làng chính), Rừng Mực Loang, Hồ Nghiên Mực, Loạn Số Cốc, Động Phủ của riêng mỗi người.
  Thấy người chơi khác đi lại, kênh, chat (Thế giới / Khu vực / Bạn bè / Tổ Đội), bạn bè, tặng quà, chặn, báo cáo.
- **Linh Phong Sào** (tổ ong): ấp trứng, cho ăn, ong làm Linh Mật, ong hộ vệ bay theo người chơi. **Câu cá**
  (30 loài, cần, mồi, mưa, kỷ lục); cá hiếm cắn câu thì hỏi câu toán. **Linh Thú** (12 con giáp) đi theo chủ.
- **Thiên Cơ Các**: gacha Trứng Ong và Linh Thú, tỉ lệ và bảo hiểm công khai. **Sạp Tạp Hóa** của Bà Chủ Sạp,
  nhiệm vụ cốt truyện và nhiệm vụ hằng ngày.

**Bốn chế độ (M10)** — mọi câu theo tầng và bậc của chính người chơi, đều tính vào lộ trình học:
- **Bí cảnh toán** (Cổng Bí Cảnh; một mình hoặc tổ đội 2–5): gian Trận Nhãn rồi trùm; mỗi người nhận câu của mình.
  Còn **Mặc Ảnh Động** (giờ mở cửa) và **Khe Nứt Mực** (khe nứt ngẫu nhiên) cho tổ đội.
- **Hầm ngục**: sinh theo hạt giống, mỗi phòng một loại câu.
- **Cơ duyên**: sau đủ câu đúng có thể gặp Lão nhân ra đề hoặc Rương đề.
- **Thủ thành toán** (Cổng Thủ Thành ở Trúc Lâm Thôn hoặc cửa trong Động Phủ): mỗi tháp là một mảng toán; đặt và
  nâng tháp phải trả lời đúng. Trận chạy trên client, máy chủ chạy lại nhật ký (`td_sim.py`) để chống gian lận.

## Chạy game

Cần **Python 3.11 trở lên**.

**Nhanh nhất (Windows):** nháy đúp `chay_game.bat` → **Bắt đầu** → đăng ký bằng email (Firebase) → tab *Thế giới
của tôi* → **Tạo** → **Mở thế giới**. Game tự chạy máy chủ của thế giới đó trên máy (ẩn) và mở cho mạng LAN; bạn bè
cùng Wi-Fi vào tab *Tham gia mạng LAN*. Thế giới nằm ở `client/worlds/<tên>/world.db` (bản exe: `worlds/` cạnh exe).
macOS/Linux: `./chay_game.sh`.

**Máy chủ riêng** (tài khoản tên đăng nhập + mật khẩu): tạo `client/config.json` với
`{"firebase_api_key": "", "server_url": "http://127.0.0.1:8000"}`, rồi chạy `chay_server.bat` (hoặc
`chay_server_choi_chung.bat` để mở cho mạng LAN) và `chay_game.bat`. Từ dòng lệnh:

```bash
# máy chủ
cd server
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --port 8000          # http://localhost:8000/docs để thử API

# game (thư mục gốc dự án)
python -m pip install -r client/requirements.txt
python -m client.main
```

Thử nhanh: trong `server/.env` đặt `BALANCE_PROFILE=dev` (Tu Vi mỗi tầng rất ít, cá cắn nhanh, bí cảnh mở suốt)
và/hoặc `TIME_SCALE=1440` (1 ngày trong game = 1 phút). Xoá dòng đó là về số liệu thật.

Dữ liệu của máy chủ riêng nằm trong `server/dev.db` (và `server/.env`); bản cập nhật không chứa hai file này và
máy chủ tự nâng cấp cơ sở dữ liệu khi khởi động.

**Chơi qua Internet:** Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8000`) hoặc một máy chủ thật —
Docker + PostgreSQL + Caddy, Render + Neon, Oracle Always Free: [`docs/DEPLOY.md`](docs/DEPLOY.md).
**Quản trị:** `ADMIN_USERNAMES=ten_cua_ban` trong `server/.env`, rồi gõ `/admin help` trong khung chat.

**Đóng gói exe** (Windows): `dong_goi_exe.bat` → `dist/ToanTuTien/ToanTuTien.exe` và file zip để phát hành; đẩy tag
`vX.Y.Z` thì GitHub Actions tự build và đính vào Release. Game tự báo khi có bản mới (`update_repo` trong
`config.json`). Ra bản mới: sửa `GAME_VERSION` trong `client/config.py` **và** `server/app/config.py` (đổi giao thức
thì tăng cả `PROTOCOL_VERSION`).

### Điều khiển

| Phím | Việc |
|---|---|
| WASD / mũi tên | Đi lại |
| E | Tương tác (NPC, cổng, bồ đoàn, lò, bảng nhiệm vụ, Thủ Thư...) ; gần quái: đánh |
| Chuột trái / Space | Đánh quái |
| 1–6 | Chiêu thức gắn câu hỏi |
| F | Câu cá khi đứng sát mép nước; giữ chuột (hoặc Space) để kéo cá |
| M | Buổi luyện toán (ở Động Phủ) |
| L | Tàng Thư Các (kinh thư toán, rồi kệ phổ) |
| B | Kệ phổ (Yêu Quái, Ong, Ngư, Bảo Vật, Linh Thú) |
| K | Tu luyện (cảnh giới, chỉ số, trang bị, đột phá) |
| J | Nhiệm vụ (cốt truyện / hằng ngày) |
| O | Linh Thú |
| H / G | Linh Phong Sào / Thiên Cơ Các (ở Động Phủ) |
| G (ngoài vùng đất) | Chạm: Đạp Kiếm Lướt qua vực; giữ: ngự kiếm bay (mũi tên lái, G lần nữa để hạ) |
| T / R | Bày pháp trận / Cưỡi linh thú |
| Tab | Túi đồ |
| Y | Tổ đội |
| P | Bạn bè |
| Enter | Chat (`/w Tên` nhắn riêng, `/t` Thế giới, `/k` Khu vực, `/d` Tổ Đội) |
| Esc | Đóng / Cài đặt |

## Kiểm tra

```bash
cd server && python -m pytest -q          # test máy chủ (gồm WebSocket thật với nhiều client)
cd .. && python -m pytest client/tests -q # test client: các test *_flow chạy máy chủ thật và bấm qua giao diện
python tools/check_all.py                 # kiểm tra nội dung toán: Đạo Thụ, ngân hàng câu, bộ sinh câu, đáp án,
                                          # Tàng Thư, công thức, bài tập, quái lỗi sai, Lò Toán, chiêu thức, bốn chế độ
python tools/economy_sim.py               # không có vòng lặp tạo tiền + dòng Linh Thạch 30 ngày của 3 kiểu người chơi
```

Bộ test đầy đủ chạy lâu (cỡ 45 phút); khi sửa một phần thì chạy file test của phần ấy. Nhiều test client nhận
một thư mục để lưu ảnh chụp màn hình, ví dụ `python -m client.tests.test_math_flow anh/`.

## Công cụ

```bash
python tools/math_review.py         # bảng duyệt câu hỏi -> tools/reports/math_review_<môn>.md
python tools/math_verify.py         # tính lại đáp án của mọi câu sinh ra bằng SymPy (và math_verify_*.py theo môn/tầng)
python tools/build_formulas.py      # dựng ảnh công thức cho Tàng Thư Các (cần Node: cd tools/formulas && npm install)
python tools/build_problem_tests.py # sinh đáp án test ẩn của bài tập lập trình từ lời giải mẫu
python tools/check_tree.py          # kiểm tra Đạo Thụ (server/data/math/tree.json)
python tools/check_sources.py       # kiểm tra nguồn tài liệu học (docs/NGUON_HOC.md)
python tools/build_fish.py          # dựng server/data/creatures/fish.json từ tools/curation/fish.json
python tools/gen_maps.py            # dựng lại bản đồ (.tmj, mở được bằng Tiled)
python tools/realm_bots.py --math   # bot cùng vượt bí cảnh toán qua WebSocket
python tools/math_dungeon_bot.py    # bot chơi thử hầm ngục (math_fortune_bot.py, math_td_bot.py tương tự)
python tools/load_bots.py --bots 50 --minutes 10   # thử tải thế giới chung (docs/LOAD_TEST.md)
python tools/build_exe.py           # đóng gói exe rồi tự chạy thử
```

Mỹ thuật: nhân vật và chiêu thức dựng từ Blender (`tools/blender/`, [`docs/ART_PIPELINE.md`](docs/ART_PIPELINE.md)),
phần còn lại vẽ bằng code (`client/art/`).

## Nội dung toán

- Câu hỏi: `server/data/math/items/` và bộ sinh câu `server/app/learning/math_gen/`. Mọi câu do AI viết nên **cần
  người duyệt** (cờ `reviewed`).
- Bài đọc Tàng Thư Các: `server/data/math/library/` (Markdown rút gọn: `##` một mục cho mỗi vi kỹ năng, `$$...$$`
  công thức, `:::matrix` ma trận, `>` lời nhắc). Mỗi công thức được dựng sẵn thành ảnh PNG đi kèm game.
- Đạo Thụ: `server/data/math/tree.json`; nguồn học: [`docs/NGUON_HOC.md`](docs/NGUON_HOC.md); quái lỗi sai:
  `server/data/math/monsters.json`, `drops.json`; Lò Toán: `crafting.json`; chiêu thức: `skills.json`; bốn chế độ:
  `server/data/realms.json`, `math/dungeon.json`, `math/fortune.json`, `math/td.json`.
- Bài tập lập trình: `server/data/math/problems/` (lời giải mẫu nằm cạnh đề, không bao giờ gửi cho game). Bài làm
  được lưu thành file `.py` thật trong `bai_lam/` cạnh `session.json`.
- Mọi con số cân bằng game ở `server/data/balance/*.json`; kinh tế: [`docs/BALANCE.md`](docs/BALANCE.md).

## Cấu trúc

```
server/            FastAPI + SQLAlchemy + Alembic (docs/API.md)
  app/learning/    math_* (lộ trình, Đạo Thụ, câu hỏi, bộ sinh câu, Tàng Thư, bài tập), quiz (phiên câu hỏi chung)
  app/systems/     math_ask (mọi chế độ lấy câu ở đây), math_practice, math_combat, math_skills, math_realm,
                   math_dungeon, math_fortune, math_td (+ td, td_sim), math_craft, math_code, cultivation,
                   inventory, items, books (kệ phổ, danh hiệu, đan phương), codex, bees, fishing, pets, alchemy,
                   gacha, shop, quests, social, secret_realm
  app/realtime/    WebSocket /ws: thế giới 20 Hz, vùng, kênh, chiến đấu, tổ đội, bí cảnh (docs/PROTOCOL.md)
  data/            math/ (nội dung toán), balance/, creatures/, items/, maps
client/            pygame-ce
  scenes/          world, abode (Động Phủ), math_* (luyện, Đạo Thụ, Tàng Thư, hầm ngục, cơ duyên, thủ thành,
                   bài tập, kiểm tra đầu vào), books, rpg, hive, fishing, pets, alchemy, gacha, shop, realm, social...
  engine/          hiển thị pixel, chữ, tilemap, âm thanh; td_sim / fishing_sim / alchemy_fire (bản sao y hệt server)
  art/, assets/    vẽ bằng code, sprite và model dựng sẵn, phông chữ, ảnh công thức
tools/             kiểm tra nội dung, bot, đóng gói, bản đồ, mỹ thuật
docs/              API, PROTOCOL, DECISIONS (nhật ký quyết định), SPEC (đặc tả gốc, có ghi chú phần đã bỏ), DEPLOY...
deploy/            docker-compose (máy chủ + PostgreSQL + Caddy + sao lưu), render.yaml ở thư mục gốc
```

## Giấy phép

Font theo SIL OFL 1.1. Nguồn tài nguyên và giấy phép: `CREDITS.md`.
