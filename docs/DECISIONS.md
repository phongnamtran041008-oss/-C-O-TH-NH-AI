# Quyết định thiết kế

Ghi lại những chỗ đặc tả để mở và phương án đã chọn. Mỗi mục: quyết định — lý do.

## Chung

- **Tên game là "Khu Vườn Tu Tiên"** (theo yêu cầu của người dùng, thay cho "Vườn Chữ: Tu Tiên Lộ" trong đặc tả). Phụ đề tiếng Trung 字园仙途 giữ từ đặc tả; đây là tên sáng tác, không dùng làm câu hỏi từ vựng.
- **Thời gian lưu dưới dạng UTC không kèm múi giờ** trong DB (SQLite không lưu múi giờ). Mốc reset hằng ngày tính theo UTC+7 (`app/clock.py`). Mọi thời gian lấy từ `clock.now()` để test có thể "tua" thời gian.
- **Từ vựng được đồng bộ vào bảng `words`** lúc server khởi động (nguồn sự thật vẫn là các file JSON) để các bảng khác có khóa ngoại tới từ.

## Dữ liệu từ vựng (mục 5)

- **CC-CEDICT lấy từ bản export gốc của MDBG đóng gói trong gói PyPI `pycccedict` khi không tải được mdbg.net.** Máy dựng dữ liệu lần đầu bị chặn truy cập mdbg.net; file trong gói là bản export nguyên vẹn (ngày 2023-11-07, đúng header và số mục của MDBG). Script luôn thử mdbg.net trước; chạy lại `build_wordlist.py --refresh` trên máy có mạng thường sẽ lấy bản mới nhất. Nguồn và mã băm ghi trong `tools/raw/SOURCES.md`.
- **Danh sách từ được chọn tay trong `tools/curation/words.json`, kèm âm đọc muốn dùng; còn pinyin, nghĩa tiếng Anh, lượng từ và cấu tạo chữ thì script lấy từ nguồn.** Lý do: danh sách HSK của repo gộp mọi âm đọc của CC-CEDICT (ví dụ 听 có cả *yǐn* "mỉm cười (cổ)"), nên cần người chỉ định âm nào được dạy; script kiểm tra âm đó có trong cả danh sách HSK lẫn CC-CEDICT, lệch là ghi vào `pinyin_conflicts.csv` và bỏ từ đó ra.
- **Tier 1 có 83 từ học + 6 chữ ẩn (好 吗 明 林 森 休) + 3 thành ngữ.** 苹果 (HSK 3) và 个 được thêm vào 80 từ gốc vì câu mẫu của đặc tả (我喜欢吃苹果) và hầu hết câu có số đếm cần chúng. 好 và 吗 là chữ HSK 1 nhưng thành chữ ẩn vì đặc tả cho chúng mở khóa qua phản ứng kề ô.
- **Chữ bắt buộc không có trong danh sách HSK (木) không có tần suất HSK**, nên được xếp như từ phổ biến nhất (Common), tránh việc chữ cơ bản cho phản ứng 林/森 lại thành Epic.
- **Câu ví dụ chỉ dùng từ có trong dữ liệu game** (không chỉ "trong phạm vi HSK 1–2"), để pinyin của câu được ghép từ pinyin đã kiểm chứng của từng từ và để câu nào cũng ghép được bằng quả chữ.
- **Chữ ghép bằng bộ thủ biến thể** (休 = 亻 + 木) được coi là khớp công thức 人 + 木 qua bảng biến thể bộ thủ trong `build_wordlist.py`. Cả 6 công thức ghép chữ hiện tại đều khớp cấu tạo thật trong makemeahanzi.
- **makemeahanzi `dictionary.txt` có giấy phép LGPL-3.0+** (đã kiểm tra file COPYING): game chỉ dùng các trường bộ thủ/cấu tạo, ghi công trong `CREDITS.md`.

## Gacha (mục 6.1, 13)

- **Pity ép "ít nhất" độ hiếm đó**: lần thứ 40 không có Epic+ sẽ ra Epic hoặc Legendary theo tỉ lệ tương đối 7:1; lần thứ 90 ra Legendary. Ra Legendary cũng reset bộ đếm Epic.
- **Đảm bảo của gói 10 lần** chỉ can thiệp ở lượt thứ 10 nếu 9 lượt trước toàn Common.
- **Tỉ lệ hiển thị gồm cả tỉ lệ gốc và tỉ lệ thực tế khi tính pity** (Legendary gốc 1%, thực tế ≈1,68%), cho minh bạch.
- **Giới hạn 15 hạt/ngày tính theo số lượt quay** (kể cả hạt trùng và lượt miễn phí). Gói 10 lần bị từ chối nếu không còn đủ 10 lượt, thay vì chỉ quay một phần.
- **Quay ra từ mới thì từ vào `collection` ngay (chưa "được giới thiệu")**; chỉ khi xem thẻ giới thiệu và bấm "Đã nhớ" thì từ mới tính là đã học và mới được dùng làm câu hỏi ở nơi khác.
- **Hạt trùng bán được 20 Linh Thạch, hoặc gieo lại** để trồng lại một chữ đã thu hoạch (lấy thêm quả cho Ghép Câu, ôn lại từ). Một chữ có thể mọc ở nhiều ô cùng lúc (cần cho 林 = 木 + 木 và 森 = 3 × 木); mỗi ô có lịch ôn riêng. (Giai đoạn 2 đổi từ "chỉ để bán": nếu không, sau khi thu hoạch hết vườn không còn gì để trồng, và không thể ghép 林/森.)
- **Chữ ẩn và thành ngữ không bao giờ làm đáp án nhiễu**, để không lộ trước phát hiện.
- **Quầy Trứng Ong và Linh Thú đã cấu hình** trong `balance/gacha.json` nhưng `enabled: false` cho tới giai đoạn 5 và 8.
- Người chơi mới nhận sẵn hạt 水 (hướng dẫn của Trúc Lão) và 1 lượt quay miễn phí mỗi ngày.

## SRS và sương mực (mục 6.2, 6.3)

- **`TIME_SCALE` chia mọi thời gian chờ SRS và tốc độ sương mực**, không chia thời hạn trả lời câu hỏi. Server từ chối `TIME_SCALE ≠ 1` ngoài môi trường dev.
- **Sương mực tính lười nhưng "phát lại" chính xác**: nếu người chơi vắng mặt lâu, mỗi lần cây lùi giai đoạn được tính tại đúng thời điểm nó xảy ra, nên tải vườn trễ cho cùng kết quả như theo dõi liên tục (có test).
- **Khi wither chạm 100**: cây lùi 1 giai đoạn (không thấp hơn Nảy mầm), wither đặt lại 60, cây đến hạn ôn ngay. Trả lời sai cũng có thể đẩy wither tới 100.
- **Cây Chín không bị sương mực** (không còn lịch ôn).
- **Một ô chỉ có một câu hỏi vườn đang mở**: hỏi lại trả về đúng câu cũ, không cho "đổi câu" đến khi gặp câu dễ.
- **Giai đoạn 4 hỏi Q5 (gõ pinyin) trước, Q7 nếu không tạo được**; nếu một chữ không tạo được dạng câu của giai đoạn (vd 吗 không có biến thể thanh cho Q3), dùng Q1/Q2 thay thế.

## Câu hỏi (mục 8.2)

- **Câu nghe (Q4) lấy âm qua `/quiz/{session}/audio`**, không gửi tên file theo mã từ, vì mã từ chính là đáp án. Không có file âm thì câu hiện pinyin thay (đúng đặc tả).
- **Đáp án nhiễu Q3 không bao giờ là một âm đọc khác có thật của chữ** (vd 只 có cả zhī và zhǐ), lấy từ toàn bộ âm đọc CC-CEDICT. Thanh nhẹ chỉ dùng làm đáp án nhiễu khi hết lựa chọn khác.
- **Q4 không có hai đáp án đồng âm** (他/它 đều là tā).
- **Q6 không bao giờ dùng 个 làm đáp án nhiễu** (lượng từ chung dùng được với rất nhiều danh từ), chỉ hỏi những danh từ có lượng từ riêng trong CC-CEDICT. Nếu từ được hỏi là một lượng từ (只, 条…), câu hỏi dùng một danh từ trong dữ liệu đi với nó.
- **Q7, Q9 có kèm nghĩa tiếng Việt của câu** để chỉ một đáp án hợp lý.
- **Q8 chỉ hỏi chữ hội ý / hình thanh** (theo trường `etymology` của makemeahanzi). Chữ tượng hình như 木, 日 có "cấu tạo" chỉ là nét vẽ (木 = 十 + 八) nên không hỏi.
- **Q11 bỏ qua chữ đa âm có thanh khác nhau** (vd 只), vì cả hai thanh đều đúng.
- **Câu chưa duyệt (`reviewed: false`) chỉ dùng khi `ALLOW_UNREVIEWED` bật** (mặc định bật ở dev, tắt ở production). Hiện mọi câu đều chưa duyệt, nên ở production Q7/Q9/Q10 sẽ không xuất hiện tới khi duyệt.
- **Hết giờ = sai**; giới hạn giờ trên server cộng 1,5 giây bù độ trễ. Câu vườn có hạn 10 phút.
- Mức cảnh giới tối thiểu của từng dạng câu đặt trong `balance/quiz.json` (`min_tier`).

## Tài khoản và chống gian lận (mục 15.4, 17)

- **Mã khôi phục 12 ký tự** chia nhóm `XXXX-XXXX-XXXX`, bỏ ký tự dễ nhầm (I, O, 0, 1); dùng xong thì cấp mã mới và đăng xuất mọi thiết bị.
- **Tên đăng nhập không phân biệt hoa thường** khi kiểm tra trùng và khi đăng nhập.
- **Giới hạn tần suất giữ trong RAM** của một tiến trình server (đúng với kiến trúc một tiến trình của đặc tả); nhiều tiến trình thì cần đổi sang lưu chung.
- **Cộng/trừ tiền dùng một câu `UPDATE … WHERE số dư + delta >= 0`** nên hai yêu cầu chi tiền chạy song song không thể làm số dư âm (có test).

## Giai đoạn 2 — client và vườn đầy đủ

- **Phông chữ giao diện là VT323** (SIL OFL, đủ dấu tiếng Việt). Fusion/Ark Pixel Font không tải được từ máy dựng (GitHub Releases bị chặn) và các font pixel khác trên Google Fonts thiếu dấu tiếng Việt. Ký tự VT323 không có (chữ Hán, một số dấu pinyin, mũi tên) tự chuyển sang **Noto Sans SC** trong cùng một dòng (`client/engine/text.py`).
- **Noto Sans SC được cắt gọn (subset)** còn ~1,9 MB: toàn bộ GB2312 (6.763 chữ thông dụng) + mọi ký tự trong dữ liệu game + chữ Latin/tiếng Việt/pinyin. `tools/fetch_assets.py --full` giữ bản đầy đủ 8 MB.
- **Hình vẽ**: nhân vật, Trúc Lão, ngựa, hạt giống, biểu tượng là lưới ký tự trong `client/art/sprites/`; ô đất, cây trồng, đạo cụ được vẽ bằng code (`client/art/build.py`) để đủ 6 giai đoạn × 4 độ hiếm × mức sương mực mà không cần hàng trăm lưới. Không dùng asset ngoài.
- **Chữ Hán của cây hiện trên một thẻ giấy cắm cạnh gốc** thay vì trên thân: ở độ phân giải 480×270, chữ 10 px trên nền giấy dễ đọc hơn chữ đè lên lá. Rê chuột vào ô sẽ hiện chữ to, pinyin, giai đoạn, thời gian ôn.
- **Vườn rộng tối đa 5×5**, mở đầu 3×3 như bản 1. Ô mới phải nằm cạnh ô đã có; giá khai hoang tăng dần (150, 200, 250…). Người chơi đi lại được trên các luống đất (giống game nông trại), bấm E hoặc bấm chuột vào ô.
- **Phản ứng kề ô**: 水 nhân thời gian chờ ôn ×0,8 (cộng dồn nếu kề nhiều cây), "lớn nhanh hơn 10%" của 火 cài là ×0,9. Lửa làm cháy gỗ được tung xúc xắc mỗi ngày (theo giờ UTC+7) với hạt giống cố định theo ô và ngày, nên tải lại vườn không bao giờ "tung lại" một ngày.
- **Giâm cành**: mua thêm một hạt của chữ đã học (60 Linh Thạch). Cần thiết vì 林 (木 + 木) và 森 (3 × 木) đòi nhiều cây cùng một chữ, và hạt trùng từ gacha chỉ đến khi đã có hết từ cùng độ hiếm.
- **Ghép câu không lộ đáp án**: người chơi chỉ thấy nghĩa tiếng Việt và số ô; chỉ những câu đã đủ quả mới hiện ra. Sai thứ tự thì không mất quả, Trúc Lão chỉ ra ô sai đầu tiên.
- **Sự cố thanh điệu được kiểm tra ở mọi ngữ cảnh** (không chỉ vườn), và câu Q3 ưu tiên cho xuất hiện đáp án nhiễu gây sự cố để chúng thật sự xảy ra. Trừ Linh Thạch tối đa 10 và không bao giờ âm.
- **Tên nhân vật**: 2–16 ký tự chữ/số (mọi bảng chữ, gồm tiếng Việt và chữ Hán), không trùng (không phân biệt hoa thường), qua bộ lọc từ tục. Bộ lọc phân biệt có dấu/không dấu để "Lớn" không bị nhầm với từ tục.
- **Hướng dẫn tân thủ do server lưu bước** (`users.flags.tutorial`), chỉ tiến không lùi, nên thoát giữa chừng vào lại không phải xem lại từ đầu.
- **Vị trí nhân vật trong động phủ** được lưu mỗi 60 giây và khi thoát game (REST). Thế giới chung ở giai đoạn 3 sẽ đi qua WebSocket.
- **Câu hỏi trong vườn không có đồng hồ đếm ngược** (chỉ hết hạn sau 10 phút như đặc tả); câu ở nơi khác hiện thanh thời gian.
- **Âm thanh hiệu ứng được tổng hợp bằng code** (sóng sin/vuông/nhiễu), không dùng file âm thanh có bản quyền. Phát âm từ vựng chỉ có khi chạy `tools/generate_audio.py` (cần mạng tới dịch vụ edge-tts, máy dựng không truy cập được).
- **Server làm tròn lên thời gian còn lại** (`seconds_until_due`), để client không bao giờ báo "đến giờ ôn" sớm hơn server.

## Giai đoạn 3 — thế giới online

- **Một tiến trình, trạng thái thế giới trong RAM** (`server/app/realtime/`): `World` giữ các phiên kết nối, mỗi
  vùng có danh sách kênh (`ChannelZone`), vòng tick 20 Hz chạy trong cùng event loop với FastAPI. Không dùng
  Redis (đúng mục 2). Muốn chạy nhiều tiến trình thì phải đổi kiến trúc, ghi rõ ở đây để không ai bật `--workers`.
- **Di chuyển theo kiểu "gửi phím, phát lại"**: client gửi các bước `(dx, dy, ms)` của từng khung hình; server áp
  dụng bằng cùng một hàm (`movement.py` có hai bản giống hệt nhau ở server và client, có test so sánh từng dòng
  code và 3.000 bước ngẫu nhiên). Nhờ vậy dự đoán ở client luôn khớp, chỉ bị kéo lại khi gian lận hoặc mạng quá
  tệ. Đây vẫn là "client chỉ gửi ý định" (mục 15.1), và đồng thời đúng mục 17 "server kiểm tra tốc độ và va chạm".
- **Chống hack tốc độ bằng ngân sách thời gian**: mỗi người tích thời gian thật đã trôi (tối đa 600 ms để chịu
  được mạng giật), gói di chuyển chỉ chạy khi đủ ngân sách; một gói tối đa 250 ms; hàng đợi quá 1,5 giây thì bỏ.
  Chạy nhanh gấp đôi là không thể; tích được tối đa ~0,6 giây đi "bù".
- **Gói đi qua cổng**: client gửi `join` ngay khi dự đoán mình đã đứng trong cổng; nếu server chưa chạy hết các
  bước cuối, nó chờ (tối đa 1 giây) thay vì từ chối. Vùng cổng trên bản đồ kéo dài ra ngoài mép bản đồ vài pixel để
  người chơi không thể "đi quá" cổng.
- **Snapshot**: 10 lần/giây, chỉ phần thay đổi so với lần trước gửi cho chính người đó; vùng quan tâm 3 × 3 ô lưới
  16 tile. Thực thể không đổi thì client tự thêm mẫu "đứng yên" để nội suy không bị kéo dài. Vị trí của chính mình
  gửi chính xác (không làm tròn) vì client phát lại từ đó.
- **Quái ở giai đoạn 3 chỉ đi lang thang** trong vùng của mình (`monster_area` trên bản đồ), có tên và hình riêng
  (Mực Con, Thanh Điệu Yêu), kênh không có người thì quái "ngủ". Bấm vào quái chỉ hiện lời nhắn: chiến đấu Vấn Đạo
  thuộc giai đoạn 4. `creatures/monsters.json` đã khai báo dạng câu hỏi của từng loài (mục 8.2).
- **Động phủ vẫn là cảnh riêng của từng người, chạy qua REST** như giai đoạn 2 (không có trong WebSocket). Thăm động
  phủ của bạn là **xem**: người thăm đi lại trong bản sao động phủ của bạn và tưới giúp, nhưng chủ nhà không thấy
  người thăm đi lại theo thời gian thực (chỉ nhận thông báo "đã tưới giúp"). Thăm từ trong làng thì nhân vật ở làng
  đứng yên tại chỗ cho đến khi quay lại.
- **Tưới giúp** chỉ hỏi chữ mà **người thăm đã học** (nguyên tắc "câu hỏi luôn công bằng"); hỏi Q1/Q2/Q3. Mỗi lượt
  mở câu hỏi đều tính vào giới hạn 5 lượt/ngày (kể cả trả lời sai), để không thể bỏ câu khó rồi chờ câu dễ. Đúng
  thì cả hai +10 Linh Thạch qua `inventory` (có `audit_log`); cây của chủ vườn **không** lớn thêm, vì giai đoạn cây
  chỉ đổi khi chính chủ ôn (mục 8.3). Xem vườn không bao giờ ghi gì vào vườn của chủ (sương mực tính trên bản sao).
- **Bạn bè lưu hai dòng** khi đã đồng ý (A→B, B→A); lời mời là một dòng `pending`. Hai người cùng mời nhau thì
  thành bạn luôn. Chặn ai thì hủy kết bạn, chặn lời mời, và lọc tin nhắn của người đó ở mọi kênh (kể cả lịch sử).
- **Chat bạn bè gửi theo đạo hiệu** (`/w Tên nội dung`, tên có dấu cách được nhận ra bằng cách so với danh sách bạn).
  Kênh Tổ Đội trả lời "chưa ở trong tổ đội nào" cho tới khi có tổ đội (giai đoạn 9).
- **Bộ lọc chat**: dùng chung bộ lọc tên nhân vật; từ cấm bị thay bằng `***`, cụm từ cấm nhiều chữ thì cả tin thành
  `***`. Danh sách chỉnh được trong `server/data/banned_words.txt`.
- **Enter để chat** (đặc tả 7.2), nên trong động phủ Enter không còn là phím tương tác: tương tác là E (hoặc bấm chuột).
  Khi đang gõ chat, các phím tắt (Tab, G, B, C, P) và di chuyển bị tắt.
- **Ngày/đêm**: một ngày game = 2 giờ thật theo đồng hồ server (UTC); trời tối dần từ 18 giờ game và sáng lại lúc 6 giờ.
  Ở giai đoạn này chỉ là hình ảnh; cá, quái, 明 phát sáng dùng tới sau.
- **Cảnh giới chặn vùng** theo `recommended_realm` trong `data/zones.json` với biên 1 bậc (Phàm Nhân vào được Rừng
  Mực Loang dành cho Luyện Khí, nhưng chưa vào được nơi dành cho Trúc Cơ).
- **Lưu vị trí theo lô** (mục 15.2, 19): ghi ngay khi đổi vùng và khi nhân vật rời thế giới, mỗi 60 giây cho người
  đã di chuyển, và khi tắt máy chủ; tất cả trong một câu `UPDATE` nhiều dòng. Lưu từ REST của động phủ bị bỏ qua khi
  nhân vật đang ở thế giới (tránh lần lưu đến muộn kéo nhân vật về động phủ).
- **Đăng nhập lại khi đang ở ngoài thế giới** thì quay lại đúng vùng, đúng chỗ (`zone_id` của nhân vật). Vị trí lưu
  bị chặn (ví dụ bản đồ đã đổi) thì xuất hiện ở điểm `spawn` của vùng.
- **bcrypt chạy trên luồng phụ** (`auth.ahash/acheck`): mỗi lần băm ~70 ms; chạy thẳng trong event loop sẽ làm tick trễ
  mỗi khi có người đăng nhập. **Sau khi khởi động gọi `gc.freeze()`**: dữ liệu từ vựng và bản đồ sống suốt đời tiến trình,
  không cần bộ gom rác quét lại (một lượt quét đầy đủ từng làm tick trễ ~60 ms khi nhiều người vào cùng lúc).
  Bản đồ được nạp sẵn lúc khởi động vì lý do tương tự.
- **`ACCOUNTS_PER_IP`** (biến môi trường) cho phép tăng giới hạn 5 tài khoản mới/IP/ngày để chạy `tools/load_bots.py`.
  Khi chạy sau Cloudflare Tunnel, mọi yêu cầu đến từ `127.0.0.1`, nên `chay_server_choi_chung.bat` bật `--proxy-headers`
  để giới hạn tính theo IP thật của từng người.
- **`/server/stats` công khai** nhưng chỉ có số đếm và thời gian tick, không có thông tin cá nhân.

## Giai đoạn 4 — chiến đấu Vấn Đạo, tu luyện, Thiên Kiếp

- **Câu trả lời chiến đấu đi qua REST `/quiz/answer`** như mọi câu hỏi khác (một đường chấm duy nhất, đáp án không bao
  giờ rời server), rồi handler `combat` áp kết quả vào trận đấu trong bộ nhớ ngay. Câu hỏi được tạo bằng tác vụ DB
  chạy nền khi đòn đầu tiên trúng quái; tới lúc câu tới, nhân vật được **Hộ Thể** cho tới hạn trả lời (không bị đánh,
  input di chuyển bị bỏ). Hết giờ thì vòng tick chấm sai, nên treo máy giữa trận không né được Mặc Kích.
- **Mặc Thuẫn không bao giờ để quái chết**: còn khiên thì mỗi đòn chỉ 1 sát thương và máu bị giữ ≥ 1. Một người phá khiên
  là khiên vỡ cho mọi người đang đánh con đó (câu hỏi của họ bị hủy bằng `q_end: broken`).
- **Quái tinh anh mọc lại khiên ở ngưỡng** (Mặc Hồ: 50%): máu bị chặn đúng ở ngưỡng kể cả khi một đòn lớn lẽ ra
  vượt qua, nên không thể "một đòn xuyên ngưỡng" bỏ qua câu hỏi thứ hai.
- **Mặc Kích = Sinh Lực tối đa × 10/15/20% (thường/tinh anh/boss) × (1 − Kháng Mực)**, Kháng Mực tối đa 60%. Mặc Kích
  bỏ qua Hộ Thể (đó là cái giá của câu sai) nhưng vẫn bị Sơn Chữ Quyết giảm.
- **Sơn Chữ Quyết (山) là "giữ thế" giảm 50% sát thương trong 5 giây**, không dựng tường như gợi ý trong đặc tả: tường
  cần va chạm động đồng bộ cho mọi client và có thể dùng để chặn người khác ở cổng. Để sau nếu cần.
- **Bậc Pháp Chữ theo độ thuộc chữ** (50/70/90/100 → bậc 1–4); quên chữ thì pháp yếu đi. Học pháp bằng bí kíp rơi từ quái
  và cần chữ đó ≥ 50%.
- **Tầng trong một cảnh giới tự lên** khi đủ Tu Vi; chỉ **bước sang cảnh giới mới** mới cần đan dược và Thiên Kiếp
  (Tu Vi dừng ở mức đầy, gọi là "bình cảnh"). Tu Vi đến từ mọi câu đúng theo ngữ cảnh (`xp_per_correct`: vườn 10,
  đánh quái 6, tưới giúp 4, luyện tập 2, đả tọa 15, câu Thiên Kiếp 0), thu hoạch 15, nhiệm vụ và hạ quái.
- **Thiên Kiếp lưu trong bảng `tribulation_runs`**: 20 chữ chọn sẵn từ toàn bộ chữ đã học, thoát giữa chừng thì tiếp tục
  đúng câu đang dở (câu quá hạn tính sai). Qua thì dùng mất đan dược; trượt thì giữ đan, mất 10% Tu Vi của tầng, chờ
  30 phút (chia `TIME_SCALE`).
- **Chết mất Tu Vi bằng 5% lượng cần cho tầng hiện tại**, không bao giờ tụt tầng; hồi sinh ở Trúc Lâm Thôn sau 3 giây.
- **Máu/linh lực sống trong thế giới**, ghi vào DB theo lô cùng vị trí. Về động phủ thì hồi đầy, ở vùng an toàn hồi
  nhanh gấp 3. **Đan dược chỉ dùng được trong thế giới chung** (máu ở động phủ luôn đầy), thời gian chờ 15 giây.
- **Trang bị là bản thể riêng** (`equipment_instances`: độ hiếm, cấp cường hóa) thay vì chồng trong túi; vật phẩm
  thường vẫn là số lượng. Cường hóa thất bại chỉ mất nguyên liệu + Linh Thạch, không tụt cấp, không vỡ đồ.
- **Tiêu hao vật phẩm lấy cả bản khóa (bound) lẫn bản thường** (`inventory.consume_item`, ưu tiên bản khóa vì bản đó
  không giao dịch được), để đan dược nhận từ nhiệm vụ dùng được như đan mua.
- **Nói chuyện với NPC cho nhiệm vụ** (`/quests/talk`) kiểm tra khoảng cách trên server bằng vị trí trong thế giới, nên
  không thể hoàn thành nhiệm vụ "gặp Trúc Lão" từ xa.
- **`BALANCE_PROFILE=dev`** đè `server/data/balance/dev/*.json` lên số liệu thật (gộp sâu) để thử nhanh từ Phàm Nhân lên
  Trúc Cơ; bị từ chối khi `ENV` không phải `dev`. Số liệu thật không đổi.
- **Giao thức WebSocket lên bản 3**: `me` và trạng thái thực thể có thêm máu/khiên, nên game bản cũ được báo "cần
  cập nhật" thay vì vẽ sai.
- **Màu độ hiếm Phàm/Thiên đậm hơn** (`#7D7468`, `#C99A3A`) để đọc được trên nền giấy; màu trong
  `data/items/equipment.json`.

## Giai đoạn 5 — Linh Phong (ong linh)

- **18 loài ong, mỗi loài gắn một chữ trong dữ liệu từ vựng đã kiểm chứng** (`tools/curation/bees.json`). Tên Hán là
  chữ đó + 蜂. `tools/build_bees.py` lấy pinyin của chữ từ danh sách từ, pinyin của 蜂 (fēng) từ CC-CEDICT, rồi tra
  cả cụm trong CC-CEDICT: chỉ 黄蜂 là từ có thật (nghĩa "ong vò vẽ", game ghi rõ điều đó), các tên khác đánh dấu
  `real_word: false` và hiện "(tên sáng tác)". Tên ong không bao giờ được dùng làm câu hỏi. Không dùng chữ ẩn
  (林, 明…) để khỏi lộ phát hiện. Đủ 5 độ hiếm: Phàm 5, Linh 5, Huyền 4, Địa 2, Thiên 2.
- **Thụ phấn chỉ cắt tối đa 25% thời gian chờ ôn — và chỉ một lần cho mỗi lần cây được thụ phấn.** Lịch lặp lại ngắt
  quãng (10 phút / 1 / 3 / 7 ngày) là thứ làm người chơi nhớ lâu; nếu ong rút ngắn nhiều hơn, người chơi có thể "mua"
  lịch ôn dày đặc bằng ong và tưởng là đã thuộc. 25% đủ để thấy ong có ích (cây 3 ngày thành ~2,25 ngày) mà khoảng
  cách giữa các lần ôn vẫn tăng dần. Giới hạn này là hằng số trong code (`MAX_REVIEW_CUT`), file cân bằng có ghi số
  lớn hơn thì vẫn bị chặn ở 25% (có test). Cắt vào **lượt chờ đang chạy** lúc thanh phấn đầy (tính trên độ dài lượt
  chờ đầy đủ, kể cả hiệu ứng kề ô 水/火), không bao giờ sớm hơn lúc đầy; nếu cây đang đến hạn ôn thì để dành cho lượt
  chờ kế tiếp sau câu trả lời đúng. Câu sai (chờ 5 phút ôn lại) không được cắt.
- **Thụ phấn không bao giờ đổi giai đoạn cây.** Chỉ thanh `pollen` và cờ `pollinated` thay đổi; giai đoạn chỉ đổi
  trong `srs.apply_correct/apply_wrong` (có test chạy ong nhiều ngày liền). Cây dưới Ra hoa (giai đoạn < 3) không nhận phấn.
- **Phấn hoa tính lười, phát lại theo sự kiện**: từ lần tính trước tới nay, mỗi ong chia đều sức của nó cho các cây
  đang ra hoa chưa đầy; khi một cây đầy, thời điểm đầy được tính chính xác rồi phần sức đó chia lại cho các cây còn
  lại. Ong cùng hệ với chính cây hoặc một cây kề bên (水 雨 海… là Thủy; 火 日 红… là Hỏa — bảng trong
  `balance/bees.json`) thụ phấn nhanh ×1,5. Phấn được tính tới hiện tại trước mọi thao tác có thể đổi tập cây đang
  ra hoa (tải vườn, trả lời ôn, thu hoạch, đổi vai trò ong). Một cây lùi giai đoạn vì sương mực khi vắng mặt vẫn
  được tính như đang ra hoa trong khoảng vắng đó (sai số nhỏ, chấp nhận được).
- **Mật và phấn chạy theo `TIME_SCALE`** giống lịch ôn, để thử nhanh trọn vòng nuôi ong.
- **Mỗi con ong luôn chiếm một ô tổ, kể cả khi đang thụ phấn hay hộ vệ** (đặc tả: "mỗi ong chiếm một ô"), nên số ô là
  giới hạn số ong. 30 ô xếp 6 × 5 lục giác (hàng lẻ lệch nửa ô), mở dần từ giữa ra; ô 11+, 16+, 21+, 26+ cần 3/6/9/12
  loài trong Ong Phổ. Đồng hệ cộng hưởng: +5% mỗi ong cùng hệ ở ô kề, tối đa 3 (+15%), áp cho mật, phấn và chỉ số hộ vệ.
- **Trứng ong là vật phẩm trong túi** (gacha, nhiệm vụ, mốc Ong Phổ), loài chỉ quyết định lúc **nở** ở tổ (cùng độ
  hiếm, loài chưa có nặng ×2) để có khoảnh khắc mở trứng. Người chơi nào cũng nhận một Trứng Ong Phàm (khóa) ở lần
  mở tổ đầu tiên, kèm chuỗi nhiệm vụ "Linh Phong" (nở → cho ăn → thụ phấn → hộ vệ → Ong Phổ 4 loài). Chuỗi nhiệm vụ mới
  tự mở cho cả tài khoản cũ (`quests.on_event` gọi `ensure` trước).
- **Gacha Trứng Ong**: 300 Linh Thạch hoặc 5 Tiên Ngọc một lượt, 2.700 / 45 cho 10 lượt (10 lượt chắc chắn có ít nhất
  một trứng Linh). Bảo hiểm Huyền ở lượt 30, Thiên ở lượt 90. Không tính vào giới hạn 15 hạt/ngày; lượt miễn phí hằng
  ngày chỉ dành cho Hạt Chữ.
- **Ong lên cấp** bằng cho ăn (Linh Mật 25, quả chữ 12–60 theo độ hiếm, Linh Quả 90, cá nhỏ 35 kinh nghiệm), thụ phấn
  (12 mỗi cây đầy) và hạ quái (8). Cấp tối đa 20, mỗi cấp +8% chỉ số. Món thích: kinh nghiệm ×2, thân thiết +8 (thường
  +2); thân thiết 100 = +10%. Lần đầu cho đúng món thích thì món đó hiện trong Ong Phổ; trước đó chỉ có một câu gợi ý.
- **Học chữ làm ong mạnh hơn**: mỗi loài gắn một chữ, độ thuộc chữ đó cộng tối đa +10% (100%). Đây là cách "Chữ Đạo"
  chạm tới ong mà không biến ong thành đường tắt bỏ qua câu hỏi.
- **Số ong hộ vệ theo cảnh giới** (Phàm Nhân 0, Luyện Khí 2, Trúc Cơ 3, Kim Đan 4, Nguyên Anh 5) đặt trong
  `balance/bees.json` và kiểm tra ở server cả lúc gán vai trò lẫn lúc đưa ong ra thế giới.
- **Ong hộ vệ không bao giờ gây sát thương cho quái còn Mặc Thuẫn**, kể cả lửa đang cháy (`guard.bee_hurt` từ chối);
  với quái tinh anh, đòn ong cũng dừng ở ngưỡng khiên mọc lại như đòn người. Ong chích làm quái quay sang đánh chủ
  (chủ được tính là đã giao chiến), nên phần thưởng khi hạ quái luôn thuộc về chủ. Đòn báo trước của quái khi rơi xuống
  trúng mọi ong đang chích nó (50% công của quái); ong hết máu về tổ nghỉ 60 giây rồi quay lại đầy máu.
- **Vị trí ong không đi qua mạng**: snapshot chỉ mang loài, %máu, mục tiêu và trạng thái nghỉ; client tự vẽ đường bay
  cong quanh chủ hoặc quanh quái (`client/engine/beeflock.py`). Giao thức lên **bản 4**.
- **Kỹ năng bị động**: đốt (Hỏa Diệm, Kim Ô), làm chậm (Thảo, Vũ, Thủy Linh, Băng Tâm, Hải Triều), choáng (Sơn Thạch,
  Lôi Vân — quái đứng yên, đòn đang báo trước bị hủy), hồi máu cho chủ (Dược Sư, Nguyệt Quang), nhặt đồ rơi (Ngọc Bích:
  +25% Linh Thạch và tỉ lệ rơi đồ của quái nó đã chích), chích nhanh (Phong Hành), nét bút ×3 mỗi 4 cú (Thư Pháp).
- **Tổ ong nâng cấp 5 cấp** bằng Linh Thạch + Sáp Ong (ong làm mật tiết ra, 0,1 sáp mỗi mật) + Gỗ Linh Mộc (rơi từ quái
  ở Rừng Mực Loang). Mỗi cấp tăng sức chứa và tốc độ làm mật và mở một món trang trí (đèn lồng, chậu sen, chuông gió,
  cờ phướn) đặt quanh tổ trong động phủ; bật/tắt được.
- **Làng mua lại Linh Mật, Sáp Ong, Gỗ, Linh Quả, Mực Tinh** với giá thấp (`sell_price` trong `items/materials.json`)
  để mật có chỗ dùng trước khi có luyện đan (giai đoạn 8). Giá cố ý thấp; dòng tiền tổng thể sẽ cân lại ở giai đoạn 8.
- **Thả ong** (giải phóng ô) trả lại Sáp Ong theo độ hiếm, có hỏi xác nhận.
- **Cá Nhỏ** đã có trong dữ liệu (ong ăn được) nhưng chưa có nguồn cho tới giai đoạn 6 (câu cá).
- **Khi thăm động phủ bạn bè** thấy ong của bạn bay quanh tổ và vườn (trừ ong hộ vệ, vì chúng đi theo chủ).

## Giai đoạn 6 — Câu cá

- **Câu cá đi qua REST, không qua WebSocket** (đặc tả 16 gợi ý WebSocket). Cả ao động phủ (vốn chạy REST) lẫn hồ ngoài
  thế giới dùng chung một đường; với hồ, máy chủ đọc **vị trí thật trong thế giới** của nhân vật (như `/quests/talk`)
  để biết có đứng sát nước không, nên không câu từ xa được. Ao động phủ chỉ câu được khi nhân vật không đứng ngoài thế
  giới. Lượt câu đang dở nằm trong RAM (một tiến trình, như thế giới chung); khởi động lại máy chủ thì mất lượt đó
  (mồi đã dùng không trả lại).
- **Máy chủ quyết định mọi thứ**: thời điểm cá cắn (lúc quăng), loài và kích thước (lúc giật, không gửi cho client tới
  khi câu được). Trò kéo cá là một mô phỏng tất định (`fishing_sim.py`, hai bản giống hệt từng byte ở server và client,
  có test): client gửi **các bước mà nút đổi trạng thái**, máy chủ chạy lại đúng trò đó bằng hạt giống của nó để biết câu
  được hay không. Kết quả cần N bước thì phải có ít nhất ~85% × N × 20 ms thời gian thật trôi qua (`too_fast`). Chỉ dùng
  cộng trừ nhân chia và `random.Random.random()` nên hai bên tính ra số thực giống hệt nhau. Một client tự viết có thể
  chơi "hoàn hảo" (vì biết hạt giống) — chấp nhận được: đó vẫn là kỹ năng kéo cá, không đổi được loài, kích thước hay tỉ
  lệ, và vẫn phải chờ đủ thời gian.
- **Trò kéo cá**: thanh dọc, cá (vùng xanh) bơi lên xuống theo những đoạn ngẫu nhiên, móc câu lên khi giữ nút và chìm khi
  nhả. "Dây căng quá lâu thì đứt" = giữ nút trong lúc móc đã vượt lên trên con cá làm thanh Dây đầy dần. Cá hiếm hơn:
  vùng xanh hẹp hơn, bơi nhanh hơn, khỏe hơn (cá to cũng khỏe hơn). Độ khó chỉnh bằng một bot có độ trễ phản xạ 180 ms:
  với Cần Trúc Thô bắt được ~99% cá Phàm, ~87% cá Linh, ~50% cá Huyền; Cần Long Cốt thì ~70% cá Địa.
- **Tỉ lệ cá**: trọng số độ hiếm 70 / 21 / 6,5 / 2 / 0,5; độ hiếm r được nhân `1 + may_mắn × hệ_số_r` (hệ số 0 / 0,6 /
  1,2 / 1,8 / 2,5), may mắn = cần + mồi. Độ hiếm không có loài nào cắn được (sai nơi, sai giờ, sai mồi) bị bỏ rồi chia lại.
  Trong một độ hiếm các loài chia đều, loài được mồi "dụ" tính gấp đôi. Công thức này (`rarity_odds`, `species_odds`)
  được test so với 100.000 lần quay cho 5 tổ hợp cần/mồi/nơi/giờ (sai số < 1%).
- **Câu không mồi được** nhưng cắn chậm ×1,5 và chỉ ra cá Phàm/Linh, để người mới hết tiền vẫn câu được. Mồi trừ lúc quăng.
  Mồi Mực chỉ dụ cá có nhãn "mực" và bị từ chối ban ngày (đặc tả: "chỉ câu được cá Mực ở đêm"); vì vậy có cá Mực ở nhiều
  độ hiếm (Chạch, Lóc, Mực Nang, Nghiên Linh Ngư) để Mồi Mực không thành đường tắt ra cá Huyền.
- **Câu hỏi khi cá cắn**: dạng câu theo độ hiếm (Linh: Q1/Q2/Q11; Huyền: Q3/Q4/Q2; Địa: Q5/Q6/Q7/Q3; Thiên: Q5/Q8/Q7/
  Q6/Q3), lọc theo `min_tier` của cảnh giới như chiến đấu, chữ chọn bằng `selection.pick_word` (ưu tiên chữ cần ôn).
  Đúng: vùng xanh ×1,3; sai: ×0,65; **không bao giờ mất máu**. Cá Thiên: đúng câu 1 thì có câu 2; sai bất kỳ câu nào là
  vào trò kéo với vùng hẹp. Chưa học chữ nào thì không hỏi (vùng bình thường). Câu đúng +6 Tu Vi, độ thuộc ±2 như mọi
  nơi ngoài vườn.
- **Tên cá**: 28 loài có thật lấy tên Hán, pinyin và nghĩa tiếng Anh từ CC-CEDICT (`tools/build_fish.py`); 鲲 (Côn) là từ
  có thật trong CC-CEDICT nên giữ nguyên, chỉ đánh dấu `mythical`. Hai tên sáng tác (化龙鲤, 砚灵鱼) đánh dấu `fictional`,
  từng âm được kiểm tra là một cách đọc của chữ đó. Tên cá không nằm trong danh sách từ nên không bao giờ thành câu hỏi.
  娃娃鱼 thật ra là kỳ giông khổng lồ, 黄鳝 là lươn — game ghi rõ trong mô tả.
- **Ngày/đêm của cá** dùng đúng đồng hồ thế giới (1 ngày game = 2 giờ thật, đêm từ 18 giờ tới 6 giờ). **Mưa** theo từng
  vùng, mỗi 30 phút thật tung một lần bằng hàm băm (vùng, chu kỳ): ai cũng thấy giống nhau, không cần lưu gì
  (Hồ Nghiên Mực mưa 35% thời gian, làng và động phủ 25%). Client hỏi `/world/weather` mỗi phút để vẽ mưa.
- **Cần câu là vật phẩm trong túi** (khóa, không giao dịch), cấp nâng cấp lưu trong `users.flags.fishing` cùng cần/mồi
  đang dùng. Nâng cấp ở Lò Rèn phải đứng cạnh Thợ Rèn, mua bán ở Ngư Ông phải đứng cạnh Ngư Ông (kiểm tra trên máy chủ).
  Cần Thiên Tơ chưa có cách lấy cho tới khi có nguyên liệu bí cảnh (giai đoạn 9).
- **Vảy Linh Ngư** (1/2/3/5 theo độ hiếm Linh→Thiên) là nguyên liệu mua cần cao cấp và nâng cấp cần, để câu cá hiếm
  dẫn tới cần tốt hơn mà không phải chỉ cày Linh Thạch.
- **Cá Nhỏ có nguồn**: cá Phàm nhỏ hơn 25% khoảng kích thước của loài thành `ca_nho` (ong ăn được) thay cho con cá,
  nhưng vẫn tính vào Ngư Phổ. Cá câu được là vật phẩm `fish_<loài>`, làng mua theo giá loài (Phàm 6–14, Thiên 1000–1500);
  dòng tiền sẽ cân lại ở giai đoạn 8 cùng luyện đan.
- **Ngư Phổ** dùng bảng `fish_catches` có sẵn từ migration đầu (số con, con to nhất, lần đầu), không cần migration mới.
  Mốc 5/10/20/30 loài: 200 Linh Thạch, 3/6/15 Tiên Ngọc (đặc tả 12.1: Tiên Ngọc từ mốc thư viện). **Kỷ lục**: 3 con to nhất
  mỗi loài trên toàn máy chủ (một dòng mỗi người), tính từ cùng bảng.
- **Hồ Nghiên Mực** nối với **cổng Tây** của Trúc Lâm Thôn (đặc tả không nói hồ nằm đâu; cổng Tây đang trống), cảnh giới
  khuyến nghị Luyện Khí như Rừng Mực Loang (Phàm Nhân vào được nhờ biên 1 bậc). Ngư Ông đứng ở chân bến gỗ; Mặc Quái chỉ
  đi lang thang ở bờ tây, bờ bắc và góc đông nam, xa bến. Ao trong làng giờ cũng câu được (cá ao như ở động phủ).
- **`BALANCE_PROFILE=dev`** thêm `dev/fishing.json`: cá cắn sau 1,5–3 giây và cá hiếm cắn nhiều hơn hẳn, để thử nhanh.
- **Chuỗi nhiệm vụ "Ngư Ông"** (chào Ngư Ông → câu 3 con → Ngư Phổ 5 loài) tự mở cho cả tài khoản cũ như chuỗi Linh Phong;
  bước "5 loài" tính cả những loài đã câu trước khi bước đó mở.
- **Test client dừng máy chủ thử bằng Ctrl+Break trên Windows** (trước đây `terminate()` giết tiến trình ngay nên máy chủ
  không kịp lưu vị trí, làm `test_reconnect` lỗi trên Windows dù game đúng). `test_tests_leave_no_settings_in_game_folder`
  giờ kiểm tra test **không đổi** `client/config.json`/`session.json` thay vì đòi hai file không tồn tại (máy người chơi
  thật có `session.json`).
- `tools/gen_maps.py` ghi bản đồ với xuống dòng LF trên mọi hệ điều hành (trước đây Windows ghi CRLF làm file đổi dù
  nội dung như cũ).

## Giai đoạn 7 — Ải Thủ Vườn và Tàng Thư Các

- **Trò thủ vườn chạy ở client, máy chủ chạy lại nhật ký** (đặc tả 16, 17) bằng `td_sim.py` — một file giống hệt từng
  byte ở `server/app/systems/` và `client/engine/` (có test), cùng kiểu với `fishing_sim.py`: chỉ cộng trừ nhân chia và
  `random.Random`, nên hai bên ra cùng số thực. Client ghi mọi hành động thành sự kiện `{s: bước, k: loại, ...}`; khi ải
  kết thúc nó gửi cả nhật ký và kết quả nó thấy (`result, core_hp, wave, steps`). Máy chủ chạy lại; nhật ký bị từ chối nếu
  có sự kiện trái luật (`bad_log`: cây không mang theo, trồng sai ô, thiếu Linh Khí, đi ngược thời gian, câu hỏi không có,
  dùng hai lần, sai loại, Tụ Khí chưa hồi...), nếu kết quả chơi lại khác kết quả gửi lên (`log_mismatch`), hoặc nếu số bước
  cần nhiều thời gian thật hơn đã trôi (`too_fast`, chia cho tốc độ tua tối đa ×2). Phép chạy lại nằm trên luồng phụ
  (`asyncio.to_thread`) để không làm trễ vòng tick thế giới.
- **Kết quả câu hỏi lấy từ máy chủ, không từ client.** Mỗi câu hỏi trong ải được tạo qua `/td/question` (ghi vào lượt
  chơi trong RAM) và chấm qua `/quiz/answer` như mọi câu khác; phép chạy lại dùng đúng/sai mà máy chủ đã chấm. Mọi câu
  máy chủ đã tạo trong lượt phải xuất hiện đúng một lần trong nhật ký (câu chưa trả lời tính là sai), nên không thể giấu
  một câu Tụ Khí trả lời sai để khỏi mất Linh Khí. Một client tự viết vẫn có thể chơi "hoàn hảo" (nó biết hạt giống và
  luật) — chấp nhận được: đó vẫn là cách đặt cây, không đổi được câu trả lời, phần thưởng hay thời gian.
- **Lượt đang chơi lưu trong bảng `td_runs`** (migration 0005) cùng nhật ký của nó. Client gửi phần nhật ký mới qua
  **`/td/event`** (đặc tả 16) sau mỗi câu hỏi, mỗi đợt, và ít nhất 2 giây một lần; thoát game hay khởi động lại máy chủ giữa
  ải thì lần sau bản đồ ải hiện "Lượt dở… Chơi tiếp": `/td/resume` trả lại tham số, nhật ký đã lưu và kết quả các câu hỏi,
  client dựng lại đúng trận bằng `td_sim.replay(..., finish=False)` (dừng ngay sau sự kiện cuối) rồi chơi tiếp.
  **Đoạn đã lưu không bao giờ sửa hay xóa được**: gửi lại một đoạn đã lưu phải giống hệt (`log_conflict`), không được bỏ
  cách (`log_gap`), và nhật ký gửi ở `/td/finish` phải bắt đầu bằng đúng đoạn đã lưu — nên tắt game không giúp "đi lại"
  một nước đã lưu. Chỉ những thao tác sau lần lưu cuối (tối đa ~2 giây) là mất khi tắt ngang. Câu hỏi được hỏi sau lần
  lưu cuối thì chưa từng được áp dụng: khi chơi tiếp chúng bị bỏ (một câu Tụ Khí trả lời sai rồi tắt game ngay trước khi
  lưu sẽ không bị trừ 10 Linh Khí — chấp nhận được). Lượt quá 3 giờ bị xóa.
- **Thời gian chỉ trôi trong đợt quái, và dừng khi thẻ câu hỏi đang mở.** Giữa các đợt người chơi bày cây thong thả;
  câu hỏi là để học, không phải để đua với quái. Linh Khí tự tăng theo thời gian trong đợt. Hồi chiêu Tụ Khí 10 giây tính
  theo thời gian trong ải. Trước mỗi đợt (cả đợt đầu) tự hiện 3 câu Linh Khí Vấn Đạo; sai không mất gì. Tụ Khí đúng +10,
  sai −10 (không âm). Nâng cấp: trả đủ Linh Khí rồi hỏi đúng chữ của cây; sai thì mất số Linh Khí đó (đặc tả 9.1).
- **Sức mạnh cây = hệ số độ thuộc × hệ số sương mực** (0 → 60%, 100 → 130%; wither 100 → −30%). Wither lấy ô **khỏe nhất**
  đang trồng chữ đó trong vườn thật (tính lười bằng `srs.refresh_wither` như khi tải vườn); chữ không còn trồng thì không
  có sương mực. Sức mạnh nhân vào sát thương, máu Mộc, Linh Khí sinh ra và sức hỗ trợ; tính lúc vào ải và gửi trong
  `params`, không đổi giữa ải.
- **Vai trò cây** (`server/data/plants/plant_roles.json`): chữ đặc biệt gán tay (`by_hanzi`), còn lại theo chủ đề
  (`by_topic`). Một số chữ ví dụ của đặc tả không có trong danh sách từ (金 刀 力 石 光 米), nên Kim nhận các chủ đề số
  đếm, hành động, con vật, đồ vật; 苹果 là Sinh Khí qua chủ đề đồ ăn; ngữ pháp, lượng từ và tính từ (大 小) là Sơn. Test
  kiểm tra mọi chữ đều có vai trò và mọi ví dụ của đặc tả có trong dữ liệu đều đúng vai.
- **"Tối đa 8 loại"** là 8 chữ khác nhau; mỗi loại trồng bao nhiêu cây cũng được nếu đủ Linh Khí. Chỉ mang được chữ đã
  học (`introduced`). **Thành ngữ không trồng** mà là tuyệt chiêu một lần mỗi ải: 一石二鸟 đánh mạnh 2 con nhiều máu nhất,
  画蛇添足 làm mọi quái chậm hẳn 8 giây, 对牛弹琴 làm cả đám đứng ngẩn 5 giây.
- **Mộc trồng trên đường** (chặn quái, máu cao, có gai làm mất máu con bị chặn), các vai khác trồng cạnh đường; ô cổng và
  ô Linh Mạch không trồng được. **Tầm bắn tính tới ô đường**: một con quái trong tầm khi ô đường gần nó nhất nằm trong
  bán kính (vừa tất định vừa rẻ); vùng nổ của Hỏa đo dọc theo đường. Kim nhắm con **nhiều máu nhất**, các vai khác nhắm
  con đi xa nhất.
- **Phản ứng kề ô trong ải** (`combos` trong `balance/td.json`): 女 cạnh 子 thành 好 (cả hai +30%), 日/太阳 cạnh 月/月亮 thành
  明 (vùng sáng ×2), 3 cây 木/林/森/树 liền nhau thành 森 (cả cụm +50% máu), 人 cạnh cây gỗ thành 休 (cây gỗ tự hồi máu).
  Hiện thông báo khi một phản ứng thành hình.
- **Quái của ải là 6 loài mới** (Mực Con, Mực Phi, Mực Đặc, Mực Ẩn, Thạch Mặc, Mặc Vương), kháng/yếu nguyên tố trong
  `balance/td.json`, thẻ thông tin khi rê chuột và ở bản đồ ải. Mực Ẩn chỉ bị đánh khi đứng trong vùng sáng (cây Quang),
  cây Mộc vẫn chặn được. Gặp/hạ quái của ải ghi vào **Yêu Quái Phổ** với mã `td_<loài>` (Yêu Quái Phổ giờ có trang).
- **30 ải sinh bằng `tools/gen_td_levels.py`** (bản đồ 12 × 7 từ các mẫu đường đi vẽ tay, đợt quái từ "ngân sách máu"
  tăng theo ải và theo đợt, số liệu trong `level_gen` của `balance/td.json`) vào `server/data/td/levels.json`; test kiểm
  tra file khớp với script. Chương 1/2/3 cần Phàm Nhân/Luyện Khí/Trúc Cơ và ải trước đó; Linh Khí khởi đầu theo chương
  (110/200/300). **Độ khó chỉnh bằng `tools/td_bot.py`**: một người chơi tham lam đơn giản (8 cây, độ thuộc 40–50, đúng 85%)
  thắng cả chương 1 (Linh Mạch còn ≥ 16 điểm), gần hết chương 2; cuối chương 3 cần cây mạnh hơn hoặc chơi khéo hơn.
- **Sao theo điểm Linh Mạch còn lại** (≥ 16 / 8 / 1 trên 20). Thưởng lần đầu cho **từng sao mới đạt** (đạt 1 sao rồi sau
  đó 3 sao thì nhận phần của sao 2 và 3), cộng thưởng riêng ở vài ải (bí kíp, Gỗ Linh Mộc, Tiên Ngọc, một hạt giống của
  chữ đã học). Thắng lại một ải đã có sao: thưởng nhỏ, **tối đa 5 lần/ngày, dùng chung với Vô Tận Trận**.
- **Vô Tận Trận** mở sau ải c1_10. Hạt giống theo tuần (băm của tuần ISO, giờ UTC+7) nên cả máy chủ đánh cùng một trận
  trong tuần; đợt quái sinh vô hạn trong `td_sim.endless_wave` (tối đa 60). Kỷ lục tuần lưu trong `td_progress` với
  `level_id = endless_<năm>w<tuần>`, bảng xếp hạng lấy từ đó. Thưởng Linh Thạch theo số đợt giữ được (có trần).
- **Một migration mới (0005, bảng `td_runs`)** cho lượt đang chơi; `td_progress`, `td_loadout` đã có từ migration đầu;
  lượt thưởng trong ngày, mốc thư viện, danh hiệu, khung avatar lưu trong `users.flags`. Máy chủ tự nâng cấp `dev.db` khi
  khởi động như mọi lần.
- **`BALANCE_PROFILE=dev` chỉ đổi tốc độ tua tối đa** (×40 thay vì ×2) để thử nhanh và để test giao diện chơi hết chương 1
  trong vài phút; số liệu ải không đổi. Tốc độ tua chọn lần trước được giữ cho ải sau.
- **Thẻ câu hỏi trong ải bỏ qua cú bấm và phím số trong 0,3 giây đầu**: một đợt quái có thể kết thúc đúng lúc người chơi
  đang bấm lên bản đồ, thẻ hiện ra dưới con trỏ sẽ nhận nhầm cú bấm thành một đáp án.
- **Font không có ký tự ★** (hiện ô vuông) nên ngôi sao được vẽ bằng hình đa giác.
- **Tàng Thư Các** gom 6 phổ: Bách Thảo Phổ (mới), Yêu Quái Phổ, Ong Phổ, Ngư Phổ, Sổ Phát Hiện, Bảo Vật Phổ (mới), cùng
  Sổ Lỗi (đặc tả 8.3). Mở bằng Thủ Thư ở Trúc Lâm Thôn, phím **L**, hoặc nút trong Sổ Phát Hiện. Linh Thú Phổ chờ giai
  đoạn 8 (chưa có pet nào trong game).
- **Bảo Vật Phổ** = trang bị, đan dược và cần câu từng có. Không cần lưu thêm gì: lấy từ `audit_log` (mọi lần nhận vật
  phẩm, `item:<id>` / `equip:<id>:<độ hiếm>` với delta dương) cộng những gì đang giữ; dùng hết rồi vẫn còn trong phổ. Bí
  kíp, nguyên liệu, cá không tính (đã có phổ riêng hoặc không phải bảo vật).
- **Danh hiệu và khung avatar** (thưởng mốc thư viện) đeo được trong Tàng Thư Các (`/library/wear`), lưu trong
  `users.flags`, có trong `/me`. Danh hiệu hiện sau tên trên thẻ nhân vật (thế giới, động phủ, bảng Tu luyện), khung là
  viền màu quanh chân dung. Người chơi khác **chưa** thấy (phải đổi giao thức WebSocket; để giai đoạn sau).
- **Kệ bí kíp của Thủ Thư** (đặc tả 8.4: bí kíp "mua ở Tàng Thư Các"): 4 bí kíp Pháp Chữ, giá Linh Thạch trong
  `balance/library.json`. Xem được ở mọi nơi, nhưng chỉ mua được khi đứng cạnh Thủ Thư (máy chủ kiểm tra vị trí thật như
  Ngư Ông). Học bí kíp vẫn theo luật cũ (thuộc chữ ≥ 50%), đã học vẫn mua được (hiện "Đã học"). % = số mục đã có ÷ tổng (làm tròn xuống); mốc 25/50/75/100% của từng phổ trong `balance/library.json`
  (Linh Thạch, Tiên Ngọc, danh hiệu, khung avatar, một ô tổ ong không cần điều kiện). Các mốc riêng của Ngư Phổ (theo số
  loài) và Ong Phổ vẫn giữ, đây là mốc chung của thư viện.
- **Bách Thảo Phổ**: một trang cho mỗi chữ. "Đã có" = chữ nằm trong `collection` (kể cả hạt vừa quay chưa xem thẻ giới
  thiệu, vì trang chỉ chép lại thông tin của hạt); chưa có thì là bóng đen với dấu "?", **cây ẩn** (明 林 森 好 休 吗) chưa
  phát hiện chỉ là khung trống, máy chủ không gửi gì ngoài mã. Lời bình của Trúc Lão ghép từ độ thuộc và vai trò.
- **Tìm kiếm chỉ trong những gì đã phát hiện** (chữ, cá, ong, quái): gõ chữ Hán, pinyin có dấu, không dấu hoặc dạng số,
  nghĩa tiếng Việt có hoặc không dấu. Tìm một chữ chưa có không bao giờ làm lộ nó.
- `xp_per_correct.td = 4`: câu đúng trong ải cho Tu Vi như mọi nơi.
- **Test client không nạp gói `app` của máy chủ**: `app/config.py` đọc `server/.env` vào biến môi trường của tiến trình,
  và các máy chủ thử chạy sau đó trong cùng phiên test sẽ thừa hưởng (vd `BALANCE_PROFILE`). Test client dựng `params`
  của ải thẳng từ các file JSON.
- Sửa test câu cá `test_client_cannot_choose_the_fish_or_claim_a_catch` của giai đoạn 6 bị chập chờn: nó dùng "giữ nút
  suốt" làm đầu vào chắc chắn đứt dây, nhưng khi cá bơi sát mặt nước thì móc nằm trong vùng xanh và đôi khi câu được thật.
  Giờ dùng "không bấm gì" (móc nằm đáy, luôn dưới con cá) — chắc chắn sổng.

## Giai đoạn 8 — Luyện đan, khắc văn, Linh Thú, kinh tế

- **Đan phương là vật phẩm giữ mãi** (`dp_*` trong `items/materials.json`, kind `recipe`): có trong túi là luyện được,
  không mất khi luyện. Nguồn: nhiệm vụ "Đan Đạo", kệ sách Thủ Thư (mua một lần, mua lại bị từ chối), quái làm rơi
  (Thanh Điệu Yêu: Kháng Mực; Mặc Hồ: Trúc Cơ). Nút kệ đổi tên thành "Kệ sách" (bí kíp + đan phương).
- **Nguyên liệu** theo đặc tả: quả chữ (theo độ hiếm tối thiểu), Linh Quả, Linh Mật, Sáp Ong, cá (theo độ hiếm), Mực Tinh,
  và **dược thảo** mới: Trúc Diệp Thảo (sạp bán, quái rừng rơi) và Mặc Linh Chi (Thanh Điệu Yêu, Mặc Hồ). Đặc tả nói dược
  thảo hái ở "Núi Trúc" nhưng bản đồ chưa có vùng đó; tạm để quái rơi + sạp bán, Núi Trúc để giai đoạn sau.
  Máy chủ tự chọn quả/cá **ít quý nhất** thỏa điều kiện (loại nhiều nhất trước), người chơi không phải chọn từng quả.
- **Lò**: Đan Lô trong động phủ (đặt gần bàn đả tọa, `tools/gen_maps.py`) nâng được 3 cấp (vùng văn hỏa rộng +3/+5,
  cấp 3 có 25% ra thêm 1 viên); lò công cộng của Đan Sư ở làng luôn cấp 1. Máy chủ kiểm tra vị trí như Ngư Ông: không ở
  thế giới chung = ở nhà; trong làng phải đứng cạnh Đan Sư. Sạp Vải giờ là biển "đóng cửa" (Bà Chủ Sạp ngay cạnh).
- **Canh lửa** (`alchemy_fire.py` chung cho máy chủ và client, như `td_sim.py`): kim chạy 0 → 100 → 0, mỗi lần bấm kim
  chạy lại từ 0, chu kỳ ngắn dần qua 3 lần và theo độ khó của đan. Nguyên liệu và phí trừ khi **nhóm lửa**
  (`/alchemy/start`) — bỏ dở là mất (không "thử lại tới khi đẹp"). Máy chủ chọn chỗ vùng văn hỏa; client gửi thời gian
  kim chạy trước mỗi lần bấm, máy chủ tính lại vị trí kim và từ chối nếu tổng thời gian dài hơn thời gian thật đã trôi
  (`too_fast`, cho 2 giây mạng). Một client tự viết vẫn bấm "hoàn hảo" được (nó biết vùng) — chấp nhận được như ải thủ
  vườn: đó chỉ là kỹ năng bấm, không đổi được câu trả lời pinyin hay phần thưởng.
- **Chữ trên tên đan**: tên Hán đúng nghĩa Hán-Việt (回血丹 Hồi Huyết Đan, 聚灵丹 Tụ Linh Đan...), pinyin kiểm bằng
  CC-CEDICT trong test. Phần lớn các chữ này không có trong HSK 1–2, nên "chữ đã học" = chữ nằm trong **bất kỳ** từ đã học
  (气 có trong 天气, 空气). Chữ chưa học thì hiện chữ + pinyin + âm Hán-Việt để học (đặc tả: bỏ bước gõ). Phẩm chất tính
  theo **tỉ lệ** điểm / điểm tối đa (bấm: tuyệt hảo 2, văn hỏa 1, trượt 0; pinyin đúng +1, sai −1): từ 85% thượng, 60%
  trung, 30% hạ, dưới nữa là phế đan — người chưa học chữ nào vẫn luyện được thượng phẩm bằng 3 lần bấm tuyệt hảo, còn
  người đã học thì gõ sai bị trừ. Phẩm chất đổi **số viên** (đan thường: hạ 1, trung 2, thượng 3; đan đột phá luôn 1),
  không đẻ thêm loại vật phẩm.
- **Đan dược**: Hồi Huyết / Hồi Khí như cũ. **Tụ Linh Đan không cho Tu Vi trực tiếp** (luật cũ: không có Tu Vi nếu không
  trả lời) mà là bùa 10 phút: mỗi câu đúng +50% Tu Vi. Kháng Mực: +15 Kháng Mực 10 phút. Ngộ Tính: +3 giây cho mọi câu có
  giờ trong 10 phút (cộng vào `time_limit` khi tạo phiên). Bùa lưu trong `users.flags.buffs` (hạn tuyệt đối), uống thêm
  thì cộng dồn tối đa 2 liều; ngoài thế giới dùng chung hồi chiêu 15 giây với Hồi Huyết Đan. Phong Vương Đan cho ong ăn
  (400 kinh nghiệm, +15 thân thiết). Kim Đan Đan luyện được từ Trúc Cơ (cảnh giới Kim Đan để giai đoạn 11).
- **Khắc Văn**: 3 câu liên tiếp về đúng chữ đó (context `forge` của đặc tả mục 4), dạng câu xoay vòng Q1/Q2/Q3/Q5/Q4 để
  không ba lần cùng một kiểu; sai một câu là hỏng, phí (60 Linh Thạch + 2 Mực Tinh) trả khi bắt đầu. Ô khắc: Phàm/Linh 1,
  Huyền/Địa 2, Thiên 3. Thuộc tính theo chữ của đặc tả (火 công, 山 thủ, 心 Linh Lực, 人 Sinh Lực, 日/月 bạo kích); **水
  "kháng làm chậm"** đổi thành Kháng Mực vì người chơi chưa bao giờ bị làm chậm; chữ khác theo vai trò Thủ Vườn của nó
  (`plant_roles.json`), nhân hệ số độ hiếm. Giá trị cố định lúc khắc. Mài chữ 30 Linh Thạch. Chữ khắc hiện nhỏ cạnh tên
  trang bị ở Lò Rèn. Câu khắc văn cho mastery ±2 và Tu Vi như mọi câu ngoài vườn.
- **Linh Thú**: 12 con giáp theo thứ tự Việt Nam (**Mèo** thay Thỏ, **Dê** cho 羊), chữ Hán và pinyin kiểm bằng CC-CEDICT.
  Độ hiếm theo bảng gacha (Thường 4, Hiếm 4, Quý 3, Huyền thoại 1 = Rồng). Bốn kỹ năng của bản 1 giữ nguyên (Chuột +5%
  Hiếm — lấy 5% từ phần Thường; Trâu +20% tiền ôn đúng; Hổ sương mực chậm 50%; Rồng gấp đôi câu thứ 5 liên tiếp); tám con
  còn lại mỗi con một kỹ năng tự thiết kế, móc vào đúng chỗ nó tác động (Gà Tu Vi ôn vườn, Chó đồ rơi, Lợn bán quả, Mèo
  may mắn câu cá, Dê mật khi thu, Rắn Mặc Kích, Khỉ Linh Khí đầu ải, Ngựa Linh Thạch hạ quái). Không kỹ năng nào trả lời
  hay bỏ qua câu hỏi. Chuỗi của Rồng tính mọi câu ôn vườn (đúng +1, sai về 0), lưu `users.flags.garden_streak`.
- **Trùng pet** thì lên cấp (tối đa 5, chỉ số +25% mỗi cấp); quá cấp 5 thành Linh Thạch (60/120/250/600 — trung bình chỉ
  ~117 trên 500 mỗi lượt). Gacha Linh Thú 500 / 4.500 cho 10 (giảm 10% như các quầy khác), 10 / 90 Tiên Ngọc, 10 lượt có
  ít nhất 1 Hiếm. Pity như cấu hình sẵn từ giai đoạn 1 (Quý 20, Huyền thoại 60).
- **Pet đi theo**: hình vẽ bằng code (`art/build.py pet_frames`, 4 dáng: thú bốn chân, gà, rắn, rồng; tai/đuôi/sừng/bờm/
  mào theo `look` trong `pets.json`). Ở động phủ và thế giới chung con vật chạy theo sau chủ; người khác cũng thấy (trường
  `pet` của người chơi trong snapshot, không đổi số phiên bản giao thức). Phím **O** mở bảng Linh Thú; trong làng có nút
  "Linh Thú" ở thanh dưới; ở động phủ thanh nút đã đầy nên có nút trong bảng Tu luyện (K).
- **Sạp Tạp Hóa** (`balance/shop.json`): đan cơ bản, Trúc Diệp Thảo, Mực Tinh, giun, **Hạt Giống Thường** (hạt Thường
  ngẫu nhiên, ưu tiên chữ chưa có, tính vào 15 hạt mới/ngày), đồ Phàm/Linh mọi loại; giới hạn mỗi món mỗi ngày (UTC+7)
  lưu trong `users.flags`. Bán lại: vật phẩm và quả qua API cũ (`/inventory/sell`, `/fruits/sell`, bán ở đâu cũng được như
  trước), trang bị qua `/shop/sell_equipment` (phải tới sạp, không bán đồ đang mặc). Giá thu mua trang bị theo độ hiếm,
  +10% mỗi cấp cường hóa — luôn thấp xa chi phí.
- **Tặng quà** (đặc tả 12.4): chỉ vật phẩm **không ràng buộc** thuộc loại ăn được, nguyên liệu, dược thảo, mồi, đan, cá,
  trứng; 1–5 cái mỗi lần, 5 lần mỗi ngày mỗi người tặng; không tặng tiền, trang bị, bí kíp, đan phương. Người nhận được
  thông báo ngay nếu đang online. Nút "Tặng quà" trong danh sách bạn bè.
- **Nhiệm vụ hằng ngày**: mỗi ngày 1 việc cố định ("Ôn 15 chữ" = 15 câu đúng ở bất cứ đâu, vì vườn theo lịch SRS không đủ
  15 lần ôn/ngày cho người mới) + 2 việc chọn từ bảng (đánh 10 quái, câu 3 cá, thụ phấn 2 cây, luyện 2 mẻ, thắng 2 ải, đả
  tọa 3 câu, ôn vườn 4 lần), chọn cố định theo (người chơi, ngày) nên mở lại không đổi. Lưu cùng bảng `quests` (id
  `d<ngày>:<việc>`), việc hôm qua bị xóa khi tạo việc hôm nay; xong cả 3 thì thêm 50 Linh Thạch + 1 Tiên Ngọc một lần.
  `GET /me` tạo sẵn việc của ngày để mọi sự kiện đều được tính. Bảng Nhiệm vụ có hai tab và cuộn được.
- **Chuỗi nhiệm vụ "Đan Đạo"**: gặp Đan Sư (nhận đan phương Hồi Huyết + dược thảo) → luyện mẻ đầu → khắc văn một lần →
  luyện thêm 5 mẻ (10 Tiên Ngọc, đan phương Phong Vương).
- **Kinh tế** (`docs/BALANCE.md`): `tools/economy_sim.py` tính "giá có được" rẻ nhất của mọi món chỉ bằng Linh Thạch qua
  mọi phép đổi tức thời (mua, luyện, cắt mồi, cường hóa, gacha theo kỳ vọng) và báo vòng lặp nếu có món bán được ≥ giá đó;
  mô hình 30 ngày cho 3 kiểu người chơi in dòng tiền từng ngày. `server/tests/test_economy.py` chạy cả hai. Đan dược giờ
  bán được cho làng (6–120) nhưng luôn rẻ hơn nguyên liệu.
- **Một migration mới (0006, bảng `alchemy_sessions`)**: mẻ đan đang luyện (vùng văn hỏa, chữ phải gõ kèm đáp án) sống sót
  qua khởi động lại máy chủ; mở lò lần nữa thì "Luyện tiếp" đúng mẻ đó. Những thứ khác (cấp lò, bùa, lượt mua trong ngày,
  lượt tặng quà, chuỗi Rồng, lần khắc văn đang làm) nằm trong `users.flags`; pet dùng bảng `pets` có từ migration đầu.
- Test cũ được cập nhật theo thiết kế mới: `test_closed_banner` (quầy Linh Thú giờ mở; quầy tắt vẫn bị từ chối, kiểm bằng
  cách tắt tạm trong cấu hình) và hai test Tàng Thư Các (thêm Linh Thú Phổ, kệ có đan phương).

## Giai đoạn 9 — Bí cảnh hợp tác

- **Tổ đội** sống trong bộ nhớ của máy chủ (`realtime/party.py`), như cả thế giới: khởi động lại là mất, không cần bảng
  mới. Mời bằng đạo hiệu (người đó phải online, không chặn nhau), chỉ đội trưởng mời/mời ra/nhường; đội còn 1 người là
  giải tán; ngoại tuyến quá 60 giây thì rời đội. Trạng thái đội (máu %, vùng, online, hồn ma) gửi lại khi có thay đổi,
  tối đa 1 lần/giây. Kênh chat **Tổ Đội** (`/d`, tab riêng; trong bí cảnh là kênh mặc định). **Chia Tu Vi**: khi quái chết,
  đồng đội trong cùng kênh, cách quái ≤ 220 px mà không đánh nó vẫn nhận 50% Tu Vi của quái (không nhận Linh Thạch/đồ rơi).
- **Hai bí cảnh** (`data/realms.json`): **Khe Nứt Mực** (khe nứt ngẫu nhiên, Luyện Khí, HSK 1, 3 phòng câu đố + boss,
  15 phút, boss 70% máu) và **Mặc Ảnh Động** (định kỳ, Trúc Cơ — đúng bảng 7.3 "Trúc Cơ: bí cảnh cấp 1", HSK 2, 5 phòng +
  boss, 20 phút). Có khe nứt để người Luyện Khí cũng được chơi. "Đúng cấp bí cảnh" hiểu là chữ có cấp ≤ cấp bí cảnh.
- **Lịch** (`balance/realm.json`): 12:00, 19:00, 21:00 giờ Việt Nam, mở 15 phút, thông báo toàn máy chủ trước 10 phút và
  lúc mở (tin `notice`). `BALANCE_PROFILE=dev` thì Mặc Ảnh Động luôn mở, khe nứt xuất hiện thường hơn và hàng chờ ghép
  nhanh hơn — để thử. **Vào Mặc Ảnh Động** phải đứng ở **Cổng Bí Cảnh** (giữa quảng trường Trúc Lâm Thôn); thành viên khác
  ở đâu ngoài thế giới cũng được kéo vào (không ở trong động phủ, không đang gục, đủ cảnh giới).
- **Khe Nứt Mực**: mỗi 60 giây, mỗi kênh có người của Rừng Mực Loang / Hồ Nghiên Mực có 12% mọc một khe nứt cách một
  người chơi 70–170 px, sống 5 phút, tối đa 2 khe cả máy chủ. Khe là một thực thể (`k: "r"`) trong vùng quan tâm như quái,
  nên chỉ ai ở gần mới thấy; người ở gần nhận thông báo. Đội trưởng đứng sát khe (≤ 56 px) dẫn đội vào; người đi một mình
  bấm "Chờ người cùng vào" để vào hàng chờ của chính khe đó (phải đứng gần). Một khe dùng được cho nhiều đội tới khi khép.
- **Hàng chờ ghép đội**: chỉ cho người đi một mình (đội thì đội trưởng bấm vào). Ghép theo **đúng cảnh giới**; đủ 5 người
  thì vào ngay, đủ 2 người mà người đợi lâu nhất đã chờ 20 giây thì vào; nếu sau 40 giây vẫn không ghép được vì lệch cảnh
  giới (ít người online) thì trộn cảnh giới. Ghép xong là một tổ đội bình thường.
- **2 lượt/ngày/bí cảnh** (UTC+7), đếm trong bảng mới `realm_members` (migration 0007). Lượt bị tính khi vào; nếu cả đội
  không vào được vì có người vừa đi khỏi trong lúc mở cửa thì lượt được trả lại (xóa lượt chơi). Rời giữa chừng vẫn mất
  lượt.
- **Instance**: mỗi lượt là một `RealmInstance` — chính là một `ChannelZone` riêng trên bản đồ `bi_canh` (6 gian kín: Ghép
  Chữ, Đứt Đoạn, Thanh Điệu, Gương, Mê Cung, hang boss), nên di chuyển có kiểm tra, Vấn Đạo, ong hộ vệ, Linh Thú, snapshot
  đều dùng lại nguyên vẹn. Các gian **không nối nhau**: phòng xong thì sau 4 giây máy chủ chuyển cả đội sang phòng kế (gửi
  lại `zone`), thứ tự phòng ngẫu nhiên, chỉ chọn loại câu đố mà đội chơi được bằng chữ đã học (Ghép Chữ cần một chữ ⿰/⿱
  có người đã học; Đứt Đoạn cần một câu mà mọi từ đều có người đã học). Mê cung cố định (sinh bằng code, mở bằng Tiled
  được). Client chỉ thấy gian đang đứng (camera cố định giữa gian, ngoài gian tô đen).
- **Phòng xong = câu đố giải + quái trong phòng (Mặc Ảnh, Bút Yêu — không mọc lại) bị hạ.** Câu đố do máy chủ quyết định
  từ vị trí đứng và lệnh `ract` (đánh trụ); mỗi người chỉ nhận phần riêng của mình (`mine`): mảnh chữ, mấy mảnh câu (xáo
  thứ tự, không lộ vị trí), chữ trước gương. Nước đi trong câu đố về một chữ cũng tính như trả lời ngoài vườn (mastery ±2,
  sai thì đánh dấu cần ôn) nếu người đó có chữ ấy.
  - **Cửa Ghép Chữ**: chữ có cấu tạo 2 phần trái-phải (⿰) hoặc trên-dưới (⿱) theo makemeahanzi, ví dụ 好 = 女 + 子. Bốn bệ
    hình chữ thập, sáng 2 bệ theo kiểu ghép. Hai người cầm đúng mảnh, người còn lại cầm mảnh nhiễu. Đứng đủ hai bệ: đúng
    thì mở; sai thì **người đứng sai** mất 10% máu, chia mảnh lại, nghỉ 2,5 giây. 10 giây tính từ lúc có người bước lên;
    hết giờ thì ai đang đứng mất 5%; mọi người bước xuống hết thì bỏ qua không phạt. Còn một người thì chỉ cần một bệ.
  - **Câu Văn Đứt Đoạn**: câu 3–8 từ (sàn có 8 ô số), mỗi mảnh giao cho người đã học từ đó nếu có. Bước lên ô k+1 mà mình
    giữ mảnh thứ k+1: đúng; người khác bước lên ô đó: mất 10% máu. Bước sớm lên ô của mình: chỉ nhắc "chưa tới lượt".
    Người giữ mảnh rời đi/gục thì mảnh chuyển cho người khác.
  - **Trụ Thanh Điệu**: không phát âm (mã âm thanh chứa số thanh, sẽ lộ đáp án) mà hiện **chữ Hán + pinyin không dấu** như
    đặc tả cho phép. Máy chủ chọn thanh trước, rồi chọn chữ mang thanh đó **trong số chữ người đứng gần trụ đó nhất đã
    học** (để "người phải trả lời đã học chữ đó"). Ai đánh đúng trụ trong 5 giây (+1 giây mạng) cũng tính; đánh nhầm thì
    người đánh mất máu; hết giờ thì người gần trụ đúng nhất lúc tượng đọc mất máu; sai hay hết giờ chuỗi về 0. 8 lần đúng
    liền thì xong.
  - **Gương Nghĩa**: mỗi người được một từ đã học, nghĩa không trùng nhau; gương hiện nghĩa từ của một người. Phải **bước
    vào** gương (đang đứng sẵn trong đó thì ra rồi vào lại). Sai người: cả đội mất 6%; 25 giây không ai vào: cả đội mất 3%.
    Đúng 3 lần thì xong.
  - **Mê Cung Mực**: người đã học **明** (hoặc 光 nếu sau này có trong danh sách từ) tỏa sáng bán kính 64 px. Đặc tả nói
    "có kỹ năng Quang" — chưa có Pháp Chữ Quang nên dùng "đã học chữ". Không ai học thì người học nhiều chữ nhất cầm
    **đèn lồng** sáng yếu (40 px) để mê cung luôn qua được. Đứng ngoài ánh sáng: mất 2% máu mỗi giây. Mọi người còn đứng
    tới cửa ra là xong.
- **Boss Nghiên Ma** (48×48): Mặc Thuẫn hồi ở 75/50/25% → 4 pha. Mỗi pha khiên lớn chỉ vỡ khi **N người khác nhau trả lời
  đúng**, N = số người còn sống và còn kết nối (người gục giữa pha làm N giảm ngay). Ai đúng rồi thì không bị hỏi thêm pha
  đó (đánh thường vẫn chỉ 1 sát thương). Mỗi 8 giây một vùng **Mặc Triều** đỏ bán kính 44 px dưới chân một người, 1,6 giây
  sau trúng 15% máu (đang trả lời — Hộ Thể — thì không trúng). Máu boss ×(1 + 40% mỗi người thêm). Boss tỉnh sau 3 giây.
- **Hồn ma**: hết máu trong bí cảnh không mất Tu Vi, không về làng: thành hồn ma (vẽ mờ) vẫn đi theo đội nhưng không đánh,
  không giải đố, không bị đánh; hồi sinh 50% máu khi đội sang phòng kế (hoặc khi kết thúc). Cả đội là hồn ma = thất bại.
- **Kết thúc**: thắng (hạ boss), thất bại, hết giờ, hoặc mọi người đã rời. Màn kết quả 30 giây rồi cả đội về Cổng Bí Cảnh.
  Vị trí trong bí cảnh **không bao giờ được lưu**: lưu định kỳ hay rời thế giới đều ghi chỗ Cổng Bí Cảnh, nên khởi động lại
  máy chủ giữa chừng thì người chơi đứng ở làng.
- **Rớt mạng** (đặc tả 14.3): trong bí cảnh nhân vật chờ 60 giây (ngoài thế giới 30). Vào lại kịp thì máy chủ gửi lại toàn
  bộ (`start`, `room` kèm phần riêng, `end` nếu đã xong). Quá hạn thì rời bí cảnh, `realm_members.result = "disconnected"`,
  vẫn giữ phần thưởng các phòng đã qua. Người đang rớt mạng không tính vào "người chơi được" (không chia mảnh cho họ,
  không tính vào N của boss).
- **Phần thưởng riêng, không nhận hai lần**: mỗi lần nhận là một dòng `realm_claims(run_id, user_id, stage)` (khóa chính)
  ghi **cùng giao dịch** với tiền/đồ. Gọi lại hay hai yêu cầu cùng lúc thì yêu cầu sau vi phạm khóa chính và không được gì.
  Mỗi phòng xong: mỗi người còn trong lượt tự tung xúc xắc (15–30 Linh Thạch, Mực Tinh, Thiên Tằm Ti, Hồi Huyết Đan, 20 Tu
  Vi). Rương cuối: Linh Thạch, Tiên Ngọc, **Mảnh Bảo Vật chung** (cùng số cho cả đội = gốc + 1 cho mỗi phòng câu đố không
  sai lần nào), 2–3 lần mở bảng đồ (Thiên Tằm Ti, Mặc Linh Chi, trứng ong Huyền/Địa/Thiên, đan phương Kim Đan, đồ bộ Mặc
  Ảnh), Tu Vi. Xong trong nửa thời gian: ×1,5 Linh Thạch và thêm một lần mở bảng.
- **Đồ bộ Mặc Ảnh** (Quan, Bào, Ngoa, Bội): rơi từ rương (phẩm Linh/Huyền trở lên) hoặc **Ghép Bảo Vật** ở Cổng Bí Cảnh:
  12 Mảnh Bảo Vật + 600 Linh Thạch → một món phẩm Thiên tự chọn. Thưởng bộ: 2 món +8 Kháng Mực, 4 món +40 Sinh Lực, +6 Công
  (`equipment.json → sets`, cộng trong `stats_for`). **Cần Thiên Tơ** giờ mua được ở Ngư Ông bằng 12 Thiên Tằm Ti + 30 Vảy
  Linh Ngư + 6.000 Linh Thạch.
- **Ping biểu tượng**: chuột phải trong bí cảnh đặt dấu "!" (giữ Shift: "→") cho cả đội thấy 3 giây (1 lần/giây).
- **Giao thức lên bản 5** (thêm `party`, `realm`, `ract`, `mark`; snapshot `me` có thêm cờ hồn ma; thực thể khe nứt).
- **Kiểm thử**: `server/tests/test_realm.py` (27 test, máy chủ trong tiến trình với đồng hồ giả: 3 bot đi bằng gói tin thật
  qua cả 5 câu đố + boss, và từng luật: lượt/ngày, cảnh giới, giờ mở, hàng chờ, khe nứt, giá của mỗi sai lầm, hồn ma, N của
  boss, rớt mạng, nhận thưởng một lần kể cả khi gọi đồng thời, ghép đồ bộ). `server/tests/test_realm_ws.py`: máy chủ thật +
  3 bot trên 3 kết nối WebSocket (`tools/realm_bots.py`) vượt Mặc Ảnh Động. `client/tests/test_realm_flow.py`: game thật mở
  cổng, lập đội bằng bảng Tổ đội, vào bí cảnh cùng 2 bot rồi rời; 2 bot vượt nốt; rồi phát lại cả lượt chơi trên game để
  vẽ mọi phòng. Bot biết đáp án Vấn Đạo bằng cách đọc cơ sở dữ liệu (chỉ trong test).
- Test cũ cập nhật: số quái trong Yêu Quái Phổ (thêm 3 quái bí cảnh), phiên bản giao thức 5, Cần Thiên Tơ giờ báo
  `realm_too_low` thay vì `not_sold` với người chưa Trúc Cơ.

## Giai đoạn 10 — Phát hành

- **Exe một thư mục, không một file**: `tools/build_exe.py` mặc định build PyInstaller dạng thư mục
  (`dist/VuonChu/VuonChu.exe` + `_internal/`) rồi nén thành `VuonChu-<bản>-windows.zip` (~30 MB). Bản một file phải tự giải
  nén vào thư mục tạm mỗi lần mở (chậm vài giây) và bị phần mềm diệt virus báo nhầm nhiều hơn hẳn; `--onefile` vẫn có cho ai
  cần. Đặc tả gọi tên `VuonChu.exe` — vẫn đúng tên đó, chỉ nằm trong thư mục. `client/main.py` dùng import tương đối nên
  PyInstaller không lần theo được từ chính file đó (một lần build ra exe thiếu cả package `client` mà vẫn "thành công");
  build dùng một file khởi động hai dòng `from client.main import main`. Vì lỗi kiểu này im lặng, build **tự chạy exe** với
  `--smoke-test <mọi module>`: nạp mọi module của game, font và bản đồ từ trong gói, lỗi thì build báo hỏng.
  Biểu tượng exe vẽ bằng chính code sprite (cây chữ huyền thoại chín trên nền giấy dó), lưu dạng PNG-trong-ICO.
- **Exe chạy không có cửa sổ lệnh**, nên lỗi làm game tắt được ghi vào `vuonchu_loi.txt` cạnh exe và báo bằng hộp thoại
  Windows. `config.json`/`session.json` nằm cạnh exe như đặc tả; nếu thư mục không ghi được (giải nén vào Program Files)
  thì ghi vào `%LOCALAPPDATA%\KhuVuonTuTien`, nhưng vẫn đọc `config.json` đi kèm exe nếu người chơi chưa lưu cái riêng.
- **`server_list_url` là nguồn sự thật**, trừ khi người chơi tự gõ máy chủ trong Cài đặt (`session.json → server_manual`).
  Trước đây game bỏ qua danh sách hễ đã từng đăng nhập (đã lưu `server_url`), nên với quick tunnel (địa chỉ đổi mỗi lần)
  người cũ kẹt ở địa chỉ chết. Giờ: địa chỉ đã lưu còn trong danh sách thì giữ (danh sách có nhiều máy), không còn thì
  chuyển sang mục đầu tiên. Xóa trống ô Máy chủ rồi Lưu để quay về danh sách. Địa chỉ dán vào được chuẩn hóa (thêm
  `http://`, bỏ `/server/info` và `/` cuối), nên dán cả link trang trạng thái cũng được.
- **Kiểm tra phiên bản khi mở game** (mục 15.5): menu gọi `/server/info`; lệch giao thức thì không cho Bắt đầu, báo cập nhật
  kèm `client_download_url`. Exe mới hơn (`LATEST_CLIENT_VERSION`) chỉ nhắc nhẹ, vẫn chơi được. Menu và màn đăng nhập hiện
  thông báo bảo trì / thông báo chung. Trước giai đoạn này `check_version` có sẵn nhưng không nơi nào gọi.
- **`/server/info` vừa là API vừa là trang**: game nhận JSON; trình duyệt (`Accept: text/html`) nhận trang trạng thái nhỏ
  (online, phiên bản, đã chạy bao lâu, thông báo, nút tải game) — một địa chỉ để gửi cho người chơi. `/` chuyển về đó.
  `/healthz` riêng cho kiểm tra sống, không chạm DB, để Render gọi liên tục mà Neon vẫn ngủ được.
- **Lệnh admin qua chat** (`app/admin.py`): dòng bắt đầu `/admin` bị chặn ở `ChatService` trước mọi kiểm tra khác, không bao
  giờ phát ra kênh nào, kể cả khi gõ sai hay không có quyền. Quyền đọc lại từ DB mỗi lệnh (thu hồi quyền có hiệu lực ngay
  với kết nối đang mở). Tên người chơi có dấu cách nên `<tên> <thời hạn> [lý do]` tách ở token đầu tiên đọc được là thời
  hạn; `@username` để chỉ đích danh tài khoản. SQLite chỉ hạ chữ hoa ASCII nên tên có chữ hoa tiếng Việt được so bằng
  `casefold()` trong Python khi truy vấn không ra. Không dùng `ilike` cho username (dấu `_` là ký tự đại diện của LIKE).
  Có tên lệnh tiếng Việt không dấu (`camchat`, `khoa`, `thongbao`...). Quản trị viên trong game không tác động được lên mình
  hay quản trị viên khác; dòng lệnh máy chủ (`python -m app.admin_cli`) thì được — đó là chủ máy chủ.
- **Khóa/cấm chat dùng cột có sẵn** (`banned_until`, `chat_banned_until`, từ giai đoạn 1) — chặn ở `/auth/login`, mọi
  request có token và WebSocket. Khóa thì đá kết nối ngay (mã đóng 4010; 4005 đã là `timeout`). Mọi lệnh làm thay đổi gì đều
  ghi bảng mới `admin_actions` (migration 0008), lưu cả tên để còn đọc được khi tài khoản đã xóa. Thời gian trong lệnh admin
  hiển thị theo giờ Việt Nam.
- **Không có gì tự cấm**: đặc tả 17 yêu cầu đánh dấu tài khoản trả lời bất thường; cột `suspicious_flag` có từ giai đoạn 1
  nhưng chưa nơi nào ghi. Giờ mỗi câu trả lời cập nhật `flags.fast_streak` (đúng và nhanh hơn `fast_ms` thì +1, ngược lại về
  0; chỉ ghi khi đổi); chạm `streak` (200 câu dưới 500 ms, `balance/quiz.json → bot_watch`) thì đánh dấu. Thời gian đo ở
  máy chủ (gồm cả mạng), nên người thật gần như không thể chạm ngưỡng. `/admin flagged`, `/admin who`, `/admin unflag`.
- **`ADMIN_USERNAMES`**: Render free không có shell để chạy lệnh cấp quyền, nên tên trong biến này được cấp `is_admin` lúc
  khởi động và lúc đăng ký. Bỏ tên khỏi biến không thu hồi (tránh mất quyền vì gõ nhầm biến); thu hồi bằng `admin_cli revoke`.
- **`TIME_SCALE` đổi lúc chạy** (`/admin timescale`) chỉ khi `ENV=dev`, giống ràng buộc lúc khởi động. Mọi nơi đọc
  `settings.time_scale` tại thời điểm dùng nên đổi là có hiệu lực ngay; mất khi khởi động lại. Thông báo bảo trì/thông báo
  chung cũng chỉ ở trong RAM (`server_state.py`) — không cần bảng mới cho hai chuỗi.
- **Chuỗi kết nối của Neon**: Neon đưa `?sslmode=require&channel_binding=require`, asyncpg không hiểu cả hai (nó dùng
  `ssl=`), nên `normalize_database_url` dịch/bỏ chúng; host `-pooler` (PgBouncer chế độ transaction) thì tắt bộ đệm
  prepared statement của asyncpg. Khuyên dùng kết nối trực tiếp.
- **Để Neon ngủ**: pool SQLAlchemy giữ kết nối mở mãi, làm Neon không tạm dừng và tính giờ cả khi không ai chơi.
  `DB_IDLE_CLOSE_SECONDS` (mặc định 300, Render 240): không có truy vấn trong khoảng đó thì `engine.dispose()` đóng hết;
  truy vấn sau tự kết nối lại. Không đổi sang `NullPool` vì mỗi request phải bắt tay TLS với Neon lại từ đầu.
- **`ENV=prod` bắt buộc `JWT_SECRET` ≥ 32 ký tự**: trước chỉ chặn đúng chuỗi mặc định, còn để trống (dòng `JWT_SECRET=`
  trong file .env mẫu) thì lọt.
- **Docker**: `python:3.12-slim` (đa kiến trúc), chạy bằng người dùng thường, cổng lấy từ `PORT` (Render tự đặt).
  Không bật `--proxy-headers` của uvicorn: IP người chơi sau proxy do ứng dụng tự đọc khi `TRUST_PROXY_HEADERS=1`, để chỉ có
  một chỗ quyết định có tin header hay không. `docker-compose.yml` dùng cho cả A và C: Caddy nằm trong profile `https`; cổng
  8000 chỉ mở cho `127.0.0.1`. Mọi image (python, postgres:16-alpine, caddy:2-alpine) có bản arm64.
  `.github/workflows/docker.yml` build `linux/amd64,linux/arm64` bằng buildx + QEMU lên GHCR.
  **Chưa build thử được image trên máy làm giai đoạn này** (Docker Desktop không khởi động); file Docker được test đọc và đối
  chiếu (`server/tests/test_release.py`), còn build thật chạy trên GitHub Actions.
- **Sao lưu**: `tools/backup_db.sh` (POSIX sh, chạy trong container `postgres:16-alpine` có sẵn `pg_dump`; dịch vụ `backup`
  của compose sao lưu khi khởi động rồi mỗi ngày 20:00 UTC = 3:00 sáng VN) và `tools/backup_db.py` (Windows/SQLite dùng API
  backup của SQLite nên sao lưu được khi máy chủ đang chạy; PostgreSQL thì gọi `pg_dump`). Cùng tên file
  `khuvuon-YYYYmmdd-HHMMSS.*`, sắp theo tên là theo thời gian, giữ 7. Đường dẫn có dấu cách (như "khu vườn tu tiên") được
  xử lý. `pg_dump` ghi ra file tạm rồi mới nén (sh POSIX không có `pipefail`, ống `pg_dump | gzip` sẽ nuốt lỗi).
- **`ALLOW_UNREVIEWED=1` trong file mẫu triển khai**: 44 câu luyện tập chưa câu nào được đánh dấu đã duyệt, mà `ENV=prod` mặc
  định tắt câu chưa duyệt — các dạng câu dùng câu ví dụ sẽ không có câu nào. Ghi chú trong `.env.example`: đặt 0 khi đã duyệt.
- **GitHub Actions**: đẩy tag `v*` → build exe trên Windows (kèm chạy thử), đính zip vào Release; build image đa kiến trúc;
  test máy chủ + client mỗi lần đẩy. Địa chỉ máy chủ của exe lấy từ biến repo `SERVER_URL`/`SERVER_LIST_URL`.
- **Phiên bản 1.0.0** (`GAME_VERSION` ở cả hai phía). Giao thức vẫn **5**: chỉ thêm gói `admin` và trường `notice.kind`,
  client cũ bỏ qua được, không cần buộc mọi người cập nhật.
- **Tiêu chí "triển khai thật, hai người trên hai mạng tải exe từ GitHub Releases"** cần tài khoản Oracle/Render/Neon/GitHub
  của chủ dự án nên không làm thay được; `docs/DEPLOY.md` mục G là danh sách kiểm tra cho lần đó. Phần đã làm ở đây: build
  exe thật, exe tự chạy thử, exe chạy thật nối vào máy chủ cục bộ (gọi `/server/info`), và test WebSocket thật cho lệnh admin.

## Bản 1.1 — Thế giới LAN kiểu Minecraft, tài khoản Firebase

Yêu cầu: không thuê máy chủ; dữ liệu lưu trên máy người mở thế giới, người khác cùng mạng LAN vào chơi; tài khoản đăng ký
một lần, lần sau chỉ đăng nhập, dùng Firebase (dự án và API key do chủ dự án tạo).

- **Không viết lại game**: máy chủ FastAPI có sẵn chính là "thế giới". Game mở một thế giới bằng cách chạy máy chủ đó
  trên máy người chơi, như một **tiến trình con** (`VuonChu.exe --host-server`, hoặc `python -m client.main --host-server`
  khi chạy từ mã nguồn). Tiến trình riêng thay vì một luồng: vòng tick 20 Hz của thế giới không tranh GIL với vòng vẽ 60
  khung hình, mỗi lần mở thế giới có cấu hình riêng (`settings` của máy chủ đọc biến môi trường lúc import), và lỗi của máy
  chủ không làm đổ game. Mọi luật chống gian lận (máy chủ có thẩm quyền, câu hỏi chấm ở máy chủ...) giữ nguyên — kể cả người
  chủ cũng chơi qua máy chủ của mình như người khác. Người chủ đương nhiên sửa được file dữ liệu của chính mình; đó là bản
  chất của kiểu Minecraft.
- **Tắt êm**: game giữ stdin của tiến trình con; ghi `stop` (hoặc game chết và stdin đóng) thì uvicorn dừng bình thường,
  `world.stop()` lưu vị trí mọi người. Không dùng `TerminateProcess`/`os.kill` (trên Windows `os.kill(pid, 0)` còn giết
  luôn tiến trình). Có `kill` dự phòng sau 10 giây.
- **Thế giới là một thư mục** `worlds/<slug>/` trong `data_dir()` (cạnh exe; `client/worlds/` khi chạy từ mã nguồn):
  `world.json` (tên, ngày, khóa ký token riêng của thế giới — để token còn hiệu lực sau khi mở lại), `world.db` (SQLite),
  `server.log`. Nhiều thế giới, tạo/chọn trong game; chép thư mục là sao lưu. SQLite vì không cần cài gì; máy chủ chạy
  `ENV=prod` (khóa token bắt buộc, không `TIME_SCALE`) với `ALLOW_UNREVIEWED=1` như file mẫu triển khai.
- **Tài khoản Firebase, dữ liệu theo thế giới**: game đăng nhập Firebase Authentication bằng REST (email + mật khẩu —
  đăng nhập Google trong một game pygame cần luồng OAuth qua trình duyệt, phức tạp hơn nhiều mà không thêm gì cho việc
  chơi LAN). Refresh token lưu trong `session.json` nên lần sau không phải gõ; ID token (1 giờ) được làm mới khi còn dưới 5
  phút. Khi vào một thế giới, game gửi ID token tới `POST /auth/firebase` của thế giới đó; thế giới hỏi Firebase
  (`accounts:lookup`) xem token của ai — chỉ cần API key công khai, không cần service account, nên máy ai cũng làm chủ được
  — rồi tìm/tạo tài khoản cục bộ gắn `firebase_uid` (migration 0009) và trả token phiên của chính nó. Mọi API cũ dùng
  token đó như trước, không đổi gì. Giống Minecraft: một danh tính, mỗi thế giới một nhân vật và một túi đồ riêng.
- **Tên đăng nhập cục bộ** sinh từ phần trước `@` của email (`ban.be@…` → `ban_be`, trùng thì `ban_be2`), vì cột
  `username` là khóa của nhiều thứ (admin, báo cáo). Mật khẩu cục bộ là chuỗi không băm được (`!firebase`) nên tài khoản
  Firebase không bao giờ đăng nhập được bằng `/auth/login`. Thế giới mở từ game đặt `LOCAL_ACCOUNTS=0`: `/auth/register` và
  `/auth/login` trả `local_off`, mọi người trong thế giới đều là tài khoản Firebase.
- **Người mở thế giới là quản trị viên** (`HOST_FIREBASE_UID` = uid của người chủ), dùng được `/admin ...` của giai đoạn 10.
- **Tác giả game là quản trị viên ở mọi thế giới** (1.1.2): tài khoản Firebase có email trong `OWNER_EMAILS`
  (`server/app/config.py`, tài khoản phongfoxyd) hoặc `ADMIN_EMAILS` được `is_admin` khi vào bất kỳ thế giới nào. Khớp theo
  email chứ không theo tên đăng nhập: tên trong thế giới lấy từ phần trước `@` nên ai cũng chiếm được, còn email thì Firebase
  giữ duy nhất. Vì thế thế giới mở từ game đặt `ADMIN_USERNAMES=""` (không lấy từ `server/.env` của máy chủ).
- **Tìm thế giới trên LAN**: thế giới phát gói UDP broadcast nhỏ (`{"g": "khuvuon-lan", v, name, host, port, online}`) tới
  `255.255.255.255:47654` mỗi 1,5 giây (và tới `127.0.0.1` để máy không có mạng vẫn thấy chính mình); tab *Tham gia mạng LAN*
  nghe cổng đó (`SO_REUSEADDR`, nhiều game cùng máy vẫn nghe được) và quên thế giới im lặng quá 5 giây. Không dùng
  multicast/mDNS: broadcast đủ cho mạng nhà, không cần thư viện. Router chặn broadcast (một số Wi-Fi khách) thì vẫn gõ
  địa chỉ được; địa chỉ LAN của người chủ hiện trong chat và Cài đặt. Cổng TCP bắt đầu từ `host_port` (8000), bận thì thử
  cổng sau.
- **Broadcast ra từng card mạng** (sửa lỗi 1.1.0): Windows gửi `255.255.255.255` từ socket không gắn địa chỉ ra **một** card
  duy nhất — card có metric thấp nhất, thường là card ảo (WSL/Hyper-V/VPN) — nên bạn bè trên Wi-Fi thật không thấy thế
  giới. Thế giới mở một socket gắn vào từng địa chỉ IPv4 của máy (bỏ 127.x, 169.254.x; làm mới mỗi 30 giây) và gửi qua
  từng cái. Máy có cả Wi-Fi lẫn dây được nghe từ hai IP: tab LAN gộp theo (tên, chủ, cổng), chọn cố định một IP, ưu tiên
  `192.168.*` rồi `10.*` (dải `172.16–31` thường là card ảo).
- **Kiểm tra phiên bản khi vào thế giới** (`/server/info` có thêm `auth` và `local_accounts`): khác giao thức thì báo hai
  máy cần cùng bản game; địa chỉ là máy chủ riêng (không phải thế giới LAN) thì báo rõ. Bản game 1.1.0 (giao thức vẫn 5).
- **Cần Internet lúc đăng nhập** (Firebase), cả ở máy người vào lẫn máy người chủ (để hỏi Firebase). Chơi thì chỉ cần LAN.
  Chế độ hoàn toàn offline không làm: không có cách nào kiểm tra danh tính mà không có máy chủ chung.
- **Chế độ máy chủ riêng vẫn còn**: `firebase_api_key` rỗng trong `config.json` → game quay về màn đăng nhập tên + mật khẩu
  với một `server_url` cố định (giai đoạn 10, `docs/DEPLOY.md`). Test client cũ dựng `Config(...)` trong code (không có
  key) nên vẫn chạy luồng đó. Khi chạy từ mã nguồn mà chưa có `client/config.json`, game đọc `client/config.example.json`
  (có key của dự án).
- **Firebase Auth Emulator**: cả máy chủ lẫn game đọc `FIREBASE_AUTH_EMULATOR_HOST` (quy ước của Firebase), dùng cho test
  trọn vòng `client/tests/test_lan_worlds.py`: game mở thế giới thật (tiến trình con), thế giới phát tín hiệu LAN và được
  nghe thấy, người chủ vào bằng token qua một "emulator" giả, được làm quản trị viên, rồi tắt thế giới êm (mã thoát 0).
- **Exe mang theo máy chủ**: `build_exe.py` thêm package `app` của máy chủ, `data/`, `maps/`, `alembic/` (migration được
  đọc như file), `uvicorn`/`alembic` (nạp module theo tên lúc chạy), bỏ những gói kéo theo vô ích (jedi, PIL,
  cryptography... ≈ 45 MB). Chạy thử sau build có thêm bước mở một thế giới bằng chính exe (`--host-server`), chờ
  `/server/info` báo `auth: firebase`, gửi `stop` và kiểm tra thoát 0, `world.db` được tạo. Zip ≈ 36 MB.
- **Dự án Firebase của chủ dự án chưa bật Authentication** lúc làm bản này: mọi lời gọi trả `CONFIGURATION_NOT_FOUND`
  (key đúng, chưa bấm *Get started* / chưa bật Email/Password). Game hiện thông báo tiếng Việt chỉ đúng bước cần làm.
- **Báo bản mới qua GitHub Releases** (1.1.1): thế giới LAN không có máy chủ chung để hỏi `latest_client_version`, nên
  game hỏi thẳng `GET api.github.com/repos/<update_repo>/releases/latest` lúc mở (không cần token; giới hạn 60 lần/giờ mỗi
  IP là quá đủ cho một lần mỗi lần mở game). Chạy trên luồng riêng bằng `httpx` chứ không qua `Api`: lỗi mạng ở đó sẽ bật
  thanh "mất kết nối" dù chơi LAN không cần Internet. Bỏ qua draft/prerelease; so phiên bản theo số (`1.10.0` > `1.9.0`).
  Nút Tải về mở thẳng link file zip của release (không có zip thì trang release). `update_repo` do `tools/build_exe.py`
  ghi vào `config.json` (lấy từ `--update-repo`, mặc định là remote `origin`); workflow release truyền
  `github.repository`. Không tự cài đè: exe đang chạy không ghi đè được chính nó trên Windows, và giải nén đè thủ công
  giữ nguyên `worlds/` + `session.json` vì chúng không có trong zip.
- **MessageBox tự đo chiều cao chữ** (sửa lỗi): trước tính mỗi dòng 10 đơn vị trong khi chữ cỡ 8 cao ~13,4 (kể cả giãn
  dòng 1,15), nên thông báo dài từ 4–5 dòng trở lên bị hai nút đè lên chữ.

## Nhánh `toan-tu-tien` — M2: vòng câu hỏi toán

- **Dùng chung dịch vụ câu hỏi cũ** (`learning/quiz.py`) thay vì viết một vòng riêng: câu toán là một `QuizSession`
  `context = "math"`, nên đếm giờ, chống trả lời hai lần, cờ nghi bot và nhiệm vụ "trả lời câu hỏi" chạy y như cũ.
  `quiz.py` có thêm ba chỗ đăng ký: `register_grader` (chấm theo dạng câu), `register_xp_rule` (Tu Vi theo bậc thay cho
  bảng `xp_per_correct` theo ngữ cảnh) và người nghe Tu Vi thực nhận (đã nhân đan dược) để ghi vào buổi luyện.
- **`quiz_sessions.word_id` → `item_id`, bỏ khóa ngoại tới `words`** (migration 0010), `qtype` dài 20 ký tự. Câu từ vựng
  vẫn ghi mã chữ vào đó, câu toán ghi mã câu. Trên SQLite bảng được dựng lại từ một mô tả viết tay trong migration:
  khóa ngoại do 0001 tạo không có tên, và cách "đặt tên theo quy ước rồi drop" của Alembic không tìm ra nó ở
  Alembic 1.20/SQLAlchemy 2.1. PostgreSQL thì tìm tên khóa bằng inspector rồi `DROP CONSTRAINT`; **đường PostgreSQL
  chưa được chạy thử** (máy phát triển chỉ có SQLite). Hạ cấp xóa các phiên câu hỏi toán (mã của chúng không phải chữ).
- **Chưa gỡ phần từ vựng.** `words` còn là khóa ngoại của `plots`, `seeds`, `collection`, `fruits`; gỡ dần theo từng
  mốc, bảng `words` gỡ sau cùng.
- **Bậc của một câu = min(bậc của buổi luyện, bậc đã mở của vi kỹ năng)** (`learning/math_adaptive.py`). Luật 2: 2 câu
  đúng liền thì buổi luyện lên một bậc, 2 câu sai liền thì xuống một bậc, không ra khỏi khoảng bậc của tầng; chuỗi đã
  dùng để đổi bậc thì tính lại từ đầu. Luật 3: bậc N của một vi kỹ năng chỉ mở khi có ít nhất 3 câu đúng trong
  **5 câu gần nhất** ở bậc N-1 của chính vi kỹ năng đó (`tier_unlock.window`; con số 5 là giá trị tạm, kế hoạch chỉ nói
  "gần đây"). Bậc thấp nhất của tầng luôn mở.
- **Tu Vi theo bậc** `xp_per_correct.by_tier = [3, 5, 8, 12, 18]` trong `balance/math.json` (giá trị tạm, chờ chủ dự án
  quyết). Vẫn cộng vào thanh Tu Vi cũ; việc 4 bí cảnh x 9 tầng gắn thế nào với Luyện Khí tầng 1-9 để lại cho mốc cổng
  thông thạo (M5).
- **Chọn câu**: rút một vi kỹ năng của tầng rồi một câu của nó ở bậc được phép; câu có dấu vân tay nằm trong 50 câu trả
  lời gần nhất bị bỏ qua khi còn câu khác, hết câu mới thì câu hỏi lâu nhất quay lại. Dấu vân tay = vi kỹ năng + mẫu +
  bộ số (câu viết tay là mẫu của chính nó). Tiền điều kiện giữa các vi kỹ năng chưa chặn gì: cần "thông thạo", thuộc M5.
- **Ba dạng câu chơi được ở M2**: Đúng/Sai, trắc nghiệm một đáp án, điền số. Điền số so bằng phân số chính xác với sai
  số `numeric_tolerance`; dấu phẩy là dấu ngăn các số nên số thập phân viết bằng dấu chấm. Các dạng còn lại trong
  `balance/math.json` có giờ nhưng chưa có câu và chưa có màn hình.
- **Ngân hàng câu M2 chỉ là hạt giống**: 27 câu viết tay cho tầng 1 (mỗi vi kỹ năng ít nhất 2 câu mỗi bậc), tất cả
  `reviewed: false`, nên máy chủ `ALLOW_UNREVIEWED=0` không hỏi câu nào. Bộ sinh câu và ngân hàng tầng 1-3 là việc của M3;
  "câu song song sau khi sai" (luật 6) cũng cần bộ sinh nên M2 mới hiện lời giải từng bước.
- **Hết giờ ở máy khách**: thẻ câu hỏi tự gửi `{"timed_out": true}` khi đồng hồ của nó về 0 (máy chủ còn 1,5 giây bù
  mạng nên tự nó chưa coi là hết giờ); máy chủ ghi `math_answers.timed_out` trong cả hai trường hợp.
- **Lối vào**: nút "Toán" (phím M) trên thanh dưới của Động Phủ. Vòng luyện là một màn phủ lên Động Phủ nên không có
  thế giới nào chạy phía sau trong lúc câu hỏi mở; "thế giới dừng khi mở câu hỏi" sẽ cần xử lý khi câu toán vào chiến
  đấu (M7).

## Nhánh `toan-tu-tien` — M3: ngân hàng câu tầng 1-3, bộ sinh câu, chống lặp

- **Bộ sinh câu = dữ liệu + hàm.** Mỗi bộ có một dòng trong `data/math/items/<bí cảnh>.json` (`generators`: mã, vi kỹ
  năng, bậc, dạng, `reviewed`) và một hàm cùng mã trong `learning/math_gen/` (`@generator`). Dữ liệu giữ phần người
  duyệt cần sửa (bậc, cờ duyệt); phần sinh số thì phải là mã. Kiểm tra hai chiều: dòng không có hàm và hàm không có
  dòng đều là lỗi. Hàm chỉ dùng `rng` được truyền vào nên cùng hạt giống cho cùng câu hỏi.
- **Tính lại đáp án bằng SymPy, tách khỏi game.** Hàm sinh câu tự tính đáp án bằng số nguyên/phân số của thư viện
  chuẩn; `tools/math_verify.py` tính lại từ bộ số đã rút (`Draw.params`) bằng SymPy theo đường khác (tập hợp, số
  phức, ma trận của SymPy; giải phương trình thay vì chuyển vế bằng tay). SymPy chỉ nằm trong
  `server/requirements-dev.txt`: máy chủ, Docker và exe không phải mang theo. Không dùng NumPy: mọi đáp án ở tầng 1-3
  là số hữu tỉ, SymPy tính đúng tuyệt đối. CI cài bản dev và chạy `tools/check_all.py`.
- **`check_all.py` có 4 kiểm tra**: lộ trình; ngân hàng câu (hợp lệ, không có hai câu viết tay chỉ khác số, đủ chỉ
  tiêu); bộ sinh câu (200 lần rút đều là câu hợp lệ, cùng hạt giống cùng câu, đủ đa dạng); đáp án sinh ra (SymPy).
- **Chỉ tiêu ngân hàng** (`bank_targets`): tầng nào có câu thì phải có ít nhất 30 dạng câu, 3 bộ sinh câu và 2 dạng
  cho mỗi (vi kỹ năng, bậc); 200 lần rút của một bộ phải cho ít nhất 8 câu khác nhau. Tầng chưa viết không bị tính.
  Hiện có: tầng 1 = 27 câu viết tay + 13 bộ, tầng 2 = 21 + 12, tầng 3 = 23 + 12.
- **Phát hiện câu gần trùng**: hai câu viết tay của cùng vi kỹ năng giống nhau từ 95% trở lên sau khi thay mọi con số
  bằng `#` là lỗi (cùng một câu, khác số là việc của bộ sinh câu). Ngưỡng 90% bắt nhầm "A giao B" với "hiệu A \ B".
- **Ma trận là hình, không phải chữ.** Câu hỏi gửi `prompt.matrices`, game vẽ ngoặc vuông và các phần tử; lời đề viết
  "ma trận A như hình". Phần tử là số, phân số hoặc một chữ thường (ẩn `x`, `y`). Vectơ vẫn viết trong câu: `(1, -2, 0)`.
  Số phức viết `3 - 2i`; đáp án số phức nhập hai số "phần thực, phần ảo".
- **Chống lặp** (`systems/math_practice.choose_item`), theo thứ tự ưu tiên: câu có dấu vân tay ngoài 50 câu trả lời gần
  nhất *và* thuộc dạng câu không nằm trong 4 câu gần nhất (`template_cooldown`); câu ngoài 50 câu gần nhất; một bộ sinh
  câu (bộ số đành lặp); câu viết tay hỏi lâu nhất. Bộ sinh câu rút tối đa 30 lần để tìm bộ số chưa gặp.
- **Câu song song, "tâm ma" (luật 6)**: mỗi câu sai (kể cả hết giờ) ghi một dòng `math_retries` (migration 0011). Sau
  khi người chơi trả lời thêm `parallel_question.after_answers` = 1 câu khác, ý đó quay lại: bộ sinh câu thì rút bộ số
  mới (không bao giờ đúng câu vừa sai); câu viết tay thì lấy một dạng khác cùng vi kỹ năng và cùng bậc, ưu tiên bộ
  sinh câu, chỉ lặp lại chính nó khi không còn dạng nào. Trả lời đúng thì xóa; sai thì chờ tiếp. Hàng chờ theo người
  chơi và tầng, sống qua các buổi luyện, tối đa `max_open` = 5 (ý cũ nhất bị bỏ). Con số 1 và 5 là giá trị tạm.
  Câu song song giữ bậc của câu đã sai, kể cả khi buổi luyện đã đổi bậc.
- **Bảng duyệt**: `python tools/math_review.py` ghi `tools/reports/math_review_<bí cảnh>.md` (mọi câu viết tay và 3
  mẫu của mỗi bộ sinh câu, kèm đáp án và lời giải). Tất cả 108 dạng câu hiện `reviewed: false`.

## Nhánh `toan-tu-tien` — M4: Tàng Thư Các, công thức dựng sẵn

- **Công thức là ảnh dựng sẵn, không dựng lúc chơi.** `$$...$$` trong bài đọc được MathJax đổi thành SVG
  (`fontCache: 'none'` nên mọi nét chữ là đường vẽ, không cần phông), rồi resvg đổi thành PNG nền trong suốt
  (`tools/formulas/render.mjs`, chạy qua `tools/build_formulas.py`). Ảnh đi kèm game trong
  `client/assets/formulas/`, nên lúc chơi không cần Node, không cần mạng, không cần phông toán. Node chỉ cần
  khi thêm hoặc sửa công thức. Tên ảnh là băm của chính công thức, nên công thức không đổi thì không dựng lại,
  và không bao giờ có chuyện ảnh lệch với công thức.
- **Không dùng matplotlib** như kế hoạch đã ghi (mathtext không vẽ được môi trường ma trận), cũng không dùng
  Pillow: máy không có sẵn và không cần. Chỗ duy nhất cần xử lý ảnh lúc chơi là thu phóng, pygame làm được.
- **Ma trận thì game tự vẽ**, không thành ảnh: nó chỉ là các số trong ngoặc vuông, nét luôn sắc ở mọi cỡ cửa
  sổ, và các số còn thay đổi theo từng câu hỏi (M3). Mã vẽ dùng chung giữa thẻ câu hỏi và trang sách
  (`client/ui/mathdraw.py`).
- **Công thức trong dòng vẫn viết ASCII** (A^T, !=, A \ B) đúng như kế hoạch; chỉ công thức đứng riêng mới
  thành ảnh. Nhờ vậy câu hỏi, lời giải và phần lớn bài đọc vẫn là chữ thật, tìm kiếm được, đọc được bằng
  phông của game.
- **Mỗi công thức có sẵn dạng chữ thường (`alt`)** do `tex_to_ascii` sinh ra từ chính công thức đó, nên không
  có hai nguồn sự thật. Lệnh TeX nào chưa có cách viết bằng chữ thì `tools/check_all.py` báo lỗi ngay, không
  đợi đến lúc thiếu ảnh mới lộ. Game hiện `alt` khi ảnh thiếu, nên trang sách không bao giờ trống.
- **Một bài đọc cho một tầng**, chia thành đúng một mục `##` cho mỗi vi kỹ năng, theo thứ tự `skills` trong
  front matter. Nhờ vậy câu hỏi dẫn thẳng tới đúng mục (`question.math.doc.block`) mà không cần mỗi vi kỹ
  năng một file. Kiểm tra bắt buộc: tầng nào có câu hỏi thì phải có bài đọc, và bài đọc phải phủ đủ vi kỹ năng
  của tầng.
- **Markdown rút gọn, không có thư viện Markdown nào.** Chỉ 8 loại khối (mục, tiêu đề nhỏ, đoạn văn, gạch đầu
  dòng, các bước, công thức, ma trận, lời nhắc). Máy chủ tách sẵn thành khối rồi mới gửi; game không bao giờ
  phải hiểu Markdown. Không có in đậm, in nghiêng hay bảng: `ui.text` của game không vẽ được chữ hỗn hợp kiểu.
- **Kiểm tra phông chữ** (`check_all.py`): gom mọi chuỗi game hiện ra — tên tầng, vi kỹ năng, mọi câu hỏi viết
  tay, 5 lần rút của mỗi bộ sinh câu, mọi bài đọc, và toàn bộ `client/strings_vi.py` — rồi soát từng ký tự với
  bảng mã của hai phông đi kèm, theo đúng cách `client/engine/text.py` chọn phông. Đây là lưới an toàn cho cả
  phần chữ Hán cũ, không riêng phần toán.
- **So ảnh màn hình**: kế hoạch ghi việc này trong `check_all.py`, nhưng ảnh chuẩn dễ lệch theo máy và theo
  phiên bản SDL. Thay vào đó `client/tests/test_math_library_flow.py` dựng và vẽ **mọi trang của mọi bài đọc**
  không cần màn hình, rồi kiểm tra: không dòng nào, ảnh nào, ma trận nào rộng quá khổ trang; mọi ảnh công thức
  đều có thật (không trang nào phải lùi về chữ thay thế); cuộn được từ đầu tới cuối và nhảy mục đúng chỗ.
  Ảnh chụp vẫn được lưu để người xem (`python -m client.tests.test_math_library_flow <thư mục>`).
- **Cỡ chữ công thức**: 1 ex = 4,5 đơn vị nền, ảnh dựng ở 3 lần cỡ đó. Cửa sổ thường ở scale 3 nên ảnh vẽ
  đúng 1:1, không mờ. Giới hạn 380 x 90 đơn vị nền cho vừa trang đọc; `check_all.py` chặn công thức quá khổ.

## Nhánh `toan-tu-tien` — M5: cổng thuần thục, Thiên kiếp nhỏ, ôn xoắn ốc

- **"Bậc hiện tại" của cổng thuần thục = bậc cao nhất của tầng.** Kế hoạch (luật 3a) viết "mỗi vi kỹ năng đã
  đúng >= 80% trong 5 câu gần nhất ở bậc hiện tại". Bậc mà một vi kỹ năng *đang* được hỏi chính là bậc cao
  nhất đang mở của nó (luật 4), nên cổng đòi thêm: vi kỹ năng phải đã mở tới bậc cao nhất của tầng. Nếu
  không, người chơi có thể rời tầng mà chưa từng chạm câu khó nhất của tầng ấy.
- **Phải đủ 5 câu mới xét**, không chỉ xét tỉ lệ: "5 câu gần nhất" mà mới có 4 câu thì chưa có gì để xét. Nhờ
  vậy bảng tiến độ của cổng luôn đọc được: "đúng 4/5 câu gần nhất ở bậc 2".
- **Thiên kiếp nhỏ không có đồng hồ riêng.** Bảng 3.4 chỉ cho "Thiên kiếp (tổng hợp)" 8 và 12 phút ở bậc 4-5,
  tức là bài tổng hợp lúc độ kiếp lên cảnh giới (làm sau). Thiên kiếp nhỏ của tầng là **một chuỗi câu hỏi**,
  mỗi câu giữ nguyên thời gian của loại câu và bậc của nó. Không phải viết thêm đồng hồ cho cả bài, và tầng
  thấp (bậc 1-3, chỗ bảng 3.4 để trống) cũng chạy được.
- **Mỗi vi kỹ năng một câu, được sai một câu** (`mastery_gate.trial`: `questions_per_skill: 1`, `max_wrong: 1`).
  Hai con số này tôi tự chọn, kế hoạch không ghi — tầng nhỏ nhất có 3 vi kỹ năng nên "được sai 1" vẫn là 2/3
  đúng. **Thi trượt dừng ngay** khi đã sai quá số cho phép: không bắt ai làm nốt một bài đã hỏng.
- **Thi lại được ngay** (luật 3: "không bị chặn cứng quá lâu"). Tầng đã qua vẫn thi lại được; qua một lần là
  qua.
- **Tầng đã qua = có một buổi `mode: "trial"` với `passed: true`**, chứ không phải một cột trạng thái riêng.
  Nhật ký là sự thật duy nhất, và bảng `math_runs` đã có sẵn mọi thứ cần đếm.
- **Ôn xoắn ốc đi theo `share_max`**: câu thứ n là câu ôn khi `review_asked < int(share_max * n)`, tức cứ 4
  câu có 1 câu ôn (0,25) — vẫn nằm trong khoảng 20-25% của kế hoạch. `share_min` không bị bỏ quên:
  `check_all.py` báo lỗi nếu nhịp số nguyên gần nhất rơi xuống dưới nó.
- **Lịch lặp lại ngắt quãng đọc thẳng từ nhật ký trả lời**, không có bảng lịch riêng: số câu đúng liên tiếp
  gần nhất của một vi kỹ năng quyết định thời gian chờ (1 → 3 → 7 → 14 ngày), một câu sai xoá chuỗi đó. Vi kỹ
  năng **vừa sai thì đến hạn ngay**, không chờ một ngày — đó chính là "tâm ma" cho các tầng dưới, và cũng là
  cách spaced repetition xử lí một lần quên.
- **Câu ôn lấy ở bậc cao nhất đang mở của vi kỹ năng ấy trên tầng của nó**, nên ôn lại không bao giờ dễ hơn
  lúc học, mà cũng không khó hơn những gì người chơi đã qua.
- **Câu sai trong lúc ôn thuộc về tầng của câu**, không thuộc buổi luyện: nó chờ buổi luyện của tầng ấy (quy
  tắc hàng đợi tâm ma theo tầng của M3). Trong buổi đang chơi nó vẫn quay lại rất nhanh, vì vừa sai thì đến
  hạn ngay và hàng đợi ôn xếp vi kỹ năng yếu lên trước.
- **Thiên kiếp nhỏ không trộn câu ôn và không có tâm ma**: bài thi của một tầng chỉ hỏi đúng tầng ấy.
- **Chưa làm ở mốc này**: bài kiểm tra đầu vào (luật 7) và "bậc thang" của câu bậc 5 (luật 8) — bậc 5 chỉ xuất
  hiện từ tầng 7 trở lên, mà tầng 7-9 chưa có câu hỏi nào. Cả hai chờ mốc M11.

## Nhánh `toan-tu-tien` — M6: bài tập lập trình

- **Bài làm chạy trên máy người học, máy chủ không chạy mã của ai cả.** Kế hoạch 5.2 đã ghi vậy, và đó cũng là
  lựa chọn an toàn nhất: máy chủ có thể cho bạn bè chơi chung, mà chạy mã lạ trên máy chủ thì phải có hộp cát
  thật sự. Ở đây máy chủ chỉ gửi *dữ liệu vào*; game chạy đúng một file Python mà chính người chơi viết, với
  dòng lệnh cố định (`-I -X utf8 <file>`), dữ liệu test chỉ đi vào qua stdin. Game không bao giờ chạy mã do
  máy chủ gửi xuống.
- **Chấm ở máy chủ.** Đáp án của test ẩn và lời giải mẫu không bao giờ rời máy chủ, nên muốn qua bài thì phải
  giải thật. Một máy khách bị sửa vẫn có thể khai gian verdict - đây là game tự học của một người, gian lận là
  gian lận với chính mình, mà đáp án thì vẫn giấu được.
- **`-I` nên `PYTHONIOENCODING` vô tác dụng**, vì vậy dùng `-X utf8`: in tiếng Việt chạy được trên mọi máy, kể
  cả Windows dùng bảng mã cũ. (Test `test_a_program_may_print_vietnamese_whatever_the_code_page_is` bắt lỗi
  này, lúc đầu tôi đặt biến môi trường và nó bị bỏ qua.)
- **CE lấy từ `compile()` trước khi chạy**, nên lỗi cú pháp không bao giờ phải chạy thử mới biết, và việc kiểm
  tra cú pháp không thực thi gì cả. RE và TLE là của chính lần chạy; AC/WA là so sánh.
- **Chạy tới test hỏng đầu tiên là dừng.** Các test sau đó ghi `-` (chưa chạy) chứ không ghi RE: nói đúng
  những gì đã xảy ra. Tỉ lệ test đạt vẫn tính được, nên hỏng ở test 3 vẫn được thưởng cho 2 test đầu.
- **Dấu cách không bao giờ quyết định đúng sai**: so sánh theo từng "từ" nên thừa dấu cách, thừa dòng trống,
  `\r\n` đều không sao. Bài chấm số thực so với sai số 1e-6, tương đối theo số lớn hơn (kế hoạch 5.2).
- **Mỗi bài có một lời giải mẫu nằm ở máy chủ** (`problems/<bí cảnh>/<id>.py`). `tools/check_all.py` chạy nó
  trên **mọi ví dụ và mọi test ẩn** và bắt buộc phải ra đúng đáp án đã ghi. Đáp án của ví dụ do tôi viết tay
  nên đây là phép thử thật cho lời giải mẫu; đáp án của test ẩn do `tools/build_problem_tests.py` sinh ra từ
  chính lời giải mẫu, nên phép thử này bắt được mọi trường hợp test hoặc lời giải bị sửa lệch nhau.
- **Thưởng theo tỉ lệ test đạt** (kế hoạch 5.2), nhưng **chỉ trả phần hơn** lần tốt nhất trước đó: nộp đi nộp
  lại một bài làm không cày được Tu Vi.
- **Bài làm là một file .py thật**, nằm cạnh `session.json` trong thư mục `bai_lam/`. Ai thích viết Python
  trong editor của mình thì cứ viết rồi bấm Chạy thử. Trình soạn trong game là loại nhỏ nhất dùng được (có số
  dòng, caret, cuộn, tự thụt lề như Python, Tab là 4 dấu cách), không tô màu cú pháp, không undo - file mới là
  chỗ ở thật của bài làm.
- **Bài tập theo đúng khoá tầng của M5**: tầng chưa mở thì không xem được đề, không nhận được test.
- **Chỉ Python.** Chương trình học là AI nên Python là ngôn ngữ của khoá; thêm ngôn ngữ khác sau cũng chỉ là
  thêm cách gọi trình biên dịch, phần chấm không đổi.

## Nhánh `toan-tu-tien` — dọn trước M7: test phải ổn định

- **Test không được đọc đồng hồ thật để quyết định đúng sai.** `client/tests/test_stage8_flow.py` tính thời
  điểm bấm phím từ `time` lúc ấy rồi giả định chỉ mất ~20 ms mới bấm được, trong khi driver phải chạy ba frame
  nữa mới gửi phím đi; vùng "perfect" của luyện đan chỉ rộng ±27 ms nên máy chậm một nhịp là trượt. Nay driver
  có `fixed_dt` (ghim dt của vòng lặp) và test đặt luôn `round_ms` ngay trước khi bấm, nên cây kim rơi đúng chỗ
  test muốn. Test còn **chặt hơn** trước: bắt buộc cả ba lần đều "perfect" (trước chỉ cần một lần).
- **Bot cũng phải "ping".** Máy chủ ngắt kết nối im lặng quá `idle_timeout_seconds` (45 s, `world.json`), còn
  `tools/realm_bots.py` chỉ gửi gói khi di chuyển: một bot đứng chờ cả đội làm xong phòng của họ thì không gửi
  gì cả. Máy chạy chậm (một lượt test dài gấp đôi) là có bot bị ngắt giữa bí cảnh, `realm_members.result` thành
  `disconnected` và `test_three_bots_clear_a_realm_over_websockets` hỏng. Nay bot đập nhịp 15 s đúng như máy
  khách thật (`client/net/ws_client.py`), có test giữ cho `HEARTBEAT * 2` luôn nhỏ hơn `idle_timeout_seconds`,
  và bot nhớ gói `kicked` để lần sau hỏng thì đọc ra được lý do ngay.
- **Chờ điều kiện, đừng chờ đồng hồ - và phải là đúng điều kiện.** Chỗ `asyncio.sleep(1.0)` "rương được trả
  ngay sau khi xong" đổi thành đợi gói loot của rương (hạn trên 30 s). Nhưng *rương về* không có nghĩa là
  *mọi phần thưởng đã ghi xong*: mỗi chặng được trả bằng một tác vụ nền riêng với một giao dịch riêng
  (`realm.py` `_pay_room` / `_pay_chest`), gói loot chỉ gửi sau khi giao dịch ấy commit, và thứ tự commit
  **không** theo thứ tự tạo tác vụ. Hậu quả: `test_three_bots_clear_a_realm_over_websockets` đọc
  `realm_claims` lúc chưa có `room5` (phòng trùm) rồi báo thiếu, trong khi cơ sở dữ liệu của chính lượt hỏng
  ấy xem lại thì đủ cả 7 dòng cho cả 3 bot - `room5` ghi trước `chest` 2,7 ms, chỉ là commit sau. Nay
  `run_team` đợi loot của **mọi** chặng người thắng được nhận (`stages_owed()`: mỗi phòng kể cả phòng trùm,
  cộng rương), đúng bằng tập mà người gọi sẽ đọc lại từ cơ sở dữ liệu, và có một test rẻ giữ lấy quy tắc đó.
  Chứng cứ: 8 lượt liên tiếp, 12/24 lượt-bot có rương về **trước** phòng trùm (đúng là cuộc đua ấy), và cả
  24 lượt-bot đều đủ dòng trong cơ sở dữ liệu.
- **Một cú click không chắc là một đòn đánh.** `engage()` của test đánh đúng một lần rồi đợi thẻ Vấn Đạo.
  Nhưng vũ khí có hồi chiêu (bút lông 0,7 s) và máy chủ **im lặng bỏ qua** đòn đánh gửi trong lúc ấy (không
  lỗi, không sự kiện), nên một đòn đánh ngay sau một tràng vẩy bút có thể rơi vào khoảng chết và không có gì
  xảy ra cả; click cũng có thể trượt con đã kịp đi khỏi chỗ ngắm. Nay test đánh lại cho tới khi thẻ mở, đúng
  như người chơi, và trả về **con thật sự đã hỏi** (không phải con gần nhất). Nếu hết 15 s mà không có thẻ,
  lời báo lỗi in luôn những phiên Vấn Đạo máy chủ còn để mở, nên lần sau hỏng là đọc ra ngay.
- **Con bên cạnh cũng có quyền hỏi.** `beat()` coi mọi thẻ Vấn Đạo hiện ra giữa lúc đánh là lỗi, trong khi một
  nhát vẩy trúng con khác (hoặc một con tự xông vào đánh) mà con ấy còn Mặc Thuẫn thì nó hỏi câu của nó - đúng
  luật 8.1. Chứng cứ: chạy lại 6 lượt thì hỏng 2 lượt, và bảng `quiz_sessions` của lượt hỏng có hai phiên,
  phiên thứ hai `ref` trỏ sang `m1_0` chứ không phải con đang đánh. Nay `beat()` trả lời câu của con bên cạnh
  rồi đánh tiếp, và chỉ báo lỗi khi câu hỏi là của **chính** con đang đánh (nghĩa là khiên mọc lại, chỉ tinh
  anh mới vậy).
- **Bot phải được phép bước ra khỏi chỗ mình đang đứng.** `path()` của bot (`tests/realm_bot.py`) nhận
  danh sách `avoid` để không đi qua những ô không được đạp lên - ví dụ các phiến đá khác của Câu Văn
  Đứt Đoạn. Nhưng danh sách ấy cũng cấm luôn **ô bot đang đứng**: một bot vừa đạp xong phiến của nó thì
  đang đứng trong một ô bị cấm, mà các phiến kề sát nhau nên mọi ô lân cận đều bị cấm - BFS không có
  bước đi hợp lệ nào, trả về đường rỗng, bot đứng đó mãi. Nó không rời phiến để về chỗ chờ, và tới lượt
  nó giữ chữ kế tiếp thì cũng không đi tới phiến đúng được: phòng treo vĩnh viễn với `fails: 0`.
  Đây là lỗi của bot (dụng cụ test), không phải của game - người chơi thật chỉ việc bước ra.
  Chứng cứ: `RealmInstance` dùng `random.Random()` không gieo hạt nên mỗi lượt là một cấu hình khác;
  gieo hạt cố định rồi quét 200 hạt thì **6 hạt treo** (34, 38, 98, 99, 172, 173), cả 6 đều cùng một
  dấu vết - chủ của chữ đang tới có `route_left=0` và `on_tile` là một phiến **khác** phiến đích. Ba
  hạt chạy lại hai lần đều treo y nguyên, nên đây là tất định theo hạt, không phải đua đồng hồ (test
  này chạy trên đồng hồ ảo `FakeMono`, 18000 nhịp 0,05 s, nên máy chậm không ảnh hưởng). Nay `path()`
  tìm lần hai khi không thấy đường: lần ấy bỏ cấm **đúng những ô đang chứa bot** - được bước ra khỏi ô
  mình đứng, không được bước vào ô khác. Cả 6 hạt đều qua, và
  `test_a_bot_can_walk_off_a_stone_it_must_avoid` đứng canh: test ấy **trượt** với `path()` cũ.
- **Chạy được cả trên PostgreSQL.** `KVTT_TEST_URL` cho phép chỉ cho bộ test trỏ sang một cơ sở dữ liệu khác,
  nên `alembic upgrade/downgrade` và cả bộ test máy chủ đều đã chạy thật trên PostgreSQL 18 (0013 lên, xuống
  0009, lên lại). Không có gì phải sửa trong migration.
- **Test của bài tập lập trình phải có răng.** `tools/check_all.py` nay chạy ba bài làm sai (rỗng, in một hằng
  số, in đáp án ví dụ 1) trên mọi bài tập và bắt buộc bài nào cũng **phải trượt**, và không cho phép mọi test
  ẩn của một bài hỏi cùng một đáp án. Lời giải mẫu vẫn phải đúng trên mọi test.

## Nhánh `toan-tu-tien` — M7: thế giới và chiến đấu (quái = lỗi sai)

- **Một con quái là một lỗi sai, không phải một con vật.** `data/math/monsters.json` giữ 9 con cho Đại Số
  Tuyến Tính tầng 1-3, mỗi con trỏ tới **một vi kỹ năng** và **một mục** của Tàng Thư Các. 18 mục "Lỗi
  thường gặp" viết ở M4 chính là danh sách lỗi có sẵn, nên M7 không phải nghĩ ra lỗi mới: con quái chỉ là
  cái mặt của một ghi chú đã có. Chọn 9 trong 18 (3 mỗi tầng) cho vừa một vùng chơi được; số còn lại để
  dành. "Hoán Vị Ma" (AB = BA) trong kế hoạch phải chờ: phép nhân ma trận là tầng 4 trở lên, chưa có câu.
- **Bậc câu hỏi thuộc về người chơi, không thuộc về con quái.** Con quái cố định vi kỹ năng; bậc thì đọc từ
  `math_answers` của chính người chơi ở vi kỹ năng ấy (luật 3.3). Vì thế một con Phần Tử Ma vẫn còn việc để
  dạy sau mười lần gặp, và không ai bị hỏi bậc mà lộ trình chưa mở. Nếu vi kỹ năng ấy chưa có câu nào ở bậc
  đó thì con quái giữ khiên và người chơi được nhắc đi luyện - thà không hỏi còn hơn hỏi sai bậc.
- **Đánh quái ngoài thế giới cũng là học.** Câu trả lời ghi vào `math_answers` với `run_id = NULL`, nên nó
  tính vào bậc đã mở và vào cổng thuần thục y như câu ở Động Phủ. Giá trị tôi tự chọn: **không** chạy luật 6
  ("tâm ma") ở đây, vì câu song song không có buổi luyện nào để quay về; sai thì chịu Mặc Kích và được ghi
  lại, thế thôi.
- **Ghi chú lỗi sai là thứ giữ lại, không phải thứ tiêu đi.** Vật phẩm `kind: "note"` không bán được, đọc
  không mất, và đọc là mở đúng mục giải thích (máy chủ tự tính tài liệu + khối từ `skill`, nên dữ liệu
  không phải nhắc lại số thứ tự mục). Tàng Thư Các **không** bị khoá sau con quái: kế hoạch nói đọc tài
  liệu phải không có rào, nên ghi chú chỉ là đường tắt tới đúng trang.
- **Chỉ rèn được thứ mình đã hiểu.** Công thức ở Lò Toán (`data/math/crafting.json`) đòi hai thứ khác loại:
  nguyên liệu (tiêu mất) và ghi chú (chỉ kiểm tra). Luật "đánh đẹp là học đúng" của kế hoạch nằm trong dữ
  liệu, không nằm trong lời thuyết. Phẩm chất món rèn ra ghi cố định trong công thức, không rút thăm: gom đủ
  nguyên liệu thì biết trước mình được gì, và test khẳng định được.
- **Một sổ quái duy nhất.** Trước M7 có hai chỗ đọc `creatures/monsters.json`: `systems/catalog.py` (rớt đồ,
  Yêu Quái Phổ, nhiệm vụ) và `realtime/ai.py` (sinh quái). Nếu chỉ thêm quái toán vào một chỗ thì con quái
  đánh được mà không rớt gì (hoặc ngược lại). Nay `catalog.monsters()` gộp cả hai file và `ai.monster_types()`
  gọi chính nó, nên không thể lệch. Hai test cũ phải sửa theo: `test_monster_data_is_complete` giờ đòi
  `qtypes` ở Mặc Quái và đòi `skill`/`note`/`mistake_vi` ở quái lỗi sai (**chặt hơn** trước), còn
  `test_monster_book_hides_unmet` đếm từ dữ liệu chứ không ghi cứng số 6.
- **Thẻ Vấn Đạo có hai loại, thế giới chỉ cần biết một tên.** Thẻ chữ (`rpg.CombatQuizScene`) và thẻ toán
  (`math_practice.MathCombatQuizScene`) không cùng cha, nên `world.py` nhận cả hai bằng một lớp dấu hiệu
  `quiz.CombatCard`. Trước đó `world.py` dò `isinstance(..., CombatQuizScene)` ở ba chỗ (không xếp hai thẻ,
  đóng thẻ khi `q_end`, đóng thẻ khi chết) và `main.py` một chỗ; thiếu một chỗ là thẻ toán sống sót sau khi
  chết.
- **Danh sách vùng của máy khách cũng phải biết vùng mới.** `strings_vi.WORLD_ZONES` quyết định chỗ người
  chơi quay lại khi đăng nhập; thiếu `loan_so_coc` trong đó thì ai đăng xuất giữa Loạn Số Cốc sẽ tỉnh dậy ở
  Động Phủ. Test dòng chảy M7 bắt được lỗi này ngay lần chạy đầu.
- **Kiểm tra dữ liệu M7 có răng.** `tools/check_all.py` nay 12 kiểm tra: một con quái phải có vi kỹ năng
  thật, mục tài liệu thật, ghi chú trỏ về đúng vi kỹ năng và đúng con quái, hình vẽ ở `client/art/math_art.py`
  (cùng `shape` và cùng màu thân với dữ liệu), và phải có vùng sinh ra nó; mỗi công thức phải rèn ra trang bị
  thật từ thứ thật sự rớt. Đã thử làm sai 5 chỗ (đổi vi kỹ năng, xoá ghi chú, lệch màu, thêm con không ai
  sinh, nguyên liệu không tồn tại): cả 5 đều bị bắt.

## Nhánh `toan-tu-tien` — M8: đường ống Blender

- **Sprite là thứ được commit, Blender thì không bắt buộc.** `tools/make_character.py` chạy bốn bước: dựng
  `.blend`, render, ghép sheet + JSON, kiểm tra. Chỉ hai bước đầu cần Blender; game và cả hai bộ test chỉ
  đọc `client/assets/chars/*.png|json`. Ai clone về mà không có Blender vẫn chơi và vẫn chạy test được, và
  `world.py` không crash khi thiếu sheet.
- **Ảnh render trung gian không vào git.** `art/render/`, `art/render_items/` và `*.blend1` nằm trong
  `.gitignore` vì dựng lại được bằng một lệnh; `.blend` và model `.glb` thì giữ, vì đó là nguồn.
- **Năm luật chất lượng của kế hoạch 7.3 là một công cụ, không phải lời dặn.** `tools/sprite_qc.py` kiểm
  điểm neo, mép khung, nền trong suốt, số khung khớp JSON và kích thước thống nhất giữa các nhân vật; bộ
  test client chạy nó trên các sheet đã commit.
- **Icon vật phẩm đi cùng giấy phép của nó.** `art/models/manifest.json` ghi tên, tác giả, giấy phép và
  link của từng model (CC0, CC-BY, tự dựng); có test bắt buộc mọi model CC-BY phải có mặt trong
  `CREDITS.md`. Game vẫn chạy khi chưa có icon nào.
- **Tám bộ dáng theo danh sách cảnh giới của người chơi ghi, dữ liệu tu luyện chưa đụng tới.** Game đang
  có 5 cảnh giới và gọi tầng 3 là Kim Đan; danh sách dựng sprite có 8 và gọi là Kết Đan. Chờ quyết định.
- **Hàng "trái" và "phải" từng bị đảo (sửa ở M9).** `render_character.DIRS` xoay nhân vật +90 độ cho hướng
  "trái", tức là quay mặt sang phải. M8 không lộ vì game chỉ vẽ hướng "xuống"; M9 vẽ người thi triển theo
  hướng đang nhìn nên lộ ra. Nay trái là 270 độ, phải là 90 độ; các khung cũ giữ nguyên từng pixel, chỉ
  đổi nhãn, và có test ghim lại.

## Nhánh `toan-tu-tien` — M9: chiêu thức gắn câu hỏi

- **Câu hỏi chính là chiêu đang vận.** Bấm phím chiêu chưa đánh gì cả: máy chủ hỏi một câu thuộc loại của
  chiêu, qua đúng ô `p.question` của Vấn Đạo, nên người thi triển có Hộ Thể và không mở được câu thứ hai.
  Linh khí và hồi chiêu bị trừ lúc chiêu được nhận, trước khi trả lời.
- **Chiêu hụt không phải Mặc Kích.** Sai hoặc hết giờ: không sát thương, combo về 0, mất linh khí và hồi
  chiêu, không mất máu. Kế hoạch chỉ nói rõ trường hợp hết giờ ("chiêu hụt nhưng không mất đồ"); giá trị
  tự chọn là áp dụng cho cả trả lời sai. Sau chiêu hụt, con quái còn khiên vẫn hỏi câu của chính nó sau
  vài giây như luật cũ.
- **Chiêu trúng không hồi linh khí.** Câu Vấn Đạo đúng thì được `correct_qi_gain`; chiêu thì không, nếu
  không Thường Quyền (0 linh khí) thành máy cày linh khí.
- **Bậc vẫn thuộc về người chơi.** Câu của chiêu lấy đúng vi kỹ năng của con quái lỗi sai đang nhắm (không
  có thì vi kỹ năng khác cùng tầng), ở bậc người chơi đang mở, không bao giờ cao hơn; thiếu mẫu ở bậc ấy
  thì lùi xuống bậc gần nhất còn mẫu, không dưới `min_tier`. Câu trả lời ghi vào `math_answers` với
  `run_id = NULL` như M7, nên tính vào lộ trình.
- **Mở khoá theo lộ trình học, không theo cảnh giới.** `unlock.floor` so với tầng đang mở (tầng chính thấp
  nhất chưa qua, lấy cao nhất giữa các môn). Danh sách cảnh giới chưa chốt nên không có gì đọc nó.
- **Combo.** `combo_mult = min(max_mult, 1 + per_streak x n)`, n là số câu chiêu đúng liên tiếp trước câu
  này: câu đầu x1,0, câu hai x1,1, chặn ở x1,5. Combo nằm trong bộ nhớ, về 0 khi hụt, khi chết và khi rời
  thế giới. Trả lời nhanh là chí mạng theo đúng luật Ngộ Đạo.
- **Khiên nhóm của trùm bí cảnh không bị đi tắt.** Chiêu trúng chỉ tính là một câu đúng của người ấy
  (`combat.group_hit`, dùng chung với `on_answer`); vẫn phải đủ số người khiên mới vỡ.
- **Câu đúng của người khác không huỷ chiêu đang vận.** `break_shield` kết thúc câu Vấn Đạo đang mở của
  những người cùng đánh con ấy, nhưng bỏ qua câu của chiêu: khiên vỡ rồi thì chiêu vẫn nên trúng.
- **Hai loại câu mới, vì bảng 4.4 đòi.** Trận pháp cần Ghép cặp / Sắp xếp bước giải, nên `matching` và
  `ordering` thành loại chơi được (18 câu viết tay cho tầng 1-3, mỗi tầng 3 + 3). Câu sắp xếp không bao
  giờ hiện ra ở đúng thứ tự sẵn; câu ghép cặp luôn có ít nhất một vế bị dời chỗ. Bài làm sai định dạng
  được chấm là sai, không ném lỗi. Hệ quả: buổi luyện ở Động Phủ cũng rút ra hai loại câu này.
- **Tuyệt kỹ có trong dữ liệu nhưng chưa thi triển được.** `thien_loi_tuyet_ky` cần câu Thiên kiếp bậc 4,
  mà bậc 4 bắt đầu ở tầng 5 và tầng 7-9 chưa có câu (M11). `check_all` cho phép đúng một ngoại lệ này: mọi
  chiêu mở ở tầng <= 3 phải có câu để thi triển ngay khi người chơi vừa tới tầng ấy.
- **FX vẽ bằng code, không phải ảnh.** `client/art/skill_fx.py` có sáu hiệu ứng là hàm thuần của tiến độ
  0..1 và toạ độ, nên test được không cần màn hình; mỗi hiệu ứng có bản "chiêu hụt" riêng.
- **Người thi triển tạm đổi sang sprite Đạo Sĩ.** Trong lúc ra chiêu, nhân vật được vẽ bằng clip `anim`
  của sheet `dao_si_luyen_khi` (cố định, chưa nối với cảnh giới). Thiếu clip thì lùi về `slash`, thiếu sheet
  thì lùi về động tác vung cũ. Sprite người chơi bình thường vẫn là sprite pixel cũ, nên có một lần đổi
  hình; muốn liền mạch thì phải vẽ người chơi bằng sprite Đạo Sĩ suốt, việc ấy chờ quyết định cảnh giới.
- **Phím chiêu là 1-6** (từ sau M10; lúc đầu là Z X C V G N vì hàng 1-4 còn thuộc về Pháp Chữ cũ - xem mục
  "Công pháp không còn tiếng Trung" bên dưới).
- **Kiểm tra phông chữ quét thêm phần mới.** Vế ghép cặp, bước sắp xếp, lời đáp án hiện sau khi trả lời,
  câu hướng dẫn của từng loại câu và chữ của chiêu thức đều vào `displayed_strings()`.
- **Câu hỏi tới lúc thẻ trước còn hiện kết quả thì chờ, không bị bỏ.** Trước M9, `world.py` bỏ mọi gói `q`
  tới trong lúc còn một thẻ chiến đấu trên màn hình, kể cả thẻ chỉ đang hiện kết quả. Máy chủ thì đã mở câu
  ấy rồi: người chơi bị giữ trong Hộ Thể vì một câu không ai thấy, mọi chiêu bị từ chối "đang trả lời câu
  khác", và hết giờ thì ăn Mặc Kích. M6 đã ghi nhận nhưng chưa gặp lần nào; với chiêu thức thì gặp ở cả 6/6
  lượt chạy có đo, vì chiêu vừa trúng là con quái bên cạnh hỏi ngay. Nay câu ấy chờ (`waiting_q`): thẻ trước
  đóng là mở, quá `WAITING_Q_MAX` = 2,5 giây thì tự đóng thẻ trước; thời gian đã chờ được trừ vào đồng hồ của
  thẻ mới, vì đồng hồ máy chủ vẫn chạy. Thẻ còn đang trả lời thì không bao giờ bị đóng thay.
- **`client/main.py` phải biết gói `mcast`.** Danh sách gói được chuyển tới màn thế giới nằm ở `Game._on_net`;
  thiếu `mcast` thì lời từ chối của máy chủ (chưa hồi xong, thiếu linh khí, còn khoá) không bao giờ hiện.

### 2026-11-20: vùng hoang chỉ hỏi khi bị quái đánh trúng (thay luật "trả lời để ra chiêu" ở trên)

Tác giả yêu cầu "chỉ hỏi khi quái đánh trúng mình"; thiết kế đã duyệt là phần `combat` của
`server/data/math/world_plan.json`. Nay nó chạy: `"wired_sections": ["combat"]`, còn `"wired"` vẫn `false` vì
vùng đất, binh khí, linh thú chưa nối. Mọi con số đọc từ file ấy (`realtime/combat.py`).

- **Chỉ vùng hoang.** Bí cảnh (`realm.RealmInstance`, `instance = True`) vẫn là Vấn Đạo và chiêu ra bằng câu
  hỏi; hầm ngục, thủ thành, cơ duyên không đụng tới. Các test cũ của Vấn Đạo và chiêu M9 (`test_combat`,
  `test_math_skills`, `test_bee_guard`) ghim luật cũ lên một vùng hoang để vẫn kiểm được đường mã bí cảnh dùng.
- **"Trận đấu dừng lại" chỉ dừng cho người bị hỏi.** Từ lúc đòn trúng tới lúc trả lời (hay hết giờ) người ấy
  có Hộ Thể: không mất máu, không đi, không đánh, không né, không ra chiêu, và không quái nào chọn họ làm mục
  tiêu. Thế giới không dừng: người khác trong vùng vẫn đánh, kể cả chính con quái ấy, và nó quay sang họ; đòn
  đang báo trước vẫn rơi xuống ai đứng trong vùng. Không ai trả lời hộ ai, câu đúng của người này không đóng
  câu của người kia. Trong lúc máy chủ soạn câu, người bị trúng được giữ yên tối đa `question_wait_seconds`
  (số mới, 3 giây) để đòn khác không chồng lên.
- **Câu hỏi đi đúng đường cũ.** Quái lỗi sai hỏi vi kỹ năng của nó ở bậc người chơi đã mở (`math_combat.
  question_for`), Mặc Quái hỏi phần Đạo Thụ của người chơi (`math_ask.pick_own`); câu trả lời ghi vào
  `math_answers` nên tính vào bậc, cổng thuần thục và lịch ôn xoắn ốc (`test_combat_on_hit` kiểm cả ba).
- **Phản Đòn** = `base_damage × counter_multiplier`, không có chí mạng "trả lời nhanh" (luật mới không nói tới);
  quái choáng `stun_seconds`; Linh Lực cộng `linh_luc_gain` (số mới, 8 như `correct_qi_gain` cũ); Tu Vi theo bậc
  câu như mọi câu toán.
- **Sai hoặc hết giờ**: đòn của con quái trúng nguyên vẹn (công quái trừ phòng thủ), **không còn Mặc Kích** ở vùng
  hoang. Hệ quả chờ tác giả quyết: Kháng Mực và Linh Thú Rắn (giảm Mặc Kích) nay chỉ có tác dụng trong bí cảnh.
- **Không soạn được câu** (`no_math_question`): đòn tính như đòn trong thời gian nghỉ (nửa sát thương) và thời
  gian nghỉ bắt đầu; không hỏi lại ngay.
- **Quái chết trong lúc người bị trúng đang trả lời**: câu vẫn được chấm; đúng thì không có đòn phản để đánh
  (`gone`), sai thì đòn vẫn trúng - đòn đã rơi xuống rồi, người khác hạ quái không xoá được nó.
- **Khiên**: quái thường ở vùng hoang không có Mặc Thuẫn (`shielded_ranks` = tinh anh, thủ lĩnh), nên đòn thường
  hạ được. Khiên tinh anh chỉ vỡ khi Phản Đòn; khiên mọc lại theo `shield_regen` như cũ và lại cần Phản Đòn.
  Chiêu và ong hộ vệ không phá được khiên ở vùng hoang.
- **Hình vùng đánh**: tròn, quạt, thẳng đều làm (rẻ: phép thử hình học trên máy chủ, sheet `warn_cone_*` /
  `warn_line_*` đã có). Quái thường đánh tròn; tinh anh lần lượt quạt, tròn, thẳng; thủ lĩnh tròn, quạt, thẳng
  (`telegraph.by_rank`); quái có thể ghi `attack_shape` riêng. Quạt và thẳng đi từ con quái về phía mục tiêu.
- **Né Đòn**: lướt `dash_px` = 40 px trong `dash_ms` = 150 ms (hai số mới), bất khả xâm phạm 0,25 giây, hồi 1,2
  giây. Cú lướt xếp vào hàng di chuyển dưới số thứ tự riêng để máy chủ đi đúng như client đoán; bị từ chối thì
  vẫn chiếm số ấy (bước rỗng). Mở theo tu vi (Luyện Khí tầng 1, mục `ne_don`), nên Phàm Nhân chưa né được.
  Không né trong bí cảnh. Phím Shift.
- **Chiêu thức ngoài vùng hoang ra tự do**: cùng mở khoá theo Đạo Thụ, linh lực, hồi chiêu, tầm và công thức,
  không câu hỏi. **Combo** nay đếm số **Phản Đòn liên tiếp** (về 0 khi trả lời sai, hết giờ, chết, rời thế giới),
  để học vẫn làm chiêu mạnh hơn. `qtypes` và `min_tier` chỉ còn dùng trong bí cảnh. Máy chủ đọc mở khoá trước
  nên chiêu còn khoá luôn nói "còn khoá" trước "chưa hồi" hay "chưa chọn mục tiêu".
- **Client**: thẻ `rpg.ParryCard` (con của thẻ quái lỗi sai) ghi rõ đòn bao nhiêu, kết quả Phản Đòn / trúng đòn,
  thời gian nghỉ; trả lời sai thì thẻ ở lại 4,5 giây để đọc lời giải (Enter đóng sớm). `client/main.py` (phiên khác
  giữ) không chuyển gói `dodge` và `stats` tới màn thế giới, nên client tự kiểm mở khoá Né Đòn từ cảnh giới của
  nhân vật và tự tính hồi chiêu; máy chủ vẫn là bên quyết định.

### 2026-11-20: linh thú và thần thông Luyện Khí (`wired_sections` thêm `beasts`, `abilities`)

- **Một mô hình bạn đồng hành.** Linh thú thu phục là một dòng của bảng `pets` và một loài của `pets.species()`
  (gộp từ `world_plan.json`), đeo một con một lúc như con giáp; Thiên Cơ Các không bao giờ quay ra nó, Linh Thú
  Phổ vẫn là mười hai con giáp. Kỹ năng của nó là `gift` của kế hoạch, đọc ở chỗ nó tác dụng.
- **Thu phục bằng Phản Đòn.** Linh thú là quái của vùng chỉ hiện với người đủ tầng Đạo Thụ; không chết; mỗi Phản
  Đòn của một người được đếm, đủ `parries_to_tame` thì nó chịu phục người ấy 90 giây. Phong Ấn Phù bán ở Sạp Tạp
  Hóa (nguồn không khoá theo luật rơi đồ); phong ấn cần thần thông tầng 3.
- **Thần thông đi trong dòng di chuyển.** Đạp Kiếm Lướt và lên/xuống thú cưỡi xếp hàng dưới số thứ tự riêng như
  Né Đòn, nên máy chủ quyết định đúng ở bước client đã đoán; chỗ đáp lướt kiểm bằng cùng một hàm hình học ở hai
  bên (`realtime/glide.py`, bản chép ở client). Máy chủ là bên duy nhất áp tốc độ cưỡi.
- Chi tiết và các lựa chọn đổi được: `docs/DAO_THU_TRONG_GAME.md`, phần "Linh thú và thần thông Luyện Khí".

- **Một chỗ duy nhất để chọn câu hỏi.** `systems/math_ask.py` là nơi cả bốn chế độ lấy câu: bậc là của người
  chơi ở vi kỹ năng ấy và không bao giờ cao hơn, không hỏi tầng chưa tới, cửa sổ chống lặp là cả sổ trả lời,
  và câu trả lời ghi vào `math_answers` với `run_id = NULL` (`math_ask.record`) nên tính vào lộ trình như M7
  và M9. Bốn chế độ không được chép lại các luật này. `pick(..., highest=True)` là "bài tổng hợp": câu khó
  nhất mà người chơi ấy được phép gặp.
- **Không chế độ nào đọc cảnh giới.** Mọi thứ mở theo tầng của lộ trình học, vì danh sách cảnh giới chưa chốt.
- **Thứ cần nội dung chưa có thì nằm trong dữ liệu và hiện là khoá, không làm giả.** Tháp Xác Suất và Tháp
  Gradient (môn chưa có câu), trùm bí cảnh hỏi "Tìm chỗ sai" (loại câu chưa chơi được), các tầng 4 trở lên
  của hầm ngục. Chúng tự mở khi M11 thêm nội dung; với hai tháp có test giả lập một môn để chứng minh.

### Bí cảnh toán (tổ đội)
- **Dùng lại máy bí cảnh cũ, chỉ đổi thứ được hỏi.** Bí cảnh mới `toan_tran` chạy trên đúng bộ máy stage 9
  (phòng, tổ đội, hồn ma, khiên nhóm, rương, cổng). Kênh của một bí cảnh toán có `question_source`; `combat.py`
  hỏi qua nó thay vì hỏi câu của con quái. Bí cảnh chữ cũ không đổi gì và có test giữ.
- **Mỗi người nhận câu theo tầng của chính mình** (kế hoạch 4.3), dù quái, trận nhãn hay trùm hỏi. Hai người
  ở tầng 1 và tầng 3 đánh chung một con thì nhận câu tầng 1 và tầng 3. Chiêu thức M9 ra trong bí cảnh cũng
  theo luật này: ngoài bí cảnh, chiêu hỏi theo tầng của con quái bị nhắm; trong bí cảnh thì theo tầng của
  người ra chiêu.
- **Trận Nhãn** là loại phòng giải đố mới, đứng cạnh các loại cũ và mượn phòng cùng các phiến đá có sẵn của
  bản đồ `bi_canh` nên không sửa bản đồ. Đứng lên một trận nhãn thì được hỏi một câu; đúng thì trận nhãn vỡ.
  Phòng mở khi đủ số trận nhãn vỡ (tăng theo số người) và đủ số người khác nhau đã phá. Ai đã phá rồi mà
  phá tiếp sẽ làm thiếu phần của người khác thì bị từ chối, nên phòng không thể kẹt.
- **Trùm:** khiên nhóm như cũ, mỗi người một câu đúng, và câu ấy là bài tổng hợp của người đó. Dữ liệu ghi
  loại câu ưu tiên là `find_mistake`; khi loại ấy chơi được thì trùm tự dùng, không cần sửa code.
- **Ai không có câu nào để hỏi thì được báo và không bị chờ:** không tính vào số trận nhãn cần phá và số người
  cần cho khiên nhóm. Nếu ngân hàng không có tầng nào cho một người thì cả tổ đội không vào được và không
  mất lượt.
- **Vào một mình được** (`party_min: 1`), 3 lượt mỗi ngày, 20 phút một lượt.

### Hầm ngục
- **Bố cục là hàm thuần của (hạt giống, môn, tầng).** Số phòng, loại phòng, vi kỹ năng mỗi phòng, kẻ canh,
  rương cuối: cùng hạt giống thì cùng hầm ngục, không đọc đồng hồ và không đọc người chơi. Câu hỏi bên trong
  thì theo bậc của người chơi nên không nằm trong hạt giống. Bố cục được lưu cùng lượt chơi, nên sửa dữ liệu
  không đổi lượt đang chơi dở.
- **Mỗi phòng một loại câu, và chỉ sinh ra phòng hỏi được:** cặp (loại câu, vi kỹ năng) phải có mẫu ở bậc
  thấp nhất của tầng - bậc luôn mở. Kiểm trên 300 hạt giống x tầng 1-3.
- **Tâm lực:** sai hoặc hết giờ mất một; về 0 thì dừng và giữ mọi thứ đã nhận. Phòng cuối là Trấn Thủ: bài
  tổng hợp.
- **Tắt game không né được câu hỏi:** câu đang mở mà hết giờ lúc người chơi vắng mặt được chấm là hết giờ ở
  lần kế tiếp nhìn vào lượt chơi.
- **Thưởng có giới hạn ngày, học thì không:** 5 lượt đầu mỗi ngày có Linh Thạch và nguyên liệu; các lượt sau
  vẫn chơi được, vẫn được Tu Vi và vẫn tính vào lộ trình.

### Cơ duyên
- **Cơ duyên đến từ việc học.** Mỗi câu toán đúng - ở Động Phủ, đánh quái, ra chiêu hay trong chế độ khác -
  cộng một vào bộ đếm; đủ ngưỡng thì gieo một lần. Câu của chính cơ duyên không cộng vào bộ đếm. Mọi câu trả
  lời đi qua một chỗ nghe duy nhất (`math_combat.add_answer_listener`) nên không chế độ nào bị sót.
- **Thua không mất gì.** Sai, hết giờ hoặc bỏ qua: không thưởng, không phạt.
- **Trạng thái nằm trong `users.flags`**, như bộ đếm ngày của thủ thành: không thêm bảng.
- **Hai vật phẩm hiếm mới (Ngọc Giản Lão Nhân, Ấn Rương Đề) hiện chỉ bán được.** Chưa có công thức Lò Toán
  nào dùng chúng; đó là quyết định về nội dung, để người chơi quyết.

### Thủ thành toán
- **Một bộ mô phỏng cho cả hai bản.** `td_sim.py` nhận thêm `place_needs_answer`: một sự kiện "đặt tháp" phải
  kèm một câu hỏi "đặt" về đúng tháp ấy và mỗi câu chỉ dùng một lần. Bản chữ cũ không bật cờ này nên các con
  số của nó không đổi; không test cũ nào bị sửa. `client/engine/td_sim.py` và `server/app/systems/td_sim.py`
  vẫn giống nhau từng byte.
- **Máy chủ vẫn là bên quyết định:** client mô phỏng và gửi nhật ký, máy chủ chạy lại rồi mới phát thưởng.
  Năm kiểu nhật ký giả bị từ chối: đặt tháp không có câu hỏi, nâng tháp mà câu đặt đã sai, dùng câu của
  tháp khác, một câu cho hai tháp, dùng câu nâng để đặt.
- **Sai thì mất Linh Khí đã bỏ ra, ngoài ra không mất gì** - cùng luật "không hoàn lại" của thủ thành cũ và
  cùng tinh thần chiêu hụt của M9. Tụ Khí sai thì không mất gì.
- **Sức mạnh tháp không còn dựa vào độ thuộc chữ:** lấy từ dữ liệu nhân với hệ số theo bậc của câu hỏi đã
  dựng tháp. Máy chủ chốt hệ số lúc ra câu hỏi và ghi cùng câu trả lời, nên việc chạy lại vẫn tất định.
- **Hai bản không thấy lượt chơi của nhau:** lượt toán dùng lại bảng `td_runs` / `td_progress` với mã ải bắt
  đầu bằng `math_`, không thêm bảng.

### Việc chung
- **Thông báo cơ duyên nằm ở thẻ câu hỏi toán**, không nằm ở từng chế độ: câu trả lời nào mang
  `math.fortune_offer` thì thẻ báo khi đóng, chế độ nào hỏi cũng vậy.
- **`check_all.py` nay 17 kiểm tra:** mỗi chế độ có `validate()` riêng trong module của nó và `check_all` gọi
  bốn hàm ấy; kiểm tra phông chữ quét thêm mọi chuỗi `_vi` trong dữ liệu của bốn chế độ.
- **Chỉ hầm ngục thêm bảng** (`math_dungeon_runs`, migration `0014_math_dungeon`).

### Công pháp không còn tiếng Trung (sau M10, theo yêu cầu của người chơi)
- **Ô chiêu hiện icon dựng từ model 3D, không hiện chữ Hán.** Mỗi chiêu trong `skills.json` có `icon` (và
  `icon_variant`): tên một icon của `client/assets/icons/items.json`, tức ảnh render từ model trong
  `art/models/` (M8). Thường Quyền = găng, Phá Mê Kiếm Quyết = kiếm, Hỏa Cầu Thuật = quạt, Ngũ Hành Trận =
  sách, Hộ Thân Trận = khiên, Thiên Lôi Tuyệt Kỹ = cuộn thư. `check_all` đòi icon ấy phải có trong sheet; test
  đòi không hai chiêu nào chung một hình. Bản clone không có sheet icon thì ô hiện chữ viết tắt tên tiếng
  Việt ("HC"), không bao giờ hiện chữ Hán.
- **Pháp Chữ cũ rời khỏi màn hình.** Hàng 1-4 gắn với chữ Hán đã học, chữ Hán to hiện trên đầu người ra
  chiêu, danh sách "Pháp Chữ" trong bảng nhân vật và các dòng gợi ý nhắc tới nó đều đã gỡ. Chiêu thức nhận
  hàng ấy và các phím 1-6; bảng nhân vật nay liệt kê sáu chiêu thức kèm icon.
- **Chưa gỡ ở máy chủ và trong dữ liệu game cũ:** `data/skills.json`, lệnh `skill`, và bốn món "Bí kíp ... Chữ
  Quyết" vẫn rớt từ quái, vẫn là thưởng nhiệm vụ / thủ thành chữ và vẫn bán ở Thủ Thư. Chúng thuộc kinh tế
  của game chữ cũ, gỡ thì phải sửa bảng rớt đồ, nhiệm vụ, cửa hàng và test của các phần ấy - chờ người chơi
  quyết.
- **"Hạt giống" của hầm ngục gọi là "linh thạch số".** Trên màn hình: "Linh thạch số 1001", ô nhập "Linh thạch
  số", nút "Chơi lại linh thạch này". Trong code và API vẫn là `seed`. Đây chỉ là cách gọi: vào hầm ngục không
  tốn Linh Thạch.

## Nhánh `toan-tu-tien` — M11: ba bí cảnh còn lại của Luyện Khí (tầng 1-3), Tìm chỗ sai, kiểm tra đầu vào

- **Phạm vi: khung đủ 9 tầng, viết đầy đủ tầng 1-3.** Kế hoạch ghi M11 là "thêm 3 bí cảnh còn lại" mà không
  nói bao nhiêu tầng. Làm giống M1-M4 với Đại Số Tuyến Tính, đúng lời dặn trong phần rủi ro ("chia nhỏ theo
  tầng, chỉ làm tầng 1-3 trước"): mỗi môn mới có đủ 9 tầng chính + tầng ẩn 10 (tên tầng theo mục 3.5, vi kỹ
  năng, tiên quyết) và tầng 1-3 có ngân hàng câu, bộ sinh câu, bài đọc. **Tầng 4-9 của cả bốn môn chưa có
  câu** - 24 tầng, phần lớn nhất của Luyện Khí. Vì thế vẫn chưa có câu bậc 4-5: Thiên Lôi Tuyệt Kỹ còn khoá,
  loại câu Thiên kiếp chưa chơi được, và luật 8 (thang câu cho bậc 5) chưa có gì để áp dụng.
- **Ba môn mới:** Giải Tích (`giai_tich`, tiền tố `gt`), Xác Suất và Thống Kê (`xac_suat_thong_ke`, `xs`), Tối Ưu
  và Toán Rời Rạc (`toi_uu_roi_rac`, `tr`). Mỗi môn có file riêng cho mọi thứ: lộ trình, câu hỏi,
  `math_gen/<tiền tố>_floor<N>.py`, `tools/math_verify_<tiền tố>.py`, thư mục bài đọc, bảng duyệt. Nhờ vậy ba
  môn được viết song song mà không đụng file của nhau.
- **Toán phải đúng, và có hai lớp kiểm.** Mỗi bộ sinh câu có phép tính lại bằng sympy theo đường khác với
  chính nó (giải tích: `limit`, `solve`, chuỗi; xác suất: liệt kê cả không gian mẫu hoặc `sympy.stats`; rời
  rạc: bảng chân trị, liệt kê mọi cấu hình, luỹ thừa ma trận cho truy hồi). Câu viết tay thì không máy nào
  kiểm thay được: người viết phải tính lại độc lập, và mọi câu vẫn là `reviewed: false` cho tới khi người
  chơi đọc bảng duyệt ở `tools/reports/`. Các câu người viết tự thấy kém chắc được nêu tên trong lời commit.
- **Hai môn cùng chạm tổ hợp.** Tầng 1 của Xác Suất ("giải tích kết hợp") và tầng 1-2 của Toán Rời Rạc đều
  đếm; đó là trùng lặp có sẵn trong đề cương. Xác Suất đếm để tính xác suất; Toán Rời Rạc dạy đếm như một
  môn riêng (nguyên lý cộng / nhân, bù trừ, truy hồi) cùng logic mệnh đề và quy nạp.
- **Ký hiệu.** Câu hỏi viết ASCII như các câu cũ (`C(n, k)`, `p => q`, `x -> +vô cùng`); bài đọc dùng công
  thức `$$...$$` dựng thành ảnh. Phần bù viết Ā; logic trong câu hỏi viết bằng chữ ("không p", "p và q").
- **Số chương trong `syllabus_ref` của ba môn mới chưa được đối chiếu với đề cương** - người viết không tra
  mạng. Tên tầng thì theo đúng mục 3.5 của kế hoạch.

### Tìm chỗ sai (`find_mistake`)
- **Một lời giải viết sẵn, chọn bước đầu tiên bị sai.** Các bước giữ nguyên thứ tự, không bao giờ xáo: đó là
  một lời giải. Đúng một dòng sai; các dòng sau có thể sai theo nên đề luôn hỏi "bước đầu tiên". Chỉ có từ
  bậc 2 (bảng thời gian của kế hoạch 3.4 không có bậc 1).
- **Chơi được ở mọi thẻ câu hỏi toán**, và mọi thứ liệt kê loại câu đều biết loại thứ sáu: hầm ngục có thêm
  "Phòng Soi Lỗi" (chỉ sinh ra từ tầng 3, vì tầng 1-2 bắt đầu ở bậc 1), các bot và hàm trả lời của test.
- **Trùm bí cảnh toán tự dùng nó**, đúng như M10 đã để sẵn: ai có câu Tìm chỗ sai ở bậc của mình thì nhận câu
  ấy, ai chưa có thì nhận bài tổng hợp.
- **Cơ duyên cố ý không dùng:** cơ duyên phải hỏi được người mới ở bậc 1.

### Bài kiểm tra đầu vào (luật 7)
- **Tuỳ chọn, theo từng môn, chỉ khi chưa qua tầng nào của môn ấy.** 10-15 câu, mỗi tầng đã viết 5 câu, khó
  dần theo tầng rồi theo bậc. Đạt một tầng khi đúng từ 80% số câu của tầng; tầng xuất phát là tầng thấp nhất
  chưa đạt và không bao giờ là tầng chưa có câu. Dừng sớm ngay khi một tầng không thể đạt nữa.
- **Đây là ngoại lệ duy nhất của luật 4,** và chỉ một hàm được phép phá luật ấy: `math_placement._question`
  tự chọn câu ở bậc của ô đang hỏi, không qua `math_ask.pick`.
- **Tầng được miễn khác tầng đã qua.** Tầng bỏ qua nhờ kiểm tra đầu vào hiện "Được miễn" (lượt `MathRun` có
  mode "placement"), tầng qua bằng Thiên kiếp nhỏ hiện "Đã qua". Ở tầng xuất phát, cổng thuần thục và Thiên
  kiếp nhỏ vẫn áp dụng như với mọi người.
- **Một nguồn duy nhất cho "người chơi đang ở tầng nào":** `math_practice.cleared_floors` = tầng qua bằng Thiên
  kiếp nhỏ + tầng được miễn. Lộ trình, `math_ask.open_floor` và qua đó cả bốn chế độ M10 lẫn chiêu thức đều
  đọc từ đây, nên sau khi xếp tầng mọi thứ tự hỏi theo tầng mới.
- **Làm lại:** nhảy được tầng thì kết quả là chốt; bị xếp ở tầng 1 hoặc bỏ dở thì 7 ngày sau làm lại được.
  Trong lúc kiểm tra không có tâm ma, không đổi bậc thích ứng, không cộng bộ đếm cơ duyên.
- **Không thêm bảng:** `MathRun.mode = "placement"` là đủ.

### Sảnh toán cho bốn môn
- **Mỗi môn một thẻ** (chuột hoặc phím Trái / Phải); sảnh mở ở môn đang luyện dở. Tàng Thư Các có cùng hàng
  thẻ và cuộn được. Mọi mã widget cũ giữ nguyên nên test dòng chảy cũ không phải sửa.
- **Tháp Xác Suất và Tháp Gradient đã mở** vì môn của chúng có câu, đúng như M10 đã viết luật. Cả hai hiện
  hỏi tầng 1 của môn mình; "Gradient" là nội dung tầng 9 của Giải Tích, nên tên tháp đang đi trước nội dung.
- **Bí cảnh toán, hầm ngục và cơ duyên vẫn hỏi theo môn đầu tiên có câu** (Đại Số Tuyến Tính). Ba môn mới
  chơi được qua buổi luyện, kiểm tra đầu vào, Tàng Thư Các và thủ thành; cho người chơi chọn môn trong ba chế
  độ kia là việc chưa làm.
- **Quái lỗi sai (M7) và bài tập lập trình (M6) chưa có cho ba môn mới.**
- **Xưng hô:** game gọi người chơi là "con" ở mọi nơi, kể cả phần kiểm tra đầu vào.

## Nhánh `toan-tu-tien` — tầng ẩn 10 của bốn môn (Tài Năng)

Viết nội dung cho tầng ẩn 10 của Đại Số, Giải Tích, Xác Suất và Tối Ưu - Rời Rạc (19 vi kỹ năng), theo cùng cách viết
tầng 4-9. Những chỗ phải tự quyết:

- **Số lượng.** Mỗi vi kỹ năng có 8-12 câu viết tay (tầng 7-9 có 6-7) và mỗi môn có 6-10 bộ sinh câu: Xác Suất 49
  câu + 6 bộ sinh, Đại Số 48 + 10, Giải Tích 53 + 7, Tối Ưu - Rời Rạc 43 + 10. Tầng 10 chỉ có bậc 5 (cấu hình), nên
  mọi câu viết tay đều có thang (luật 8) hai rung bậc 3-4 của cùng môn, ở tầng không cao hơn 10. Vì tầng 1-2 chỉ có
  bậc 1-2 nên rung luôn lấy từ tầng 3-8; chúng gần chủ đề nhất có thể nhưng có lúc chỉ là "việc dễ hơn cùng kiểu"
  (ví dụ nhóm và vành thang bằng ma trận khả nghịch và không gian con của tầng 6-7).
- **Đạo Thụ quyết điều gì được hỏi.** Cả năm vi kỹ năng tầng 10 của Đại Số và cả năm của Giải Tích nằm trong danh
  sách `cut` của `tree.json` (hệ tài năng thiên về chứng minh): câu có trong kho, qua kiểm tra, nhưng không chế độ
  nào hỏi (`math_practice._templates` bỏ chúng). Vi kỹ năng "Tiên đề xác suất" của Xác Suất cũng bị cắt. Bốn vi kỹ
  năng còn lại của Xác Suất và bốn của Tối Ưu - Rời Rạc được hỏi.
- **Nút "Hiệp phương sai, tương quan và hồi quy" (Xác Suất, tầng 8 chính đạo) hết "đang biên soạn".** Nút nay có
  câu hỏi nên **bắt buộc**: muốn qua tầng 8 phải qua Thiên kiếp nhỏ của phần này. Phần có 3 vi kỹ năng nên 3 câu
  bậc 5, và `trial_allowed` cho sai tối đa 3 // 4 = 0 câu: phải đúng cả ba. Nút bàng môn "Hàm của biến ngẫu nhiên"
  và "Phương pháp tính" cũng có câu, không chặn gì. Cờ `"content"` trong `tree.json` của ba nút này vẫn ghi
  `chua_co` (file đó không thuộc phần việc này): game đọc số câu thật nên chạy đúng, chỉ `tools/check_tree.py` và
  `docs/GIAO_TRINH_CAY.md` còn ghi "chưa có".
- **Quy ước nêu trong đề.** "Chữ số đáng tin" là chữ số hàng 10^s có sai số tuyệt đối <= 0.5 . 10^s; chia đôi: sau
  n lần đoạn nghiệm dài (b - a)/2^n và sai số của trung điểm không quá (b - a)/2^(n+1); sai số lan truyền theo công
  thức bậc nhất (tổng, hiệu cộng sai số tuyệt đối; tích, thương cộng sai số tương đối; hàm: |f'| Delta). Ký hiệu ASCII
  như các tầng trước: `~` cho "xấp xỉ", `A'` cho sự kiện đối, `B \ A` cho hiệu hai tập, bảng phân phối đồng thời vẽ
  bằng ma trận `P` (hàng ứng với X, cột ứng với Y).
- **Kiểm đáp án.** Ngoài phép tính lại của bộ sinh câu (`EXPECTED`), mỗi `tools/math_verify_<môn>_t10.py` có bảng
  `HAND` tính lại bằng sympy mọi đáp số của câu viết tay (và các mệnh đề, đáp án trắc nghiệm mà máy quyết được);
  `tests/test_math_<môn>_t10.py` thử cả việc bảng đó bắt được một đáp án bị sửa sai. Việc "metric hay không" chỉ
  được kiểm bằng tìm phản ví dụ trên một lưới số hữu tỉ (không chứng minh được khẳng định đúng), nên các mệnh đề
  đúng còn dựa vào lý do một dòng trong lời giải.
- **Bảng duyệt.** `tools/reports/math_review_*.md` ở bản trước chỉ có tầng 1-3 (chưa ai dựng lại sau M11); bản
  mới dựng lại cả tầng 4-10, nên khác biệt rất lớn.

## Nhánh `toan-tu-tien` — M12: bản web (pygbag) cho điện thoại
Chi tiết, cách build và kết quả chạy thật: `docs/WEB_BUILD.md`.
- **Một chỗ chọn đường mạng:** `client/net/transport.py`. Máy tính vẫn dùng httpx + websockets trên luồng
  riêng như cũ; trình duyệt dùng `fetch` và `WebSocket` của trang (`client/net/web.py`) sau cùng giao diện
  `Api` / `WsClient`, nên không cảnh nào phải sửa.
- **Máy chủ phát luôn bản web ở `/web/`** khi đã build: trang và API cùng một địa chỉ. Gọi chéo cổng bị
  Chrome mới chặn khi trang mở bằng địa chỉ Wi-Fi (quy tắc "Local Network Access", đã thấy khi thử).
  CORS vẫn bật (`CORS_ORIGINS`, mặc định `*`, không cookie) cho ai chỉ mở trang ở chỗ khác.
- **Bài tập lập trình chạy ngay trong trang** (không có tiến trình con): stdin/stdout giả, giới hạn thời gian
  bằng bộ dò dòng lệnh, được gấp 3 lần thời gian vì dò làm Python chậm đi. Trang không có luồng, nên "luồng"
  của cảnh bài tập chạy luôn tại chỗ (trang đứng trong lúc chạy).
- **Không có thế giới LAN trên web:** trang không mở được máy chủ hay quét mạng, nên bản web luôn dùng tài
  khoản tên + mật khẩu của máy chủ thường.

## 2026-11-20: the Chinese-vocabulary game is removed

Tác giả quyết định xoá hẳn mọi thứ của trò học chữ Hán cũ ("Khu Vườn Tu Tiên") và xoá hẳn khu vườn; game bây
giờ chỉ là Toán tu tiên. Làm theo ba đợt:

- **Đợt 1 (đã gộp):** đả tọa, Thiên Kiếp, quái ngoài thế giới, câu cá, bí cảnh và thủ thành hỏi câu toán qua
  `systems/math_ask.py`; bản hỏi chữ của chúng bị xoá, cùng ải Thủ Vườn trồng cây chữ (`/td/*`, `td_bot`,
  `gen_td_levels`, Vô Tận Trận) và các phòng câu đố chữ của bí cảnh.
- **Đợt 2:** vườn chữ, khắc văn, Pháp Chữ, Sổ Phát Hiện và mọi phần chỉ dùng chữ của ong, Linh Thú, luyện đan,
  sạp, gacha, nhiệm vụ, bạn bè (mỗi phần do một agent ghi trong báo cáo của mình). Riêng Tàng Thư Các cũ: xoá
  Bách Thảo Phổ, ô tìm kiếm chữ / pinyin, Sổ Lỗi chữ, bí kíp trên kệ Thủ Thư, `/library*`, `/codex/plant`,
  `systems/library.py`, `systems/word_plants.py`, `data/plants/plant_roles.json`, các khoá `roles`,
  `idiom_skills`, `power` của `balance/td.json`. Tin `ract` của bí cảnh và đồ vật Gương Nghĩa cũng đi.
- **Đợt 3 (xong, đợt cuối):** các module chữ (`learning/wordbank, question_bank, pinyin, srs, selection`), bảng
  cơ sở dữ liệu của chữ (migration `0017_drop_word_game`), `server/data/words`, công cụ dựng từ vựng, nửa
  từ vựng của thẻ câu hỏi ở client. Chi tiết ở mục "Đợt 3" bên dưới.

Quyết định khi tách Tàng Thư Các:

- **Thứ không dính chữ thì giữ, chuyển sang `systems/books.py` (`/books`).** Kệ phổ còn Yêu Quái, Ong, Ngư, Bảo
  Vật, Linh Thú với mốc 25/50/75/100% như cũ; danh hiệu và khung avatar do các mốc ấy cho vẫn đeo được. Danh
  hiệu và khung chỉ Bách Thảo Phổ / Sổ Phát Hiện cho (Người Gieo Chữ, Bách Thảo Tiên, Người Giải Chữ, Khung
  Trúc Xanh) không còn hiện ở đâu; cờ trong `users.flags` để nguyên, không cần migration.
- **Kệ đan phương ở lại với Thủ Thư.** Nhiều đan phương đột phá (Trúc Cơ trở lên) chỉ mua được ở đây, nên bỏ kệ
  là chặn đường tu luyện. Giá không đổi.
- **Thủ Thư và phím L mở kinh thư toán trước**; đóng kinh thư là thấy kệ phổ bên dưới (mua đan phương vẫn phải
  đứng cạnh Thủ Thư).

Quyết định khi gỡ chữ khỏi luyện đan, Pháp Chữ và Khắc Văn:

- **Luyện đan chỉ còn canh lửa.** Không còn gõ pinyin tên đan, không còn quả chữ. Điểm = ba lần bấm (perfect 2,
  good 1, miss 0, tối đa 6); ngưỡng phẩm chất hạ xuống 0,8 / 0,5 / 0,15 để cùng một tay canh lửa ra đúng phẩm
  chất mà trước đây người gõ đúng hết mọi chữ nhận được (hai perfect một good vẫn là Thượng phẩm, ba good là
  Trung phẩm, một good là Hạ phẩm). Khác duy nhất: trượt cả ba giờ là Phế đan (trước còn Hạ phẩm nhờ 3 điểm
  pinyin). Tu Vi 3 mỗi chữ gõ đúng (tối đa 9) đổi thành Tu Vi cố định mỗi mẻ ra đan: hạ 3, trung 6, thượng 9
  (`balance/alchemy.json` `brew_xp`, nhân Tụ Linh).
- **Quả chữ và Linh Quả trong đan phương đổi sang thứ đang rơi/bán.** Hồi Huyết: 3 Mực Tinh + 1 Trúc Diệp Thảo;
  Hồi Khí: 2 Mực Tinh + 1 Gỗ Linh Mộc + 1 Trúc Diệp Thảo (bỏ cả Linh Mật để người mới luyện được ngay); các đan
  khác lấy Mảnh Tập Hợp, Tinh Số Phức, Lõi Ma Trận của quái lỗi sai, Mặc Linh Chi, Gỗ Linh Mộc. Hồi Huyết / Hồi
  Khí lấy 3 và 2 Mực Tinh chứ không ít hơn để giá bán đan vẫn dưới giá nguyên liệu (`test_economy`).
- **Pháp Chữ và bốn bí kíp bị xoá hẳn**; chiêu thức (M9) là kỹ năng duy nhất. Phần thưởng bí kíp của chuỗi Nhập
  Môn đổi thành đan: 2 Hồi Khí Đan, 1 Kháng Mực Đan, 1 Tụ Linh Đan, 1 Ngộ Tính Đan; quái không còn rơi bí kíp.
  Bảng `skills` để nguyên tới đợt 3.
- **Khắc Văn bị xoá hẳn.** Cột `equipment_instances.inscriptions` để nguyên (không migration) nhưng không ai đọc
  nữa, chỉ số trang bị không còn cộng chữ khắc. Bước "Chữ trên binh khí" của chuỗi Đan Đạo đổi thành "Đan hồi
  khí": luyện một mẻ Hồi Khí Đan; giữ id `dd3_khac_van` để người đang làm dở bước ấy không bị kẹt chuỗi.

Đợt 3 (phía máy chủ, dữ liệu, công cụ, tài liệu):

- **`learning/quiz.py` chỉ còn là dịch vụ phiên câu hỏi trung lập.** Không còn câu từ vựng, âm thanh câu nghe,
  sự cố sai thanh điệu, bộ đếm theo từ, handler `practice`, hệ số Gà khi ôn vườn. Loại câu nào chưa đăng ký
  cách chấm (`register_grader`) thì `create_session` từ chối ngay (`LookupError`) thay vì sau này chấm sai;
  mọi loại câu toán được `systems/math_practice.py` đăng ký. `create_session` nhận bất kỳ câu hỏi nào có
  `qtype, item_id, time_limit, answer_key, public()` (Protocol `quiz.Question`).
- **Migration `0017_drop_word_game`:** xoá bảng `words`, `plots`, `seeds`, `collection`, `fruits`,
  `crafted_sentences`, `skills`, `td_loadout`; xoá cột `equipment_instances.inscriptions`, `hive.pollen_checked_at`,
  `friendships.help_count_date`, `friendships.help_count`, `users.current_letter_id`. Hai cột mang tên cũ được
  đổi cho đúng việc chúng làm: `users.daily_new_seeds_count` → `daily_rolls_count` (số lượt gacha trong ngày),
  `tribulation_runs.words` (danh sách giữ chỗ, một phần tử mỗi câu) → `total` (số nguyên, giữ nguyên giá trị).
  Downgrade dựng lại mọi bảng (rỗng, đúng lược đồ cũ) và mọi cột (giá trị mặc định cũ); có test nâng cấp một
  cơ sở dữ liệu còn dòng trong các bảng cũ rồi hạ xuống lại.
- **Dữ liệu xoá:** `server/data/words/`, `audio/`, `sentences.json`, `tone_mishaps.json`, `combos.json`,
  `balance/garden.json`; các dạng câu Q1..Q11 và số liệu chọn từ trong `balance/quiz.json` (còn `network_grace`,
  `bot_watch`); `rewards` thừa của `balance/td.json` (thưởng nằm ở `math/td.json`); khoá `hsk` của
  `realms_cultivation.json`. Route `/quiz/{id}/audio`, `inventory.change_fruit`, `balance.garden()`,
  `sync_words` lúc khởi động. Tên máy chủ (`/server/info`, tiêu đề FastAPI, logger) là "Toán Tu Tiên".
- **Linh Quả giữ lại.** Nguồn duy nhất của nó là thu hoạch vườn, nên giờ không còn cách nào có thêm; nhưng
  Linh Quả Vụn (mồi làm từ Linh Quả) là mồi duy nhất của Cá Chép Hóa Long, và túi của người chơi cũ vẫn có thể
  còn Linh Quả. Mô tả đổi sang trung tính; cho nó một nguồn mới (rương, quái...) là việc thiết kế còn để ngỏ.
- **Công cụ xoá:** `tools/build_wordlist.py`, `apply_review.py`, `generate_audio.py`, `tools/raw/`, phần từ vựng
  của `tools/curation/` (còn `fish.json` cho `build_fish.py`) và `tools/reports/` (còn bảng duyệt câu toán).
- **Test canh "không còn chữ cũ"** giờ dùng `tests/helpers.old_script()`: chữ Hán hoặc nguyên âm có dấu
  thanh chỉ phiên âm tiếng Trung mới dùng (gạch ngang, mũ ngược; tiếng Việt không có) ở bất cứ đâu trong gói
  dữ liệu, thay cho việc liệt kê tên khoá cũ.
- **Để nguyên, có lý do:** tên trường `word` trong `td_sim.py` (bản sao y hệt ở client, là id loại tháp) và
  `td_runs.questions`; id các gian của bản đồ bí cảnh (`compose`, `sentence`, `tone`...) dùng chung với
  client và `realms.json`; mã tín hiệu LAN `khuvuon-lan` (đổi là máy cũ và mới không thấy nhau).

## 2026-11-20: rơi đồ theo tu vi

Tác giả: "từ quái và các bí cảnh đồ xịn thì càng đi lên cao ms càng mở khóa nhé k p tống hết con nào cx rơi ra đc
thì chết tôi".

- **Một mốc tu vi cho mỗi món rơi** (`server/data/loot_tiers.json`, `server/app/systems/loot.py`): "cao" là tu vi
  (cảnh giới + tầng), không phải tầng toán. Mốc được kiểm tra ở chỗ trao đồ: quái (`realtime/combat.py::_reward`,
  từng người trong tổ đội), bí cảnh (`secret_realm.claim_room`, `claim_chest`, số Mảnh Bảo Vật), hầm ngục
  (`math_dungeon._grant`), cơ duyên (`math_fortune.grant`). Món đã rơi mà chưa tới mốc không mất trong im lặng:
  gói loot có `locked` (tối đa 3) và client hiện một dòng "Tu vi chưa đủ: … (cần …)". Món quên ghi mốc: lỗi ở
  `check_all`, và khi chạy thì khoá tới tầng cao nhất (thà khoá nhầm còn hơn thả nhầm). Ghi chú lỗi sai không khoá.
- **Không phải con nào cũng rơi mọi thứ:** mỗi vùng hoang và mỗi bí cảnh có trần; `loot.validate()` (dòng mới của
  `check_all`) từ chối mọi bảng vượt trần, tính cả quái sinh ra ở đó. Trúc Cơ Đan và đan phương của nó rời Mặc Hồ
  (Rừng Mực Loang, trần Luyện Khí tầng 5) sang Đối Xứng Ma (Loạn Số Cốc).
- **Hai món mồ côi có nguồn lại, có khoá:** Mảnh Bảo Vật (Kết Đan sơ kỳ) ở rương Mặc Ảnh Động với số cũ (4 + 1 mỗi
  gian không sai); Linh Quả (Trúc Cơ sơ kỳ) ở rương Mặc Ảnh Động và Toán Trận, nên Cá Chép Hóa Long câu được lại. Luật 7
  của bí cảnh toán (`math_realm.validate`) nới đúng phần này: được trả Mảnh Bảo Vật và Linh Quả; vẫn không Tu Vi,
  không Tiên Ngọc từ rương.
- Không khoá: cửa hàng, thưởng nhiệm vụ và mốc sưu tập, gacha, chế tạo, câu cá, luyện đan, thưởng sao thủ thành.

## 2026-11-20: binh khí - năm phẩm, rơi từ quái, lò rèn nhiều bậc, sáu kỳ binh

Chủ dự án: binh khí rơi từ quái phải phát sáng nhẹ, mỗi phẩm một màu; loại binh khí quá ít; làm thật kỹ.

- **Năm phẩm, ánh sáng là màu độ hiếm.** `qualities`: hạ `ha` (Phàm, power 1.0), trung `trung` (Linh, 1.35),
  thượng `thuong` (Huyền, 1.8), cực `cuc` (Địa, 2.4), tuyệt `tuyet` (Thiên, 3.2). Id và độ hiếm là giao ước với hoạ
  sĩ và người làm hiệu ứng (`weapons.QUALITY_RARITY`, `validate()` giữ nó). Vì sao 2.4 và 3.2: bậc 2 có `atk` 24 =
  2,4 lần bậc 1, nên Mộc cực phẩm bằng Thiết hạ phẩm và Mộc tuyệt phẩm (32) ngang Thiết trung phẩm (32,4): lên phẩm
  không bao giờ vượt hẳn một bậc cao hơn.
- **Rơi từ quái, bảng ở kế hoạch, không sửa `drops` của từng con.** `weapon_drops` (thêm vào `wired_sections`):
  quái của một vùng rơi loại chính của vùng, bậc của cảnh giới vùng. Thường 3%, tinh anh 15%, trùm 100%; tỉ lệ phẩm
  thường 80/17/3/0/0, tinh anh 50/35/13/2/0, trùm 20/40/28/10/2 (hạ/trung/thượng/cực/tuyệt). `combat._reward` hỏi
  `weapons.grant_drops` sau bảng `drops` cũ (thứ tự xúc xắc của bảng cũ không đổi).
- **Luật rơi đồ theo tu vi giữ nguyên.** Phẩm bị chặn bởi tu vi nhân vật (`loot_tiers.json` `equipment_rarity`) và
  trần nơi hạ quái (`source_caps`). Bị tu vi chặn: nhận phẩm cao nhất được phép, món cao hơn vào `locked` (người chơi
  biết leo thêm thì được). Bị nơi chốn chặn: chỉ nhận phẩm cao nhất nơi ấy cho, **không** báo khoá - leo tu vi không
  mở được nó ở đây, báo thì là nói sai. Ngày nay mọi vùng Luyện Khí có trần Luyện Khí tầng 9, nên cực và tuyệt phẩm
  chỉ ra từ lò rèn; vùng Trúc Cơ sau này tự mở cực phẩm.
- **Lôi Long có thể rơi bậc 2, có khoá.** Lôi Kiếp Đài không có loại riêng: Lôi Long rơi một trong sáu loại chính,
  bậc 1 (trọng số 3) hoặc bậc 2 (trọng số 1, `tu_vi` Trúc Cơ sơ kỳ). Chưa Trúc Cơ mà xúc xắc ra bậc 2: nhận bậc 1,
  bậc 2 vào `locked`. Trùm vẫn chắc chắn rơi.
- **Tin `loot` nói món nằm đâu.** Mỗi món trong `equipment` (cả đồ cũ) có thêm `item`, `quality`, `quality_vi`,
  `weapon` (bool: ô vũ khí), `weapon_info` (khối binh khí), `x`, `y` (chỗ quái chết, lệch vài pixel khi nhiều món).
  Khối `weapon` của dạng `equipment` đổi thành bool **chỉ trong tin `loot`** (client hôm nay chỉ đọc `name_vi`,
  `rarity_vi`, `color`); món đã cấp ngay nên bỏ đi không mất. Hình trên đất và ánh sáng: đợt sau.
- **Lò rèn bốn bậc.** `crafting.json` `upgrades`: hạ→trung (`nang_pham`, Đạo Thụ Luyện Khí 4, phí 40), trung→thượng
  (Đạo Thụ Luyện Khí 7, tu vi Luyện Khí 6, phí 150), thượng→cực (Đạo Thụ và tu vi Trúc Cơ 1, phí 500), cực→tuyệt (Đạo
  Thụ Kết Đan 1, tu vi Kết Đan sơ kỳ, phí 1500). Nguyên liệu chỉ là thứ quái Luyện Khí rơi thật (Lõi Ma Trận, Thiên
  Tằm Ti, Mặc Linh Chi, Ấn Rương Đề, Tinh Số Phức), số lượng tăng dần, vì chưa có nguyên liệu cao hơn nào rơi; khi
  có, đổi ở đây. `validate()` đòi chuỗi liền (mỗi bước đúng một phẩm), phí tăng, mốc không lùi, nguyên liệu rơi
  không muộn hơn lúc bước mở. Bước đầu giữ mốc tu vi `pham_nhan` như trước (Đạo Thụ đã chặn nó).
- **Sáu kỳ binh, chờ hình.** `kich` Kích (Đại Số, Kiếm Trủng Sơn, slash, tầm 34, 0,75 s, ×1,2), `roi` Roi (Giải
  Tích, Lưu Vân Cốc, slash, 44, 0,65 s, ×0,9), `am_khi` Ám Khí (Xác Suất, Vạn Tượng Trạch, shoot, 52, 0,45 s,
  ×0,75), `luan` Luân (Thuật Toán, Mê Đồ Lâm, shoot, 48, 0,85 s, ×1,1), `phu` Phủ (Lập Trình, Thiên Công Phường,
  slash, 22, 1,0 s, ×1,45), `cam` Cầm (Thực Chiến, Linh Xạ Nguyên, cast, 50, 0,9 s, ×1,05). `drop_only`: chỉ tinh
  anh (5%) và trùm (35%) của vùng rơi, hiếm hơn loại chính. Mỗi loại có `status` `co` / `cho_hinh`; sáu kỳ binh ở
  `cho_hinh`: là dữ liệu đã kiểm, không rơi, không phải trang bị, `check_all` và `test_art2` bỏ qua hình của chúng.
  Hình vào thì chỉ đổi `status` (test `test_flipping_the_status_is_the_only_change_needed`). Riêng client:
  `client/scenes/world.py` `PLAN_WEAPON_RANGE` / `PLAN_WEAPON_LOOK` (ngắm tự động, hình vẽ bằng code khi tắt v2) do
  người làm hiệu ứng giữ, cần thêm sáu dòng; thiếu thì loại ấy ngắm với tầm mặc định.

## Bách thú: mười ba quái và sáu linh thú (2026-11-20)

- **Quái mới mỗi vùng một thường một tinh anh** (Lôi Kiếp Đài: hai Lôi Linh): Thiết Giáp Thú, Vong Hồn Kiếm Sĩ, Vân
  Điệp, Lôi Ưng, U Minh Đăng, Huyết Ngạc, Hoa Yêu, Bạch Viên, Cơ Quan Thú, Lò Linh, Thảo Nhân, Xích Diễm Mã, Lôi
  Linh (`server/data/math/monsters.json`, thêm trước `loi_long`, không sửa dòng cũ). Mỗi con hỏi ít nhất một nút
  mà quái cùng vùng cùng bậc chưa hỏi. Số và đồ rơi theo quái cũ cùng bậc; chỉ dùng nguyên liệu đã có bậc trong
  `loot_tiers.json`, không thêm vật phẩm mới. Thêm 4-5 con mỗi vùng (vùng đông nhất, Kiếm Trủng Sơn, từ 36 lên 40).
- **Nhịp đòn của tinh anh**: `attack_shape` nay nhận một danh sách hình dùng lần lượt (một chuỗi vẫn là một hình
  cố định). `math_tree` kiểm từng hình là hình của `telegraph_shapes`.
- **Lôi Linh** không chủ động, Công 6, ở hai mép Lôi Kiếp Đài cách vùng Lôi Long hơn tầm nhìn của nó (96 px).
- **Hình tạm**: quái mới mượn bộ hình gần nhất có sẵn trong `wiring.json` `monsters`; con bay mượn hình đang ở
  `monster_float`. Khi hình thật về, đổi dòng của nó thành `<id>` (tinh anh: `<id>_di` nếu có) và thêm id ấy vào
  `monster_float` cho bốn con bay.
- **Sáu linh thú, sáu quà mới, chờ hình**: Ngọc Thố (`heal_on_right` 5% sinh lực mỗi Phản Đòn), Tầm Bảo Thử
  (`stone_bonus` +20% linh thạch), Bích Nhãn Kim Thiềm (`drop_luck` tỉ lệ rơi ×1,15, cổng tu vi vẫn chặn), Bạch Hổ
  Con (`atk_bonus` Công +8%), Cửu Vĩ Hồ (`xp_bonus` +10% tu vi câu toán đúng ngoài Đạo Thụ), Kim Sí Điểu
  (`glide_range` lướt xa +40%, tức 112 px). Quà nhỏ: `math_tree` đòi `0 < value <= 0,5`. Mỗi vùng một con mới;
  hiện từ tầng 3, 4, 5, 6, 8, 9; Kim Sí Điểu cần Đạp Kiếm Lướt (mỏm đá trong mây cạnh Đao, ô 21,3). `status` mới
  `cho_hinh` cho linh thú, nghĩa như của binh khí: kiểm đủ như con đã dựng, không có trong game, quà đọc ra 0,
  `check_all` bỏ qua hình. Hình vào thì chỉ đổi `status` (`server/tests/test_bestiary.py`). Một chỗ đứng không được
  trùng chỗ binh khí hay linh thú khác (`math_tree` kiểm).
- **Chỗ tác dụng của quà**, mỗi chỗ một lời gọi: `combat.parry_heal` trong `_parry`, `beasts.loot_gift` cuối
  `combat._loot_bonus`, `beasts.stat_gift` trong `cultivation.current_stats` (sau `stats_for`), nhánh `xp_bonus`
  trong `pets.on_math_answer`, `abilities.glide_max_px` cho lướt và cho số gửi client.
