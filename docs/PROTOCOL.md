# Giao thức WebSocket (thế giới chung)

Đường dẫn: `ws://<máy chủ>/ws` (hoặc `wss://` khi máy chủ chạy HTTPS, ví dụ qua Cloudflare Tunnel).
Mỗi gói tin là **một object JSON**, trường `t` cho biết loại. Phiên bản giao thức hiện tại: **3**
(3 = giai đoạn 4: chiến đấu; `me` và trạng thái thực thể có thêm máu/khiên)
(`server/app/config.py` và `client/config.py`; `/server/info` trả `protocol_version`).

Định nghĩa trong code: `server/app/realtime/protocol.py` (kiểm tra gói tin từ client), xử lý ở
`world.py`, `zone.py`, `chat.py`, `combat.py`, `ai.py`. Mọi con số dưới đây nằm trong
`server/data/balance/world.json`, `social.json` và `combat.json`.

## Kết nối

1. Client mở WebSocket, gói tin **đầu tiên** phải là `hello` (trong 10 giây):

   ```json
   {"t": "hello", "v": 4, "token": "<JWT lấy từ /auth/login>"}
   ```

2. Server trả `welcome`, hoặc `error` rồi đóng kết nối:

   | `code` | mã đóng | ý nghĩa |
   |---|---|---|
   | `version` | 4002 | client cũ, cần cập nhật |
   | `bad_token`, `token_expired` | 4003 | đăng nhập lại |
   | `no_character` | 4004 | chưa tạo nhân vật |
   | `banned` | 4003 | tài khoản bị khóa |

   ```json
   {"t": "welcome", "v": 4, "you": {"uid": 7, "id": "p7", "name": "Tiểu Trúc"},
    "zone": "abode", "st": 1234.5, "day": 0.42, "day_length": 7200}
   ```

   `zone` là nơi nhân vật đang đứng: `abode` (động phủ, riêng tư, không đi qua WebSocket) hoặc một vùng của
   thế giới (nếu lần trước thoát ở đó, hoặc vừa rớt mạng chưa quá 30 giây). `st` là đồng hồ server (giây),
   `day` là vị trí trong ngày của game (0 = nửa đêm, 0,5 = giữa trưa; một ngày game = 2 giờ thật).

3. **Một tài khoản một kết nối**: kết nối mới làm kết nối cũ nhận `{"t":"kicked","reason":"elsewhere"}` (mã 4001).

4. **Heartbeat**: client gửi `{"t":"ping","c":<giờ client>}` mỗi 15 giây khi không có gì khác để gửi; server trả
   `{"t":"pong","c":...,"st":...}`. Im lặng quá 45 giây thì server ngắt (`kicked`, `reason: timeout`, mã 4005).

5. **Giới hạn**: tối đa 30 gói tin/giây (vượt thì `kicked`, `reason: flood`, mã 4008), mỗi gói tối đa 4 KB.

6. **Rớt mạng**: nhân vật đứng yên 30 giây rồi mới rời khỏi vùng. Kết nối lại trong lúc đó thì gửi
   `join` với `via: "resume"` để nhận lại đúng chỗ. Client tự kết nối lại, chờ 1, 2, 4… tối đa 30 giây.

## Client → server

| `t` | Trường | Ý nghĩa |
|---|---|---|
| `ping` | `c` (số, tùy chọn) | heartbeat |
| `join` | `zone`, `via`: `abode` \| `portal` \| `resume` | vào một vùng (xem dưới) |
| `in` | `s` (số thứ tự tăng dần), `k`: `[[dx, dy, ms], …]` | ý định di chuyển |
| `face` | `f`: `down` \| `up` \| `left` \| `right` | quay mặt, không đi |
| `channel` | `n` | đổi kênh trong vùng hiện tại (`n` = số kênh có sẵn, hoặc số lớn nhất + 1 để mở kênh mới) |
| `chat` | `ch`: `world` \| `zone` \| `friend` \| `party`, `text`, `to` (đạo hiệu của bạn, khi `friend`) | chat |
| `atk` | `id` (quái) | đánh thường (giai đoạn 4); server kiểm tra tầm vũ khí và thời gian hồi |
| `dodge` | `s` (số thứ tự kế tiếp của dòng `in`), `dx`, `dy` (-1/0/1) | **Né Đòn** (luật vùng hoang, xem dưới): một cú lướt xếp vào hàng di chuyển dưới số `s` |
| `glide` | `s` (số kế tiếp của dòng `in`), `x`, `y` (chỗ đáp client đã chọn) | **Đạp Kiếm Lướt** (thần thông, xem dưới) |
| `ride` | `s` (số kế tiếp của dòng `in`), `on` (true/false) | **Cưỡi linh thú**: lên / xuống thú cưỡi đang đeo |
| `fly` | `s` (số kế tiếp của dòng `in`), `on` (true/false) | **Ngự kiếm**: đạp kiếm bay lên / hạ xuống (xem dưới) |
| `tran` | — | **Bày pháp trận** dưới chân |

### Vào vùng (`join`)

- `via: "abode"`: từ cổng tre của động phủ, chỉ dẫn tới `truc_lam_thon` (xuất hiện ở điểm `from_abode`).
- `via: "portal"`: nhân vật phải **đứng trong cổng** (vùng `portal` của bản đồ Tiled) dẫn tới vùng đó. Nếu
  vài bước cuối còn trong hàng đợi, server chờ chúng (tối đa 1 giây) rồi mới quyết định. Cổng `to_abode`
  đưa về động phủ: server trả `zone` với `"zone": "abode"`.
- `via: "resume"`: quay lại vùng đã lưu (hoặc nhân vật còn đứng đó sau khi rớt mạng).
- **Cảnh giới**: không vào được vùng có cảnh giới khuyến nghị cao hơn mình quá 1 bậc (`data/zones.json`,
  `realm_gate_margin`), lỗi `realm_too_low`.
- Mỗi vùng chia **kênh**, tối đa 40 người/kênh; vào vùng thì được xếp vào kênh số nhỏ nhất còn chỗ, đầy hết
  thì tự mở kênh mới (tối đa 20). Kênh phụ trống tự đóng.

### Di chuyển (`in`)

Mỗi khung hình client ghi lại phím hướng đang giữ (`dx`, `dy` ∈ {-1, 0, 1}) và số mili giây của khung đó, rồi
gom lại gửi tối đa 20 lần/giây:

```json
{"t": "in", "s": 41, "k": [[0, -1, 17], [1, -1, 16], [1, -1, 17]]}
```

Server là bên quyết định vị trí: mỗi tick (20 lần/giây) nó áp dụng các bước bằng **đúng cùng hàm**
`movement.step` (tốc độ 74 px/giây, đi chéo × 0,7071, va chạm theo từng trục với khung chân 10 × 6 px).
Chống hack tốc độ: mỗi người có một "ngân sách thời gian" tăng theo giờ thật (tối đa 600 ms tích lũy); một
gói chỉ được áp dụng khi ngân sách đủ, một gói tối đa 250 ms, hàng đợi tối đa 1,5 giây. Bước sai luật bị bỏ,
và client tự kéo về vị trí đúng nhờ snapshot. Gói trùng hoặc số thứ tự cũ bị bỏ qua.

## Server → client

| `t` | Trường | Khi nào |
|---|---|---|
| `welcome` | xem trên | sau `hello` |
| `zone` | `zone`, `name_vi`, `safe`, `channel`, `channels` [`{n, players, cap}`], `x`, `y`, `f`, `ack`, `st`, `day`, `combat` | vừa vào vùng / đổi kênh / về động phủ. `combat` = luật vùng hoang (xem dưới) hoặc `null` (bí cảnh, động phủ) |
| `snap` | `st`, `ack`, `me` [`x`, `y`, `facing`, …, ong], `add`, `e`, `rm`, `fx` | 10 lần/giây khi đang ở trong vùng |
| `chat` | `ch`, `from` {`uid`, `id`, `name`}, `text`, `ts`, `to` (friend), `zone`/`channel` (zone) | tin nhắn |
| `chat_history` | `ch` (`world` \| `zone`), `items` [chat] | sau `welcome` và khi vào vùng |
| `friend` | `event`: `online` \| `offline` \| `request` \| `accepted` \| `helped`, `user` {`uid`, `name`}, `reward` | bạn bè |
| `pong` | `c`, `st` | trả `ping` |
| `error` | `code`, `message_vi` | thao tác bị từ chối |
| `kicked` | `reason` (`elsewhere`, `timeout`, `flood`, `banned`, `admin`), `message_vi` | sắp bị ngắt |
| `notice` | `text`, `kind` (`announce` \| `maintenance`, chỉ khi quản trị viên gửi) | thông báo |
| `admin` | `ok`, `lines` [chuỗi] | trả lời lệnh `/admin` (giai đoạn 10) |
| `q` | `mid` (quái), `q` (câu hỏi như REST, `context: "combat"`), `first_meet`, `hit` | **Vấn Đạo** (bí cảnh): câu hỏi phá Mặc Thuẫn. Ở vùng hoang: câu của **một đòn vừa trúng**, `hit` = `{dmg, monster_vi, rest}`. Từ lúc gửi tới hạn trả lời nhân vật có **Hộ Thể** (không bị đánh, không di chuyển) |
| `dodge` | `ok`, `ready_in` hoặc `code` (`cannot` \| `answering` \| `locked` \| `cooldown`), `message_vi` | trả lời gói `dodge` |
| `glide` | `ok`, `x`, `y`, `ms` hoặc `code` (`cannot` \| `answering` \| `glide_locked` \| `cooldown` \| `too_far` \| `too_short` \| `bad_landing` \| `blocked`), `message_vi` | trả lời gói `glide`: từ chối ngay, hoặc khi server tới số `s` trong dòng di chuyển (lướt xong hay bị từ chối ở đó) |
| `ride` | `ok`, `on`, `mult` hoặc `code` (`cannot` \| `ride_locked` \| `no_mount`), `message_vi` | trả lời gói `ride`; cũng gửi khi tháo thú cưỡi |
| `tran` | `ok`, `ready_in` hoặc `code` (`cannot` \| `answering` \| `formation_locked` \| `cooldown` \| `flying`), `message_vi` | trả lời gói `tran` |
| `fly` | `ok`, `on` (0 \| 1 \| 2), `why` (`up` \| `land` \| `gauge` \| `fall` \| `knocked` \| `gone`), `x`, `y`, `gauge` hoặc `code` (`cannot` \| `answering` \| `fly_locked` \| `riding` \| `struck` \| `gauge_low` \| `no_landing`), `message_vi`, `on` | trả lời gói `fly` (từ chối ngay, hoặc `no_landing` khi server tới số `s`); cũng gửi khi server tự hạ người bay: cạn kiếm khí (`gauge`; trên nước thì `fall`: đưa về bờ), trúng đòn lúc đang bay lên (`knocked`), rớt mạng / đổi kênh (`gone`) |
| `q_end` | `sid`, `reason`: `broken` (người khác vừa phá khiên) \| `killed` \| `gone` \| `dead` | câu hỏi không cần trả lời nữa |
| `dead` | `respawn_in` | hết máu; sau đó server tự đưa về điểm hồi sinh (một gói `zone` mới) |
| `xp_lost` | `lost` | Tu Vi mất do chết |
| `loot` | `monster`, `stones`, `spirit_stones` (số dư mới), `items`, `equipment` [trang bị nằm trên đất, xem dưới], `kills`, `xp`, `quests`, `locked`? | phần thưởng khi hạ quái (gửi cho mọi người đã đánh trúng). `locked` = `[{name_vi, need_vi}]` (tối đa 3): món rút ra mà tu vi chưa cho nhận |
| `stats` | `realm`, `stage`, `stats`, `stage_up`, `hp`, `max_hp`, `combat` | chỉ số đổi (lên tầng, đổi trang bị); `combat` như trong `zone` (Né Đòn có thể vừa mở) |
| `quest` | `event: "done"`, `quest` | một nhiệm vụ vừa đủ điều kiện |
| `achievement` | `unlocks` [`{key, id, tier, tiers, name_vi, tier_name_vi, category, icon, points, title, hidden, reveal_vi}`] | Thành Tựu: một hay nhiều bậc vừa đạt, ở bất cứ đâu (động phủ, thế giới, bí cảnh, sau một gọi REST). Chỉ gửi **sau khi** giao dịch đã commit; client hiện dải vàng từng cái một rồi gửi `POST /achievements/seen`. Không trực tuyến lúc đạt thì `GET /achievements/new` trả lại lúc đăng nhập (`docs/THANH_TUU.md`) |
| `act_fail` | `code`: `too_far` \| `no_target` | đòn đánh bị từ chối (đang hồi chiêu thì bỏ qua im lặng) |

**Trang bị rơi trong `loot`** (binh khí của Thiên Địa Đồ rơi từ quái, `world_plan.json` `weapon_drops`, và đồ cũ
của bảng `drops`). Món đã được **cấp ngay** vào túi khi gửi tin (người chơi bỏ đi cũng không mất); các trường dưới
đây để client vẽ nó nằm trên đất chỗ quái chết, phát sáng theo màu phẩm, tới khi người chơi đi qua. Mỗi mục của
`equipment` là dạng `equipment` của `GET /inventory` (`id`, `item_id`, `name_vi`, `slot`, `rarity`, `rarity_vi`,
`color`, `stats`, `enhance`...) cộng thêm:

| Trường | Nghĩa |
|---|---|
| `item` | id món (= `item_id`; binh khí là `<loại>_<bậc>`, `kiem_1`) |
| `name_vi` | tên hiện (Mộc Kiếm) |
| `rarity` | độ hiếm: `pham`, `linh`, `huyen`, `dia`, `thien` |
| `color` | màu của độ hiếm (`#7D7468`, `#6A994E`, `#4A7CC8`, `#8E5AC8`, `#C99A3A`): màu phát sáng |
| `quality` | phẩm của binh khí: `ha`, `trung`, `thuong`, `cuc`, `tuyet` (cùng thứ tự với độ hiếm); `null` với đồ cũ |
| `quality_vi` | Hạ phẩm ... Tuyệt phẩm; `null` với đồ cũ |
| `weapon` | `true` khi món nằm ở ô vũ khí (binh khí của Thiên Địa Đồ, cả Kiếm Gỗ Đào cũ); `false` với nhẫn, áo... |
| `weapon_info` | chỉ với binh khí của Thiên Địa Đồ: khối `weapon` của `GET /weapons` (loại, bậc, phẩm, Công, hiệu ứng) |
| `x`, `y` | toạ độ thế giới (pixel) nơi món nằm: chỗ quái chết, hơi lệch khi một con rơi nhiều món (lệch tối đa 10 px ngang, 8 px dọc, không hai món trùng chỗ); `null` khi server không biết chỗ |

Client hiện tại chỉ hiện thông báo (`name_vi`, `rarity_vi`, `color`) rồi tải lại túi; hình nằm trên đất và ánh sáng
là việc của đợt sau.

Câu trả lời của `q` gửi qua REST `POST /quiz/answer` như mọi câu hỏi khác; server chấm, rồi áp kết quả vào trận
đấu trong bộ nhớ ngay lập tức. Hết giờ mà không trả lời thì vòng tick tự chấm là sai.

### Snapshot

```json
{"t": "snap", "st": 1290.15, "ack": 41, "me": [452.0, 512.3, 1, 88.0, 120.0, 40.0, 60.0],
 "add": [{"id": "p9", "k": "p", "uid": 9, "n": "Lão Mai", "ap": {"hair_color": "#8E8E8E", "hair_style": "ngan", "body": "nam"},
          "realm": "pham_nhan", "stage": 3, "x": 470.0, "y": 500.0, "f": 0, "m": 0, "hp": 100, "wp": "brush"},
         {"id": "m1_3", "k": "m", "type": "ink_slime", "n": "Mực Con", "rank": "normal",
          "x": 300.5, "y": 260.1, "f": 2, "m": 1, "hp": 100, "sh": 1, "alive": 1}],
 "e": [["p12", 520.25, 410.0, 3, 1, 100], ["m1_3", 301.0, 262.4, 2, 1, 64, 0, 1]],
 "rm": ["p4"],
 "fx": [{"k": "hit", "id": "m1_3", "v": 46, "c": 1, "by": "p7", "x": 301.0, "y": 262.4, "sh": 0}]}
```

- `me` = `[x, y, hướng, máu, máu tối đa, linh lực, linh lực tối đa, ong]`; `ong` (bản 4) là danh sách ong hộ vệ của
  mình `[id, loài, máu, máu tối đa, giây còn nghỉ trong tổ, id quái đang chích]`.
- Người chơi trong `add` có `stage` = tầng của cảnh giới `realm` (0 khi không có tầng): client dùng `realm` + `stage`
  để vẽ kiếm khí theo tu vi của người ấy (chỉ là hình ảnh; client cũ bỏ qua khóa này).
- Đại Địa Đồ (2026-11-21): quái trong `add` đứng trong một khu chia dải tu vi của vùng đất lớn có thêm `kv` = dải của
  nó (1 Ngoại Vi, tầng 1-3; 2 Trung Vực, tầng 4-6; 3 Thâm Xứ, tầng 7-9; xem `server/app/realtime/dia_do.py` và
  `docs/DAI_DIA_DO.md`). Quái ở bản đồ không chia dải không có khóa này. Máu, công, thủ, tu vi và linh thạch của nó
  đã nhân theo dải (`server/data/math/dia_do.json`); client có thể vẽ dấu dải cạnh tên, client cũ bỏ qua khóa này.
- Trong `e`, người chơi là `[id, x, y, hướng, đang đi, %máu, ong]` với `ong` = `[[loài, %máu, id quái đang chích hoặc "", đang nghỉ 0/1], …]`
  (cũng có trong `add` dưới khóa `bees`); quái là `[id, x, y, hướng, đang đi, %máu, khiên, còn sống]`.
- `fx` (chỉ có khi có chuyện xảy ra, lọc trong bán kính `event_radius`): `hit` (quái trúng đòn, `c` = chí mạng),
  `shield` (`on` 0 = vỡ, 1 = mọc lại), `atk` (vung vũ khí), `tele` (quái sắp đánh vào vòng `r` sau `d` giây),
  `mk` (người chơi trúng Mặc Kích; đòn thường của quái vào người chơi cũng là `hit`), `heal` (`q` = 1 nếu là linh lực), `skill` (`s` = pháp),
  `die`. Bản 4 thêm: `hit` có `b` = loài ong khi ong hộ vệ chích (`by` là chủ ong), `ink` (Ong Thư Pháp viết chữ,
  `s` = loài), `stun` (quái bị choáng `d` giây), `bee_down` (ong của `id` bị hạ, bay về tổ 60 giây), `heal` có `b` = 1
  khi ong hồi máu cho chủ.
- Luật vùng hoang thêm: `tele` có `sh` (`circle` \| `cone` \| `line`); với `cone`/`line` thì `x, y` là gốc (chỗ con
  quái), `a` là hướng (độ, trục x sang phải, y xuống), `r` là tầm, `deg` là độ mở của hình quạt, `w` là bề ngang
  của đường thẳng. Client cũ không biết `sh` vẫn vẽ được một vòng tròn. `struck` (`id` = người vừa trúng đòn,
  `by` = quái: thẻ câu hỏi sắp tới), `parry` (Phản Đòn: `id` = quái, `by` = người, `px, py` = chỗ người ấy, `st` =
  giây choáng), `gb` (trả lời sai: đòn trúng thẳng vào người `id`, `v` máu mất), `dodge` (`id` bắt đầu lướt theo
  `dx, dy`), `dodged` (khoảnh khắc bất khả xâm phạm của Né Đòn đỡ được một đòn).

### Luật vùng hoang: chỉ hỏi khi bị quái đánh trúng

Phần `combat` của `server/data/math/world_plan.json` (nối vào game qua `wired_sections`); mọi con số đọc từ đó.
Bí cảnh vẫn theo Vấn Đạo ở trên.

- `zone.combat` = `{"rule": "on_hit", "rest": giây nghỉ, "dodge": {"ok", "unlock": {"realm", "stage"}, "dash_px",
  "dash_ms", "cooldown", "iframes", "step_ms"}}`. Client dùng đúng các số này để đoán trước cú lướt.
- Chiêu thức chỉ ra được từ sáu ô Công Pháp (`not_slotted` nếu không). Sự kiện `mskill` của Chiêu Thức II mang thêm `hits[[eid, x, y]]`, `ex, ey, w` (đường thẳng) và `d` (thời gian băng/trói/dải cháy/chuông/kiếm vực); dải cháy và kiếm vực tiếp tục chém theo nhịp bằng các sự kiện `hit` thường (chi tiết: `docs/API.md`, mục chiêu thức).
- Đánh thường (`atk`) và chiêu thức (`mskill`) không hỏi gì. Quái thường không có Mặc Thuẫn; tinh anh và thủ
  lĩnh có, và khiên chỉ vỡ khi Phản Đòn.
- Quái ra đòn có báo trước (`tele`). Đòn rơi xuống người đang đứng trong vùng: trong lúc Né Đòn còn bất khả xâm
  phạm thì `dodged`; trong thời gian nghỉ (sau mỗi câu) thì mất nửa máu, không hỏi; còn lại thì `struck`, rồi gói
  `q` có `hit`. Trả lời qua `POST /quiz/answer` như mọi câu.
- **"Trận đấu dừng lại" chỉ dừng cho người bị hỏi.** Từ lúc trúng đòn tới khi trả lời (hoặc hết giờ) người ấy có Hộ
  Thể: không mất máu, không đi, không đánh, không né, không ra chiêu, và không con quái nào chọn họ làm mục tiêu.
  Thế giới không dừng: người khác trong vùng vẫn đánh tiếp, kể cả đánh chính con quái ấy, và nó quay sang đánh họ.
  Đòn đang báo trước vẫn rơi xuống những người khác đứng trong vùng. Không ai trả lời hộ ai: câu đúng của người
  này không đóng câu của người kia.
- `dodge` đi cùng dòng `in`: client gửi hết bước đang gom rồi gửi `{"t": "dodge", "s": <số kế tiếp>, ...}` và tự
  đi trước cú lướt (các bước `step_ms` mili giây, tốc độ `dash_px / dash_ms`). Bị từ chối thì số `s` vẫn được
  nhận (một bước rỗng) nên các bước sau không lệch.

### Linh thú và thần thông Luyện Khí (Thiên Địa Đồ)

Phần `beasts`, `beast_taming` và các thần thông trong `unlocks` của `world_plan.json` (`wired_sections`: `beasts`,
`abilities`). "Mở" nghĩa là tầng trên Đạo Thụ đủ (không phải cảnh giới nhân vật). Không có trong bí cảnh.

- `zone.abilities` = `{"thu_phuc_linh_thu": {...}, "phap_tran": {..., "radius", "seconds", "cooldown", "fx"},
  "dap_kiem_luot": {..., "max_px", "min_px", "ms", "cooldown", "over" (tên ô lướt qua được), "sheet"},
  "cuoi_linh_thu": {..., "mult" (tốc độ thú cưỡi đang đeo, 0 = không cưỡi được), "riding"}}`, mỗi mục có `ok`,
  `name_vi`, `unlock` {`realm`, `stage`}; `null` trong bí cảnh. `zone.formations` = các pháp trận đang có
  `[{x, y, r, left, by}]`.
- **Linh thú** là một quái trong `add` có `"beast": 1` và `need` (số Phản Đòn để thu). Server chỉ gửi nó cho
  người đủ tầng (và có thần thông nó cần, chưa thu nó); với người khác nó không tồn tại. Nó đánh theo luật vùng
  hoang. `fx` thêm: `tame` (`id` = linh thú, `by` = người, `n`/`need` = đã đếm / cần, `ok` = 1 khi nó chịu phục),
  `seal` (đã phong ấn), `fire` (đòn phản của người đeo Hỏa Tước). Kết quả của câu trả lời (`combat` trong
  `POST /quiz/answer`) có `tame` = `{beast, name_vi, n, need, yielded}` khi đòn là của linh thú, `fire`, và
  `guarded` (đeo Huyền Quy, trả lời sai), và `healed` (Phản Đòn: số sinh lực Ngọc Thố vừa hồi, 0 khi không đeo;
  kèm `fx` `heal` như mọi lần hồi máu). `dap_kiem_luot.max_px` là tầm lướt *của người ấy* (xa hơn khi đeo Kim Sí
  Điểu, quà `glide_range`); server kiểm lướt bằng đúng số ấy. Phong ấn bằng REST `POST /beasts/seal` (`docs/API.md`).
- `glide`, `ride` đi trong dòng `in` như `dodge`: client gửi hết bước đang gom, rồi gói có `s` = số kế tiếp, và tự
  đoán trước (lướt: đặt mình ở chỗ đáp; cưỡi: đi bằng tốc độ `74 × mult` từ bước ấy). Chỗ đáp do client chọn
  bằng đúng hàm của server (`realtime/glide.py`, bản chép `client/engine/glide.py`); khi tới số `s`, server kiểm lại
  từ chỗ người ấy thật sự đứng. `fx`: `glide` (`id`, `x0, y0` → `x, y`, `ms`), `ride` (`id`, `on`), `tran` (`by`,
  `x, y, r`, `d` giây, `fx`). Người cưỡi có `"rd": 1` trong `add`.
- **Ngự kiếm (2026-11-20)**: `fly` cũng đi trong dòng `in`. Từ số `s` ấy, các bước sau đó được **bay**: tốc độ
  `74 × speed_mult` của bậc, mỗi bước kiểm bằng `glide.fly_step` (qua ô nước và vực, không qua tường, cây, nhà);
  client đoán trước bằng đúng hàm ấy. Bậc 1 (`dap_kiem_luot.flight`) có thanh kiếm khí: cạn trên không thì server
  hạ xuống. Bậc 2 (`ngu_kiem_phi_hanh.flight`, Trúc Cơ) không cạn. `snap.me` thêm hai số cuối: `[..., ghost, fly
  (0/1/2), gauge (giây còn lại)]`; client phát lại các gói `fly` chưa xác nhận từ trạng thái ấy. Người bay có
  `"fl": 1|2, "fs": "<phi_kiem_n>"` trong `add` (người tới sau cũng thấy); `fx`: `fly` (`id`, `on`, `why`, `x, y`,
  `sw` = phi kiếm; `fall` thêm `x0, y0` = chỗ đang treo trên nước), `soar` (`id`, `by`: đòn dưới đất trượt qua
  người bay), `glide` thêm `sw`. Trên không: `atk` trả `act_fail` `flying`; `dodge`, `mskill`, `ride`, `glide`,
  `tran` và phong ấn trả `code` `flying`. Gói `zone`: `abilities.dap_kiem_luot.flight` = `{level, levels[1..2]
  {speed_mult, lift, rise, over, gauge}, gauge_max, refill, min_gauge, hit_lock, sword, flying, gauge_now}`, và
  `abilities.ngu_kiem_phi_hanh` (`ok`, `unlock`). Không cần tăng `PROTOCOL_VERSION`: client cũ bỏ qua số và khoá
  mới, và không bao giờ gửi `fly`.
- Quái đứng trong một pháp trận lúc ra đòn thì `tele.d` dài hơn (`windup_mult`).

### Ong hộ vệ (bản 4, giai đoạn 5)

Server mô phỏng ong như mọi thứ khác: client không gửi gì về ong, chỉ vẽ. Mỗi người mang theo các ong vai trò
`guard` (số lượng theo cảnh giới). Ong chỉ chích quái **đã mất Mặc Thuẫn** trong bán kính `guard.range` quanh chủ
(ưu tiên con chủ đang đánh); con quái bị chích quay sang đánh chủ, và phần thưởng khi hạ thuộc về chủ. Đòn của quái
khi rơi xuống cũng trúng những con ong đang chích nó; ong hết máu bay về tổ nghỉ 60 giây. Vị trí bay của ong
(đường cong quanh chủ hoặc quanh quái) do client tự vẽ (`client/engine/beeflock.py`).
- `me`: vị trí thật của chính mình sau khi server áp dụng đến gói `ack` (số chính xác, không làm tròn).
  Client đặt nhân vật về đó rồi **áp dụng lại** các gói chưa được xác nhận: vì cùng một hàm, kết quả trùng với
  vị trí đã dự đoán, nên bình thường không thấy giật.
- **Vùng quan tâm**: chỉ gửi những thứ nằm trong 3 × 3 ô lưới, mỗi ô 16 × 16 tile (256 px) quanh người chơi.
- **Chỉ gửi phần thay đổi**: `add` là thứ mới lọt vào tầm nhìn (đủ thông tin), `e` là `[id, x, y, hướng, đang đi]`
  của thứ đã biết mà vừa đổi, `rm` là thứ đã ra khỏi tầm nhìn hoặc rời vùng. Hướng: 0 xuống, 1 lên, 2 trái, 3 phải.
- Người chơi khác và quái được vẽ **trễ 100 ms**, nội suy giữa hai snapshot (`client/net/interpolation.py`).
- `id` người chơi là `p<user_id>`; quái `m<kênh>_<số>`.
- Quái chết vẫn nằm trong snapshot với `alive = 0` cho tới khi mọc lại (client làm mờ).

## Chat

- `world`: mọi người đang online; `zone`: những ai ở cùng kênh của vùng; `friend`: một người bạn đang online
  (theo đạo hiệu, không phân biệt hoa thường); `party`: chưa có tổ đội (`no_party`).
- Tối đa 200 ký tự, mỗi người một tin mỗi 2 giây (`chat_too_fast`, có `wait`), bộ lọc từ tục
  (`server/data/banned_words.txt`, từ bị thay bằng `***`), người bị cấm chat nhận `chat_banned`.
- Người bạn đã chặn (`POST /blocks`) không bao giờ đến được bạn, ở mọi kênh, kể cả lịch sử chat.

## Lưu dữ liệu

Vị trí và vùng của nhân vật ghi vào bảng `characters` theo lô: ngay khi đổi vùng, khi nhân vật rời thế giới
(sau 30 giây rớt mạng), mỗi 60 giây cho những ai đã di chuyển, và khi tắt máy chủ. Không có truy vấn DB nào
trong vòng tick.


## Giai đoạn 8

- Thực thể người chơi trong `snap.add` có thêm `"pet"`: loài Linh Thú đang đeo (`null` nếu không). Client vẽ con vật
  chạy theo sau người đó (hình lấy từ `looks` của `GET /pets`). Đổi pet thì máy chủ gửi lại `add` của người đó cho mọi
  người đang nhìn thấy. Phiên bản giao thức không đổi (trường mới, client cũ bỏ qua).
- Thông báo bạn bè mới: `{t: "friend", event: "gift", item, name_vi, qty, user{uid, name}}`.
- **Linh căn (2026-11-20):** thực thể người chơi trong `snap.add` có thêm `"lc"`: chỉ số giai của linh căn đang
  mang (1 Phàm … 9 Hỗn Độn, 0 = chưa trắc linh) để client vẽ một dấu theo màu giai (màu ở `GET /linh-can` →
  `giai[].color`). Đổi linh căn thì máy chủ gửi lại `add` của người đó cho mọi người đang nhìn thấy, và gửi
  `stats` cho chính người đó; `stats.stats` có `lc` và `lc_fx` (`docs/API.md`). Phiên bản giao thức không đổi.
- Kháng Mực Đan đang có hiệu lực làm Mặc Kích nhẹ đi ngay (máy chủ giữ hạn của bùa theo đồng hồ của vòng thế giới).

## Giai đoạn 9 — Tổ đội và bí cảnh (giao thức bản 5)

Client → server:

| `t` | Trường | Việc |
|---|---|---|
| `party` | `op`: `invite` (`name` = đạo hiệu) \| `accept` / `decline` (`uid` = người mời) \| `leave` \| `kick` (`uid`) \| `promote` (`uid`) | tổ đội, tối đa 5 người |
| `realm` | `op`: `enter` \| `queue` \| `unqueue` \| `leave`; `realm` (id bí cảnh định kỳ) hoặc `rift` (id khe nứt) | đội trưởng dẫn đội vào; người đi một mình vào hàng chờ; rời bí cảnh |
| `mark` | `x`, `y`, `i` (0–3) | ping cho đội, tối đa 1 lần/giây |
| `chat` | `ch: "party"` | kênh Tổ Đội |

Server → client:

- `{t: "party", event: "state", party{id, leader, max, members[{uid, name, realm, online, zone, hp, ghost, dead}]}}` khi có
  thay đổi (máu: tối đa 1 lần/giây); `event: "invite", from{uid, name, realm}`; `"invited", to{}`; `"declined", by{}`;
  `"left", reason: leave|kicked|disbanded|offline`.
- `{t: "party_xp", xp}`: Tu Vi chia từ đồng đội đánh quái gần đó.
- `{t: "notice", text}`: thông báo (bí cảnh sắp mở/đã mở, khe nứt vừa xuất hiện gần đây).
- `{t: "realm", event: ...}`:
  - `entering{realm, name_vi}`, `queued{key, realm, waiting}`, `unqueued` (ngoài bí cảnh);
  - `start{run{id, realm, name_vi, left (giây), math: true, rooms[{kind, name_vi}], members[{uid, name, in, floor}]}}`;
  - `room{i, n, kind, place, math, name_vi, how_vi, left, phase, puzzle}`: vào phòng (ngay sau `zone`). Mọi bí cảnh là
    bí cảnh toán (M10, xem API.md): phòng là `seal` (Trận Nhãn) hoặc `boss`;
  - `puzzle{i, puzzle}` khi đổi: `seal{seal_kind, seals[{name, broken, busy}], broken, need, missing[uid]}`, `boss{boss,
    hp, shield, phase, hits, need}`; loại nào cũng có `kind, solved, fails`;
  - `seal{ok, by}` sau mỗi câu của một ấn; `hint{code, text_vi}`;
  - `cleared{i, flawless, next_in}`; `loot{loot{stage: roomN|chest, stones, spirit_stones, items[], equipment[], jade?,
    immortal_jade?, fast?, xp?}}` (chỉ phần của người nhận); `member_left{uid, name, reason}`; `revived{hp}`;
  - `end{result: won|failed|timeout|abandoned, time, flawless, puzzles, fast, fragments, exit_in}`; `left` khi đã ra ngoài.
- `{t: "dead", ghost: 1}`: gục trong bí cảnh, thành hồn ma (không về làng).
- Snapshot: `me` có thêm phần tử thứ 9 (cờ hồn ma); thực thể người chơi có `gh`; khe nứt là thực thể `{id, k: "r", x, y,
  realm, n, left}` trong vùng quan tâm như quái.
- Hiệu ứng mới trong `fx`: `mark{by, x, y, i}`, `pz{e: solve|fail|ask|seal|open|wave, x, y, ...}`, `gshield{id, n, need,
  by}` (tiến độ khiên lớn của boss); `tele` có thêm `big: 1` cho Mặc Triều.
- Lỗi mới (`error.code`): `need_party`, `not_leader`, `party_full`, `already_in_party`, `player_offline`, `no_invite`,
  `party_self`, `cannot_enter`, `realm_closed`, `daily_limit`, `too_far`, `rift_gone`, `no_realm`, `in_party`,
  `not_in_realm`, `realm_error`.
- Rớt mạng trong bí cảnh: nhân vật chờ 60 giây. `welcome.zone = "bi_canh"` thì client vào lại bằng `join{via: "resume"}` và
  nhận lại `zone`, `realm start`, `realm room` (và `end` nếu đã xong). Vùng `bi_canh` không vào được bằng cổng hay `resume`
  khi nhân vật đã rời thế giới.

## Giai đoạn 10 — Lệnh quản trị (giao thức vẫn là bản 5)

Thêm, không đổi gì cũ (client cũ bỏ qua gói lạ), nên `PROTOCOL_VERSION` vẫn là 5.

- Tin `chat` có `text` bắt đầu bằng `/admin` (ở bất kỳ kênh nào) **không bao giờ được phát** cho ai. Máy chủ đọc cờ
  `is_admin` trong cơ sở dữ liệu (không tin cờ của phiên), chạy lệnh rồi trả `{t: "admin", ok, lines}` cho người gõ.
  Người không có quyền nhận `ok: false`. Lệnh của quản trị viên không bị giới hạn 2 giây/tin và vẫn chạy khi đang bị cấm chat.
- `/admin ban`: người bị khóa nhận `{t: "kicked", reason: "banned", message_vi}` rồi bị đóng với mã **4010**; kết nối lại
  nhận `error{code: "banned"}`. `/admin kick`: `reason: "admin"`, mã **4011**.
- `/admin mute`: người bị cấm nhận `notice` ngay; tin chat sau đó nhận `error{code: "chat_banned"}`.
- `/admin announce` và `/admin maintenance`: mọi người online nhận `{t: "notice", text, kind}`.
